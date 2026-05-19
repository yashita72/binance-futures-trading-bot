import argparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bot.orders import place_order
from bot.validators import (
    validate_side,
    validate_order_type
)

console = Console()


def main():

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT)"
    )

    parser.add_argument(
        "--side",
        required=True,
        help="BUY or SELL"
    )

    parser.add_argument(
        "--type",
        required=True,
        help="MARKET or LIMIT"
    )

    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity"
    )

    parser.add_argument(
        "--price",
        type=float,
        help="Price required for LIMIT orders"
    )

    args = parser.parse_args()

    try:

        side = validate_side(args.side)
        order_type = validate_order_type(args.type)

        if args.quantity <= 0:
            raise ValueError(
                "Quantity must be greater than 0"
            )

        if order_type == "LIMIT" and not args.price:
            raise ValueError(
                "Price is required for LIMIT orders"
            )

        console.print(
            Panel.fit(
                "[bold cyan]ORDER REQUEST[/bold cyan]"
            )
        )

        request_table = Table(show_header=True)

        request_table.add_column("Field")
        request_table.add_column("Value")

        request_table.add_row("Symbol", args.symbol)
        request_table.add_row("Side", side)
        request_table.add_row("Order Type", order_type)
        request_table.add_row("Quantity", str(args.quantity))

        if args.price:
            request_table.add_row(
                "Price",
                str(args.price)
            )

        console.print(request_table)

        response = place_order(
            symbol=args.symbol,
            side=side,
            order_type=order_type,
            quantity=args.quantity,
            price=args.price
        )

        console.print(
            Panel.fit(
                "[bold green]ORDER RESPONSE[/bold green]"
            )
        )

        response_table = Table(show_header=True)

        response_table.add_column("Field")
        response_table.add_column("Value")

        response_table.add_row(
            "Order ID",
            str(response.get("orderId"))
        )

        response_table.add_row(
            "Status",
            str(response.get("status"))
        )

        response_table.add_row(
            "Executed Qty",
            str(response.get("executedQty"))
        )

        response_table.add_row(
            "Average Price",
            str(response.get("avgPrice"))
        )

        console.print(response_table)

        console.print(
            "\n[bold green]Order placed successfully![/bold green]"
        )

    except Exception as e:

        console.print(
            f"\n[bold red]Error:[/bold red] {str(e)}"
        )


if __name__ == "__main__":
    main()