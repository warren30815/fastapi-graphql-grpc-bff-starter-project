import grpc
import logging

class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        if handler is None:
            return None

        def log_unary_unary(request, context):
            logging.info(f"gRPC call: {handler_call_details.method} | request: {request}")
            response = handler.unary_unary(request, context)
            logging.info(f"gRPC response: {handler_call_details.method} | response: {response}")
            return response

        def log_unary_stream(request, context):
            logging.info(f"gRPC call: {handler_call_details.method} | request: {request}")
            for resp in handler.unary_stream(request, context):
                logging.info(f"gRPC stream response: {handler_call_details.method} | response: {resp}")
                yield resp

        def log_stream_unary(request_iterator, context):
            logging.info(f"gRPC call: {handler_call_details.method} | streaming request")
            response = handler.stream_unary(request_iterator, context)
            logging.info(f"gRPC response: {handler_call_details.method} | response: {response}")
            return response

        def log_stream_stream(request_iterator, context):
            logging.info(f"gRPC call: {handler_call_details.method} | streaming request")
            for resp in handler.stream_stream(request_iterator, context):
                logging.info(f"gRPC stream response: {handler_call_details.method} | response: {resp}")
                yield resp

        if handler.unary_unary:
            return grpc.unary_unary_rpc_method_handler(
                log_unary_unary,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        if handler.unary_stream:
            return grpc.unary_stream_rpc_method_handler(
                log_unary_stream,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        if handler.stream_unary:
            return grpc.stream_unary_rpc_method_handler(
                log_stream_unary,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        if handler.stream_stream:
            return grpc.stream_stream_rpc_method_handler(
                log_stream_stream,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )
        return handler
