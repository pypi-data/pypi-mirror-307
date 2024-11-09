# kaziro/custom/websocket.py
import json
import ssl
import threading
from typing import Callable, Optional

from websocket import WebSocketApp

from ..util.logging import log


class KaziroWebSocket:
    def __init__(self, ws_url: str, api_key: str, verbose: bool = False, verify_ssl: bool = True):
        self.ws_url = ws_url
        self.api_key = api_key
        self.ws: Optional[WebSocketApp] = None
        self.verify_ssl = verify_ssl
        self.connected = False
        self.verbose = verbose
        self.message_callback: Optional[Callable[[str], None]] = None

    def connect(self):
        log("Connecting to WebSocket", verbose=self.verbose)

        if not self.verify_ssl:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        self.ws = WebSocketApp(
            self.ws_url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            header={"Kaziro-API-Key": self.api_key},
        )

        if not self.verify_ssl:
            wst = threading.Thread(target=self.ws.run_forever, kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}})
        else:
            wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def _on_open(self, ws):
        log("WebSocket connection opened", verbose=self.verbose)
        self.connected = True
        self.subscribe("public:all")

    def _on_message(self, ws, message):
        log(f"Received message: {message}", verbose=self.verbose)
        if self.message_callback:
            self.message_callback(message)

    def _on_error(self, ws, error):
        log(f"WebSocket error: {error}", verbose=self.verbose)

    def _on_close(self, ws, close_status_code, close_msg):
        log("WebSocket connection closed", verbose=self.verbose)
        self.connected = False

    def subscribe(self, channel):
        if self.connected and self.ws:
            self.ws.send(json.dumps({"type": "subscribe", "channel": channel}))
        else:
            log("WebSocket is not connected. Please connect first.", verbose=self.verbose)

    def send(self, message):
        if self.connected and self.ws:
            self.ws.send(json.dumps(message))
        else:
            log("WebSocket is not connected. Please connect first.", verbose=self.verbose)

    def set_message_callback(self, callback: Callable[[str], None]):
        self.message_callback = callback
