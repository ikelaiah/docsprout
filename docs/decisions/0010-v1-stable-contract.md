# Decision 0010: v1.0 stable contract

v1.0.0 is DocKit's commitment point for a small, usable documentation
workflow. The release does not add a new feature family; it freezes the
contract that v0.18.1 qualified.

## The Five Promises

1. **Easy to use:** `init`, `serve`, `check`, `audit`, `build`, `doctor` and
   the Pages preparation flow are short, diagnosable actions.
2. **Easy to learn:** the README and beginner guide take a first-time user from
   existing Markdown to a local preview, then explain configuration and
   publication decisions in that order.
3. **Easy to look good:** the default output is responsive, keyboard-friendly,
   local-asset-only and coherent across Classic, Paper and Midnight with
   System, Light and Dark modes.
4. **Easy to create from existing repositories:** adoption preserves Markdown,
   supports generic and Pascal-shaped repositories, and keeps navigation and
   identity explicit.
5. **Easy to maintain:** schema-1 configuration, machine output, token names,
   routes and workflow inputs are documented, tested and release-pinned.

The qualification page records the evidence and separates automated checks,
manual checks and known limitations. The maintained visual fixture is the
review surface for responsive, accessibility and custom-CSS mechanics; it does
not turn screenshots or internal DOM details into a public contract.

## Compatibility decision

The stable boundary is the documented schema-version-1 configuration, the
documented CLI commands/options and exit behavior, generated routes, the
versioned machine-readable files, the public `--dk-*` token family, the safe
`theme.custom_css` inclusion mechanism, reusable-workflow inputs, and
`dockit_fp.__version__`. Private Python modules, internal selectors/DOM
wrappers, unlisted CSS variables, exact whitespace and human-readable prose
remain implementation details.

Within 1.x, compatible additions are preferred. A deprecation keeps the old
surface working for at least one minor release, is called out in the changelog
and migration guide, and is removed only in the next major release. A bug fix
may tighten validation when the prior behavior was unsafe or outside the
documented contract; it must include a regression test and migration guidance
when a user action is required. Schema or machine-format changes require a
new schema version and an explicit migration path.
