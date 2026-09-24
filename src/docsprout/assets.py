"""Shared DocSprout browser assets."""

SITE_CSS = r'''
:root{
  color-scheme:light dark;
  --dk-accent:#2563eb;
  --dk-accent-secondary:#0ea5e9;
  --dk-bg:#fff;
  --dk-surface:#f8fafc;
  --dk-text:#172033;
  --dk-muted:#526076;
  --dk-border:#d9e0ea;
  --dk-code-bg:#111827;
  --dk-code-text:#e5e7eb;
  --dk-raised:#fff;
  --dk-focus-ring:#087ea4;
  --dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000);
  --dk-on-interactive:#fff;
  --dk-content-width:46rem;
  --dk-reading-width:43rem;
  --dk-shell-width:90rem;
  --dk-radius:.35rem;
  --dk-font-ui:system-ui,-apple-system,"Segoe UI",Inter,"Aptos",sans-serif;
  --dk-font-display:var(--dk-font-ui);
  --dk-font-body:var(--dk-font-ui);
  --dk-font-mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Cascadia Code",monospace;
}
html[data-content-width="compact"]{--dk-content-width:40rem;--dk-reading-width:38rem;--dk-shell-width:84rem}
html[data-content-width="wide"]{--dk-content-width:54rem;--dk-reading-width:46rem;--dk-shell-width:98rem}
html[data-theme="light"]{color-scheme:light}
html[data-theme="dark"]{color-scheme:dark;--dk-bg:#111827;--dk-surface:#1f2937;--dk-text:#f3f4f6;--dk-muted:#b8c2d3;--dk-border:#3b4659;--dk-code-bg:#030712;--dk-raised:#172033;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="paper"]{--dk-bg:#fdfbf7;--dk-surface:#f4eee3;--dk-text:#312d26;--dk-muted:#6c6254;--dk-border:#d7cab7;--dk-code-bg:#2b2925;--dk-raised:#fffefb;--dk-focus-ring:#9a3412;--dk-font-display:Georgia,"Times New Roman",serif;--dk-font-body:Georgia,"Times New Roman",serif}
html[data-visual-theme="paper"][data-theme="dark"]{color-scheme:dark;--dk-bg:#1c1a17;--dk-surface:#29251f;--dk-text:#f7f0e5;--dk-muted:#c9bcaa;--dk-border:#554b3d;--dk-code-bg:#11100e;--dk-raised:#24211c;--dk-focus-ring:#fdba74;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="midnight"]{color-scheme:dark;--dk-bg:#0d1220;--dk-surface:#182033;--dk-text:#eef3ff;--dk-muted:#b4c0d8;--dk-border:#35415a;--dk-code-bg:#050912;--dk-raised:#121a2b;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="midnight"][data-theme="light"]{color-scheme:light;--dk-bg:#f5f8ff;--dk-surface:#e8eefb;--dk-text:#17223a;--dk-muted:#52617c;--dk-border:#c7d2e8;--dk-code-bg:#101827;--dk-raised:#fff;--dk-focus-ring:#075985;--dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000)}
html[data-visual-theme="e-ink"]{color-scheme:light;--dk-bg:#fff;--dk-surface:#f2f2ee;--dk-text:#121212;--dk-muted:#4a4a4a;--dk-border:#d8d8d2;--dk-code-bg:#1a1a1a;--dk-code-text:#f0f0ea;--dk-raised:#fff;--dk-focus-ring:#121212;--dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000);--dk-shadow:none;--dk-radius:.15rem}
html[data-visual-theme="e-ink"][data-theme="dark"]{color-scheme:dark;--dk-bg:#0d0d0d;--dk-surface:#181818;--dk-text:#dadada;--dk-muted:#9b9b9b;--dk-border:#303030;--dk-code-bg:#050505;--dk-code-text:#d6d6d6;--dk-raised:#1e1e1e;--dk-focus-ring:#f5f5f5;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="glassmorphic"]{color-scheme:light;--dk-bg:#e9f0f9;--dk-surface:#f6f9fd;--dk-text:#14202f;--dk-muted:#4c5a72;--dk-border:#cfdaeb;--dk-code-bg:#0f1b2d;--dk-raised:#fff;--dk-focus-ring:#075985;--dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000);--dk-radius:.7rem}
html[data-visual-theme="glassmorphic"][data-theme="dark"]{color-scheme:dark;--dk-bg:#0a0f1e;--dk-surface:#161c2c;--dk-text:#e7edff;--dk-muted:#9fb0cd;--dk-border:#29334a;--dk-code-bg:#060a14;--dk-raised:#111726;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
@media(prefers-color-scheme:dark){html[data-visual-theme="classic"]:not([data-theme]){color-scheme:dark;--dk-bg:#111827;--dk-surface:#1f2937;--dk-text:#f3f4f6;--dk-muted:#b8c2d3;--dk-border:#3b4659;--dk-code-bg:#030712}}
@media(prefers-color-scheme:dark){html[data-visual-theme="classic"]:not([data-theme]){--dk-raised:#172033;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}
@media(prefers-color-scheme:dark){html[data-visual-theme="paper"]:not([data-theme]){color-scheme:dark;--dk-bg:#1c1a17;--dk-surface:#29251f;--dk-text:#f7f0e5;--dk-muted:#c9bcaa;--dk-border:#554b3d;--dk-code-bg:#11100e;--dk-raised:#24211c;--dk-focus-ring:#fdba74;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}
@media(prefers-color-scheme:dark){html[data-visual-theme="e-ink"]:not([data-theme]){color-scheme:dark;--dk-bg:#0d0d0d;--dk-surface:#181818;--dk-text:#dadada;--dk-muted:#9b9b9b;--dk-border:#303030;--dk-code-bg:#050505;--dk-code-text:#d6d6d6;--dk-raised:#1e1e1e;--dk-focus-ring:#f5f5f5;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}
@media(prefers-color-scheme:dark){html[data-visual-theme="glassmorphic"]:not([data-theme]){color-scheme:dark;--dk-bg:#0a0f1e;--dk-surface:#161c2c;--dk-text:#e7edff;--dk-muted:#9fb0cd;--dk-border:#29334a;--dk-code-bg:#060a14;--dk-raised:#111726;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}
*{box-sizing:border-box}
.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
body{margin:0;background:var(--dk-bg);color:var(--dk-text);font-family:var(--dk-font-body);font-size:17px;line-height:1.72;font-synthesis:none;font-kerning:normal;font-optical-sizing:auto;font-variant-ligatures:common-ligatures contextual;text-rendering:optimizeLegibility}
::selection{background:color-mix(in srgb,var(--dk-accent) 24%,transparent)}
.reading-progress{position:fixed;inset:0 0 auto;z-index:3;height:3px;background:var(--dk-border);pointer-events:none}.reading-progress span{display:block;width:100%;height:100%;background:var(--dk-accent);transform:scaleX(0);transform-origin:left}
.site-header{border-bottom:1px solid var(--dk-border);background:var(--dk-bg);position:sticky;top:0;z-index:2}
.topbar{display:flex;gap:1rem;align-items:center;max-width:var(--dk-shell-width);margin:auto;padding:.7rem 1rem;font-family:var(--dk-font-ui)}
.brand{display:inline-flex;align-items:center;gap:.35rem;font-family:var(--dk-font-display);font-size:.95rem;font-weight:750;letter-spacing:-.025em;color:var(--dk-text);text-decoration:none;white-space:nowrap}
.brand>span{color:var(--dk-text)}.brand em{color:var(--dk-interactive);font-style:normal}
.brand-mark{width:1.05rem;height:1.05rem;fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:1.4;color:var(--dk-interactive)}
.search-control{position:relative;display:flex;align-items:center;min-width:8rem;max-width:25rem;flex:1}
.topbar .search-control input{width:100%;min-width:0;max-width:none;padding:.5rem 2rem .5rem .6rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);background:var(--dk-surface);color:var(--dk-text);font:inherit;font-size:.82rem}
.search-control kbd{position:absolute;right:.45rem;border:1px solid var(--dk-border);border-radius:.2rem;padding:0 .22rem;color:var(--dk-muted);font-family:var(--dk-font-mono);font-size:.7rem;line-height:1.3}
select,button{min-height:2.5rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);padding:.35rem .5rem;background:var(--dk-surface);color:var(--dk-text);font:inherit;font-size:.82rem}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--dk-focus-ring);outline-offset:3px}
.shell{max-width:var(--dk-shell-width);margin:auto;display:grid;grid-template-columns:15rem minmax(0,var(--dk-content-width)) 13rem;gap:2.5rem;padding:2rem 1rem 2.5rem}
.sidebar{font-size:.86rem;line-height:1.45}
.sidebar a{display:block;padding:.28rem .35rem;color:var(--dk-muted);text-decoration:none}
.sidebar a:hover{color:var(--dk-text);text-decoration:underline;text-decoration-color:var(--dk-accent-secondary);text-underline-offset:.2em}
.sidebar a.active{color:var(--dk-interactive);font-weight:700;border-left:3px solid var(--dk-accent)}
.sidebar h2{margin:1.1rem 0 .5rem;font-family:var(--dk-font-display);font-size:.72rem;font-weight:750;letter-spacing:.09em;text-transform:uppercase}
.sidebar h2:first-child{margin-top:.25rem}
.prose{min-width:0;max-width:var(--dk-content-width)}
.prose h1,.prose h2,.prose h3{font-family:var(--dk-font-display);font-weight:720;letter-spacing:-.032em;text-wrap:balance}
.prose h1{font-size:clamp(2.3rem,4vw,3rem);line-height:1.08;margin:0 0 1rem}
.prose h2{font-size:1.7rem;line-height:1.2;margin:2.75rem 0 .8rem}
.prose h3{font-size:1.25rem;line-height:1.3;margin:2.15rem 0 .6rem}
.prose h4,.prose h5,.prose h6{font-family:var(--dk-font-display);font-weight:700;letter-spacing:0;text-wrap:balance;scroll-margin-top:6.5rem}
.prose h4{font-size:1.05rem;line-height:1.4;margin:1.9rem 0 .5rem}
.prose h5{font-size:.95rem;line-height:1.4;margin:1.7rem 0 .45rem}
.prose h6{font-size:.85rem;line-height:1.45;margin:1.6rem 0 .4rem;color:var(--dk-muted);letter-spacing:.05em;text-transform:uppercase}
.prose p,.prose li,.prose dl{max-width:var(--dk-reading-width)}
.prose img{max-width:100%;height:auto}
.prose p{margin:.8rem 0}
.prose ul,.prose ol{padding-left:1.45rem}
.prose blockquote{max-width:var(--dk-reading-width);margin:1.25rem 0;padding:.1rem 1rem;border-left:3px solid var(--dk-border);color:var(--dk-muted)}
.prose hr{margin:2.5rem 0;border:0;border-top:1px solid var(--dk-border)}
html[data-visual-theme="paper"] .prose h1,html[data-visual-theme="paper"] .prose h2,html[data-visual-theme="paper"] .prose h3{letter-spacing:-.018em}
html[data-visual-theme="midnight"] .prose h1{color:color-mix(in srgb,var(--dk-text) 88%,var(--dk-accent-secondary))}
/* v1.2 — e-ink: an ink-on-paper manual. Flat surfaces, ruled headings, square
   corners, permanently underlined links and an undecorated hero. */
html[data-visual-theme="e-ink"] .prose pre,html[data-visual-theme="e-ink"] .capability-strip li,html[data-visual-theme="e-ink"] .search-results,html[data-visual-theme="e-ink"] .hero{box-shadow:none}
html[data-visual-theme="e-ink"] .prose pre,html[data-visual-theme="e-ink"] .capability-strip li,html[data-visual-theme="e-ink"] .search-results,html[data-visual-theme="e-ink"] .hero,html[data-visual-theme="e-ink"] .table-scroll{border-color:var(--dk-border);border-radius:.15rem}
html[data-visual-theme="e-ink"] .hero{border-color:var(--dk-text)}
html[data-visual-theme="e-ink"] .hero::before,html[data-visual-theme="e-ink"] .hero::after{display:none}
html[data-visual-theme="e-ink"] .prose h2{padding-bottom:.35rem;border-bottom:1px solid var(--dk-border)}
html[data-visual-theme="e-ink"] .prose a{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.18em}
html[data-visual-theme="e-ink"] .prose a:hover{text-decoration-thickness:2px}
html[data-visual-theme="e-ink"] .prose blockquote{border-left-color:var(--dk-text);font-style:italic}
html[data-visual-theme="e-ink"] .table-scroll{border-color:var(--dk-text)}
.task-list{display:inline-block;width:1.25em;color:var(--dk-interactive);font-weight:700}
.capability-strip{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.5rem;margin:1.25rem 0 1.5rem;padding:0;list-style:none}
.capability-strip li{max-width:none;padding:.7rem .8rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);background:var(--dk-raised);line-height:1.4}
.capability-strip strong{display:block;font-family:var(--dk-font-display);font-size:.78rem;font-weight:750;letter-spacing:.01em;color:var(--dk-text)}
.capability-strip span{display:block;margin-top:.15rem;color:var(--dk-muted);font-size:.75rem}
.release-context{display:flex;gap:.5rem;align-items:baseline;margin:1rem 0;padding:.55rem .75rem;border-left:3px solid var(--dk-accent);background:var(--dk-surface);font-size:.82rem}.release-context strong{font-family:var(--dk-font-display)}.release-context span{color:var(--dk-muted);font-family:var(--dk-font-mono)}
.prose a{color:var(--dk-interactive);font-weight:600;text-decoration-thickness:.08em;text-underline-offset:.16em}
.prose a:hover{text-decoration-thickness:.13em}
.prose pre{position:relative;overflow:auto;background:var(--dk-code-bg);color:var(--dk-code-text);padding:1.05rem 1.2rem;border:1px solid color-mix(in srgb,var(--dk-border) 55%,transparent);border-radius:var(--dk-radius);font-size:.9rem;line-height:1.65;tab-size:2}
.prose code{font-family:var(--dk-font-mono);font-size:.88em}
.prose :not(pre)>code{background:var(--dk-surface);border:1px solid var(--dk-border);padding:.08rem .28rem;border-radius:.2rem}
.syntax-highlight .tok-property{color:#93c5fd}.syntax-highlight .tok-keyword{color:#c4b5fd}.syntax-highlight .tok-function{color:#67e8f9}.syntax-highlight .tok-string{color:#86efac}.syntax-highlight .tok-number{color:#fcd34d}.syntax-highlight .tok-boolean{color:#f9a8d4}.syntax-highlight .tok-constant{color:#fda4af}.syntax-highlight .tok-comment{color:#94a3b8;font-style:italic}.syntax-highlight .tok-heading{color:#93c5fd;font-weight:700}.syntax-highlight .tok-code{color:#fcd34d}
.copy-code{position:absolute;top:.55rem;right:.55rem;min-height:0;padding:.2rem .45rem;border-color:#ffffff3d;background:#ffffff12;color:inherit;font-family:var(--dk-font-mono);font-size:.7rem;line-height:1.3;opacity:0;transition:opacity .15s ease}.prose pre:hover .copy-code,.copy-code:focus-visible{opacity:1}
.table-scroll{overflow:auto;margin:1.4rem 0;border:1px solid var(--dk-border);border-radius:var(--dk-radius)}
.prose table{border-collapse:collapse;min-width:32rem;width:100%;font-size:.92rem;line-height:1.5;font-variant-numeric:tabular-nums}
.prose th,.prose td{border:0;border-bottom:1px solid var(--dk-border);padding:.65rem .75rem;text-align:left;vertical-align:top}
.prose tr:last-child td{border-bottom:0}.prose tbody tr:nth-child(even){background:color-mix(in srgb,var(--dk-surface) 62%,transparent)}
.prose th{font-family:var(--dk-font-display);font-weight:700;background:var(--dk-surface)}
.admonition{--admonition-accent:var(--dk-accent);max-width:var(--dk-reading-width);margin:1.35rem 0;border:1px solid var(--dk-border);border-left:4px solid var(--admonition-accent);border-radius:0 var(--dk-radius) var(--dk-radius) 0;padding:.8rem 1rem;background:var(--dk-surface)}
.admonition.note{--admonition-accent:#0284c7}.admonition.important{--admonition-accent:#7c3aed}.admonition.tip{--admonition-accent:#0f766e}.admonition.warning{--admonition-accent:#b45309}
.admonition p:first-child{margin-top:0}.admonition p:last-child{margin-bottom:0}
.banner{max-width:100%;height:auto;max-height:14rem}
.search-results{position:absolute;top:3.8rem;left:max(1rem,calc((100% - var(--dk-shell-width))/2 + 16rem));width:min(34rem,calc(100% - 2rem));background:var(--dk-raised);border:1px solid var(--dk-border);border-radius:var(--dk-radius);box-shadow:0 .7rem 2rem #0003;padding:.35rem}
.search-results a{display:block;color:var(--dk-text);padding:.5rem .6rem;text-decoration:none}.search-results a:hover{background:var(--dk-surface)}.search-results small{display:block;color:var(--dk-muted);font-size:.76rem}.search-results mark{background:var(--dk-surface);color:inherit;border-radius:.1rem}.search-results mark{background:color-mix(in srgb,var(--dk-accent) 18%,transparent)}.search-empty{margin:.25rem;padding:.55rem .6rem;color:var(--dk-muted);font-size:.82rem}
.mobile-nav{display:none}.toc{position:sticky;top:5rem;align-self:start;font-size:.8rem;line-height:1.4;color:var(--dk-muted)}
.toc-title{margin:0 0 .5rem;font-family:var(--dk-font-display);font-size:.7rem;font-weight:750;letter-spacing:.08em;text-transform:uppercase;color:var(--dk-text)}
.toc a{display:block;padding:.24rem 0;color:var(--dk-muted);text-decoration:none}.toc a:hover,.toc a.is-active{color:var(--dk-interactive)}.toc a.is-active{font-weight:700}.toc .toc-level-3{padding-left:.75rem;font-size:.94em}.toc-empty-copy{margin:0;font-size:.9em}
.page-navigation{display:flex;gap:.75rem;margin:3.25rem 0 1rem;padding-top:1rem;border-top:1px solid var(--dk-border)}.page-navigation a{display:flex;flex-direction:column;max-width:48%;color:var(--dk-text);font-family:var(--dk-font-display);text-decoration:none}.page-navigation a small{font-family:var(--dk-font-mono);font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--dk-muted)}.page-navigation a span{font-size:1rem}.page-navigation a:hover span{color:var(--dk-interactive);text-decoration:underline;text-decoration-thickness:.08em;text-underline-offset:.16em}.page-navigation .page-next{margin-left:auto;text-align:right;align-items:flex-end}
.site-footer{display:flex;gap:1rem;flex-wrap:wrap;max-width:var(--dk-shell-width);margin:0 auto;padding:1rem;border-top:1px solid var(--dk-border);color:var(--dk-muted);font-family:var(--dk-font-ui);font-size:.82rem}.site-footer a{color:var(--dk-interactive);font-weight:650;text-decoration-thickness:.08em;text-underline-offset:.16em}
@media(max-width:1024px){.shell{grid-template-columns:13rem minmax(0,var(--dk-content-width));gap:2rem}.toc{display:none}}
@media(max-width:768px){body{font-size:16px}.topbar{flex-wrap:wrap}.search-control{order:3;flex-basis:100%;max-width:none}.shell{display:block;padding-top:1rem}.sidebar{display:none}.mobile-nav{display:block;padding:0 1rem 1rem}.mobile-nav summary{cursor:pointer}.toc{display:none}.prose h1{font-size:2.05rem}.copy-code{opacity:1}}
@media(max-width:600px){.topbar{gap:.5rem}.brand{flex:0 0 100%}.topbar select{flex:0 1 calc(50% - .25rem);width:calc(50% - .25rem);min-width:0}.capability-strip{grid-template-columns:1fr}}
@media(max-width:420px){.topbar{gap:.5rem}.brand{font-size:.9rem}.topbar select,button{font-size:.78rem}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}}
@media(forced-colors:active){button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline-color:Highlight}.reading-progress span{background:Highlight}}

/* v0.12 — a quiet visual layer for publication-ready defaults. */
:root{
  --dk-space-1:.25rem;
  --dk-space-2:.5rem;
  --dk-space-3:.75rem;
  --dk-space-4:1rem;
  --dk-space-5:1.5rem;
  --dk-space-6:2rem;
  --dk-space-7:3rem;
  --dk-shadow:0 .75rem 2rem color-mix(in srgb,#000 12%,transparent);
  --dk-focus-offset:.2rem;
  --dk-control-height:2.5rem;
}
body{line-height:1.7}
.site-header{box-shadow:0 1px 0 color-mix(in srgb,var(--dk-border) 55%,transparent)}
.topbar{display:grid;grid-template-columns:auto minmax(12rem,30rem) max-content;grid-template-rows:auto var(--dk-control-height);gap:var(--dk-space-2) var(--dk-space-3);align-items:stretch;padding:.65rem clamp(1rem,3vw,2rem)}
.brand{grid-row:1 / span 2;align-self:center;min-height:var(--dk-control-height)}
.brand-logo{display:block;width:2rem;height:2rem;flex:0 0 2rem;object-fit:contain}
.search-control{grid-column:2;grid-row:2;min-width:12rem;max-width:30rem;align-self:stretch}
.topbar .search-control input{height:var(--dk-control-height);min-height:var(--dk-control-height);padding:.55rem 2.25rem .55rem .75rem;background:var(--dk-surface)}
.search-control kbd{top:50%;transform:translateY(-50%)}
.header-controls{grid-column:3;grid-row:1 / span 2;display:grid;grid-template-columns:repeat(3,minmax(5.2rem,max-content));align-items:stretch;gap:var(--dk-space-2)}
.header-control{display:grid;grid-template-rows:auto var(--dk-control-height);gap:.2rem;min-width:5.2rem}
.header-control>span{padding-left:.1rem;color:var(--dk-muted);font-size:.65rem;font-weight:700;letter-spacing:.08em;line-height:1;text-transform:uppercase}
.header-control select{width:100%;height:var(--dk-control-height);min-height:var(--dk-control-height);padding:.35rem .55rem;background:var(--dk-surface)}
select:hover,.topbar .search-control input:hover{border-color:color-mix(in srgb,var(--dk-accent) 52%,var(--dk-border))}
.shell{grid-template-columns:minmax(12rem,15rem) minmax(0,var(--dk-content-width)) minmax(10rem,13rem);gap:clamp(1.75rem,3.5vw,3.5rem);padding:clamp(2rem,5vw,4rem) clamp(1rem,3vw,2rem) 3rem}
.sidebar{position:sticky;top:5.75rem;max-height:calc(100vh - 7rem);overflow:auto;padding-right:.35rem;scrollbar-color:var(--dk-border) transparent;scrollbar-width:thin}
.sidebar h2{margin:1.5rem 0 .45rem;padding-left:.7rem;color:var(--dk-muted);font-size:.67rem;letter-spacing:.12em}
.sidebar h2:first-child{margin-top:.15rem}
.sidebar a{padding:.42rem .7rem;border-left:2px solid transparent;border-radius:0 .25rem .25rem 0;overflow-wrap:anywhere}
.sidebar a:hover{background:var(--dk-surface);text-decoration:none}
.sidebar a.active{border-left-width:2px;background:color-mix(in srgb,var(--dk-accent) 9%,transparent);text-decoration:none}
.prose{padding-bottom:var(--dk-space-2)}
.prose h1,.prose h2,.prose h3{scroll-margin-top:6.5rem}
.prose h1{max-width:none;margin-bottom:1.25rem}
/* v1.4 — the splash hero: one designed opening on the home page. The
   accent-derived backdrop, derived call to action and card icons are all
   offline CSS/HTML; generated pages carry the shared semantic tokens only. */
.hero{position:relative;isolation:isolate;margin:0 0 2.75rem;padding:clamp(1.5rem,4.5vw,3rem);border:1px solid color-mix(in srgb,var(--dk-accent) 20%,var(--dk-border));border-radius:1rem;background:var(--dk-surface);overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(48rem 22rem at 12% -12%,color-mix(in srgb,var(--dk-accent) 20%,transparent),transparent 62%),radial-gradient(38rem 20rem at 96% 4%,color-mix(in srgb,var(--dk-accent-secondary) 18%,transparent),transparent 60%)}
.hero::after{content:"";position:absolute;inset:0;z-index:-1;background-image:radial-gradient(color-mix(in srgb,var(--dk-accent) 26%,transparent) 1px,transparent 1px);background-size:1.15rem 1.15rem;-webkit-mask-image:linear-gradient(155deg,#000 8%,transparent 58%);mask-image:linear-gradient(155deg,#000 8%,transparent 58%)}
.hero h1{font-size:clamp(2.4rem,5vw,3.4rem);letter-spacing:-.04em;margin-bottom:1rem;overflow-wrap:break-word}
.hero-copy{min-width:0}
.hero .hero-copy>p{max-width:42rem;color:var(--dk-muted);font-size:1.16rem;line-height:1.62}
.hero .release-context{display:inline-flex;align-self:flex-start;margin:0 0 1.15rem}
.hero-actions{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1.6rem}
.prose .hero-actions a{display:inline-flex;align-items:center;justify-content:center;min-height:2.65rem;padding:.55rem 1.2rem;border-radius:999px;font-family:var(--dk-font-display);font-size:.92rem;font-weight:700;text-decoration:none;transition:transform .16s ease,box-shadow .16s ease}
.prose .hero-actions a:hover{text-decoration:none}
.prose .hero-primary{border:1px solid color-mix(in srgb,var(--dk-interactive) 72%,#000);background:var(--dk-interactive);color:var(--dk-on-interactive,#fff)}
.prose .hero-primary:hover{box-shadow:0 .45rem 1.1rem color-mix(in srgb,var(--dk-accent) 34%,transparent)}
.prose .hero-secondary{border:1px solid var(--dk-border);background:var(--dk-raised);color:var(--dk-interactive)}
.prose .hero-secondary:hover{border-color:color-mix(in srgb,var(--dk-accent) 44%,var(--dk-border))}
.hero.hero-art{display:flex;flex-direction:column;padding:0}
.hero.hero-art h1{font-size:clamp(2.2rem,4vw,2.9rem);letter-spacing:-.035em}
.hero.hero-art .hero-copy{padding:clamp(1.5rem,4vw,2.9rem)}
.hero-figure{overflow:hidden;border-bottom:1px solid var(--dk-border)}
.hero-figure .banner{display:block;width:100%;height:auto;max-height:15rem;margin:0;border:0;border-radius:0;object-fit:cover;object-position:center}
.prose h2{margin-top:3.5rem;padding-top:.25rem}
.prose h3{margin-top:2.5rem}
.prose p{margin:1rem 0}
.prose ul,.prose ol{margin:1rem 0 1.35rem}
.prose li+li{margin-top:.35rem}
.prose li>ul,.prose li>ol{margin-top:.35rem;margin-bottom:.25rem}
.prose p,.prose li,.prose dd{text-wrap:pretty;orphans:3;widows:3}
.prose p,.prose li{overflow-wrap:break-word;hyphens:auto;-webkit-hyphens:auto;hyphenate-limit-chars:6 3 2}
.prose dl{margin:1.35rem 0}
.prose dt{margin-top:1rem;font-family:var(--dk-font-display);font-weight:750}
.prose dd{margin:.2rem 0 0 1.25rem;color:var(--dk-text)}
.prose pre+h2,.prose pre+h3,.prose .table-scroll+h2,.prose .table-scroll+h3,.prose .admonition+h2,.prose .admonition+h3{margin-top:3.75rem}
.prose blockquote{margin:1.5rem 0;padding:.2rem 1.25rem;border-left-width:3px}
.prose hr{margin:3rem 0}
.prose a{font-weight:650}
.prose :not(pre)>code{color:var(--dk-text);font-weight:650;line-height:1.4;hyphens:none;overflow-wrap:break-word}
.banner{display:block;width:100%;max-height:16rem;margin:0 0 1.75rem;border:1px solid var(--dk-border);border-radius:.5rem;object-fit:cover}
.capability-strip{grid-template-columns:repeat(4,minmax(0,1fr));align-items:stretch;grid-template-rows:minmax(0,1fr);gap:var(--dk-space-3);margin:0 0 2.75rem}
.capability-strip[data-card-count="2"]{grid-template-columns:repeat(2,minmax(0,1fr))}
.capability-strip[data-card-count="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}
.capability-strip[data-card-count="4"]{grid-template-columns:repeat(4,minmax(0,1fr))}
.capability-strip li{display:flex;flex-direction:column;align-self:stretch;min-height:0;padding:1.1rem 1.15rem;border:1px solid var(--dk-border);border-radius:.55rem;background:var(--dk-raised);box-shadow:0 1px 0 color-mix(in srgb,var(--dk-border) 70%,transparent);line-height:1.5;transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}
.card-icon{display:block;width:1.45rem;height:1.45rem;margin-bottom:.7rem;color:var(--dk-interactive)}
.capability-strip li+li{margin-top:0}
.capability-strip strong{font-size:.8rem;line-height:1.35}
.capability-strip span{margin-top:.35rem;font-size:.78rem;line-height:1.5}
.release-context{gap:.65rem;margin:1.5rem 0;padding:.75rem 1rem;border-left-width:3px;border-radius:0 .3rem .3rem 0}
.release-context strong{font-size:.76rem;letter-spacing:.08em;text-transform:uppercase}
.release-context span{font-size:.8rem}
.prose pre{margin:1.5rem 0;padding:2.85rem 1.25rem 1.25rem;border-radius:.5rem;box-shadow:var(--dk-shadow);scrollbar-color:#64748b var(--dk-code-bg);scrollbar-width:thin}
.prose pre code{display:block;min-width:max-content;font-size:.9rem;line-height:1.7;font-variant-ligatures:none}
.syntax-highlight .tok-keyword{font-weight:650}
.syntax-highlight .tok-function{font-weight:600}
.copy-code{top:.65rem;right:.65rem;min-height:2rem;padding:.3rem .55rem;border-radius:.25rem;opacity:.78;letter-spacing:.01em}
.prose pre:hover .copy-code,.copy-code:focus-visible{opacity:1}
.table-scroll{margin:1.5rem 0;border-radius:.5rem;-webkit-overflow-scrolling:touch;scrollbar-color:var(--dk-border) transparent;scrollbar-width:thin}
.prose table{font-size:.9rem}
.prose th,.prose td{padding:.75rem .9rem}
.prose tbody tr:hover{background:color-mix(in srgb,var(--dk-surface) 82%,transparent)}
.prose th{font-size:.88rem;letter-spacing:.01em}
.admonition{display:grid;grid-template-columns:auto minmax(0,1fr);gap:.15rem .75rem;margin:1.6rem 0;padding:1rem 1.1rem;border-left-width:4px;border-radius:0 .4rem .4rem 0}
.admonition>strong{grid-row:1;color:var(--admonition-accent);font-size:.76rem;letter-spacing:.07em;line-height:1.6;text-transform:uppercase}
.admonition>p{grid-column:2;margin:0;line-height:1.6}
.search-results{top:100%;left:max(1rem,calc((100% - var(--dk-shell-width))/2 + 16rem));max-height:min(60vh,30rem);overflow:auto;padding:.45rem;border-radius:.45rem;box-shadow:var(--dk-shadow)}
.search-results a{padding:.7rem .75rem;border-radius:.25rem}
.search-results a+a{margin-top:.15rem}
.search-results a:hover,.search-results a:focus-visible{background:var(--dk-surface);text-decoration:none}
.search-results a strong{display:block;font-family:var(--dk-font-display);font-size:.9rem;line-height:1.35}
.search-results small{margin-top:.2rem;line-height:1.45}
.search-results mark{padding:0 .1em;background:color-mix(in srgb,var(--dk-accent) 22%,transparent);color:var(--dk-text);font-weight:700}
.search-empty{padding:.7rem .75rem}
.toc{top:6rem;max-height:calc(100vh - 7rem);overflow:auto;padding-left:1rem;border-left:1px solid var(--dk-border);scrollbar-color:var(--dk-border) transparent;scrollbar-width:thin}
.toc-title{margin-bottom:.65rem;font-size:.68rem;letter-spacing:.1em}
.toc a{padding:.3rem .6rem;border-left:2px solid transparent;overflow-wrap:anywhere}
.toc a:hover{color:var(--dk-text);text-decoration:underline;text-underline-offset:.2em}
.toc a.is-active{margin-left:-1.1rem;border-left-color:var(--dk-accent);color:var(--dk-interactive);font-weight:700;text-decoration:none}
.toc .toc-level-3{padding-left:1.15rem}
.toc .toc-level-4{padding-left:1.5rem;font-size:.96em}
.toc .toc-level-5{padding-left:1.85rem;font-size:.92em}
.toc .toc-level-6{padding-left:2.2rem;font-size:.92em}
.page-navigation{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start;gap:var(--dk-space-3);margin:4rem 0 1rem;padding-top:1.25rem}
.page-navigation a{min-height:0;max-width:none;padding:0;border:0;border-radius:0;background:transparent}
.page-navigation a:hover{border-color:transparent;text-decoration:none}
.page-navigation a span{margin-top:.15rem;line-height:1.4}
.page-navigation .page-next{grid-column:2;margin-left:0;justify-self:end}
.site-footer{padding:1.25rem clamp(1rem,3vw,2rem)}
@media(hover:hover){.capability-strip li:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--dk-accent) 42%,var(--dk-border));box-shadow:var(--dk-shadow)}}
/* v1.2 — glassmorphic: a mesh-tinted page under frosted chrome with specular
   edges. Tints are capped at 12% accent and translucent text surfaces at
   78-86% opacity; the palette proof covers the worst-case composites those
   bounds can produce, and blur is progressive enhancement over solid tokens. */
html[data-visual-theme="glassmorphic"] body{background:radial-gradient(42rem 30rem at 8% -10%,color-mix(in srgb,var(--dk-accent) 12%,transparent),transparent 55%),radial-gradient(36rem 28rem at 92% 0%,color-mix(in srgb,var(--dk-accent-secondary) 12%,transparent),transparent 55%),radial-gradient(34rem 30rem at 50% 112%,color-mix(in srgb,var(--dk-accent) 9%,transparent),transparent 58%),var(--dk-bg)}
html[data-visual-theme="glassmorphic"] .site-header{background:color-mix(in srgb,var(--dk-surface) 78%,transparent);border-bottom-color:color-mix(in srgb,var(--dk-border) 55%,transparent);box-shadow:0 1px 0 color-mix(in srgb,var(--dk-raised) 65%,transparent),0 1.1rem 2.8rem color-mix(in srgb,var(--dk-bg) 55%,transparent)}
html[data-visual-theme="glassmorphic"] .hero{border-color:color-mix(in srgb,var(--dk-accent) 22%,transparent);border-radius:1.4rem;background:color-mix(in srgb,var(--dk-surface) 84%,transparent);box-shadow:0 1.4rem 3.4rem color-mix(in srgb,var(--dk-bg) 55%,transparent)}
html[data-visual-theme="glassmorphic"] .hero::before{background:radial-gradient(48rem 22rem at 12% -12%,color-mix(in srgb,var(--dk-accent) 30%,transparent),transparent 62%),radial-gradient(38rem 20rem at 96% 4%,color-mix(in srgb,var(--dk-accent-secondary) 26%,transparent),transparent 60%)}
html[data-visual-theme="glassmorphic"] .capability-strip li{background:color-mix(in srgb,var(--dk-raised) 86%,transparent);border-color:color-mix(in srgb,var(--dk-raised) 55%,var(--dk-border));border-radius:1.05rem;box-shadow:0 1.15rem 2.6rem color-mix(in srgb,var(--dk-bg) 45%,transparent)}
html[data-visual-theme="glassmorphic"] .release-context{background:color-mix(in srgb,var(--dk-surface) 88%,transparent);border-radius:.55rem}
html[data-visual-theme="glassmorphic"] .search-results{background:color-mix(in srgb,var(--dk-raised) 84%,transparent);border-color:color-mix(in srgb,var(--dk-raised) 50%,var(--dk-border));border-radius:.85rem;box-shadow:0 1.4rem 3.2rem color-mix(in srgb,var(--dk-bg) 50%,transparent)}
html[data-visual-theme="glassmorphic"] .topbar select,html[data-visual-theme="glassmorphic"] .topbar button,html[data-visual-theme="glassmorphic"] .topbar .search-control input{background:color-mix(in srgb,var(--dk-surface) 78%,transparent);border-color:color-mix(in srgb,var(--dk-raised) 45%,var(--dk-border));border-radius:.65rem}
@supports ((backdrop-filter:blur(2px)) or (-webkit-backdrop-filter:blur(2px))){
  html[data-visual-theme="glassmorphic"] .site-header{backdrop-filter:blur(22px) saturate(1.35);-webkit-backdrop-filter:blur(22px) saturate(1.35)}
  html[data-visual-theme="glassmorphic"] .hero,html[data-visual-theme="glassmorphic"] .capability-strip li,html[data-visual-theme="glassmorphic"] .search-results{backdrop-filter:blur(14px) saturate(1.2);-webkit-backdrop-filter:blur(14px) saturate(1.2)}
}
/* v1.2 — sidebar hierarchy: section labels are quiet small-cap headers that
   step back behind the page entries; page links carry the visual weight. */
.sidebar h2{margin:1.85rem 0 .55rem;padding-left:.7rem;font-size:.75rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--dk-muted)}
.sidebar h2:first-child{margin-top:.25rem}
.sidebar a{font-size:.88rem;font-weight:500;color:var(--dk-text)}
.sidebar a:hover{color:var(--dk-text)}
.sidebar a.active{color:var(--dk-interactive);font-weight:700}
.mobile-nav h2{font-size:.72rem;letter-spacing:.12em}
@media(max-width:768px){
  .topbar{display:flex;flex-wrap:wrap;align-items:center}
  .header-controls{order:2;display:flex;flex:1;min-width:0;align-items:flex-end}
  .search-control{order:3;flex-basis:100%;max-width:none}
  .shell{padding-top:1.5rem}
  .sidebar{display:none}
  .mobile-nav{display:block;margin:0;padding:0 1rem .75rem;border-bottom:1px solid var(--dk-border);background:var(--dk-surface)}
  .mobile-nav summary{min-height:2.75rem;padding:.65rem 0;cursor:pointer;font-family:var(--dk-font-display);font-size:.86rem;font-weight:700;list-style-position:inside}
  .mobile-nav h2{margin:1rem 0 .35rem;padding-left:.25rem;color:var(--dk-muted);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase}
  .mobile-nav a{display:block;padding:.55rem .25rem;color:var(--dk-muted);text-decoration:none}
  .mobile-nav a.active{color:var(--dk-interactive);font-weight:700}
  .toc{display:none}
  .prose h1{font-size:2.15rem}
  .capability-strip[data-card-count="4"],.capability-strip[data-card-count="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:600px){
  .topbar{gap:.5rem}
  .brand{flex:0 0 100%}
  .header-controls{width:100%;gap:.35rem}
  .header-control{flex:1;min-width:0}
  .header-control>span{font-size:.6rem}
  .topbar select{width:100%;min-width:0}
  .capability-strip,.capability-strip[data-card-count="2"],.capability-strip[data-card-count="3"],.capability-strip[data-card-count="4"]{grid-template-columns:1fr}
  .page-navigation{grid-template-columns:1fr;margin-top:3rem}
  .page-navigation .page-next{grid-column:1;justify-self:start}
  .page-navigation .page-next{text-align:left;align-items:flex-start}
}
@media(max-width:420px){
  .header-control select{font-size:.75rem}
  .prose pre{margin-inline:-.25rem;border-radius:.35rem;padding-inline:1rem}
}
@media print{
  .reading-progress,.site-header,.mobile-nav,.toc,.page-navigation,.hero-actions{display:none}
  .hero::before,.hero::after{display:none}
  .hero{border-color:#999;background:none}
  body{background:#fff;color:#000;font-size:12pt;line-height:1.5}
  .prose p,.prose li{hyphens:none}
  .shell{display:block;max-width:none;padding:0}
  .prose,.prose p,.prose li,.prose dl,.prose blockquote,.admonition{max-width:none}
  .prose a{color:inherit;text-decoration:underline}
  .prose pre,.table-scroll,.admonition,.banner{border-color:#999;box-shadow:none}
  .copy-code{display:none}
}
'''

SITE_JS = r'''
(()=>{
  const root=document.documentElement,key='docsprout-theme',legacyKey='dockit-fp-theme',select=document.querySelector('#theme-select');
  function readStored(primary,legacy){try{const value=localStorage.getItem(primary);if(value!==null)return value;const previous=localStorage.getItem(legacy);if(previous!==null){localStorage.setItem(primary,previous);localStorage.removeItem(legacy);return previous}}catch(_){}return null}
  function setTheme(value){if(value==='system')delete root.dataset.theme;else root.dataset.theme=value;try{localStorage.setItem(key,value)}catch(_){}}
  try{const value=readStored(key,legacyKey);if(['light','dark','system'].includes(value)){select.value=value;setTheme(value)}}catch(_){}
  select?.addEventListener('change',()=>setTheme(select.value));
  const visual=document.querySelector('#visual-theme'),visualKey='docsprout-visual-theme',legacyVisualKey='dockit-fp-visual-theme';
  function setVisualTheme(value){root.dataset.visualTheme=value;try{localStorage.setItem(visualKey,value)}catch(_){}}
  try{const value=readStored(visualKey,legacyVisualKey);if(['classic','paper','midnight','e-ink','glassmorphic'].includes(value)){visual.value=value;setVisualTheme(value)}else if(visual){visual.value=root.dataset.visualTheme||'classic'}}catch(_){ }
  visual?.addEventListener('change',()=>setVisualTheme(visual.value));
  const version=document.querySelector('#version-select');
  version?.addEventListener('change',()=>{location.href=version.value});

  const input=document.querySelector('#search'),results=document.querySelector('#search-results');
  let entries=[];
  function closeSearch(){if(!results)return;results.hidden=true;input?.setAttribute('aria-expanded','false')}
  function appendHighlight(element,text,query){
    const haystack=text.toLowerCase();let offset=0,index=haystack.indexOf(query,offset);
    while(index!==-1){element.append(text.slice(offset,index));const mark=document.createElement('mark');mark.textContent=text.slice(index,index+query.length);element.append(mark);offset=index+query.length;index=haystack.indexOf(query,offset)}
    element.append(text.slice(offset));
  }
  function excerpt(text,query){const index=text.toLowerCase().indexOf(query);if(index<0)return text.slice(0,90);const start=Math.max(0,index-36),end=Math.min(text.length,index+query.length+54);return `${start?'…':''}${text.slice(start,end)}${end<text.length?'…':''}`}
  function rank(entry,terms){
    const title=entry.title.toLowerCase(),section=entry.section.toLowerCase(),text=entry.text.toLowerCase();
    if(!terms.every(term=>(title+' '+section+' '+text).includes(term)))return Number.POSITIVE_INFINITY;
    return terms.reduce((score,term)=>score+(title===term?0:title.startsWith(term)?1:title.includes(term)?2:section.startsWith(term)?3:section.includes(term)?4:text.indexOf(term)/Math.max(text.length,1)+5),0);
  }
  function showSearch(){
    const query=input.value.trim().toLowerCase();
    if(!query){closeSearch();return}
    const terms=query.split(/\s+/),matches=entries.map(entry=>({entry,score:rank(entry,terms)})).filter(match=>Number.isFinite(match.score)).sort((left,right)=>left.score-right.score||left.entry.title.localeCompare(right.entry.title)).slice(0,8);
    if(!matches.length){const empty=document.createElement('p');empty.className='search-empty';empty.textContent=`No pages match “${input.value.trim()}”.`;results.replaceChildren(empty)}
    else results.replaceChildren(...matches.map(({entry})=>{
      const link=document.createElement('a');link.href=entry.url;
      const title=document.createElement('strong');appendHighlight(title,entry.title,terms[0]);
      const summary=document.createElement('small');summary.textContent=`${entry.section} — `;appendHighlight(summary,excerpt(entry.text,terms[0]),terms[0]);
      link.append(title,summary);return link;
    }));
    results.hidden=false;input.setAttribute('aria-expanded','true');
  }
  if(input&&results){
    fetch(input.dataset.searchIndex||'search-index.json').then(response=>response.ok?response.json():[]).then(value=>{entries=Array.isArray(value)?value:value?.entries||[];if(input.value.trim())showSearch()}).catch(()=>{});
    input.addEventListener('input',showSearch);
    input.addEventListener('keydown',event=>{
      const links=[...results.querySelectorAll('a')];const current=links.indexOf(document.activeElement);
      if(event.key==='ArrowDown'&&links.length){event.preventDefault();links[Math.min(current+1,links.length-1)].focus()}
      if(event.key==='ArrowUp'&&links.length){event.preventDefault();if(current>0)links[current-1].focus();else input.focus()}
      if(event.key==='End'&&links.length){event.preventDefault();links[links.length-1].focus()}
      if(event.key==='Enter'&&links.length){event.preventDefault();links[0].click()}
    });
    results.addEventListener('keydown',event=>{const links=[...results.querySelectorAll('a')],current=links.indexOf(document.activeElement);if(event.key==='ArrowDown'&&current>=0&&current+1<links.length){event.preventDefault();links[current+1].focus()}if(event.key==='ArrowUp'&&current>=0){event.preventDefault();if(current)links[current-1].focus();else input.focus()}if(event.key==='Home'&&links.length){event.preventDefault();links[0].focus()}if(event.key==='End'&&links.length){event.preventDefault();links[links.length-1].focus()}if(event.key==='Escape'){closeSearch();input.focus()}});
    document.addEventListener('pointerdown',event=>{if(!results.contains(event.target)&&event.target!==input)closeSearch()});
  }
  document.addEventListener('keydown',event=>{
    if(event.key==='/'&&document.activeElement!==input){event.preventDefault();input?.focus()}
    if(event.key==='Escape')closeSearch();
  });

  document.querySelectorAll('.prose pre').forEach(block=>{
    const code=block.querySelector('code');
    if(!code)return;
    const button=document.createElement('button');button.type='button';button.className='copy-code';
    const setCopyLabel=label=>{button.textContent=label;button.setAttribute('aria-label',label)};
    setCopyLabel('Copy code');
    button.addEventListener('click',async()=>{
      if(!navigator.clipboard?.writeText){setCopyLabel('Copy unavailable');return}
      try{await navigator.clipboard.writeText(code.textContent||'');setCopyLabel('Copied');window.setTimeout(()=>{setCopyLabel('Copy code')},1600)}catch(_){setCopyLabel('Copy unavailable')}
    });
    block.append(button);
  });

  const progress=document.querySelector('.reading-progress span');
  function updateProgress(){if(!progress)return;const range=document.documentElement.scrollHeight-window.innerHeight;const amount=range>0?Math.min(1,Math.max(0,window.scrollY/range)):0;progress.style.transform=`scaleX(${amount})`}
  if(progress){window.addEventListener('scroll',updateProgress,{passive:true});window.addEventListener('resize',updateProgress);updateProgress()}

  const tocLinks=[...document.querySelectorAll('.toc a[href^="#"]')];
  if(tocLinks.length&&'IntersectionObserver'in globalThis){
    const linksById=new Map(tocLinks.map(link=>[link.getAttribute('href').slice(1),link]));
    const activate=id=>tocLinks.forEach(link=>{const current=link===linksById.get(id);link.classList.toggle('is-active',current);if(current)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')});
    const observer=new IntersectionObserver(entries=>{const visible=entries.find(entry=>entry.isIntersecting);if(visible)activate(visible.target.id)},{rootMargin:'0px 0px -70% 0px'});
    linksById.forEach((_link,id)=>{const heading=document.getElementById(id);if(heading)observer.observe(heading)});
  }
})();
'''

MATH_JS = r'''
(()=>{function render(node,displayMode){if(!globalThis.katex){node.textContent=node.dataset.tex||'';return}try{globalThis.katex.render(node.dataset.tex||'',node,{displayMode,throwOnError:false,strict:'ignore'})}catch(_){node.textContent=node.dataset.tex||''}}document.querySelectorAll('.math-inline').forEach(node=>render(node,false));document.querySelectorAll('.math-display').forEach(node=>render(node,true))})();
'''
