from django.dispatch import receiver
from wagtail.blocks import RichTextBlock
from wagtail.core.signals import page_published
from wagtail.core.templatetags.wagtailcore_tags import richtext

import grpc

from say_wagtail.grpc import webpage_pb2_grpc
from say_wagtail.grpc import webpage_pb2
from .models import SimplePage


@receiver(page_published, sender=SimplePage)
def send_grpc_on_save(instance, **kwargs):
    with grpc.insecure_channel("localhost:5060") as channel:
        stub = webpage_pb2_grpc.PageStub(channel)
        val = ""
        for content in instance.body:
            if isinstance(content.block, RichTextBlock):
                val += str(richtext(content.value)) + "\n"
            else:
                val += content.value + "\n"
        telegram_actions = instance.page_telegramactions.all()
        if instance.first_published_at == instance.latest_revision_created_at:
            for action in telegram_actions:
                if action.publish_message:
                    response = stub.PublishSuperPage(
                        webpage_pb2.SuperPage(
                            chat_id=action.telegram_instance_chat_id,
                            id=instance.id,
                            body=val,
                        )
                    )
        else:
            for action in telegram_actions:
                response = stub.PublishSuperPage(
                    webpage_pb2.SuperPage(
                        chat_id=action.telegram_instance.chat_id,
                        id=instance.id,
                        body=val,
                        edit_originals=action.telegram_publish_mode.edit_past_messages,
                        reference_original=bool(
                            action.telegram_publish_mode.as_reference_to_original_message
                        ),
                    )
                )
        print("Greeter client received: " + response.message)
