from django.core.cache import cache

from . import webpage_pb2, webpage_pb2_grpc


def grpc_hook(server):
    webpage_pb2_grpc.add_ManageInstanceServicer_to_server(
        ManageInstanceServicer(), server
    )


class ManageInstanceServicer(webpage_pb2_grpc.ManageInstanceServicer):
    def ValidateToken(self, request, context):
        token = cache.get(request.token)
        if token:
            # Priject.object.get
            if request.commit:
                cache.set(token, "commit")
            return webpage_pb2.Project(name="ok")
        return webpage_pb2.Project(name="")
