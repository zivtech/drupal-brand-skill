# Approach 3: Fresh Template Migration

**This is the only approach that achieves full brand compliance when your source deck has a different design aesthetic than the Drupal brand template.**

## When This Approach is Required

- Source deck lacks GUI Block design elements
- Source deck uses a different visual language (no outlined frames, different patterns)
- You need the full Drupal brand look, not just color/font fixes
- The deck will be used for external/high-stakes presentations

## Prerequisites

1. **Official Drupal Brand Template**
   - Google Slides: [Drupal Brand Template](https://docs.google.com/presentation/d/1bJ1GMZWMyeFWBPN9u49chepN7fhuGI4GJVt-DEw-S68/edit)
   - PowerPoint: `/templates/presentations/drupal-brand-template.pptx`

2. **Source deck** you want to migrate

3. **Drupal brand fonts installed** (ZT Gatha, Noto Sans) from `/fonts/`

---

## Migration Workflow

### Phase 1: Preparation

#### 1.1 Inventory the Source Deck

Create a slide inventory spreadsheet or document:

```
| Slide # | Type | Title/Content Summary | Priority | Target Layout |
|---------|------|----------------------|----------|---------------|
| 1 | Title | "Promote Drupal Pitch Deck v2.0" | High | Title Slide |
| 2 | Section | "Introduction" | High | Section Divider |
| 3 | Content | Key Drupal benefits (bullets) | Medium | Content Layout |
| ... | ... | ... | ... | ... |
```

**Priority levels:**
- **High**: Title, section dividers, key message slides
- **Medium**: Supporting content slides
- **Low**: Appendix, detailed reference slides

#### 1.2 Identify Template Layouts

Review the Drupal brand template and note available layouts:

| Layout Name | Best For |
|-------------|----------|
| Title Slide | Opening slide, major section starts |
| Section Divider | Chapter breaks, topic transitions |
| Content (bullets) | Text-heavy informational slides |
| Two Column | Comparisons, side-by-side content |
| Image + Text | Feature highlights with visuals |
| Full Image | Impact slides, photography |
| Quote | Testimonials, key statements |
| Stats/Numbers | Data highlights |

#### 1.3 Extract Text Content (Optional)

For large decks, extract text programmatically:

```bash
# Extract all text from PPTX slides
unzip -p source.pptx 'ppt/slides/slide*.xml' | \
  grep -oP '(?<=<a:t>)[^<]+' | \
  grep -v '^$' > slide-content.txt
```

---

### Phase 2: Migration (Iterative)

Work in priority order: High → Medium → Low

#### 2.1 For Each Slide:

1. **Identify the slide type** and best matching template layout
2. **Create new slide** in template using that layout
3. **Copy text content** (paste as plain text to strip formatting)
4. **Apply template styling** (should happen automatically with layouts)
5. **Handle images**:
   - Re-import images
   - Place within GUI Block frames if applicable
   - Ensure proper sizing and positioning
6. **Review and adjust** spacing, alignment

#### 2.2 Content Transformation Guidelines

| Source Element | Transform To |
|----------------|--------------|
| Plain bullet list | Template bullet style |
| Numbered list | Template numbered style |
| Standalone image | Image in GUI Block frame |
| Screenshot | Screenshot in device mockup or GUI Block |
| Chart/graph | Recreate with brand colors |
| Quote text | Quote layout with attribution |
| Statistics | Stats layout with large numbers |

#### 2.3 Image Treatment

The new Drupal brand uses GUI Blocks as frames around images:

**Before** (old style):
```
┌──────────────┐
│    Image     │
└──────────────┘
```

**After** (new brand):
```
┌──────────────────┐
│ ┌──────────────┐ │
│ │    Image     │ │
│ └──────────────┘ │
│        ○ ○ ○     │  ← Control dots
└──────────────────┘
     ↑ GUI Block outline
```

Use GUI Block assets from `/assets/` or recreate using the guidelines in the brand documentation.

---

### Phase 3: Quality Assurance

#### 3.1 Visual Consistency Check

- [ ] All slides use template layouts (no custom formatting)
- [ ] Typography is consistent (ZT Gatha headlines, Noto Sans body)
- [ ] Colors are from brand palette only
- [ ] GUI Block frames used appropriately
- [ ] Logo placement follows guidelines

#### 3.2 Content Integrity Check

- [ ] All source content has been migrated
- [ ] No text truncated or hidden
- [ ] Images are high quality (not stretched/pixelated)
- [ ] Links still work
- [ ] Speaker notes preserved (if needed)

#### 3.3 Accessibility Check

- [ ] Text contrast meets WCAG AA (4.5:1)
- [ ] Alt text on images
- [ ] Logical reading order
- [ ] No color-only information

---

## Example Migration: Title Slide

### Source (v2.0)
```
┌─────────────────────────────────┐
│                                 │
│    [Background Image]           │
│                                 │
│    Promote Drupal Pitch Deck    │
│              v2.0               │
│                                 │
└─────────────────────────────────┘
Font: Ubuntu Light
Colors: Non-brand
```

### Target (v3.0)
```
┌─────────────────────────────────┐
│ [Brand Gradient Background]     │
│                                 │
│  ┌─────────┐                    │
│  │ Drupal  │  Promote Drupal    │
│  │  Logo   │  Pitch Deck        │
│  └─────────┘                    │
│              v3.0               │
│         ○ ○ ○                   │
│   [GUI Block decorative]        │
└─────────────────────────────────┘
Font: ZT Gatha Bold (title), Noto Sans (version)
Colors: Brand gradient, Navy text
```

### Migration Steps:
1. Start with Title Slide layout from template
2. Update title text: "Promote Drupal Pitch Deck"
3. Update version: "v3.0"
4. Verify logo is properly placed
5. Adjust any decorative GUI Block elements

---

## Time Estimates by Deck Size

| Deck Size | Estimated Effort |
|-----------|------------------|
| Small (< 20 slides) | 1-2 hours |
| Medium (20-50 slides) | 3-5 hours |
| Large (50-100 slides) | 1-2 days |
| Very Large (100+ slides) | 2-4 days |

**Note**: These estimates assume familiarity with the template and straightforward content. Complex graphics or charts add time.

---

## Tips for Efficiency

1. **Batch similar slides** - Do all bullet-list slides together, all image slides together, etc.

2. **Use keyboard shortcuts**:
   - `Ctrl+Shift+V` (Paste without formatting)
   - `Ctrl+D` (Duplicate slide)

3. **Create a "parts bin" slide** with commonly used elements:
   - GUI Block frames in various sizes
   - Decorative elements
   - Icon set

4. **Don't perfectionism early** - Get content in first, polish later

5. **Review in presentation mode** periodically to see how it flows

---

## Deliverables

After migration, you should have:

1. **New presentation file** (v3.0) using brand template
2. **Migration log** noting any issues or decisions made
3. **Source content archive** (original deck preserved)

---

## Related Resources

- [Brand Template](../../templates/presentations/)
- [GUI Block Guidelines](../../assets/README.md)
- [Color Palettes](../../colors/PALETTES.md)
- [Typography Guidelines](../../CLAUDE.md)
