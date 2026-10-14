# Pre-publish checklist

Use only the checklist for the mode you chose in [GitHub Pages](github-pages.md).
Run every command from the project folder.

Do not rush a release because the code is ready. A calm local check is much
easier to repair than a broken public tag.

## Before either kind of site

- [ ] Read the changed pages as someone new to the project.
- [ ] Run `docsprout doctor` and resolve every line beginning with `ERROR`,
      except the pending tag described below for a historical-release PR.
- [ ] Run `docsprout check` and confirm the reported page total makes sense.
- [ ] Run `docsprout audit --strict` and resolve every error and warning.
- [ ] Run `docsprout build --output build/docs-site` and open the local site.
- [ ] Check one phone-sized width, one desktop width, keyboard navigation, and
      Light and Dark mode.
- [ ] If you configure `theme.custom_css`, repeat the width, keyboard and
      mode checks with the stylesheet applied, and confirm its load order by
      looking at the page source (the `custom.css` link must come after
      `site.css`).
- [ ] Confirm **Settings → Pages → Source** is **GitHub Actions**.

During a historical-release PR, `doctor` reports the new `vX.Y.Z` tag as
missing because the tag must point to the merged commit. Do not tag the PR
branch to silence that expected message. Resolve other errors before the PR,
then rerun `doctor` after the merge and tag.

### Optional offline archive

To distribute the same local site as a download, add `--offline-archive` to a
normal build:

```bash
docsprout build --output build/docs-site --offline-archive dist/mylibrary-docs.zip
```

This writes a deterministic ZIP and the matching
`dist/mylibrary-docs.zip.sha256` checksum. Keep the site output and archive
under review together: both contain the generated documentation and local
assets from that build.

## Single-version site

This path updates the public site from a branch such as `main`.

1. Confirm there is no `docs/versions.json`.
2. Confirm the workflow contains `versioned: false`.
3. Build the exact site locally:

   ```bash
   docsprout build --release latest --output build/docs-site
   ```

4. Commit the documentation and workflow.
5. Run `git status --short`. No output means the project folder is clean.
6. Push the configured branch.
7. Open GitHub's **Actions** page and confirm the Documentation run is green.
8. Open the public URL and check one page and one search result.

## Historical site

This path publishes an immutable site for every listed release. This release
is `1.3.3`.

1. Add release `1.3.3` and source ref `v1.3.3` to `docs/versions.json`. Set
   `current` to `1.3.3`.
2. Run `docsprout check`.
3. Commit all release files, including package metadata, documentation,
   examples and workflows, on a branch named `dev/vX.Y.Z`:

   ```bash
   git add pyproject.toml src/docsprout README.md CHANGELOG.md CONTRIBUTING.md docs .github examples tests tasks
   git diff --cached --check
   git commit -m "Prepare v1.3.3 documentation"
   ```

4. Push the qualified branch and open a PR against `main`. Wait for every
   required CI/qualification check, inspect failures, and merge only the green
   candidate. Do not tag the unmerged PR head.

5. Check out the merged `main` commit and create the tag on that exact commit:

   ```bash
   git tag -a v1.3.3 -m "v1.3.3"
   ```

6. Run the release checks and historical build:

   ```bash
   docsprout check-release
   docsprout build-all --output build/docs-site
   ```

   The release check should report immutable releases. The build should contain
   one folder per release and a `versions.json` file at its root. `build-all`
   keeps the previous complete site if any release fails.

7. Run `git status --short`. No output means tracked release files are clean.
8. Push the annotated tag (the merge commit is already on `main`):

   ```bash
   git push origin v1.3.3
   ```

9. Create the GitHub Release from the tag. Put the release notes in the body
   without repeating the release title there. Confirm both CI and the
   Documentation workflow are green on GitHub.
10. Open the public site, switch between two releases, and confirm their content
   is different where expected.

## If you find a mistake

If the tag exists only on your computer, correct and commit the files, delete
the local tag with `git tag -d v1.3.3`, then create it again on the corrected
commit.

If the tag has been pushed, do not move or replace it. Publish the correction
as a new patch release, such as `v1.3.4`, so links and historical documentation
remain trustworthy.
