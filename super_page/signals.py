from django.dispatch import receiver
from wagtail.blocks import RichTextBlock
from wagtail.core.signals import page_published
from wagtail.core.templatetags.wagtailcore_tags import richtext

import grpc

from say_wagtail.grpc import helloworld_pb2_grpc
from say_wagtail.grpc import helloworld_pb2
from .models import SimplePage


@receiver(page_published, sender=SimplePage)
def send_grpc_on_save(instance, **kwargs):
    with grpc.insecure_channel("localhost:5060") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        # response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
        val = ""
        for content in instance.body:
            if isinstance(content.block, RichTextBlock):
                val += str(richtext(content.value)) + "\n"
            else:
                val += content.value + "\n"
        response = stub.PublishRichText(helloworld_pb2.RichText(body=val))
        print("Greeter client received: " + response.message)
