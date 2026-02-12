---
name: drupal-presentation-manus
description: Create and repair on-brand Drupal presentations using Manus. This skill uses the slide tools to build and fix decks, leveraging the assets and learned best practices from the drupal-brand-skill repo. Use this for creating new presentations or fixing existing ones with Manus.
---

# Drupal Presentation Creation & Repair with Manus

This skill guides Manus in creating and repairing brand-compliant Drupal presentations. It is based on the experience of building and fixing an 88-slide deck and contains the specific workflows, asset paths, layout techniques, and troubleshooting steps required for success.

## Core Principle: Avoid Common Pitfalls

Building presentations with code is fragile. This skill is designed to avoid common errors that lead to poor quality output. The most common errors are:

1.  **Stretched Images**: Using `background-size: 100% 100%` on GUI blocks or other images with fixed aspect ratios.
2.  **Missing Images**: Referencing incorrect or non-existent image paths, especially after migrating from other systems (e.g., CDN URLs).
3.  **Off-Center Text**: Text not being properly centered within GUI block frames or other layout elements.
4.  **Empty GUI Blocks**: Using a GUI block as a side-panel decoration without placing content (an image or text) inside it.

This skill provides specific techniques to prevent and fix these issues.

## Workflow

### 1. Initialization & Outline

Always start with `slide_initialize`. This creates the project structure and `slide_state.json` file that all other slide tools depend on.

-   **`project_dir`**: A new, dedicated directory for the presentation.
-   **`outline`**: Define all slides upfront. Each slide needs a unique `id`, `page_title`, and `summary`.
-   **`style_instruction`**: Provide a clear aesthetic direction, color palette, and typography. Refer to `/colors/PALETTES.md` and the brand guidelines for correct values.

### 2. Asset Gathering & Planning

Before writing slides, identify the visual assets needed. **Do not search for new assets unless explicitly requested.** All required assets are in this repository.

-   **Review the Asset Catalog**: Read the `references/asset_catalog.md` file to understand the available assets and their locations.
-   **Plan Image Usage**: For each slide in the outline, decide which photo, logo, or GUI block to use. This prevents missing images and ensures variety.

### 3. Slide Authoring (`slide_edit`)

Author slides one by one using `slide_edit`. This is the most critical step.

-   **Use Proven Layouts**: Refer to `references/layout_techniques.md` for battle-tested HTML/CSS patterns for common layouts (e.g., title slides, text-with-image, logo grids).
-   **Image-in-Frame Technique**: For placing images inside GUI blocks, use the `position: relative` and `position: absolute` overlay method described in the layout techniques.
-   **CSS Best Practices**: Use flexbox and grid for layout. Avoid absolute positioning for major page elements. Use `object-fit: contain` for images to prevent stretching.

### 4. Iterative Review & Repair

After authoring a few slides, or if the user reports issues, use a systematic repair process.

1.  **Read the slide HTML** to understand the current code.
2.  **Identify the issue** by comparing the code to the techniques in this skill (e.g., is it using `background-size: 100% 100%`?).
3.  **Rewrite the slide** using the correct layout pattern from `references/layout_techniques.md`.
4.  **Verify all image paths** are correct and point to files in the `assets` directories.

### 5. Final Presentation

Once all slides are authored and reviewed, use `slide_present` to deliver the final deck to the user.

## Key Reference Files

This skill relies on the following reference files. Read them as needed.

-   `references/asset_catalog.md`: A guide to the visual assets available in this repository.
-   `references/layout_techniques.md`: A cookbook of proven HTML/CSS patterns for common slide layouts.
-   `references/common_pitfalls.md`: A troubleshooting guide for the most frequent errors and their solutions.
