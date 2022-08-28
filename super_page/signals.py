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
        # response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
        val = ""
        for content in instance.body:
            if isinstance(content.block, RichTextBlock):
                val += str(richtext(content.value)) + "\n"
            else:
                val += content.value + "\n"
        if instance.first_published_at == instance.latest_revision_created_at:
            response = stub.PublishSuperPage(
                webpage_pb2.SuperPage(id=instance.id, body=val)
            )
        else:
            response = stub.PublishSuperPage(
                webpage_pb2.SuperPage(
                    id=instance.id,
                    body=val,
                    edit_originals=True,
                    reference_original=True,
                )
            )
        print("Greeter client received: " + response.message)
