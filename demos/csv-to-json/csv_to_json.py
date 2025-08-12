#!/usr/bin/env python3
import csv, json, sys, argparse, itertools

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--path', help='CSV file path (optional). If omitted, read stdin')
    p.add_argument('--limit', type=int, help='max rows to read (excluding header)')
    p.add_argument('--out', dest='out_path', help='optional output JSON file path')
    args = p.parse_args()

    if args.path:
        f = open(args.path, 'r', newline='', encoding='utf-8')
        close_f = True
    else:
        f = sys.stdin
        close_f = False

    try:
        reader = csv.DictReader(f)
        rows = list(reader)
        if args.limit is not None:
            rows = rows[: args.limit]
        payload = {
            'items': rows,
            'count': len(rows)
        }
        text = json.dumps(payload)
        if args.out_path:
            with open(args.out_path, 'w', encoding='utf-8') as out_f:
                out_f.write(text)
        print(text)
    finally:
        if close_f:
            f.close()

if __name__ == '__main__':
    main()
