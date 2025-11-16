import argparse
import os
import sys
import shlex

try:
    import qrcode  # type: ignore[import]
except Exception:
    print("Missing dependency 'qrcode'. Install with: pip install -r requirements.txt")
    sys.exit(1)


def ensure_extension(filename, default_ext=".png"):
    """Return filename with extension. If none, append `default_ext`.

    This helps users who pass e.g. `-o qrcode` to automatically get `qrcode.png`.
    """
    root, ext = os.path.splitext(filename)
    if not ext:
        return filename + default_ext
    return filename


def main():
    """Parse CLI args, collect input (argument, stdin, or prompt), build the QR,
    and save it to an image file.

    Major steps:
    - Parse arguments and options (output path, sizing, colors, error correction)
    - Determine input data (positional argument, stdin when '-' provided, or interactive prompt)
    - Normalize output filename
    - Create a `qrcode.QRCode` with requested error-correction and sizing
    - Render to an image and save to disk
    """

    parser = argparse.ArgumentParser(description="Generate a QR code image from text or a URL.")
    parser.add_argument("data", nargs="?", help="Text or URL to encode. Use '-' to read from stdin.")
    parser.add_argument("-o", "--output", default="qrcode.png", help="Output filename (default: qrcode.png).")
    parser.add_argument("--box-size", type=int, default=10, help="Size of each QR box in pixels.")
    parser.add_argument("--border", type=int, default=4, help="Border size (boxes).")
    parser.add_argument("--fill-color", default="black", help="Fill color for QR code.")
    parser.add_argument("--back-color", default="white", help="Background color.")
    parser.add_argument("--error-correction", choices=["L", "M", "Q", "H"], default="M",
                        help="Error correction level: L, M, Q, or H (default M).")

    args = parser.parse_args()

    # Determine source of the data to encode
    if args.data and args.data != "-":
        # Data was provided as a positional argument
        data = args.data
    else:
        # If '-' specified or stdin is not a TTY, read from stdin, otherwise prompt interactively
        if args.data == "-" or not sys.stdin.isatty():
            data = sys.stdin.read().strip()
        else:
            # Show a short customization help message before prompting the user
            # so they know which CLI options are available and how they affect
            # the generated QR code. We accept a simple `-o name` or
            # `--output=name` suffix in the interactive input to override the
            # output filename without re-running the script.
            print("\nYou can customize the QR appearance with these options:")
            print(f"  box size (module pixels): --box-size {args.box_size}  # default {args.box_size}")
            print(f"  border (white margin in modules): --border {args.border}  # default {args.border}")
            print(f"  fill color: --fill-color {args.fill_color}  # default {args.fill_color}")
            print(f"  background color: --back-color {args.back_color}  # default {args.back_color}")
            print(f"  error correction: --error-correction {args.error_correction}  # default {args.error_correction}")
            # Examples and sample commands are intentionally omitted here
            # so interactive prompt stays focused; see USAGE.md for examples.

            # Read a raw line from the user. They may optionally append
            # `-o filename` or `--output=filename` to override the output.
            raw = input("Enter the text or URL: ").strip()
            data = raw

            # Quick parsing: allow the user to supply a trailing -o <name>
            # or --output=<name> in the interactive input. We use shlex so
            # quoted values are handled correctly.
            try:
                parts = shlex.split(raw)
            except ValueError:
                parts = raw.split()

            if parts:
                # Find `-o` or `--output` in the token list
                new_parts = []
                i = 0
                output_override = None
                while i < len(parts):
                    tok = parts[i]
                    if tok == "-o" and i + 1 < len(parts):
                        output_override = parts[i + 1]
                        i += 2
                        continue
                    if tok.startswith("--output="):
                        output_override = tok.split("=", 1)[1]
                        i += 1
                        continue
                    if tok == "--output" and i + 1 < len(parts):
                        output_override = parts[i + 1]
                        i += 2
                        continue
                    new_parts.append(tok)
                    i += 1

                if output_override:
                    # Set the args.output so the rest of the code handles
                    # extension and directory logic as usual.
                    args.output = output_override
                    data = " ".join(new_parts).strip()

    if not data:
        print("No data provided. Exiting.")
        sys.exit(1)

    # Ensure the output filename has an extension (we default to .png)
    output = ensure_extension(args.output, ".png")

    # If the user provided only a filename (no directory), save outputs
    # into the `generated_png/` directory by default. If a path was
    # provided (e.g. `out/qr.png`), respect the provided directory.
    out_dir = os.path.dirname(output)
    if not out_dir:
        out_dir = "generated_png"
        output = os.path.join(out_dir, output)

    # Ensure the output directory exists before saving
    os.makedirs(out_dir, exist_ok=True)

    # Map error-correction flag to the library constant
    ec_map = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    # Build the QR code and save the image
    try:
        qr = qrcode.QRCode(
            error_correction=ec_map[args.error_correction],
            box_size=args.box_size,
            border=args.border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=args.fill_color, back_color=args.back_color)
        img.save(output)
    except Exception as exc:
        # Any failure while generating or saving is surfaced here
        print(f"Failed to generate QR code: {exc}")
        sys.exit(1)

    print(f"QR code saved as {output}")


if __name__ == "__main__":
    main()
# duplicate corrupted content removed