"""Build the Ashgrove Heating & Air concept site into ./docs/.

Usage:  python build.py [BASE_URL]
Run make_photos.py first (photos -> assets/img/*.webp).
"""
import json, shutil, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://liampcurran.github.io/ashgrove-heating").rstrip("/")
TODAY = date.today().isoformat()

BIZ = {
    "name": "Ashgrove Heating & Air",
    "phone": "(613) 555-0142",
    "tel": "+16135550142",
    "email": "hello@example.com",
    "weekday": "Mon–Fri 7am–7pm",
    "sat": "Sat 8am–4pm",
    "emerg": "24/7 no-heat emergencies",
}
RATING = ("4.9", "380+")  # illustrative (concept site) — deliberately NOT emitted as schema

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="#0f2c48"/>'
        '<path d="M20 7c4 6 9 9 9 16a9 9 0 0 1-18 0c0-4 2-6 4-8 0 3 1 5 3 6-1-6 0-10 2-14z" fill="#e8742a"/>'
        '<path d="M20 22c2 2 4 3 4 6a4 4 0 0 1-8 0c0-2 2-4 4-6z" fill="#fff"/></svg>')


def ico(path, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'


I = {
    "phone": ico('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'),
    "flame": ico('<path d="M12 2c3 4.5 6 7 6 12a6 6 0 0 1-12 0c0-3 1.5-4.5 3-6 0 2 .8 3.5 2 4-.6-4 0-7 1-10z"/>'),
    "clock": ico('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'),
    "check": ico('<path d="M20 6 9 17l-5-5"/>'),
    "shield": ico('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
    "star": '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
    "wrench": ico('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>'),
    "calendar": ico('<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
    "doc": ico('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>'),
    "pin": ico('<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    "leaf": ico('<path d="M11 20A7 7 0 0 1 4 13c0-6 6-10 16-10 0 10-4 16-10 16"/><path d="M4 21c4-6 8-9 12-11"/>'),
    "home": ico('<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>'),
    "dollar": ico('<path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'),
    "arrow": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "snow": ico('<path d="M12 2v20M4.9 7l14.2 10M4.9 17 19.1 7"/>'),
    "fan": ico('<circle cx="12" cy="12" r="2"/><path d="M12 10c0-4 1-8 4-8s3 4-4 8zM14 12c4 0 8 1 8 4s-4 3-8-4zM12 14c0 4-1 8-4 8s-3-4 4-8zM10 12c-4 0-8-1-8-4s4-3 8 4z"/>'),
    "user": ico('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
}
STARS = '<span class="stars" role="img" aria-label="5 out of 5 stars">' + I["star"] * 5 + "</span>"


def img(name, widths, alt, sizes="100vw", cls="", eager=False, ratio=None):
    """Responsive <img> for assets/img/<name>-<w>.webp. ratio = (w, h) for intrinsic size."""
    srcset = ", ".join(f"{{p}}assets/img/{name}-{w}.webp {w}w" for w in widths)
    w = widths[-1]
    h = round(w * ratio[1] / ratio[0]) if ratio else round(w * 0.75)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{{p}}assets/img/{name}-{widths[0]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load} decoding="async">')


NAV = [("index.html", "Home"), ("services.html", "Services"), ("furnace-repair-ottawa.html", "Furnace Repair"),
       ("heat-pump-installation-ottawa.html", "Heat Pumps"), ("about.html", "About"), ("blog/", "Advice"), ("contact.html", "Contact")]

AREAS = ["Kanata", "Barrhaven", "Nepean", "Orléans", "Stittsville", "Westboro", "The Glebe", "Alta Vista",
         "Manotick", "Riverside South", "Gloucester", "Centretown", "Hintonburg", "Old Ottawa South", "Greely", "Carp"]

BUSINESS_LD = {
    "@context": "https://schema.org", "@type": "HVACBusiness", "@id": BASE + "/#business",
    "name": BIZ["name"], "url": BASE + "/", "telephone": BIZ["tel"], "email": BIZ["email"],
    "image": BASE + "/assets/og.png", "logo": BASE + "/assets/logo.svg", "priceRange": "$$",
    "description": "Furnace, heat pump and air conditioning installation, repair and maintenance across Ottawa. (Concept project: fictional business.)",
    "address": {"@type": "PostalAddress", "addressLocality": "Ottawa", "addressRegion": "ON", "addressCountry": "CA"},
    "areaServed": [{"@type": "City", "name": "Ottawa"}] + [{"@type": "Place", "name": f"{a}, Ottawa"} for a in AREAS],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "16:00"}],
}


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u}
                                for i, (u, n) in enumerate(items)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs) + "</div>"


def quote_form(fid, title="Get a free quote", sub="We reply within one business hour.", compact=False):
    extra = "" if compact else '<div class="f-full"><label for="{f}-msg">Anything we should know?</label><textarea id="{f}-msg" name="msg" rows="3"></textarea></div>'
    return f'''<form class="lead-form{' compact' if compact else ''}" id="{fid}" novalidate>
<p class="f-title">{title}</p><p class="f-sub">{sub}</p>
<div class="f-full"><label for="{fid}-need">I need help with</label>
<select id="{fid}-need" name="need"><option>No heat / furnace repair</option><option>Heat pump quote</option><option>New furnace quote</option><option>Air conditioning</option><option>Maintenance plan</option><option>Something else</option></select></div>
<div><label for="{fid}-name">Name</label><input id="{fid}-name" name="name" autocomplete="name" required></div>
<div><label for="{fid}-phone">Phone</label><input id="{fid}-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div class="f-full"><label for="{fid}-postal">Postal code</label><input id="{fid}-postal" name="postal" autocomplete="postal-code" placeholder="K2G 1A1"></div>
{extra.format(f=fid)}
<button class="btn btn-lg f-full" type="submit">Request my free quote</button>
<p class="f-fine f-full">{I['shield']} No obligation. Upfront prices, no pressure.</p>
<p class="form-msg f-full" role="status">Thanks! This is a concept site, so nothing was sent. On a live site this request would go to the office inbox and the CRM, and the customer would get an instant text confirmation.</p>
</form>'''


def page(path, title, desc, body, schemas=(), prefix="", hero_preload=None):
    canonical = BASE + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    nav = "".join(
        f'<li><a href="{prefix}{h}"' + (' aria-current="page"' if (h == path or (h == "blog/" and path.startswith("blog/"))) else "") + f'>{l}</a></li>'
        for h, l in NAV)
    preload = ""
    if hero_preload:
        n, ws = hero_preload
        preload = (f'<link rel="preload" as="image" type="image/webp" href="{prefix}assets/img/{n}-{ws[0]}.webp" '
                   f'imagesrcset="' + ", ".join(f"{prefix}assets/img/{n}-{w}.webp {w}w" for w in ws) + '" imagesizes="100vw" fetchpriority="high">')
    html = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f2c48">
<link rel="icon" href="{prefix}assets/logo.svg" type="image/svg+xml">
<link rel="preload" href="{prefix}assets/jakarta.woff2" as="font" type="font/woff2" crossorigin>
{preload}
<link rel="stylesheet" href="{prefix}assets/style.css">
{chr(10).join(ld(s) for s in schemas)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
<span class="tb-emerg">{I['flame']} No heat? 24/7 emergency service</span>
<span class="tb-rating">{STARS} <strong>{RATING[0]}</strong> from {RATING[1]} Google reviews</span>
<span class="tb-hours">{I['clock']} {BIZ['weekday']} · {BIZ['sat']}</span>
</div></div>
<header class="site"><div class="wrap">
<a class="brand" href="{prefix}index.html">{LOGO}<span>Ashgrove<small>Heating &amp; Air</small></span></a>
<nav class="main" aria-label="Main"><ul>{nav}</ul></nav>
<div class="h-actions">
<a class="h-phone" href="tel:{BIZ['tel']}" aria-label="Call {BIZ['phone']}, 24/7">{I['phone']}<span><small>Call 24/7</small>{BIZ['phone']}</span></a>
<a class="btn" href="{prefix}contact.html">Book service</a>
<details class="menu"><summary aria-label="Open menu"><span></span><span></span><span></span></summary><nav aria-label="Mobile"><ul>{nav}</ul>
<a class="btn btn-block" href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a></nav></details>
</div>
</div></header>
<main id="main">
{body.replace("{p}", prefix)}
</main>
<footer class="site">
<div class="wrap f-grid">
<div class="f-brand"><a class="brand light" href="{prefix}index.html">{LOGO}<span>Ashgrove<small>Heating &amp; Air</small></span></a>
<p>Furnaces, heat pumps and air conditioning for Ottawa homes. Licensed gas technicians, upfront prices and tidy work, since 2009.</p>
<p class="f-badges"><span>TSSA licensed</span><span>HRAI member</span><span>Fully insured</span></p></div>
<div><h2>Services</h2><ul>
<li><a href="{prefix}furnace-repair-ottawa.html">Furnace repair</a></li>
<li><a href="{prefix}services.html#furnace">Furnace replacement</a></li>
<li><a href="{prefix}heat-pump-installation-ottawa.html">Heat pump installation</a></li>
<li><a href="{prefix}services.html#ac">Air conditioning</a></li>
<li><a href="{prefix}services.html#maintenance">Maintenance plans</a></li></ul></div>
<div><h2>Company</h2><ul>
<li><a href="{prefix}about.html">About us</a></li>
<li><a href="{prefix}blog/">Homeowner advice</a></li>
<li><a href="{prefix}contact.html">Book service</a></li>
<li><a href="{prefix}index.html#areas">Service areas</a></li></ul></div>
<div><h2>Get in touch</h2><ul class="f-contact">
<li>{I['phone']}<a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></li>
<li>{I['doc']}<a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
<li>{I['clock']}<span>{BIZ['weekday']}<br>{BIZ['sat']}<br>{BIZ['emerg']}</span></li>
<li>{I['pin']}<span>Serving all of Ottawa</span></li></ul></div>
</div>
<div class="wrap concept">Concept project by Liam Curran: a fictional business. Names, phone numbers, reviews, ratings and prices are illustrative only. Photos: Unsplash.</div>
</footer>
<div class="mbar"><a href="tel:{BIZ['tel']}">{I['phone']} Call now</a><a class="q" href="{prefix}contact.html">{I['doc']} Free quote</a></div>
<script src="{prefix}assets/site.js" defer></script>
</body>
</html>
'''
    dest = OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return path


def emergency_band():
    return f'''<section class="emerg">
{img("winter", (800, 1440), "", sizes="100vw", cls="bg", ratio=(16, 9))}
<div class="wrap"><div>
<p class="eyebrow light">{I['flame']} Heating season emergency line</p>
<h2>No heat at 2am? A real person answers.</h2>
<p>No-heat calls get priority 24/7 from October to April. Most homes are warm again the same day.</p></div>
<div class="emerg-ctas"><a class="btn btn-lg" href="tel:{BIZ['tel']}">{I['phone']} Call {BIZ['phone']}</a>
<a class="btn btn-lg btn-ghost-light" href="{{p}}contact.html">Book online</a></div>
</div></section>'''


def page_hero(crumbs, h1, lede, photo, ctas=True):
    trail = " <span>/</span> ".join(f'<a href="{{p}}{u}">{n}</a>' for u, n in crumbs[:-1]) + f" <span>/</span> {crumbs[-1][1]}"
    cta = (f'<div class="ctas"><a class="btn btn-lg" href="tel:{BIZ["tel"]}">{I["phone"]} Call {BIZ["phone"]}</a>'
           f'<a class="btn btn-lg btn-ghost-light" href="{{p}}contact.html">Get a free quote</a></div>') if ctas else ""
    return f'''<section class="page-hero">
{img(photo, (800, 1440), "", sizes="100vw", cls="bg", eager=True, ratio=(4, 3))}
<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">{trail}</nav>
<h1>{h1}</h1><p class="lede">{lede}</p>{cta}
<ul class="hero-trust"><li>{I['check']} Licensed gas technicians</li><li>{I['check']} Price before work starts</li><li>{I['check']} {RATING[0]}★ from {RATING[1]} reviews</li></ul>
</div></section>'''


def sidebar(fid):
    return f'''<aside class="side">{quote_form(fid, "Book a visit", "Tell us what's going on. We'll call you back to confirm a time.", compact=True)}
<div class="side-card"><p class="f-title">Why homeowners pick us</p><ul class="ticks">
<li>{I['check']} Firm price before any work</li><li>{I['check']} Technicians not paid on commission</li>
<li>{I['check']} 2-year labour warranty on repairs</li><li>{I['check']} Boot covers, drop cloths, no mess</li></ul></div></aside>'''


REVIEWS = [
    ("Furnace died on a Sunday night in January. The tech was here before 9 the next morning, found a cracked igniter and had us warm by 10. The price was exactly what they quoted on the phone.", "Sarah M.", "Barrhaven"),
    ("Two other companies told us we needed a whole new system. Ashgrove replaced a $190 flame sensor instead. We'll be calling them when it's actually time to replace.", "Daniel K.", "Kanata"),
    ("They walked us through three heat pump options with real running-cost numbers, helped with the rebate paperwork and left the basement cleaner than they found it.", "Priya &amp; Tom", "Westboro"),
]


def reviews_html():
    cards = "".join(f'''<figure class="review">{STARS}<blockquote>“{q}”</blockquote>
<figcaption><span class="av">{n[0]}</span><span><strong>{n}</strong><small>{a} · Google review</small></span></figcaption></figure>''' for q, n, a in REVIEWS)
    return f'''<section class="block"><div class="wrap">
<div class="sec-head center"><p class="eyebrow">Reviews</p><h2>Rated {RATING[0]} out of 5 by Ottawa homeowners</h2>
<p class="big-rating">{STARS} <strong>{RATING[0]}</strong> average from {RATING[1]} Google reviews</p></div>
<div class="grid c3">{cards}</div></div></section>'''


pages = []
HP_GUIDE = (ROOT / "posts" / "heat-pump-vs-furnace-ottawa.html").exists()
HP_GUIDE_LINK = ('<p class="guide-link">Want the full picture? Read our guide: <a href="blog/heat-pump-vs-furnace-ottawa.html">'
                 'Heat pump or furnace? What actually makes sense in Ottawa</a>.</p>' if HP_GUIDE else "")

# ================= Home =================
home_faqs = [
    ("Do you charge for estimates?", "Quotes for new furnaces, heat pumps and air conditioners are free. For repairs there's a flat diagnostic fee, and we tell you the repair price before any work starts."),
    ("How fast can you come when the heat is out?", "No-heat calls get priority, 24/7 during the heating season. Most are reached the same day."),
    ("Should I repair my furnace or replace it?", "If the furnace is under about 15 years old and the repair is a fraction of a new unit, repair usually wins. We'll show you the numbers both ways and let you decide."),
    ("Do heat pumps work in an Ottawa winter?", "Modern cold-climate heat pumps keep heating well below −20°C. Most Ottawa homes pair one with a furnace or electric backup for the coldest nights."),
    ("Do you offer financing?", "Yes. New systems can be financed with monthly payments, on approved credit. We'll show you the monthly figure alongside the upfront price."),
    ("Which brands do you service?", "All major furnace, heat pump and air conditioner brands. We're not tied to one manufacturer, so we recommend whatever fits your home and budget."),
]
SERVICES = [
    ("furnace", "Furnace repair &amp; replacement", "Same-day diagnosis on most no-heat calls, and honest advice on whether to repair or replace.", "furnace-repair-ottawa.html", "Furnace repair"),
    ("heatpump", "Heat pump installation", "Cold-climate heat pumps sized for your actual home, with rebate and financing help.", "heat-pump-installation-ottawa.html", "Heat pumps"),
    ("ac", "Air conditioning", "Central AC installs, repairs and tune-ups before the July heat arrives.", "services.html#ac", "Air conditioning"),
    ("thermostat", "Maintenance plans", "Yearly tune-ups, priority booking and no overtime fees, from $14 a month.", "services.html#maintenance", "Maintenance plans"),
]
svc_cards = "".join(f'''<a class="svc" href="{{p}}{u}">{img(n, (480, 800), "", sizes="(max-width:640px) 100vw, (max-width:1000px) 50vw, 280px", ratio=(4, 3))}
<span class="svc-body"><strong>{t}</strong><span>{d}</span><span class="more">{l} {I['arrow']}</span></span></a>''' for n, t, d, u, l in SERVICES)

pages.append(page("index.html",
    "Ashgrove Heating & Air | Furnace, Heat Pump & AC Service in Ottawa",
    "Furnace repair, heat pump installation and air conditioning across Ottawa. Upfront prices, licensed technicians and 24/7 no-heat service. Call (613) 555-0142.",
    f'''<section class="hero">
{img("hero", (800, 1440), "Ashgrove technician servicing an outdoor heat pump unit", sizes="100vw", cls="bg", eager=True, ratio=(16, 9))}
<div class="wrap hero-grid">
<div class="hero-copy">
<p class="pill">{STARS} <strong>{RATING[0]}</strong> · {RATING[1]} Google reviews</p>
<h1>Ottawa furnace, heat pump and AC service, done right the first time</h1>
<p class="lede">From a furnace that quit at 2am to a full heat pump upgrade, we diagnose it honestly, quote it upfront and leave your home cleaner than we found it.</p>
<div class="ctas"><a class="btn btn-lg" href="tel:{BIZ['tel']}">{I['phone']} Call {BIZ['phone']}</a><a class="btn btn-lg btn-ghost-light" href="#quote-hero">Get a free quote</a></div>
<ul class="hero-trust"><li>{I['check']} Licensed gas technicians</li><li>{I['check']} Price before work starts</li><li>{I['check']} 24/7 no-heat calls</li></ul>
</div>
{quote_form("quote-hero", "Get a free quote", "Takes 30 seconds. We call back within the hour.", compact=True)}
</div></section>

<section class="actions"><div class="wrap grid c3">
<a class="action urgent" href="tel:{BIZ['tel']}"><span class="a-ico">{I['flame']}</span><span><strong>No heat right now?</strong><small>Priority 24/7 dispatch. Call {BIZ['phone']}</small></span>{I['arrow']}</a>
<a class="action" href="{{p}}contact.html"><span class="a-ico">{I['wrench']}</span><span><strong>Book a repair or tune-up</strong><small>Pick a time online. Confirmed by text.</small></span>{I['arrow']}</a>
<a class="action" href="{{p}}heat-pump-installation-ottawa.html"><span class="a-ico">{I['leaf']}</span><span><strong>Thinking about a heat pump?</strong><small>Free in-home quote and rebate check.</small></span>{I['arrow']}</a>
</div></section>

<section class="stats"><div class="wrap">
<div><strong>15+</strong><span>years keeping Ottawa warm</span></div>
<div><strong>6,200+</strong><span>homes serviced</span></div>
<div><strong>Same day</strong><span>on most no-heat calls</span></div>
<div><strong>10-year</strong><span>parts &amp; labour warranty on new systems</span></div>
</div></section>

<section class="block"><div class="wrap">
<div class="sec-head"><p class="eyebrow">What we do</p><h2>Heating and cooling for every season</h2>
<p>One local team for everything from a $150 repair to a complete system upgrade.</p></div>
<div class="svc-grid">{svc_cards}</div>
</div></section>

<section class="block tint"><div class="wrap split">
<div class="split-img">{img("ductless", (640, 1000), "Ductless heat pump head mounted in a bright living room", sizes="(max-width:900px) 100vw, 480px", ratio=(4, 5))}
<div class="float-card"><strong>Up to 40%</strong><span>lower heating bills with a dual-fuel heat pump*</span></div></div>
<div>
<p class="eyebrow">Heat pumps, rebates &amp; financing</p>
<h2>Cut your heating bill without freezing in February</h2>
<p>A cold-climate heat pump heats and cools your home on electricity, and it can run alongside your existing furnace for the coldest nights. We do the math for your house before you spend a dollar.</p>
<ul class="ticks lg">
<li>{I['check']} <span><strong>Proper sizing:</strong> a room-by-room heat-loss calculation, not a guess from square footage</span></li>
<li>{I['check']} <span><strong>Rebate help:</strong> we check current federal, provincial and utility programs and handle the paperwork</span></li>
<li>{I['check']} <span><strong>Financing:</strong> monthly payments on approved credit, shown next to the upfront price</span></li>
</ul>
<div class="ctas"><a class="btn btn-lg" href="{{p}}heat-pump-installation-ottawa.html">Explore heat pumps</a><a class="btn btn-lg btn-ghost" href="{{p}}contact.html">Book a free quote</a></div>
<p class="fine">*Typical range for a gas-heated Ottawa home switching most of its heating to a heat pump. Your savings depend on your home and energy prices.</p>
</div></div></section>

<section class="block"><div class="wrap">
<div class="sec-head center"><p class="eyebrow">How it works</p><h2>Booking a visit is easy</h2></div>
<ol class="process">
<li><span class="p-ico">{I['calendar']}</span><strong>Book online or call</strong><p>We ask a few questions so the technician arrives with the right parts.</p></li>
<li><span class="p-ico">{I['user']}</span><strong>We arrive on time</strong><p>A text when the tech is on the way, with their name and photo.</p></li>
<li><span class="p-ico">{I['doc']}</span><strong>Diagnosis &amp; firm price</strong><p>The problem in plain English and a fixed price before we touch anything.</p></li>
<li><span class="p-ico">{I['home']}</span><strong>Fixed, tested, tidy</strong><p>Drop cloths down, old parts removed and a written summary of the visit.</p></li>
</ol></div></section>

<section class="block dark"><div class="wrap split rev">
<div>
<p class="eyebrow light">Why Ashgrove</p>
<h2>The heating company that tells you the truth</h2>
<p>Our technicians aren't paid on commission. Their job is to find the real problem and give you options, which usually means a repair, not a sales pitch.</p>
<div class="why">
<div>{I['dollar']}<strong>Upfront pricing</strong><span>The quote is the price. No surprise line items.</span></div>
<div>{I['wrench']}<strong>Repair-first advice</strong><span>If a $200 part fixes it, we won't sell you a $6,000 furnace.</span></div>
<div>{I['snow']}<strong>Built for −30°C</strong><span>Equipment sized for real Ottawa winters.</span></div>
<div>{I['shield']}<strong>Warranty you can use</strong><span>2 years on repair labour, 10 years on new systems.</span></div>
</div></div>
<div class="split-img">{img("cozy", (640, 1000), "Family warming their feet by the fire in a cozy living room", sizes="(max-width:900px) 100vw, 520px", ratio=(16, 9))}</div>
</div></section>

{reviews_html()}

<section class="block tint"><div class="wrap">
<div class="sec-head center"><p class="eyebrow">Maintenance plans</p><h2>Skip the January breakdown</h2>
<p>A yearly tune-up catches the small problems before they leave you without heat.</p></div>
<div class="plans">
<div class="plan"><h3>Furnace Care</h3><p class="price">$14<span>/month</span></p>
<ul class="ticks"><li>{I['check']} Annual furnace tune-up &amp; safety check</li><li>{I['check']} Carbon monoxide test</li><li>{I['check']} Priority booking</li><li>{I['check']} 10% off repairs</li></ul>
<a class="btn btn-ghost btn-block" href="{{p}}contact.html">Choose Furnace Care</a></div>
<div class="plan featured"><span class="tag">Most popular</span><h3>Year-Round Care</h3><p class="price">$22<span>/month</span></p>
<ul class="ticks"><li>{I['check']} <span>Furnace <em>and</em> AC or heat pump tune-ups</span></li><li>{I['check']} Carbon monoxide test</li><li>{I['check']} Priority booking, no overtime fees</li><li>{I['check']} 15% off repairs</li></ul>
<a class="btn btn-block" href="{{p}}contact.html">Choose Year-Round Care</a></div>
</div></div></section>

<section class="block" id="areas"><div class="wrap split areas-split">
<div><p class="eyebrow">Service area</p><h2>Proudly serving all of Ottawa</h2>
<p>Our technicians are spread across the city, so there's usually one close by. Not sure if we cover your street? Give us a call.</p>
<a class="btn btn-ghost" href="tel:{BIZ['tel']}">{I['phone']} {BIZ['phone']}</a></div>
<ul class="chips">{"".join(f"<li>{I['pin']}{a}</li>" for a in AREAS)}</ul>
</div></section>

<section class="block tint"><div class="wrap split faq-split">
<div><p class="eyebrow">FAQ</p><h2>Common questions</h2><p>Can't find your answer? Call <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a> and talk to a real person.</p>
<p class="brands"><strong>We service all major brands,</strong> including Lennox, Carrier, Trane, Goodman, Mitsubishi, Daikin, Rheem and Napoleon.</p></div>
{faq_html(home_faqs)}
</div></section>
{emergency_band()}''',
    schemas=[BUSINESS_LD, faq_ld(home_faqs)], hero_preload=("hero", (800, 1440))))

# ================= Services =================
pages.append(page("services.html",
    "Heating & Cooling Services in Ottawa | Ashgrove Heating & Air",
    "Furnace repair and replacement, heat pump installation, central air conditioning and maintenance plans for Ottawa homes. See what's included and typical prices.",
    page_hero([("index.html", "Home"), ("services.html", "Services")], "Heating and cooling services",
              "Everything a typical Ottawa home needs to stay warm in January and cool in July.", "gauges")
    + f'''<section class="block"><div class="wrap with-side">
<div class="prose">
<div class="svc-row" id="furnace">{img("furnace", (480, 800), "Technician repairing furnace components", sizes="(max-width:700px) 100vw, 300px", ratio=(4, 3))}
<div><h2>Furnace repair and replacement</h2>
<p>We service all major gas furnace brands. Most no-heat problems come down to a short list of parts: igniters, flame sensors, pressure switches and blower motors. Our technicians carry the common ones, so most repairs are finished on the first visit.</p>
<p>If replacement makes more sense, we'll do a proper heat-loss calculation and quote two or three options at different price points. <a href="furnace-repair-ottawa.html">More about furnace repair →</a></p></div></div>
<div class="svc-row" id="heat-pumps">{img("heatpump", (480, 800), "Outdoor heat pump unit beside a modern home", sizes="(max-width:700px) 100vw, 300px", ratio=(4, 3))}
<div><h2>Heat pump installation</h2>
<p>Cold-climate air-source heat pumps can heat and cool your home and cut your gas bill. We'll tell you honestly whether one suits your house, what it will cost and which rebates may apply. <a href="heat-pump-installation-ottawa.html">More about heat pumps →</a></p></div></div>
<div class="svc-row" id="ac">{img("ac", (480, 800), "Air conditioner condenser beside a house", sizes="(max-width:700px) 100vw, 300px", ratio=(4, 3))}
<div><h2>Air conditioning</h2>
<p>Central AC installation, repairs and spring tune-ups. If you're replacing an older AC, it's worth asking about a heat pump instead. It cools the same way and heats too.</p></div></div>
<div class="svc-row" id="maintenance">{img("thermostat", (480, 800), "Homeowner adjusting a smart thermostat", sizes="(max-width:700px) 100vw, 300px", ratio=(4, 3))}
<div><h2>Maintenance plans</h2>
<p>A yearly tune-up catches the small problems that turn into January breakdowns.</p>
<table class="prices">
<thead><tr><th>Plan</th><th>Includes</th><th>Price</th></tr></thead>
<tbody>
<tr><td>Furnace Care</td><td>Annual furnace tune-up and safety check, priority booking, 10% off repairs</td><td>$14/month</td></tr>
<tr><td>Year-Round Care</td><td>Furnace and AC tune-ups, priority booking, no overtime fees, 15% off repairs</td><td>$22/month</td></tr>
</tbody></table></div></div>
<p class="note">Prices on this concept site are illustrative only.</p>
</div>
{sidebar("quote-svc")}
</div></section>
{reviews_html()}
{emergency_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("services.html", "Services")]),
             {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "provider": {"@id": BASE + "/#business"}, "areaServed": "Ottawa, ON"}}
                 for i, n in enumerate(["Furnace repair and replacement", "Heat pump installation", "Air conditioning", "HVAC maintenance plans"])]}],
    hero_preload=("gauges", (800, 1440))))

# ================= Heat pump page =================
hp_faqs = [
    ("How much does a heat pump cost in Ottawa?", "For a typical detached home, a ducted cold-climate heat pump usually costs roughly $9,000 to $16,000 installed, before any rebates. It depends on the size of the home, the ductwork and whether the electrical panel needs work. We give a fixed quote after a home visit."),
    ("Will a heat pump keep my house warm at −25°C?", "A properly sized cold-climate model keeps producing heat at those temperatures, just less efficiently. Most Ottawa installs keep the existing furnace or add electric backup for the handful of very cold nights."),
    ("Can I keep my gas furnace?", "Yes. A dual-fuel (hybrid) setup uses the heat pump most of the year and switches to the furnace when it's very cold. It's the most common choice for Ottawa homes that already have a working furnace."),
    ("Are there rebates?", "Federal, provincial and utility programs change often, so we check what's currently available for your home during the quote visit and help you with the application."),
]
pages.append(page("heat-pump-installation-ottawa.html",
    "Heat Pump Installation in Ottawa | Cold-Climate Experts | Ashgrove",
    "Cold-climate heat pump installation in Ottawa. Proper sizing, dual-fuel options, honest pricing and rebate help. Book a free in-home quote.",
    page_hero([("index.html", "Home"), ("services.html", "Services"), ("heat-pump-installation-ottawa.html", "Heat pump installation")],
              "Heat pump installation in Ottawa", "Cold-climate heat pumps, sized for your home and set up to handle a real Ottawa winter.", "heatpump")
    + f'''<section class="block"><div class="wrap with-side">
<div class="prose">
<h2>Is a heat pump right for your home?</h2>
<p>A heat pump moves heat instead of burning fuel to make it. In summer it works like an air conditioner. In winter it runs in reverse and pulls heat from the outdoor air, even when it's well below freezing.</p>
<p>For most Ottawa homes the real question isn't whether a heat pump works. It's which setup makes sense for your house and budget:</p>
<div class="opt-grid">
<div class="opt"><span class="tag">Most popular</span><h3>Dual-fuel</h3><p>A heat pump plus your existing gas furnace for the coldest days. Best when the furnace still has life left.</p></div>
<div class="opt"><h3>All-electric</h3><p>A cold-climate heat pump with electric backup heat, for homes without gas or owners who want to drop it.</p></div>
<div class="opt"><h3>Ductless mini-split</h3><p>For homes without ductwork, additions, or a cold room over the garage.</p></div>
</div>
<h2>What our installation includes</h2>
<ul class="ticks lg">
<li>{I['check']} <span>An in-home heat-loss calculation, so the unit is sized to your house, not guessed from the square footage</span></li>
<li>{I['check']} <span>A duct and electrical panel check, flagged before you sign, not after</span></li>
<li>{I['check']} <span>Installation by licensed technicians, plus thermostat setup and a walkthrough</span></li>
<li>{I['check']} <span>Help finding and applying for current rebate programs</span></li>
<li>{I['check']} <span>A first-year check-up visit and a 10-year parts &amp; labour warranty</span></li>
</ul>
<h2>Typical project timeline</h2>
<ol class="timeline">
<li><strong>Home visit (1 hour)</strong><span>Measurements, a look at the ducts and panel, and your goals.</span></li>
<li><strong>Written quote within 2 days</strong><span>Two or three options with running-cost estimates.</span></li>
<li><strong>Install day</strong><span>Most ducted installs take one to two days.</span></li>
<li><strong>Follow-up</strong><span>We check performance after the first cold snap.</span></li>
</ol>
<h2>Heat pump questions we hear most</h2>
{faq_html(hp_faqs)}
{HP_GUIDE_LINK}
</div>
{sidebar("quote-hp")}
</div></section>
{reviews_html()}
{emergency_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("services.html", "Services"), ("heat-pump-installation-ottawa.html", "Heat pump installation")]),
             {"@context": "https://schema.org", "@type": "Service", "serviceType": "Heat pump installation", "name": "Heat pump installation in Ottawa",
              "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "City", "name": "Ottawa"}},
             faq_ld(hp_faqs)], hero_preload=("heatpump", (800, 1440))))

# ================= Furnace repair page =================
fr_faqs = [
    ("Why is my furnace running but blowing cold air?", "Common causes are a dirty flame sensor, a failed igniter, a clogged filter causing the furnace to overheat and shut off its burners, or a thermostat set to 'fan on'. Check the filter and thermostat first; if that doesn't fix it, call us."),
    ("How much does furnace repair cost?", "Most common repairs, such as a flame sensor, igniter or pressure switch, run roughly $150 to $450 including the diagnostic. Blower motors and control boards cost more. You get the exact price before we start."),
    ("Is it safe to keep resetting my furnace?", "No. If it keeps locking out, something is wrong, and repeated resets can mask a safety problem. If you ever smell gas, leave the house and call your gas utility's emergency line first."),
]
pages.append(page("furnace-repair-ottawa.html",
    "Furnace Repair in Ottawa | Same-Day No-Heat Service | Ashgrove",
    "Fast furnace repair in Ottawa. Same-day service on most no-heat calls, upfront prices, all major brands. Call (613) 555-0142, 24/7 in heating season.",
    page_hero([("index.html", "Home"), ("services.html", "Services"), ("furnace-repair-ottawa.html", "Furnace repair")],
              "Furnace repair in Ottawa", "No heat? We prioritize no-heat calls 24/7 during the heating season, and most are fixed on the first visit.", "furnace")
    + f'''<section class="block"><div class="wrap with-side">
<div class="prose">
<h2>Before you call: three quick checks</h2>
<div class="checks">
<div><span>1</span><strong>Thermostat</strong><p>Set to "Heat", a few degrees above room temperature, with fresh batteries.</p></div>
<div><span>2</span><strong>Filter</strong><p>A clogged filter can make the furnace overheat and shut itself off. Swap it if it's grey.</p></div>
<div><span>3</span><strong>Power switch</strong><p>The light-style switch near the furnace should be on, and the breaker shouldn't be tripped.</p></div>
</div>
<p>Still nothing? Call us. Don't keep resetting it.</p>
<h2>Problems we fix every week</h2>
<ul class="ticks two">
<li>{I['check']} Furnace won't ignite or keeps clicking</li>
<li>{I['check']} Burners light, then shut off (often the flame sensor)</li>
<li>{I['check']} Blowing cold air</li>
<li>{I['check']} Loud banging, squealing or rattling</li>
<li>{I['check']} Short cycling: on and off constantly</li>
<li>{I['check']} Error codes or a blinking status light</li>
</ul>
<div class="callout"><h2>Repair or replace?</h2>
<p>We'll give you our honest opinion, with numbers. As a rough guide:</p>
<ul><li><strong>Repair</strong> if the furnace is under ~15 years old and the fix is a small fraction of a new unit.</li>
<li><strong>Consider replacing</strong> if it's 18+ years old, needs a major part, or has needed several repairs in two winters.</li></ul>
<p>Thinking about replacing? Ask about a <a href="heat-pump-installation-ottawa.html">heat pump or dual-fuel system</a>.</p></div>
<h2>Furnace repair FAQ</h2>
{faq_html(fr_faqs)}
</div>
{sidebar("quote-fr")}
</div></section>
{reviews_html()}
{emergency_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("services.html", "Services"), ("furnace-repair-ottawa.html", "Furnace repair")]),
             {"@context": "https://schema.org", "@type": "Service", "serviceType": "Furnace repair", "name": "Furnace repair in Ottawa",
              "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "City", "name": "Ottawa"}},
             faq_ld(fr_faqs)], hero_preload=("furnace", (800, 1440))))

# ================= About =================
pages.append(page("about.html",
    "About Ashgrove Heating & Air | Ottawa HVAC Company",
    "Ashgrove Heating & Air is an Ottawa heating and cooling company built on upfront prices, repair-first advice and tidy work. Meet the team's approach.",
    page_hero([("index.html", "Home"), ("about.html", "About")], "A heating company that tells you the truth",
              "Local, independent and not paid on commission, since 2009.", "cozy", ctas=False)
    + f'''<section class="block"><div class="wrap split">
<div class="prose">
<p class="lead-p">Ashgrove started with a simple frustration: too many homeowners were being sold new furnaces they didn't need. A cracked igniter would become a $7,000 replacement because that's what paid the best commission.</p>
<p>We work differently. Our technicians aren't paid on commission. Their job is to find the real problem, explain it in plain English and give you options. Sometimes that means a new system. More often it means a $180 part and a clean filter.</p>
<h2>What you can expect from us</h2>
<ul class="ticks lg">
<li>{I['check']} <span><strong>A firm price before work starts.</strong> If we find something else, we stop and ask.</span></li>
<li>{I['check']} <span><strong>Licensed, background-checked technicians</strong> who wear boot covers and use drop cloths.</span></li>
<li>{I['check']} <span><strong>A short written summary</strong> of every visit: what we found, what we did and what to watch for.</span></li>
<li>{I['check']} <span><strong>A phone that gets answered,</strong> by a person, including on cold January nights.</span></li>
</ul>
<h2>Where we work</h2>
<p>We're an Ottawa company serving homes from Kanata and Stittsville to Orléans, and from Manotick up to Centretown. See the full list in our <a href="index.html#areas">service areas</a>.</p>
</div>
<div class="about-side">
<div class="stats stack">
<div><strong>15+</strong><span>years in Ottawa</span></div>
<div><strong>6,200+</strong><span>homes serviced</span></div>
<div><strong>{RATING[0]}★</strong><span>from {RATING[1]} reviews</span></div></div>
{img("gauges", (800, 1440), "Technician checking refrigerant pressure on an outdoor unit", sizes="(max-width:900px) 100vw, 480px", ratio=(3, 2))}
</div></div></section>
{reviews_html()}
{emergency_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("about.html", "About")])], hero_preload=("cozy", (800, 1440))))

# ================= Contact =================
pages.append(page("contact.html",
    "Contact Ashgrove Heating & Air | Book Service in Ottawa",
    "Book furnace, heat pump or AC service in Ottawa. Call (613) 555-0142 or request a free quote online. 24/7 no-heat calls in heating season.",
    page_hero([("index.html", "Home"), ("contact.html", "Contact")], "Book a visit or request a quote",
              "No heat right now? Call us. It's the fastest way to reach a technician.", "hero")
    + f'''<section class="block"><div class="wrap with-side contact-grid">
{quote_form("quote", "Tell us what you need", "We'll call you back to confirm a time, usually within the hour.")}
<aside class="side">
<div class="side-card"><p class="f-title">Reach us directly</p>
<ul class="f-contact dark">
<li>{I['phone']}<a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></li>
<li>{I['doc']}<a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
<li>{I['clock']}<span>{BIZ['weekday']}<br>{BIZ['sat']}<br>{BIZ['emerg']}</span></li>
<li>{I['pin']}<span>All of Ottawa, including {", ".join(AREAS[:6])} and more</span></li></ul></div>
<div class="side-card warn"><p class="f-title">Smell gas?</p><p>Leave the house first, then call your gas utility's emergency line from outside. Don't use light switches or phones indoors.</p></div>
</aside>
</div></section>''',
    schemas=[crumbs_ld([("", "Home"), ("contact.html", "Contact")]), BUSINESS_LD], hero_preload=("hero", (800, 1440))))

# ================= Blog =================
POSTS = [("heat-pump-vs-furnace-ottawa.html", "Heat pump or furnace? What actually makes sense in Ottawa",
          "A plain-English comparison of costs, comfort and cold-weather performance for Ottawa homes.", "heatpump")]
posts_html = "".join(f'''<a class="post-card" href="{u}">{img(ph, (480, 800), "", sizes="(max-width:640px) 100vw, 360px", ratio=(4, 3))}
<span><small>Heat pumps · 8 min read</small><strong>{t}</strong><span>{d}</span></span></a>''' for u, t, d, ph in POSTS if (ROOT / "posts" / u).exists())
pages.append(page("blog/index.html",
    "Home Heating & Cooling Advice for Ottawa | Ashgrove Heating & Air",
    "Plain-English advice on furnaces, heat pumps and air conditioning for Ottawa homeowners, from the Ashgrove Heating & Air team.",
    page_hero([("index.html", "Home"), ("blog/", "Advice")], "Heating and cooling advice",
              "Straight answers to the questions Ottawa homeowners ask us most.", "thermostat", ctas=False)
    + f'<section class="block"><div class="wrap"><div class="post-grid">{posts_html or "<p>Articles coming soon.</p>"}</div></div></section>',
    schemas=[crumbs_ld([("", "Home"), ("blog/", "Advice")])], prefix="../", hero_preload=("thermostat", (800, 1440))))

for u, t, d, ph in POSTS:
    src = ROOT / "posts" / u
    if src.exists():
        pages.append(page("blog/" + u, t + " | Ashgrove Heating & Air", d,
            page_hero([("index.html", "Home"), ("blog/", "Advice"), ("blog/" + u, t)], t, d, ph, ctas=False)
            + f'<article class="block"><div class="wrap with-side"><div class="prose">{src.read_text(encoding="utf-8")}</div>{sidebar("quote-post")}</div></article>{emergency_band()}',
            schemas=[crumbs_ld([("", "Home"), ("blog/", "Advice"), ("blog/" + u, t)]),
                     {"@context": "https://schema.org", "@type": "BlogPosting", "headline": t, "description": d,
                      "datePublished": TODAY, "author": {"@type": "Organization", "name": BIZ["name"]},
                      "publisher": {"@id": BASE + "/#business"}, "mainEntityOfPage": BASE + "/blog/" + u,
                      "image": BASE + "/assets/og.png"}], prefix="../", hero_preload=(ph, (800, 1440))))

# ================= 404 =================
page("404.html", "Page not found | Ashgrove Heating & Air", "That page doesn't exist.",
     '''<section class="block"><div class="wrap prose"><h1>That page doesn't exist</h1>
<p>Try the <a href="/ashgrove-heating/">home page</a> or <a href="/ashgrove-heating/contact.html">book a visit</a>.</p></div></section>''',
     prefix="/ashgrove-heating/")

# ================= Static extras =================
if (OUT / "assets").exists():
    shutil.rmtree(OUT / "assets")
shutil.copytree(ROOT / "assets", OUT / "assets")
shutil.copy(ROOT.parent / "_fonts" / "plus-jakarta-sans-latin-wght-normal.woff2", OUT / "assets" / "jakarta.woff2")
(OUT / "assets" / "logo.svg").write_text(LOGO.replace(' aria-hidden="true"', ' xmlns="http://www.w3.org/2000/svg"'), encoding="utf-8")

urls = "".join(f"<url><loc>{BASE}/{'' if p == 'index.html' else p.replace('index.html', '')}</loc><lastmod>{TODAY}</lastmod></url>" for p in pages)
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                 + urls + "</urlset>\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built {len(pages)} pages to {OUT} (base {BASE})")
