#!/usr/bin/env python3
"""
Add new template slides for complex content types.

Creates:
- Stats Dashboard (4-6 stat zones)
- Case Study Full (description + bullets + quote)
- Logo Grid (title + image placeholders)

Usage:
    python add_template_slides.py
"""

import os
import sys
import zipfile
import shutil
import tempfile
from pathlib import Path
from lxml import etree

SCRIPT_DIR = Path(__file__).parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "templates/presentations/drupal-brand-template.pptx"
OUTPUT_PATH = SCRIPT_DIR.parent / "templates/presentations/drupal-brand-template-extended.pptx"

# Namespaces
NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

# Drupal brand colors
COLORS = {
    'blue': '009CDE',
    'dark_blue': '006AA9',
    'navy': '12285F',
    'light_blue': 'CCEDF9',
    'yellow': 'FFC423',
    'white': 'FFFFFF',
    'black': '000000',
}

# EMU conversions (914400 EMU = 1 inch)
INCH = 914400
SLIDE_WIDTH = int(24 * INCH)  # 24 inches (widescreen)
SLIDE_HEIGHT = int(13.5 * INCH)  # 13.5 inches


def create_text_shape(shape_id, name, x, y, width, height, text, font_size=2400, color='FFFFFF', bold=False):
    """Create a text box shape XML element.

    Args:
        shape_id: Unique shape ID
        name: Shape name
        x, y: Position in EMUs
        width, height: Size in EMUs
        text: Text content
        font_size: Size in hundredths of a point (2400 = 24pt)
        color: Hex color without #
        bold: Whether to bold the text
    """
    shape = etree.Element('{%s}sp' % NSMAP['p'])

    # Non-visual properties
    nvSpPr = etree.SubElement(shape, '{%s}nvSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(shape_id))
    cNvPr.set('name', name)
    cNvSpPr = etree.SubElement(nvSpPr, '{%s}cNvSpPr' % NSMAP['p'])
    cNvSpPr.set('txBox', '1')
    nvPr = etree.SubElement(nvSpPr, '{%s}nvPr' % NSMAP['p'])

    # Shape properties (position and size)
    spPr = etree.SubElement(shape, '{%s}spPr' % NSMAP['p'])
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NSMAP['a'])
    off = etree.SubElement(xfrm, '{%s}off' % NSMAP['a'])
    off.set('x', str(int(x)))
    off.set('y', str(int(y)))
    ext = etree.SubElement(xfrm, '{%s}ext' % NSMAP['a'])
    ext.set('cx', str(int(width)))
    ext.set('cy', str(int(height)))

    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NSMAP['a'])
    prstGeom.set('prst', 'rect')
    etree.SubElement(prstGeom, '{%s}avLst' % NSMAP['a'])
    etree.SubElement(spPr, '{%s}noFill' % NSMAP['a'])

    # Text body
    txBody = etree.SubElement(shape, '{%s}txBody' % NSMAP['p'])
    bodyPr = etree.SubElement(txBody, '{%s}bodyPr' % NSMAP['a'])
    bodyPr.set('wrap', 'square')
    bodyPr.set('anchor', 'ctr')
    etree.SubElement(txBody, '{%s}lstStyle' % NSMAP['a'])

    p = etree.SubElement(txBody, '{%s}p' % NSMAP['a'])
    pPr = etree.SubElement(p, '{%s}pPr' % NSMAP['a'])
    pPr.set('algn', 'ctr')

    r = etree.SubElement(p, '{%s}r' % NSMAP['a'])
    rPr = etree.SubElement(r, '{%s}rPr' % NSMAP['a'])
    rPr.set('lang', 'en-US')
    rPr.set('sz', str(font_size))
    if bold:
        rPr.set('b', '1')

    solidFill = etree.SubElement(rPr, '{%s}solidFill' % NSMAP['a'])
    srgbClr = etree.SubElement(solidFill, '{%s}srgbClr' % NSMAP['a'])
    srgbClr.set('val', color)

    t = etree.SubElement(r, '{%s}t' % NSMAP['a'])
    t.text = text

    return shape


def create_placeholder_shape(shape_id, name, ph_type, x, y, width, height, idx=None, text='Placeholder'):
    """Create a placeholder shape (title, body, etc.)."""
    shape = etree.Element('{%s}sp' % NSMAP['p'])

    # Non-visual properties
    nvSpPr = etree.SubElement(shape, '{%s}nvSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(shape_id))
    cNvPr.set('name', name)
    cNvSpPr = etree.SubElement(nvSpPr, '{%s}cNvSpPr' % NSMAP['p'])
    cNvSpPr.set('txBox', '1')
    nvPr = etree.SubElement(nvSpPr, '{%s}nvPr' % NSMAP['p'])

    # Placeholder definition
    ph = etree.SubElement(nvPr, '{%s}ph' % NSMAP['p'])
    ph.set('type', ph_type)
    if idx is not None:
        ph.set('idx', str(idx))

    # Shape properties
    spPr = etree.SubElement(shape, '{%s}spPr' % NSMAP['p'])
    xfrm = etree.SubElement(spPr, '{%s}xfrm' % NSMAP['a'])
    off = etree.SubElement(xfrm, '{%s}off' % NSMAP['a'])
    off.set('x', str(int(x)))
    off.set('y', str(int(y)))
    ext = etree.SubElement(xfrm, '{%s}ext' % NSMAP['a'])
    ext.set('cx', str(int(width)))
    ext.set('cy', str(int(height)))

    prstGeom = etree.SubElement(spPr, '{%s}prstGeom' % NSMAP['a'])
    prstGeom.set('prst', 'rect')
    etree.SubElement(prstGeom, '{%s}avLst' % NSMAP['a'])
    etree.SubElement(spPr, '{%s}noFill' % NSMAP['a'])

    # Text body
    txBody = etree.SubElement(shape, '{%s}txBody' % NSMAP['p'])
    bodyPr = etree.SubElement(txBody, '{%s}bodyPr' % NSMAP['a'])
    bodyPr.set('wrap', 'square')
    bodyPr.set('anchor', 't' if ph_type == 'body' else 'ctr')
    etree.SubElement(txBody, '{%s}lstStyle' % NSMAP['a'])

    p = etree.SubElement(txBody, '{%s}p' % NSMAP['a'])
    r = etree.SubElement(p, '{%s}r' % NSMAP['a'])
    rPr = etree.SubElement(r, '{%s}rPr' % NSMAP['a'])
    rPr.set('lang', 'en-US')
    t = etree.SubElement(r, '{%s}t' % NSMAP['a'])
    t.text = text

    return shape


def create_stats_dashboard_slide(base_id=500):
    """Create a stats dashboard slide with 6 stat zones.

    Layout:
    [Stat1] [Stat2] [Stat3]
    [Stat4] [Stat5] [Stat6]
    """
    # Create slide root
    sld = etree.Element('{%s}sld' % NSMAP['p'], nsmap=NSMAP)

    # Color slide
    cSld = etree.SubElement(sld, '{%s}cSld' % NSMAP['p'])

    # Background - Drupal Blue
    bg = etree.SubElement(cSld, '{%s}bg' % NSMAP['p'])
    bgPr = etree.SubElement(bg, '{%s}bgPr' % NSMAP['p'])
    solidFill = etree.SubElement(bgPr, '{%s}solidFill' % NSMAP['a'])
    srgbClr = etree.SubElement(solidFill, '{%s}srgbClr' % NSMAP['a'])
    srgbClr.set('val', COLORS['blue'])

    # Shape tree
    spTree = etree.SubElement(cSld, '{%s}spTree' % NSMAP['p'])

    # Group shape properties (required)
    nvGrpSpPr = etree.SubElement(spTree, '{%s}nvGrpSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvGrpSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(base_id))
    cNvPr.set('name', f'Shape {base_id}')
    etree.SubElement(nvGrpSpPr, '{%s}cNvGrpSpPr' % NSMAP['p'])
    etree.SubElement(nvGrpSpPr, '{%s}nvPr' % NSMAP['p'])

    grpSpPr = etree.SubElement(spTree, '{%s}grpSpPr' % NSMAP['p'])
    xfrm = etree.SubElement(grpSpPr, '{%s}xfrm' % NSMAP['a'])
    for elem in ['off', 'ext', 'chOff', 'chExt']:
        e = etree.SubElement(xfrm, '{%s}%s' % (NSMAP['a'], elem))
        e.set('x' if 'Off' in elem or elem == 'off' else 'cx', '0')
        e.set('y' if 'Off' in elem or elem == 'off' else 'cy', '0')

    # Add title placeholder
    title = create_placeholder_shape(
        base_id + 1, 'Title', 'title',
        x=1*INCH, y=0.5*INCH,
        width=22*INCH, height=1.5*INCH,
        text='Stats Dashboard Title'
    )
    spTree.append(title)

    # Add 6 stat zones (2 rows of 3)
    stat_width = 6 * INCH
    stat_height = 4 * INCH
    margin = 1.5 * INCH

    stats = [
        ('72%', 'Stat description 1'),
        ('1.4M', 'Stat description 2'),
        ('46K+', 'Stat description 3'),
        ('118k', 'Stat description 4'),
        ('12%', 'Stat description 5'),
        ('51%', 'Stat description 6'),
    ]

    for i, (number, label) in enumerate(stats):
        row = i // 3
        col = i % 3
        x = margin + col * (stat_width + 0.5*INCH)
        y = 2.5*INCH + row * (stat_height + 0.5*INCH)

        # Number (large)
        num_shape = create_text_shape(
            base_id + 10 + i*2, f'Stat{i+1}_Number',
            x, y, stat_width, 2*INCH,
            number, font_size=7200, color='FFFFFF', bold=True
        )
        spTree.append(num_shape)

        # Label (smaller)
        label_shape = create_text_shape(
            base_id + 11 + i*2, f'Stat{i+1}_Label',
            x, y + 2*INCH, stat_width, 1.5*INCH,
            label, font_size=1800, color='CCEDF9'
        )
        spTree.append(label_shape)

    # Color map override
    clrMapOvr = etree.SubElement(sld, '{%s}clrMapOvr' % NSMAP['p'])
    etree.SubElement(clrMapOvr, '{%s}masterClrMapping' % NSMAP['a'])

    return sld


def create_case_study_slide(base_id=600):
    """Create a case study slide with multiple content zones.

    Layout:
    [Logo]              [Screenshot]
    [Description]
    [Why Drupal:]       [Quote Box]
    [Bullets]           [Attribution]
    """
    sld = etree.Element('{%s}sld' % NSMAP['p'], nsmap=NSMAP)
    cSld = etree.SubElement(sld, '{%s}cSld' % NSMAP['p'])

    # White background
    bg = etree.SubElement(cSld, '{%s}bg' % NSMAP['p'])
    bgPr = etree.SubElement(bg, '{%s}bgPr' % NSMAP['p'])
    solidFill = etree.SubElement(bgPr, '{%s}solidFill' % NSMAP['a'])
    srgbClr = etree.SubElement(solidFill, '{%s}srgbClr' % NSMAP['a'])
    srgbClr.set('val', COLORS['white'])

    spTree = etree.SubElement(cSld, '{%s}spTree' % NSMAP['p'])

    # Group properties
    nvGrpSpPr = etree.SubElement(spTree, '{%s}nvGrpSpPr' % NSMAP['p'])
    cNvPr = etree.SubElement(nvGrpSpPr, '{%s}cNvPr' % NSMAP['p'])
    cNvPr.set('id', str(base_id))
    cNvPr.set('name', f'Shape {base_id}')
    etree.SubElement(nvGrpSpPr, '{%s}cNvGrpSpPr' % NSMAP['p'])
    etree.SubElement(nvGrpSpPr, '{%s}nvPr' % NSMAP['p'])

    grpSpPr = etree.SubElement(spTree, '{%s}grpSpPr' % NSMAP['p'])
    xfrm = etree.SubElement(grpSpPr, '{%s}xfrm' % NSMAP['a'])
    for elem in ['off', 'ext', 'chOff', 'chExt']:
        e = etree.SubElement(xfrm, '{%s}%s' % (NSMAP['a'], elem))
        e.set('x' if 'Off' in elem or elem == 'off' else 'cx', '0')
        e.set('y' if 'Off' in elem or elem == 'off' else 'cy', '0')

    # Title placeholder (company name)
    title = create_placeholder_shape(
        base_id + 1, 'Title', 'title',
        x=1*INCH, y=0.5*INCH,
        width=10*INCH, height=1*INCH,
        text='Company Name'
    )
    spTree.append(title)

    # Description (body placeholder)
    desc = create_placeholder_shape(
        base_id + 2, 'Description', 'body',
        x=1*INCH, y=2*INCH,
        width=10*INCH, height=3*INCH,
        idx=1,
        text='Company description and what they did with Drupal.'
    )
    spTree.append(desc)

    # Bullets section
    bullets = create_placeholder_shape(
        base_id + 3, 'Bullets', 'body',
        x=1*INCH, y=5.5*INCH,
        width=10*INCH, height=4*INCH,
        idx=2,
        text='Why Drupal was chosen:\n• Bullet 1\n• Bullet 2\n• Bullet 3'
    )
    spTree.append(bullets)

    # Quote box (right side, Navy background)
    quote = create_text_shape(
        base_id + 4, 'Quote',
        x=12*INCH, y=6.5*INCH,
        width=10*INCH, height=5*INCH,
        text='"Quote from the customer about their experience with Drupal."',
        font_size=2400, color='FFFFFF', bold=True
    )
    spTree.append(quote)

    # Attribution
    attr = create_text_shape(
        base_id + 5, 'Attribution',
        x=12*INCH, y=11*INCH,
        width=10*INCH, height=1*INCH,
        text='— Name, Title at Company',
        font_size=1600, color='CCEDF9'
    )
    spTree.append(attr)

    clrMapOvr = etree.SubElement(sld, '{%s}clrMapOvr' % NSMAP['p'])
    etree.SubElement(clrMapOvr, '{%s}masterClrMapping' % NSMAP['a'])

    return sld


def add_slides_to_template():
    """Add new template slides to the PPTX file."""
    print(f"Adding new template slides...")
    print(f"Source: {TEMPLATE_PATH}")
    print(f"Output: {OUTPUT_PATH}")

    if not TEMPLATE_PATH.exists():
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)

        # Extract template
        with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zf:
            zf.extractall(work_dir)

        slides_dir = work_dir / 'ppt/slides'
        rels_dir = slides_dir / '_rels'

        # Count existing slides
        existing_slides = len(list(slides_dir.glob('slide*.xml')))
        print(f"Existing slides: {existing_slides}")

        # Create new slides
        new_slides = [
            (create_stats_dashboard_slide(500), 'stats_dashboard'),
            (create_case_study_slide(600), 'case_study_full'),
        ]

        for i, (slide_xml, slide_type) in enumerate(new_slides):
            slide_num = existing_slides + i + 1
            slide_path = slides_dir / f'slide{slide_num}.xml'

            # Write slide XML
            tree = etree.ElementTree(slide_xml)
            tree.write(str(slide_path), xml_declaration=True, encoding='UTF-8', standalone=True)
            print(f"Created slide {slide_num}: {slide_type}")

            # Create relationships file
            rels_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>'''
            rels_path = rels_dir / f'slide{slide_num}.xml.rels'
            rels_path.write_text(rels_content)

        # Update Content_Types.xml
        ct_path = work_dir / '[Content_Types].xml'
        ct_tree = etree.parse(str(ct_path))
        ct_root = ct_tree.getroot()
        ct_ns = 'http://schemas.openxmlformats.org/package/2006/content-types'

        for i in range(len(new_slides)):
            slide_num = existing_slides + i + 1
            override = etree.SubElement(ct_root, f'{{{ct_ns}}}Override')
            override.set('PartName', f'/ppt/slides/slide{slide_num}.xml')
            override.set('ContentType', 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml')

        ct_tree.write(str(ct_path), xml_declaration=True, encoding='UTF-8', standalone=True)

        # Update presentation.xml.rels
        pres_rels_path = work_dir / 'ppt/_rels/presentation.xml.rels'
        pres_rels_tree = etree.parse(str(pres_rels_path))
        pres_rels_root = pres_rels_tree.getroot()
        rels_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'

        # Find max rId
        max_rid = 0
        for rel in pres_rels_root:
            rid = rel.get('Id', 'rId0')
            num = int(rid.replace('rId', ''))
            max_rid = max(max_rid, num)

        for i in range(len(new_slides)):
            slide_num = existing_slides + i + 1
            rel = etree.SubElement(pres_rels_root, f'{{{rels_ns}}}Relationship')
            rel.set('Id', f'rId{max_rid + i + 1}')
            rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
            rel.set('Target', f'slides/slide{slide_num}.xml')

        pres_rels_tree.write(str(pres_rels_path), xml_declaration=True, encoding='UTF-8', standalone=True)

        # Update presentation.xml
        pres_path = work_dir / 'ppt/presentation.xml'
        pres_tree = etree.parse(str(pres_path))
        pres_root = pres_tree.getroot()
        pres_ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}

        sld_id_lst = pres_root.find('.//p:sldIdLst', pres_ns)
        if sld_id_lst is not None:
            # Find max slide ID
            max_sld_id = 256
            for sld_id in sld_id_lst:
                sid = int(sld_id.get('id', '256'))
                max_sld_id = max(max_sld_id, sid)

            for i in range(len(new_slides)):
                sld_id = etree.SubElement(sld_id_lst, f'{{{pres_ns["p"]}}}sldId')
                sld_id.set('id', str(max_sld_id + i + 1))
                sld_id.set(f'{{{NSMAP["r"]}}}id', f'rId{max_rid + i + 1}')

        pres_tree.write(str(pres_path), xml_declaration=True, encoding='UTF-8', standalone=True)

        # Create output PPTX
        with zipfile.ZipFile(OUTPUT_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root_path, dirs, files in os.walk(work_dir):
                for file in files:
                    file_path = Path(root_path) / file
                    arc_path = file_path.relative_to(work_dir)
                    zf.write(file_path, arc_path)

        print(f"\nCreated: {OUTPUT_PATH}")
        print(f"New slides added at indices {existing_slides + 1}-{existing_slides + len(new_slides)}")

        return existing_slides + 1, existing_slides + len(new_slides)


if __name__ == '__main__':
    add_slides_to_template()
