/**
 * Google Apps Script to copy slide designs into master layouts
 *
 * This script attempts to copy the design elements from individual slides
 * into the slide master as reusable layouts.
 *
 * To use:
 * 1. Open your Google Slides presentation
 * 2. Go to Extensions > Apps Script
 * 3. Paste this code
 * 4. Run the createLayoutsFromSlides() function
 */

function createLayoutsFromSlides() {
  // Get the active presentation
  const presentation = SlidesApp.getActivePresentation();
  const slides = presentation.getSlides();
  const masters = presentation.getMasters();

  if (masters.length === 0) {
    Logger.log("No masters found in presentation");
    return;
  }

  const master = masters[0]; // Use the first master
  const existingLayouts = master.getLayouts();

  Logger.log("Found " + slides.length + " slides");
  Logger.log("Found " + existingLayouts.length + " existing layouts");

  // Process specific slides that have good designs
  // These are the slide indices (0-based) with designs we want to preserve
  const designSlideIndices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]; // First 10 slides

  for (let i = 0; i < Math.min(designSlideIndices.length, slides.length); i++) {
    const slideIndex = designSlideIndices[i];
    if (slideIndex >= slides.length) continue;

    const slide = slides[slideIndex];
    const layoutName = "Custom Layout " + (slideIndex + 1);

    Logger.log("Processing slide " + (slideIndex + 1) + " -> " + layoutName);

    // Get all page elements from the slide
    const elements = slide.getPageElements();
    Logger.log("  Found " + elements.length + " elements");

    // Log element types for analysis
    elements.forEach(function(element, index) {
      const type = element.getPageElementType();
      Logger.log("    Element " + index + ": " + type);

      if (type === SlidesApp.PageElementType.SHAPE) {
        const shape = element.asShape();
        if (shape.getText()) {
          Logger.log("      Text: " + shape.getText().asString().substring(0, 50) + "...");
        }
      }
    });
  }

  Logger.log("\n=== LIMITATION ===");
  Logger.log("Unfortunately, Google Apps Script cannot CREATE new layouts in the master.");
  Logger.log("The Layout class is read-only for layout creation.");
  Logger.log("You can only:");
  Logger.log("  - Get existing layouts: master.getLayouts()");
  Logger.log("  - Apply layouts to slides: slide.applyLayout(layout)");
  Logger.log("  - Get layout properties");
  Logger.log("\nYou CANNOT:");
  Logger.log("  - Create new layouts programmatically");
  Logger.log("  - Copy slide content into a layout");
  Logger.log("  - Modify layout structure");
  Logger.log("\nThe only way to create custom layouts is through the Google Slides UI:");
  Logger.log("  View > Master > Insert Layout");
}

/**
 * Alternative approach: Document the slide designs for manual recreation
 * This extracts all the design information so you can recreate layouts manually
 */
function documentSlideDesigns() {
  const presentation = SlidesApp.getActivePresentation();
  const slides = presentation.getSlides();

  let report = "# Slide Design Documentation\n\n";
  report += "Use this information to manually recreate layouts in the master.\n\n";

  for (let i = 0; i < Math.min(10, slides.length); i++) {
    const slide = slides[i];
    const elements = slide.getPageElements();
    const layout = slide.getLayout();

    report += "## Slide " + (i + 1) + "\n";
    report += "- Layout: " + layout.getLayoutName() + "\n";
    report += "- Elements: " + elements.length + "\n\n";

    elements.forEach(function(element, index) {
      const type = element.getPageElementType();
      const transform = element.getTransform();

      report += "### Element " + (index + 1) + ": " + type + "\n";
      report += "- Position: (" + Math.round(element.getLeft()) + ", " + Math.round(element.getTop()) + ")\n";
      report += "- Size: " + Math.round(element.getWidth()) + " x " + Math.round(element.getHeight()) + "\n";

      if (type === SlidesApp.PageElementType.SHAPE) {
        const shape = element.asShape();
        const text = shape.getText();
        if (text) {
          report += "- Text: \"" + text.asString().substring(0, 100).replace(/\n/g, "\\n") + "\"\n";
        }
        report += "- Shape Type: " + shape.getShapeType() + "\n";
      } else if (type === SlidesApp.PageElementType.IMAGE) {
        report += "- Image (design element)\n";
      }
      report += "\n";
    });

    report += "---\n\n";
  }

  Logger.log(report);
  return report;
}

/**
 * List all available layouts in the master
 */
function listAvailableLayouts() {
  const presentation = SlidesApp.getActivePresentation();
  const masters = presentation.getMasters();

  if (masters.length === 0) {
    Logger.log("No masters found");
    return;
  }

  const master = masters[0];
  const layouts = master.getLayouts();

  Logger.log("=== Available Layouts ===\n");

  layouts.forEach(function(layout, index) {
    const name = layout.getLayoutName();
    const placeholders = layout.getPlaceholders();

    Logger.log((index + 1) + ". " + name);
    Logger.log("   Placeholders: " + placeholders.length);

    placeholders.forEach(function(ph) {
      Logger.log("     - " + ph.getPlaceholderType());
    });
    Logger.log("");
  });
}
