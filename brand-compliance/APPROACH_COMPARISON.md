# Brand Compliance Approaches: Comparison & Recommendations

This document compares three approaches for bringing presentations into Drupal brand compliance.

## Test Case

- **Source**: Drupal Pitch Deck v2.0 (121 slides)
- **Issues Found**:
  - Non-Drupal theme ("CTI Digital Master Theme")
  - Wrong fonts (Ubuntu Light/Ubuntu instead of ZT Gatha/Noto Sans)
  - Off-brand colors (orange, teal, lime green instead of Drupal palette)

---

## Approach 1: Theme XML Update

**Method**: Programmatically modify the PPTX theme file to use Drupal brand colors and fonts.

### What We Changed
```xml
<!-- Colors -->
accent1: FFAB40 → 009CDE (Drupal Blue)
accent2: 212121 → 12285F (Drupal Navy)
accent3: 78909C → 006AA9 (Drupal Dark Blue)
accent4: FFAB40 → FFC423 (Drupal Yellow)
accent5: 0097A7 → F46351 (Drupal Red)
accent6: EEFF41 → 397618 (Drupal Green)
dk2: 595959 → 12285F (Drupal Navy)
lt2: EEEEEE → CCEDF9 (Drupal Light Blue)

<!-- Fonts -->
majorFont: Arial → ZT Gatha
minorFont: Arial → Noto Sans
```

### Results
| Aspect | Result |
|--------|--------|
| Theme colors | Updated in definition |
| Elements using theme colors | Should recolor (if any exist) |
| Hard-coded colors | NOT changed |
| Theme fonts | Updated in definition |
| Hard-coded fonts | NOT changed (slides still show Ubuntu) |
| GUI Blocks / Design elements | NOT added |
| Overall visual appearance | **Virtually unchanged** |
| Effort | Low (automated) |
| Completeness | **~5-10%** for this deck |

### Actual Test Results
When tested on the Drupal Pitch Deck v2.0:
- **Visual difference**: Minimal to none
- **Why**: The entire deck uses hard-coded colors, fonts, and lacks the GUI Block design language of the new brand
- **Missing**: Outlined image frames, gradient backgrounds, brand patterns, proper typography

### Verdict
**Good for**: Decks built with theme-referenced colors/fonts (rare)
**Bad for**: Most real-world decks, especially those with a different design aesthetic
**Reality check**: This approach is only useful as a first step, not a solution

---

## Approach 2: Manual Checklist

**Method**: Provide a comprehensive checklist for manual brand compliance updates.

### What's Included
- Pre-flight setup (fonts, color reference)
- Theme color update instructions
- Font replacement steps (with bulk replace)
- Slide-by-slide review checklist
- Logo usage guidelines
- Accessibility checks

### Results
| Aspect | Result |
|--------|--------|
| Completeness | 100% (if followed fully) |
| Effort | High (manual work per slide) |
| Skill required | Moderate (PowerPoint/Slides proficiency) |
| Consistency | Depends on user diligence |
| Reusability | High (checklist works for any deck) |

### Verdict
**Good for**: Important presentations where quality matters, smaller decks, users comfortable with presentation software
**Bad for**: Very large decks (100+ slides), tight deadlines

---

## Approach 3: Fresh Template Migration

**Method**: Start with the official brand template, migrate content from source.

### What's Involved
- Copy official template
- Extract text content from source
- Rebuild slides using brand-compliant layouts
- Re-import and adjust images
- Quality check

### Results
| Aspect | Result |
|--------|--------|
| Completeness | 100% (guaranteed brand compliance) |
| Effort | Highest (full rebuild) |
| Quality | Highest (clean, consistent) |
| Risk | May lose nuanced layouts |
| Time | Significant for large decks |

### Verdict
**Good for**: Decks needing major overhaul, critical external presentations, when starting fresh makes sense
**Bad for**: Quick turnarounds, decks with complex custom layouts you want to preserve

---

## Recommendation Matrix

| Scenario | Recommended Approach |
|----------|---------------------|
| Deck uses theme colors (rare) | **Approach 1** (Theme Update) |
| Minor color tweaks needed | **Approach 2** (Checklist) |
| Different design aesthetic than new brand | **Approach 3** (Fresh Template) - **Required** |
| Missing GUI Blocks, brand patterns | **Approach 3** (Fresh Template) - **Required** |
| High-stakes external presentation | **Approach 3** (Fresh Template) |
| Deck has complex custom layouts to preserve | **Approach 2** (Checklist) - accept partial compliance |
| Tight deadline, low stakes | **Approach 1** (Theme Update) - minimal improvement |

### Key Finding from Testing

**If your source deck has a fundamentally different design language than the target brand template, Approach 3 (Fresh Template Migration) is the only viable path.**

Approach 1 and 2 can only fix colors and fonts - they cannot add:
- GUI Block design elements
- Outlined image frames
- Brand-specific gradients and patterns
- The overall visual aesthetic

---

## Combined Approach (Recommended for Most Cases)

For best results, combine approaches:

1. **Start with Approach 1** (Theme Update)
   - Quick win, fixes theme-dependent elements
   - Takes minutes, not hours

2. **Follow up with Approach 2** (Checklist)
   - Address hard-coded elements
   - Focus on high-visibility slides (title, section breaks, key content)
   - Skip minor internal slides if time-constrained

3. **Use Approach 3** (Fresh Template) for:
   - Title slide (make great first impression)
   - Key slides shown to external audiences
   - Slides that are badly broken

---

## Files Included in This Test

```
/approach1-theme-update/
  └── drupal-pitch-deck-v3-theme-updated.pptx  # Theme-modified version

/approach2-checklist/
  └── BRAND_COMPLIANCE_CHECKLIST.md            # Comprehensive manual checklist

/approach3-fresh-template/
  └── MIGRATION_GUIDE.md                       # Guide for template migration
```

---

## Try It Yourself

1. Open `drupal-pitch-deck-v3-theme-updated.pptx` to see Approach 1 results
2. Use the checklist to manually improve specific slides
3. For critical slides, migrate to the official template

Report findings and improvements back to the skill repository!
