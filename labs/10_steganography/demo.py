from kryptografia.steganography import (
    embed_hex_line_endings,
    embed_message_lsb,
    extract_hex_line_endings,
    extract_message_lsb,
    hex_to_bits,
)


def main() -> None:
    print("Lab 10 - LSB and whitespace steganography")
    print("=" * 45)

    carrier = bytes([255] * 256)
    message = "hidden message"
    embedded = embed_message_lsb(carrier, message)
    changed_bytes = sum(
        1 for before, after in zip(carrier, embedded, strict=True) if before != after
    )

    print("\n1. Least-significant-bit byte carrier")
    print(f"message:          {message}")
    print(f"changed bytes:    {changed_bytes}")
    print(f"recovered:        {extract_message_lsb(embedded)}")

    print("\n2. HTML line-ending whitespace carrier")
    html = "\n".join(f"<p>line {index}</p>" for index in range(16))
    hex_message = "a5"
    watermark = embed_hex_line_endings(html, hex_message)
    print(f"hex message:      {hex_message}")
    print(f"message bits:     {hex_to_bits(hex_message)}")
    print(f"watermark lines:  {len(watermark.splitlines())}")
    print(f"recovered hex:    {extract_hex_line_endings(watermark, len(hex_message))}")


if __name__ == "__main__":
    main()
