# Drupal Brand Slide Template Catalog

This catalog provides comprehensive documentation for each slide layout in the Drupal brand presentation template, enabling AI tools and designers to select and populate the correct template for any presentation need.

**Template File**: `drupal-brand-template.pptx`
**Total Slides**: 48
**Unique Layouts**: 21

---

## Table of Contents

1. [Master Layout Reference](#master-layout-reference)
2. [Opening/Title Slides](#openingtitle-slides)
3. [Content Slides](#content-slides)
4. [Statistics & Data Slides](#statistics--data-slides)
5. [Quote Slides](#quote-slides)
6. [Photo Feature Slides](#photo-feature-slides)
7. [Two-Column Layouts](#two-column-layouts)
8. [Closing Slides](#closing-slides)
9. [Blank Templates](#blank-templates)

---

## Master Layout Reference

These are the 21 master layouts available in the template. Each slide inherits from one of these.

| Index | Layout Name | Placeholders | Primary Use |
|-------|-------------|--------------|-------------|
| 0 | TITLE_AND_BODY | 4 | Title + body text + optional image |
| 1 | Photo | 2 | Photo background with text overlay |
| 2 | TITLE | 3 | Simple title slide |
| 3 | Photo - Horizontal | 4 | Horizontal photo with text |
| 4 | Title - Centre | 2 | Centered title |
| 5 | Photo - Vertical | 4 | Vertical photo with text alongside |
| 6 | Title - Top | 2 | Top-aligned title |
| 7 | Title & Bullets | 3 | Title with bullet points |
| 8 | Title, Bullets & Live Video Small | 3 | Title, bullets, small video placeholder |
| 9 | Title, Bullets & Live Video Large | 3 | Title, bullets, large video placeholder |
| 10 | Bullets | 2 | Bullet list only |
| 11 | Photo - 3 Up | 4 | Three photo arrangement |
| 12 | Quote | 3 | Quote with attribution |
| 13 | Blank | 0 | Completely blank |
| 14 | TITLE_1 | 2 | Alternate title style |
| 15 | DEFAULT | 0 | Default blank |
| 16 | CUSTOM | 2 | Custom: title + image |
| 17 | ONE_COLUMN_TEXT_1_1 | 2 | Single column text |
| 18 | CUSTOM_1 | 2 | Custom: title + full-bleed image |
| 19 | TITLE_1_1 | 3 | Alternate title with body |
| 20 | BLANK | 1 | Blank with single placeholder |

---

## Text Styling Reference

### Color Quick Reference
| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Drupal Navy | #12285F | RGB(18, 40, 95) | Headlines on light backgrounds |
| Drupal Blue | #009CDE | RGB(0, 156, 222) | Primary brand, backgrounds |
| White | #FFFFFF | RGB(255, 255, 255) | Text on dark backgrounds |
| Black | #000000 | RGB(0, 0, 0) | Body text alternative |
| Yellow | #FFC423 | RGB(255, 196, 35) | Accent backgrounds |
| Coral/Red | #F46351 | RGB(244, 99, 81) | GUI block accent |

### Background-Based Text Rules

| Background Type | Headline | Body Text | Notes |
|-----------------|----------|-----------|-------|
| White/Light | Navy #12285F | Navy #12285F | Most common content slides |
| Drupal Blue #009CDE | White OR Navy | White OR Navy | Depends on slide type (see individual entries) |
| Navy #12285F | White | White | Quotes, emphasis slides |
| Yellow #FFC423 | Navy #12285F | Black or Navy | High-energy feature slides |
| Coral/Red #F46351 | Navy #12285F | Navy | Inside GUI blocks |
| Photo (full-bleed) | White (in GUI block) | White | Text always in GUI block |
| Gradient (purple-blue) | Navy #12285F | Navy | Two-column layouts |

### GUI Block Text Rules
- **Navy GUI block on light background**: White text inside
- **Blue/Light GUI block on any background**: Navy text inside
- **Coral/Red GUI block**: Navy text inside

---

## Opening/Title Slides

### SLIDE-TITLE-SPEAKER
**Slide Index**: 0
**Layout**: TITLE_AND_BODY
**Purpose**: Opening slide with presentation title and speaker information

**Visual Description**:
- Large headline in center-bottom area
- Speaker name and title below headline
- Drupal logo/branding in upper portion
- Drupal Blue (#009CDE) solid background

**Text Styling**:
| Element | Color | Font |
|---------|-------|------|
| Headline | White #FFFFFF | ZT Gatha Bold |
| Speaker info | White #FFFFFF | Noto Sans Regular |

**Placeholders**:
| Name | Type | Position (EMUs) | Size (EMUs) | Content Guidelines |
|------|------|-----------------|-------------|---------------------|
| Title | TITLE (1) | left: 1778000, top: 5747309 | 20828100 x 2780100 | Main headline, 2-3 lines max, ZT Gatha Bold |
| Body | BODY (2) | left: 1778000, top: 9772072 | 20828100 x 1587600 | Speaker name + title, Noto Sans |

**Best For**:
- Conference presentations
- Webinars
- Sales pitches
- Training sessions

**Example Content**:
```
Title: "Create ambitious experiences that scale"
Body: "Speaker Name\nSpeaker Title, Company"
```

---

### SLIDE-HERO-PHOTO
**Slide Index**: 1
**Layout**: ONE_COLUMN_TEXT_1_1
**Purpose**: Dramatic opening with full-bleed photo and headline overlay

**Visual Description**:
- Large photo covers most of slide (right side)
- Navy (#12285F) GUI block frame on left with headline
- Drop logo in bottom left (Drupal Blue)
- White background on left portion

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Headline | White #FFFFFF | ZT Gatha Bold | Inside Navy GUI block |

**Placeholders**:
| Name | Type | Position | Content Guidelines |
|------|------|----------|---------------------|
| Headline | TEXT_BOX | left: 2508525, top: 3333650 | Bold statement, 3-5 words per line, max 3 lines |

**Best For**:
- Opening impact
- Section dividers
- Inspirational messages

**Avoid When**:
- Need detailed information
- Multiple bullet points required

**Example Content**:
```
"Create ambitious digital experiences that scale"
```

---

### SLIDE-STATEMENT-CENTER
**Slide Index**: 3
**Layout**: Photo - Vertical
**Purpose**: Bold centered statement over pattern/light background

**Visual Description**:
- Light pattern background (diagonal lines)
- Single centered two-part headline
- Drupal logo in corner (Drupal Blue)
- Clean, minimalist design

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Primary headline | Navy #12285F | ZT Gatha Bold | Bold emphasis words |
| Secondary line | Navy #12285F | Noto Sans Regular | Lighter weight continuation |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Center Title | CENTER_TITLE (3) | left: 831200, top: 5615467 | 22721700 x 1844100 | Single powerful statement, 1-2 lines |

**Best For**:
- Key messages
- Mission statements
- Section transitions
- "Aha moment" slides

**Example Content**:
```
"Drupal is the platform
that unleashes your digital ambitions"
```

---

### SLIDE-SECTION-DIVIDER
**Slide Index**: 40
**Layout**: TITLE_AND_BODY
**Purpose**: Section divider with bold title and optional subtitle

**Visual Description**:
- Drupal Blue (#009CDE) solid background
- Large GUI block frame (white outline with control dots)
- Title text centered in left portion
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Section title | Navy #12285F | ZT Gatha Bold | Large, bold |
| Subtitle (if used) | Navy #12285F | Noto Sans Regular | Smaller, below title |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | left: 1778000, top: 4528109 | 20828000 x 2780182 | Section name, 3-5 words |

**Best For**:
- Introducing new sections
- Topic transitions
- Agenda items

**Example Content**:
```
"Lets talk about the unicorn"
Subtitle: "Sub Title Slide"
```

---

## Content Slides

### SLIDE-HEADLINE-BODY-LEFT
**Slide Index**: 2
**Layout**: ONE_COLUMN_TEXT_1_1
**Purpose**: Headline with supporting body text, visual on right

**Visual Description**:
- Yellow (#FFC423) solid background
- Large headline in upper left
- Body text below headline
- Photo in Drop shape on right
- White GUI block with Drupal logo badge in corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Headline | Navy #12285F | ZT Gatha Bold | Bold, impactful |
| Body text | Black #000000 | Noto Sans Regular | Supporting detail |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Body | BODY (2) | left: 2006450, top: 6858000 | 7434600 x 3600300 | 2-4 sentences, key supporting points |

**Best For**:
- Feature introductions
- Key concepts
- Value propositions

**Example Content**:
```
Headline: "The DXP foundation for ambitious organizations"
Body: "Get the benefits of DXP with the freedom to design your own roadmap and technology stack"
```

---

### SLIDE-FEATURE-GRID
**Slide Index**: 9
**Layout**: ONE_COLUMN_TEXT_1_1
**Purpose**: Feature/integration showcase with photo grid

**Visual Description**:
- White background
- Large headline and body text on left
- Grid of photos in multi-colored GUI block frames on right
- GUI blocks have Navy/Yellow/Blue/Coral borders
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Headline | Navy #12285F | ZT Gatha Bold | Large, 3-4 words per line |
| Body text | Navy #12285F | Noto Sans Regular | Paragraph format |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Body | BODY (2) | left: 1581000, top: 5209900 | 5762100 x 3600300 | Feature description, 2-3 sentences |

**Best For**:
- Integration showcases
- Partner logos
- Technology stack displays
- Ecosystem overviews

**Example Content**:
```
Headline: "Seamless integrations ready-to-go"
Body: "Thousands of add-ons are available that support your marketing tooling. You can control data privacy and how customer insights are used."
```

---

### SLIDE-FEATURE-BULLETS
**Slide Index**: 21
**Layout**: ONE_COLUMN_TEXT_1_1
**Purpose**: Feature with bullet point benefits

**Visual Description**:
- Drupal Blue (#009CDE) solid background (left half)
- White area or photo on right
- Photo in Yellow (#FFC423) GUI block frame
- Drupal badge at top right

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Headline | Navy #12285F | ZT Gatha Bold | Large, on blue background |
| Body text | Navy #12285F | Noto Sans Regular | Bullet points on blue bg |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Body | BODY (2) | left: 2634500, top: 6983938 | 6264000 x 3600300 | Bullet points, 3-5 items |

**Best For**:
- Feature details
- Benefit lists
- Capability overviews

**Example Content**:
```
Headline: "No vendor lock-in"
Body: "Get access to new core features every six months\n\nDon't pay for extra features or user accounts"
```

---

### SLIDE-CONTENT-RIGHT
**Slide Index**: 38
**Layout**: TITLE_AND_BODY
**Purpose**: Title and body on right, image on left

**Visual Description**:
- Drupal Blue (#009CDE) solid background
- Photo in white GUI block frame on left (with control dot)
- Title and body text on right
- Drupal Blue badge overlapping bottom right of photo
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Title | White #FFFFFF | ZT Gatha Bold | Large headline |
| Body text | White #FFFFFF | Noto Sans Regular | Paragraph format |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | left: 12324772, top: 1424709 | 10223501 x 2286001 | Section title, 3-6 words |
| Body | BODY (2) | left: 12410200, top: 3710700 | 10223400 x 8580600 | Detailed content, can include bullets |

**Best For**:
- Speaker bio slides
- Case study details
- Feature deep-dives

**Example Content**:
```
Title: "Title right"
Body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
```

---

## Statistics & Data Slides

### SLIDE-STAT-LARGE
**Slide Index**: 10
**Layout**: Photo - Vertical
**Purpose**: Large statistic with supporting context

**Visual Description**:
- White background
- GUI block on left with control dots (Navy/Yellow/Blue layered frames)
- Large statistic number inside GUI block
- Supporting headline and bullet points on right
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Large statistic | Drupal Blue #009CDE | ZT Gatha Bold | Inside GUI block, very large |
| Context headline | Navy #12285F | ZT Gatha Bold | "56% of Government Websites run on Drupal" |
| Bullet label | Navy #12285F | Noto Sans Bold | "Compliance", "Supported", etc. |
| Bullet text | Navy #12285F | Noto Sans Regular | Supporting detail |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | left: 2595850, top: 4722375 | 6714900 x 4236600 | Large stat (e.g., "56%") |
| Body | BODY (2) | left: 11669725, top: 2809788 | 9891900 x 7536600 | Context + 3 bullet points |

**Best For**:
- Market statistics
- Adoption numbers
- Impact metrics
- Research findings

**Example Content**:
```
Title: "56%"
Body: "56% of Government Websites run on Drupal\n\nCompliance - Control over data residency; accessibility & security\n\nSupported - A network of certified Drupal Partners\n\nComposability - You pick the tools you want to integrate with"
```

---

## Quote Slides

### SLIDE-QUOTE
**Slide Index**: 8
**Layout**: Quote
**Purpose**: Customer/testimonial quote with attribution

**Visual Description**:
- Navy (#12285F) solid background
- Large white GUI block frame with control dots (3 unfilled circles)
- Quote in center of GUI block
- Attribution below quote
- Drupal logo badge in bottom right of GUI block

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Quote text | White #FFFFFF | ZT Gatha Bold | Large, impactful |
| Attribution name | White #FFFFFF | Noto Sans Bold | Speaker name emphasized |
| Attribution title | White #FFFFFF | Noto Sans Regular | Title/company below name |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Attribution | BODY (2) | left: 4150475, top: 9424775 | 13327200 x 1210800 | Name + Title + Company |
| Quote | BODY (2) | left: 4233050, top: 4712850 | 15552300 x 4114200 | Quote text, use curly quotes |

**Best For**:
- Customer testimonials
- Expert endorsements
- Case study quotes
- Leadership statements

**Avoid When**:
- Quote is longer than 3 sentences
- No attribution available

**Example Content**:
```
Quote: ""Drupal strips away barriers to innovative development.""
Attribution: "David Munn\nHead of Information Technology at Greater London Authority"
```

---

### SLIDE-QUOTE-CENTERED
**Slide Index**: 41
**Layout**: TITLE_AND_BODY
**Purpose**: Large centered quote or short impactful text

**Visual Description**:
- Navy (#12285F) solid background
- Large white GUI block frame (rounded rectangle with control dot)
- Text centered in GUI block
- Drupal Blue badge in bottom right of GUI block
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Quote/Statement | White #FFFFFF | Noto Sans Regular | Large, centered in GUI block |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | left: 3333172, top: 2848669 | 16032000 x 8018700 | Short quote or statement |

**Best For**:
- Short powerful quotes
- Key takeaways
- Transition statements

**Example Content**:
```
"Quote or Short Text"
```

---

## Photo Feature Slides

### SLIDE-PHOTO-LOGOS
**Slide Index**: 4
**Layout**: Photo
**Purpose**: Statement with client/partner logos

**Visual Description**:
- White background
- Client/partner logos arranged on left (grid layout)
- Navy (#12285F) GUI block on right with statement
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Statement | White #FFFFFF | ZT Gatha Bold | Inside Navy GUI block |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Body | BODY (2) | left: 15855373, top: 4131071 | 7887296 x 5453858 | Single statement, 1-2 lines |

**Best For**:
- "Who uses Drupal" slides
- Client showcases
- Partner highlights

**Example Content**:
```
"The most powerful brands run on Drupal"
```

---

### SLIDE-PHOTO-TEXT-LEFT
**Slide Index**: 35
**Layout**: Photo
**Purpose**: Photo background with text in GUI block on left

**Visual Description**:
- Full-bleed photo background
- Blue (#009CDE) GUI block frame on left with control dots
- White Drupal badge inside GUI block
- Clean, minimal design

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Statement | White #FFFFFF | ZT Gatha Bold | Inside Blue GUI block |

**Placeholders**: None (uses TEXT_BOX)

**Best For**:
- Community highlights
- Culture slides
- Visual storytelling

**Example Content**:
```
"Community is in our DNA"
```

---

### SLIDE-PHOTO-TEXT-RIGHT
**Slide Index**: 47
**Layout**: Photo
**Purpose**: Text in GUI block on left, open area on right

**Visual Description**:
- White background
- Navy (#12285F) filled GUI block on left with 45° shadow lines
- Statement text inside the Navy block
- Photo placeholder area on right (optional)
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Statement | White #FFFFFF | Noto Sans Regular | Inside Navy GUI block |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Body | BODY (2) | left: 2961548, top: 4334271 | 7887300 x 5454000 | Description text, 2-4 sentences |

**Best For**:
- Team introductions
- Community highlights
- Photo essays

**Example Content**:
```
"Active makers"
```

---

## Two-Column Layouts

### SLIDE-TWO-COLUMN-BULLETS
**Slide Index**: 42
**Layout**: TITLE_AND_BODY
**Purpose**: Two-column layout with separate titles and bullet content

**Visual Description**:
- Drupal Blue (#009CDE) solid background
- Large GUI block frame (white outline with control dots at corners)
- Two equal columns inside frame
- Each column has title + body text
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Column titles | White #FFFFFF | ZT Gatha Bold | Large column headers |
| Body text | White #FFFFFF | Noto Sans Regular | Paragraph text |
| Bullet points | White #FFFFFF | Noto Sans Regular | List items |

**Alternate Variant** (Slide 44 - Navy text):
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Column titles | Navy #12285F | ZT Gatha Bold | For smaller title variant |
| Body text | White #FFFFFF | Noto Sans Regular | Body remains white |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Main Title | TITLE (1) | left: 1778000, top: 4528109 | 20828100 x 2780100 | Optional main title |
| Left Title | TITLE (1) | left: 2030775, top: 2111525 | 9833100 x 2286000 | Left column header |
| Left Body | BODY (2) | left: 2030775, top: 4528100 | 9833100 x 7536600 | Left column bullets |
| Right Title | TITLE (1) | left: 12561575, top: 2111525 | 9833100 x 2286000 | Right column header |
| Right Body | BODY (2) | left: 12561575, top: 4528100 | 9833100 x 7536600 | Right column bullets |

**Best For**:
- Comparison slides
- Before/after
- Two related topics
- Pros/cons

**Example Content**:
```
Left Title: "Two Column Title"
Left Body: "Bullet 1\nBullet 2\nBullet 3"
Right Title: "Title"
Right Body: "Lorem ipsum..."
```

---

### SLIDE-SPEAKER-BIO
**Slide Index**: 36
**Layout**: TITLE_AND_BODY
**Purpose**: Speaker biography with photo

**Visual Description**:
- Drupal Blue (#009CDE) solid background
- Photo in pink/magenta GUI block frame on left (with control dots)
- Name as large title on right
- Bio bullet points below name
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Speaker name | White #FFFFFF | ZT Gatha Bold | Large, prominent |
| Bio bullets | White #FFFFFF | Noto Sans Regular | Bullet list format |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | left: 12324772, top: 1424709 | 10223501 x 2286001 | Speaker name |
| Body | BODY (2) | left: 12410200, top: 3710700 | 10223400 x 8580600 | Bio bullets |
| Image | PICTURE (18) | left: 3352200, top: 3227725 | 6802876 x 7876203 | Headshot photo |

**Best For**:
- Speaker introductions
- Team member highlights
- Expert profiles

**Example Content**:
```
Title: "Baddý Sonja Breidert"
Body: "Icelandic\nCEO and Co-Founder of 1xINTERNET\nDrupal contributor since 2013\nBoard member of the Drupal Association 2018-2023\nBoard Chair 2022-2023"
```

---

## Closing Slides

### SLIDE-CTA-CLOSING
**Slide Index**: 33
**Layout**: Photo - Vertical
**Purpose**: Closing slide with call-to-action

**Visual Description**:
- Light diagonal stripe pattern background
- Two-line centered text
- Bold headline + lighter tagline
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Primary CTA | Navy #12285F | ZT Gatha Bold | "Build the open web with Drupal" |
| Secondary tagline | Navy #12285F | Noto Sans Regular | "Create remarkable websites that scale" |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Center Title | CENTER_TITLE (3) | left: 831200, top: 5615467 | 22721700 x 1844100 | CTA + tagline |

**Best For**:
- Presentation endings
- Call-to-action slides
- Contact information

**Example Content**:
```
"Build the open web with Drupal
Create remarkable websites that scale"
```

---

### SLIDE-CLOSING-STATEMENT
**Slide Index**: 46
**Layout**: DEFAULT
**Purpose**: Final statement with full visual

**Visual Description**:
- White background
- Large GUI block frame (light blue outline with control dot)
- Multi-line text statement inside block
- Drupal Blue badge in bottom right of block
- Drupal Blue logo in bottom right corner

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Statement | Black #000000 | Noto Sans Regular | Multi-line, inside GUI block |

**Best For**:
- Final thoughts
- Mission statements
- Brand messages

**Note**: This slide has no editable placeholders - text is in fixed AUTO_SHAPE.

**Example Content**:
```
"Drupal is the leading open CMS that gives you the power to bring your brand to life with innovative digital experiences..."
```

---

## Blank Templates

### SLIDE-BLANK-TITLE-IMAGE
**Slide Index**: 27
**Layout**: CUSTOM
**Purpose**: Clean template with title and image placeholders only

**Visual Description**:
- Title area on left
- Image placeholder on right
- Minimal background elements
- Maximum flexibility

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | left: 3222775, top: 3376275 | 6867600 x 4546500 | Headline text |
| Image | PICTURE (18) | left: 11308350, top: 2882975 | 7214700 x 7336200 | Photo or graphic |

**Best For**:
- Custom content slides
- Flexible layouts
- When other templates don't fit

---

### SLIDE-BLANK-IMAGE-FULL
**Slide Index**: 28
**Layout**: CUSTOM_1
**Purpose**: Template with full-bleed image and title

**Visual Description**:
- Full-height image on right (edge to edge)
- Title area on left
- Clean, modern layout

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | left: 2781575, top: 2877475 | 5582400 x 4853400 | Headline, can be multi-line |
| Image | PICTURE (18) | left: 11433200, top: 0 | 12950700 x 13716000 | Full-bleed vertical image |

**Best For**:
- Photo-forward slides
- Visual storytelling
- When image is the focus

---

## Numbered Content Series

### SLIDE-NUMBERED-CONTENT (02-05)
**Slide Indices**: 29, 30, 31, 32
**Layout**: Photo - Vertical
**Purpose**: Sequential numbered content slides

**Visual Description**:
- White background
- GUI block on left with large number
- Body text paragraphs on right
- Different GUI block colors for each number:
  - 02: Coral (#F46351) filled
  - 03: Blue (#009CDE) outline
  - 04: Yellow (#FFC423) filled
  - 05: Coral (#F46351) outline

**Text Styling**:
| Element | Color | Font | Notes |
|---------|-------|------|-------|
| Number (02, 04) | Navy #12285F | ZT Gatha Bold | Inside colored GUI block |
| Number (03, 05) | Blue #009CDE or Coral #F46351 | ZT Gatha Bold | Inside outline GUI block |
| Body text | Navy #12285F | Noto Sans Regular | Paragraph format |

**Placeholders**:
| Name | Type | Position | Size | Content Guidelines |
|------|------|----------|------|---------------------|
| Title | TITLE (1) | varies | varies | Number (02, 03, 04, 05) |
| Body | BODY (2) | varies | varies | Content paragraphs |

**Best For**:
- Step-by-step processes
- Numbered lists
- Sequential topics
- Agenda items

**Example Content**:
```
Title: "02"
Body: "Lorem ipsum dolor sit amet..."
```

---

## Usage Guidelines

### Content Import Strategy

When importing content into a presentation, follow these steps:

#### 1. Content Analysis
Before selecting slides, analyze your source content:
- **Identify key messages**: What are the 3-5 main points?
- **Count content types**: How many stats, quotes, features, bullets?
- **Assess imagery needs**: What photos or screenshots are required?
- **Determine flow**: Opening → Problem → Solution → Evidence → CTA

#### 2. Slide Variety & Visual Balance
Create visual interest by alternating layouts:

| Sequence | Layout Pattern | Why |
|----------|---------------|-----|
| Slide N | Content LEFT, Image RIGHT | Establishes pattern |
| Slide N+1 | Image LEFT, Content RIGHT | Creates visual rhythm |
| Slide N+2 | Full-width statement | Breaks monotony |
| Slide N+3 | Content LEFT, Image RIGHT | Returns to pattern |

**Avoid**: 3+ consecutive slides with same layout orientation.

#### 3. Background Color Rotation
Vary background colors to maintain engagement:

| Content Type | Recommended Backgrounds |
|--------------|------------------------|
| Opening | Drupal Blue (#009CDE) |
| Key statement | White with pattern |
| Feature content | Yellow (#FFC423) or White |
| Statistics | White with GUI blocks |
| Quotes | Navy (#12285F) |
| Section dividers | Drupal Blue (#009CDE) |
| Closing | Light pattern or gradient |

**Rule**: Never use the same background color for 3+ consecutive slides.

### Text Color by Background (Accessibility)

**WCAG AA requires 4.5:1 contrast ratio for body text, 3:1 for large text.**

| Background | Headline Color | Body Text | Contrast Ratio |
|------------|---------------|-----------|----------------|
| White #FFFFFF | Navy #12285F | Navy #12285F | 12.6:1 ✓ |
| Drupal Blue #009CDE | White #FFFFFF | White #FFFFFF | 3.4:1 ✓ (large text only) |
| Drupal Blue #009CDE | Navy #12285F | Navy #12285F | 3.7:1 ✓ (large text only) |
| Navy #12285F | White #FFFFFF | White #FFFFFF | 12.6:1 ✓ |
| Yellow #FFC423 | Navy #12285F | Black #000000 | 10.2:1 / 12.4:1 ✓ |
| Coral #F46351 | Navy #12285F | Navy #12285F | 3.3:1 ✓ (large text only) |

**Important Notes**:
- On Drupal Blue backgrounds, body text should be kept **large** (18pt+) for accessibility
- Navy (#12285F) on white provides excellent contrast for all text sizes
- Never use Drupal Blue text on Navy background (insufficient contrast)
- Test all combinations with a contrast checker tool

### Selecting the Right Slide

| Need | Recommended Slide |
|------|-------------------|
| Opening with speaker info | SLIDE-TITLE-SPEAKER (0) |
| Bold opening statement | SLIDE-HERO-PHOTO (1) or SLIDE-STATEMENT-CENTER (3) |
| Feature with supporting body | SLIDE-HEADLINE-BODY-LEFT (2) - Yellow bg |
| Introduce a section | SLIDE-SECTION-DIVIDER (40) |
| Show a statistic | SLIDE-STAT-LARGE (10) |
| Customer quote | SLIDE-QUOTE (8) - Navy bg |
| Feature with bullets | SLIDE-FEATURE-BULLETS (21) |
| Content with photo (image right) | SLIDE-FEATURE-GRID (9) |
| Content with photo (image left) | SLIDE-CONTENT-RIGHT (38) |
| Two topics comparison | SLIDE-TWO-COLUMN-BULLETS (42) |
| Speaker bio | SLIDE-SPEAKER-BIO (36) |
| Community/culture | SLIDE-PHOTO-TEXT-LEFT (35) |
| Closing CTA | SLIDE-CTA-CLOSING (33) |
| Custom content | SLIDE-BLANK-TITLE-IMAGE (27) |

### GUI Block Color Variations

GUI blocks can use different color combinations:

| GUI Block Style | Border Colors | Best For |
|-----------------|--------------|----------|
| Standard | Navy + Yellow + Blue | Statistics, features |
| Blue outline | Blue (#009CDE) | Photos on white bg |
| Navy filled | Navy solid | Statements, quotes |
| Coral filled | Coral (#F46351) | Energy, action items |
| Yellow filled | Yellow (#FFC423) | Highlights, key points |
| White outline | White strokes | On dark backgrounds |

### Position Units

All positions are in EMUs (English Metric Units):
- 914400 EMUs = 1 inch
- 12700 EMUs = 1 point
- Slide dimensions: 24384000 x 13716000 EMUs (typical 16:9)

### Content Best Practices

1. **Headlines**: Keep to 2-3 lines max, use ZT Gatha Bold
2. **Body text**: Use Noto Sans, keep paragraphs short (16pt minimum for accessibility)
3. **Bullet points**: 3-5 items per slide maximum
4. **Statistics**: Use large, bold numbers (72pt+) with brief context
5. **Quotes**: Include attribution, keep under 3 sentences
6. **Images**: Use high-quality photos that support the message
7. **Contrast**: Always verify text is readable against background

### Placeholder Naming Convention

When referencing placeholders programmatically:
- `idx: 0` = Primary title
- `idx: 1` = Primary body
- `idx: 2` = Secondary element (varies)
- `idx: 4294967295` = Special/center elements

### Accessibility Checklist

Before finalizing any slide:
- [ ] Text contrast meets WCAG AA (4.5:1 body, 3:1 large text)
- [ ] Font size is 16pt minimum for body text
- [ ] No text overlaps images without sufficient contrast
- [ ] Alternative text descriptions for images (in speaker notes)
- [ ] Color is not the only way information is conveyed
- [ ] Heading hierarchy is logical (H1 → H2 → Body)

---

## Slide Variations & Alternates

Many slide types have visual variations. Use these to create variety:

### Statistic Slide Variations (based on slides 11-17)

| Variation | GUI Block Style | Stat Color | Body Text Position |
|-----------|----------------|------------|-------------------|
| Standard (slide 11) | Navy/Yellow/Blue outline | Drupal Blue | Right side |
| Inverted (slide 12) | Coral filled | Navy | Left side |
| Photo left (slides 13-14) | Coral filled | White | On photo bg |
| With logos (slide 14) | Navy filled | White | Logo grid right |
| Photo bg (slides 16-17) | Navy filled OR Blue outline | White | Overlaid on photo |

### Feature Slide Variations (based on slides 18-22)

| Variation | Background | GUI Block | Text Colors |
|-----------|-----------|-----------|-------------|
| Yellow feature (slide 18) | White | Yellow filled | Navy headline on yellow |
| Coral feature (slide 19) | White | Coral filled | White text on coral |
| Outline left (slide 20) | White | Navy/Yellow/Blue outline | Navy on white |
| Outline right (slide 21) | White | Navy/Yellow/Blue outline | Navy on white |
| Blue half (slide 22) | Blue + White split | Yellow frame | Navy on blue |

### Photo Background Variations

| Style | Text Treatment | Best For |
|-------|---------------|----------|
| GUI block overlay | White text in Navy/Blue block | High-impact statements |
| Faded photo | Text over faded area | When photo is secondary |
| Split layout | Clean half for text | Balance of text and visual |

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-27 | 1.0 | Initial catalog creation |
| 2026-01-27 | 1.1 | Added text styling for all slides, accessibility guidelines, content import strategy, variation documentation |
