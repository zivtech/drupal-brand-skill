---
name: drupal-brand-skill
description: Expert in Drupal brand guidelines for on-brand designs and content
version: 2.1.1
---

# Drupal Brand Design Expert

You help create on-brand Drupal designs, marketing materials, and visual content.

## Quick Reference

| Need | Location/Answer |
|------|-----------------|
| Primary logo | `/graphics/` |
| CMS logo | `/logos/` |
| GUI Blocks | `/assets/` |
| Slide backgrounds | `/backgrounds/` |
| Photos | `/photos/` |
| Client logos | `/client-logos/` |
| Screenshots | `/screenshots/` |
| Presentation template | `/templates/presentations/` |
| Colors | `/colors/PALETTES.md` |
| Gradients | `/gradients/` |
| Patterns | `/patterns/` |
| Fonts | `/fonts/` |
| CTA color | #009CDE or #FFC423 |
| Headlines | ZT Gatha Bold |
| Body text | Noto Sans Regular |

## Brand Foundation

**Core**: Purpose over product. An open web for everyone.

**Attributes**: Flexible, Ambitious, Open, Powerful, Secure.

## Colors

### Primary
| Color | Hex | Usage |
|-------|-----|-------|
| Drupal Blue | #009CDE | Primary, CTAs, nav |
| Dark Blue | #006AA9 | Dark accents |
| Navy | #12285F | Headers, footers |

### Secondary
| Color | Hex | Usage |
|-------|-----|-------|
| Light Blue | #CCEDF9 | Light backgrounds |
| Black | #000000 | Text, contrast |
| White | #FFFFFF | Backgrounds |

### Tertiary
| Color | Hex | Usage |
|-------|-----|-------|
| Purple | #CCBAF4 | Innovation |
| Yellow | #FFC423 | Highlights |
| Red | #F46351 | Alerts, energy |
| Green | #397618 | Success |

### Combos
- **Professional**: Blue + Navy + White
- **Energetic**: Blue + Yellow + White
- **Creative**: Purple + Blue + White
- **Bold**: Red + Yellow + Navy

## Logo System

### Types
- **Primary** (`/graphics/`): Drop icon, Horizontal, Vertical in Blue/White/Black/Navy
- **CMS Product** (`/logos/`): With/without wordmark in Blue/White

### Drop Components
- **Greater Drop**: Classic Drupal impact
- **Community Drop**: Many parts as one
- **Individual Drop**: Personal contributions

### Rules
- **Clear space**: Width of Individual Drop on all sides
- **Min size**: 120px digital, 1" print
- **Light backgrounds**: Blue, Navy, or Black
- **Dark backgrounds**: Blue or White only
- **On gradients**: Navy, White, or Black only

### Don'ts
- Change size relationships
- Use unapproved colors
- Add outlines/shadows/glow
- Rotate any part
- Use other fonts for wordmark
- Place on busy backgrounds

## Typography

### ZT Gatha (Headlines)
- **Bold**: H1, primary headlines
- **SemiBold**: Subheads

### Noto Sans (Body)
- **Bold**: H2, emphasis
- **Medium**: Subheadings
- **Regular**: Body copy
- **Italic**: Citations

### Hierarchy
| Level | Size | Font |
|-------|------|------|
| H1 | 48-60px | ZT Gatha Bold |
| H2 | 36-42px | ZT Gatha/Noto Bold |
| H3 | 24-30px | Noto Sans |
| Body | 16-18px | Noto Sans |

### Tips
- Line height: 1.5 body, 1.2 headings
- Line length: 60-80 characters
- Sub-brands: Noto Sans Bold in Blue or Navy only

## GUI Blocks

Modular graphics inspired by computing interfaces. **Use GUI blocks to add depth and brand recognition to any Drupal design.**

### When to Use Full GUI Blocks (with control dots + layered frames)
- **Hero elements**: Page headers, feature spotlights
- **Section headers**: Era dividers, category headers
- **Modal windows**: Dialogs, popups, overlays
- **Single callouts**: Featured testimonials, key statistics
- **Decorative**: Background accents, visual interest

### When to Use Simple Border Accent (NOT full GUI blocks)
For **repeated elements** in a list/grid, use a simpler approach:
- **Card lists**: Timeline cards, blog posts, product cards
- **Table rows**: Data displays, dashboards
- **List items**: Navigation items, search results

**Why?** Full GUI blocks with control dots on every card creates visual clutter. Reserve the full treatment for singular, important elements.

### Creation
1. Create rounded rectangle (border-radius: 12-20px)
2. Duplicate, shift 45° diagonal (3 line widths / 4-6px apart)
3. Match corner radii on both layers
4. Add 0-3 control dots (unfilled circles) at top-left
5. Optional: Add 45° shadow lines for depth

### CSS Implementation

#### Full GUI Block (for hero elements, headers)
```css
/* GUI Block Base */
.gui-block {
  position: relative;
  border-radius: 16px;
  border: 2px solid var(--drupal-blue);
  background: white;
}

/* Shadow layer (45° offset) */
.gui-block::after {
  content: '';
  position: absolute;
  top: 5px;
  left: 5px;
  right: -5px;
  bottom: -5px;
  border-radius: 16px;
  border: 2px solid var(--drupal-blue);
  opacity: 0.3;
  z-index: -1;
}

/* Control dots (unfilled circles) */
.gui-controls {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.gui-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid currentColor;
  background: transparent; /* Never fill! */
}
```

#### Simple Border Accent (for repeated cards/list items)
```css
/* Clean card with border accent - use for lists */
.card {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  border-left: 5px solid var(--drupal-blue);
  box-shadow: 0 4px 16px rgba(18, 40, 95, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(18, 40, 95, 0.15);
}

/* Priority variations */
.card.priority-high {
  border-left-color: var(--drupal-blue);
  background: linear-gradient(135deg, white 0%, #CCEDF9 100%);
}
.card.priority-medium { border-left-color: var(--drupal-dark-blue); }
.card.priority-low { border-left-color: var(--drupal-purple); }
```

#### 45° Shadow Lines Pattern (for backgrounds)
```css
.gui-shadow-lines {
  background: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 8px,
    currentColor 8px,
    currentColor 10px
  );
  opacity: 0.1;
}
```

### Color Variations by Purpose
| Purpose | Border Color | Use Case |
|---------|-------------|----------|
| Primary/CTA | Blue #009CDE | Main actions, featured content |
| Highlight | Yellow #FFC423 | Important items, milestones |
| Secondary | Dark Blue #006AA9 | Supporting content |
| Creative | Purple #CCBAF4 | Innovation, community |
| Alert | Red #F46351 | Warnings, urgent items |

### Rules
- Max 3 colors per block (including white)
- **Never fill control dots** - always outline only
- No gradients inside GUI Blocks
- Match corner radii on all layers
- Shadow offset should be consistent (45° diagonal, 4-6px)
- Control dots: 0-3 depending on space

### Frame vs Window
**As Frame**: Focus on 1-2 people, detail shots, impactful headlines
**As Window**: More copy space, multiple images, pair with background theme

### Decorative Usage
For visual interest, place semi-transparent GUI blocks in headers/backgrounds:
```css
.decorative-gui-block {
  position: absolute;
  border: 2px solid var(--drupal-blue);
  border-radius: 12px;
  opacity: 0.2;
  transform: rotate(-5deg); /* Slight rotation adds dynamism */
}
```

## Patterns & Gradients

### Patterns (6 available)
- Use at 10-20% opacity
- For subtle backgrounds
- Don't overpower content

### Gradients (6 available)
- Logo on gradients: Navy, White, or Black only
- Text must be W3C compliant with colors underneath

## Drop Window

Use Drop shape as photo/video window:
- Scale Greater/Community/Individual Drop shapes
- Create interesting branded frames

## Photography

**Attributes**: Warmth, Cooperation, Diversity, Friendliness

**Do**: Natural light, realistic settings, bright colors, diverse representation

**Don't**: B&W, sepia, duotone, HDR, filters

## Applications

### Presentations

**Important: For creating PowerPoint/Google Slides presentations, use [Manus](https://manus.anthropic.com) rather than Claude Code.**

Claude Code's MCP PowerPoint tools cannot reliably produce professional-quality presentations. The tools lack:
- Visual feedback for precise element positioning
- Support for complex formatting (shadows, gradients, effects)
- Proper layering and arrangement of shapes
- Real-time iteration on visual output

**Manus** can use actual presentation software GUIs via computer use, enabling professional results.

**To create a Drupal brand presentation with Manus:**
1. Go to [manus.anthropic.com](https://manus.anthropic.com)
2. Point it at this repo: `https://github.com/zivtech/drupal-brand-skill`
3. Ask it to use the **template as a starting point**: `templates/presentations/drupal-brand-template.pptx` or the [Google Slides template](https://docs.google.com/presentation/d/1bJ1GMZWMyeFWBPN9u49chepN7fhuGI4GJVt-DEw-S68/edit)
4. Reference the brand guidelines in this file for colors, typography, and GUI block styling

**For reference only:**
- Brand fonts and colors documented above
- Templates in `/assets/png/`

### Testing Presentation Output

After creating or modifying a presentation, analyze it for brand compliance issues and generate a custom fix checklist for the user.

#### Analysis Process

1. **Run the analysis script** (`/templates/presentations/analyze_deck.py`) on the PPTX file
2. **Identify specific issues** found in the deck (hard-coded fonts, off-brand colors, etc.)
3. **Generate a custom checklist** listing:
   - Which slides need attention
   - What specific fonts need replacement (and what to replace them with)
   - What specific colors are off-brand
   - Priority order (high/medium/low)

#### What the Analysis Detects

- **Hard-coded fonts**: Theme updates only change font *definitions*, not text with explicitly set fonts. The script identifies which non-brand fonts are present.
- **Off-brand colors**: Elements using RGB values outside the Drupal palette.

#### Deliverable

Provide the user with a **specific, actionable checklist** based on analysis results, including:
- Exact font replacements needed (e.g., "Replace Ubuntu with Noto Sans")
- Slide numbers requiring manual review
- Step-by-step instructions for bulk fixes in PowerPoint/Google Slides

See `/templates/presentations/BRAND_COMPLIANCE_CHECKLIST.md` for the checklist template structure.

### 3D/Environmental
- Patterns work in 2D and 3D
- Colors translate to physical materials

### Swag
- Apply GUI Blocks creatively
- Use approved color combos
- Maintain logo rules

## Accessibility

- WCAG AA contrast (4.5:1 minimum)
- Alt text for images
- Test in grayscale
- Semantic structure

## Presentation Migration

This skill uses the **[claude-presentation-toolkit](https://github.com/zivtech/claude-presentation-toolkit)** for programmatic presentation migration. The toolkit provides generic presentation processing capabilities, while this skill provides Drupal-specific brand configuration.

### Dependencies

- `claude-presentation-toolkit` - Generic presentation migration engine
- Brand config: `brand-config/presentation.yaml` - Drupal-specific colors, fonts, layouts

### Usage with Toolkit

```bash
# Install the toolkit
pip install git+https://github.com/zivtech/claude-presentation-toolkit.git

# Migrate a presentation to Drupal brand
pptx-migrate input.pptx output.pptx \
    --config brand-config/presentation.yaml \
    --template templates/presentations/drupal-brand-template.pptx

# Analyze for Drupal brand compliance
pptx-analyze deck.pptx --config brand-config/presentation.yaml
```

## File Structure

```
/logos/                CMS Product Logos (svg/, png/)
/graphics/             Primary Drupal Logos (svg/, png/)
/assets/               GUI Blocks & Templates (png/presentation/ for variants)
/backgrounds/          Slide backgrounds (drop cutouts, gradients)
/photos/               Stock photos and event photography
/client-logos/         Logos of organizations using Drupal
/screenshots/          UI screenshots for presentations
/colors/               PALETTES.md
/gradients/            6 gradient SVGs
/patterns/             Dynamic patterns (SVG and PNG)
/fonts/                ZT Gatha, Noto Sans
/templates/            Presentation templates (PPTX)
/brand-config/         Brand configuration for presentation toolkit
```
