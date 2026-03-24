"""
Example usage:

python rest/client.py health
python rest/client.py list-users
python rest/client.py create-user --name Alice --email alice@example.com
python rest/client.py get-user 1

python rest/client.py update-user 1 --name "Alice Updated"
python rest/client.py update-user 1 --email "alice.new@example.com"
python rest/client.py update-user 1 --inactive
python rest/client.py update-user 1 --name "Alice" --email "alice@example.com" --active

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
    parser = argparse.ArgumentParser(description="Simple client for the REST simulation API")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health")
    subparsers.add_parser("list-users")

    get_user = subparsers.add_parser("get-user")
    get_user.add_argument("user_id", type=int)

    create_user = subparsers.add_parser("create-user")
    create_user.add_argument("--name", required=True)
    create_user.add_argument("--email", required=True)
    create_user.add_argument("--inactive", action="store_true")

    update_user = subparsers.add_parser("update-user")
    update_user.add_argument("user_id", type=int)
    update_user.add_argument("--name")
    update_user.add_argument("--email")
    update_user.add_argument("--active", action="store_true")
    update_user.add_argument("--inactive", action="store_true")

    delete_user = subparsers.add_parser("delete-user")
    delete_user.add_argument("user_id", type=int)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "health":
        send_request("GET", "/health", base_url=args.base_url)
    elif args.command == "list-users":
        send_request("GET", "/users", base_url=args.base_url)
    elif args.command == "get-user":
        send_request("GET", f"/users/{args.user_id}", base_url=args.base_url)
    elif args.command == "create-user":
        send_request(
            "POST",
            "/users",
            base_url=args.base_url,
            payload={
                "name": args.name,
                "email": args.email,
                "is_active": not args.inactive,
            },
        )
    elif args.command == "update-user":
        payload = {}
        if args.name is not None:
            payload["name"] = args.name
        if args.email is not None:
            payload["email"] = args.email
        if args.active:
            payload["is_active"] = True
        if args.inactive:
            payload["is_active"] = False

        send_request(
            "PATCH",
            f"/users/{args.user_id}",
            base_url=args.base_url,
            payload=payload,
        )
    elif args.command == "delete-user":
        send_request("DELETE", f"/users/{args.user_id}", base_url=args.base_url)


if __name__ == "__main__":
    main()
