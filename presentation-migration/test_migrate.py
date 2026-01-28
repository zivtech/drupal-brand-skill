#!/usr/bin/env python3
"""
Presentation Migration Test Harness

Tests the migrate.py tool with specific inputs and validates outputs.
Generates reports on text placement, font sizes, and placeholder targeting.

Usage:
    python test_migrate.py                    # Run all batches
    python test_migrate.py --batch 1          # Run specific batch
    python test_migrate.py --test 1a          # Run specific test
"""

import os
import sys
import json
import shutil
import zipfile
import tempfile
import argparse
from pathlib import Path
from datetime import datetime
from lxml import etree

# Import from migrate.py
from migrate import (
    TEMPLATE_PATH,
    NSMAP,
    detect_content_type,
    clean_text,
)

# ============================================================
# CONSTANTS
# ============================================================

SCRIPT_DIR = Path(__file__).parent
TEST_OUTPUT_DIR = SCRIPT_DIR / "test-output"
PLACEHOLDER_SIZES_FILE = SCRIPT_DIR / "placeholder_sizes.json"

# EMU conversion (English Metric Units)
EMU_PER_INCH = 914400
EMU_PER_PT = 12700

# Minimum font sizes (in hundredths of a point)
MIN_TITLE_SIZE = 2400  # 24pt
MIN_BODY_SIZE = 1400   # 14pt

# ============================================================
# TEST CASES
# ============================================================

BATCH_1_TITLE = [
    {
        "id": "1a",
        "name": "Basic Title",
        "template_slide": 1,
        "input": {
            "title": "Welcome to Drupal",
            "body": "Jane Smith\nDirector of Digital Strategy"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
            "min_title_pt": 24,
            "min_body_pt": 18,
        }
    },
    {
        "id": "1b",
        "name": "Long Title (Overflow Test)",
        "template_slide": 1,
        "input": {
            "title": "The Digital Experience Platform Foundation for Ambitious Organizations Building the Future",
            "body": "Enterprise Solutions Team"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
            "title_should_wrap_or_scale": True,
        }
    },
]

BATCH_2_STATS = [
    {
        "id": "2a",
        "name": "Short Stat",
        "template_slide": 11,
        "input": {
            "title": "72%",
            "body": "of enterprise organizations report improved content management efficiency"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
            "min_title_pt": 72,
        }
    },
    {
        "id": "2b",
        "name": "Medium Stat",
        "template_slide": 11,
        "input": {
            "title": "1.3M+",
            "body": "Community members contributing to Drupal worldwide"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
        }
    },
    {
        "id": "2c",
        "name": "Long Stat Description",
        "template_slide": 11,
        "input": {
            "title": "56%",
            "body": "of Government websites run on Drupal\n\n- Trusted by 14 of the top 20 federal agencies\n- Enterprise security architecture\n- Proven scalability"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
            "bullets_preserved": True,
        }
    },
]

BATCH_3_CONTENT = [
    {
        "id": "3a",
        "name": "Photo + Text (Left Layout - Title Only)",
        "template_slide": 38,
        # Slide 38 only has one text box, so body won't be visible
        "input": {
            "title": "Powering Digital Experiences",
            "body": "",  # This slide type doesn't have a body placeholder
            "image": "hero-photo.jpg"
        },
        "expected": {
            "title_visible": True,
            "body_visible": False,  # Single text box slide
        }
    },
    {
        "id": "3b",
        "name": "Photo + Text (Right Layout)",
        "template_slide": 2,
        "input": {
            "title": "Powering Digital Experiences",
            "body": "Drupal provides the flexibility and power to build exactly what your organization needs.",
            "image": "hero-photo.jpg"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
        }
    },
    {
        "id": "3c",
        "name": "Quote Slide (Title Only)",
        "template_slide": 8,
        # Slide 8 is a quote slide with single text area
        "input": {
            "title": "Drupal gave us the flexibility to build exactly what we needed without compromise — Sarah Chen, CTO",
            "body": "",  # Single text area slide
        },
        "expected": {
            "title_visible": True,
            "body_visible": False,  # Quote content goes in title
        }
    },
]

BATCH_4_BULLETS = [
    {
        "id": "4a",
        "name": "3-Item List",
        "template_slide": 21,
        "input": {
            "title": "Key Benefits",
            "body": "- Flexibility to customize\n- Enterprise security\n- Scalable architecture"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
            "bullet_count": 3,
        }
    },
    {
        "id": "4b",
        "name": "5-Item List (Overflow)",
        "template_slide": 21,
        "input": {
            "title": "Drupal Features",
            "body": "- Content modeling\n- Workflow management\n- Multi-site support\n- API-first architecture\n- Accessibility compliance"
        },
        "expected": {
            "title_visible": True,
            "body_visible": True,
            "bullet_count": 5,
        }
    },
]

BATCH_5_DETECTION = [
    {
        "id": "5a",
        "name": "Detect Statistic",
        "input": {"title": "56% of Government websites use Drupal", "body": ""},
        "expected_type": "statistic",
    },
    {
        "id": "5b",
        "name": "Detect Quote",
        "input": {"title": '"Drupal transformed how we work" - CTO', "body": ""},
        "expected_type": "quote",
    },
    {
        "id": "5c",
        "name": "Detect Bullet List",
        "input": {"title": "Benefits", "body": "- Point one\n- Point two\n- Point three"},
        "expected_type": "bullet_list",
    },
    {
        "id": "5d",
        "name": "Detect Case Study",
        "input": {"title": "How NASA rebuilt their website with Drupal", "body": "Customer success story"},
        "expected_type": "case_study",
    },
]

ALL_BATCHES = {
    "batch1_title": BATCH_1_TITLE,
    "batch2_stats": BATCH_2_STATS,
    "batch3_content": BATCH_3_CONTENT,
    "batch4_bullets": BATCH_4_BULLETS,
    "batch5_detection": BATCH_5_DETECTION,
}

# ============================================================
# PLACEHOLDER EXTRACTION
# ============================================================

def find_placeholder(root, ph_type, idx=None):
    """Find shape by placeholder type.

    Args:
        root: XML root element
        ph_type: Placeholder type ('title', 'body', 'subTitle', etc.)
        idx: Optional placeholder index

    Returns:
        Shape element or None
    """
    if idx is not None:
        xpath = f'.//p:sp[.//p:ph[@type="{ph_type}" and @idx="{idx}"]]'
    else:
        xpath = f'.//p:sp[.//p:ph[@type="{ph_type}"]]'

    shapes = root.xpath(xpath, namespaces=NSMAP)
    return shapes[0] if shapes else None


def find_text_boxes(root):
    """Find all text box shapes (p:sp with txBox="1").

    Returns list of shapes sorted by position (top-to-bottom, left-to-right).
    """
    # Find all shapes that are text boxes
    xpath = './/p:sp[p:nvSpPr/p:cNvSpPr[@txBox="1"]]'
    shapes = root.xpath(xpath, namespaces=NSMAP)

    # Sort by position (y first, then x)
    def get_position(shape):
        xfrm = shape.find('.//a:xfrm', namespaces=NSMAP)
        if xfrm is not None:
            off = xfrm.find('a:off', namespaces=NSMAP)
            if off is not None:
                return (int(off.get('y', 0)), int(off.get('x', 0)))
        return (0, 0)

    return sorted(shapes, key=get_position)


def get_placeholder_dimensions(shape):
    """Extract dimensions from a shape element.

    Returns:
        dict with x, y, width, height in EMUs
    """
    if shape is None:
        return None

    xfrm = shape.find('.//a:xfrm', namespaces=NSMAP)
    if xfrm is None:
        return None

    off = xfrm.find('a:off', namespaces=NSMAP)
    ext = xfrm.find('a:ext', namespaces=NSMAP)

    if off is None or ext is None:
        return None

    return {
        'x': int(off.get('x', 0)),
        'y': int(off.get('y', 0)),
        'width': int(ext.get('cx', 0)),
        'height': int(ext.get('cy', 0)),
        'width_inches': int(ext.get('cx', 0)) / EMU_PER_INCH,
        'height_inches': int(ext.get('cy', 0)) / EMU_PER_INCH,
    }


def get_text_from_shape(shape):
    """Extract all text from a shape."""
    if shape is None:
        return ""

    texts = []
    for t in shape.xpath('.//a:t', namespaces=NSMAP):
        if t.text:
            texts.append(t.text)
    return ' '.join(texts)


def get_font_size_from_shape(shape):
    """Get the first font size found in a shape (in hundredths of a point)."""
    if shape is None:
        return None

    # Check run properties
    for rPr in shape.xpath('.//a:rPr[@sz]', namespaces=NSMAP):
        return int(rPr.get('sz'))

    # Check default run properties
    for defRPr in shape.xpath('.//a:defRPr[@sz]', namespaces=NSMAP):
        return int(defRPr.get('sz'))

    return None


# ============================================================
# TEST FUNCTIONS
# ============================================================

def extract_template_slide(template_path, slide_num, work_dir):
    """Extract a single slide from the template to a working directory.

    Returns the path to the extracted slide XML.
    """
    with zipfile.ZipFile(template_path, 'r') as zf:
        zf.extractall(work_dir)

    slide_path = work_dir / f'ppt/slides/slide{slide_num}.xml'
    if not slide_path.exists():
        raise FileNotFoundError(f"Slide {slide_num} not found in template")

    return slide_path


def replace_text_in_placeholder(root, ph_type, new_text, idx=None):
    """Replace text in a specific placeholder by type.

    This is the CORRECT approach - targeting placeholders, not arbitrary text runs.
    """
    shape = find_placeholder(root, ph_type, idx)
    if shape is None:
        return False

    # Find all text runs in this shape
    text_runs = shape.xpath('.//a:t', namespaces=NSMAP)

    if not text_runs:
        return False

    # Replace first text run, clear others
    text_runs[0].text = new_text
    for t in text_runs[1:]:
        t.text = ""

    return True


def replace_text_in_textbox(shape, new_text):
    """Replace text in a text box shape."""
    if shape is None:
        return False

    text_runs = shape.xpath('.//a:t', namespaces=NSMAP)
    if not text_runs:
        return False

    text_runs[0].text = new_text
    for t in text_runs[1:]:
        t.text = ""

    return True


def test_single_slide(test_case, output_dir):
    """Create a single-slide PPTX for testing.

    Args:
        test_case: Test case dict with id, template_slide, input, expected
        output_dir: Directory for test output

    Returns:
        dict with validation results
    """
    test_id = test_case['id']
    template_slide = test_case.get('template_slide')
    input_data = test_case['input']

    # For detection tests, skip PPTX generation
    if 'expected_type' in test_case:
        return validate_detection(test_case)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save input
    input_file = output_dir / f"test_{test_id}_input.json"
    with open(input_file, 'w') as f:
        json.dump(input_data, f, indent=2)

    # Create output PPTX
    output_pptx = output_dir / f"test_{test_id}_output.pptx"

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)

        # Extract template
        slide_path = extract_template_slide(TEMPLATE_PATH, template_slide, work_dir)

        # Parse and modify slide
        tree = etree.parse(str(slide_path))
        root = tree.getroot()

        # Get original placeholder info
        title_shape = find_placeholder(root, 'title')
        body_shape = find_placeholder(root, 'body')

        title_dims = get_placeholder_dimensions(title_shape)
        body_dims = get_placeholder_dimensions(body_shape)

        # Replace text using correct placeholder targeting
        title_replaced = replace_text_in_placeholder(root, 'title', input_data.get('title', ''))
        body_replaced = replace_text_in_placeholder(root, 'body', input_data.get('body', ''), idx='1')

        # If body placeholder with idx=1 not found, try without idx
        if not body_replaced:
            body_replaced = replace_text_in_placeholder(root, 'body', input_data.get('body', ''))

        # Fallback: If no standard placeholders, find text boxes
        if not title_replaced or not body_replaced:
            text_boxes = find_text_boxes(root)
            if text_boxes:
                # First text box is typically title
                if not title_replaced and len(text_boxes) >= 1:
                    title_replaced = replace_text_in_textbox(text_boxes[0], input_data.get('title', ''))
                # Second text box is typically body (or use first if only one)
                if not body_replaced:
                    if len(text_boxes) >= 2:
                        body_replaced = replace_text_in_textbox(text_boxes[1], input_data.get('body', ''))
                    elif len(text_boxes) >= 1 and not title_replaced:
                        body_replaced = replace_text_in_textbox(text_boxes[0], input_data.get('body', ''))

        # Save modified slide
        tree.write(str(slide_path), xml_declaration=True, encoding='UTF-8', standalone=True)

        # Create output PPTX (single-slide version)
        # Keep only slide 1 in package structure
        create_single_slide_pptx(work_dir, template_slide, output_pptx)

    # Validate output
    validation = validate_output(output_pptx, test_case)
    validation['input_file'] = str(input_file)
    validation['output_file'] = str(output_pptx)
    validation['title_dims'] = title_dims
    validation['body_dims'] = body_dims
    validation['title_replaced'] = title_replaced
    validation['body_replaced'] = body_replaced

    return validation


def create_single_slide_pptx(work_dir, slide_num, output_path):
    """Create a PPTX with a single slide for testing."""
    slides_dir = work_dir / 'ppt/slides'
    rels_dir = slides_dir / '_rels'

    # Rename the target slide to slide1.xml if needed
    if slide_num != 1:
        src = slides_dir / f'slide{slide_num}.xml'
        dst = slides_dir / 'slide1.xml'
        if src.exists():
            shutil.copy(src, dst)

        src_rels = rels_dir / f'slide{slide_num}.xml.rels'
        dst_rels = rels_dir / 'slide1.xml.rels'
        if src_rels.exists():
            shutil.copy(src_rels, dst_rels)

    # Update Content_Types.xml to only reference slide1
    ct_path = work_dir / '[Content_Types].xml'
    ct_tree = etree.parse(str(ct_path))
    ct_root = ct_tree.getroot()

    ns = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
    for override in ct_root.xpath('.//ct:Override[contains(@PartName, "/ppt/slides/slide")]', namespaces=ns):
        part_name = override.get('PartName')
        if part_name != '/ppt/slides/slide1.xml':
            ct_root.remove(override)

    ct_tree.write(str(ct_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    # Update presentation.xml.rels
    rels_path = work_dir / 'ppt/_rels/presentation.xml.rels'
    if rels_path.exists():
        rels_tree = etree.parse(str(rels_path))
        rels_root = rels_tree.getroot()

        # Update slide relationships
        for rel in list(rels_root):
            target = rel.get('Target', '')
            if 'slides/slide' in target and 'slide1' not in target:
                rels_root.remove(rel)

        rels_tree.write(str(rels_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    # Update presentation.xml
    pres_path = work_dir / 'ppt/presentation.xml'
    if pres_path.exists():
        pres_tree = etree.parse(str(pres_path))
        pres_root = pres_tree.getroot()

        pres_ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
        sld_id_lst = pres_root.find('.//p:sldIdLst', pres_ns)

        if sld_id_lst is not None:
            # Keep only first slide reference
            children = list(sld_id_lst)
            for child in children[1:]:
                sld_id_lst.remove(child)

        pres_tree.write(str(pres_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    # Create output ZIP
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root_path, dirs, files in os.walk(work_dir):
            for file in files:
                file_path = Path(root_path) / file
                arc_path = file_path.relative_to(work_dir)
                zf.write(file_path, arc_path)


def validate_output(pptx_path, test_case):
    """Validate the output PPTX.

    Returns:
        dict with validation results
    """
    results = {
        'test_id': test_case['id'],
        'test_name': test_case['name'],
        'passed': True,
        'issues': [],
    }

    input_data = test_case['input']
    expected = test_case.get('expected', {})

    # Extract and analyze
    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)

        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(work_dir)

        slide_path = work_dir / 'ppt/slides/slide1.xml'
        if not slide_path.exists():
            results['passed'] = False
            results['issues'].append("slide1.xml not found in output")
            return results

        tree = etree.parse(str(slide_path))
        root = tree.getroot()

        # Check title placeholder (or text box fallback)
        title_shape = find_placeholder(root, 'title')
        if title_shape is None:
            text_boxes = find_text_boxes(root)
            if text_boxes:
                title_shape = text_boxes[0]

        title_text = get_text_from_shape(title_shape)
        title_font_size = get_font_size_from_shape(title_shape)

        results['title_present'] = bool(title_text)
        results['title_text'] = title_text
        results['title_font_size'] = title_font_size
        results['title_font_pt'] = title_font_size / 100 if title_font_size else None

        # Check body placeholder (or text box fallback)
        body_shape = find_placeholder(root, 'body')
        if body_shape is None:
            text_boxes = find_text_boxes(root)
            if len(text_boxes) >= 2:
                body_shape = text_boxes[1]

        body_text = get_text_from_shape(body_shape)
        body_font_size = get_font_size_from_shape(body_shape)

        results['body_present'] = bool(body_text)
        results['body_text'] = body_text
        results['body_font_size'] = body_font_size
        results['body_font_pt'] = body_font_size / 100 if body_font_size else None

        # Validation checks
        if expected.get('title_visible') and not results['title_present']:
            results['passed'] = False
            results['issues'].append("Title not visible (expected content)")

        if expected.get('body_visible') and not results['body_present']:
            results['passed'] = False
            results['issues'].append("Body not visible (expected content)")

        # Check for truncation
        if input_data.get('title') and title_text:
            if len(title_text) < len(input_data['title']) * 0.9:
                results['issues'].append(f"Title may be truncated: {len(title_text)} vs {len(input_data['title'])} chars")

        if input_data.get('body') and body_text:
            # Account for whitespace normalization
            body_input_len = len(input_data['body'].replace('\n', ' '))
            if len(body_text) < body_input_len * 0.8:
                results['issues'].append(f"Body may be truncated: {len(body_text)} vs {body_input_len} chars")

        # Check minimum font sizes
        min_title_pt = expected.get('min_title_pt', 24)
        if title_font_size and title_font_size < min_title_pt * 100:
            results['issues'].append(f"Title font too small: {title_font_size/100}pt (min {min_title_pt}pt)")

        min_body_pt = expected.get('min_body_pt', 14)
        if body_font_size and body_font_size < min_body_pt * 100:
            results['issues'].append(f"Body font too small: {body_font_size/100}pt (min {min_body_pt}pt)")

        # Check bullet preservation
        if expected.get('bullet_count'):
            bullet_markers = body_text.count('-') + body_text.count('•')
            results['bullet_count'] = bullet_markers
            if bullet_markers < expected['bullet_count']:
                results['issues'].append(f"Bullets may be lost: found {bullet_markers}, expected {expected['bullet_count']}")

        # Check em-dash preservation
        if expected.get('em_dash_preserved'):
            if '—' not in body_text and '-' not in body_text:
                results['issues'].append("Em-dash not preserved in attribution")

    return results


def validate_detection(test_case):
    """Validate content type detection."""
    input_data = test_case['input']
    input_data['number'] = 5  # Middle slide position

    detected = detect_content_type(input_data)
    expected = test_case.get('expected_type')

    return {
        'test_id': test_case['id'],
        'test_name': test_case['name'],
        'passed': detected == expected,
        'detected_type': detected,
        'expected_type': expected,
        'issues': [] if detected == expected else [f"Expected {expected}, got {detected}"],
    }


def run_batch(batch_name, tests, output_base_dir):
    """Run all tests in a batch."""
    output_dir = output_base_dir / batch_name
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for test in tests:
        print(f"  Running test {test['id']}: {test['name']}...")
        result = test_single_slide(test, output_dir)
        results.append(result)

        status = "PASS" if result.get('passed', False) else "FAIL"
        print(f"    {status}")
        if result.get('issues'):
            for issue in result['issues']:
                print(f"      - {issue}")

    return results


def write_validation_report(all_results, output_dir):
    """Write validation report as markdown."""
    report_path = output_dir / "validation_report.md"

    lines = [
        "# Presentation Migration Test Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
    ]

    # Summary
    total_tests = sum(len(r) for r in all_results.values())
    passed_tests = sum(1 for results in all_results.values() for r in results if r.get('passed'))

    lines.extend([
        "## Summary",
        "",
        f"- **Total Tests:** {total_tests}",
        f"- **Passed:** {passed_tests}",
        f"- **Failed:** {total_tests - passed_tests}",
        "",
    ])

    # Batch results
    for batch_name, results in all_results.items():
        batch_passed = sum(1 for r in results if r.get('passed'))
        lines.extend([
            f"## {batch_name.replace('_', ' ').title()}",
            "",
            f"Passed: {batch_passed}/{len(results)}",
            "",
            "| Test | Name | Status | Issues |",
            "|------|------|--------|--------|",
        ])

        for r in results:
            status = "✅ PASS" if r.get('passed') else "❌ FAIL"
            issues = "; ".join(r.get('issues', [])) or "-"
            lines.append(f"| {r['test_id']} | {r['test_name']} | {status} | {issues} |")

        lines.append("")

    # Detailed results
    lines.extend([
        "---",
        "",
        "## Detailed Results",
        "",
    ])

    for batch_name, results in all_results.items():
        lines.append(f"### {batch_name}")
        lines.append("")

        for r in results:
            lines.extend([
                f"#### Test {r['test_id']}: {r['test_name']}",
                "",
            ])

            if 'title_text' in r:
                lines.extend([
                    f"- **Title present:** {r.get('title_present')}",
                    f"- **Title text:** {r.get('title_text', 'N/A')[:50]}...",
                    f"- **Title font:** {r.get('title_font_pt', 'N/A')}pt",
                    f"- **Body present:** {r.get('body_present')}",
                    f"- **Body text:** {r.get('body_text', 'N/A')[:50]}...",
                    f"- **Body font:** {r.get('body_font_pt', 'N/A')}pt",
                ])
            elif 'detected_type' in r:
                lines.extend([
                    f"- **Expected type:** {r.get('expected_type')}",
                    f"- **Detected type:** {r.get('detected_type')}",
                ])

            if r.get('issues'):
                lines.append("- **Issues:**")
                for issue in r['issues']:
                    lines.append(f"  - {issue}")

            lines.append("")

    with open(report_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"\nReport written to: {report_path}")
    return report_path


# ============================================================
# PLACEHOLDER SIZE EXTRACTION
# ============================================================

def extract_all_placeholder_sizes(template_path, output_file):
    """Extract placeholder dimensions from all template slides."""
    sizes = {}

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)

        with zipfile.ZipFile(template_path, 'r') as zf:
            zf.extractall(work_dir)

        slides_dir = work_dir / 'ppt/slides'

        for slide_file in sorted(slides_dir.glob('slide*.xml')):
            slide_num = int(slide_file.stem.replace('slide', ''))

            tree = etree.parse(str(slide_file))
            root = tree.getroot()

            slide_data = {
                'title': None,
                'body': None,
            }

            # Get title placeholder
            title_shape = find_placeholder(root, 'title')
            if title_shape is not None:
                slide_data['title'] = get_placeholder_dimensions(title_shape)

            # Get body placeholder
            body_shape = find_placeholder(root, 'body')
            if body_shape is not None:
                slide_data['body'] = get_placeholder_dimensions(body_shape)

            sizes[slide_num] = slide_data

    with open(output_file, 'w') as f:
        json.dump(sizes, f, indent=2)

    print(f"Extracted placeholder sizes for {len(sizes)} slides to {output_file}")
    return sizes


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Test presentation migration')
    parser.add_argument('--batch', type=int, help='Run specific batch (1-5)')
    parser.add_argument('--test', type=str, help='Run specific test (e.g., 1a, 2b)')
    parser.add_argument('--extract-sizes', action='store_true', help='Extract placeholder sizes from template')
    args = parser.parse_args()

    print("=" * 60)
    print("Presentation Migration Test Harness")
    print("=" * 60)

    # Extract placeholder sizes if requested
    if args.extract_sizes:
        extract_all_placeholder_sizes(TEMPLATE_PATH, PLACEHOLDER_SIZES_FILE)
        return

    # Create output directory
    TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which batches to run
    batches_to_run = {}

    if args.test:
        # Find the test by ID
        for batch_name, tests in ALL_BATCHES.items():
            for test in tests:
                if test['id'] == args.test:
                    batches_to_run[batch_name] = [test]
                    break
        if not batches_to_run:
            print(f"Test '{args.test}' not found")
            sys.exit(1)
    elif args.batch:
        batch_map = {1: 'batch1_title', 2: 'batch2_stats', 3: 'batch3_content',
                     4: 'batch4_bullets', 5: 'batch5_detection'}
        batch_name = batch_map.get(args.batch)
        if batch_name:
            batches_to_run[batch_name] = ALL_BATCHES[batch_name]
        else:
            print(f"Batch {args.batch} not found")
            sys.exit(1)
    else:
        batches_to_run = ALL_BATCHES

    # Run tests
    all_results = {}
    for batch_name, tests in batches_to_run.items():
        print(f"\nRunning {batch_name}...")
        results = run_batch(batch_name, tests, TEST_OUTPUT_DIR)
        all_results[batch_name] = results

    # Write report
    write_validation_report(all_results, TEST_OUTPUT_DIR)

    # Summary
    total = sum(len(r) for r in all_results.values())
    passed = sum(1 for results in all_results.values() for r in results if r.get('passed'))

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)

    sys.exit(0 if passed == total else 1)


if __name__ == '__main__':
    main()
