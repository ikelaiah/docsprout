# Single-version Pages example

Choose this example when readers only need the latest documentation. The site
updates from `main` and does not use release tags or `docs/versions.json`.

## Try it locally

From the DocSprout repository root, run:

```bash
docsprout check --root examples/single-version
docsprout build --root examples/single-version --release latest --output build/single-version-example
python -m http.server 8000 --directory build/single-version-example
```

Open <http://localhost:8000>. Press `Ctrl+C` to stop the server.

## Use it in your project

1. Copy this example's `docs/` folder and
   `.github/workflows/documentation.yml` file.
2. Replace the project name and words.
3. Run `docsprout check` and `docsprout build`.
4. In GitHub, set **Settings → Pages → Source** to **GitHub Actions**.
5. Push `main` and confirm the Documentation workflow is green.

The workflow pins DocSprout and sets `versioned: false`. Update the pin only
when you deliberately upgrade DocSprout.
