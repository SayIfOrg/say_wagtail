from django.dispatch import receiver
from wagtail.core.signals import page_published

from say_wagtail.grpc import helloworld_pb2_grpc
from say_wagtail.grpc import helloworld_pb2
import grpc

from .models import SimplePage


@receiver(page_published, sender=SimplePage)
def send_grpc_on_save(instance, **kwargs):
    with grpc.insecure_channel("localhost:5060") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        # response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
        response = stub.PublishRichText(helloworld_pb2.RichText(body="\n".join([str(i.value) for i in instance.body])))
        print("Greeter client received: " + response.message)
