# kaziro/templates/bots.py
import json
import time
from typing import Literal


class BaseReplierTemplate:
    def __init__(self, kaziro):
        print("Initializing BaseReplierTemplate...")
        self.kaziro = kaziro
        self.wallet = self.kaziro.wallet.retrieve().wallets[0]
        print(f"Wallet Balance: {self.wallet.balance}")

    def start(self):
        print("Starting BaseReplierTemplate...")

        def on_message(message: str):
            data = json.loads(message)
            if data.get("event_type") == "order_created":
                order = data.get("data", {}).get("order", {})
                if order.get("order_type") == "MARKET_REPLY":
                    print("Market reply order detected...")
                    request_id = order.get("request_id")
                    probability = order.get("probability")
                    initializer = order.get("initializer")
                    outcome = order.get("outcome")
                    size = order.get("size")
                    if request_id and probability is not None and initializer and size:
                        new_probability = max(0.02, probability - 0.01)
                        if validate_balance(probability, new_probability, size):
                            if validate_request(request_id):
                                create_order(request_id, new_probability, outcome)
                            else:
                                print("Request validation failed")
                        else:
                            print("Balance validation failed")
                    else:
                        # print("Missing required order details")
                        pass
                else:
                    # print(f"Non-market reply order type: {order.get('order_type')}")
                    pass
            else:
                # print(f"Non-order created event type: {data.get('event_type')}")
                pass

        def validate_balance(existing_probability: float, new_probability: float, size: float, allowed_risk: float = 0.3):
            implied_request_size = round(size / (1 - existing_probability) - size, 2)
            expected_reply_size = round((1 / new_probability) * implied_request_size - implied_request_size, 2)
            # Get realtime balance
            current_balance = self.kaziro.wallet.retrieve().wallets[0].balance
            if (current_balance * allowed_risk) < expected_reply_size:
                print(f"Insufficient balance for allowed risk. Max allowed risk: {current_balance * allowed_risk}")
                return False
            return True

        def validate_request(request_id: str):
            print(f"Validating request: request_id={request_id}")
            response = self.kaziro.order.retrieve(order_ids=[request_id])
            if response.success and response.orders:
                request = response.orders[0]
                if request.wallet_id == self.wallet.id:
                    print("Cannot reply to own request")
                    return False
                return True
            else:
                print(f"Failed to retrieve request or no orders found: {response}")
                return False

        def create_order(request_id: str, probability: float, outcome: Literal[1, 2]):
            try:
                response = self.kaziro.order.create_single_reply(request_id=request_id, probability=probability, outcome=outcome)
                print(f"Order created successfully: {response}")
            except Exception as e:
                print(f"Error creating order: {str(e)}")
                print(f"Error type: {type(e).__name__}")

        self.kaziro.set_websocket_callback(on_message)
        self.kaziro.connect_websocket()
        self.kaziro.subscribe_websocket("public:all")
        print("Market Maker Bot started. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Bot stopped.")
