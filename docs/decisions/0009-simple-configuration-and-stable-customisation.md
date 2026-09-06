# Simple configuration and stable customisation

v0.18 makes the pre-1.0 contract candidates explicit. The product statement is
**minimal CLI + obvious declarative configuration**: commands perform
operations, and the committed JSON files describe the site.

The navigation editing model is a pure `layout.json` edit surface: page
objects, section titles, written order, the `home` object and the `unlisted`
policy. No page-management, section-management, rename, move or reorder
commands exist, and `init` never rewrites an authoritative `layout.json`.
Appearance and identity remain `dockit.json` fields.

Customisation is layered: presets and exact colours (beginner), the documented
intermediate configuration (identity, banner, homepage, content width), and
one deliberately bounded advanced escape hatch—`theme.custom_css`, a
repository-local stylesheet whose safe inclusion DocKit owns and whose
accessibility the author owns. The stylesheet loads after DocKit's styles on
every page including nested and versioned builds.

The generic first-class theme tokens (`--bg`, `--surface`, `--text`, and
friends) are renamed pre-1.0 to the namespaced `--dk-*` family so 1.x can
commit to a documented public token contract; internal implementation
variables are explicitly excluded from the contract.

Machine surfaces are hardened before 1.0: generated routes get pre-build
collision detection (exact and case-insensitive), `search-index.json` and
audit JSON become versioned schema-1 documents, unknown configuration fields
fail loudly with `Did you mean` suggestions built from the field families that
legitimately existed in released tags, and the Python API boundary is
documented (CLI plus `__version__`; everything else implementation detail).

These choices keep DocKit small, stdlib-only and offline while making the
1.0 commitment unambiguous.