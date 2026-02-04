# Brand Assets for Home Assistant

## Files in this directory

- `icon_original.png` - Original icon source (1024x1024 JPEG)
- `logo_original.png` - Original logo source (1024x1024 JPEG)

## Required files for submission

Create these files manually (see prepare_brands_simple.py for instructions):

- `icon.png` - 256x256px, PNG format, transparent background
- `icon@2x.png` - 512x512px, PNG format, transparent background
- `logo.png` - Shortest side max 256px, PNG format, preserves aspect ratio
- `logo@2x.png` - Shortest side max 512px, PNG format, preserves aspect ratio

## Home Assistant Requirements

### Icon
- Must be square (1:1 aspect ratio)
- 256x256 for normal, 512x512 for HD
- PNG format with transparent background
- Optimized file size

### Logo
- Landscape preferred
- Shortest side: 128-256px (normal), 256-512px (HD)
- PNG format with transparent background
- Preserves brand aspect ratio

## When ready to submit

1. Verify all 4 PNG files exist in this directory
2. Check file sizes (should be optimized, < 100KB each ideally)
3. Fork https://github.com/home-assistant/brands
4. Copy this directory to: custom_integrations/custody_schedule/
5. Create Pull Request with title: "Add Custody integration brand assets"
