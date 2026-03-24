"""
Simple client for order API testing

It supports:
    - list-orders
    - get-order <order_id>
    - create-order --user-id ... --product-name ... --quantity ...
    - update-order <order_id> --product-name ... --quantity ... --status ...
    - delete-order <order_id>

Example usage with your existing users:
    - uv run rest/order_client.py create-order --user-id 1 --product-name Laptop --quantity 1
    - uv run rest/order_client.py create-order --user-id 2 --product-name Keyboard --quantity 2
    - uv run rest/order_client.py list-orders
    - uv run rest/order_client.py get-order 1
    - uv run rest/order_client.py update-order 1 --status shipped
    - uv run rest/order_client.py delete-order 1
"""

import argparse
import json
from urllib import error, request


DEFAULT_BASE_URL = "http://127.0.0.1:8000/api/v1"


def send_request(
    method: str,
    path: str,
    *,
    base_url: str,
    payload: dict | None = None,
) -> None:
    url = f"{base_url}{path}"
    data = None
    headers = {}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = request.Request(url, data=data, headers=headers, method=method)

    try:
        with request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            print(f"Status: {response.status}")
            print(body if body else "<empty>")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        print(f"Status: {exc.code}")
        print(body if body else "<empty>")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple client for order API testing")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-orders")

    get_order = subparsers.add_parser("get-order")
    get_order.add_argument("order_id", type=int)

    create_order = subparsers.add_parser("create-order")
    create_order.add_argument("--user-id", type=int, required=True)
    create_order.add_argument("--product-name", required=True)
    create_order.add_argument("--quantity", type=int, default=1)

    update_order = subparsers.add_parser("update-order")
    update_order.add_argument("order_id", type=int)
    update_order.add_argument("--product-name")
    update_order.add_argument("--quantity", type=int)
    update_order.add_argument("--status")

    delete_order = subparsers.add_parser("delete-order")
    delete_order.add_argument("order_id", type=int)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list-orders":
        send_request("GET", "/orders", base_url=args.base_url)
    elif args.command == "get-order":
        send_request("GET", f"/orders/{args.order_id}", base_url=args.base_url)
    elif args.command == "create-order":
        send_request(
            "POST",
            "/orders",
            base_url=args.base_url,
            payload={
                "user_id": args.user_id,
                "product_name": args.product_name,
                "quantity": args.quantity,
            },
        )
    elif args.command == "update-order":
        payload = {}
        if args.product_name is not None:
            payload["product_name"] = args.product_name
        if args.quantity is not None:
            payload["quantity"] = args.quantity
        if args.status is not None:
            payload["status"] = args.status

        send_request(
            "PATCH",
            f"/orders/{args.order_id}",
            base_url=args.base_url,
            payload=payload,
        )
    elif args.command == "delete-order":
        send_request("DELETE", f"/orders/{args.order_id}", base_url=args.base_url)


if __name__ == "__main__":
    main()
