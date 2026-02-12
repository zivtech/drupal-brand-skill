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
