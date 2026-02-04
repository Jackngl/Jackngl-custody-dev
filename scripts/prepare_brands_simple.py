#!/usr/bin/env python3
"""
Simple brand assets preparation script using only Python stdlib.
Copies and documents the steps for manual preparation.
"""
import shutil
from pathlib import Path


def main():
    project_root = Path(__file__).parent.parent
    icon_source = project_root / "icon.png"
    logo_source = project_root / "logo.png"
    output_dir = project_root / "brands-ready" / "custody_schedule"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("Home Assistant Brand Assets Preparation")
    print("=" * 70)
    print()
    print("Source files detected:")
    print(f"  - Icon: {icon_source} (JPEG 1024x1024)")
    print(f"  - Logo: {logo_source} (JPEG 1024x1024)")
    print()
    
    # Copy original files with instructions
    shutil.copy2(icon_source, output_dir / "icon_original.png")
    shutil.copy2(logo_source, output_dir / "logo_original.png")
    
    print("✓ Original files copied to brands-ready/custody_schedule/")
    print()
    print("=" * 70)
    print("MANUAL STEPS REQUIRED")
    print("=" * 70)
    print()
    print("Your images are currently JPEG format and need to be converted")
    print("to PNG format with transparency. Here are your options:")
    print()
    print("Option 1 - Using Preview (macOS built-in):")
    print("  1. Open brands-ready/custody_schedule/icon_original.png in Preview")
    print("  2. File → Export → Format: PNG")
    print("  3. Tools → Adjust Size → 256x256 pixels")
    print("  4. Save as: icon.png")
    print("  5. Repeat with resize to 512x512, save as: icon@2x.png")
    print("  6. Same process for logo (max 256 shortest side / 512 for @2x)")
    print()
    print("Option 2 - Using online tool (easypeasy):")
    print("  1. Go to: https://www.iloveimg.com/resize-image")
    print("  2. Upload icon_original.png")
    print("  3. Resize to 256x256 (icon.png) and 512x512 (icon@2x.png)")
    print("  4. Download and save to brands-ready/custody_schedule/")
    print("  5. Repeat for logo")
    print()
    print("Option 3 - Install ImageMagick:")
    print("  brew install imagemagick")
    print("  Then run:")
    print(f"    cd {project_root}")
    print("    magick icon.png -resize 256x256 brands-ready/custody_schedule/icon.png")
    print("    magick icon.png -resize 512x512 brands-ready/custody_schedule/icon@2x.png")
    print("    magick logo.png -resize x256 brands-ready/custody_schedule/logo.png")
    print("    magick logo.png -resize x512 brands-ready/custody_schedule/logo@2x.png")
    print()
    print("=" * 70)
    print("TARGET FILES NEEDED:")
    print("=" * 70)
    print("  brands-ready/custody_schedule/")
    print("    ├── icon.png       (256x256, PNG with transparency)")
    print("    ├── icon@2x.png    (512x512, PNG with transparency)")
    print("    ├── logo.png       (max 256px shortest side, PNG)")
    print("    └── logo@2x.png    (max 512px shortest side, PNG)")
    print("=" * 70)
    
    # Create README
    readme_content = """# Brand Assets for Home Assistant

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
"""
    
    readme_path = output_dir / "README.md"
    readme_path.write_text(readme_content)
    print()
    print(f"✓ Created {readme_path}")
    print()


if __name__ == "__main__":
    main()
