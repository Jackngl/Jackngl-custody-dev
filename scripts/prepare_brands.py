#!/usr/bin/env python3
"""Script to prepare brand assets for Home Assistant submission."""
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is not installed.")
    print("Install it with: pip install Pillow")
    sys.exit(1)


def prepare_icon(source_path: Path, output_dir: Path) -> None:
    """Prepare icon images (256x256 and 512x512)."""
    print(f"Processing icon from {source_path}...")
    
    # Open and convert to RGBA
    img = Image.open(source_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create 256x256 version
    icon_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
    icon_256_path = output_dir / "icon.png"
    icon_256.save(icon_256_path, "PNG", optimize=True)
    print(f"  ✓ Created {icon_256_path} (256x256)")
    
    # Create 512x512 version
    icon_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    icon_512_path = output_dir / "icon@2x.png"
    icon_512.save(icon_512_path, "PNG", optimize=True)
    print(f"  ✓ Created {icon_512_path} (512x512)")


def prepare_logo(source_path: Path, output_dir: Path) -> None:
    """Prepare logo images (shortest side max 256 and 512)."""
    print(f"Processing logo from {source_path}...")
    
    # Open and convert to RGBA
    img = Image.open(source_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    width, height = img.size
    shortest = min(width, height)
    
    # Calculate new sizes preserving aspect ratio
    if shortest > 256:
        scale_256 = 256 / shortest
        new_width_256 = int(width * scale_256)
        new_height_256 = int(height * scale_256)
        logo_256 = img.resize((new_width_256, new_height_256), Image.Resampling.LANCZOS)
    else:
        logo_256 = img
    
    logo_256_path = output_dir / "logo.png"
    logo_256.save(logo_256_path, "PNG", optimize=True)
    print(f"  ✓ Created {logo_256_path} ({logo_256.size[0]}x{logo_256.size[1]})")
    
    # Create @2x version (max 512 on shortest side)
    if shortest > 512:
        scale_512 = 512 / shortest
        new_width_512 = int(width * scale_512)
        new_height_512 = int(height * scale_512)
        logo_512 = img.resize((new_width_512, new_height_512), Image.Resampling.LANCZOS)
    else:
        logo_512 = img
    
    logo_512_path = output_dir / "logo@2x.png"
    logo_512.save(logo_512_path, "PNG", optimize=True)
    print(f"  ✓ Created {logo_512_path} ({logo_512.size[0]}x{logo_512.size[1]})")


def main():
    """Main function."""
    # Get paths
    project_root = Path(__file__).parent.parent
    icon_source = project_root / "icon.png"
    logo_source = project_root / "logo.png"
    output_dir = project_root / "brands-ready" / "custody_schedule"
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Home Assistant Brand Assets Preparation")
    print("=" * 60)
    print()
    
    # Check if source files exist
    if not icon_source.exists():
        print(f"ERROR: Icon not found at {icon_source}")
        sys.exit(1)
    
    if not logo_source.exists():
        print(f"ERROR: Logo not found at {logo_source}")
        sys.exit(1)
    
    # Process images
    prepare_icon(icon_source, output_dir)
    print()
    prepare_logo(logo_source, output_dir)
    
    print()
    print("=" * 60)
    print("✓ All brand assets prepared successfully!")
    print(f"Output directory: {output_dir}")
    print()
    print("Files created:")
    for file in sorted(output_dir.glob("*.png")):
        size_bytes = file.stat().st_size
        size_kb = size_bytes / 1024
        print(f"  - {file.name} ({size_kb:.1f} KB)")
    print("=" * 60)


if __name__ == "__main__":
    main()
