#!/usr/bin/env python3
"""
Drupal Brand Migration using Presentation Toolkit.

This module integrates the claude-presentation-toolkit with Drupal-specific
brand configuration for intelligent presentation migration.

Key features:
- Structured content extraction (preserves bullets, tables, formatting)
- Claude-powered or heuristic content classification
- Brand-aware layout selection using Drupal slide catalog
- Output validation to ensure content preservation

Usage:
    from toolkit_migrate import migrate_to_drupal_brand

    result = migrate_to_drupal_brand(
        source_path="input.pptx",
        output_path="output.pptx",
    )

    if result.success:
        print(f"Created: {result.output_path}")
    else:
        print(result.summary())
"""

import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field

# Import from presentation toolkit
try:
    from presentation_toolkit import (
        extract_presentation,
        analyze_template,
        create_presentation,
        validate_output,
        Presentation,
        Slide,
        TemplateInfo,
        MigrationPlan,
        SlideTransformation,
        LayoutChoice,
        ContentMapping,
        ContentType,
        ValidationResult,
    )
    from presentation_toolkit.classify import (
        classify_slide_with_claude,
        classify_slide_heuristic,
        suggest_layout,
    )
    from presentation_toolkit.transform import (
        create_content_mappings,
        check_content_fit,
    )
    TOOLKIT_AVAILABLE = True
except ImportError:
    TOOLKIT_AVAILABLE = False
    print("Warning: presentation_toolkit not installed. Install with:")
    print("  pip install git+https://github.com/zivtech/claude-presentation-toolkit.git")


# Default paths
SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / "brand-config/presentation.yaml"
DEFAULT_TEMPLATE = SKILL_DIR / "templates/presentations/drupal-brand-template.pptx"
EXTENDED_TEMPLATE = SKILL_DIR / "templates/presentations/drupal-brand-template-extended.pptx"


@dataclass
class DrupalBrandConfig:
    """Drupal brand configuration loaded from YAML."""
    colors: Dict[str, Dict[str, str]]
    fonts: Dict[str, Any]
    slide_catalog: Dict[str, Dict[str, Any]]
    text_capacity: Dict[str, List[int]]
    content_patterns: Dict[str, Dict[str, List[str]]]
    orientations: Dict[str, List[str]]
    gui_colors: List[str]

    @classmethod
    def load(cls, config_path: Path = CONFIG_PATH) -> 'DrupalBrandConfig':
        """Load config from YAML file."""
        with open(config_path) as f:
            data = yaml.safe_load(f)

        return cls(
            colors=data.get('colors', {}),
            fonts=data.get('fonts', {}),
            slide_catalog=data.get('slide_catalog', {}),
            text_capacity=data.get('text_capacity', {}),
            content_patterns=data.get('content_patterns', {}),
            orientations=data.get('orientations', {}),
            gui_colors=data.get('gui_colors', []),
        )


@dataclass
class DrupalLayoutChoice:
    """Drupal-specific layout selection."""
    catalog_key: str  # e.g., 'stat_outline_gui', 'bullet_list'
    template_index: int
    confidence: float
    reason: str
    gui_color: Optional[str] = None
    orientation: Optional[str] = None


@dataclass
class DrupalMigrationResult:
    """Result of Drupal brand migration."""
    success: bool
    output_path: Path
    source: 'Presentation'
    layout_assignments: List[DrupalLayoutChoice]
    validation: Optional['ValidationResult'] = None
    warnings: List[str] = field(default_factory=list)

    def summary(self) -> str:
        """Generate migration summary."""
        lines = [
            "# Drupal Brand Migration Summary",
            "",
            f"**Source:** {self.source.source_path.name}",
            f"**Output:** {self.output_path.name}",
            f"**Slides:** {len(self.layout_assignments)}",
            f"**Status:** {'✅ Success' if self.success else '⚠️ Issues found'}",
            "",
        ]

        if self.warnings:
            lines.append("## Warnings")
            for w in self.warnings[:10]:
                lines.append(f"- {w}")
            lines.append("")

        lines.append("## Layout Assignments")
        for i, la in enumerate(self.layout_assignments, 1):
            lines.append(f"- Slide {i}: **{la.catalog_key}** (template #{la.template_index})")

        return '\n'.join(lines)


class DrupalLayoutSelector:
    """Selects Drupal brand layouts based on content type and variety."""

    def __init__(self, config: DrupalBrandConfig):
        self.config = config
        self.recent_layouts: List[str] = []
        self.recent_orientations: List[str] = []
        self.gui_color_idx = 0

    def select_layout(
        self,
        slide: 'Slide',
        content_type: ContentType,
    ) -> DrupalLayoutChoice:
        """Select best Drupal layout for slide content."""

        # Map ContentType to Drupal catalog keys
        catalog_key = self._map_content_type(content_type, slide)

        # Get template indices for this catalog key
        catalog_entry = self.config.slide_catalog.get(catalog_key, {})
        indices = catalog_entry.get('indices', [1])  # Default to slide 1

        # Select index with variety
        template_index = self._select_with_variety(indices, catalog_key)

        # Determine orientation
        orientation = self._get_orientation(catalog_key)

        # Get GUI color for this slide
        gui_color = self._next_gui_color()

        # Calculate confidence
        confidence = 0.8 if content_type != ContentType.UNKNOWN else 0.5

        # Build reason
        reason = f"Content type: {content_type.value}"
        if orientation:
            reason += f", orientation: {orientation}"

        return DrupalLayoutChoice(
            catalog_key=catalog_key,
            template_index=template_index,
            confidence=confidence,
            reason=reason,
            gui_color=gui_color,
            orientation=orientation,
        )

    def _map_content_type(self, content_type: ContentType, slide: 'Slide') -> str:
        """Map toolkit ContentType to Drupal slide catalog key."""

        # Direct mappings
        mappings = {
            ContentType.TITLE: 'title_opening',
            ContentType.SECTION_HEADER: 'section_divider',
            ContentType.STATISTIC: 'stat_outline_gui',
            ContentType.STATS_DASHBOARD: 'stats_dashboard',
            ContentType.QUOTE: 'quote_navy_bg',
            ContentType.CASE_STUDY: 'case_study_full',
            ContentType.COMPARISON: 'two_column',
            ContentType.IMAGE_FOCUSED: 'photo_text_left',
            ContentType.CLOSING: 'closing_cta',
        }

        if content_type in mappings:
            return mappings[content_type]

        # Bullet list - choose based on variety
        if content_type == ContentType.BULLET_LIST:
            feature_options = [
                'feature_blue_bg',
                'feature_white_bg',
                'feature_coral_gui',
                'feature_yellow_gui',
            ]
            # Pick one not recently used
            for opt in feature_options:
                if opt not in self.recent_layouts[-3:]:
                    return opt
            return feature_options[0]

        # Feature slides
        if content_type == ContentType.FEATURE:
            return 'content_image_right'

        # Default
        return 'feature_white_bg'

    def _select_with_variety(self, indices: List[int], catalog_key: str) -> int:
        """Select index while maintaining variety."""
        if len(indices) == 1:
            return indices[0]

        # Prefer indices not used recently
        for idx in indices:
            if idx not in [la for la in self.recent_layouts[-5:]]:
                self.recent_layouts.append(catalog_key)
                return idx

        # Fall back to first
        self.recent_layouts.append(catalog_key)
        return indices[0]

    def _get_orientation(self, catalog_key: str) -> Optional[str]:
        """Determine orientation for layout."""
        for orientation, keys in self.config.orientations.items():
            if catalog_key in keys:
                return orientation
        return None

    def _next_gui_color(self) -> str:
        """Get next GUI color in rotation."""
        if not self.config.gui_colors:
            return 'blue'
        color = self.config.gui_colors[self.gui_color_idx]
        self.gui_color_idx = (self.gui_color_idx + 1) % len(self.config.gui_colors)
        return color


def classify_for_drupal(
    slide: 'Slide',
    config: DrupalBrandConfig,
    use_claude: bool = True,
) -> ContentType:
    """
    Classify slide content with Drupal-specific enhancements.

    Uses toolkit classification but enhances with Drupal keywords.
    """
    # Get base classification
    if use_claude:
        content_type = classify_slide_with_claude(slide)
    else:
        content_type = classify_slide_heuristic(slide)

    # Enhance with Drupal-specific patterns
    title = (slide.title or '').lower()
    body = slide.body_text.lower() if slide.body_text else ''
    combined = f"{title} {body}"

    # Check for case study keywords
    case_study_keywords = config.content_patterns.get('case_study', {}).get('keywords', [])
    if any(kw in combined for kw in case_study_keywords):
        # Check if it's a full case study (has bullets + quote)
        has_bullets = len(slide.all_bullets) >= 2
        has_quote = '"' in combined or '"' in combined
        if has_bullets and has_quote:
            return ContentType.CASE_STUDY
        # Simple case study goes to feature
        if content_type == ContentType.UNKNOWN:
            return ContentType.FEATURE

    # Check for stats dashboard (multiple statistics)
    import re
    stat_patterns = [r'\b\d+%', r'\b\d+[KMB]\+?\b', r'\$[\d,]+']
    stat_count = sum(len(re.findall(p, combined, re.IGNORECASE)) for p in stat_patterns)
    if stat_count >= 4:
        return ContentType.STATS_DASHBOARD

    return content_type


def migrate_to_drupal_brand(
    source_path: Path,
    output_path: Path,
    template_path: Optional[Path] = None,
    config_path: Path = CONFIG_PATH,
    use_claude: bool = True,
    validate: bool = True,
    extract_images: bool = True,
) -> DrupalMigrationResult:
    """
    Migrate presentation to Drupal brand.

    This is the main entry point. It:
    1. Extracts content from source using toolkit
    2. Loads Drupal brand configuration
    3. Classifies content with Drupal enhancements
    4. Selects layouts from Drupal slide catalog
    5. Assembles output using toolkit
    6. Validates result

    Args:
        source_path: Path to source PPTX
        output_path: Where to save output
        template_path: Drupal template (default or extended)
        config_path: Path to brand config YAML
        use_claude: Use Claude for classification
        validate: Run validation after migration
        extract_images: Extract and migrate images

    Returns:
        DrupalMigrationResult with output path and assignments
    """
    if not TOOLKIT_AVAILABLE:
        raise ImportError("presentation_toolkit is required. Install with pip.")

    source_path = Path(source_path)
    output_path = Path(output_path)

    # Load brand config
    config = DrupalBrandConfig.load(config_path)

    # Determine template
    if template_path is None:
        template_path = DEFAULT_TEMPLATE
    template_path = Path(template_path)

    print(f"Migrating to Drupal brand...")
    print(f"  Source: {source_path}")
    print(f"  Template: {template_path}")
    print(f"  Output: {output_path}")

    # Step 1: Extract source content
    source = extract_presentation(source_path, extract_images=extract_images)
    print(f"  Extracted {len(source.slides)} slides")

    # Step 2: Analyze template
    template = analyze_template(template_path)

    # Step 3: Classify and select layouts
    selector = DrupalLayoutSelector(config)
    layout_assignments = []
    warnings = []

    for slide in source.slides:
        # Classify with Drupal enhancements
        content_type = classify_for_drupal(slide, config, use_claude)

        # Select Drupal layout
        layout_choice = selector.select_layout(slide, content_type)
        layout_assignments.append(layout_choice)

        # Check capacity
        capacity = config.text_capacity.get(
            layout_choice.catalog_key,
            config.text_capacity.get('default', [150, 500, 2400, 1400])
        )
        title_max, body_max = capacity[0], capacity[1]

        if slide.title and len(slide.title) > title_max:
            warnings.append(f"Slide {slide.number}: Title may be truncated ({len(slide.title)} > {title_max})")
        if slide.body_text and len(slide.body_text) > body_max:
            warnings.append(f"Slide {slide.number}: Body may be truncated ({len(slide.body_text)} > {body_max})")

    # Step 4: Build migration plan compatible with toolkit
    transformations = []
    for slide, la in zip(source.slides, layout_assignments):
        # Map to toolkit structures
        layout = template.get_layout(la.template_index)
        if not layout:
            # Fallback to first layout
            layout = template.layouts[0] if template.layouts else None

        if layout:
            mappings = create_content_mappings(slide, layout)
            fit_warnings = check_content_fit(slide, layout)
            warnings.extend([f"Slide {slide.number}: {w}" for w in fit_warnings])

            transformations.append(SlideTransformation(
                source_slide=slide.number,
                target_layout=LayoutChoice(
                    layout_index=la.template_index,
                    layout_name=la.catalog_key,
                    confidence=la.confidence,
                    reason=la.reason,
                ),
                content_type=ContentType.UNKNOWN,  # Already used for selection
                content_mappings=mappings,
                images_to_insert=[str(img.path) for img in slide.images if img.path],
                warnings=fit_warnings,
            ))

    plan = MigrationPlan(
        source=source,
        template=template,
        transformations=transformations,
    )

    # Step 5: Create output
    create_presentation(plan, output_path)
    print(f"  Created: {output_path}")

    # Step 6: Validate
    validation = None
    if validate:
        validation = validate_output(source, output_path)
        if not validation.valid:
            warnings.append("Validation found issues - check output manually")

    success = (validation is None or validation.valid) and len(warnings) < 5

    return DrupalMigrationResult(
        success=success,
        output_path=output_path,
        source=source,
        layout_assignments=layout_assignments,
        validation=validation,
        warnings=warnings,
    )


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Drupal Brand Migration (Toolkit Edition)")
        print("")
        print("Usage: python toolkit_migrate.py <input.pptx> [output.pptx] [options]")
        print("")
        print("Options:")
        print("  --no-claude    Use heuristic classification (no API required)")
        print("  --no-validate  Skip output validation")
        print("  --no-images    Skip image extraction")
        print("  --extended     Use extended template (more layouts)")
        print("")
        print("Requires: pip install git+https://github.com/zivtech/claude-presentation-toolkit.git")
        sys.exit(1)

    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else "drupal-branded-output.pptx"

    use_claude = '--no-claude' not in sys.argv
    validate = '--no-validate' not in sys.argv
    extract_images = '--no-images' not in sys.argv
    use_extended = '--extended' in sys.argv

    template = EXTENDED_TEMPLATE if use_extended else DEFAULT_TEMPLATE

    result = migrate_to_drupal_brand(
        source_path=source,
        output_path=output,
        template_path=template,
        use_claude=use_claude,
        validate=validate,
        extract_images=extract_images,
    )

    print("")
    print(result.summary())

    sys.exit(0 if result.success else 1)


if __name__ == '__main__':
    main()
