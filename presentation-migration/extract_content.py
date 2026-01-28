#!/usr/bin/env python3
"""
Content Extraction Utility for Drupal Brand Presentation Skill

Extracts content from PPTX files into markdown format that can be
edited and then migrated to the Drupal brand template.

Now includes slide-to-image mapping for proper image migration.
"""

import re
import os
import sys
import json
from pathlib import Path
from lxml import etree
import zipfile
import tempfile
import shutil
from datetime import datetime

NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
}


def clean_text(text):
    """Remove control characters."""
    if not text:
        return ""
    return ''.join(c if ord(c) >= 32 or c in '\n\t' else ' ' for c in str(text)).strip()


def get_layout_name(rels_content, layout_map):
    """Extract layout name from relationships XML."""
    if not rels_content:
        return "UNKNOWN"

    rels_tree = etree.fromstring(rels_content)
    for rel in rels_tree:
        target = rel.get('Target', '')
        if 'slideLayout' in target:
            match = re.search(r'slideLayout(\d+)', target)
            if match:
                layout_num = int(match.group(1))
                return layout_map.get(layout_num, f"LAYOUT_{layout_num}")
    return "UNKNOWN"


def get_slide_images(rels_content):
    """Extract image references from slide relationships XML.

    Returns list of image filenames used by this slide.
    """
    if not rels_content:
        return []

    images = []
    rels_tree = etree.fromstring(rels_content)

    for rel in rels_tree:
        rel_type = rel.get('Type', '')
        target = rel.get('Target', '')

        # Check if this is an image relationship
        if 'image' in rel_type.lower() and target:
            # Extract filename from path like "../media/image18.png"
            img_name = Path(target).name
            images.append(img_name)

    return images


def extract_pptx_to_markdown(pptx_path, output_path=None, extract_images=False):
    """
    Extract PPTX content to markdown format.

    Args:
        pptx_path: Path to source PPTX
        output_path: Path for output markdown (default: same name with .md)
        extract_images: If True, also extract images to a folder

    Returns:
        slides_data: List of slide dictionaries with content and image mappings
    """
    pptx_path = Path(pptx_path)

    if output_path is None:
        output_path = pptx_path.with_suffix('.md')
    else:
        output_path = Path(output_path)

    print(f"Extracting: {pptx_path.name}")

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)

        # Extract PPTX
        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(work_dir)

        slides_dir = work_dir / 'ppt/slides'
        rels_dir = slides_dir / '_rels'

        # Build layout name map from slideLayouts
        layout_map = {}
        layouts_dir = work_dir / 'ppt/slideLayouts'
        if layouts_dir.exists():
            for layout_file in layouts_dir.glob('slideLayout*.xml'):
                num = int(re.search(r'slideLayout(\d+)', layout_file.name).group(1))
                tree = etree.parse(str(layout_file))
                root = tree.getroot()

                # Try to get layout name
                name_attr = root.get('matchingName') or root.get('name')
                if name_attr:
                    # Normalize name
                    name = name_attr.upper().replace(' ', '_').replace('-', '_')
                    name = re.sub(r'[^A-Z0-9_]', '', name)
                    layout_map[num] = name
                else:
                    layout_map[num] = f"LAYOUT_{num}"

        # Get all slide files sorted by number
        slide_files = sorted(
            [f for f in slides_dir.glob('slide*.xml') if f.is_file()],
            key=lambda x: int(re.search(r'slide(\d+)', x.name).group(1))
        )

        slides_data = []
        image_mapping = {}  # slide_num -> [image_files]

        for slide_file in slide_files:
            num = int(re.search(r'slide(\d+)', slide_file.name).group(1))

            # Parse slide XML
            tree = etree.parse(str(slide_file))
            root = tree.getroot()

            # Get layout and images from rels
            rels_file = rels_dir / f'slide{num}.xml.rels'
            layout = "DEFAULT"
            images = []

            if rels_file.exists():
                with open(rels_file, 'rb') as f:
                    rels_content = f.read()
                    layout = get_layout_name(rels_content, layout_map)
                    images = get_slide_images(rels_content)

            # Store image mapping
            if images:
                image_mapping[num] = images

            # Extract all text
            texts = []
            for t in root.xpath('.//a:t', namespaces=NSMAP):
                if t.text:
                    texts.append(clean_text(t.text))

            # Deduplicate adjacent identical texts
            unique_texts = []
            prev = None
            for t in texts:
                if t != prev and t:
                    unique_texts.append(t)
                    prev = t

            # First text is usually title
            title = unique_texts[0] if unique_texts else ""
            body = '\n'.join(unique_texts[1:]) if len(unique_texts) > 1 else ""

            slides_data.append({
                'number': num,
                'layout': layout,
                'title': title,
                'body': body,
                'images': images,
                'image_count': len(images),
            })

        # Extract images if requested
        images_dir = None
        if extract_images:
            images_dir = output_path.parent / f"{output_path.stem}-images"
            images_dir.mkdir(parents=True, exist_ok=True)

            media_dir = work_dir / 'ppt/media'
            if media_dir.exists():
                for img in media_dir.iterdir():
                    if img.is_file():
                        shutil.copy(img, images_dir / img.name)
                print(f"Extracted {len(list(images_dir.iterdir()))} images to {images_dir.name}/")

            # Save image mapping JSON
            mapping_file = output_path.parent / f"{output_path.stem}-image-mapping.json"
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'source': pptx_path.name,
                    'images_dir': str(images_dir.name),
                    'slide_images': {str(k): v for k, v in image_mapping.items()},
                    'total_images': sum(len(v) for v in image_mapping.values()),
                    'slides_with_images': len(image_mapping),
                }, f, indent=2)
            print(f"Created image mapping: {mapping_file.name}")

    # Generate markdown
    md_content = generate_markdown(slides_data, pptx_path.name)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"Created: {output_path}")
    print(f"Slides: {len(slides_data)}")
    print(f"Slides with images: {len(image_mapping)}")

    return slides_data


def generate_markdown(slides_data, source_name):
    """Generate markdown from slides data."""
    # Count slides with images
    slides_with_images = sum(1 for s in slides_data if s.get('images'))
    total_images = sum(s.get('image_count', 0) for s in slides_data)

    lines = [
        f"# {Path(source_name).stem} - Content Catalog",
        "",
        f"**Source:** {source_name}",
        f"**Total Slides:** {len(slides_data)}",
        f"**Slides with Images:** {slides_with_images}",
        f"**Total Image References:** {total_images}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
    ]

    for slide in slides_data:
        lines.extend([
            f"## Slide {slide['number']}",
            f"**Layout:** {slide['layout']}",
            f"**Title:** {slide['title']}",
        ])

        # Add image info
        if slide.get('images'):
            lines.append(f"**Images:** {', '.join(slide['images'])}")
        else:
            lines.append("**Images:** (none)")

        lines.extend([
            "",
            "### Content",
            slide['body'] if slide['body'] else "(No additional content)",
            "",
            "---",
            "",
        ])

    return '\n'.join(lines)


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: python extract_content.py <input.pptx> [output.md] [--images]")
        print("")
        print("Options:")
        print("  --images    Also extract images and create slide-to-image mapping")
        print("")
        print("Output files created:")
        print("  - <name>.md                    Content catalog")
        print("  - <name>-images/               Extracted images folder")
        print("  - <name>-image-mapping.json    Slide to image mapping")
        print("")
        print("Example:")
        print("  python extract_content.py presentation.pptx content.md --images")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    extract_images = '--images' in sys.argv

    # Find output file (if specified and not a flag)
    for arg in sys.argv[2:]:
        if not arg.startswith('--'):
            output_file = arg
            break

    print("=" * 60)
    print("Drupal Brand - Content Extraction")
    print("=" * 60)

    try:
        extract_pptx_to_markdown(input_file, output_file, extract_images)
        print("\n Extraction complete!")

    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
