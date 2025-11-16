# QR Code Generator

Generate a QR code image from text or a URL using Python.

## Quick start

1. Clone the repository (if you haven't already):

```bash
git clone https://github.com/predrag-milanovic/qr-code-generator-py.git
cd qr-code-generator-py
```

2. (Optional but recommended) Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```


4. Create the output directory that will hold generated PNGs:

```bash
mkdir -p generated_png
```

5. Run the script interactively to generate a QR code:

```bash
python qr-code-generator.py
```

6. Or run with a single argument and save to a file:

```bash
python qr-code-generator.py "https://example.com" -o example.png
```

Note: if you provide only a filename (no directory) the script will save
generated PNG files into the `generated_png/` directory by default. The
directory is created automatically if it doesn't exist.

## Install

Install dependencies into your environment:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

See `USAGE.md` for detailed usage examples, options, and sample commands.

## Files

- `qr-code-generator.py` — main script.
- `requirements.txt` — Python dependencies (`qrcode` and `Pillow`).

## Optional Enhancements

- Implement a feature that lets the user generate multiple QR codes at once by providing a list of URLs or texts. Each QR code should be saved with a unique filename.

## Contributing

Contributions are welcome — open a PR against `main`.

## License

See the [LICENSE](LICENSE) file for details.
 
