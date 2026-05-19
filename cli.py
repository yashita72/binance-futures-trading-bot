import argparse

from bot.orders import place_order
from bot.validators import (
    validate_side,
    validate_order_type
)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    try:

        side = validate_side(args.side)
        order_type = validate_order_type(args.type)

        if order_type == "LIMIT" and not args.price:
            raise ValueError(
                "Price is required for LIMIT orders"
            )

        print("\n=== ORDER REQUEST ===")
        print(f"Symbol: {args.symbol}")
        print(f"Side: {side}")
        print(f"Type: {order_type}")
        print(f"Quantity: {args.quantity}")

        if args.price:
            print(f"Price: {args.price}")

        response = place_order(
            symbol=args.symbol,
            side=side,
            order_type=order_type,
            quantity=args.quantity,
            price=args.price
        )

        print("\n=== ORDER RESPONSE ===")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")

        if response.get("avgPrice"):
            print(f"Average Price: {response.get('avgPrice')}")

        print("\nOrder placed successfully!")

    except Exception as e:

        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()