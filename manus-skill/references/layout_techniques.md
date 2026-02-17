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

**Use Case**: A slide with a GUI block that contains centered text. This is the correct approach for placing text inside a GUI block frame without overflow.

```html
<div class="slide-container" style="display: flex; align-items: center; justify-content: center;">
  <div style="width: 100%; height: 680px; position: relative;">
    <img src="/path/to/gui-block.png" style="width: 100%; height: 100%; object-fit: fill;" />
    <div style="position: absolute; top: 10%; left: 8%; right: 8%; bottom: 12%; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 20px;">
      <!-- Text content here -->
    </div>
  </div>
</div>
```

**Critical**: The percentage-based insets (`top: 10%; left: 8%; right: 8%; bottom: 12%`) keep text within the visible rounded-rectangle area, away from the decorative corners and control dots. Adjust these values based on the specific GUI block frame being used.

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

## 5. Split-Panel Color Slide

**Use Case**: A slide with a solid brand color on one side and text content on the other. Alternate sides and colors across consecutive slides for visual variety.

### Color on LEFT, text on RIGHT:

```html
<div class="slide-container" style="display: grid; grid-template-columns: 45% 55%; min-height: 720px;">
  <div style="background-color: #009CDE; min-height: 720px; display: flex; align-items: center; justify-content: center; padding: 40px;">
    <h2 style="color: white; font-size: 36px; font-weight: bold; text-align: center;">Section Title</h2>
  </div>
  <div style="display: flex; flex-direction: column; justify-content: center; padding: 60px; background-color: #FFFFFF;">
    <!-- Text content here -->
  </div>
</div>
```

### Color on RIGHT, text on LEFT:

```html
<div class="slide-container" style="display: grid; grid-template-columns: 55% 45%; min-height: 720px;">
  <div style="display: flex; flex-direction: column; justify-content: center; padding: 60px; background-color: #FFFFFF;">
    <!-- Text content here -->
  </div>
  <div style="background-color: #12285F; min-height: 720px; display: flex; align-items: center; justify-content: center; padding: 40px;">
    <h2 style="color: white; font-size: 36px; font-weight: bold; text-align: center;">Section Title</h2>
  </div>
</div>
```

**Color rotation order**: Cyan (#009CDE) → Navy (#12285F) → Yellow (#FFC423) → Orange (#FF6D42) → Purple (#CCBAF4).

## 6. Full-Bleed Background with Text Overlay

**Use Case**: A slide with a full-bleed photo background and text overlay with semi-transparent scrim.

```html
<div class="slide-container" style="position: relative; min-height: 720px;">
  <img src="/path/to/photo.jpg" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;" />
  <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to right, rgba(18,40,95,0.85) 0%, rgba(18,40,95,0.4) 100%);">
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; padding: 60px; max-width: 60%;">
      <!-- White text content here -->
    </div>
  </div>
</div>
```
