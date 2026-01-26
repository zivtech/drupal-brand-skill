# Brand Compliance Testing & Tools

This directory contains tools, guides, and test results for bringing presentations and other assets into Drupal brand compliance.

## Overview

When you have existing presentations that need to align with Drupal brand guidelines, there are three main approaches. We've tested all three and documented the results.

## Approaches

| Approach | Best For | Effort | Completeness |
|----------|----------|--------|--------------|
| [1. Theme Update](./approach1-theme-update/) | Decks built with theme colors (rare) | Low | ~5-10% |
| [2. Manual Checklist](./approach2-checklist/) | Minor fixes, preserving layouts | Medium-High | Colors/fonts only |
| [3. Fresh Template](./approach3-fresh-template/) | Different design aesthetic | High | **100% (only full solution)** |

### Key Finding

**If your deck has a different design language than the Drupal brand template (missing GUI Blocks, different aesthetic), only Approach 3 will achieve true brand compliance.** Approaches 1 and 2 can fix colors and fonts, but cannot add design elements.

## Quick Start

1. **Read the comparison**: [APPROACH_COMPARISON.md](./APPROACH_COMPARISON.md)
2. **Pick your approach** based on your needs
3. **Follow the guide** in the relevant subdirectory

## Directory Structure

```
brand-compliance/
├── README.md                    # This file
├── APPROACH_COMPARISON.md       # Detailed comparison of all approaches
├── approach1-theme-update/
│   ├── README.md                # Theme update instructions
│   ├── drupal-theme.xml         # Drupal brand theme definition
│   └── drupal-pitch-deck-v3-theme-updated.pptx  # Example result
├── approach2-checklist/
│   └── BRAND_COMPLIANCE_CHECKLIST.md  # Comprehensive manual checklist
└── approach3-fresh-template/
    └── MIGRATION_GUIDE.md       # Guide for fresh template migration
```

## Test Case

These approaches were tested on:
- **Drupal Pitch Deck v2.0** (121 slides)
- Original issues: wrong theme, Ubuntu fonts, off-brand colors

## Using with Claude Code

After invoking `/drupal-brand`, you can ask:

- "Review my presentation for brand compliance"
- "Apply the theme update approach to my PPTX"
- "Generate a brand compliance checklist for my slides"
- "Help me migrate this slide to the official template"

## Contributing

Found a better approach? Have improvements to suggest?

1. Test your approach on a real presentation
2. Document the steps and results
3. Submit a PR with your findings

## Related Resources

- [Official Brand Template](../templates/presentations/)
- [Color Palettes](../colors/PALETTES.md)
- [Brand Guidelines](../drupal-brand-guidelines.md)
