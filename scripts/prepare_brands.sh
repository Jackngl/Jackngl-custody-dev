#!/bin/bash
# Script to prepare brand assets for Home Assistant using sips (macOS built-in tool)
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/brands-ready/custody_schedule"

echo "============================================================"
echo "Home Assistant Brand Assets Preparation"
echo "============================================================"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Processing icon..."
# Convert JPEG to PNG and resize to 256x256
sips -s format png "$PROJECT_ROOT/icon.png" -z 256 256 --out "$OUTPUT_DIR/icon.png" > /dev/null 2>&1
echo "  ✓ Created icon.png (256x256)"

# Convert JPEG to PNG and resize to 512x512
sips -s format png "$PROJECT_ROOT/icon.png" -z 512 512 --out "$OUTPUT_DIR/icon@2x.png" > /dev/null 2>&1
echo "  ✓ Created icon@2x.png (512x512)"

echo ""
echo "Processing logo..."
# Convert JPEG to PNG and resize (preserving aspect ratio, max 256 on shortest side)
sips -s format png "$PROJECT_ROOT/logo.png" -Z 256 --out "$OUTPUT_DIR/logo.png" > /dev/null 2>&1
LOGO_SIZE=$(sips -g pixelWidth -g pixelHeight "$OUTPUT_DIR/logo.png" | grep -E 'pixelWidth|pixelHeight' | awk '{print $2}' | tr '\n' 'x' | sed 's/x$//')
echo "  ✓ Created logo.png ($LOGO_SIZE)"

# Create @2x version (max 512 on shortest side)
sips -s format png "$PROJECT_ROOT/logo.png" -Z 512 --out "$OUTPUT_DIR/logo@2x.png" > /dev/null 2>&1
LOGO2X_SIZE=$(sips -g pixelWidth -g pixelHeight "$OUTPUT_DIR/logo@2x.png" | grep -E 'pixelWidth|pixelHeight' | awk '{print $2}' | tr '\n' 'x' | sed 's/x$//')
echo "  ✓ Created logo@2x.png ($LOGO2X_SIZE)"

echo ""
echo "============================================================"
echo "✓ All brand assets prepared successfully!"
echo "Output directory: $OUTPUT_DIR"
echo ""
echo "Files created:"
ls -lh "$OUTPUT_DIR" | grep -v "^total" | awk '{printf "  - %s (%s)\n", $9, $5}'
echo "============================================================"
