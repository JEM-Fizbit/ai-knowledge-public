#!/usr/bin/env python3
"""Render a public-presence register as one searchable HTML page.

Usage:  python3 build_dashboard.py REGISTER.md [--out PAGE.html]

The register (markdown) is the source of truth; never edit the HTML by hand.
Default output sits next to the register with an .html suffix — keep it out of
any public repo or site (gitignore it) and publish it only somewhere private.

The page leaves out the "Account email" column and the "## Private settings"
section on purpose: login addresses and contact data stay in the register.

Expected register shapes (see assets/register-template.md):
  ## Table P1 / P2 / P3 headings, each with "### P1a — Title" subsections
  holding one markdown table; a "## Findings" table whose Status column is
  Open / In progress / Resolved; "## Plan" with "### Phase N — Title · Status"
  subsections of "- " bullets (Status Done / Now / Waiting / Next / Later);
  and "- " bullets under "## Maintenance".
"""
import argparse, datetime, html, io, pathlib, re, subprocess

DROP_COLS = {"Account email"}

TIERS = [  # (key, heading prefix in the register, display title, one-line dek)
    ("P1", "## Table P1", "You control", "Your own accounts and sites. You can change these directly."),
    ("P2", "## Table P2", "You can influence", "Hosted by others, but you can edit, claim, file, or ask for a correction."),
    ("P3", "## Table P3", "Little or no control", "Brokers, mirrors, press and namesakes. Opt-outs at best."),
]


def esc(s):
    return html.escape(str(s), quote=True)


def inline(s):
    """Render the register's inline markdown: code, links, bold, italic, strike, ⚠."""
    s = html.escape(s, quote=False)
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               lambda m: f'<a href="{m.group(2).replace(chr(34), "%22")}" target="_blank" rel="noopener">{m.group(1)}</a>', s)
    s = re.sub(r"~~(.+?)~~", r"<s>\1</s>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = s.replace("⚠", '<span class="mark" title="Major issue">⚠</span>')
    s = re.sub("\x00(\\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)
    return s


def plain(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return re.sub(r"[*`~]", "", s).lower()


def cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def tables_in(block):
    """Yield (header, rows, trailing_paragraphs) for each markdown table in a block."""
    lines = block.split("\n")
    i, out = 0, []
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            head = cells(lines[i])
            rows, i = [], i + 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            notes = []
            while i < len(lines) and not lines[i].startswith(("|", "#", "---")):
                if lines[i].strip():
                    notes.append(lines[i].strip())
                i += 1
            out.append((head, rows, notes))
        else:
            i += 1
    return out


def section(text, start, stop="\n## "):
    a = text.index(start)
    b = text.find(stop, a + len(start))
    return text[a:b if b != -1 else len(text)]


def status_class(t):
    l = plain(t)
    if "private" in l:
        return "st-private"
    if "stale" in l or "blocked" in l:
        return "st-warn"
    if any(k in l for k in ("dead", "removed", "not found", "taken down")):
        return "st-off"
    if any(k in l for k in ("dormant", "empty", "placeholder", "redirect", "historical", "permanent", "low", "unverified")):
        return "st-quiet"
    if any(k in l for k in ("live", "active", "current")):
        return "st-live"
    return "st-quiet"


def table_html(tier, head, rows):
    keep = [i for i, h in enumerate(head) if h not in DROP_COLS]
    st = head.index("Status") if "Status" in head else -1
    th = "".join(f'<th scope="col" class="c{n}">{esc(head[i])}</th>' for n, i in enumerate(keep))
    body = []
    for r in rows:
        r = (r + [""] * len(head))[:len(head)]
        flag = any("⚠" in c for c in r)
        tds = []
        for n, i in enumerate(keep):
            c = r[i]
            if i == st and c:
                tds.append(f'<td class="c{n}"><span class="st {status_class(c)}">{inline(c)}</span></td>')
            elif n == 0:
                tds.append(f'<th scope="row" class="c0">{inline(c)}</th>')
            else:
                tds.append(f'<td class="c{n}">{inline(c)}</td>')
        body.append(f'<tr data-tier="{tier}" data-flag="{int(flag)}" data-q="{esc(plain(" ".join(r)))}">{"".join(tds)}</tr>')
    return (f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


def build(reg, out):
    text = io.open(reg, encoding="utf-8").read()
    m = re.search(r"\*\*Last updated:\*\*\s*(\d{4}-\d{2}-\d{2})", text)
    updated = datetime.date.fromisoformat(m.group(1)) if m else datetime.date.today()

    # About: the header blockquote plus every "**Label:** text" paragraph above
    # the first "## " section (tiers, settings, decision rules, conventions)
    about = []
    for line in text.split("\n## ")[0].split("\n"):
        lm = re.match(r">\s*\*\*(.+?):\*\*\s*(.*)", line) or re.match(r"\*\*([^*]+?):\*\*\s*(.*)", line)
        if lm:
            about.append((lm.group(1), lm.group(2)))

    # Tiers
    counts, tier_html, flagged = {}, [], 0
    for key, start, title, dek in TIERS:
        blk = section(text, start)
        subs = re.split(r"\n### ", blk)
        parts, n_rows = [], 0
        groups = [(None, subs[0])] + [(s.split("\n", 1)[0], s) for s in subs[1:]] if len(subs) > 1 else [(None, blk)]
        for name, sub in groups:
            for head, rows, notes in tables_in(sub):
                n_rows += len(rows)
                flagged += sum(any("⚠" in c for c in r) for r in rows)
                label = re.sub(r"^P\d[a-z]\s+—\s+", "", name) if name else ""
                h3 = (f'<h3>{esc(label)} <span class="n" data-count>{len(rows)}</span></h3>' if label else "")
                note = "".join(f'<p class="tnote">{inline(x)}</p>' for x in notes)
                parts.append(f'<div class="group">{h3}{table_html(key, head, rows)}{note}</div>')
        counts[key] = n_rows
        tier_html.append(
            f'<section class="tier" id="{key.lower()}" data-tier-section="{key}" aria-labelledby="{key}-h">'
            f'<header class="tier-head"><span class="tier-chip t-{key}">{key}</span>'
            f'<div><h2 id="{key}-h">{esc(title)} <span class="n" data-count>{n_rows}</span></h2>'
            f'<p class="sub">{esc(dek)}</p></div></header>{"".join(parts)}</section>')

    # Findings
    _, frows, _ = tables_in(section(text, "## Findings"))[0]
    order = {"Open": 0, "In progress": 1, "Resolved": 2}
    items = sorted(frows, key=lambda r: order.get(r[1], 3))
    live = [r for r in items if r[1] != "Resolved"]
    done = [r for r in items if r[1] == "Resolved"]
    chip = {"Open": "f-open", "In progress": "f-prog", "Resolved": "f-done"}

    def finding(r):
        return (f'<li class="finding"><span class="fchip {chip.get(r[1], "f-open")}">{esc(r[1])}</span>'
                f'<div class="ftext"><p class="fwhat">{inline(r[0])}</p><p class="fnext">{inline(r[2])}</p></div></li>')

    findings_html = (f'<ul class="findings">{"".join(finding(r) for r in live)}</ul>'
                     f'<details class="done"><summary><span class="fchip f-done">Resolved</span>'
                     f'<span class="n">{len(done)}</span></summary>'
                     f'<ul class="findings">{"".join(finding(r) for r in done)}</ul></details>')

    # Phase 2 and maintenance bullets
    def bullets(start):
        blk = section(text, start)
        return "".join(f"<li>{inline(l[2:].strip())}</li>" for l in blk.split("\n") if l.startswith("- "))

    plan_chip = {"done": "f-done", "now": "f-open", "waiting": "f-prog", "next": "f-prog", "later": "f-later"}
    plan = []
    for sub in re.split(r"\n### ", section(text, "## Plan"))[1:]:
        head, _, body = sub.partition("\n")
        title, _, status = head.partition(" · ")
        items = "".join(f"<li>{inline(l[2:].strip())}</li>" for l in body.split("\n") if l.startswith("- "))
        plan.append(f'<div class="phase"><div class="phase-head"><h3>{inline(title)}</h3>'
                    f'<span class="fchip {plan_chip.get(status.strip().lower(), "f-later")}">{esc(status.strip())}</span></div>'
                    f'<ul>{items}</ul></div>')
    plan = "".join(plan)
    maint = bullets("## Maintenance")

    try:
        sha = subprocess.check_output(["git", "-C", str(reg.parent), "rev-parse", "--short", "HEAD"],
                                      text=True, stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "-C", str(reg.parent), "status", "--porcelain", reg.name],
                                        text=True, stderr=subprocess.DEVNULL).strip()
        stamp = f"commit {sha}{' + uncommitted edits' if dirty else ''}"
    except Exception:
        stamp = "not under git"

    n_open = sum(1 for r in live if r[1] == "Open")
    n_prog = sum(1 for r in live if r[1] == "In progress")
    about_html = "".join(f"<dt>{esc(k)}</dt><dd>{inline(v)}</dd>" for k, v in about)
    built = datetime.date.today().strftime("%-d %B %Y")

    page = TEMPLATE.format(
        updated=updated.strftime("%-d %B %Y"), p1=counts["P1"], p2=counts["P2"], p3=counts["P3"],
        n_open=n_open, n_prog=n_prog, n_done=len(done), flagged=flagged,
        findings=findings_html, tiers="".join(tier_html), plan=plan, maint=maint,
        about=about_html, built=built, stamp=esc(stamp), reg=esc(reg.name),
    )
    io.open(out, "w", encoding="utf-8").write(page)
    print(f"Wrote {out}: P1 {counts['P1']} · P2 {counts['P2']} · P3 {counts['P3']} · "
          f"findings open {n_open}, in progress {n_prog}, resolved {len(done)} · flagged rows {flagged}")


TEMPLATE = """<title>Public Presence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<style>
:root {{
  color-scheme: light;
  --bg: #fbfcfb; --band: #eef3f1; --ink: #111917; --ink-2: #47524e; --ink-3: #6c7773;
  --rule: #dde4e1; --rule-2: #c4ceca;
  --accent: #0d5c55; --accent-ink: #ffffff; --accent-wash: #dfeeea;
  --p2: #2a5fa8; --p2-wash: #e3ecf8; --p3: #5d6865; --p3-wash: #e9eeec;
  --good-ink: #0b6b0b; --good-wash: #e2f2e2;
  --warn-ink: #855600; --warn-wash: #fbf0d6;
  --serious-ink: #a3401a; --serious-wash: #fbe6dc;
  --muted-wash: #e9eeec;
  --f-sans: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --f-cond: "IBM Plex Sans Condensed", "IBM Plex Sans", "Arial Narrow", system-ui, sans-serif;
  --f-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --bg: #151b1a; --band: #1c2422; --ink: #edf2f0; --ink-2: #b3beba; --ink-3: #8a9591;
    --rule: #28322f; --rule-2: #38443f;
    --accent: #62c7ba; --accent-ink: #062320; --accent-wash: #173430;
    --p2: #8ab4ec; --p2-wash: #1b2a3d; --p3: #a3aeaa; --p3-wash: #222b29;
    --good-ink: #58d158; --good-wash: #16291a;
    --warn-ink: #f2b233; --warn-wash: #2f2710;
    --serious-ink: #f09a73; --serious-wash: #35221a;
    --muted-wash: #222b29;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --bg: #151b1a; --band: #1c2422; --ink: #edf2f0; --ink-2: #b3beba; --ink-3: #8a9591;
  --rule: #28322f; --rule-2: #38443f;
  --accent: #62c7ba; --accent-ink: #062320; --accent-wash: #173430;
  --p2: #8ab4ec; --p2-wash: #1b2a3d; --p3: #a3aeaa; --p3-wash: #222b29;
  --good-ink: #58d158; --good-wash: #16291a;
  --warn-ink: #f2b233; --warn-wash: #2f2710;
  --serious-ink: #f09a73; --serious-wash: #35221a;
  --muted-wash: #222b29;
}}
body {{ background: var(--bg); color: var(--ink); font: 14px/1.5 var(--f-sans); -webkit-font-smoothing: antialiased; }}
.wrap {{ max-width: 1240px; margin-inline: auto; padding-inline: clamp(16px, 4vw, 40px); padding-block: 36px 56px; display: flex; flex-direction: column; gap: 40px; }}
h1, h2, h3, p, ul, dl, dd {{ margin: 0; }}
ul {{ padding: 0; list-style: none; }}
a {{ color: var(--accent); text-underline-offset: 2px; text-decoration-thickness: 1px; }}
a:hover {{ text-decoration-thickness: 2px; }}
code {{ font: 12px var(--f-mono); color: var(--ink-2); background: var(--band); padding: 1px 5px; border-radius: 3px; overflow-wrap: anywhere; }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }}
.vh {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
.sub {{ color: var(--ink-3); font-size: 13px; }}
.n {{ font: 500 12px var(--f-mono); color: var(--ink-2); background: var(--band); border-radius: 999px; padding: 1px 8px; vertical-align: 2px; font-variant-numeric: tabular-nums; }}
.mark {{ color: var(--serious-ink); font-weight: 600; }}

.mast {{ display: flex; flex-direction: column; gap: 8px; max-width: 70ch; }}
.eyebrow {{ font: 500 12px var(--f-cond); letter-spacing: 0.09em; text-transform: uppercase; color: var(--ink-3); }}
h1 {{ font: 600 clamp(32px, 5vw, 46px)/1.02 var(--f-cond); letter-spacing: -0.015em; text-wrap: balance; }}
.dek {{ color: var(--ink-2); font-size: 15px; }}

.figures {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; background: var(--rule); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; }}
.fig {{ background: var(--band); padding: 18px 20px 20px; display: flex; flex-direction: column; gap: 4px; text-decoration: none; color: inherit; }}
a.fig:hover {{ background: var(--accent-wash); }}
.fig-label {{ font: 500 12px var(--f-cond); letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-3); display: flex; align-items: center; gap: 8px; }}
.fig-value {{ font: 600 34px/1.1 var(--f-sans); letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }}
.fig-note {{ font-size: 13px; color: var(--ink-2); }}
.fig-warn {{ color: var(--serious-ink); }}
@media (max-width: 880px) {{ .figures {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}

h2 {{ font: 600 20px/1.2 var(--f-cond); letter-spacing: -0.005em; text-wrap: balance; }}
h3 {{ font: 600 15px/1.3 var(--f-cond); letter-spacing: 0.01em; color: var(--ink); }}

/* findings */
.attention {{ display: flex; flex-direction: column; gap: 12px; }}
.attention-head {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 8px 14px; }}
.findings {{ display: flex; flex-direction: column; }}
.finding {{ display: grid; grid-template-columns: 7.2rem minmax(0, 1fr); gap: 14px; padding: 13px 0; border-bottom: 1px solid var(--rule); }}
.finding:first-child {{ border-top: 1px solid var(--rule); }}
.ftext {{ display: flex; flex-direction: column; gap: 4px; max-width: 92ch; }}
.fwhat {{ text-wrap: pretty; }}
.fnext {{ font-size: 13px; color: var(--ink-2); text-wrap: pretty; }}
.fchip {{ justify-self: start; align-self: start; font: 600 11.5px var(--f-cond); letter-spacing: 0.07em; text-transform: uppercase; padding: 2px 9px; border-radius: 999px; white-space: nowrap; }}
.f-open {{ background: var(--serious-wash); color: var(--serious-ink); }}
.f-prog {{ background: var(--warn-wash); color: var(--warn-ink); }}
.f-done {{ background: var(--good-wash); color: var(--good-ink); }}
.f-later {{ background: var(--muted-wash); color: var(--ink-3); }}
.done summary {{ display: flex; align-items: center; gap: 10px; cursor: pointer; list-style: none; padding: 12px 0 10px; font-size: 13px; }}
.done summary::-webkit-details-marker {{ display: none; }}
.done summary::after {{ content: "Show"; color: var(--accent); font-size: 12.5px; }}
.done[open] summary::after {{ content: "Hide"; }}
@media (max-width: 560px) {{ .finding {{ grid-template-columns: minmax(0, 1fr); gap: 6px; }} }}

/* controls */
.controls {{ display: flex; flex-wrap: wrap; gap: 10px 14px; align-items: center; padding: 12px 0; border-block: 1px solid var(--rule); position: sticky; top: env(safe-area-inset-top, 0px); background: var(--bg); z-index: 5; }}
.seg-ctl {{ display: inline-flex; flex-wrap: wrap; gap: 2px; padding: 2px; border: 1px solid var(--rule-2); border-radius: 8px; background: var(--bg); }}
.seg-ctl button {{ font: 500 13px var(--f-sans); color: var(--ink-2); background: transparent; border: 0; border-radius: 6px; padding: 6px 10px; cursor: pointer; }}
.seg-ctl button:hover {{ background: var(--band); color: var(--ink); }}
.seg-ctl button[aria-pressed="true"] {{ background: var(--accent); color: var(--accent-ink); }}
.toggle {{ display: inline-flex; align-items: center; gap: 7px; font-size: 13px; color: var(--ink-2); cursor: pointer; }}
.toggle input {{ accent-color: var(--accent); width: 15px; height: 15px; }}
.search {{ flex: 1 1 13rem; max-width: 24rem; }}
.search input {{ width: 100%; box-sizing: border-box; font: 13px var(--f-sans); color: var(--ink); background: var(--bg); border: 1px solid var(--rule-2); border-radius: 8px; padding: 7px 10px; }}
.search input::placeholder {{ color: var(--ink-3); }}
#shown {{ margin-left: auto; font: 12px var(--f-mono); color: var(--ink-3); font-variant-numeric: tabular-nums; }}

/* tiers */
.tiers {{ display: flex; flex-direction: column; gap: 44px; }}
.tier {{ display: flex; flex-direction: column; gap: 22px; scroll-margin-top: 72px; }}
.tier-head {{ display: flex; gap: 14px; align-items: flex-start; }}
.tier-chip {{ font: 600 13px/1 var(--f-mono); padding: 7px 8px; border-radius: 6px; flex: none; margin-top: 1px; }}
.t-P1 {{ background: var(--accent); color: var(--accent-ink); }}
.t-P2 {{ background: var(--p2-wash); color: var(--p2); }}
.t-P3 {{ background: var(--p3-wash); color: var(--p3); }}
.group {{ display: flex; flex-direction: column; gap: 10px; }}
.table-wrap {{ overflow-x: auto; border: 1px solid var(--rule); border-radius: 10px; background: var(--bg); }}
table {{ width: 100%; min-width: 900px; border-collapse: collapse; font-size: 13px; }}
thead th {{ text-align: left; font: 600 11.5px var(--f-cond); letter-spacing: 0.07em; text-transform: uppercase; color: var(--ink-3); background: var(--band); padding: 9px 12px; border-bottom: 1px solid var(--rule); white-space: nowrap; }}
td, tbody th {{ padding: 10px 12px; border-bottom: 1px solid var(--rule); vertical-align: top; text-align: left; font-weight: 400; overflow-wrap: anywhere; }}
tbody th {{ font-weight: 600; min-width: 11rem; }}
tbody tr:last-child td, tbody tr:last-child th {{ border-bottom: 0; }}
tbody tr:hover td, tbody tr:hover th {{ background: var(--band); }}
tr[data-flag="1"] th.c0 {{ box-shadow: inset 3px 0 0 var(--serious-ink); }}
td:last-child {{ min-width: 20rem; color: var(--ink-2); }}
.st {{ display: inline-block; font-size: 11.5px; font-weight: 500; padding: 1px 8px; border-radius: 999px; white-space: nowrap; }}
.st strong {{ font-weight: 600; }}
.st-live {{ color: var(--good-ink); background: var(--good-wash); }}
.st-warn {{ color: var(--warn-ink); background: var(--warn-wash); }}
.st-private {{ color: var(--accent); background: var(--accent-wash); }}
.st-quiet, .st-off {{ color: var(--ink-3); background: var(--muted-wash); }}
.st-off {{ text-decoration: line-through; }}
.tnote {{ font-size: 12.5px; color: var(--ink-3); max-width: 100ch; }}
.empty {{ padding: 28px; text-align: center; color: var(--ink-3); border: 1px dashed var(--rule-2); border-radius: 10px; }}

/* plan, about, footer */
.phases {{ margin-top: 14px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); gap: 1px; background: var(--rule); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; }}
.phase {{ background: var(--bg); padding: 16px 18px 18px; display: flex; flex-direction: column; gap: 10px; }}
.phase-head {{ display: flex; justify-content: space-between; align-items: baseline; gap: 10px; }}
.phase ul {{ margin-top: 0; gap: 7px; font-size: 13px; }}
.next ul, .about ul {{ margin-top: 10px; display: flex; flex-direction: column; gap: 8px; max-width: 90ch; }}
.next li, .about li {{ color: var(--ink-2); padding-left: 16px; position: relative; }}
.next li::before, .about li::before {{ content: ""; position: absolute; left: 0; top: 0.62em; width: 6px; height: 6px; border-radius: 1px; background: var(--rule-2); }}
.about summary {{ cursor: pointer; font: 600 20px/1.2 var(--f-cond); list-style: none; display: flex; align-items: center; gap: 10px; }}
.about summary::-webkit-details-marker {{ display: none; }}
.about summary::after {{ content: "Show"; color: var(--accent); font: 12.5px var(--f-sans); }}
.about[open] summary::after {{ content: "Hide"; }}
.about dl {{ margin-top: 14px; display: grid; grid-template-columns: 11rem minmax(0, 1fr); gap: 10px 20px; max-width: 110ch; }}
.about dt {{ font: 600 12px var(--f-cond); letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-3); padding-top: 2px; }}
.about dd {{ color: var(--ink-2); }}
.about h3 {{ margin-top: 22px; }}
@media (max-width: 640px) {{ .about dl {{ grid-template-columns: minmax(0, 1fr); gap: 2px; }} .about dd {{ margin-bottom: 10px; }} }}
.foot {{ border-top: 1px solid var(--rule); padding-top: 16px; font-size: 12.5px; color: var(--ink-3); max-width: 90ch; }}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior: smooth; }} }}
</style>

<div class="wrap">
  <header class="mast">
    <p class="eyebrow">Personal register · updated {updated}</p>
    <h1>Public Presence</h1>
    <p class="dek">Every public place that identifies you, sorted by how much control you have over it, with the issues found and where each one stands.</p>
  </header>

  <section class="figures" aria-label="Summary">
    <a class="fig" href="#p1"><p class="fig-label"><span class="tier-chip t-P1">P1</span>You control</p><p class="fig-value">{p1}</p><p class="fig-note">accounts and sites</p></a>
    <a class="fig" href="#p2"><p class="fig-label"><span class="tier-chip t-P2">P2</span>You can influence</p><p class="fig-value">{p2}</p><p class="fig-note">pages others host</p></a>
    <a class="fig" href="#p3"><p class="fig-label"><span class="tier-chip t-P3">P3</span>Little control</p><p class="fig-value">{p3}</p><p class="fig-note">types of site</p></a>
    <a class="fig" href="#findings"><p class="fig-label">Open findings</p><p class="fig-value fig-warn">{n_open}</p><p class="fig-note">plus {n_prog} in progress and {n_done} resolved</p></a>
  </section>

  <section class="attention" id="findings" aria-labelledby="f-h">
    <div class="attention-head"><h2 id="f-h">Findings</h2><p class="sub">Major issues, most urgent first. Phase 3 checks every surface for accuracy.</p></div>
    {findings}
  </section>

  <div class="controls" role="search">
    <div class="seg-ctl" role="group" aria-label="Tier">
      <button type="button" id="t-all" data-t="all" aria-pressed="true">All</button>
      <button type="button" id="t-p1" data-t="P1" aria-pressed="false">P1 · control</button>
      <button type="button" id="t-p2" data-t="P2" aria-pressed="false">P2 · influence</button>
      <button type="button" id="t-p3" data-t="P3" aria-pressed="false">P3 · little</button>
    </div>
    <label class="toggle" for="flagged"><input type="checkbox" id="flagged"> Flagged only ({flagged})</label>
    <label class="search"><span class="vh">Search surfaces</span><input id="q" type="search" placeholder="Search surfaces, owners, notes" autocomplete="off"></label>
    <span id="shown" aria-live="polite"></span>
  </div>

  <div class="tiers" id="tiers">
    {tiers}
    <p class="empty" id="empty" hidden>Nothing matches. Clear the search or switch tier.</p>
  </div>

  <section class="next" id="plan" aria-labelledby="n-h">
    <h2 id="n-h">Plan</h2>
    <div class="phases">{plan}</div>
  </section>

  <details class="about">
    <summary>About this register</summary>
    <dl>{about}</dl>
    <h3>Keeping it current</h3>
    <ul>{maint}</ul>
  </details>

  <footer class="foot">
    <p>Built {built} from <code>{reg}</code> ({stamp}). Login emails and private settings stay in the register and are left off this page. To refresh, edit the register and rebuild with the public-presence-audit skill's <code>build_dashboard.py</code>, or ask Claude to rebuild the page.</p>
  </footer>
</div>

<script>
(() => {{
  const rows = [...document.querySelectorAll('#tiers tbody tr')];
  const sections = [...document.querySelectorAll('[data-tier-section]')];
  let t = 'all', flag = false, q = '';
  try {{ const s = JSON.parse(localStorage.getItem('presence-view') || '{{}}'); if (s.t) t = s.t; if (s.flag) flag = true; }} catch (e) {{}}
  const flagBox = document.getElementById('flagged');
  const apply = () => {{
    const needle = q.trim().toLowerCase();
    let n = 0;
    for (const r of rows) {{
      const ok = (t === 'all' || r.dataset.tier === t) && (!flag || r.dataset.flag === '1') && (!needle || r.dataset.q.includes(needle));
      r.hidden = !ok; if (ok) n++;
    }}
    document.querySelectorAll('.group').forEach((g) => {{
      const vis = g.querySelectorAll('tbody tr:not([hidden])').length;
      g.hidden = vis === 0;
      const c = g.querySelector('[data-count]'); if (c) c.textContent = vis;
    }});
    sections.forEach((s) => {{
      const vis = s.querySelectorAll('tbody tr:not([hidden])').length;
      s.hidden = vis === 0;
      const c = s.querySelector('.tier-head [data-count]'); if (c) c.textContent = vis;
    }});
    document.getElementById('empty').hidden = n > 0;
    document.getElementById('shown').textContent = `${{n}} of ${{rows.length}} shown`;
    document.querySelectorAll('[data-t]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.t === t)));
    flagBox.checked = flag;
    try {{ localStorage.setItem('presence-view', JSON.stringify({{ t, flag }})); }} catch (e) {{}}
  }};
  document.querySelector('.seg-ctl').addEventListener('click', (e) => {{ const b = e.target.closest('button'); if (b) {{ t = b.dataset.t; apply(); }} }});
  flagBox.addEventListener('change', () => {{ flag = flagBox.checked; apply(); }});
  document.getElementById('q').addEventListener('input', (e) => {{ q = e.target.value; apply(); }});
  document.querySelectorAll('a.fig[href^="#p"]').forEach((a) => a.addEventListener('click', () => {{ t = 'all'; apply(); }}));
  apply();
}})();
</script>
"""

def main():
    ap = argparse.ArgumentParser(description="Render a public-presence register as one searchable HTML page.")
    ap.add_argument("register", type=pathlib.Path, help="path to the register markdown")
    ap.add_argument("--out", type=pathlib.Path, help="output HTML (default: next to the register)")
    a = ap.parse_args()
    reg = a.register.resolve()
    build(reg, (a.out or reg.with_suffix(".html")).resolve())


if __name__ == "__main__":
    main()
