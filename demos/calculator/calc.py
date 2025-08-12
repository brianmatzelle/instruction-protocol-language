#!/usr/bin/env python3
import argparse
import json
import math
import sys


def calculate(operation: str, left: float, right: float) -> float:
    if operation == "add":
        return left + right
    if operation == "sub":
        return left - right
    if operation == "mul":
        return left * right
    if operation == "div":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        return left / right
    raise ValueError(f"unsupported operation: {operation}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculator backend")
    parser.add_argument("--op", required=True, choices=["add", "sub", "mul", "div"], help="operation")
    parser.add_argument("--a", required=True, type=float, help="left operand")
    parser.add_argument("--b", required=True, type=float, help="right operand")
    args = parser.parse_args()

    try:
        result = calculate(args.op, args.a, args.b)
        if not math.isfinite(result):
            raise ArithmeticError("non-finite result")
        print(json.dumps({
            "op": args.op,
            "a": args.a,
            "b": args.b,
            "result": result
        }))
        return 0
    except ZeroDivisionError:
        print(json.dumps({"error": "DIVIDE_BY_ZERO", "code": "DIVIDE_BY_ZERO"}))
        return 2
    except ValueError as e:
        print(json.dumps({"error": str(e), "code": "INVALID_OPERATION"}))
        return 3
    except Exception as e:
        print(json.dumps({"error": str(e), "code": "INTERNAL_ERROR"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
