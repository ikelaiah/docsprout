"""Build-time accessible brand colours for generated sites.

One configured accent is enough. DocSprout proves link and focus colours
against every reading surface it ships, and substitutes a verification-passing
variant only when the exact configured colour would fail WCAG AA. The
documented ``--dk-*`` token family is unchanged: the verified values override
the internal defaults of ``--dk-interactive`` and ``--dk-focus-ring`` in every
theme and colour mode.
"""

from __future__ import annotations

import colorsys
from dataclasses import dataclass

AA_TEXT = 4.5
AA_UI = 3.0

RGB = tuple[int, int, int]

# Reading surfaces copied from the shipped stylesheet. A regression test keeps
# these tuples and SITE_CSS in sync, so a stylesheet change cannot silently
# invalidate the contrast proof.
CLASSIC_LIGHT = ("#ffffff", "#f8fafc", "#ffffff")
CLASSIC_DARK = ("#111827", "#1f2937", "#172033")
PAPER_LIGHT = ("#fdfbf7", "#f4eee3", "#fffefb")
PAPER_DARK = ("#1c1a17", "#29251f", "#24211c")
EINK_LIGHT = ("#ffffff", "#f2f2ee", "#ffffff")
EINK_DARK = ("#0d0d0d", "#181818", "#1e1e1e")
GLASS_LIGHT = ("#eaf1fa", "#f3f7fd", "#ffffff")
GLASS_DARK = ("#070b16", "#111b2e", "#1a2540")
# Glassmorphic reading surfaces include the worst-case composites the shipped
# CSS can produce: mesh stops tint the body by up to 11% (light) and 15% (dark)
# each and can stack on small viewports, and translucent panels composite a
# 78-82% surface with a 32-40% raised sheen over the darkest (light) or
# lightest (dark) backdrop those bounds allow. The tuples below hold that
# worst backdrop plus the surface, control and sheen composites over it.
GLASS_LIGHT_PROOF = GLASS_LIGHT + ("#cbd1d9", "#eaeff5", "#ecf0f6", "#f3f6fa")
GLASS_DARK_PROOF = GLASS_DARK + ("#343841", "#192132", "#172031", "#182237")


@dataclass(frozen=True)
class _Context:
    selector: str
    mode: str
    backgrounds: tuple[str, ...]
    system_dark: bool = False


_CONTEXTS = (
    _Context(":root", "light", CLASSIC_LIGHT),
    _Context('html[data-visual-theme="paper"]', "light", PAPER_LIGHT),
    _Context('html[data-visual-theme="e-ink"]', "light", EINK_LIGHT),
    _Context('html[data-visual-theme="glassmorphic"]', "light", GLASS_LIGHT_PROOF),
    _Context('html[data-visual-theme="classic"][data-theme="dark"]', "dark", CLASSIC_DARK),
    _Context('html[data-visual-theme="paper"][data-theme="dark"]', "dark", PAPER_DARK),
    _Context('html[data-visual-theme="e-ink"][data-theme="dark"]', "dark", EINK_DARK),
    _Context('html[data-visual-theme="glassmorphic"][data-theme="dark"]', "dark", GLASS_DARK_PROOF),
    _Context('html[data-visual-theme="classic"]:not([data-theme])', "dark", CLASSIC_DARK, system_dark=True),
    _Context('html[data-visual-theme="paper"]:not([data-theme])', "dark", PAPER_DARK, system_dark=True),
    _Context('html[data-visual-theme="e-ink"]:not([data-theme])', "dark", EINK_DARK, system_dark=True),
    _Context('html[data-visual-theme="glassmorphic"]:not([data-theme])', "dark", GLASS_DARK_PROOF, system_dark=True),
)


@dataclass(frozen=True)
class PaletteEntry:
    selector: str
    interactive: str
    focus: str
    on_interactive: str
    system_dark: bool = False


@dataclass(frozen=True)
class Palette:
    accent: str
    accent_secondary: str
    secondary_derived: bool
    entries: tuple[PaletteEntry, ...]
    light_adjusted: bool

    def stylesheet(self) -> str:
        """Return the deterministic per-theme override block for the site shell."""
        direct = [entry for entry in self.entries if not entry.system_dark]
        system = [entry for entry in self.entries if entry.system_dark]
        rules = ["".join((entry.selector, "{", _declarations(entry), "}")) for entry in direct]
        if system:
            media = "".join(f"html{entry.selector.removeprefix('html')}{{{_declarations(entry)}}}" for entry in system)
            rules.append(f"@media(prefers-color-scheme:dark){{{media}}}")
        return "".join(rules)

    @property
    def note(self) -> str | None:
        """Explain an adjusted light-mode link colour, or return None when exact."""
        if not self.light_adjusted:
            return None
        adjusted = next(entry.interactive for entry in self.entries if entry.selector == ":root")
        return (
            f"theme.accent {self.accent} fails WCAG AA contrast on light pages; "
            f"links use the verification-safe {adjusted}. Choose a darker accent to keep the exact colour."
        )


def _declarations(entry: PaletteEntry) -> str:
    return f"--dk-interactive:{entry.interactive};--dk-focus-ring:{entry.focus};--dk-on-interactive:{entry.on_interactive}"


def parse_hex(value: str) -> RGB:
    """Parse a validated ``#RRGGBB`` colour into an 8-bit channel tuple."""
    return (int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16))


def format_hex(rgb: RGB) -> str:
    """Format an 8-bit channel tuple as a lowercase ``#rrggbb`` colour."""
    red, green, blue = (max(0, min(255, round(channel))) for channel in rgb)
    return f"#{red:02x}{green:02x}{blue:02x}"


def relative_luminance(rgb: RGB) -> float:
    """Return WCAG relative luminance for an 8-bit sRGB colour."""

    def linear(channel: int) -> float:
        value = channel / 255
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (linear(channel) for channel in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(left: RGB, right: RGB) -> float:
    """Return the WCAG contrast ratio between two colours (1.0 to 21.0)."""
    high, low = sorted((relative_luminance(left), relative_luminance(right)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def _from_hls(hue: float, lightness: float, saturation: float) -> RGB:
    red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)
    return (round(red * 255), round(green * 255), round(blue * 255))


def _minimum_contrast(rgb: RGB, backgrounds: tuple[RGB, ...]) -> float:
    return min(contrast_ratio(rgb, background) for background in backgrounds)


def _verification_safe(rgb: RGB, backgrounds: tuple[RGB, ...], target: float, mode: str) -> RGB:
    """Return *rgb* when it passes *target*, otherwise the nearest passing variant.

    Light pages darken the candidate and dark pages lighten it, preserving hue
    and saturation so the result still reads as the configured brand colour.
    """
    if _minimum_contrast(rgb, backgrounds) >= target:
        return rgb
    hue, lightness, saturation = colorsys.rgb_to_hls(*(channel / 255 for channel in rgb))
    limit = 0.0 if mode == "light" else 1.0
    for step in range(1, 501):
        candidate_lightness = max(limit, lightness - step / 500) if mode == "light" else min(limit, lightness + step / 500)
        candidate = _from_hls(hue, candidate_lightness, saturation)
        if _minimum_contrast(candidate, backgrounds) >= target:
            return candidate
        if candidate_lightness == limit:
            break
    return (0, 0, 0) if mode == "light" else (255, 255, 255)


def _on_colour(rgb: RGB) -> str:
    """Return the black or white text colour with the higher contrast."""
    white, black = (255, 255, 255), (0, 0, 0)
    return "#ffffff" if contrast_ratio(white, rgb) >= contrast_ratio(black, rgb) else "#000000"


def derive_secondary(accent: RGB) -> RGB:
    """Derive an analogous secondary accent from one configured brand colour."""
    hue, lightness, saturation = colorsys.rgb_to_hls(*(channel / 255 for channel in accent))
    return _from_hls((hue + 28 / 360) % 1.0, lightness, saturation)


def derive_palette(accent: str, secondary: str | None) -> Palette:
    """Derive every contrast-proven theme value from the configured colours.

    ``secondary`` is derived from the accent only when the project configured an
    accent without a secondary; curated presets keep their documented pair.
    """
    accent_rgb = parse_hex(accent)
    secondary_derived = secondary is None
    secondary_rgb = derive_secondary(accent_rgb) if secondary_derived else parse_hex(secondary)
    entries: list[PaletteEntry] = []
    # A note is only useful when the configured accent genuinely fails on the
    # light reading surface; near-threshold surface tints adjust silently.
    light_adjusted = any(
        contrast_ratio(accent_rgb, parse_hex(context.backgrounds[0])) < AA_TEXT
        for context in _CONTEXTS
        if context.mode == "light"
    )
    for context in _CONTEXTS:
        backgrounds = tuple(parse_hex(value) for value in context.backgrounds)
        interactive = _verification_safe(accent_rgb, backgrounds, AA_TEXT, context.mode)
        focus = _verification_safe(accent_rgb, backgrounds, AA_UI, context.mode)
        entries.append(
            PaletteEntry(
                selector=context.selector,
                interactive=format_hex(interactive),
                focus=format_hex(focus),
                on_interactive=_on_colour(interactive),
                system_dark=context.system_dark,
            )
        )
    return Palette(
        accent=format_hex(accent_rgb),
        accent_secondary=format_hex(secondary_rgb),
        secondary_derived=secondary_derived,
        entries=tuple(entries),
        light_adjusted=light_adjusted,
    )
