import grpc
from typing import Optional, Callable, Any, Type
from abc import ABC, abstractmethod
import weakref
import logging
import asyncio

logger = logging.getLogger(__name__)


class GrpcClientError(Exception):
    """Base exception for gRPC client errors"""
    pass


class ConnectionError(GrpcClientError):
    """Raised when connection fails"""
    pass


class MethodNotFoundError(GrpcClientError):
    """Raised when gRPC method not found"""
    pass


class BaseGrpcClient(ABC):
    _instances = weakref.WeakSet()

    @property
    @abstractmethod
    def stub_class(self) -> Type:
        """Subclasses must implement: return the gRPC stub class"""
        pass

    @abstractmethod
    def protobuf_to_model(self, proto_obj: Any) -> Any:
        """Subclasses must implement: convert proto message to domain model"""
        pass

    def __init__(self, host: str, port: int, **channel_options):
        self.host = host
        self.port = port
        self.channel_options = channel_options
        self.channel: Optional[grpc.aio.Channel] = None
        self.stub: Optional[Any] = None
        self._instances.add(self)

    @property
    def address(self) -> str:
        """Returns the full address string"""
        return f"{self.host}:{self.port}"

    @property
    def is_connected(self) -> bool:
        """Check if client is connected and channel is ready"""
        return (
            self.channel is not None
            and self.stub is not None
            and self.channel.get_state() not in [
                grpc.ChannelConnectivity.SHUTDOWN,
                grpc.ChannelConnectivity.TRANSIENT_FAILURE
            ]
        )

    async def connect(self):
        """Establish connection to gRPC server"""
        try:
            # Close existing connection if it's in bad state
            if self.channel and self.channel.get_state() == grpc.ChannelConnectivity.SHUTDOWN:
                await self.close()

            # Create new connection if needed
            if not self.channel:
                self.channel = grpc.aio.insecure_channel(
                    self.address,
                    options=list(self.channel_options.items()) if self.channel_options else None
                )
                logger.debug(f"Created new gRPC channel to {self.address}")

            # Create stub if needed
            if not self.stub:
                self.stub = self.stub_class(self.channel)
                logger.debug(f"Created gRPC stub for {self.address}")

        except Exception as e:
            logger.error(f"Failed to connect to gRPC server {self.address}: {e}")
            raise ConnectionError(f"Failed to connect to {self.address}: {e}") from e

    async def close(self):
        """Close the gRPC connection"""
        if self.channel:
            try:
                await self.channel.close()
                logger.debug(f"Closed gRPC channel to {self.address}")
            except Exception as e:
                logger.warning(f"Error closing channel to {self.address}: {e}")
            finally:
                self.channel = None
                self.stub = None

    async def _ensure_connected(self):
        """Ensures the channel and stub are initialized and connected"""
        if not self.is_connected:
            await self.connect()

    async def _call(
        self,
        method_name: str,
        request: Any,
        to_model: Optional[Callable] = None,
        timeout: Optional[float] = None
    ):
        """
        Unified gRPC call helper

        Args:
            method_name: Name of the gRPC method to call
            request: Request message
            to_model: Optional function to convert response to domain model
            timeout: Optional timeout in seconds

        Returns:
            Response message or converted model

        Raises:
            ConnectionError: If connection fails
            MethodNotFoundError: If method doesn't exist
            grpc.RpcError: For gRPC specific errors
        """
        try:
            await self._ensure_connected()

            # Get the method from stub
            if not hasattr(self.stub, method_name):
                raise MethodNotFoundError(f"Method '{method_name}' not found in stub")

            method = getattr(self.stub, method_name)

            # Make the gRPC call
            response = await method(request, timeout=timeout)

            # Convert response if converter provided
            if to_model:
                return to_model(response)
            return response

        except grpc.RpcError as e:
            logger.error(f"gRPC call failed for {method_name}: {e.code()}: {e.details()}")
            raise
        except (ConnectionError, MethodNotFoundError):
            raise
        except Exception as e:
            logger.error(f"Unexpected error in gRPC call {method_name}: {e}")
            raise GrpcClientError(f"Unexpected error in {method_name}: {e}") from e

    async def call_with_model(
        self,
        method_name: str,
        request: Any,
        timeout: Optional[float] = None
    ):
        """
        Call gRPC method and automatically convert response to domain model

        Args:
            method_name: Name of the gRPC method to call
            request: Request message
            timeout: Optional timeout in seconds

        Returns:
            Converted domain model
        """
        return await self._call(
            method_name,
            request,
            to_model=self.protobuf_to_model,
            timeout=timeout
        )

    async def call_raw(
        self,
        method_name: str,
        request: Any,
        timeout: Optional[float] = None
    ):
        """
        Call gRPC method and return raw protobuf response

        Args:
            method_name: Name of the gRPC method to call
            request: Request message
            timeout: Optional timeout in seconds

        Returns:
            Raw protobuf response
        """
        return await self._call(method_name, request, timeout=timeout)

    async def health_check(self, timeout: float = 5.0) -> bool:
        """
        Check if the gRPC server is healthy

        Args:
            timeout: Timeout in seconds

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            await self._ensure_connected()
            # Try to get channel state with timeout
            try:
                await asyncio.wait_for(
                    asyncio.to_thread(self.channel.get_state, True),
                    timeout=timeout
                )
                state = self.channel.get_state(try_to_connect=True)
            except asyncio.TimeoutError:
                logger.warning(f"Health check timed out for {self.address}")
                return False
            return state == grpc.ChannelConnectivity.READY
        except Exception as e:
            logger.warning(f"Health check failed for {self.address}: {e}")
            return False

    @classmethod
    async def cleanup_all(cls):
        """Clean up all client instances"""
        instances = list(cls._instances)
        logger.info(f"Cleaning up {len(instances)} gRPC client instances")

        for instance in instances:
            try:
                await instance.close()
            except Exception as e:
                logger.warning(f"Error cleaning up instance {instance.address}: {e}")

    def __repr__(self) -> str:
        status = "connected" if self.is_connected else "disconnected"
        return f"{self.__class__.__name__}({self.address}, {status})"
