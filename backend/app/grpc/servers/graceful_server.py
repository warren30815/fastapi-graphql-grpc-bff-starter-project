import signal
import threading
import logging

class GracefulGRPCServer:
    def __init__(self, server, name="gRPC server"):
        self.server = server
        self.name = name
        self.stop_event = threading.Event()

    def _handle_sigterm(self, *_):
        logging.info(f"Received termination signal, shutting down {self.name} gracefully...")
        self.stop_event.set()
        self.server.stop(grace=None)

    def start_and_wait(self):
        self.server.start()
        signal.signal(signal.SIGINT, self._handle_sigterm)
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        self.stop_event.wait()
        logging.info(f"{self.name} stopped.")
