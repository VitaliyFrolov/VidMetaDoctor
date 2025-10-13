#!/usr/bin/env bash

set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
RES_DIR="$BASE_DIR/resources/exiftool"

mkdir -p "$RES_DIR"

echo "Detecting platform..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="mac"
    URL="https://exiftool.org/Image-ExifTool-13.38.tar.gz"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
    URL="https://exiftool.org/Image-ExifTool-13.38.tar.gz"
else
    echo "Unsupported platform via shell. Use PowerShell on Windows!"
    exit 1
fi

TARGET="$RES_DIR/$PLATFORM"
mkdir -p "$TARGET"

echo "Downloading ExifTool from $URL..."

TMP_FILE="/tmp/exiftool.tar.gz"
curl -L "$URL" -o "$TMP_FILE"

echo "Extracting..."

tar -xzf "$TMP_FILE" -C "$TARGET" --strip-components=1

mv "$TARGET/exiftool" "$TARGET/exiftool.pl" 2>/dev/null || true
cp "$TARGET/exiftool.pl" "$TARGET/exiftool" 2>/dev/null || true

chmod +x "$TARGET/exiftool"

echo "Done! ExifTool installed to $TARGET"
