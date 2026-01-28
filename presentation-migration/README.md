# Drupal Brand Presentation Migration

Migrate any presentation to the official Drupal brand template with full visual verification.

## Quick Start

### 1. Extract Content from Source

```bash
python extract_content.py source-presentation.pptx
```

Outputs:
- `source-presentation-catalog.md` - Text content by slide
- `source-presentation-images/` - Extracted images

### 2. Build New Deck

```bash
python migrate.py --input content-catalog.md --output new-deck.pptx
```

### 3. Test via PDF

```bash
# Convert to PDF
soffice --headless --convert-to pdf new-deck.pptx --outdir .

# For large decks, split into parts (Claude has PDF size limits)
pdftk new-deck.pdf cat 1-20 output part1.pdf
pdftk new-deck.pdf cat 21-40 output part2.pdf
```

### 4. Review with Claude

Ask Claude to read each PDF and check for issues:
- Text overflow
- Wrong fonts
- Off-brand colors
- Alignment problems

### 5. Fix Issues

Claude generates a checklist. Apply fixes in PowerPoint:
- Bulk font replacement: Home → Replace → Replace Fonts
- Manual fixes for individual slides

### 6. Re-verify

Convert to PDF again and confirm all issues resolved.

---

## Workflow Diagram

```
Source PPTX → Extract Content → Build Deck → PDF Test → Fix → Re-verify → Done
```

---

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Complete documentation |
| `SLIDE-CATALOG.md` | All 48 template slides with details |
| `migrate.py` | Migration script |
| `extract_content.py` | Content extraction |
| `template_map.json` | Layout mapping |

## Template

Location: `/templates/presentations/drupal-brand-template.pptx`

[Google Slides Version](https://docs.google.com/presentation/d/1bJ1GMZWMyeFWBPN9u49chepN7fhuGI4GJVt-DEw-S68/edit)

---

## Testing Notes

**PDF Size Limits**: Claude cannot read very large PDFs in one pass. For decks over 30-40 slides, split into smaller PDFs:

```bash
# Split into 20-page chunks
pdftk presentation.pdf cat 1-20 output part1.pdf
pdftk presentation.pdf cat 21-40 output part2.pdf
pdftk presentation.pdf cat 41-60 output part3.pdf
```

**Checklist Output**: After review, Claude generates a todo list for the content author with:
- Slide numbers needing fixes
- Specific issues (font, color, overflow)
- Priority (High/Medium)
- Recommended fix

See `SKILL.md` for complete testing workflow.

---

## Brand Reference

| Color | Hex |
|-------|-----|
| Drupal Blue | #009CDE |
| Navy | #12285F |
| Yellow | #FFC423 |
| Red | #F46351 |

**Fonts**: ZT Gatha (headlines), Noto Sans (body)

---

## Future Work: Additional Input Formats

The migration tool is designed to be extensible. Future versions should support additional input formats beyond PPTX, Markdown, and CSV:

### Planned Format Support

| Format | Use Case | Parsing Strategy |
|--------|----------|------------------|
| Word Documents (.docx) | Migration from Word-based presentations/handouts | Extract text, headings, images; map H1→title, body→content |
| PDF Files (.pdf) | Migration from locked/legacy decks | OCR or text extraction; page→slide mapping |
| Google Slides | Direct API integration | Use Google Slides API to extract slide content |
| HTML/Markdown | Web content migration | Parse document structure, extract headings and content blocks |

### Implementation Notes

Each format parser should:
1. Extract slide-like content units (page breaks, sections, or explicit markers)
2. Identify title vs body content
3. Extract and reference images
4. Output standard slide dictionaries compatible with `migrate_presentation()`

### Priority

1. **Word Documents** - Common for proposal content, easy win
2. **PDFs** - Useful for archived presentations
3. **HTML** - Website content migration
4. **Google Slides** - Native integration for Google Workspace users
