# Layout Techniques

This document provides proven HTML/CSS patterns for common slide layouts.

## 1. Text with Image (Side-by-Side)

**Use Case**: A slide with text on one side and an image on the other.

```html
<div class="slide-container" style="display: grid; grid-template-columns: 1fr 1fr;">
  <div style="display: flex; flex-direction: column; justify-content: center; padding: 40px;">
    <!-- Text content here -->
  </div>
  <div style="display: flex; align-items: center; justify-content: center; padding: 40px;">
    <img src="/path/to/image.png" style="max-width: 100%; max-height: 500px; object-fit: contain;" />
  </div>
</div>
```

## 2. Image Inside a GUI Block Frame

**Use Case**: Placing a photograph or other visual inside a GUI block that acts as a frame.

**Technique**: Use a `position: relative` container for the GUI block `<img>`, and a `position: absolute` container for the photo `<img>` that sits on top of it.

```html
<div style="width: 90%; position: relative;">
  <img src="/path/to/gui-block-frame.png" style="width: 100%; height: auto; object-fit: contain; display: block;" />
  <div style="position: absolute; top: 8%; left: 4%; right: 4%; bottom: 8%; overflow: hidden;">
    <img src="/path/to/photo.jpg" style="width: 100%; height: 100%; object-fit: cover;" />
  </div>
</div>
```

-   The `top`, `left`, `right`, `bottom` percentages on the absolute container may need to be adjusted based on the thickness of the GUI block frame.
-   Use `object-fit: cover` for the photo to ensure it fills the frame without distortion.

## 3. Centered Text in a GUI Block

**Use Case**: A slide with a GUI block that contains centered text.

```html
<div class="slide-container" style="display: flex; align-items: center; justify-content: center;">
  <div style="width: 80%; position: relative;">
    <img src="/path/to/gui-block.png" style="width: 100%; height: auto; object-fit: contain;" />
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 40px;">
      <!-- Text content here -->
    </div>
  </div>
</div>
```

## 4. Logo Grid

**Use Case**: Displaying a grid of partner or client logos.

```html
<div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 32px; align-items: center; justify-items: center;">
  <div style="display: flex; align-items: center; justify-content: center; height: 80px; width: 100%;">
    <img src="/path/to/logo1.png" style="max-height: 60px; max-width: 140px; object-fit: contain;" />
  </div>
  <!-- Repeat for each logo -->
</div>
```
