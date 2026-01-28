-- Convert PPTX to PDF using Microsoft PowerPoint
-- Usage: osascript convert_to_pdf.scpt /path/to/presentation.pptx /path/to/output.pdf

on run argv
    set inputPath to POSIX file (item 1 of argv) as alias
    set outputFolder to "/Users/AlexUA/gitjawns/drupal-brand-skill/templates/presentations/"
    set outputName to "verification-output.pdf"

    tell application "Microsoft PowerPoint"
        activate
        open inputPath
        delay 3 -- Wait for file to load

        tell active presentation
            save in (outputFolder & outputName) as save as PDF
        end tell

        close active presentation saving no
    end tell

    return outputFolder & outputName
end run
