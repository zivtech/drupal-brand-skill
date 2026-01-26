# Drupal Brand Compliance Checklist

Use this checklist to manually update a presentation to comply with Drupal brand guidelines.

## Pre-Flight

- [ ] Download the official Drupal fonts (ZT Gatha, Noto Sans) from `/fonts/`
- [ ] Install fonts on your system
- [ ] Have the color palette reference open (`/colors/PALETTES.md`)

---

## 1. Theme Colors

Update your presentation's color theme to use official Drupal colors:

### Primary Colors (Required)
| Role | Color Name | Hex Code | Where to Use |
|------|------------|----------|--------------|
| Accent 1 | Drupal Blue | #009CDE | Primary buttons, links, key highlights |
| Accent 2 | Drupal Navy | #12285F | Headers, footers, dark backgrounds |
| Accent 3 | Drupal Dark Blue | #006AA9 | Secondary accents |
| Dark 1 | Black | #000000 | Primary text |
| Light 1 | White | #FFFFFF | Backgrounds, text on dark |
| Dark 2 | Drupal Navy | #12285F | Secondary dark elements |
| Light 2 | Drupal Light Blue | #CCEDF9 | Light backgrounds |

### Secondary/Tertiary Colors (For variety)
| Color Name | Hex Code | Use For |
|------------|----------|---------|
| Drupal Yellow | #FFC423 | Highlights, CTAs, energy |
| Drupal Red | #F46351 | Alerts, emphasis |
| Drupal Green | #397618 | Success, growth |
| Drupal Purple | #CCBAF4 | Innovation, creativity |

### How to Update in PowerPoint
1. Go to **View → Slide Master**
2. Click **Colors → Customize Colors**
3. Update each color slot with the hex values above
4. Save as new theme

### How to Update in Google Slides
1. Go to **Slide → Edit theme**
2. Click **Colors → Choose a custom color**
3. Enter hex values for each element
4. Apply to all layouts

---

## 2. Typography

### Font Replacements
| Current Font | Replace With | Usage |
|--------------|--------------|-------|
| Ubuntu Light | ZT Gatha Bold | Headlines (H1) |
| Ubuntu | ZT Gatha SemiBold | Subheadings |
| Arial | Noto Sans Regular | Body text |
| Any sans-serif | Noto Sans | Body text |

### Font Sizes (Recommended)
| Element | Size | Font |
|---------|------|------|
| H1 / Title | 48-60px | ZT Gatha Bold |
| H2 / Section | 36-42px | ZT Gatha SemiBold or Noto Sans Bold |
| H3 / Subsection | 24-30px | Noto Sans Bold |
| Body | 16-18px | Noto Sans Regular |
| Caption | 12-14px | Noto Sans Regular |

### How to Bulk Replace Fonts

**PowerPoint:**
1. Go to **Home → Replace → Replace Fonts**
2. Select old font, choose new font
3. Click Replace All
4. Repeat for each font

**Google Slides:**
1. Use **Edit → Find and Replace** for text
2. For fonts: Select all text (Ctrl+A on each slide)
3. Change font family in toolbar

---

## 3. Slide-by-Slide Review

### Title Slides
- [ ] Logo placed correctly (use files from `/graphics/` or `/logos/`)
- [ ] Minimum clear space around logo (width of Individual Drop)
- [ ] Title in ZT Gatha Bold
- [ ] Subtitle in Noto Sans
- [ ] Background uses approved gradient or solid color

### Content Slides
- [ ] Headlines in ZT Gatha or Noto Sans Bold
- [ ] Body text in Noto Sans Regular
- [ ] Bullet points properly formatted
- [ ] Images have appropriate treatment (no filters, B&W, or heavy effects)
- [ ] Charts/graphs use brand colors

### Section Dividers
- [ ] Use brand gradients from `/gradients/` or solid brand colors
- [ ] Text is high contrast (check WCAG compliance)
- [ ] Logo visible if using dark background (use white or blue version)

---

## 4. Logo Usage

### Correct Logo Files
| Background | Logo to Use | Location |
|------------|-------------|----------|
| White/Light | Blue or Navy logo | `/graphics/svg/` |
| Dark/Navy | White or Blue logo | `/graphics/svg/` |
| Gradient | Navy, White, or Black | `/graphics/svg/` |

### Logo Don'ts
- [ ] Not rotated or skewed
- [ ] Not recolored (only approved colors)
- [ ] No added effects (shadows, glows, outlines)
- [ ] Not placed on busy backgrounds
- [ ] Minimum size respected (120px digital)

---

## 5. Images & Photography

- [ ] Photos show warmth, cooperation, diversity
- [ ] Natural lighting (no heavy HDR)
- [ ] No black & white or sepia filters
- [ ] No duotone effects
- [ ] Bright, optimistic colors

---

## 6. GUI Blocks (if applicable)

- [ ] Maximum 3 colors per block (including white)
- [ ] Control dots not filled
- [ ] No gradients inside blocks
- [ ] Corner radii match throughout
- [ ] 45-degree angles for shadow lines

---

## 7. Accessibility Check

- [ ] Text contrast meets WCAG AA (4.5:1 minimum)
- [ ] All images have alt text
- [ ] Logical reading order
- [ ] No color-only information

---

## 8. Final Review

- [ ] Open in presentation mode
- [ ] Check all slides for color consistency
- [ ] Verify fonts render correctly
- [ ] Test on projector if possible
- [ ] Export to PDF and verify

---

## Quick Color Reference

```
Drupal Blue:       #009CDE
Drupal Dark Blue:  #006AA9
Drupal Navy:       #12285F
Drupal Light Blue: #CCEDF9
Drupal Yellow:     #FFC423
Drupal Red:        #F46351
Drupal Green:      #397618
Drupal Purple:     #CCBAF4
Black:             #000000
White:             #FFFFFF
```

## Quick Font Reference

```
Headlines:    ZT Gatha Bold
Subheads:     ZT Gatha SemiBold / Noto Sans Bold
Body:         Noto Sans Regular
Emphasis:     Noto Sans Bold
Captions:     Noto Sans Regular (smaller)
```
