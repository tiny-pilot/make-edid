# Make EDID

## Format hex EDID

```bash
. venv/bin/activate
echo "someedid" | ./app/main.py
```

## Format binary EDID

```bash
. venv/bin/activate
./app/main.py -b -i edid.bin
```
