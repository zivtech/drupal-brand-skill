# Drupal Pitch Deck 2.0 → Brand Template Migration Plan

**Source:** drupal-pitch-deck-2.0.pptx (121 slides, ~230 images)
**Target:** Drupal Brand Template (48 slide designs)

---

## Executive Summary

This plan outlines the migration of the complete 121-slide Drupal Pitch Deck 2.0 to the official Drupal brand template. The deck is organized into **5 phases** based on content type and complexity.

---

## Phase Overview

| Phase | Slides | Content Type | Approach |
|-------|--------|--------------|----------|
| **1** | 1-19 | Intro & Value Props | Full migration with text + layout mapping |
| **2** | 20-115 | Case Studies (13 industries) | Batch processing by industry |
| **3** | 116-121 | Closing | Full migration |
| **4** | — | Images | Extract, organize, reinsert |
| **5** | — | QA & Polish | Visual verification, text fitting |

---

## Phase 1: Introduction & Value Propositions (Slides 1-19)

### Slide Mapping

| Source Slide | Content | Target Template Slide | Notes |
|--------------|---------|----------------------|-------|
| 1 | Title: Promote Drupal Pitch Deck | 0 (Title) | Blue bg, white text |
| 2 | Credits/License | 2 (Feature Yellow) | Attribution info |
| 3 | Maintainers | 26 (Multi-column) | 3 people layout |
| 4 | Build engaging experiences | 34 (Big Statement) | Hero slide |
| 5 | What is Drupal? | 2 (Feature Yellow) | Definition |
| 6 | Content Management | 6 (Content Left) | Benefits list |
| 7 | Channels (visual) | 4 (Photo) | Infographic |
| 8 | Marketing Integrations | 28 (Logo grid) | 17 tool logos |
| 9 | Turn Ideas Into Experiences | 6 (Content Left) | Feature bullets |
| 10 | High Performance | 7 (Content Right) | Feature bullets |
| 11 | Simplicity for Editors | 6 (Content Left) | Feature bullets |
| 12 | Multilingual | 7 (Content Right) | Feature bullets |
| 13 | Flexibility | 6 (Content Left) | Feature bullets |
| 14 | Security | 7 (Content Right) | Feature bullets |
| 15 | Accessibility | 6 (Content Left) | Feature bullets |
| 16 | API-First (visual) | 4 (Photo) | Diagram |
| 17 | Why Drupal? | 8 (Quote) | Positioning statement |
| 18 | Case Studies Header | 40 (Section Divider) | Blue bg |
| 19 | Guidance | 2 (Feature Yellow) | Instructions |

### Text Styling for Phase 1

| Background | Headline | Body |
|------------|----------|------|
| Blue #009CDE | White | White |
| Yellow #FFC423 | Navy | Black |
| White | Navy | Navy |
| Navy #12285F | White | White |

---

## Phase 2: Case Studies by Industry (Slides 20-115)

### Industry Breakdown

| Industry | Slides | Section Header | Case Studies |
|----------|--------|----------------|--------------|
| Sports | 20-25 | 1 | 5 |
| Government | 26-36 | 1 | 10 |
| Healthcare | 37-44 | 1 | 7 |
| Media & Publishing | 45-56 | 1 | 11 |
| NGOs | 57-62 | 1 | 5 |
| Nonprofits | 63-69 | 1 | 6 |
| Education | 70-78 | 1 | 8 |
| Arts & Culture | 79-80 | 1 | 1 |
| Travel & Tourism | 81-85 | 1 | 4 |
| Commerce | 86-92 | 1 | 6 |
| Banking & Finance | 93-98 | 1 | 5 |
| Enterprise | 99-102 | 1 | 3 |
| Membership | 103-107 | 1 | 4 |
| Misc | 108-115 | 1 | 7 |
| **TOTAL** | **96** | **14** | **82** |

### Case Study Template Mapping

Each industry section follows a consistent pattern:

```
1. Section Header (TITLE_1) → Template Slide 40 (Section Divider)
2. Case Study slides (ONE_COLUMN_TEXT_1_1 or BLANK) → Rotating templates:
   - Template 22: Content + Screenshot (left)
   - Template 24: Content + Screenshot (right)
   - Template 30: Stats highlight
   - Template 8: Quote testimonial
```

### Case Study Content Structure

Each case study typically contains:
- **Organization name** (headline)
- **Challenge/context** (1-2 sentences)
- **Why Drupal was chosen** (bullet list)
- **Results/quote** (optional)
- **Screenshot(s)** of website

### Batch Processing Strategy

Process one industry at a time:
1. Create section header slide
2. Process each case study:
   - Extract text content
   - Map to appropriate template
   - Alternate left/right layouts for visual variety
3. Verify text fits
4. Move to next industry

---

## Phase 3: Closing Slides (116-121)

| Source Slide | Content | Target Template |
|--------------|---------|-----------------|
| 116 | World of Digital Experiences | 34 (Big Statement) |
| 117-118 | Platform logos | 28 (Logo grid) |
| 119 | Submit your case study | 38 (Content Right) |
| 120 | Getting involved | 36 (Content Left) |
| 121 | Thank you | 46/47 (Closing) |

---

## Phase 4: Image Handling

### Image Categories

| Category | Count | Approach |
|----------|-------|----------|
| Website screenshots | ~150 | Extract, resize to template dimensions |
| Company logos | ~50 | Extract as PNG, place in logo grids |
| Marketing tool logos | 17 | Recreate logo grid slide |
| Decorative/icons | ~15 | Use template's built-in graphics |

### Image Extraction Process

```bash
# 1. Extract all images from source PPTX
unzip drupal-pitch-deck-2.0.pptx -d extracted/
ls extracted/ppt/media/

# 2. Catalog images by slide
# (Use python-pptx to map image → slide)

# 3. Organize by industry
mkdir -p images/{sports,government,healthcare,...}
```

### Image Placement Strategy

- **Screenshots**: Place in template picture placeholders
- **Logos**: Group in designated logo areas
- **Preserve aspect ratios**: Don't stretch images

---

## Phase 5: Quality Assurance

### Visual Verification Checklist

For each slide:
- [ ] Text fits within placeholder bounds
- [ ] Font size readable (min 14pt for body)
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Images properly positioned
- [ ] No text overflow/truncation
- [ ] Brand colors applied correctly

### PDF Verification Workflow

```
1. Save batch of slides as PPTX
2. Convert to PDF using platform-specific method:
   - macOS: osascript convert_to_pdf.scpt presentation.pptx
   - Windows: PowerShell COM automation
   - Linux: libreoffice --headless --convert-to pdf presentation.pptx
3. Read PDF with Claude to verify each slide
4. Review for issues
5. Fix and re-verify
```

### Common Issues to Watch

| Issue | Solution |
|-------|----------|
| Text overflow | Reduce content or use smaller font |
| Image cropping | Adjust placeholder size or image position |
| Color mismatch | Apply correct brand hex values |
| Font fallback | Ensure Noto Sans is embedded |

---

## Template Slide Usage Summary

| Template Slide | Usage | Count |
|----------------|-------|-------|
| 0 (Title) | Opening | 1 |
| 2 (Feature Yellow) | Definitions, credits | 4 |
| 4 (Photo) | Visual slides | 2 |
| 6 (Content Left) | Features, case studies | ~35 |
| 7 (Content Right) | Features, case studies | ~35 |
| 8 (Quote) | Testimonials | ~15 |
| 22 (Screenshot Left) | Case studies | ~20 |
| 24 (Screenshot Right) | Case studies | ~20 |
| 28 (Logo Grid) | Integrations | 2 |
| 30 (Stats) | Data highlights | ~10 |
| 34 (Big Statement) | Hero slides | 2 |
| 40 (Section Divider) | Industry headers | 14 |
| 46/47 (Closing) | Thank you | 1 |

---

## Execution Order

### Recommended Sequence

1. **Phase 1 first** - Establishes patterns, validates approach
2. **Phase 3 next** - Completes bookends
3. **Phase 4 parallel** - Image extraction while processing
4. **Phase 2 in batches** - One industry per session
5. **Phase 5 throughout** - QA after each batch

### Batch Sizes

- Process **5-10 slides per batch** for manageability
- Save and verify after each batch
- Industry sections are natural batch boundaries

---

## File Outputs

| Output | Purpose |
|--------|---------|
| `drupal-pitch-deck-v2-migrated.pptx` | Final migrated presentation |
| `migration-log.md` | Slide-by-slide mapping record |
| `images/` | Extracted and organized images |
| `verification-screenshots/` | Playwright QA screenshots |

---

## Success Criteria

- [ ] All 121 slides migrated to brand template
- [ ] Text content preserved accurately
- [ ] Images placed appropriately
- [ ] Brand colors and typography applied
- [ ] Visual verification passed for all slides
- [ ] No text overflow issues

---

*Plan created: January 2026*
*Source catalog: drupal-pitch-deck-2.0-catalog.md*
