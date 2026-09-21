# Mathematics

DocSprout bundles the MIT-licensed [KaTeX](https://katex.org/) runtime, stylesheet
and fonts with every generated site. Math works offline, in GitHub Pages, and
in downloaded documentation archives—no CDN is used.

## Inline math

Use a single dollar delimiter:

```md
Euler's identity is $e^{i\pi} + 1 = 0$.
```

## Display math

Use a fenced `math` block for the clearest source:

```math
\left(\sum_{k=1}^{n} a_k b_k\right)^2
\leq
\left(\sum_{k=1}^{n} a_k^2\right)
\left(\sum_{k=1}^{n} b_k^2\right)
```

`$$` delimiters are also supported:

$$
\int_0^1 x^2\,dx = \frac{1}{3}
$$

The same common LaTeX syntax renders on GitHub, which uses MathJax. KaTeX and
MathJax do not have identical macro coverage; keep project notation within the
well-supported KaTeX subset for consistent repository and site rendering.

KaTeX source and licence are included at `src/docsprout/vendor/katex/`.
