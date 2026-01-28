#!/usr/bin/env python3
"""
Drupal Brand Presentation Migration Tool

Intelligently maps content to varied template layouts with:
- Content-type detection (stats, quotes, features, bullets, etc.)
- Layout variety tracking (no consecutive repeats)
- Left/right orientation alternation
- GUI block color rotation

Supports:
- PPTX input (auto-extracts content)
- Markdown input (structured slide content)
- CSV input (spreadsheet format)

Outputs brand-compliant PPTX using the Drupal template.
"""

import re
import os
import csv
import json
import sys
from pathlib import Path
from lxml import etree
import shutil
import zipfile
import tempfile
from datetime import datetime
from collections import deque

# Default paths (relative to skill directory)
SKILL_DIR = Path(__file__).parent
TEMPLATE_PATH = SKILL_DIR.parent / "templates/presentations/drupal-brand-template.pptx"

# ============================================================
# SLIDE CATALOG - All available template slides
# ============================================================

# Slide categories with their template indices
SLIDE_CATALOG = {
    # Opening slides
    'title_opening': [0],           # SLIDE-TITLE-SPEAKER - Blue bg, speaker info
    'hero_photo': [1],              # SLIDE-HERO-PHOTO - Photo bg with Navy GUI block
    'statement_center': [3, 33],    # Centered statements - Light pattern bg

    # Section dividers
    'section_divider': [40],        # Blue bg, large title

    # Content with image LEFT (text on right)
    'content_image_left': [38],     # SLIDE-CONTENT-RIGHT - Blue bg, white GUI frame

    # Content with image RIGHT (text on left)
    'content_image_right': [2, 9],  # Yellow bg (2) or White bg with photo grid (9)

    # Feature slides with bullets (various colors)
    'feature_blue_bg': [21],        # Blue background, yellow GUI frame
    'feature_yellow_bg': [2],       # Yellow background
    'feature_white_bg': [9, 20],    # White background variations
    'feature_coral_gui': [19],      # White bg, coral filled GUI block
    'feature_yellow_gui': [18],     # White bg, yellow filled GUI block

    # Statistics slides (8 variations!)
    'stat_outline_gui': [10],       # Navy/Yellow/Blue outline GUI, stat on left
    'stat_coral_filled': [11, 12],  # Coral filled GUI block
    'stat_photo_left': [13, 14],    # Photo on left with stat
    'stat_navy_filled': [15, 16],   # Navy filled GUI block
    'stat_photo_bg': [16, 17],      # Full photo background

    # Quote slides
    'quote_navy_bg': [8],           # Navy bg, white GUI block with attribution
    'quote_centered': [41],         # Navy bg, centered in white GUI block

    # Two-column layouts
    'two_column': [42, 44],         # Comparison, before/after, pros/cons

    # Photo feature slides
    'photo_text_left': [35],        # Full photo bg, Blue GUI block on left
    'photo_text_right': [47],       # White bg, Navy GUI block on left

    # Speaker/bio slides
    'speaker_bio': [36],            # Photo in pink GUI, bio on right

    # Numbered content (step-by-step)
    'numbered_02': [29],            # Coral filled GUI
    'numbered_03': [30],            # Blue outline GUI
    'numbered_04': [31],            # Yellow filled GUI
    'numbered_05': [32],            # Coral outline GUI

    # Closing slides
    'closing_cta': [33],            # Light pattern, centered CTA
    'closing_statement': [46],      # White bg, light blue GUI block

    # Blank/flexible templates
    'blank_title_image': [27],      # Title left, image right
    'blank_full_image': [28],       # Full-bleed image right
}

# Content type detection patterns
CONTENT_PATTERNS = {
    'statistic': [
        r'^\d+%',                    # Starts with percentage
        r'^\$[\d,]+',               # Dollar amounts
        r'^[\d,]+\+?\s*(million|billion|users|websites|developers|organizations)',
        r'^\d+x',                    # Multipliers like "10x"
        r'^\d+/\d+',                # Fractions
    ],
    'quote': [
        r'^["""]',                   # Starts with quote mark
        r'^\s*—',                    # Attribution dash
        r'said\s+\w+',              # "said [Name]"
    ],
    'numbered_step': [
        r'^(step\s*)?\d+[.:\)]',    # "Step 1:" or "1." or "1)"
        r'^(first|second|third|fourth|fifth)',
    ],
    'bullet_list': [
        r'^\s*[-•▪]\s+',            # Bullet markers
        r'\n\s*[-•▪]\s+',           # Multiple bullets
    ],
    'comparison': [
        r'\bvs\.?\b',               # "vs" or "vs."
        r'\bbefore\b.*\bafter\b',   # Before/after
        r'\bpros?\b.*\bcons?\b',    # Pros/cons
    ],
}

# Orientation tracking
ORIENTATIONS = {
    'left': ['content_image_left', 'photo_text_left', 'stat_photo_left'],
    'right': ['content_image_right', 'photo_text_right', 'feature_white_bg'],
    'center': ['statement_center', 'quote_centered', 'section_divider', 'closing_cta'],
}

# Text capacity estimates per layout category
# Based on placeholder dimensions from SLIDE-CATALOG.md
# Values are (title_max_chars, body_max_chars, recommended_title_pt, recommended_body_pt)
# Character limits are generous - font scaling handles overflow
TEXT_CAPACITY = {
    # Opening slides - large titles, minimal body
    'title_opening': (200, 150, 3600, 1800),      # Big title, small speaker info
    'hero_photo': (150, 300, 3600, 1400),         # Title in GUI block
    'statement_center': (200, 300, 3200, 1600),   # Centered statement

    # Section dividers - allow longer titles
    'section_divider': (150, 300, 4000, 1800),    # Large section title

    # Content with image (half slide for text)
    'content_image_left': (150, 500, 2400, 1400),   # Title + body on right
    'content_image_right': (150, 500, 2400, 1400),  # Title + body on left

    # Feature slides - medium text areas
    'feature_blue_bg': (150, 500, 2400, 1400),
    'feature_yellow_bg': (150, 500, 2400, 1400),
    'feature_white_bg': (150, 500, 2400, 1400),
    'feature_coral_gui': (150, 500, 2400, 1400),
    'feature_yellow_gui': (150, 500, 2400, 1400),

    # Statistics - large number, supporting text
    'stat_outline_gui': (50, 500, 7200, 1400),    # Big stat number
    'stat_coral_filled': (50, 500, 7200, 1400),
    'stat_photo_left': (50, 500, 7200, 1400),
    'stat_navy_filled': (50, 500, 7200, 1400),
    'stat_photo_bg': (50, 400, 7200, 1400),

    # Quotes - medium quote, short attribution
    'quote_navy_bg': (300, 200, 2400, 1600),       # Quote text + attribution
    'quote_centered': (300, 200, 2800, 1400),     # Quote only

    # Two-column - split content
    'two_column': (100, 600, 2400, 1200),          # Two columns of bullets

    # Photo features
    'photo_text_left': (150, 300, 2800, 1400),    # Statement in GUI block
    'photo_text_right': (150, 400, 2400, 1400),

    # Speaker bio
    'speaker_bio': (100, 500, 3200, 1400),         # Name + bio bullets

    # Numbered content
    'numbered_02': (50, 500, 7200, 1400),         # Large number + body
    'numbered_03': (50, 500, 7200, 1400),
    'numbered_04': (50, 500, 7200, 1400),
    'numbered_05': (50, 500, 7200, 1400),

    # Closing
    'closing_cta': (200, 200, 3200, 1800),
    'closing_statement': (300, 200, 2000, 1400),

    # Blank/flexible
    'blank_title_image': (200, 300, 2800, 1400),
    'blank_full_image': (200, 300, 2800, 1400),

    # Default
    'default': (150, 500, 2400, 1400),
}

NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def clean_text(text):
    """Remove control characters that break XML."""
    if not text:
        return ""
    cleaned = ''.join(c if ord(c) >= 32 or c in '\n\t' else ' ' for c in str(text))
    return cleaned.strip()


# ============================================================
# CONTENT TYPE DETECTION
# ============================================================

def detect_content_type(slide):
    """Analyze slide content to determine the best content type."""
    title = slide.get('title', '').strip()
    body = slide.get('body', '').strip()
    combined = f"{title}\n{body}".lower()
    slide_num = slide.get('number', 0)

    # Check for statistics (numbers, percentages) in title OR body
    stat_patterns_title = [
        r'^\d+%',                    # Starts with percentage
        r'^\$[\d,]+',               # Dollar amounts
        r'^[\d,]+\+?\s*(million|billion|users|websites|developers|organizations)',
        r'^\d+x',                    # Multipliers like "10x"
        r'^\d+/\d+',                # Fractions
        r'^#\d+',                   # Rankings like "#1"
    ]
    stat_patterns_anywhere = [
        r'\b\d{2,}%\b',             # Any percentage 10%+
        r'\b\d+\s*(million|billion)\b',  # Large numbers
        r'\bover\s+\d+',            # "over 100"
        r'\bmore than\s+\d+',       # "more than 500"
    ]

    for pattern in stat_patterns_title:
        if re.search(pattern, title, re.IGNORECASE):
            return 'statistic'

    # Stats anywhere in content (less strict)
    for pattern in stat_patterns_anywhere:
        if re.search(pattern, combined, re.IGNORECASE):
            return 'statistic'

    # Check for quotes
    for pattern in CONTENT_PATTERNS['quote']:
        if re.search(pattern, title) or re.search(pattern, body):
            return 'quote'

    # Check for numbered steps or sequence indicators
    step_patterns = [
        r'^(step\s*)?\d+[.:\)]',    # "Step 1:" or "1." or "1)"
        r'^(first|second|third|fourth|fifth)',
        r'\bphase\s*\d+',           # "Phase 1"
        r'\bpart\s*\d+',            # "Part 1"
    ]
    for pattern in step_patterns:
        if re.search(pattern, title, re.IGNORECASE):
            return 'numbered_step'

    # Check for comparison/two-column content
    for pattern in CONTENT_PATTERNS['comparison']:
        if re.search(pattern, combined):
            return 'comparison'

    # Check for bullet lists (more than 2 bullets)
    bullet_count = len(re.findall(r'^\s*[-•▪]', body, re.MULTILINE))
    if bullet_count >= 3:
        return 'bullet_list'

    # Testimonial/case study indicators (check before section_header)
    case_study_keywords = ['customer', 'client', 'case study', 'success story',
                          'testimonial', 'partner', 'rebuilt', 'transformed',
                          'organization']
    if any(kw in combined for kw in case_study_keywords):
        return 'case_study'

    # "How X did Y" patterns (case studies)
    how_patterns = [
        r'\bhow\s+\w+\s+(rebuilt|transformed|migrated|updated|launched)',
    ]
    for pattern in how_patterns:
        if re.search(pattern, combined, re.IGNORECASE):
            return 'case_study'

    # Section headers - short titles, typically section dividers
    # Note: "how" as standalone section header (e.g., "How It Works") but not "How NASA rebuilt..."
    section_keywords = ['overview', 'introduction', 'summary', 'agenda', 'contents',
                        'why', 'what is', 'features', 'benefits', 'resources']
    title_lower = title.lower()
    # "how" only if it's near the start and title is short (typical section header pattern)
    if title_lower.startswith('how ') and len(title) < 30:
        return 'section_header'
    if any(kw in title_lower for kw in section_keywords) and len(title) < 80:
        return 'section_header'

    # Short punchy titles = statements
    if len(title) > 20 and len(title) < 80 and len(body) < 100:
        return 'statement'

    # Feature keywords
    feature_keywords = ['feature', 'capability', 'integration', 'benefit',
                       'advantage', 'solution', 'powerful', 'flexible']
    if any(kw in combined for kw in feature_keywords):
        return 'feature'

    # Default based on content length - but add variety
    if len(body) > 200:
        # Rotate between different "long content" categories
        # Use slide number to create variety
        content_types_for_long = ['detailed_content', 'feature', 'bullet_list']
        return content_types_for_long[slide_num % len(content_types_for_long)]

    return 'feature'


def detect_slide_position(slide_num, total_slides):
    """Determine if slide is opening, closing, or middle."""
    if slide_num <= 2:
        return 'opening'
    elif slide_num >= total_slides - 2:
        return 'closing'
    elif slide_num % 10 == 0 or slide_num % 10 == 1:
        # Every ~10 slides might be a section break
        return 'section_break'
    else:
        return 'middle'


# ============================================================
# INTELLIGENT LAYOUT SELECTION
# ============================================================

class LayoutSelector:
    """Selects varied layouts based on content type and recent history."""

    def __init__(self):
        # Track last 3 used slide indices to avoid repetition
        self.recent_slides = deque(maxlen=3)
        # Track last orientation (left/right/center)
        self.last_orientation = None
        # Track GUI color rotation
        self.gui_color_index = 0
        self.gui_colors = ['blue', 'coral', 'yellow', 'navy']
        # Numbered step counter
        self.step_counter = 2  # Start at 02

    def get_opposite_orientation(self):
        """Return opposite of last orientation."""
        if self.last_orientation == 'left':
            return 'right'
        elif self.last_orientation == 'right':
            return 'left'
        return 'center'

    def rotate_gui_color(self):
        """Get next GUI color in rotation."""
        color = self.gui_colors[self.gui_color_index]
        self.gui_color_index = (self.gui_color_index + 1) % len(self.gui_colors)
        return color

    def select_layout(self, slide, slide_num, total_slides):
        """Select the best template slide index for this content."""
        content_type = detect_content_type(slide)
        position = detect_slide_position(slide_num, total_slides)

        # Determine candidate categories based on content type and position
        candidates = self._get_candidates(content_type, position)

        # Filter out recently used slides
        available = []
        for cat in candidates:
            for idx in SLIDE_CATALOG.get(cat, []):
                if idx not in self.recent_slides:
                    available.append((cat, idx))

        # If all candidates were recently used, just use the candidates anyway
        if not available:
            for cat in candidates:
                for idx in SLIDE_CATALOG.get(cat, []):
                    available.append((cat, idx))

        # Select based on orientation preference
        preferred_orientation = self.get_opposite_orientation()

        # Try to find a slide with preferred orientation
        for cat, idx in available:
            for orient, cats in ORIENTATIONS.items():
                if cat in cats and orient == preferred_orientation:
                    self._record_selection(idx, orient)
                    return idx, cat

        # Fall back to first available
        if available:
            cat, idx = available[0]
            # Determine orientation of selected
            for orient, cats in ORIENTATIONS.items():
                if cat in cats:
                    self._record_selection(idx, orient)
                    return idx, cat
            self._record_selection(idx, 'center')
            return idx, cat

        # Ultimate fallback
        self._record_selection(3, 'center')
        return 3, 'default'

    def _get_candidates(self, content_type, position):
        """Get candidate categories for content type and position."""
        # Opening slides
        if position == 'opening':
            if content_type == 'statistic':
                return ['stat_outline_gui', 'stat_coral_filled']
            return ['title_opening', 'hero_photo', 'statement_center']

        # Closing slides
        if position == 'closing':
            return ['closing_cta', 'closing_statement', 'statement_center']

        # Section breaks
        if position == 'section_break':
            return ['section_divider', 'statement_center']

        # Content-based selection
        if content_type == 'statistic':
            gui_color = self.rotate_gui_color()
            if gui_color == 'coral':
                return ['stat_coral_filled', 'stat_outline_gui']
            elif gui_color == 'navy':
                return ['stat_navy_filled', 'stat_photo_bg']
            elif gui_color == 'yellow':
                return ['stat_outline_gui', 'stat_photo_left']
            else:
                return ['stat_photo_bg', 'stat_coral_filled']

        if content_type == 'quote':
            return ['quote_navy_bg', 'quote_centered']

        if content_type == 'numbered_step':
            step_map = {
                2: 'numbered_02',
                3: 'numbered_03',
                4: 'numbered_04',
                5: 'numbered_05',
            }
            step = self.step_counter
            self.step_counter = (self.step_counter % 4) + 2  # Cycle 2-5
            return [step_map.get(step, 'numbered_02')]

        if content_type == 'comparison':
            return ['two_column']

        if content_type == 'section_header':
            return ['section_divider', 'statement_center', 'hero_photo']

        if content_type == 'case_study':
            gui_color = self.rotate_gui_color()
            if gui_color == 'coral':
                return ['stat_coral_filled', 'feature_coral_gui']
            elif gui_color == 'navy':
                return ['photo_text_right', 'content_image_left']
            else:
                return ['quote_navy_bg', 'photo_text_left']

        if content_type == 'bullet_list':
            gui_color = self.rotate_gui_color()
            if gui_color == 'yellow':
                return ['feature_yellow_gui', 'feature_yellow_bg']
            elif gui_color == 'coral':
                return ['feature_coral_gui', 'feature_blue_bg']
            elif gui_color == 'navy':
                return ['content_image_left', 'feature_white_bg']
            else:
                return ['feature_blue_bg', 'feature_white_bg']

        if content_type == 'statement':
            gui_color = self.rotate_gui_color()
            if gui_color == 'navy':
                return ['hero_photo', 'photo_text_right']
            elif gui_color == 'coral':
                return ['statement_center', 'closing_statement']
            else:
                return ['statement_center', 'photo_text_left', 'hero_photo']

        if content_type == 'detailed_content':
            # Rotate through different detailed content layouts
            gui_color = self.rotate_gui_color()
            if gui_color == 'yellow':
                return ['feature_yellow_bg', 'content_image_right']
            elif gui_color == 'coral':
                return ['feature_coral_gui', 'content_image_left']
            elif gui_color == 'navy':
                return ['content_image_left', 'photo_text_right']
            else:
                return ['content_image_right', 'feature_white_bg']

        # Default feature slides with rotation
        gui_color = self.rotate_gui_color()
        if gui_color == 'yellow':
            return ['feature_yellow_bg', 'feature_yellow_gui', 'content_image_right']
        elif gui_color == 'coral':
            return ['feature_coral_gui', 'stat_coral_filled', 'numbered_02']
        elif gui_color == 'navy':
            return ['content_image_left', 'photo_text_right', 'feature_blue_bg']
        else:
            return ['content_image_right', 'feature_white_bg', 'feature_blue_bg']

    def _record_selection(self, idx, orientation):
        """Record the selected slide for history tracking."""
        self.recent_slides.append(idx)
        self.last_orientation = orientation


# ============================================================
# INPUT PARSERS
# ============================================================

def parse_markdown(md_path):
    """Parse markdown file to extract slides.

    Supports two formats:
    1. "## Slide X" followed by **Layout:**, **Title:**, ### Content
    2. "### Slide X - Name" followed by **Layout:**, **Title:**, **Text:**
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = []

    # Try format 1: "## Slide X"
    pattern1 = r'## Slide (\d+)\n(.*?)(?=\n## Slide \d+|\n*$)'
    matches1 = re.findall(pattern1, content, re.DOTALL)

    # Try format 2: "### Slide X - Name"
    pattern2 = r'### Slide (\d+)[^\n]*\n(.*?)(?=\n### Slide \d+|\n---\n*$|\Z)'
    matches2 = re.findall(pattern2, content, re.DOTALL)

    # Use whichever format found more slides
    matches = matches1 if len(matches1) >= len(matches2) else matches2

    for num, slide_content in matches:
        slide = {'number': int(num), 'layout': 'DEFAULT', 'title': '', 'body': ''}

        # Extract layout
        layout_match = re.search(r'\*\*Layout:\*\*\s*(\w+(?:_\w+)*)', slide_content)
        if layout_match:
            slide['layout'] = layout_match.group(1).upper()

        # Extract title - stop at any ** marker or ### or ---
        title_match = re.search(r'\*\*Title:\*\*\s*([^\n]*?)(?=\n|$)', slide_content)
        if title_match:
            title_text = title_match.group(1).strip()
            # Filter out metadata that might have been captured
            if not title_text.startswith('**') and title_text not in ['0', '1', '2']:
                slide['title'] = clean_text(title_text)

        # Extract body - try multiple formats
        body_text = ''

        # Format 1: "### Content" section
        content_match = re.search(r'### Content\n(.*?)(?=\n---|\Z)', slide_content, re.DOTALL)
        if content_match:
            body_text = content_match.group(1).strip()

        # Format 2: "**Text:**" section
        if not body_text:
            text_match = re.search(r'\*\*Text:\*\*\s*(.*?)(?=\n\*\*[A-Z]|\n---|\Z)', slide_content, re.DOTALL)
            if text_match:
                body_text = text_match.group(1).strip()

        # Format 3: Bullet points after title
        if not body_text:
            bullets = re.findall(r'^\s*[-•]\s+(.+)$', slide_content, re.MULTILINE)
            if bullets:
                body_text = '\n'.join(bullets)

        if body_text:
            lines = [clean_text(l) for l in body_text.split('\n') if l.strip()]
            # Filter out metadata, duplicates, and common repeated headers
            title_line = slide['title'].split('\n')[0].strip() if slide['title'] else ''
            filtered_lines = []
            seen = set()

            # Common section headers that appear on multiple slides
            skip_phrases = [
                "WHY YOU'LL LOVE DRUPAL",
                "WHY YOU",  # Catches curly apostrophe variant too
                'CASE STUDIES',
                'RESOURCES',
                'Photo:',
                'Image:',
                'https://',
                'http://',
            ]

            for l in lines:
                # Skip metadata lines
                if l.startswith('**') or l in ['0', '1', '2']:
                    continue
                # Skip title duplicates
                if l == title_line:
                    continue
                # Skip common section headers and photo credits
                if any(skip in l for skip in skip_phrases):
                    continue
                # Skip exact duplicates
                if l in seen:
                    continue
                # Skip very short lines that are likely artifacts
                if len(l) < 3:
                    continue
                seen.add(l)
                filtered_lines.append(l)

            slide['body'] = '\n'.join(filtered_lines[:15])

        # If title is empty but body has content, use first line as title
        if not slide['title'] and slide['body']:
            body_lines = slide['body'].split('\n')
            if body_lines:
                slide['title'] = body_lines[0]
                slide['body'] = '\n'.join(body_lines[1:])

        slides.append(slide)

    return slides


def parse_csv(csv_path):
    """Parse CSV file to extract slides."""
    slides = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slide = {
                'number': int(row.get('slide_number', len(slides) + 1)),
                'layout': row.get('layout', 'DEFAULT').upper(),
                'title': clean_text(row.get('title', '')),
                'body': clean_text(row.get('body', '')),
            }
            slides.append(slide)
    return slides


def parse_pptx(pptx_path):
    """Extract content from PPTX file."""
    slides = []

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)

        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(work_dir)

        slides_dir = work_dir / 'ppt/slides'

        # Get all slide files
        slide_files = sorted(
            [f for f in slides_dir.glob('slide*.xml')],
            key=lambda x: int(re.search(r'slide(\d+)', x.name).group(1))
        )

        for slide_file in slide_files:
            num = int(re.search(r'slide(\d+)', slide_file.name).group(1))
            tree = etree.parse(str(slide_file))
            root = tree.getroot()

            # Extract text
            texts = []
            for t in root.xpath('.//a:t', namespaces=NSMAP):
                if t.text:
                    texts.append(clean_text(t.text))

            # Get layout from rels
            layout = 'DEFAULT'
            rels_file = slides_dir / f'_rels/slide{num}.xml.rels'
            if rels_file.exists():
                rels_tree = etree.parse(str(rels_file))
                for rel in rels_tree.getroot():
                    target = rel.get('Target', '')
                    if 'slideLayout' in target:
                        layout_num = re.search(r'slideLayout(\d+)', target)
                        if layout_num:
                            # Map layout number to type (simplified)
                            layout = 'DEFAULT'

            slide = {
                'number': num,
                'layout': layout,
                'title': texts[0] if texts else '',
                'body': '\n'.join(texts[1:5]) if len(texts) > 1 else '',
            }
            slides.append(slide)

    return slides


def detect_and_parse(input_path):
    """Detect input format and parse accordingly."""
    path = Path(input_path)
    suffix = path.suffix.lower()

    if suffix == '.md':
        print(f"Detected Markdown input: {path.name}")
        return parse_markdown(path)
    elif suffix == '.csv':
        print(f"Detected CSV input: {path.name}")
        return parse_csv(path)
    elif suffix in ['.pptx', '.ppt']:
        print(f"Detected PPTX input: {path.name}")
        return parse_pptx(path)
    else:
        raise ValueError(f"Unsupported input format: {suffix}")


# ============================================================
# MIGRATION ENGINE
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


def get_placeholder_width(shape):
    """Get placeholder width in EMUs for font scaling."""
    if shape is None:
        return None

    xfrm = shape.find('.//a:xfrm', namespaces=NSMAP)
    if xfrm is None:
        return None

    ext = xfrm.find('a:ext', namespaces=NSMAP)
    if ext is None:
        return None

    return int(ext.get('cx', 0))


def calculate_font_size(text, placeholder_width_emu, max_size, min_size):
    """Determine font size that fits text in placeholder.

    Args:
        text: The text to fit
        placeholder_width_emu: Width in EMUs
        max_size: Maximum font size in hundredths of a point
        min_size: Minimum font size in hundredths of a point

    Returns:
        Appropriate font size in hundredths of a point
    """
    if not text or not placeholder_width_emu:
        return max_size

    # Approximate: 1 character at 100pt ≈ 70000 EMUs wide (depends on font)
    # This is a rough estimate - actual width varies by character
    char_width_at_100pt = 60000  # Conservative estimate

    for size in range(max_size, min_size - 1, -200):  # Step by 2pt
        scale = size / 10000  # Convert hundredths to points ratio
        estimated_width = len(text) * char_width_at_100pt * scale
        if estimated_width <= placeholder_width_emu * 0.95:  # 5% margin
            return size

    return min_size


def replace_text_in_placeholder(root, ph_type, new_text, font_size=None, idx=None):
    """Replace text in a specific placeholder by type.

    This is the CORRECT approach - targeting placeholders, not arbitrary text runs.

    Args:
        root: XML root element
        ph_type: Placeholder type ('title', 'body')
        new_text: Text to insert
        font_size: Optional font size in hundredths of a point
        idx: Optional placeholder index

    Returns:
        True if replacement was successful
    """
    shape = find_placeholder(root, ph_type, idx)
    if shape is None:
        return False

    # Find all text runs in this shape
    text_runs = shape.xpath('.//a:t', namespaces=NSMAP)

    if not text_runs:
        return False

    # Replace first text run with the new content
    text_runs[0].text = new_text

    # Set font size if specified
    if font_size:
        set_font_size(text_runs[0], font_size)

    # Clear subsequent text runs in this placeholder
    for t in text_runs[1:]:
        t.text = ""

    return True


def replace_text_in_slide(slide_path, new_title, new_body, title_font_size=2400, body_font_size=1400):
    """Replace text in slide XML with proper placeholder targeting.

    Uses placeholder type detection instead of arbitrary text run replacement.
    Falls back to text boxes when standard placeholders aren't found.

    Font sizes are in hundredths of a point:
    - 1200 = 12pt
    - 1400 = 14pt (default body)
    - 1800 = 18pt
    - 2400 = 24pt (default title)
    - 3600 = 36pt
    """
    tree = etree.parse(str(slide_path))
    root = tree.getroot()

    # Find placeholders by type
    title_shape = find_placeholder(root, 'title')
    body_shape = find_placeholder(root, 'body')

    # Try body with idx="1" first (common in templates)
    if body_shape is None:
        body_shape = find_placeholder(root, 'body', idx='1')

    # Fallback to text boxes if no standard placeholders
    text_boxes = None
    if title_shape is None or body_shape is None:
        text_boxes = find_text_boxes(root)
        if text_boxes:
            if title_shape is None and len(text_boxes) >= 1:
                title_shape = text_boxes[0]
            if body_shape is None and len(text_boxes) >= 2:
                body_shape = text_boxes[1]

    # Calculate font sizes based on placeholder dimensions
    if title_shape and new_title:
        title_width = get_placeholder_width(title_shape)
        if title_width:
            title_font_size = calculate_font_size(
                new_title, title_width, title_font_size, 1800  # Min 18pt for titles
            )

    if body_shape and new_body:
        body_width = get_placeholder_width(body_shape)
        if body_width:
            body_font_size = calculate_font_size(
                new_body, body_width, body_font_size, 1200  # Min 12pt for body
            )

    # Replace text in the correct placeholders
    title_replaced = False
    body_replaced = False

    if new_title:
        # Try standard placeholder first
        title_replaced = replace_text_in_placeholder(root, 'title', new_title, title_font_size)
        # If no placeholder, try text box
        if not title_replaced and text_boxes and len(text_boxes) >= 1:
            title_replaced = _replace_text_in_shape(text_boxes[0], new_title, title_font_size)
        # Ultimate fallback
        if not title_replaced:
            title_replaced = _fallback_replace_first_text(root, new_title, title_font_size)

    if new_body:
        # Try body placeholder with idx="1"
        body_replaced = replace_text_in_placeholder(root, 'body', new_body, body_font_size, idx='1')
        # Try body without idx
        if not body_replaced:
            body_replaced = replace_text_in_placeholder(root, 'body', new_body, body_font_size)
        # Try text box fallback
        if not body_replaced and text_boxes and len(text_boxes) >= 2:
            body_replaced = _replace_text_in_shape(text_boxes[1], new_body, body_font_size)
        # Ultimate fallback
        if not body_replaced:
            body_replaced = _fallback_replace_second_text(root, new_body, body_font_size)

    return tree


def _replace_text_in_shape(shape, new_text, font_size=None):
    """Replace text in any shape element."""
    if shape is None:
        return False

    text_runs = shape.xpath('.//a:t', namespaces=NSMAP)
    if not text_runs:
        return False

    text_runs[0].text = new_text
    if font_size:
        set_font_size(text_runs[0], font_size)

    # Clear subsequent text runs
    for t in text_runs[1:]:
        t.text = ""

    return True


def _fallback_replace_first_text(root, new_text, font_size):
    """Fallback method: replace first substantial text run found."""
    for t_elem in root.xpath('.//a:t', namespaces=NSMAP):
        if t_elem.text and len(t_elem.text.strip()) > 2:
            t_elem.text = new_text
            set_font_size(t_elem, font_size)
            return True
    return False


def _fallback_replace_second_text(root, new_text, font_size):
    """Fallback method: replace second substantial text run found."""
    count = 0
    for t_elem in root.xpath('.//a:t', namespaces=NSMAP):
        if t_elem.text and len(t_elem.text.strip()) > 2:
            count += 1
            if count == 2:
                t_elem.text = new_text
                set_font_size(t_elem, font_size)
                return True
    return False


def set_font_size(text_elem, size_hundredths):
    """Set font size on a text element.

    Args:
        text_elem: The <a:t> element
        size_hundredths: Size in hundredths of a point (e.g., 1400 = 14pt)
    """
    # Find or create the run properties (a:rPr) for this text
    parent = text_elem.getparent()  # This is <a:r>
    if parent is not None:
        rPr = parent.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
        if rPr is None:
            # Create run properties if they don't exist
            rPr = etree.Element('{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
            parent.insert(0, rPr)

        # Set the font size
        rPr.set('sz', str(size_hundredths))


def migrate_presentation(slides, output_path, template_path=None):
    """Create migrated presentation from slides data with intelligent layout selection."""

    if template_path is None:
        template_path = TEMPLATE_PATH

    if not Path(template_path).exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    print(f"\nMigrating {len(slides)} slides...")
    print(f"Template: {template_path}")
    print(f"Output: {output_path}")

    # Initialize layout selector for variety
    selector = LayoutSelector()

    work_dir = Path(tempfile.mkdtemp())
    template_dir = work_dir / 'template'
    output_dir = work_dir / 'output'

    # Track layout assignments for reporting
    layout_assignments = []

    try:
        # Extract template
        with zipfile.ZipFile(template_path, 'r') as zf:
            zf.extractall(template_dir)

        shutil.copytree(template_dir, output_dir)

        slides_dir = output_dir / 'ppt/slides'
        rels_dir = output_dir / 'ppt/slides/_rels'

        # Process each slide
        total_slides = len(slides)
        for i, slide in enumerate(slides):
            new_num = i + 1

            # Use intelligent layout selection
            template_slide_num, category = selector.select_layout(slide, new_num, total_slides)

            # Record assignment
            content_type = detect_content_type(slide)
            layout_assignments.append({
                'slide': new_num,
                'template': template_slide_num,
                'category': category,
                'content_type': content_type,
                'title_preview': slide['title'][:40] + '...' if len(slide['title']) > 40 else slide['title']
            })

            src_slide = template_dir / f'ppt/slides/slide{template_slide_num}.xml'
            src_rels = template_dir / f'ppt/slides/_rels/slide{template_slide_num}.xml.rels'

            if not src_slide.exists():
                # Fallback to slide 3 if template slide doesn't exist
                src_slide = template_dir / 'ppt/slides/slide3.xml'
                src_rels = template_dir / 'ppt/slides/_rels/slide3.xml.rels'
                print(f"  Warning: Template slide {template_slide_num} not found, using fallback")

            dst_slide = slides_dir / f'slide{new_num}.xml'
            dst_rels = rels_dir / f'slide{new_num}.xml.rels'

            shutil.copy(src_slide, dst_slide)
            if src_rels.exists():
                shutil.copy(src_rels, dst_rels)

            # Get text capacity for this layout category
            capacity = TEXT_CAPACITY.get(category, TEXT_CAPACITY['default'])
            title_max, body_max, title_pt, body_pt = capacity

            # Truncate text to fit capacity
            new_title = slide['title'].replace('\n', ' ')[:title_max]
            new_body = slide['body'].replace('\n', ' ')[:body_max]

            # If body is too long, use smaller font
            if len(slide['body']) > body_max:
                body_pt = max(1200, body_pt - 200)  # Reduce by 2pt, minimum 12pt

            tree = replace_text_in_slide(dst_slide, new_title, new_body, title_pt, body_pt)
            tree.write(str(dst_slide), xml_declaration=True, encoding='UTF-8', standalone=True)

            if new_num % 20 == 0:
                print(f"  Processed {new_num}/{total_slides} slides...")

        # Update package structure
        update_package_structure(output_dir, len(slides))

        # Create output PPTX
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root_path, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = Path(root_path) / file
                    arc_path = file_path.relative_to(output_dir)
                    zf.write(file_path, arc_path)

        print(f"\n Migration complete: {output_path}")

        # Print layout variety report
        print_layout_report(layout_assignments)

        return output_path

    finally:
        shutil.rmtree(work_dir)


def print_layout_report(assignments):
    """Print a summary of layout variety used."""
    print("\n" + "=" * 60)
    print("LAYOUT VARIETY REPORT")
    print("=" * 60)

    # Count template usage
    template_counts = {}
    category_counts = {}
    content_type_counts = {}

    for a in assignments:
        template_counts[a['template']] = template_counts.get(a['template'], 0) + 1
        category_counts[a['category']] = category_counts.get(a['category'], 0) + 1
        content_type_counts[a['content_type']] = content_type_counts.get(a['content_type'], 0) + 1

    print(f"\nUnique templates used: {len(template_counts)}")
    print(f"Unique categories used: {len(category_counts)}")

    print("\nTemplate distribution:")
    for idx, count in sorted(template_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  Slide {idx:2d}: {count} times")

    print("\nContent types detected:")
    for ct, count in sorted(content_type_counts.items(), key=lambda x: -x[1]):
        print(f"  {ct}: {count}")

    print("\nFirst 10 slide assignments:")
    for a in assignments[:10]:
        print(f"  Slide {a['slide']:3d} -> Template {a['template']:2d} ({a['category']}) - {a['title_preview']}")

    # Check for consecutive repeats
    consecutive_repeats = 0
    for i in range(1, len(assignments)):
        if assignments[i]['template'] == assignments[i-1]['template']:
            consecutive_repeats += 1

    print(f"\nConsecutive template repeats: {consecutive_repeats}")
    if consecutive_repeats == 0:
        print("  Excellent variety!")
    elif consecutive_repeats < 5:
        print("  Good variety with minor repeats")
    else:
        print("  Consider improving content type detection")


def update_package_structure(output_dir, num_slides):
    """Update PPTX internal structure for new slide count."""

    # Update Content_Types.xml
    ct_path = output_dir / '[Content_Types].xml'
    ct_tree = etree.parse(str(ct_path))
    ct_root = ct_tree.getroot()

    ns = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
    for override in ct_root.xpath('.//ct:Override[contains(@PartName, "/ppt/slides/slide")]', namespaces=ns):
        ct_root.remove(override)

    for i in range(1, num_slides + 1):
        override = etree.SubElement(ct_root, '{http://schemas.openxmlformats.org/package/2006/content-types}Override')
        override.set('PartName', f'/ppt/slides/slide{i}.xml')
        override.set('ContentType', 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml')

    ct_tree.write(str(ct_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    # Update presentation.xml.rels
    rels_path = output_dir / 'ppt/_rels/presentation.xml.rels'
    rels_tree = etree.parse(str(rels_path))
    rels_root = rels_tree.getroot()

    rels_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'

    for rel in list(rels_root):
        if 'slides/slide' in rel.get('Target', ''):
            rels_root.remove(rel)

    max_rid = max(int(rel.get('Id', 'rId0').replace('rId', '')) for rel in rels_root)

    for i in range(1, num_slides + 1):
        rel = etree.SubElement(rels_root, f'{{{rels_ns}}}Relationship')
        rel.set('Id', f'rId{max_rid + i}')
        rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide')
        rel.set('Target', f'slides/slide{i}.xml')

    rels_tree.write(str(rels_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    # Update presentation.xml
    pres_path = output_dir / 'ppt/presentation.xml'
    pres_tree = etree.parse(str(pres_path))
    pres_root = pres_tree.getroot()

    pres_ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
    sld_id_lst = pres_root.find('.//p:sldIdLst', pres_ns)

    if sld_id_lst is not None:
        for child in list(sld_id_lst):
            sld_id_lst.remove(child)

        for i in range(1, num_slides + 1):
            sld_id = etree.SubElement(sld_id_lst, f'{{{pres_ns["p"]}}}sldId')
            sld_id.set('id', str(255 + i))
            sld_id.set(f'{{{NSMAP["r"]}}}id', f'rId{max_rid + i}')

    pres_tree.write(str(pres_path), xml_declaration=True, encoding='UTF-8', standalone=True)


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: python migrate.py <input_file> [output_file]")
        print("")
        print("Supported inputs:")
        print("  - .md  (Markdown with slide structure)")
        print("  - .csv (Spreadsheet with slide_number, layout, title, body)")
        print("  - .pptx (PowerPoint - auto-extracts content)")
        print("")
        print("Features:")
        print("  - Intelligent content type detection (stats, quotes, bullets, etc.)")
        print("  - Layout variety tracking (no consecutive repeats)")
        print("  - Left/right orientation alternation")
        print("  - GUI block color rotation")
        print("")
        print("Example:")
        print("  python migrate.py content.md output.pptx")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "drupal-branded-output.pptx"

    print("=" * 60)
    print("Drupal Brand Presentation Migration")
    print("=" * 60)

    try:
        slides = detect_and_parse(input_file)
        print(f"Parsed {len(slides)} slides from input")

        migrate_presentation(slides, output_file)

    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
