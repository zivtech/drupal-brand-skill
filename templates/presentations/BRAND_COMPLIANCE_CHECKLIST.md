# Drupal Brand Compliance Checklist Template

This is a template for generating custom fix checklists after analyzing a presentation. The analysis script identifies specific issues, and this template provides the structure for actionable fixes.

---

## How to Use This Template

1. Run `analyze_deck.py` on the presentation
2. Fill in the sections below based on analysis results
3. Provide the completed checklist to the user

---

## Pre-Flight Setup

- [ ] Download Drupal fonts from `/fonts/` (ZT Gatha, Noto Sans)
- [ ] Install fonts on your system
- [ ] Have color reference open (`/colors/PALETTES.md`)

---

## Section 1: Font Replacements

*Fill in based on analysis results - list the specific fonts found that need replacement.*

### Fonts Found That Need Replacement

| Found Font | Replace With | Reason |
|------------|--------------|--------|
| *[font name]* | *[ZT Gatha or Noto Sans]* | *[headline/body]* |

### How to Replace (PowerPoint)

1. Go to **Home → Replace → Replace Fonts**
2. Select the font to replace from dropdown
3. Select replacement font
4. Click **Replace**
5. Repeat for each font in the table above

### How to Replace (Google Slides)

1. Select all text on slide (Ctrl/Cmd+A)
2. Change font family in toolbar
3. Repeat for each slide

---

## Section 2: Color Fixes

*Fill in based on analysis results - list specific off-brand colors found.*

### Off-Brand Colors Found

| Slide(s) | Color Found | Replace With | Element |
|----------|-------------|--------------|---------|
| *[slide #]* | *[#hexcode]* | *[Drupal color + hex]* | *[shape/text/fill]* |

### Drupal Color Palette Reference

```
Drupal Blue:       #009CDE  (Primary, CTAs)
Drupal Dark Blue:  #006AA9  (Accents)
Drupal Navy:       #12285F  (Headers, footers)
Drupal Light Blue: #CCEDF9  (Light backgrounds)
Drupal Yellow:     #FFC423  (Highlights)
Drupal Red:        #F46351  (Alerts, energy)
Drupal Green:      #397618  (Success)
Drupal Purple:     #CCBAF4  (Innovation)
Black:             #000000  (Text)
White:             #FFFFFF  (Backgrounds)
```

---

## Section 3: Slides Requiring Manual Review

*List specific slides from analysis results.*

### High Priority (Multiple Issues)
- [ ] Slide *[#]*: *[title]* - *[issues]*

### Medium Priority (Font Issues)
- [ ] Slide *[#]*: *[title]* - *[font found]*

### Lower Priority (Color Issues)
- [ ] Slide *[#]*: *[title]* - *[color issue]*

---

## Section 4: Slide-by-Slide Checklist

### Title Slide
- [ ] Logo from `/graphics/` or `/logos/` (correct version for background)
- [ ] Clear space around logo (width of Individual Drop minimum)
- [ ] Title in **ZT Gatha Bold**
- [ ] Subtitle in **Noto Sans**
- [ ] Background uses brand gradient or solid color

### Section Dividers
- [ ] Background uses brand gradient or solid Navy/Blue
- [ ] Text has high contrast (white on dark, navy on light)
- [ ] Logo visible if present (use white or blue version on dark)

### Content Slides
- [ ] Headlines in **ZT Gatha Bold** or **Noto Sans Bold**
- [ ] Body text in **Noto Sans Regular**
- [ ] Charts/graphs use brand colors only

### Image Slides
- [ ] Photos show warmth, diversity, cooperation
- [ ] No B&W, sepia, or duotone filters
- [ ] Natural lighting, bright colors

---

## Section 5: Logo Usage Check

### Correct Logo for Background

| Background | Use This Logo |
|------------|---------------|
| White/Light | Blue or Navy |
| Dark/Navy | White or Blue |
| Gradient | Navy, White, or Black |

### Logo Don'ts
- [ ] Not rotated or skewed
- [ ] Not recolored (only approved colors)
- [ ] No added effects (shadows, glows, outlines)
- [ ] Minimum size: 120px digital

---

## Section 6: Accessibility Check

- [ ] Text contrast meets WCAG AA (4.5:1 minimum)
- [ ] All images have alt text
- [ ] Logical reading order
- [ ] No color-only information

---

## Section 7: Final Review

- [ ] View in presentation mode
- [ ] Check all slides for color consistency
- [ ] Verify fonts render correctly
- [ ] Export to PDF and review

---

## Summary

| Metric | Count |
|--------|-------|
| Total slides | *[#]* |
| Clean (no issues) | *[#]* |
| Need fixes | *[#]* |
| - High priority | *[#]* |
| - Medium priority | *[#]* |
| - Lower priority | *[#]* |

### Recommended Fix Order

1. **Bulk font replacement** - fixes most issues quickly
2. **Color fixes** - review flagged slides
3. **Manual review** - title slide, section dividers, key content
4. **Re-run analysis** - verify fixes applied
