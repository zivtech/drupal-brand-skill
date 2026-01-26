# Approach 1: Theme XML Update

Programmatically update a PPTX file's theme to use Drupal brand colors and fonts.

## How It Works

PPTX files are ZIP archives containing XML files. The theme is defined in `ppt/theme/theme1.xml`. By modifying this file, we can update:

- Color scheme (accent colors, dark/light variants)
- Font scheme (major/minor fonts)
- Link colors

## Steps

### 1. Extract the PPTX

```bash
mkdir pptx-contents
unzip your-presentation.pptx -d pptx-contents
```

### 2. Update the Theme

Replace the color and font definitions in `pptx-contents/ppt/theme/theme1.xml`.

**Color Mapping (Original → Drupal)**:
```
accent1: → 009CDE (Drupal Blue)
accent2: → 12285F (Drupal Navy)
accent3: → 006AA9 (Drupal Dark Blue)
accent4: → FFC423 (Drupal Yellow)
accent5: → F46351 (Drupal Red)
accent6: → 397618 (Drupal Green)
dk2:     → 12285F (Drupal Navy)
lt2:     → CCEDF9 (Drupal Light Blue)
hlink:   → 009CDE (Drupal Blue)
folHlink: → 006AA9 (Drupal Dark Blue)
```

**Font Mapping**:
```
majorFont (headlines): → ZT Gatha
minorFont (body):      → Noto Sans
```

### 3. Repackage the PPTX

```bash
cd pptx-contents
zip -r ../updated-presentation.pptx .
```

## Drupal Brand Theme XML

Use this as a reference or replacement for your theme file:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
         name="Drupal Brand Theme">
  <a:themeElements>
    <a:clrScheme name="Drupal Brand">
      <a:dk1><a:srgbClr val="000000"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="12285F"/></a:dk2>
      <a:lt2><a:srgbClr val="CCEDF9"/></a:lt2>
      <a:accent1><a:srgbClr val="009CDE"/></a:accent1>
      <a:accent2><a:srgbClr val="12285F"/></a:accent2>
      <a:accent3><a:srgbClr val="006AA9"/></a:accent3>
      <a:accent4><a:srgbClr val="FFC423"/></a:accent4>
      <a:accent5><a:srgbClr val="F46351"/></a:accent5>
      <a:accent6><a:srgbClr val="397618"/></a:accent6>
      <a:hlink><a:srgbClr val="009CDE"/></a:hlink>
      <a:folHlink><a:srgbClr val="006AA9"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Drupal">
      <a:majorFont>
        <a:latin typeface="ZT Gatha"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="Noto Sans"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:minorFont>
    </a:fontScheme>
    <!-- ... format scheme remains unchanged ... -->
  </a:themeElements>
</a:theme>
```

## Included Files

- `drupal-pitch-deck-v3-theme-updated.pptx` - Example result from applying this approach to the Drupal Pitch Deck v2.0

## Limitations

This approach only affects elements that reference the theme:

| What Changes | What Doesn't Change |
|--------------|---------------------|
| Theme-linked colors | Hard-coded hex colors |
| Theme-linked fonts | Hard-coded font names |
| Chart colors (if theme-based) | Embedded images |
| SmartArt (if theme-based) | Text with direct formatting |

## Automation Script

For batch processing, here's a shell script:

```bash
#!/bin/bash
# update-pptx-theme.sh

INPUT="$1"
OUTPUT="${INPUT%.pptx}-drupal-branded.pptx"
TEMP_DIR=$(mktemp -d)

# Extract
unzip -q "$INPUT" -d "$TEMP_DIR"

# Update theme (using sed for simple replacement)
sed -i '' 's/val="FFAB40"/val="009CDE"/g' "$TEMP_DIR/ppt/theme/theme1.xml"
sed -i '' 's/val="212121"/val="12285F"/g' "$TEMP_DIR/ppt/theme/theme1.xml"
# ... add more replacements as needed

# Repackage
cd "$TEMP_DIR"
zip -rq "$OUTPUT" .
mv "$OUTPUT" "$(dirname "$INPUT")/"

# Cleanup
rm -rf "$TEMP_DIR"

echo "Created: $OUTPUT"
```

## Next Steps

After applying the theme update, use [Approach 2 (Checklist)](../approach2-checklist/) to fix any remaining hard-coded elements.
