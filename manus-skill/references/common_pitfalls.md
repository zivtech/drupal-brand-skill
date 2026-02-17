# Common Pitfalls and Solutions

This document outlines the most common issues encountered when building presentations with code and how to fix them.

## 1. Stretched Images

-   **Problem**: Images, especially GUI blocks, appear stretched or distorted.
-   **Cause**: Using `background-size: 100% 100%` on an element with a different aspect ratio than the image.
-   **Solution**: 
    -   For `<img>` tags, use `object-fit: contain`.
    -   For `background-image`, use `background-size: contain` and `background-repeat: no-repeat`.

## 2. Missing Images

-   **Problem**: Slides show broken image icons.
-   **Cause**: The `src` path in the `<img>` tag is incorrect, or the file does not exist.
-   **Solution**:
    1.  Verify the file exists in one of the asset directories (`/photos`, `/assets/png/presentation`, etc.).
    2.  Ensure the path in the HTML is an absolute path from the root of the sandbox (e.g., `/home/ubuntu/drupal-brand-skill/photos/photo.jpg`).
    3.  Check for typos in the filename.

## 3. Off-Center Text

-   **Problem**: Text is not correctly centered within a container or GUI block.
-   **Cause**: Incorrect or missing CSS properties for centering.
-   **Solution**: Use a combination of flexbox properties:
    -   `display: flex`
    -   `align-items: center` (for vertical centering)
    -   `justify-content: center` (for horizontal centering)
    -   `text-align: center` (for multi-line text)

## 4. Empty GUI Blocks

-   **Problem**: A slide has a side-by-side layout with a GUI block on one side, but the block is empty.
-   **Cause**: The GUI block was intended as a decorative frame, but no content was placed inside it.
-   **Solution**: Use the "Image Inside a GUI Block Frame" technique from `layout_techniques.md` to place a relevant photo inside the block.

## 5. Text Overflowing GUI Block Boundaries

-   **Problem**: Text placed inside a GUI block frame extends beyond the visible rounded-rectangle area.
-   **Cause**: Using `background-image` for the GUI block and relying on padding alone, which doesn't account for the rounded corners and decorative elements (dots, shadow lines) of the frame image.
-   **Solution**: Use the `position: relative` / `position: absolute` overlay approach:
    1.  Create a container with `position: relative` and explicit dimensions (e.g., `width: 100%; height: 680px`).
    2.  Place the GUI block as an `<img>` with `width: 100%; height: 100%; object-fit: fill`.
    3.  Overlay text with `position: absolute` and percentage-based insets: `top: 10%; left: 8%; right: 8%; bottom: 12%`.
    4.  The insets keep text within the visible area of the rounded rectangle, away from corners and decorative dots.

## 6. White Space Below Slides in Iframe

-   **Problem**: Slides rendered in iframes show a white gap at the bottom.
-   **Cause**: The slide content is 1280x720 but the iframe is a different size, and the browser's default scaling doesn't fill the frame correctly. The `min-height: 720px` inline style allows the container to grow beyond 720px.
-   **Solution**:
    1.  Override `min-height` with `height: 720px !important` on `.slide-container` in the wrapper CSS.
    2.  Use CSS transform scaling: set the iframe to 1280x720, then apply `transform: scale(containerWidth / 1280)` with `transform-origin: top left`.
    3.  Wrap the iframe in an `overflow: hidden` container sized to the scaled dimensions.

## 7. Monotonous Split-Panel Slides

-   **Problem**: All split-panel slides use the same brand color on the same side, making the deck feel repetitive.
-   **Cause**: Copy-pasting the same template without varying the layout.
-   **Solution**:
    -   Alternate which side has the color block (LEFT, RIGHT, LEFT, RIGHT).
    -   Use a different brand color for each slide. Rotate through: Cyan (#009CDE), Navy (#12285F), Yellow (#FFC423), Orange (#FF6D42), Purple (#CCBAF4).
    -   Use a 45%/55% split ratio (color panel 45%, text panel 55%).

## 8. Slides Cache Preventing Updates

-   **Problem**: After editing `slides-data.json`, the changes don't appear in the rendered slides.
-   **Cause**: The server caches the slides data on first load.
-   **Solution**: Temporarily disable the cache by commenting out `if (slidesCache) return slidesCache;` in the server code, restart the server, verify changes, then re-enable the cache.
