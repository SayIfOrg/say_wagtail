# from . import helloworld_pb2
# from . import helloworld_pb2_grpc
#
#
# def grpc_hook(server):
#     helloworld_pb2_grpc.add_GreeterServicer_to_server(MYServicer(), server)
#
#
# class MYServicer(helloworld_pb2_grpc.GreeterServicer):
#     def SayHello(self, request, context):
#         response = helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)
#         return response
