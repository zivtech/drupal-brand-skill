# Drupal Brand Assets

Official Drupal brand assets and guidelines for creating on-brand designs, marketing materials, and visual content. This repository also serves as a Claude Code skill for AI-assisted brand guidance.

## Installation

To use this as a Claude Code skill, symlink the repository to your skills directory:

```bash
ln -s /path/to/drupal-brand-skill ~/.claude/skills/drupal-brand
```

Or clone directly into your skills folder:

```bash
git clone https://github.com/your-org/drupal-brand-skill.git ~/.claude/skills/drupal-brand
```

## Usage

Once installed, invoke the skill in Claude Code using:

```
/drupal-brand
```

The skill provides brand expertise for both answering questions and actively applying guidelines to your work:

- **Color recommendations** - Get the right hex codes and color combinations for your design
- **Logo guidance** - Understand which logo variant to use and placement rules
- **Typography selection** - Choose appropriate fonts and sizes for headlines and body text
- **GUI Block creation** - Learn how to create on-brand modular graphics
- **Asset location** - Find the right files in this repository for your needs

### Example Prompts

After invoking `/drupal-brand`, you can ask questions:

- "What colors should I use for a professional presentation?"
- "Where can I find the primary Drupal logo in SVG format?"
- "What font should I use for headlines?"
- "What are the rules for placing the logo on dark backgrounds?"

You can also direct Claude to apply brand guidelines to assets you're working on:

- "Review this CSS file and update the colors to match Drupal brand guidelines"
- "Check this HTML template for brand compliance and fix any issues"
- "Update the typography in this component to use the correct fonts"
- "Generate a color palette CSS file using the official Drupal colors"
- "Create an SVG banner using the brand gradients and patterns"

## Testing

To verify the skill is working correctly:

1. **Check the symlink**:
   ```bash
   ls -la ~/.claude/skills/drupal-brand
   ```
   Should point to this repository.

2. **Verify skill loads**:
   Start a new Claude Code session and type `/drupal-brand`. The skill should activate without errors.

3. **Test basic queries**:
   - Ask "What is the primary Drupal brand color?" - Should respond with #009CDE (Drupal Blue)
   - Ask "Where are the logo files?" - Should reference `/graphics/` and `/logos/` directories
   - Ask "What font is used for headlines?" - Should respond with ZT Gatha Bold

4. **Test asset access**:
   Ask Claude to read a specific asset file to verify the skill can access repository contents.

## Folder Structure

```
drupal-brand-skill/
├── logos/            # Drupal CMS Product Logos (SVG + PNG)
├── graphics/         # Primary Drupal Logos - Drop & Wordmark (SVG + PNG)
├── assets/           # GUI Blocks & Template Graphics
├── colors/           # Color Palettes & Specifications
├── gradients/        # Brand Gradient SVGs
├── patterns/         # Dynamic Pattern SVGs
├── fonts/            # ZT Gatha & Noto Sans Typefaces
├── templates/        # Ready-to-use presentation & document templates
└── brand-compliance/ # Tools & guides for updating existing assets
```

## Quick Reference

| Need | Location |
|------|----------|
| Primary Drupal logo | `/graphics/svg/` or `/graphics/png/` |
| Drupal CMS product logo | `/logos/svg/` or `/logos/png/` |
| GUI Block elements | `/assets/svg/` or `/assets/png/` |
| Color specifications | `/colors/PALETTES.md` |
| Gradient backgrounds | `/gradients/` |
| Dynamic patterns | `/patterns/` |
| Brand fonts | `/fonts/` |
| Presentation templates | `/templates/presentations/` |
| Brand compliance tools | `/brand-compliance/` |

## Brand Compliance Tools

Have an existing presentation or asset that needs to align with Drupal brand guidelines? We've tested three approaches:

| Approach | Best For | Effort |
|----------|----------|--------|
| Theme Update | Quick fixes, theme-dependent decks | Low |
| Manual Checklist | Quality-focused updates | Medium |
| Fresh Template | Complete overhauls | High |

See `/brand-compliance/` for detailed guides, checklists, and example results.

## Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Drupal Blue | #009CDE | Primary brand color |
| Drupal Dark Blue | #006AA9 | Dark accents |
| Drupal Navy | #12285F | Headers, footers |
| Drupal Light Blue | #CCEDF9 | Light backgrounds |
| Drupal Yellow | #FFC423 | Highlights |
| Drupal Red | #F46351 | Alerts, energy |
| Drupal Green | #397618 | Success |
| Drupal Purple | #CCBAF4 | Innovation |

## Typography

- **Headlines**: ZT Gatha Bold/SemiBold
- **Body**: Noto Sans Regular
- **H2/Subheads**: Noto Sans Bold or ZT Gatha SemiBold

## Documentation

Each folder contains a README with detailed usage guidelines. See also:
- `drupal-brand-guidelines.md` - Comprehensive brand guidelines
- `CLAUDE.md` - AI assistant skill for brand guidance

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/claude-code) installed and configured
- Skill must be symlinked or cloned to `~/.claude/skills/`

## Updating the Skill

To update the skill with latest brand assets or guidelines:

```bash
cd ~/.claude/skills/drupal-brand
git pull origin main
```

The updated skill will be available in your next Claude Code session.

## Manus Presentation Skill

For users who want to create Drupal-branded presentations using [Manus](https://manus.im), a dedicated skill is available in the `manus-skill/` directory. This approach does not require Claude Code or the `ai-presentation-toolkit` and is suitable for users who want a browser-based workflow.

The skill provides a comprehensive workflow, asset catalog, and proven layout techniques for building and repairing presentations using Manus's native slide tools. It is based on the experience of building an 88-slide Drupal pitch deck and contains specific troubleshooting guidance for common issues.

To use this skill, point Manus at this repository and reference `manus-skill/SKILL.md`.
