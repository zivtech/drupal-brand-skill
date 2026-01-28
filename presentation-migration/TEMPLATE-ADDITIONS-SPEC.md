# Template Additions Specification

New slide layouts needed to support complex content types found in real-world presentations.

## Current Gap Analysis

| Content Type | Current Handling | Result |
|--------------|------------------|--------|
| Stats infographic | All stats merged into 1-2 text runs | Layout destroyed |
| Case study (full) | 4 zones merged into body text | Bullets + quote mixed together |
| Team/credits table | Columns flattened | Structure lost |
| Logo/partner grid | Logos not migrated | Only title survives |

---

## 1. Stats Dashboard Layout

**Purpose:** Display 4-6 key metrics in a visual grid arrangement.

**Content Zones:**
```
┌─────────────────────────────────────────────────────────┐
│  [Stat 1]        [Stat 2]        [Stat 3]        [Stat 4] │
│   118k            46K+            1.4M            12%     │
│  Contributors   Developers    Users on D.o    Market Share│
│                                                           │
│              ┌─────────────────────┐                      │
│              │   Central Image     │           [Stat 5]   │
│              │   (optional)        │            51%       │
│              └─────────────────────┘           Growth     │
│                                                           │
│  [Stat 6 - Full Width]                                    │
│  "Millions of websites"                                   │
└─────────────────────────────────────────────────────────┘
```

**Placeholder Structure:**
- 4-6 text placeholders for stats (each ~3" x 2")
- Each stat placeholder contains: Large number + label below
- Optional central image placeholder
- Background: Drupal Blue (#009CDE) or photo with overlay

**Font Sizes:**
- Stat number: 72-96pt, ZT Gatha Bold, White
- Stat label: 18-24pt, Noto Sans, White or Light Blue

**Slide Index Suggestion:** Add as slides 49-50 in template

---

## 2. Case Study Full Layout

**Purpose:** Showcase customer success story with description, reasons, and quote.

**Content Zones:**
```
┌─────────────────────────────────────────────────────────┐
│ [Logo - 2" x 2"]                                        │
│                              ┌────────────────────────┐ │
│ [Description Text]           │                        │ │
│ 3-4 sentences about the      │    Screenshot          │ │
│ company and what they did    │    (image placeholder) │ │
│ with Drupal.                 │                        │ │
│                              └────────────────────────┘ │
│ **Why Drupal was chosen:**                              │
│ • Bullet point 1             ┌────────────────────────┐ │
│ • Bullet point 2             │ "Quote text here"      │ │
│ • Bullet point 3             │                        │ │
│ • Bullet point 4             │ — Attribution          │ │
│                              └────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Placeholder Structure:**
- `logo` - Image placeholder, top-left, 2" x 2"
- `description` - Text placeholder, left side, ~5" x 3"
- `bullets` - Text placeholder with bullet formatting, left bottom, ~5" x 3"
- `screenshot` - Image placeholder, right top, ~7" x 4"
- `quote_box` - GUI Block with quote + attribution, right bottom, ~7" x 3"

**Colors:**
- Left side: White background
- Quote box: Navy (#12285F) background, white text
- Or: White background with Blue GUI block frame

**Slide Index Suggestion:** Add as slides 51-52 in template

---

## 3. Team/Credits Layout

**Purpose:** Display team members or contributors in a structured table/grid.

**Content Zones:**
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  [Title: "Maintainers" or "Contributors"]               │
│                                                         │
│  ┌─────────────┬─────────────┬─────────────┐           │
│  │ Name        │ Organization│ Username    │           │
│  ├─────────────┼─────────────┼─────────────┤           │
│  │ Jane Doe    │ Acme Corp   │ @janedoe    │           │
│  │ John Smith  │ Example Inc │ @johnsmith  │           │
│  │ ...         │ ...         │ ...         │           │
│  └─────────────┴─────────────┴─────────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Option A: Table Layout**
- Title placeholder at top
- 3-column table with header row
- Supports 5-8 rows of content

**Option B: Card Grid Layout**
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Photo   │  │  Photo   │  │  Photo   │
│  Name    │  │  Name    │  │  Name    │
│  Role    │  │  Role    │  │  Role    │
│  @handle │  │  @handle │  │  @handle │
└──────────┘  └──────────┘  └──────────┘
```

**Colors:**
- Background: Drupal Blue (#009CDE)
- Text: White
- Links: Light Blue (#CCEDF9) or Yellow (#FFC423)

**Slide Index Suggestion:** Add as slides 53-54 in template

---

## 4. Logo Grid Layout

**Purpose:** Display partner logos, integrations, or client logos.

**Content Zones:**
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  [Title: "Integrated with tools you love"]              │
│                                                         │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                    │
│  │Logo1│  │Logo2│  │Logo3│  │Logo4│                    │
│  └─────┘  └─────┘  └─────┘  └─────┘                    │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                    │
│  │Logo5│  │Logo6│  │Logo7│  │Logo8│                    │
│  └─────┘  └─────┘  └─────┘  └─────┘                    │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                    │
│  │Logo9│  │Logo10│ │Logo11│ │Logo12│                   │
│  └─────┘  └─────┘  └─────┘  └─────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Placeholder Structure:**
- Title placeholder at top
- 12-16 image placeholders in a 4x3 or 4x4 grid
- Each logo placeholder: ~3" x 2"

**Colors:**
- Background: White
- Title: Navy (#12285F)

**Slide Index Suggestion:** Add as slides 55-56 in template

---

## Implementation Notes

### For Manus/Manual Creation:

1. Open `templates/presentations/drupal-brand-template.pptx`
2. Duplicate an existing slide as starting point
3. Add placeholders using Insert → Placeholder
4. Use placeholder types:
   - `<p:ph type="title"/>` for titles
   - `<p:ph type="body" idx="1"/>` for first body
   - `<p:ph type="body" idx="2"/>` for second body
   - `<p:ph type="pic"/>` for images

### For Migration Tool Updates:

After adding slides, update `presentation-migration/migrate.py`:

```python
# Add to SLIDE_CATALOG
SLIDE_CATALOG = {
    ...
    'stats_dashboard': [49, 50],
    'case_study_full': [51, 52],
    'team_credits': [53, 54],
    'logo_grid': [55, 56],
}

# Add to TEXT_CAPACITY
TEXT_CAPACITY = {
    ...
    'stats_dashboard': (20, 0, 7200, 0),      # Stats only, no body
    'case_study_full': (100, 400, 2400, 1400),
    'team_credits': (50, 500, 3200, 1400),
    'logo_grid': (80, 0, 3200, 0),            # Title only
}
```

### Content Detection Updates:

Add patterns to `detect_content_type()`:

```python
# Stats dashboard detection
stat_count = len(re.findall(r'\b\d+[%KMB+]?\b', combined))
if stat_count >= 4:
    return 'stats_dashboard'

# Logo grid detection
if 'partner' in combined or 'integration' in combined or 'tool' in combined:
    if slide.get('image_count', 0) >= 6:
        return 'logo_grid'
```

---

## Priority

1. **Case Study Full** - Most common complex layout in pitch decks
2. **Stats Dashboard** - High visual impact, frequently used
3. **Logo Grid** - Common for partner/integration slides
4. **Team Credits** - Less common, lower priority

---

## Next Steps

1. [ ] Create slides in PowerPoint/Manus using this spec
2. [ ] Add new slide indices to SLIDE_CATALOG in migrate.py
3. [ ] Add content detection patterns
4. [ ] Test with selection-from-brand-deck.pdf source content
5. [ ] Update README with new layout documentation
