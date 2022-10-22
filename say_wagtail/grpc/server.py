from django.core.cache import cache

from . import webpage_pb2, webpage_pb2_grpc


def grpc_hook(server):
    webpage_pb2_grpc.add_ManageInstanceServicer_to_server(
        ManageInstanceServicer(), server
    )


class ManageInstanceServicer(webpage_pb2_grpc.ManageInstanceServicer):
    def ValidateToken(self, request, context):
        project_id = cache.get(request.token)
        if project_id:
            if request.commit:
                cache.set(request.token, "commit")
            return webpage_pb2.Project(name="ok", id=project_id)
        return webpage_pb2.Project()
