# kaziro/__init__.py

from typing import Callable, List, Literal, Optional

import urllib3

from .api.generated.kaziro import ApiClient, Configuration
from .api.generated.kaziro.api import BrokerApi, ChatApi, MarketApi, OrderApi, PositionApi, UserApi, WalletApi
from .api.generated.kaziro.models import (
    AcceptOrdersRequest,
    AcceptOrdersResponse,
    BrokerChatCompletionMessage,
    BrokerChatCompletionResponse,
    BrokerMessageRequest,
    BrokerThreadCreateResponse,
    BrokerThreadMetadata,
    Chat,
    ChatCreationRequest,
    ChatRetrievalResponse,
    MarketCreationResponse,
    MarketDetail,
    MarketPriceHistoryResponse,
    MarketRetrievalResponse,
    OpenOrdersResponse,
    OrderPair,
    OrderRequest,
    PlaceOrderResponse,
    PositionResponse,
    RequestDefaultRepliesRequest,
    RequestDefaultRepliesResponse,
    UserRetrievalResponse,
    WalletInfoResponse,
)
from .template.base_replier import BaseReplierTemplate  # noqa: F401
from .websocket.client import KaziroWebSocket


class Kaziro:
    def __init__(self, api_key: str, api_url: str = "https://api.kaziro.xyz", ws_url: str = "wss://ws.kaziro.xyz", verbose: bool = False, verify_ssl: bool = True):
        self.api_key = api_key
        self.api_url = api_url
        self.ws_url = ws_url
        self.verbose = verbose
        self.verify_ssl = verify_ssl
        # Initialize Configuration and ApiClient
        self.config = Configuration(host=self.api_url, api_key={"APIKeyHeader": self.api_key})
        self.config.verify_ssl = verify_ssl
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.api_client = ApiClient(configuration=self.config)

        # Initialize API classes
        self.user = self.User(self.api_client)
        self.market = self.Market(self.api_client)
        self.order = self.Order(self.api_client)
        self.position = self.Position(self.api_client)
        self.wallet = self.Wallet(self.api_client)
        self.chat = self.Chat(self.api_client)
        self.broker = self.Broker(self.api_client)

        # Initialize WebSocket
        self.ws = KaziroWebSocket(self.ws_url, self.api_key, verbose=self.verbose, verify_ssl=self.verify_ssl)

    class User:
        def __init__(self, api_client: ApiClient):
            self.api = UserApi(api_client)

        def retrieve(self, user_ids: Optional[List[str]] = None, usernames: Optional[List[str]] = None) -> UserRetrievalResponse:
            return self.api.profile_retrieve_endpoint_v1_user_retrieve_get(user_ids, usernames)

    class Market:
        def __init__(self, api_client: ApiClient):
            self.api = MarketApi(api_client)

        def create(self, market_details: List[MarketDetail]) -> MarketCreationResponse:
            return self.api.create_market_endpoint_v1_exchange_market_create_post(market_details)

        def create_single(self, detail: str) -> MarketCreationResponse:
            market_detail = MarketDetail(detail=detail)
            response = self.api.create_market_endpoint_v1_exchange_market_create_post([market_detail])
            return response

        def retrieve(
            self,
            market_ids: Optional[List[str]] = None,
            statuses: Optional[List[str]] = None,
            tags: Optional[List[str]] = None,
            creator_id: Optional[str] = None,
            search_query: Optional[str] = None,
            sort_by: Optional[str] = None,
            sort_direction: Optional[str] = None,
            bucket: Optional[str] = None,
            page: Optional[int] = None,
        ) -> MarketRetrievalResponse:
            return self.api.retrieve_markets_endpoint_v1_exchange_market_retrieve_get(market_ids, statuses, tags, creator_id, search_query, sort_by, sort_direction, bucket, page)

        def retrieve_ohlc(self, market_ids: List[str]) -> MarketPriceHistoryResponse:
            return self.api.retrieve_ohlc_endpoint_v1_exchange_market_retrieve_ohlc_get(market_ids)

        def retrieve_ohlc_single(self, market_id: str) -> MarketPriceHistoryResponse:
            return self.api.retrieve_ohlc_endpoint_v1_exchange_market_retrieve_ohlc_get([market_id])

    class Order:
        def __init__(self, api_client: ApiClient):
            self.api = OrderApi(api_client)

        def create(self, orders: List[OrderRequest]) -> PlaceOrderResponse:
            return self.api.create_market_endpoint_v1_exchange_order_create_post(orders)

        def create_single_request(self, size: float, market_id: str, outcome: Literal[1, 2]) -> PlaceOrderResponse:
            order = OrderRequest(size=size, market_id=market_id, order_type="MARKET_REQUEST", outcome=outcome)
            return self.api.create_market_endpoint_v1_exchange_order_create_post([order])

        def create_single_reply(self, request_id: Optional[str], probability: float, outcome: Literal[1, 2]) -> PlaceOrderResponse:
            order = OrderRequest(request_id=request_id, probability=probability, order_type="MARKET_REPLY", outcome=outcome)
            return self.api.create_market_endpoint_v1_exchange_order_create_post([order])

        def retrieve(
            self,
            order_ids: Optional[List[str]] = None,
            market_ids: Optional[List[str]] = None,
            outcome: Optional[Literal[1, 2]] = None,
            filter_user: bool = False,
            include_markets: bool = False,
            include_creators: bool = False,
        ) -> OpenOrdersResponse:
            return self.api.get_open_orders_endpoint_v1_exchange_order_retrieve_get(order_ids, market_ids, outcome, filter_user, include_markets, include_creators)

        def accept(self, orders: List[OrderPair]) -> AcceptOrdersResponse:
            accept_orders_request = AcceptOrdersRequest(orders=orders)
            return self.api.accept_orders_endpoint_v1_exchange_order_accept_post(accept_orders_request)

        def accept_single(self, request_id: str, reply_id: str) -> AcceptOrdersResponse:
            order_pair = OrderPair(request_id=request_id, reply_id=reply_id)
            return self.accept([order_pair])

        def request_default_replies(self, order_ids: List[str]) -> RequestDefaultRepliesResponse:
            request_default_replies_request = RequestDefaultRepliesRequest(order_ids=order_ids)
            return self.api.request_default_replies_endpoint_v1_exchange_order_temporary_reply_post(request_default_replies_request)

        def request_default_reply_single(self, order_id: str) -> RequestDefaultRepliesResponse:
            return self.request_default_replies([order_id])

    class Position:
        def __init__(self, api_client: ApiClient):
            self.api = PositionApi(api_client)

        def retrieve(
            self, status: Optional[str] = None, page: Optional[int] = None, sort_order: Optional[str] = None, include_markets: bool = False, include_orders: bool = False
        ) -> PositionResponse:
            return self.api.get_positions_v1_exchange_position_retrieve_get(status=status, page=page, sort_order=sort_order, include_markets=include_markets, include_orders=include_orders)

    class Wallet:
        def __init__(self, api_client: ApiClient):
            self.api = WalletApi(api_client)

        def retrieve(self) -> WalletInfoResponse:
            return self.api.wallet_info_endpoint_v1_wallet_retrieve_get()

    class Chat:
        def __init__(self, api_client: ApiClient):
            self.api = ChatApi(api_client)

        def create(self, content: str, market_id: Optional[str] = None) -> Chat:
            """Create a new chat message.

            Args:
                content: The content of the chat message
                market_id: Optional market ID to associate with the message

            Returns:
                Chat: The created chat message
            """
            chat_request = ChatCreationRequest(content=content, market_id=market_id)
            return self.api.create_chat_message_endpoint_v1_exchange_chat_create_post(chat_request)

        def retrieve(
            self,
            market_id: Optional[str] = None,
            order_id: Optional[str] = None,
            user_id: Optional[str] = None,
            is_global: Optional[bool] = None,
            limit: Optional[int] = None,
            before_date: Optional[str] = None,
            include_market: Optional[bool] = None,
        ) -> ChatRetrievalResponse:
            """Retrieve chat messages with optional filters.

            Args:
                market_id: Filter by market ID
                order_id: Filter by order ID
                user_id: Filter by user ID
                is_global: Filter by global status
                limit: Maximum number of messages to return (max 100)
                before_date: Return messages before this date
                include_market: Include full market data in response

            Returns:
                ChatRetrievalResponse: The retrieved chat messages
            """
            return self.api.retrieve_chat_messages_endpoint_v1_exchange_chat_retrieve_get(
                market_id=market_id, order_id=order_id, user_id=user_id, is_global=is_global, limit=limit, before_date=before_date, include_market=include_market
            )

    class Broker:
        def __init__(self, api_client: ApiClient):
            self.api = BrokerApi(api_client)

        def create_chat_completion(self, message: str, thread_id: Optional[str] = None) -> BrokerChatCompletionResponse:
            """Create a chat completion with the broker.

            Args:
                messages: List of message objects with 'role' and 'content'
                thread_id: Optional thread ID for continuing a conversation

            Returns:
                BrokerChatCompletionResponse: The broker's response
            """
            broker_message = BrokerChatCompletionMessage(role="user", content=message)
            request = BrokerMessageRequest(messages=[broker_message], thread_id=thread_id, model="kaziro-broker")
            return self.api.create_chat_message_endpoint_v1_broker_chat_completions_post(request)

        def get_thread_metadata(self, thread_id: str) -> BrokerThreadMetadata:
            """Retrieve metadata for a specific thread.

            Args:
                thread_id: The ID of the thread to retrieve

            Returns:
                ThreadMetadata: The thread's metadata
            """
            return self.api.get_thread_metadata_endpoint_v1_broker_thread_retrieve_get(thread_id)

        def create_thread(self) -> BrokerThreadCreateResponse:
            """Create a new conversation thread.

            Returns:
                ThreadCreateResponse: Contains the new thread ID
            """
            return self.api.create_thread_endpoint_v1_broker_thread_create_post()

    def connect_websocket(self):
        self.ws.connect()

    def subscribe_websocket(self, channel: str):
        self.ws.subscribe(channel)

    def set_websocket_callback(self, callback: Callable[[str], None]):
        self.ws.set_message_callback(callback)


__all__ = ["Kaziro"]
