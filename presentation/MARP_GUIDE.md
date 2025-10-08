# Marp Presentation Guide

## Quick Start

The file `presentation_marp.md` is ready to use with Marp!

### 1. Install Marp CLI

```bash
npm install -g @marp-team/marp-cli
```

### 2. Generate Your Presentation

```bash
# Navigate to the presentation directory
cd presentation

# Generate PDF (recommended)
marp presentation_marp.md -o slides.pdf

# Generate PowerPoint
marp presentation_marp.md -o slides.pptx

# Generate HTML (for web viewing)
marp presentation_marp.md -o slides.html --html
```

### 3. Preview While Editing (Optional)

Install the Marp for VS Code extension:
1. Open VS Code
2. Install "Marp for VS Code" extension
3. Open `presentation_marp.md`
4. Click the preview button or use `Ctrl+K V` / `Cmd+K V`

## Marp Features Used

### YAML Front Matter
```yaml
---
marp: true
theme: default
paginate: true
footer: 'Can LLMs Replace Human Grant Reviewers? | SBU School of Health Professions'
---
```

### Custom Styling
- **SBU Colors**: Maroon (#990000) for headers
- **Font Sizes**: Optimized for readability
- **Image Sizing**: `![w:900 center](image.png)` for width control

### Special Directives

#### Lead Slide (Title/Section Breaks)
```markdown
<!-- _class: lead -->
# Big Title
```

#### Disable Pagination
```markdown
<!-- _paginate: false -->
```

### Image Sizing
```markdown
![w:800 center](./image.png)    # Width 800px, centered
![h:500](./image.png)            # Height 500px
![w:100%](./image.png)           # Full width
```

## Customization Options

### Change Theme Colors

Edit the style section in the front matter:

```yaml
style: |
  section {
    background-color: #ffffff;
  }
  h1 {
    color: #990000;  # Change to your institution's color
  }
```

### Adjust Font Sizes

```yaml
style: |
  section {
    font-size: 24px;  # Main text
  }
  h1 {
    font-size: 48px;  # Title size
  }
  table {
    font-size: 20px;  # Table text
  }
```

### Change Footer

```yaml
footer: 'Your Custom Footer | Institution Name'
```

## Slide Structure

### Main Presentation: 11 Slides
1. Title Slide (lead style, no pagination)
2. Background & Motivation
3. Study Design (2 slides with figure)
4. Prompt Engineering Experiments (2 slides with table)
5. Human vs. LLM Performance (2 slides)
6. Performance by Criteria (2 slides with table)
7. Prompt Engineering Impact (2 slides)
8. Model Performance (2 slides)
9. Inter-Rater Reliability (2 slides)
10. Conclusions (2 slides)
11. Future Directions & Thank You

### Supplementary Slides: 4 Slides
- S1: Detailed Methodology
- S2: Example Review Comparison
- S3: Limitations
- S4: Ethical Considerations

## Export Tips

### For Conference Presentations
```bash
# High-quality PDF
marp presentation_marp.md -o slides.pdf --pdf-outlines

# With embedded fonts
marp presentation_marp.md -o slides.pdf --allow-local-files
```

### For Sharing Online
```bash
# Self-contained HTML
marp presentation_marp.md -o slides.html --html

# With speaker notes (if added)
marp presentation_marp.md -o slides.html --html --bespoke.progress=true
```

### For Editing in PowerPoint
```bash
# Generate PPTX
marp presentation_marp.md -o slides.pptx

# Then open in PowerPoint for final tweaks
```

## Troubleshooting

### Images Not Showing
- Ensure images are in the same directory as the markdown file
- Use relative paths: `./slide2_problem_statement.png`
- Check file names match exactly (case-sensitive)

### Tables Look Strange
- Ensure proper markdown table syntax
- Use `font-size` in style section to adjust

### Slide Overflow
- Reduce font size in style section
- Split content across multiple slides using `---`
- Use smaller images with `![w:600](image.png)`

## Advanced Features

### Two-Column Layout
```markdown
<div class="columns">
<div>

Left column content

</div>
<div>

Right column content

</div>
</div>
```

Add to style:
```css
.columns {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}
```

### Speaker Notes (for HTML export)
```markdown
---
Your slide content here

<!-- _note: These are speaker notes that won't show on the slide -->
```

### Background Image
```markdown
<!-- _backgroundImage: "url('background.jpg')" -->
```

## Resources

- **Marp Official Docs**: https://marp.app/
- **Marp CLI GitHub**: https://github.com/marp-team/marp-cli
- **VS Code Extension**: https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode
- **Theme Gallery**: https://github.com/marp-team/marp-core/tree/main/themes

## Quick Commands Reference

```bash
# Preview in browser
marp presentation_marp.md --preview

# Watch mode (auto-regenerate on save)
marp presentation_marp.md -w -o slides.pdf

# Multiple outputs at once
marp presentation_marp.md -o slides.pdf && \
marp presentation_marp.md -o slides.pptx && \
marp presentation_marp.md -o slides.html --html
```

## Tips for Best Results

1. **Test early**: Generate a PDF early to check formatting
2. **Image quality**: Use high-res images (your figures are 300 DPI ✓)
3. **Consistent sizing**: Use same width for similar images
4. **Font readability**: Test on projector if possible
5. **Color contrast**: Ensure text is readable on background
6. **Backup format**: Always have a PDF backup for compatibility
