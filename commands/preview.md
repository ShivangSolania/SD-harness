# Command: /preview
Triggers a localized artifact preview server to visualize generated HTML, UI components, or diagrams.

## Execution Sequence
1. Locate any visual assets or schemas rendered inside `sandbox/temporary/`.
2. Spin up a background service: `python3 -m http.server 8080 --directory sandbox/temporary/ &`
3. Output a direct link clickable in the terminal interface: `http://localhost:8080/preview.html`