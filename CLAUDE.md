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

Modular graphics inspired by computing interfaces.

### Creation
1. Create rounded rectangle
2. Duplicate, shift 45° diagonal (3 line widths apart)
3. Match corner radii
4. Add 0-3 control dots + shadow lines at 45°

### Rules
- Max 3 colors (including white)
- Don't fill control dots
- No gradients inside blocks
- Match corner radii

### Frame vs Window
**As Frame**: Focus on 1-2 people, detail shots, impactful headlines
**As Window**: More copy space, multiple images, pair with background theme

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
- Brand fonts and colors apply
- Templates in `/assets/png/`

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

## File Structure

```
/logos/      CMS Product Logos (svg/, png/)
/graphics/   Primary Logos (svg/, png/)
/assets/     GUI Blocks & Templates
/colors/     PALETTES.md
/gradients/  6 gradient SVGs
/patterns/   6 pattern SVGs
/fonts/      ZT Gatha, Noto Sans
```
