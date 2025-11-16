# QR Code Generator — Usage

Generate a QR code image from text or a URL using Python.

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Examples:

Interactive (prompted):

```bash
python qr-code-generator.py
```

Single argument:

```bash
python qr-code-generator.py "https://example.com" -o example.png
```

Read from stdin:

```bash
echo "Hello world" | python qr-code-generator.py - -o hello.png
```

Options:

- `-o, --output` : Output filename (default `qrcode.png`). If no extension is provided, `.png` is appended.
- `--box-size` : Size of each QR module in pixels (default `10`).
- `--border` : Border size in modules (default `4`).
- `--fill-color` / `--back-color` : Colors for the QR code (default `black` on `white`).
- `--error-correction` : Error correction level: `L`, `M`, `Q`, or `H` (default `M`).


## Usage

Interactive (prompted):

```bash
python qr-code-generator.py
```

Single argument and save to file:

```bash
python qr-code-generator.py "https://example.com" -o example.png
```

Read input from stdin:

```bash
echo "Hello world" | python qr-code-generator.py - -o hello.png
```


Options:

- `-o, --output` : Output filename (default `qrcode.png`). If no extension is provided, `.png` is appended.
- `--box-size` : Size of each QR module in pixels (default `10`). Smaller values produce more dense/compact codes, larger values create blockier, easy-to-scan images.
- `--border` : Border size in modules (default `4`). Increasing the border adds white space around the QR which can help some scanners.
- `--fill-color` / `--back-color` : Colors for the QR code (default `black` on `white`). You can create inverted or colorful QR codes (e.g., `--fill-color white --back-color black` for inverted, or `--fill-color blue --back-color yellow` for colored output).
- `--error-correction` : Error correction level: `L`, `M`, `Q`, or `H` (default `M`). Higher levels (e.g., `H`) allow the QR to be partially damaged or have a logo overlayed while remaining scannable, but increase the density of the code.

Examples and visual notes:

- Smaller modules (dense): `--box-size 4` → more data per area, look: fine-grained, more complex pattern. Use when you need smaller physical size.
- Larger modules (blocky): `--box-size 20` → large square pixels, easy to print and scan from a distance.
- Thin border: `--border 2` → small white margin. Some scanners may require at least 4 modules of quiet zone; use default unless you know the target scanner.
- Thick border: `--border 10` → lots of white padding, useful for framing or overlaying on busy backgrounds.
- Inverted: `--fill-color white --back-color black` → white QR on black background; still scannable by many apps but test on target devices.
- Colored: `--fill-color blue --back-color yellow` → visually distinctive; ensure sufficient contrast for scanners.
- High error correction: `--error-correction H` → useful when you plan to place a logo over the center or expect damage; visual density increases.

Sample commands that produce different looks:

```bash
# Dense, small size
python qr-code-generator.py "https://example.com" --box-size 4 -o generated_png/qr_small.png

# Large blocky modules for printing
python qr-code-generator.py "https://example.com" --box-size 20 -o generated_png/qr_large.png

# Colored QR
python qr-code-generator.py "https://example.com" --fill-color blue --back-color yellow -o generated_png/qr_colored.png

# High resiliency for logos or damage
python qr-code-generator.py "https://example.com" --error-correction H -o generated_png/qr_resilient.png
```