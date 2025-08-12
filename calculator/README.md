# Calculator (undefined framework)

- Entry: `_MAIN.un`
- Backend: `calc.py` (Python 3)

Run backend directly:

```bash
python3 calc.py --op add --a 2 --b 3
```

Example `_MAIN.un` flow:
- Step 1 sets `{ op, a, b }`
- Step 2 calls backend and returns `{ op, a, b, result }`
- Step 3 reports the final result
