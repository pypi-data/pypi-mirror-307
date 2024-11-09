# Kaziro Python API Client

Kaziro is a Python client for interacting with the Kaziro API. It provides a simple and intuitive interface for accessing various endpoints related to users, markets, orders, positions, and wallets.

## Quick Start

### Installation

Install the Kaziro package using pip:

```bash
pip install kaziro
```

### Basic Usage

```python
import os
from kaziro import Kaziro

# Initialize the Kaziro client
api_key = os.environ.get("KAZIRO_API_KEY")
kaziro = Kaziro(api_key=api_key)

# Retrieve user profile
user_profile = kaziro.user.retrieve()
print(f"User profile: {user_profile}")

# Retrieve markets
markets = kaziro.market.retrieve()
print(f"Markets: {markets}")

# Place an order
orders = [{"request_id": "some_id", "probability": 0.7}]
placed_orders = kaziro.order.create(orders)
print(f"Placed orders: {placed_orders}")

# Connect to WebSocket
kaziro.connect_websocket()
kaziro.subscribe_websocket("public:all")
print("WebSocket connected and subscribed to 'public:all'")
```

## Features

-   User management (retrieve)
-   Market operations (create, retrieve)
-   Order management (create, retrieve, accept)
-   Position tracking (open positions, history)
-   Wallet information retrieval
-   WebSocket support for real-time updates
-   Bot templates for automated trading

## Detailed Usage

### User Operations

```python
# Retrieve user profile
user_profile = kaziro.user.retrieve()
```

### Market Operations

```python
# Create a new market
market_details = [{"detail": "Market description", "size": 100}]
created_markets = kaziro.market.create(market_details)

# Retrieve markets
all_markets = kaziro.market.retrieve()
specific_markets = kaziro.market.retrieve(market_ids=["market_id_1", "market_id_2"])
open_markets = kaziro.market.retrieve(status="OPEN")
```

### Order Operations

```python
# Create orders
orders = [
    {"request_id": "id_1", "probability": 0.7},
    {"request_id": "id_2", "probability": 0.3}
]
placed_orders = kaziro.order.create(orders)

# Retrieve open orders
all_open_orders = kaziro.order.retrieve()
user_open_orders = kaziro.order.retrieve(filter_user=True)

# Accept orders
accepted_orders = kaziro.order.accept(["order_id_1", "order_id_2"])

# Request default replies
default_replies = kaziro.order.request_default_replies(["order_id_1", "order_id_2"])
```

### Position Operations

```python
# Get open positions
open_positions = kaziro.position.retrieve(status="ACTIVE")

# Get position history
position_history = kaziro.position.retrieve(status="CLOSED")
```

### Wallet Operations

```python
# Retrieve wallet information
wallet_info = kaziro.wallet.retrieve()
```

### WebSocket Usage

```python
# Connect to WebSocket
kaziro.connect_websocket()

# Subscribe to a channel
kaziro.subscribe_websocket("public:all")

```

### Bot Templates

```python
# Use the base market maker bot
kaziro.template.base_market_maker()
```

## Configuration

The Kaziro client can be configured with custom API and WebSocket URLs:

```python
kaziro = Kaziro(api_key="your_api_key")
```

## Development

To set up the development environment:

1. Clone the repository:

    ```
    git clone https://github.com/kazirocom/package.git
    cd package
    ```

2. Install development dependencies:

    ```
    pip install -e ".[dev]"
    ```

3. Run tests:
    ```
    pytest tests/
    ```

## Contributing

We welcome contributions to the Kaziro package. Please feel free to submit issues, fork the repository and send pull requests!

## License

This project is licensed under the terms of the license specified in the project repository.

## Support

For support, please contact the Kaziro team at support@kaziro.xyz or open an issue on the GitHub repository.
