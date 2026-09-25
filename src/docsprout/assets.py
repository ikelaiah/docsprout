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
  --dk-radius:.5rem;
  --dk-space-1:.25rem;
  --dk-space-2:.5rem;
  --dk-space-3:.75rem;
  --dk-space-4:1rem;
  --dk-space-5:1.5rem;
  --dk-space-6:2rem;
  --dk-space-7:3rem;
  --dk-shadow:0 .75rem 2rem color-mix(in srgb,#1e293b 12%,transparent);
  --dk-focus-offset:.2rem;
  --dk-control-height:2.5rem;
  --dk-font-ui:system-ui,-apple-system,"Segoe UI",Inter,"Aptos",sans-serif;
  --dk-font-display:var(--dk-font-ui);
  --dk-font-body:var(--dk-font-ui);
  --dk-font-mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Cascadia Code",monospace;
}
html[data-content-width="compact"]{--dk-content-width:40rem;--dk-reading-width:38rem;--dk-shell-width:84rem}
html[data-content-width="wide"]{--dk-content-width:54rem;--dk-reading-width:46rem;--dk-shell-width:98rem}
html[data-theme="light"]{color-scheme:light}
html[data-theme="dark"]{color-scheme:dark;--dk-bg:#111827;--dk-surface:#1f2937;--dk-text:#f3f4f6;--dk-muted:#b8c2d3;--dk-border:#3b4659;--dk-code-bg:#030712;--dk-raised:#172033;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff);--dk-shadow:0 .75rem 2rem color-mix(in srgb,#000 55%,transparent),0 1px 0 color-mix(in srgb,#fff 6%,transparent)}
html[data-visual-theme="paper"]{--dk-bg:#fdfbf7;--dk-surface:#f4eee3;--dk-text:#312d26;--dk-muted:#6c6254;--dk-border:#d7cab7;--dk-code-bg:#2b2925;--dk-raised:#fffefb;--dk-focus-ring:#9a3412;--dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000);--dk-shadow:0 .75rem 2rem color-mix(in srgb,#4a3b2a 14%,transparent);--dk-radius:.15rem;--dk-font-display:Georgia,"Times New Roman",serif;--dk-font-body:Georgia,"Times New Roman",serif}
html[data-visual-theme="paper"][data-theme="dark"]{color-scheme:dark;--dk-bg:#1c1a17;--dk-surface:#29251f;--dk-text:#f7f0e5;--dk-muted:#c9bcaa;--dk-border:#554b3d;--dk-code-bg:#11100e;--dk-raised:#24211c;--dk-focus-ring:#fdba74;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff);--dk-shadow:0 .75rem 2rem color-mix(in srgb,#000 55%,transparent),0 1px 0 color-mix(in srgb,#f7f0e5 7%,transparent)}
html[data-visual-theme="e-ink"]{color-scheme:light;--dk-bg:#fff;--dk-surface:#f2f2ee;--dk-text:#121212;--dk-muted:#4a4a4a;--dk-border:#d8d8d2;--dk-code-bg:#1a1a1a;--dk-code-text:#f0f0ea;--dk-raised:#fff;--dk-focus-ring:#121212;--dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000);--dk-shadow:none;--dk-radius:0}
html[data-visual-theme="e-ink"][data-theme="dark"]{color-scheme:dark;--dk-bg:#0d0d0d;--dk-surface:#181818;--dk-text:#dadada;--dk-muted:#9b9b9b;--dk-border:#303030;--dk-code-bg:#050505;--dk-code-text:#d6d6d6;--dk-raised:#1e1e1e;--dk-focus-ring:#f5f5f5;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}
html[data-visual-theme="glassmorphic"]{color-scheme:light;--dk-bg:#eaf1fa;--dk-surface:#f3f7fd;--dk-text:#14202f;--dk-muted:#47566e;--dk-border:#c2d1e6;--dk-code-bg:#0f1b2d;--dk-raised:#fff;--dk-focus-ring:#075985;--dk-interactive:color-mix(in srgb,var(--dk-accent) 78%,#000);--dk-radius:1rem;--dk-mesh-1:11%;--dk-mesh-2:10%;--dk-mesh-3:8%;--dk-mesh-4:7%;--dk-glass:linear-gradient(180deg,color-mix(in srgb,var(--dk-raised) 40%,transparent),transparent 45%),color-mix(in srgb,var(--dk-surface) 82%,transparent)}
html[data-visual-theme="glassmorphic"][data-theme="dark"]{color-scheme:dark;--dk-bg:#070b16;--dk-surface:#111b2e;--dk-text:#e9eeff;--dk-muted:#98abd0;--dk-border:#2b3a58;--dk-code-bg:#050810;--dk-raised:#1a2540;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff);--dk-mesh-1:15%;--dk-mesh-2:14%;--dk-mesh-3:11%;--dk-mesh-4:9%}
@media(prefers-color-scheme:dark){html[data-visual-theme="classic"]:not([data-theme]){color-scheme:dark;--dk-bg:#111827;--dk-surface:#1f2937;--dk-text:#f3f4f6;--dk-muted:#b8c2d3;--dk-border:#3b4659;--dk-code-bg:#030712;--dk-raised:#172033;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff);--dk-shadow:0 .75rem 2rem color-mix(in srgb,#000 55%,transparent),0 1px 0 color-mix(in srgb,#fff 6%,transparent)}}
@media(prefers-color-scheme:dark){html[data-visual-theme="paper"]:not([data-theme]){color-scheme:dark;--dk-bg:#1c1a17;--dk-surface:#29251f;--dk-text:#f7f0e5;--dk-muted:#c9bcaa;--dk-border:#554b3d;--dk-code-bg:#11100e;--dk-raised:#24211c;--dk-focus-ring:#fdba74;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff);--dk-shadow:0 .75rem 2rem color-mix(in srgb,#000 55%,transparent),0 1px 0 color-mix(in srgb,#f7f0e5 7%,transparent)}}
@media(prefers-color-scheme:dark){html[data-visual-theme="e-ink"]:not([data-theme]){color-scheme:dark;--dk-bg:#0d0d0d;--dk-surface:#181818;--dk-text:#dadada;--dk-muted:#9b9b9b;--dk-border:#303030;--dk-code-bg:#050505;--dk-code-text:#d6d6d6;--dk-raised:#1e1e1e;--dk-focus-ring:#f5f5f5;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff)}}
@media(prefers-color-scheme:dark){html[data-visual-theme="glassmorphic"]:not([data-theme]){color-scheme:dark;--dk-bg:#070b16;--dk-surface:#111b2e;--dk-text:#e9eeff;--dk-muted:#98abd0;--dk-border:#2b3a58;--dk-code-bg:#050810;--dk-raised:#1a2540;--dk-focus-ring:#67e8f9;--dk-interactive:color-mix(in srgb,var(--dk-accent) 45%,#fff);--dk-shadow:0 .75rem 2rem color-mix(in srgb,#000 55%,transparent),0 1px 0 color-mix(in srgb,#fff 6%,transparent);--dk-mesh-1:15%;--dk-mesh-2:14%;--dk-mesh-3:11%;--dk-mesh-4:9%}}
*{box-sizing:border-box}
.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
body{margin:0;background:var(--dk-bg);color:var(--dk-text);font-family:var(--dk-font-body);font-size:17px;line-height:1.7;font-synthesis:none;font-kerning:normal;font-optical-sizing:auto;font-variant-ligatures:common-ligatures contextual;text-rendering:optimizeLegibility}
::selection{background:color-mix(in srgb,var(--dk-accent) 24%,transparent)}
.reading-progress{position:fixed;inset:0 0 auto;z-index:3;height:3px;background:var(--dk-border);pointer-events:none}.reading-progress span{display:block;width:100%;height:100%;background:var(--dk-accent);transform:scaleX(0);transform-origin:left}
.site-header{position:sticky;top:0;z-index:2;border-bottom:1px solid var(--dk-border);background:var(--dk-bg)}
:is(.site-header,.sidebar,.toc,.mobile-nav,.capability-strip,.hero-actions,.release-context){font-family:var(--dk-font-ui)}
.brand>span{color:var(--dk-text)}.brand em{color:var(--dk-interactive);font-style:normal}
.brand-mark{display:block;width:1.35rem;height:1.35rem;flex:0 0 1.35rem}
.search-control{position:relative;display:flex;align-items:center;flex:1;grid-column:2;grid-row:2;min-width:12rem;max-width:30rem;align-self:stretch}
.topbar .search-control input{width:100%;min-width:0;max-width:none;height:var(--dk-control-height);min-height:var(--dk-control-height);padding:.55rem 2.25rem .55rem .75rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);background:var(--dk-surface);color:var(--dk-text);font:inherit;font-size:.82rem}
.search-control kbd{position:absolute;top:50%;transform:translateY(-50%);right:.45rem;border:1px solid var(--dk-border);border-radius:.2rem;padding:0 .22rem;color:var(--dk-muted);font-family:var(--dk-font-mono);font-size:.7rem;line-height:1.3}
select,button{min-height:2.5rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);padding:.35rem .5rem;background:var(--dk-surface);color:var(--dk-text);font:inherit;font-size:.82rem}
button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--dk-focus-ring);outline-offset:3px}
.shell{max-width:var(--dk-shell-width);margin:auto;display:grid;grid-template-columns:minmax(12rem,15rem) minmax(0,var(--dk-content-width)) minmax(10rem,13rem);gap:clamp(1.75rem,3.5vw,3.5rem);padding:clamp(2rem,5vw,4rem) clamp(1rem,3vw,2rem) 3rem}
.sidebar{position:sticky;top:6rem;align-self:start;max-height:calc(100vh - 7rem);overflow:auto;padding-right:.35rem;font-size:.86rem;line-height:1.45;scrollbar-color:var(--dk-border) transparent;scrollbar-width:thin}
.sidebar a{display:block;padding:.42rem .7rem;border-left:2px solid transparent;border-radius:0 .25rem .25rem 0;color:var(--dk-text);font-size:.88rem;font-weight:500;text-decoration:none;overflow-wrap:anywhere}
.sidebar a:hover{background:var(--dk-surface);color:var(--dk-text);text-decoration:none}
.sidebar a.active{border-left:2px solid var(--dk-accent);background:color-mix(in srgb,var(--dk-accent) 9%,transparent);color:var(--dk-interactive);font-weight:700;text-decoration:none}
.sidebar h2{margin:1.85rem 0 .55rem;padding-left:.7rem;color:var(--dk-muted);font-size:.68rem;font-weight:650;letter-spacing:.12em;text-transform:uppercase}
.sidebar h2:first-child{margin-top:.25rem}
.prose{min-width:0;max-width:var(--dk-content-width);padding-bottom:var(--dk-space-2)}
.prose h1,.prose h2,.prose h3{font-family:var(--dk-font-display);font-weight:720;letter-spacing:-.032em;text-wrap:balance;scroll-margin-top:6.5rem}
.prose h1{font-size:clamp(2.3rem,4vw,3rem);line-height:1.12;max-width:none;margin:0 0 1.25rem}
.prose h2{margin:3.5rem 0 .8rem;padding-top:.25rem;font-size:1.7rem;line-height:1.2}
.prose h3{margin:2.5rem 0 .6rem;font-size:1.25rem;line-height:1.3}
.prose h4,.prose h5,.prose h6{font-family:var(--dk-font-display);font-weight:700;letter-spacing:0;text-wrap:balance;scroll-margin-top:6.5rem}
.prose h4{font-size:1.05rem;line-height:1.4;margin:1.9rem 0 .5rem}
.prose h5{font-size:.95rem;line-height:1.4;margin:1.7rem 0 .45rem}
.prose h6{font-size:.85rem;line-height:1.45;margin:1.6rem 0 .4rem;color:var(--dk-muted);letter-spacing:.05em;text-transform:uppercase}
.prose p,.prose li,.prose dl{max-width:var(--dk-reading-width)}
.prose img{max-width:100%;height:auto}
.prose ul,.prose ol{margin:1rem 0 1.35rem;padding-left:1.45rem}
.prose blockquote{max-width:var(--dk-reading-width);margin:1.5rem 0;padding:.2rem 1.25rem;border-left:3px solid var(--dk-border);color:var(--dk-muted)}
.prose hr{margin:3rem 0;border:0;border-top:1px solid var(--dk-border)}
html[data-visual-theme="paper"] .prose{padding:clamp(1rem,3vw,2.5rem);border:1px solid var(--dk-border);background:var(--dk-raised);box-shadow:0 4px 0 -1px var(--dk-bg),0 4px 0 var(--dk-border),0 14px 32px -24px var(--dk-text)}
html[data-visual-theme="paper"] .prose :is(h1,h2,h3){font-weight:500;letter-spacing:-.035em}
html[data-visual-theme="paper"] .prose blockquote{border-left-color:color-mix(in srgb,var(--dk-accent) 38%,var(--dk-border));background:color-mix(in srgb,var(--dk-surface) 62%,transparent)}
html[data-visual-theme="paper"] .prose hr{border-top-style:dashed;border-top-color:color-mix(in srgb,var(--dk-muted) 45%,transparent)}
/* E-ink keeps structural rules and removes decorative depth and motion. */
html[data-visual-theme="e-ink"]{--dk-font-ui:var(--dk-font-mono);--dk-font-body:system-ui,sans-serif;--dk-font-display:var(--dk-font-body)}
html[data-visual-theme="e-ink"] :is(.prose pre,.capability-strip li,.search-results,.hero){box-shadow:none;border-color:var(--dk-border)}
html[data-visual-theme="e-ink"] .hero{border-color:var(--dk-text)}
html:not([data-visual-theme="glassmorphic"]) .hero::before,html:not([data-visual-theme="glassmorphic"]) .hero::after{display:none}
html[data-visual-theme="e-ink"] .prose :is(.hero-actions a,.capability-strip li){box-shadow:none;transition:none}
html[data-visual-theme="e-ink"] .prose h2{padding-bottom:.35rem;border-bottom:1px solid var(--dk-border)}
html[data-visual-theme="e-ink"] .prose a:not(:where(.hero-actions a,.page-navigation a)){text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.18em}
html[data-visual-theme="e-ink"] .prose a:not(:where(.hero-actions a,.page-navigation a)):hover{text-decoration-thickness:2px}
html[data-visual-theme="e-ink"] .prose blockquote{border-left-color:var(--dk-text);font-style:italic}
html[data-visual-theme="e-ink"] .table-scroll{border-color:var(--dk-text)}
html[data-visual-theme="e-ink"] .prose th{border-bottom:2px solid var(--dk-text)}
html[data-visual-theme="e-ink"] .reading-progress span{background:var(--dk-text)}
html[data-visual-theme="e-ink"] .release-context{border-left-color:var(--dk-text)}
html[data-visual-theme="e-ink"] .sidebar a.active{border-left-color:var(--dk-interactive)}
html[data-visual-theme="e-ink"] ::selection,html[data-visual-theme="e-ink"]::selection{background:color-mix(in srgb,var(--dk-text) 18%,transparent)}
.task-list{display:inline-block;width:1.25em;color:var(--dk-interactive);font-weight:700}
.prose .capability-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));align-items:stretch;grid-template-rows:minmax(0,1fr);gap:var(--dk-space-3);margin:0 0 2.75rem;padding:0;list-style:none}
.capability-strip li{display:flex;flex-direction:column;align-self:stretch;min-height:0;padding:1.1rem 1.15rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);max-width:none;background:var(--dk-raised);line-height:1.5;transition:border-color .18s ease,box-shadow .18s ease}
.capability-strip strong{display:block;font-family:var(--dk-font-display);font-size:.8rem;font-weight:750;letter-spacing:.01em;line-height:1.35;color:var(--dk-text)}
.capability-strip span{display:block;margin-top:.5rem;color:var(--dk-muted);font-size:.8rem;line-height:1.6}
.release-context{display:flex;gap:.65rem;align-items:baseline;margin:1.5rem 0;padding:.75rem 1rem;border-left:3px solid var(--dk-accent);border-radius:0 .3rem .3rem 0;background:var(--dk-surface);font-size:.82rem}.release-context strong{font-family:var(--dk-font-display);font-size:.76rem;letter-spacing:.08em;text-transform:uppercase}.release-context span{color:var(--dk-muted);font-family:var(--dk-font-mono);font-size:.8rem}
.prose a{color:var(--dk-interactive);font-weight:650;text-decoration-thickness:.08em;text-underline-offset:.16em}
.prose a:hover{text-decoration-thickness:.13em}
.prose pre{position:relative;overflow:auto;margin:1.5rem 0;padding:2.85rem 1.25rem 1.25rem;border:1px solid color-mix(in srgb,var(--dk-border) 55%,transparent);border-radius:var(--dk-radius);background:var(--dk-code-bg);color:var(--dk-code-text);font-size:.9rem;line-height:1.65;tab-size:2;box-shadow:var(--dk-shadow);scrollbar-color:#64748b var(--dk-code-bg);scrollbar-width:thin}
.prose code{font-family:var(--dk-font-mono);font-size:.88em}
.prose :not(pre)>code{background:var(--dk-surface);border:1px solid var(--dk-border);padding:.08rem .28rem;border-radius:.2rem;color:var(--dk-text);font-weight:650;line-height:1.4;hyphens:none;overflow-wrap:break-word}
.syntax-highlight .tok-property{color:#93c5fd}.syntax-highlight .tok-keyword{color:#c4b5fd}.syntax-highlight .tok-function{color:#67e8f9}.syntax-highlight .tok-string{color:#86efac}.syntax-highlight .tok-number{color:#fcd34d}.syntax-highlight .tok-boolean{color:#f9a8d4}.syntax-highlight .tok-constant{color:#fda4af}.syntax-highlight .tok-comment{color:#94a3b8;font-style:italic}.syntax-highlight .tok-heading{color:#93c5fd;font-weight:700}.syntax-highlight .tok-code{color:#fcd34d}
.copy-code{position:absolute;top:.65rem;right:.65rem;min-height:2rem;padding:.3rem .55rem;border-color:#ffffff3d;border-radius:.25rem;background:#ffffff12;color:inherit;font-family:var(--dk-font-mono);font-size:.7rem;line-height:1.3;letter-spacing:.01em;opacity:.78;transition:opacity .15s ease}.prose pre:hover .copy-code,.copy-code:focus-visible{opacity:1}
.table-scroll{overflow:auto;margin:1.5rem 0;border:1px solid var(--dk-border);border-radius:var(--dk-radius);-webkit-overflow-scrolling:touch;scrollbar-color:var(--dk-border) transparent;scrollbar-width:thin}
.prose table{border-collapse:collapse;min-width:32rem;width:100%;font-size:.9rem;line-height:1.5;font-variant-numeric:tabular-nums}
.prose th,.prose td{border:0;border-bottom:1px solid var(--dk-border);padding:.75rem .9rem;text-align:left;vertical-align:top}
.prose tr:last-child td{border-bottom:0}.prose tbody tr:nth-child(even){background:color-mix(in srgb,var(--dk-surface) 62%,transparent)}
.prose th{font-family:var(--dk-font-display);font-weight:700;background:var(--dk-surface);font-size:.88rem;letter-spacing:.01em}
.admonition{--admonition-accent:var(--dk-accent);display:grid;grid-template-columns:auto minmax(0,1fr);gap:.15rem .75rem;max-width:var(--dk-reading-width);margin:1.6rem 0;padding:1rem 1.1rem;border:1px solid var(--dk-border);border-left:4px solid var(--admonition-accent);border-radius:0 .4rem .4rem 0;background:var(--dk-surface)}
.admonition.note{--admonition-accent:#0284c7}.admonition.important{--admonition-accent:#7c3aed}.admonition.tip{--admonition-accent:#0f766e}.admonition.warning{--admonition-accent:#b45309}
.banner{display:block;width:100%;max-width:100%;height:auto;max-height:16rem;margin:0 0 1.75rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);object-fit:cover}
.search-results{position:absolute;top:100%;left:max(1rem,calc((100% - var(--dk-shell-width))/2 + 16rem));width:min(34rem,calc(100% - 2rem));max-height:min(60vh,30rem);overflow:auto;padding:.45rem;background:var(--dk-raised);border:1px solid var(--dk-border);border-radius:var(--dk-radius);box-shadow:var(--dk-shadow)}
.search-results a{display:block;padding:.7rem .75rem;border-radius:.25rem;color:var(--dk-text);text-decoration:none}.search-results small{display:block;margin-top:.2rem;color:var(--dk-muted);font-size:.76rem;line-height:1.45}.search-results mark{padding:0 .1em;background:color-mix(in srgb,var(--dk-accent) 22%,transparent);border-radius:.1rem;color:var(--dk-text);font-weight:700}.search-empty{margin:.25rem;padding:.7rem .75rem;color:var(--dk-muted);font-size:.82rem}
.mobile-nav{display:none}.toc{position:sticky;top:6rem;align-self:start;max-height:calc(100vh - 7rem);overflow:auto;padding-left:1rem;border-left:1px solid var(--dk-border);font-size:.8rem;line-height:1.4;color:var(--dk-muted);scrollbar-color:var(--dk-border) transparent;scrollbar-width:thin}
.toc-title{margin:0 0 .65rem;font-family:var(--dk-font-display);font-size:.68rem;font-weight:750;letter-spacing:.1em;text-transform:uppercase;color:var(--dk-text)}
.toc a{display:block;padding:.3rem .6rem;border-left:2px solid transparent;color:var(--dk-muted);text-decoration:none;overflow-wrap:anywhere}.toc a:hover{background:var(--dk-surface);color:var(--dk-text)}.toc .toc-level-3{padding-left:1.15rem;font-size:.94em}.toc-empty-copy{margin:0;font-size:.9em}
.page-navigation{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start;gap:var(--dk-space-3);margin:4rem 0 1rem;padding-top:1.25rem;border-top:1px solid var(--dk-border)}.page-navigation a{min-height:0;max-width:none;padding:0;border:0;border-radius:0;background:transparent;display:flex;flex-direction:column;color:var(--dk-text);font-family:var(--dk-font-display);text-decoration:none}.page-navigation a small{font-family:var(--dk-font-mono);font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--dk-muted)}.page-navigation a span{margin-top:.15rem;font-size:1rem;line-height:1.4}.page-navigation a:hover span{color:var(--dk-interactive)}.page-navigation .page-next{grid-column:2;margin-left:0;justify-self:end;text-align:right;align-items:flex-end}
.site-footer{display:flex;gap:1rem;flex-wrap:wrap;max-width:var(--dk-shell-width);margin:0 auto;padding:1.25rem clamp(1rem,3vw,2rem);border-top:1px solid var(--dk-border);color:var(--dk-muted);font-family:var(--dk-font-ui);font-size:.82rem}.site-footer a{color:var(--dk-interactive);font-weight:650;text-decoration:none}.site-footer a:hover{text-decoration:underline;text-decoration-thickness:.08em;text-underline-offset:.16em}
@media(max-width:1024px){.shell{grid-template-columns:13rem minmax(0,var(--dk-content-width));gap:2rem}.toc{display:none}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}}
@media(forced-colors:active){button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline-color:Highlight}.reading-progress span{background:Highlight}}


.topbar{display:grid;grid-template-columns:auto minmax(12rem,30rem) max-content;grid-template-rows:auto var(--dk-control-height);gap:var(--dk-space-2) var(--dk-space-3);align-items:stretch;padding:.65rem clamp(1rem,3vw,2rem)}
.brand{display:inline-flex;align-items:center;gap:.35rem;grid-row:1 / span 2;align-self:center;min-height:var(--dk-control-height);font-family:var(--dk-font-display);font-size:.95rem;font-weight:750;letter-spacing:-.025em;color:var(--dk-text);text-decoration:none;white-space:nowrap}
.brand-logo{display:block;width:2rem;height:2rem;flex:0 0 2rem;object-fit:contain}
.header-controls{grid-column:3;grid-row:1 / span 2;display:grid;grid-template-columns:repeat(3,minmax(5.2rem,max-content));align-items:stretch;gap:var(--dk-space-2)}
.header-control{display:grid;grid-template-rows:auto var(--dk-control-height);gap:.2rem;min-width:5.2rem}
.header-control>span{padding-left:.1rem;color:var(--dk-muted);font-size:.65rem;font-weight:700;letter-spacing:.08em;line-height:1;text-transform:uppercase}
.header-control select{width:100%;height:var(--dk-control-height);min-height:var(--dk-control-height);padding:.35rem .55rem;background:var(--dk-surface)}
select:hover,.topbar .search-control input:hover{border-color:color-mix(in srgb,var(--dk-accent) 52%,var(--dk-border))}
/* Shared surfaces and type; each style changes only its material and signature. */
.hero{position:relative;isolation:isolate;margin:0 0 2.75rem;padding:clamp(1.5rem,4.5vw,3rem);border:1px solid color-mix(in srgb,var(--dk-accent) 20%,var(--dk-border));border-radius:calc(var(--dk-radius)*2);background:var(--dk-surface);overflow:hidden}
.hero::before,.hero::after{content:"";position:absolute;inset:0;z-index:-1}
.hero::after{background-image:radial-gradient(color-mix(in srgb,var(--dk-accent) 26%,transparent) 1px,transparent 1px);background-size:1.15rem 1.15rem;-webkit-mask-image:linear-gradient(155deg,#000 8%,transparent 58%);mask-image:linear-gradient(155deg,#000 8%,transparent 58%)}
.hero h1{font-size:clamp(2.4rem,5vw,3.4rem);letter-spacing:-.04em;margin-bottom:1rem;overflow-wrap:break-word}
.hero-copy{min-width:0}
.hero .hero-copy>p{max-width:42rem;color:var(--dk-muted);font-size:1.16rem;line-height:1.62}
.hero .release-context{display:inline-flex;align-self:flex-start;margin:0 0 1.15rem}
.hero-actions{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:1.6rem}
.prose .hero-actions a{display:inline-flex;align-items:center;justify-content:center;min-height:2.65rem;padding:.55rem 1.2rem;border-radius:var(--dk-radius);font-family:var(--dk-font-ui);font-size:.92rem;font-weight:700;text-decoration:none;transition:box-shadow .16s ease,border-color .16s ease}
.prose .hero-actions a:hover{text-decoration:none}
.prose .hero-primary{border:1px solid color-mix(in srgb,var(--dk-interactive) 72%,#000);background:var(--dk-interactive);color:var(--dk-on-interactive,#fff)}
.prose .hero-primary:hover{box-shadow:0 .45rem 1.1rem color-mix(in srgb,var(--dk-accent) 34%,transparent)}
.prose .hero-secondary{border:1px solid var(--dk-border);background:var(--dk-raised);color:var(--dk-interactive)}
.prose .hero-secondary:hover{border-color:color-mix(in srgb,var(--dk-accent) 44%,var(--dk-border))}
.hero.hero-art{display:flex;flex-direction:column;padding:0}
.hero.hero-art h1{font-size:clamp(2rem,3.5vw,3rem);letter-spacing:-.04em}
.hero.hero-art .hero-copy{padding:clamp(1.5rem,4vw,2.9rem)}
.hero-figure{overflow:hidden;border-bottom:1px solid var(--dk-border)}
.hero-figure .banner{display:block;width:100%;height:auto;max-height:15rem;margin:0;border:0;border-radius:0;object-fit:cover;object-position:center}
.prose p{margin:1rem 0}
.prose li+li{margin-top:.35rem}
.prose li>ul,.prose li>ol{margin-top:.35rem;margin-bottom:.25rem}
.prose p,.prose li,.prose dd{text-wrap:pretty;orphans:3;widows:3}
.prose p,.prose li{overflow-wrap:break-word;hyphens:auto;-webkit-hyphens:auto;hyphenate-limit-chars:6 3 2}
.prose dl{margin:1.35rem 0}
.prose dt{margin-top:1rem;font-family:var(--dk-font-display);font-weight:750}
.prose dd{margin:.2rem 0 0 1.25rem;color:var(--dk-text)}
.prose :is(pre,.table-scroll,.admonition)+:is(h2,h3){margin-top:3.75rem}
.capability-strip[data-card-count="2"]{grid-template-columns:repeat(2,minmax(0,1fr))}
.capability-strip[data-card-count="3"]{grid-template-columns:repeat(3,minmax(0,1fr))}
.capability-strip[data-card-count="4"]{grid-template-columns:repeat(4,minmax(0,1fr))}
.card-icon{display:block;box-sizing:content-box;width:1.25rem;height:1.25rem;padding:.5rem;margin-bottom:1rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius);background:var(--dk-surface);color:var(--dk-interactive)}
.capability-strip li+li{margin-top:0}
.prose pre code{display:block;min-width:max-content;font-size:.9rem;line-height:1.7;font-variant-ligatures:none}
.syntax-highlight .tok-keyword{font-weight:650}
.syntax-highlight .tok-function{font-weight:600}
.prose tbody tr:hover{background:color-mix(in srgb,var(--dk-surface) 82%,transparent)}
.admonition>strong{grid-row:1;color:var(--admonition-accent);font-size:.76rem;letter-spacing:.07em;line-height:1.6;text-transform:uppercase}
.admonition>p{grid-column:2;margin:0;line-height:1.6}
.search-results a+a{margin-top:.15rem}
.search-results a:hover,.search-results a:focus-visible{background:var(--dk-surface);text-decoration:none}
.search-results a strong{display:block;font-family:var(--dk-font-display);font-size:.9rem;line-height:1.35}
.toc a.is-active{margin-left:-1.1rem;border-left-color:var(--dk-accent);color:var(--dk-interactive);font-weight:700;text-decoration:none}
.toc .toc-level-4{padding-left:1.5rem;font-size:.96em}
.toc .toc-level-5{padding-left:1.85rem;font-size:.92em}
.toc .toc-level-6{padding-left:2.2rem;font-size:.92em}
@media(hover:hover){.capability-strip li:hover{border-color:var(--dk-interactive);box-shadow:inset 0 3px var(--dk-interactive)}}
/* Glass composites stay within palette.py contrast bounds; blur is optional. */
html[data-visual-theme="glassmorphic"] body{background:radial-gradient(46rem 32rem at 10% 12%,color-mix(in srgb,var(--dk-accent) var(--dk-mesh-1),transparent),transparent 58%),radial-gradient(38rem 30rem at 94% 8%,color-mix(in srgb,var(--dk-accent-secondary) var(--dk-mesh-2),transparent),transparent 55%),radial-gradient(42rem 34rem at 52% 118%,color-mix(in srgb,var(--dk-accent) var(--dk-mesh-3),transparent),transparent 60%),radial-gradient(28rem 24rem at 76% 74%,color-mix(in srgb,var(--dk-accent-secondary) var(--dk-mesh-4),transparent),transparent 55%),var(--dk-bg);background-attachment:fixed}
html[data-visual-theme="glassmorphic"] :is(.site-header,.hero,.capability-strip li,.release-context,.search-results,.sidebar,.toc,.mobile-nav){background:var(--dk-glass);border-color:color-mix(in srgb,var(--dk-raised) 30%,var(--dk-border));box-shadow:inset 0 1px 0 color-mix(in srgb,var(--dk-raised) 70%,transparent),0 1.25rem 2.8rem -.55rem color-mix(in srgb,var(--dk-bg) 65%,transparent)}
html[data-visual-theme="glassmorphic"] .hero::before{background:radial-gradient(48rem 22rem at 12% -12%,color-mix(in srgb,var(--dk-accent) 34%,transparent),transparent 62%),radial-gradient(38rem 20rem at 96% 4%,color-mix(in srgb,var(--dk-accent-secondary) 30%,transparent),transparent 60%)}
html[data-visual-theme="glassmorphic"] :is(.sidebar,.toc){padding:1rem;border:1px solid var(--dk-border);border-radius:var(--dk-radius)}
html[data-visual-theme="glassmorphic"] .release-context{border-radius:.65rem}
html[data-visual-theme="glassmorphic"] .topbar :is(select,button,.search-control input){background:color-mix(in srgb,var(--dk-surface) 78%,transparent);border-color:color-mix(in srgb,var(--dk-raised) 30%,var(--dk-border));border-radius:var(--dk-radius);box-shadow:inset 0 1px 0 color-mix(in srgb,var(--dk-raised) 55%,transparent)}
@supports ((backdrop-filter:blur(2px)) or (-webkit-backdrop-filter:blur(2px))){
  html[data-visual-theme="glassmorphic"] .site-header{backdrop-filter:blur(28px) saturate(1.5);-webkit-backdrop-filter:blur(28px) saturate(1.5)}
  html[data-visual-theme="glassmorphic"] :is(.hero,.capability-strip li,.search-results,.sidebar,.toc,.mobile-nav,.topbar select,.topbar button,.topbar .search-control input){backdrop-filter:blur(20px) saturate(1.35);-webkit-backdrop-filter:blur(20px) saturate(1.35)}
}
/* Style signatures: one scoped touch per visual theme; colour modes inherit them. */
html[data-visual-theme="classic"] .hero{border-top:3px solid var(--dk-interactive)}
html[data-visual-theme="classic"] .prose h2{border-left:3px solid var(--dk-accent);padding-left:.7rem}
html[data-visual-theme="paper"] .hero{background:var(--dk-raised);border-width:0 0 1px;border-radius:0}
html[data-visual-theme="paper"] .hero .hero-copy{padding:clamp(1rem,3vw,2rem) 0}
html[data-visual-theme="paper"] .hero .hero-copy>p{font-style:italic}
html[data-visual-theme="paper"] .prose>p:first-of-type::first-letter{float:left;margin:.06em .12em 0 0;font-family:var(--dk-font-display);font-size:3.1em;font-weight:700;line-height:1;color:var(--dk-interactive)}
html[data-visual-theme="e-ink"] .prose h1{border-bottom:3px double var(--dk-text);padding-bottom:.5rem}
@supports ((background-clip:text) or (-webkit-background-clip:text)){html[data-visual-theme="glassmorphic"] .hero h1{background:linear-gradient(135deg,var(--dk-interactive),var(--dk-text));-webkit-background-clip:text;background-clip:text;color:transparent}}
html[data-visual-theme="glassmorphic"] .hero-emoji h1{background:none;color:var(--dk-text)}
@supports not ((backdrop-filter:blur(2px)) or (-webkit-backdrop-filter:blur(2px))){html[data-visual-theme="glassmorphic"]{--dk-glass:var(--dk-surface)}}
.mobile-nav h2{font-size:.72rem;letter-spacing:.12em}
summary{cursor:pointer}
@media(max-width:768px){
  body{font-size:16px}
  .topbar{display:flex;flex-wrap:wrap;align-items:center}
  .header-controls{order:2;display:flex;flex:1;min-width:0;align-items:flex-end}
  .search-control{order:3;flex-basis:100%;max-width:none}
  .shell{display:block;padding-top:1.5rem}
  .sidebar{display:none}
  .mobile-nav{display:block;margin:0;padding:0 1rem .75rem;border-bottom:1px solid var(--dk-border);background:var(--dk-surface)}
  .mobile-nav summary{min-height:2.75rem;padding:.65rem 0;cursor:pointer;font-family:var(--dk-font-display);font-size:.86rem;font-weight:700;list-style-position:inside}
  .mobile-nav h2{margin:1rem 0 .35rem;padding-left:.25rem;color:var(--dk-muted);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase}
  .mobile-nav a{display:block;padding:.55rem .25rem;color:var(--dk-muted);text-decoration:none}
  .mobile-nav a:hover{background:var(--dk-surface);color:var(--dk-text)}
  .mobile-nav a.active{color:var(--dk-interactive);font-weight:700}
  .toc{display:none}
  .prose h1{font-size:2.15rem}
  .copy-code{opacity:1}
  .capability-strip[data-card-count="4"],.capability-strip[data-card-count="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:600px){
  .topbar{gap:.5rem}
  .brand{flex:0 0 100%}
  .header-controls{width:100%;gap:.35rem}
  .header-control{flex:1;min-width:0}
  .header-control>span{font-size:.6rem}
  .topbar select{width:100%;min-width:0}
  .prose .capability-strip{grid-template-columns:1fr}
  .page-navigation{grid-template-columns:1fr;margin-top:3rem}
  .page-navigation .page-next{grid-column:1;justify-self:start;text-align:left;align-items:flex-start}
}
@media(max-width:420px){
  .brand{font-size:.9rem}
  .topbar select,button{font-size:.78rem}
  .header-control select{font-size:.75rem}
  .prose pre{margin-inline:-.25rem;padding-inline:1rem}
}
@media print{
  .reading-progress,.site-header,.mobile-nav,.toc,.page-navigation,.hero-actions{display:none}
  .hero::before,.hero::after{display:none}
  .hero{border-color:#999;background:none}
  body{background:#fff;color:#000;font-size:12pt;line-height:1.5}
  html[data-visual-theme="glassmorphic"] body{background:#fff}
  html[data-visual-theme="paper"] .prose{padding:0;border:0;background:none;box-shadow:none}
  html[data-visual-theme="glassmorphic"] :is(.hero,.capability-strip li){background:none;box-shadow:none}
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
  try{const value=readStored(visualKey,legacyVisualKey);if(['classic','paper','e-ink','glassmorphic'].includes(value)){visual.value=value;setVisualTheme(value)}else if(visual){visual.value=root.dataset.visualTheme||'classic'}}catch(_){ }
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
