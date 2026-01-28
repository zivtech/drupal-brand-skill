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

    # NEW: Extended template slides (slides 49-50)
    # Use drupal-brand-template-extended.pptx for these
    'stats_dashboard': [49],        # 6-zone stats layout
    'case_study_full': [50],        # Description + bullets + quote
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
    'center': ['statement_center', 'quote_centered', 'section_divider', 'closing_cta',
               'stats_dashboard', 'case_study_full'],  # Multi-zone layouts are centered
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

    # NEW: Extended template slides
    'stats_dashboard': (50, 300, 7200, 1800),   # Large stat numbers + descriptions
    'case_study_full': (100, 600, 2400, 1400),  # Company name + full description + bullets
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

    # Check for MULTIPLE statistics (stats dashboard - 4+ stat-like values)
    # Patterns for stat-like numbers
    stat_number_patterns = [
        r'\b\d+%',                   # Percentages
        r'\b\d+[KMB]\+?\b',         # K/M/B suffixes (like 46K+, 1.4M)
        r'\b\d{2,}k\b',             # lowercase k (like 118k)
        r'\b\$[\d,]+',              # Dollar amounts
        r'\b\d+x\b',                # Multipliers
    ]
    stat_count = 0
    for pattern in stat_number_patterns:
        stat_count += len(re.findall(pattern, combined, re.IGNORECASE))

    # If 4+ different stats found, use stats_dashboard layout
    if stat_count >= 4:
        return 'stats_dashboard'

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

    # Count bullets for subsequent checks
    bullet_count = len(re.findall(r'^\s*[-•▪]', body, re.MULTILINE))

    # Check for FULL case study BEFORE bullet_list (more specific pattern)
    # Full case study has bullets + quote OR "why chosen" section
    has_bullets = bullet_count >= 2
    # Check for quotes - including title starting with quote (common in case studies)
    has_quote = (
        bool(re.search(r'["""].*["""]', combined)) or
        '"' in combined or
        title.strip().startswith('"') or
        title.strip().startswith('"')
    )
    has_why_chosen = 'why' in combined and ('chosen' in combined or 'drupal' in combined)

    case_study_keywords = ['customer', 'client', 'case study', 'success story',
                          'testimonial', 'partner', 'rebuilt', 'transformed',
                          'organization', 'implemented', 'content hub', 'replatform',
                          'arsenal', 'premier league', 'health portal']  # Add specific org names
    is_case_study = any(kw in combined for kw in case_study_keywords)

    # Full case study: has bullets + quote OR "why chosen" section
    # Also detect case studies that start with a quote (testimonial format)
    # These are complex layouts needing multiple text zones
    # Quote chars: " (8220 left curly), " (8221 right curly), " (34 straight)
    quote_chars = ['\u201c', '\u201d', '"', "'", '\u2018', '\u2019']
    title_is_quote = any(title.strip().startswith(q) for q in quote_chars)

    if has_bullets and (has_quote or has_why_chosen):
        return 'case_study_full'

    # Title that's a quote + case study keywords = full case study
    if title_is_quote and is_case_study:
        return 'case_study_full'

    # Regular case study (simpler layout)
    if is_case_study:
        return 'case_study'

    # Generic bullet lists (only if not a case study)
    if bullet_count >= 3:
        return 'bullet_list'

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

        # PRIORITY: If the primary candidate (first in list) matches content_type exactly,
        # and it's a specialized layout (stats_dashboard, case_study_full), use it
        # These layouts are specifically designed for their content types
        specialized_layouts = ['stats_dashboard', 'case_study_full']
        if available and candidates and candidates[0] in specialized_layouts:
            cat, idx = available[0]
            if cat == candidates[0]:
                for orient, cats in ORIENTATIONS.items():
                    if cat in cats:
                        self._record_selection(idx, orient)
                        return idx, cat

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

        # PRIORITY: Specialized multi-zone layouts take precedence over position
        # These content types have specific template requirements
        if content_type == 'stats_dashboard':
            return ['stats_dashboard', 'stat_outline_gui']  # Fallback if extended template not used

        if content_type == 'case_study_full':
            return ['case_study_full', 'content_image_right']  # Fallback

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


def parse_pptx(pptx_path, image_output_dir=None):
    """Extract content and images from PPTX file.

    Args:
        pptx_path: Path to PPTX file
        image_output_dir: Directory to save extracted images (optional)

    Returns:
        List of slide dicts with 'number', 'title', 'body', 'images' keys
    """
    slides = []

    # Create image output directory if specified
    if image_output_dir:
        image_output_dir = Path(image_output_dir)
        image_output_dir.mkdir(parents=True, exist_ok=True)

    total_images_extracted = 0

    with tempfile.TemporaryDirectory() as tmpdir:
        work_dir = Path(tmpdir)

        with zipfile.ZipFile(pptx_path, 'r') as zf:
            zf.extractall(work_dir)

        slides_dir = work_dir / 'ppt/slides'
        media_dir = work_dir / 'ppt/media'

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

            # Get layout from rels and extract images
            layout = 'DEFAULT'
            extracted_images = []
            rels_file = slides_dir / f'_rels/slide{num}.xml.rels'

            if rels_file.exists():
                rels_tree = etree.parse(str(rels_file))
                for rel in rels_tree.getroot():
                    target = rel.get('Target', '')
                    rel_type = rel.get('Type', '').split('/')[-1]

                    if 'slideLayout' in target:
                        layout_num = re.search(r'slideLayout(\d+)', target)
                        if layout_num:
                            layout = 'DEFAULT'

                    # Extract images
                    if rel_type == 'image' and image_output_dir:
                        # Get source image path
                        image_name = os.path.basename(target)
                        source_path = media_dir / image_name

                        if source_path.exists():
                            try:
                                # Get image dimensions
                                import struct
                                with open(source_path, 'rb') as f:
                                    data = f.read(32)

                                width, height = 0, 0
                                ext = source_path.suffix.lower()

                                # PNG dimensions
                                if ext == '.png' and data[:8] == b'\x89PNG\r\n\x1a\n':
                                    width = struct.unpack('>I', data[16:20])[0]
                                    height = struct.unpack('>I', data[20:24])[0]
                                # JPEG dimensions (approximate)
                                elif ext in ['.jpg', '.jpeg']:
                                    width, height = 800, 600  # Default estimate

                                # Only copy images larger than 100x100
                                if width >= 100 and height >= 100:
                                    dest_filename = f"slide{num}_img{len(extracted_images)}{ext}"
                                    dest_path = image_output_dir / dest_filename
                                    shutil.copy2(source_path, dest_path)

                                    extracted_images.append({
                                        'path': str(dest_path),
                                        'width': width,
                                        'height': height,
                                        'ext': ext[1:]  # Remove dot
                                    })
                                    total_images_extracted += 1
                            except Exception:
                                pass  # Skip images that can't be processed

            slide = {
                'number': num,
                'layout': layout,
                'title': texts[0] if texts else '',
                'body': '\n'.join(texts[1:5]) if len(texts) > 1 else '',
                'images': extracted_images,
                'image_count': len(extracted_images)
            }
            slides.append(slide)

    if image_output_dir:
        print(f"  Extracted {total_images_extracted} images to {image_output_dir}")

    return slides


def parse_pdf(pdf_path, image_output_dir=None):
    """Extract content and images from PDF file.

    LIMITATIONS:
    - Text embedded in images (decorative text, logos) will NOT be extracted
    - Complex layouts may not preserve structure (tables, multi-column)
    - Image extraction captures raster images only, not vector graphics
    - Page order is preserved but slide boundaries may need manual review

    For best results:
    - Use PDFs exported from PowerPoint (text preserved as text)
    - Avoid PDFs that are scanned images
    - Review output and manually adjust content as needed

    Args:
        pdf_path: Path to PDF file
        image_output_dir: Directory to save extracted images (optional)

    Returns:
        List of slide dicts with 'number', 'title', 'body', 'images' keys
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ImportError(
            "PyMuPDF (fitz) is required for PDF parsing. "
            "Install with: pip install PyMuPDF"
        )

    slides = []
    doc = fitz.open(pdf_path)

    print(f"  PDF has {len(doc)} pages")

    # Create image output directory if specified
    if image_output_dir:
        image_output_dir = Path(image_output_dir)
        image_output_dir.mkdir(parents=True, exist_ok=True)

    total_images_extracted = 0

    for page_num, page in enumerate(doc, 1):
        # Extract text
        text = page.get_text().strip()

        # Split into lines and clean
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Heuristic: First substantial line is title, rest is body
        title = ''
        body_lines = []

        for i, line in enumerate(lines):
            if not title and len(line) > 2:
                title = line
            elif title:
                body_lines.append(line)

        body = '\n'.join(body_lines)

        # Extract images
        images = page.get_images()
        image_count = len(images)
        extracted_images = []

        if image_output_dir and images:
            for img_idx, img in enumerate(images):
                xref = img[0]  # Image XREF
                try:
                    base_image = doc.extract_image(xref)
                    if base_image:
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]

                        # Filter out tiny images (likely icons/bullets)
                        width = base_image.get("width", 0)
                        height = base_image.get("height", 0)

                        # Only save images larger than 100x100
                        if width >= 100 and height >= 100:
                            image_filename = f"page{page_num}_img{img_idx}.{image_ext}"
                            image_path = image_output_dir / image_filename

                            with open(image_path, "wb") as img_file:
                                img_file.write(image_bytes)

                            extracted_images.append({
                                'path': str(image_path),
                                'width': width,
                                'height': height,
                                'ext': image_ext
                            })
                            total_images_extracted += 1
                except Exception as e:
                    pass  # Skip images that can't be extracted

        # Track extraction quality
        text_chars = len(text)
        has_minimal_text = text_chars < 50

        slide = {
            'number': page_num,
            'layout': 'DEFAULT',
            'title': clean_text(title),
            'body': clean_text(body),
            'image_count': image_count,
            'images': extracted_images,  # List of extracted image info
            '_extraction_notes': []
        }

        # Add warnings for potential issues
        if has_minimal_text and image_count > 0:
            slide['_extraction_notes'].append(
                f"WARNING: Only {text_chars} chars extracted but {image_count} images found. "
                "Text may be embedded in images."
            )

        if not title and not body:
            slide['_extraction_notes'].append(
                "WARNING: No text extracted. This may be a title slide with image-based text."
            )

        slides.append(slide)

    doc.close()

    # Print extraction summary
    print(f"\n  Extraction Summary:")
    warnings = 0
    for slide in slides:
        if slide.get('_extraction_notes'):
            warnings += 1
            for note in slide['_extraction_notes']:
                print(f"    Page {slide['number']}: {note}")

    if warnings > 0:
        print(f"\n  {warnings} pages may need manual review.")
    else:
        print(f"  All {len(slides)} pages extracted successfully.")

    if image_output_dir:
        print(f"  Extracted {total_images_extracted} images to {image_output_dir}")

    return slides


def detect_and_parse(input_path, image_output_dir=None):
    """Detect input format and parse accordingly.

    Args:
        input_path: Path to input file (PDF, PPTX, MD, or CSV)
        image_output_dir: Directory to save extracted images (optional)

    Returns:
        List of slide dicts with content and image info
    """
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
        return parse_pptx(path, image_output_dir)
    elif suffix == '.pdf':
        print(f"Detected PDF input: {path.name}")
        return parse_pdf(path, image_output_dir)
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
    if title_shape is not None and new_title:
        title_width = get_placeholder_width(title_shape)
        if title_width:
            title_font_size = calculate_font_size(
                new_title, title_width, title_font_size, 1800  # Min 18pt for titles
            )

    if body_shape is not None and new_body:
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


# ============================================================
# MULTI-ZONE LAYOUT POPULATION
# ============================================================

def find_shape_by_name(root, name_pattern):
    """Find a shape by its name (or partial match).

    Args:
        root: XML root element
        name_pattern: Name to search for (case-insensitive partial match)

    Returns:
        Shape element or None
    """
    pattern = name_pattern.lower()
    for shape in root.xpath('.//p:sp', namespaces=NSMAP):
        nvSpPr = shape.find('.//p:nvSpPr', namespaces=NSMAP)
        if nvSpPr is not None:
            cNvPr = nvSpPr.find('p:cNvPr', namespaces=NSMAP)
            if cNvPr is not None:
                name = cNvPr.get('name', '').lower()
                if pattern in name:
                    return shape
    return None


def replace_text_in_named_shape(root, shape_name, new_text, font_size=None):
    """Replace text in a shape identified by name.

    Args:
        root: XML root element
        shape_name: Name of shape to find
        new_text: Text to insert
        font_size: Optional font size in hundredths of point

    Returns:
        True if text was replaced, False otherwise
    """
    shape = find_shape_by_name(root, shape_name)
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


def parse_stats_content(title, body):
    """Parse content into stats dashboard zones.

    Extracts statistics from content like:
    "118k contributors | 46K+ developers | 1.4M users | 12% market share"
    or multiline format with number followed by description.

    Returns:
        List of dicts with 'number' and 'label' keys
    """
    stats = []
    combined = f"{title}\n{body}"

    # Patterns that indicate a stat number
    stat_patterns = [
        r'^[\d,.$]+[%KMBkmb+]*$',     # 118k, 12%, $1.5M
        r'^\d+[\d,.]*\s*[%KMBkmb+]',  # 1.4 Million, 46K+
        r'^(Millions?|Billions?|Thousands?|Hundreds?)\b',  # Word numbers
    ]

    lines = combined.split('\n')
    current_number = None
    current_labels = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this line looks like a stat number
        is_number = False
        for pattern in stat_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                is_number = True
                break

        # Also check for lines starting with digits
        if not is_number and re.match(r'^\d', line) and len(line) < 20:
            is_number = True

        if is_number:
            # Save previous stat if exists
            if current_number:
                label = ' '.join(current_labels) if current_labels else ''
                stats.append({'number': current_number, 'label': label})
                current_labels = []
            current_number = line
        elif current_number:
            # This is a label line for the current number
            # Keep collecting labels until we hit another number
            if len(line) < 50 and not any(c in line for c in '.!?'):
                current_labels.append(line)
            else:
                # Long line - save stat and reset
                label = ' '.join(current_labels) if current_labels else ''
                stats.append({'number': current_number, 'label': label})
                current_number = None
                current_labels = []

    # Handle trailing stat
    if current_number:
        label = ' '.join(current_labels) if current_labels else ''
        stats.append({'number': current_number, 'label': label})

    return stats[:6]  # Max 6 stats


def parse_case_study_content(title, body):
    """Parse content into case study zones.

    Extracts:
    - company_name: From title
    - description: Opening paragraph(s)
    - bullets: "Why Drupal" section bullets
    - quote: Quoted text
    - attribution: Quote attribution

    Returns:
        Dict with zone keys
    """
    zones = {
        'company_name': title,
        'description': '',
        'bullets': '',
        'quote': '',
        'attribution': ''
    }

    lines = body.split('\n')
    in_bullets = False
    description_lines = []
    bullet_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for quote (starts with quote mark or contains attribution)
        if line.startswith('"') or line.startswith('"') or line.startswith("'"):
            # Extract quote text
            quote_text = line
            # Check if attribution is on same line
            if '—' in quote_text or ' - ' in quote_text:
                parts = re.split(r'\s*[—-]\s*', quote_text, 1)
                zones['quote'] = parts[0].strip(' ""\'"')
                if len(parts) > 1:
                    zones['attribution'] = '— ' + parts[1]
            else:
                zones['quote'] = quote_text.strip(' ""\'"')
            continue

        # Check for attribution line
        if line.startswith('—') or line.startswith('- '):
            zones['attribution'] = line
            continue

        # Check for "Why" section header
        if 'why' in line.lower() and ('drupal' in line.lower() or 'chosen' in line.lower()):
            in_bullets = True
            continue

        # Check for bullet points
        if line.startswith('•') or line.startswith('-') or line.startswith('*'):
            in_bullets = True
            bullet_lines.append(line)
            continue

        # Otherwise it's description
        if not in_bullets:
            description_lines.append(line)
        else:
            # After bullets started, this might be more bullets without markers
            if len(line) < 100:
                bullet_lines.append('• ' + line)

    zones['description'] = ' '.join(description_lines)
    zones['bullets'] = '\n'.join(bullet_lines)

    return zones


def populate_stats_dashboard(slide_path, title, body):
    """Populate a stats dashboard slide with parsed statistics.

    Args:
        slide_path: Path to slide XML file
        title: Slide title
        body: Body content containing statistics

    Returns:
        Modified ElementTree
    """
    tree = etree.parse(str(slide_path))
    root = tree.getroot()

    # Parse statistics from content
    stats = parse_stats_content(title, body)

    # Replace title
    replace_text_in_placeholder(root, 'title', title, 3600)

    # Populate each stat zone
    for i, stat in enumerate(stats, 1):
        number_name = f'Stat{i}_Number'
        label_name = f'Stat{i}_Label'

        replace_text_in_named_shape(root, number_name, stat['number'], 7200)  # 72pt
        replace_text_in_named_shape(root, label_name, stat['label'], 1800)    # 18pt

    return tree


def populate_case_study_full(slide_path, title, body):
    """Populate a case study slide with parsed content zones.

    Args:
        slide_path: Path to slide XML file
        title: Company name
        body: Full case study content

    Returns:
        Modified ElementTree
    """
    tree = etree.parse(str(slide_path))
    root = tree.getroot()

    # Parse case study content
    zones = parse_case_study_content(title, body)

    # Populate title (company name)
    replace_text_in_placeholder(root, 'title', zones['company_name'], 3600)

    # Populate description (body idx=1)
    replace_text_in_placeholder(root, 'body', zones['description'], 1600, idx='1')

    # Populate bullets (body idx=2)
    replace_text_in_placeholder(root, 'body', zones['bullets'], 1400, idx='2')

    # Populate quote and attribution (named shapes)
    if zones['quote']:
        quote_text = f'"{zones["quote"]}"'
        replace_text_in_named_shape(root, 'Quote', quote_text, 2400)

    if zones['attribution']:
        replace_text_in_named_shape(root, 'Attribution', zones['attribution'], 1400)

    return tree


# ============================================================
# IMAGE INSERTION
# ============================================================

def find_largest_picture(root):
    """Find the largest p:pic element in a slide (likely the content image area).

    Returns:
        Tuple of (pic_element, rId, area) or (None, None, 0)
    """
    pics = root.xpath('.//p:pic', namespaces=NSMAP)
    largest = None
    largest_rid = None
    largest_area = 0

    for pic in pics:
        spPr = pic.find('p:spPr', namespaces=NSMAP)
        if spPr is None:
            continue

        xfrm = spPr.find('a:xfrm', namespaces=NSMAP)
        if xfrm is None:
            continue

        ext = xfrm.find('a:ext', namespaces=NSMAP)
        if ext is None:
            continue

        cx = int(ext.get('cx', 0))
        cy = int(ext.get('cy', 0))
        area = cx * cy

        if area > largest_area:
            largest_area = area
            largest = pic

            # Get the relationship ID
            blip = pic.find('.//a:blip', namespaces=NSMAP)
            if blip is not None:
                largest_rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')

    return largest, largest_rid, largest_area


def insert_image_in_slide(slide_xml_path, slide_rels_path, image_path, media_dir, next_rid):
    """Insert an image into a slide by replacing the largest existing picture.

    Args:
        slide_xml_path: Path to slide XML file
        slide_rels_path: Path to slide relationships file
        image_path: Path to source image file
        media_dir: Directory where media files are stored in the PPTX
        next_rid: Next available relationship ID (e.g., 'rId10')

    Returns:
        True if image was inserted, False otherwise
    """
    tree = etree.parse(str(slide_xml_path))
    root = tree.getroot()

    # Find the largest picture element (likely the content image area)
    pic, old_rid, area = find_largest_picture(root)

    if pic is None:
        return False

    # Copy image to media directory
    image_path = Path(image_path)
    new_image_name = f"image_user_{next_rid}.{image_path.suffix.lstrip('.')}"
    dest_path = media_dir / new_image_name
    shutil.copy2(image_path, dest_path)

    # Update the blip reference in the slide XML
    blip = pic.find('.//a:blip', namespaces=NSMAP)
    if blip is not None:
        blip.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed', next_rid)

    # Update the relationships file
    rels_tree = etree.parse(str(slide_rels_path))
    rels_root = rels_tree.getroot()

    # Add new relationship
    new_rel = etree.SubElement(rels_root, 'Relationship')
    new_rel.set('Id', next_rid)
    new_rel.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
    new_rel.set('Target', f'../media/{new_image_name}')

    # Save both files
    tree.write(str(slide_xml_path), xml_declaration=True, encoding='UTF-8', standalone=True)
    rels_tree.write(str(slide_rels_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    return True


def get_next_rid(rels_path):
    """Get the next available relationship ID from a rels file.

    Returns:
        String like 'rId10'
    """
    try:
        tree = etree.parse(str(rels_path))
        root = tree.getroot()

        max_id = 0
        for rel in root:
            rid = rel.get('Id', '')
            if rid.startswith('rId'):
                try:
                    num = int(rid[3:])
                    max_id = max(max_id, num)
                except ValueError:
                    pass

        return f'rId{max_id + 1}'
    except Exception:
        return 'rId100'  # Safe fallback


def migrate_presentation(slides, output_path, template_path=None, insert_images=True):
    """Create migrated presentation from slides data with intelligent layout selection.

    Args:
        slides: List of slide dicts with 'title', 'body', and optionally 'images'
        output_path: Path for output PPTX file
        template_path: Path to template PPTX (optional, uses default if not specified)
        insert_images: Whether to insert extracted images into slides (default: True)
    """

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

            # Use specialized population for multi-zone layouts
            if content_type == 'stats_dashboard' and category == 'stats_dashboard':
                # Stats dashboard has 6 stat zones - preserve newlines for parsing
                tree = populate_stats_dashboard(dst_slide, slide['title'], slide['body'])
                tree.write(str(dst_slide), xml_declaration=True, encoding='UTF-8', standalone=True)
            elif content_type == 'case_study_full' and category == 'case_study_full':
                # Case study has description, bullets, quote zones - preserve newlines
                tree = populate_case_study_full(dst_slide, slide['title'], slide['body'])
                tree.write(str(dst_slide), xml_declaration=True, encoding='UTF-8', standalone=True)
            else:
                # Standard two-zone layout (title + body)
                new_title = slide['title'].replace('\n', ' ')[:title_max]
                new_body = slide['body'].replace('\n', ' ')[:body_max]

                # If body is too long, use smaller font
                if len(slide['body']) > body_max:
                    body_pt = max(1200, body_pt - 200)  # Reduce by 2pt, minimum 12pt

                tree = replace_text_in_slide(dst_slide, new_title, new_body, title_pt, body_pt)
                tree.write(str(dst_slide), xml_declaration=True, encoding='UTF-8', standalone=True)

            # Insert image if available
            slide_images = slide.get('images', [])
            if insert_images and slide_images:
                # Use the largest extracted image
                largest_image = max(slide_images, key=lambda x: x.get('width', 0) * x.get('height', 0))
                media_dir = output_dir / 'ppt/media'

                if dst_rels.exists():
                    next_rid = get_next_rid(dst_rels)
                    image_inserted = insert_image_in_slide(
                        dst_slide, dst_rels, largest_image['path'], media_dir, next_rid
                    )
                    if image_inserted:
                        layout_assignments[-1]['image_inserted'] = True

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
        print("Usage: python migrate.py <input_file> [output_file] [options]")
        print("")
        print("Supported inputs:")
        print("  - .pdf  (PDF - extracts text and images)")
        print("  - .pptx (PowerPoint - auto-extracts content and images)")
        print("  - .md   (Markdown with slide structure)")
        print("  - .csv  (Spreadsheet with slide_number, layout, title, body)")
        print("")
        print("Features:")
        print("  - Intelligent content type detection (stats, quotes, bullets, etc.)")
        print("  - Multi-zone layout support (stats dashboard, case study)")
        print("  - Layout variety tracking (no consecutive repeats)")
        print("  - Image extraction and insertion (PDF/PPTX)")
        print("")
        print("Options:")
        print("  --no-images              Skip image extraction/insertion")
        print("  --template <path.pptx>   Use custom template (default: drupal-brand-template.pptx)")
        print("")
        print("Examples:")
        print("  python migrate.py presentation.pdf output.pptx")
        print("  python migrate.py input.pdf output.pptx --template extended-template.pptx")
        sys.exit(1)

    # Parse arguments
    input_file = sys.argv[1]
    output_file = "drupal-branded-output.pptx"
    extract_images = True
    template_path = None

    # Simple argument parsing
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--no-images':
            extract_images = False
        elif arg == '--template' and i + 1 < len(sys.argv):
            template_path = sys.argv[i + 1]
            i += 1
        elif not arg.startswith('--'):
            output_file = arg
        i += 1

    print("=" * 60)
    print("Drupal Brand Presentation Migration")
    print("=" * 60)

    try:
        # Create temp directory for extracted images
        image_dir = None
        if extract_images:
            image_dir = Path(tempfile.mkdtemp(prefix='drupal_migrate_images_'))
            print(f"Image extraction: enabled (temp: {image_dir})")
        else:
            print("Image extraction: disabled")

        if template_path:
            print(f"Custom template: {template_path}")

        slides = detect_and_parse(input_file, image_output_dir=image_dir)
        print(f"Parsed {len(slides)} slides from input")

        # Count slides with images
        slides_with_images = sum(1 for s in slides if s.get('images'))
        if slides_with_images > 0:
            print(f"  {slides_with_images} slides have extractable images")

        migrate_presentation(slides, output_file, template_path=template_path, insert_images=extract_images)

        # Cleanup temp image directory
        if image_dir and image_dir.exists():
            shutil.rmtree(image_dir)

    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
