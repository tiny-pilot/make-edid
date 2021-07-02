# Make EDID

## Format hex EDID

```bash
. venv/bin/activate
echo "someedid" | ./app/main.py
```

## Format binary EDID

```bash
. venv/bin/activate
./app/main.py -i edid.bin
```
