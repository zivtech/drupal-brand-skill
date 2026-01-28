# Drupal Brand Presentation Migration

Convert presentations from PDF, PPTX, Markdown, or CSV into brand-compliant Drupal presentations.

## Quick Start

```bash
cd presentation-migration

# Migrate from PDF (with automatic image extraction)
python3 migrate.py input.pdf output.pptx

# Migrate from PPTX
python3 migrate.py source.pptx output.pptx

# Skip image extraction (faster, smaller output)
python3 migrate.py input.pdf output.pptx --no-images

# With extended template (for stats dashboards, case studies)
python3 migrate.py input.pdf output.pptx --template ../templates/presentations/drupal-brand-template-extended.pptx
```

## Supported Input Formats

| Format | Best For | Limitations |
|--------|----------|-------------|
| **PDF** | Existing presentations exported as PDF | Text in images not extracted |
| **PPTX** | Source PowerPoint files | Layout info may be lost |
| **Markdown** | Writing new content from scratch | Requires specific format |
| **CSV** | Bulk slide data from spreadsheets | Simple title/body only |

---

## What You Need to Know Before Starting

### Automatic Features
- **Content type detection**: Stats, quotes, bullets, case studies auto-detected
- **Template selection**: Appropriate Drupal template slide chosen for each content type
- **Layout variety**: No consecutive identical layouts
- **Font scaling**: Text sized to fit placeholders
- **Image extraction & insertion**: Images from PDF/PPTX are extracted and inserted into output slides

### What Requires Manual Work

| Task | Why It's Manual | What to Do |
|------|-----------------|------------|
| **Text in images** | PyMuPDF can't read text embedded in graphics | Copy from original |
| **Logo grids** | Logos are images, not text | Note the slide, add logos manually |
| **Complex tables** | Structure gets flattened | Recreate in PowerPoint |
| **Some image placement** | Only slides with existing picture placeholders get images | Insert manually for text-only layouts |
| **Font cleanup** | Some hard-coded fonts persist | Run `analyze_deck.py`, bulk replace |

---

## PDF Input: Extraction Details

### What Gets Extracted Successfully
- Body text (paragraphs, bullets)
- Headings and titles
- Text in standard fonts
- Page structure/order

### What Does NOT Get Extracted

| Content Type | Why Not | How to Handle |
|--------------|---------|---------------|
| Text in images | PyMuPDF extracts text layers only | Open original, copy text manually |
| Decorative/styled titles | Often rendered as graphics | Manually type the title |
| Logo grids (partner slides) | Logos are images without alt text | Note slide purpose, add logos in PowerPoint |
| Tables | Structure not preserved | Recreate table in output |
| Charts/graphs | Rasterized to images | Screenshot and place manually |
| Infographic text | Usually embedded in graphic | Type out the statistics/labels |

### Recognizing Extraction Issues

When you run the migration, watch for warnings:

```
Page 1: WARNING: Only 30 chars extracted but 3 images found.
        Text may be embedded in images.
```

These pages need manual attention after migration.

---

## Image Pipeline

### How It Works
1. **Extraction**: Images are extracted from PDF/PPTX source files
2. **Filtering**: Small images (<100x100) are skipped (icons, bullets)
3. **Selection**: The largest image per slide is selected for insertion
4. **Insertion**: Image replaces the largest picture element in the template slide

### What Gets Inserted
- Hero/banner images
- Photo backgrounds
- Large screenshots

### What Doesn't Get Inserted
- Logo grids (too many small images)
- Slides without picture placeholders (text-only layouts like section dividers)
- Decorative template images are preserved

### Disabling Image Extraction

If you prefer to add images manually:
```bash
python3 migrate.py input.pdf output.pptx --no-images
```

---

## Step-by-Step Workflow

### 1. Prepare Your Input

**For PDF input:**
- Use "Save As PDF" or "Export to PDF" (NOT "Print to PDF" which rasterizes text)
- Best results from PowerPoint-exported PDFs

**For new content:**
- Use Markdown format (see examples below)

### 2. Run the Migration

```bash
python3 migrate.py your-deck.pdf output.pptx
```

### 3. Review the Extraction Summary

```
PDF has 13 pages

Extraction Summary:
  Page 1: WARNING: Only 30 chars extracted but 3 images found.
  Page 8: WARNING: Only 44 chars extracted but 17 images found.

2 pages may need manual review.

Content Type Detection:
Page  1: statement            | Promote Drupal Pitch Deck
Page  7: stats_dashboard      | Millions
Page 11: case_study           | "Now that the huge task of...
```

### 4. Open Output and Review

In PowerPoint/Google Slides, check each slide:
- [ ] All text visible (not cut off)
- [ ] Correct template layout chosen
- [ ] Flagged slides have content added manually

### 5. Run Brand Compliance Check

```bash
python3 ../templates/presentations/analyze_deck.py output.pptx
```

This identifies:
- Non-brand fonts needing replacement
- Off-brand colors

### 6. Apply Manual Fixes

**For missing text (from images):**
1. Open original PDF side-by-side
2. Copy text manually
3. Paste into output slide

**For wrong layout:**
1. Right-click slide → "Layout"
2. Choose different template
3. Adjust text in placeholders

**For bulk font replacement:**
1. In PowerPoint: Home → Replace → Replace Fonts
2. Replace detected non-brand fonts with Noto Sans

---

## Content Type Detection

The tool automatically detects these content types and selects appropriate templates:

| Type | Detection Pattern | Template Style |
|------|-------------------|----------------|
| `stats_dashboard` | 4+ statistics (%, K, M, $) | Multi-stat layout |
| `statistic` | Single prominent number | Large stat + body |
| `quote` | Starts with " or has — attribution | Quote slide |
| `case_study` | Customer name + transformation story | Case study layout |
| `case_study_full` | Bullets + quote together | Extended template (slide 50) |
| `bullet_list` | 3+ bullet points | Feature slide with bullets |
| `section_header` | Question or "What is..." format | Section divider |
| `numbered_step` | "Step 1", "Phase 2", etc. | Numbered sequence |

---

## Input Format Examples

### Markdown Format

```markdown
## Slide 1

**Title:** Welcome to Drupal
**Body:**
The flexible, powerful CMS for ambitious organizations.

---

## Slide 2

**Title:** 72%
**Body:**
of enterprise organizations choose Drupal for complex content needs

- Flexible content modeling
- Enterprise security
- Scalable architecture

---
```

### CSV Format

```csv
slide_number,title,body
1,Welcome to Drupal,"The flexible, powerful CMS"
2,72%,"of enterprise organizations choose Drupal"
```

---

## File Structure

```
presentation-migration/
├── migrate.py              # Main migration tool
├── test_migrate.py         # Test suite (14 tests)
├── README.md               # This file
├── add_template_slides.py  # Creates extended template
├── TEMPLATE-ADDITIONS-SPEC.md  # Spec for new layouts
├── test-output/            # Test artifacts (gitignored)
└── test-file/              # Test inputs (gitignored)

templates/presentations/
├── drupal-brand-template.pptx           # Standard (48 slides)
├── drupal-brand-template-extended.pptx  # With stats/case study (50 slides)
├── analyze_deck.py                      # Brand compliance checker
└── BRAND_COMPLIANCE_CHECKLIST.md        # Fix instructions
```

---

## Troubleshooting

### "No text extracted" for a slide

The slide likely has text as part of an image. Common for:
- Title slides with stylized text
- Hero images with overlaid text
- Infographics

**Solution:** Open the original and manually type the text.

### Wrong content type detected

The detection uses heuristic patterns. If it guesses wrong:
1. Change the slide layout manually in PowerPoint
2. Or pre-edit input to add detection hints (add "%" to stats, quotes around testimonials)

### Fonts look wrong in output

Template slides have placeholder fonts that may not apply to migrated text.

**Solution:** Run `analyze_deck.py` and follow the bulk replacement instructions.

### PyMuPDF not installed

```bash
pip install PyMuPDF
# Or with specific Python:
/Library/Frameworks/Python.framework/Versions/3.13/bin/pip3 install PyMuPDF
```

---

## Requirements

- Python 3.9+
- PyMuPDF (`pip install PyMuPDF`) - for PDF parsing
- lxml (`pip install lxml`) - for PPTX manipulation

---

## Known Limitations

1. **Images not auto-migrated** - Image extraction exists but reinsertion is not implemented
2. **Table structure lost** - Tables become plain text, need manual recreation
3. **Multi-column layouts** - Content merges into single column
4. **Vector graphics** - SVGs and charts in PDFs not extracted
5. **Embedded fonts** - Unusual fonts may not render correctly

---

## Brand Reference

| Color | Hex | Usage |
|-------|-----|-------|
| Drupal Blue | #009CDE | Primary, CTAs |
| Navy | #12285F | Headers, footers |
| Yellow | #FFC423 | Highlights |
| Red | #F46351 | Alerts, energy |

**Fonts:** ZT Gatha (headlines), Noto Sans (body)

---

## Testing

Run the test suite:
```bash
python3 test_migrate.py
```

All 14 tests should pass, covering:
- Title slides
- Statistics
- Quotes
- Bullet lists
- Content type detection
