"""Build the Ashgrove Heating & Air concept site into ./site/.

Usage:  python build.py [BASE_URL]
BASE_URL defaults to the GitHub Pages URL below; change it once the
GitHub username is known. Everything else is static.
"""
import json, shutil, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"
BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://USERNAME.github.io/ashgrove-heating").rstrip("/")
TODAY = date.today().isoformat()

BIZ = {
    "name": "Ashgrove Heating & Air",
    "phone": "(613) 555-0142",
    "tel": "+16135550142",
    "email": "hello@example.com",
    "hours": "Mon–Fri 7am–7pm · Sat 8am–4pm · 24/7 no-heat emergencies",
}

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#12324f"/>'
        '<path d="M20 7c4 6 9 9 9 16a9 9 0 0 1-18 0c0-4 2-6 4-8 0 3 1 5 3 6-1-6 0-10 2-14z" fill="#d9631c"/>'
        '<path d="M20 22c2 2 4 3 4 6a4 4 0 0 1-8 0c0-2 2-4 4-6z" fill="#fff"/></svg>')

ICONS = {
    "flame": '<svg class="icon" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#fdeee3"/><path d="M24 10c4 6 9 9 9 16a9 9 0 0 1-18 0c0-4 2-6 4-8 0 3 1 5 3 6-1-6 0-10 2-14z" fill="#b4470c"/></svg>',
    "pump": '<svg class="icon" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#e6eef6"/><rect x="11" y="14" width="26" height="20" rx="3" fill="#12324f"/><circle cx="21" cy="24" r="6" fill="none" stroke="#fff" stroke-width="2"/><path d="M21 18v12M15 24h12" stroke="#fff" stroke-width="1.5"/><rect x="30" y="18" width="4" height="12" rx="1" fill="#d9631c"/></svg>',
    "snow": '<svg class="icon" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#e6eef6"/><path d="M24 11v26M13 17.5l22 13M13 30.5l22-13" stroke="#1d4a72" stroke-width="2.5" stroke-linecap="round"/></svg>',
    "wrench": '<svg class="icon" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="24" fill="#fdeee3"/><path d="M30 12a7 7 0 0 0-8 9L13 30a2.5 2.5 0 0 0 4 4l9-9a7 7 0 0 0 9-8l-4 4-4-1-1-4z" fill="#b4470c"/></svg>',
}

HERO_ART = '''<svg class="hero-art" viewBox="0 0 400 320" role="img" aria-label="Illustration of a house with a heat pump unit outside">
<rect x="0" y="270" width="400" height="50" fill="#dfe8f0"/>
<path d="M70 150 200 60l130 90v120H70z" fill="#fff" stroke="#12324f" stroke-width="5"/>
<path d="M50 160 200 52l150 108" fill="none" stroke="#12324f" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="175" y="190" width="50" height="80" rx="4" fill="#12324f"/>
<rect x="100" y="170" width="50" height="45" rx="4" fill="#cfe0ef" stroke="#12324f" stroke-width="4"/>
<rect x="250" y="170" width="50" height="45" rx="4" fill="#cfe0ef" stroke="#12324f" stroke-width="4"/>
<rect x="300" y="225" width="78" height="52" rx="6" fill="#f4f7fa" stroke="#12324f" stroke-width="4"/>
<circle cx="328" cy="251" r="17" fill="none" stroke="#12324f" stroke-width="4"/>
<path d="M328 236v30M313 251h30" stroke="#d9631c" stroke-width="3"/>
<rect x="356" y="235" width="12" height="32" rx="2" fill="#d9631c"/>
<path d="M265 40c6 10 14 14 14 25a14 14 0 0 1-28 0c0-6 3-9 6-12 0 5 2 8 4 9-1-9 1-15 4-22z" fill="#d9631c"/>
</svg>'''

NAV = [("index.html", "Home"), ("services.html", "Services"), ("heat-pump-installation-ottawa.html", "Heat Pumps"),
       ("about.html", "About"), ("blog/", "Advice"), ("contact.html", "Contact")]

AREAS = ["Kanata", "Barrhaven", "Nepean", "Orléans", "Stittsville", "Westboro", "The Glebe", "Alta Vista",
         "Manotick", "Riverside South", "Gloucester", "Centretown"]

BUSINESS_LD = {
    "@context": "https://schema.org",
    "@type": "HVACBusiness",
    "@id": BASE + "/#business",
    "name": BIZ["name"],
    "url": BASE + "/",
    "telephone": BIZ["tel"],
    "email": BIZ["email"],
    "image": BASE + "/assets/og.png",
    "logo": BASE + "/assets/logo.svg",
    "priceRange": "$$",
    "description": "Furnace, heat pump and air conditioning installation, repair and maintenance across Ottawa. (Concept project: fictional business.)",
    "address": {"@type": "PostalAddress", "addressLocality": "Ottawa", "addressRegion": "ON", "addressCountry": "CA"},
    "areaServed": [{"@type": "City", "name": "Ottawa"}] + [{"@type": "Place", "name": f"{a}, Ottawa"} for a in AREAS],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "16:00"},
    ],
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


def page(path, title, desc, body, schemas=(), prefix=""):
    """prefix = '../' for pages in subfolders."""
    canonical = BASE + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    nav_items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if (href == path or (href == "blog/" and path.startswith("blog/"))) else ""
        nav_items.append(f'<li><a href="{prefix}{href}"{cur}>{label}</a></li>')
    nav = "".join(nav_items)
    schema_html = "\n".join(ld(s) for s in schemas)
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
<meta name="theme-color" content="#12324f">
<link rel="icon" href="{prefix}assets/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="{prefix}assets/style.css">
{schema_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><span>Serving Ottawa and nearby · {BIZ['hours'].split(' · ')[2]}</span><a href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a></div></div>
<header class="site"><div class="wrap">
<a class="brand" href="{prefix}index.html">{LOGO}<span>Ashgrove Heating &amp; Air</span></a>
<nav class="main" aria-label="Main"><ul>{nav}</ul></nav>
<details class="menu"><summary>Menu</summary><nav aria-label="Mobile"><ul>{nav}</ul></nav></details>
<a class="btn" href="{prefix}contact.html">Book a visit</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<div class="grid c3">
<div><h2>Ashgrove Heating &amp; Air</h2><p>Furnaces, heat pumps and air conditioning for Ottawa homes. Licensed gas technicians, upfront prices, tidy work.</p></div>
<div><h2>Services</h2><ul>
<li><a href="{prefix}furnace-repair-ottawa.html">Furnace repair</a></li>
<li><a href="{prefix}heat-pump-installation-ottawa.html">Heat pump installation</a></li>
<li><a href="{prefix}services.html#ac">Air conditioning</a></li>
<li><a href="{prefix}services.html#maintenance">Maintenance plans</a></li></ul></div>
<div><h2>Contact</h2><ul>
<li><a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></li>
<li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
<li>{BIZ['hours'].split(' · ')[0]}</li><li>{BIZ['hours'].split(' · ')[1]}</li></ul></div>
</div>
<p class="concept">Concept project by Liam Curran – fictional business. Names, phone numbers and prices are illustrative only.</p>
</div></footer>
<script src="{prefix}assets/site.js" defer></script>
</body>
</html>
'''
    dest = OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    return path


def cta_band(prefix=""):
    return f'''<section class="cta-band"><div class="wrap">
<div><h2>No heat? Strange noise? Planning a heat pump?</h2><p>Tell us what's going on and we'll give you a straight answer and a firm price.</p></div>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a><a class="btn alt" style="border-color:#fff;color:#fff!important" href="{prefix}contact.html">Request a quote</a></div>
</div></section>'''


pages = []
HP_GUIDE_LINK = ('<p>Want more detail? Read our guide: <a href="blog/heat-pump-vs-furnace-ottawa.html">'
                 'Heat pump or furnace? What actually makes sense in Ottawa</a>.</p>'
                 if (ROOT / "posts" / "heat-pump-vs-furnace-ottawa.html").exists() else "")

# ---------------- Home ----------------
home_faqs = [
    ("Do you charge for estimates?", "Quotes for new furnaces, heat pumps and air conditioners are free. For repairs there's a flat diagnostic fee, and we tell you the repair price before any work starts."),
    ("How fast can you come when the heat is out?", "No-heat calls get priority, 24/7 during the heating season. Most are reached the same day."),
    ("Should I repair my furnace or replace it?", "If the furnace is under about 15 years old and the repair is a fraction of a new unit, repair usually wins. We'll show you the numbers both ways and let you decide."),
    ("Do heat pumps work in an Ottawa winter?", "Modern cold-climate heat pumps keep heating well below −20°C. Most Ottawa homes pair one with a furnace or electric backup for the coldest nights."),
]
pages.append(page("index.html",
    "Ashgrove Heating & Air | Furnace, Heat Pump & AC Service in Ottawa",
    "Furnace repair, heat pump installation and air conditioning across Ottawa. Upfront prices, licensed technicians and 24/7 no-heat service. Call (613) 555-0142.",
    f'''<section class="hero"><div class="wrap">
<div>
<h1>Ottawa furnace, heat pump and AC service, done properly the first time</h1>
<p class="lede">From a furnace that quit at 2am to a full heat pump upgrade, we diagnose it honestly, quote it upfront and leave your home cleaner than we found it.</p>
<div class="ctas"><a class="btn" href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a><a class="btn alt" href="contact.html">Request a free quote</a></div>
<ul class="trust"><li>Licensed gas technicians</li><li>Price before work starts</li><li>24/7 no-heat calls</li></ul>
</div>
{HERO_ART}
</div></section>

<section class="block"><div class="wrap">
<h2>What we do</h2>
<div class="grid c4">
<div class="card">{ICONS['flame']}<h3>Furnace repair &amp; replacement</h3><p>Same-day diagnosis on most no-heat calls, and honest advice on whether to repair or replace.</p><a class="more" href="furnace-repair-ottawa.html">Furnace repair →</a></div>
<div class="card">{ICONS['pump']}<h3>Heat pumps</h3><p>Cold-climate heat pumps sized for your actual home, not a rule of thumb.</p><a class="more" href="heat-pump-installation-ottawa.html">Heat pump installation →</a></div>
<div class="card">{ICONS['snow']}<h3>Air conditioning</h3><p>Central AC installs, repairs and tune-ups before the July heat arrives.</p><a class="more" href="services.html#ac">Air conditioning →</a></div>
<div class="card">{ICONS['wrench']}<h3>Maintenance plans</h3><p>One furnace and one AC tune-up a year, priority booking and no overtime fees.</p><a class="more" href="services.html#maintenance">Maintenance plans →</a></div>
</div></div></section>

<section class="block alt"><div class="wrap grid c2" style="align-items:start">
<div><h2>How a visit works</h2>
<ol class="steps">
<li><strong>You call or book online.</strong> We ask a few questions so the technician shows up with the right parts.</li>
<li><strong>We diagnose and quote.</strong> You get the problem in plain English and a firm price before we touch anything.</li>
<li><strong>We fix it and clean up.</strong> Drop cloths down, old parts removed, and a short written summary of what we did.</li>
</ol></div>
<div><h2>Why Ottawa homeowners call us</h2>
<ul class="prose">
<li><strong>Upfront pricing.</strong> The quote is the price. No surprise line items on the invoice.</li>
<li><strong>Repair-first advice.</strong> If a $200 part fixes it, we won't sell you a $6,000 furnace.</li>
<li><strong>Built for Ottawa winters.</strong> We size equipment for −30°C nights, not a mild-climate spec sheet.</li>
<li><strong>Rebate help.</strong> We'll point you to the current heat pump rebate programs and help with the paperwork.</li>
</ul></div>
</div></section>

<section class="block"><div class="wrap">
<h2>Areas we serve</h2>
<p>We cover all of Ottawa and nearby communities, including:</p>
<ul class="areas">{"".join(f"<li>{a}</li>" for a in AREAS)}</ul>
</div></section>

<section class="block alt"><div class="wrap prose">
<h2>Common questions</h2>
{faq_html(home_faqs)}
</div></section>
{cta_band()}''',
    schemas=[BUSINESS_LD, faq_ld(home_faqs)]))

# ---------------- Services ----------------
pages.append(page("services.html",
    "Heating & Cooling Services in Ottawa | Ashgrove Heating & Air",
    "Furnace repair and replacement, heat pump installation, central air conditioning and maintenance plans for Ottawa homes. See what's included and typical prices.",
    f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> › Services</div>
<h1>Heating and cooling services</h1>
<p class="lede">Everything a typical Ottawa home needs to stay warm in January and cool in July.</p>
</div></section>

<section class="block"><div class="wrap prose">
<h2 id="furnace">Furnace repair and replacement</h2>
<p>We service all major gas furnace brands. Most no-heat problems come down to a short list of parts: igniters, flame sensors, pressure switches and blower motors. Our technicians carry the common ones, so most repairs are finished on the first visit.</p>
<p>If replacement makes more sense, we'll do a proper heat-loss calculation and quote two or three options at different price points. <a href="furnace-repair-ottawa.html">More about furnace repair →</a></p>

<h2 id="heat-pumps">Heat pump installation</h2>
<p>Cold-climate air-source heat pumps can heat and cool your home and cut your gas bill. We'll tell you honestly whether one suits your house, what it will cost and which rebates may apply. <a href="heat-pump-installation-ottawa.html">More about heat pumps →</a></p>

<h2 id="ac">Air conditioning</h2>
<p>Central AC installation, repairs and spring tune-ups. If you're replacing an older AC, it's worth asking about a heat pump instead. It cools the same way and heats too.</p>

<h2 id="maintenance">Maintenance plans</h2>
<p>A yearly tune-up catches the small problems that turn into January breakdowns.</p>
<table class="prices">
<thead><tr><th>Plan</th><th>Includes</th><th>Price</th></tr></thead>
<tbody>
<tr><td>Furnace Care</td><td>Annual furnace tune-up and safety check, priority booking</td><td>$14/month</td></tr>
<tr><td>Year-Round Care</td><td>Furnace and AC tune-ups, priority booking, no overtime fees, 10% off repairs</td><td>$22/month</td></tr>
</tbody></table>
<p class="note">Prices on this concept site are illustrative only.</p>
</div></section>
{cta_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("services.html", "Services")]),
             {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": n, "provider": {"@id": BASE + "/#business"}, "areaServed": "Ottawa, ON"}}
                 for i, n in enumerate(["Furnace repair and replacement", "Heat pump installation", "Air conditioning", "HVAC maintenance plans"])]}]))

# ---------------- Heat pump page ----------------
hp_faqs = [
    ("How much does a heat pump cost in Ottawa?", "For a typical detached home, a ducted cold-climate heat pump usually costs roughly $9,000 to $16,000 installed, before any rebates. It depends on the size of the home, the ductwork and whether the electrical panel needs work. We give a fixed quote after a home visit."),
    ("Will a heat pump keep my house warm at −25°C?", "A properly sized cold-climate model keeps producing heat at those temperatures, just less efficiently. Most Ottawa installs keep the existing furnace or add electric backup for the handful of very cold nights."),
    ("Can I keep my gas furnace?", "Yes. A dual-fuel (hybrid) setup uses the heat pump most of the year and switches to the furnace when it's very cold. It's the most common choice for Ottawa homes that already have a working furnace."),
    ("Are there rebates?", "Federal, provincial and utility programs change often, so we check what's currently available for your home during the quote visit and help you with the application."),
]
pages.append(page("heat-pump-installation-ottawa.html",
    "Heat Pump Installation in Ottawa | Cold-Climate Experts | Ashgrove",
    "Cold-climate heat pump installation in Ottawa. Proper sizing, dual-fuel options, honest pricing and rebate help. Book a free in-home quote.",
    f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> › <a href="services.html">Services</a> › Heat pump installation</div>
<h1>Heat pump installation in Ottawa</h1>
<p class="lede">Cold-climate heat pumps, sized for your home and set up to handle a real Ottawa winter.</p>
<div class="ctas" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="contact.html">Book a free quote</a><a class="btn alt" href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a></div>
</div></section>

<section class="block"><div class="wrap grid c2" style="align-items:start">
<div class="prose">
<h2>Is a heat pump right for your home?</h2>
<p>A heat pump moves heat instead of burning fuel to make it. In summer it works like an air conditioner. In winter it runs in reverse and pulls heat from the outdoor air, even when it's well below freezing.</p>
<p>For most Ottawa homes the real question isn't whether a heat pump works. It's which setup makes sense for your house and budget:</p>
<ul>
<li><strong>Dual-fuel:</strong> a heat pump plus your existing gas furnace for the coldest days. It's the most common choice when the furnace still has life left.</li>
<li><strong>All-electric:</strong> a cold-climate heat pump with electric backup heat. It suits homes without gas or owners who want to drop it.</li>
<li><strong>Ductless mini-split:</strong> for homes without ductwork, additions, or a cold room over the garage.</li>
</ul>
<h2>What our installation includes</h2>
<ul>
<li>An in-home heat-loss calculation, so the unit is sized to your house, not guessed from the square footage</li>
<li>A duct and electrical panel check, flagged before you sign, not after</li>
<li>Installation by licensed technicians, plus thermostat setup and a walkthrough of how to use it</li>
<li>Help finding and applying for current rebate programs</li>
<li>A first-year check-up visit</li>
</ul>
</div>
<div class="card">
<h2 style="font-size:1.3rem">Typical project timeline</h2>
<ol class="steps">
<li><strong>Home visit (1 hour).</strong> Measurements, a look at the ducts and panel, and your goals.</li>
<li><strong>Written quote within 2 days.</strong> Two or three options with running-cost estimates.</li>
<li><strong>Install day.</strong> Most ducted installs take one to two days.</li>
<li><strong>Follow-up.</strong> We check performance after the first cold snap.</li>
</ol>
</div>
</div></section>

<section class="block alt"><div class="wrap prose">
<h2>Heat pump questions we hear most</h2>
{faq_html(hp_faqs)}
{HP_GUIDE_LINK}
</div></section>
{cta_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("services.html", "Services"), ("heat-pump-installation-ottawa.html", "Heat pump installation")]),
             {"@context": "https://schema.org", "@type": "Service", "serviceType": "Heat pump installation", "name": "Heat pump installation in Ottawa",
              "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "City", "name": "Ottawa"}},
             faq_ld(hp_faqs)]))

# ---------------- Furnace repair page ----------------
fr_faqs = [
    ("Why is my furnace running but blowing cold air?", "Common causes are a dirty flame sensor, a failed igniter, a clogged filter causing the furnace to overheat and shut off its burners, or a thermostat set to 'fan on'. Check the filter and thermostat first; if that doesn't fix it, call us."),
    ("How much does furnace repair cost?", "Most common repairs, such as a flame sensor, igniter or pressure switch, run roughly $150 to $450 including the diagnostic. Blower motors and control boards cost more. You get the exact price before we start."),
    ("Is it safe to keep resetting my furnace?", "No. If it keeps locking out, something is wrong, and repeated resets can mask a safety problem. If you ever smell gas, leave the house and call your gas utility's emergency line first."),
]
pages.append(page("furnace-repair-ottawa.html",
    "Furnace Repair in Ottawa | Same-Day No-Heat Service | Ashgrove",
    "Fast furnace repair in Ottawa. Same-day service on most no-heat calls, upfront prices, all major brands. Call (613) 555-0142, 24/7 in heating season.",
    f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> › <a href="services.html">Services</a> › Furnace repair</div>
<h1>Furnace repair in Ottawa</h1>
<p class="lede">No heat? We prioritize no-heat calls 24/7 during the heating season, and most are fixed on the first visit.</p>
<div class="ctas" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="tel:{BIZ['tel']}">Call {BIZ['phone']}</a><a class="btn alt" href="contact.html">Book online</a></div>
</div></section>

<section class="block"><div class="wrap grid c2" style="align-items:start">
<div class="prose">
<h2>Before you call: three quick checks</h2>
<ol>
<li><strong>Thermostat:</strong> set to "Heat", a few degrees above room temperature, with fresh batteries.</li>
<li><strong>Filter:</strong> a clogged filter can make the furnace overheat and shut itself off. Swap it if it's grey.</li>
<li><strong>Power switch:</strong> the light-style switch near the furnace should be on, and the breaker shouldn't be tripped.</li>
</ol>
<p>Still nothing? Call us. Don't keep resetting it.</p>
<h2>Problems we fix every week</h2>
<ul>
<li>Furnace won't ignite or keeps clicking</li>
<li>Burners light, then shut off after a few seconds (often the flame sensor)</li>
<li>Blowing cold air</li>
<li>Loud banging, squealing or rattling</li>
<li>Short cycling: turning on and off constantly</li>
<li>Error codes or a blinking status light</li>
</ul>
</div>
<div class="card">
<h2 style="font-size:1.3rem">Repair or replace?</h2>
<p>We'll give you our honest opinion, with numbers. As a rough guide:</p>
<ul>
<li><strong>Repair</strong> if the furnace is under ~15 years old and the fix is a small fraction of a new unit.</li>
<li><strong>Consider replacing</strong> if it's 18+ years old, needs a major part, or has needed several repairs in two winters.</li>
</ul>
<p>Thinking about replacing? Ask about a <a href="heat-pump-installation-ottawa.html">heat pump or dual-fuel system</a>.</p>
</div>
</div></section>

<section class="block alt"><div class="wrap prose">
<h2>Furnace repair FAQ</h2>
{faq_html(fr_faqs)}
</div></section>
{cta_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("services.html", "Services"), ("furnace-repair-ottawa.html", "Furnace repair")]),
             {"@context": "https://schema.org", "@type": "Service", "serviceType": "Furnace repair", "name": "Furnace repair in Ottawa",
              "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "City", "name": "Ottawa"}},
             faq_ld(fr_faqs)]))

# ---------------- About ----------------
pages.append(page("about.html",
    "About Ashgrove Heating & Air | Ottawa HVAC Company",
    "Ashgrove Heating & Air is an Ottawa heating and cooling company built on upfront prices, repair-first advice and tidy work. Meet the team's approach.",
    f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> › About</div>
<h1>A heating company that tells you the truth</h1>
</div></section>
<section class="block"><div class="wrap prose">
<p>Ashgrove started with a simple frustration: too many homeowners were being sold new furnaces they didn't need. A cracked igniter would become a $7,000 replacement because that's what paid the best commission.</p>
<p>We work differently. Our technicians aren't paid on commission. Their job is to find the real problem, explain it in plain English and give you options. Sometimes that means a new system. More often it means a $180 part and a clean filter.</p>
<h2>What you can expect from us</h2>
<ul>
<li><strong>A firm price before work starts.</strong> If we find something else, we stop and ask.</li>
<li><strong>Licensed, background-checked technicians</strong> who wear boot covers and use drop cloths.</li>
<li><strong>A short written summary</strong> of every visit: what we found, what we did and what to watch for.</li>
<li><strong>A phone that gets answered,</strong> by a person, including on cold January nights.</li>
</ul>
<h2>Where we work</h2>
<p>We're an Ottawa company serving homes from Kanata and Stittsville to Orléans, and from Manotick up to Centretown. See the full list on our <a href="index.html#main">home page</a>.</p>
</div></section>
{cta_band()}''',
    schemas=[crumbs_ld([("", "Home"), ("about.html", "About")])]))

# ---------------- Contact ----------------
pages.append(page("contact.html",
    "Contact Ashgrove Heating & Air | Book Service in Ottawa",
    "Book furnace, heat pump or AC service in Ottawa. Call (613) 555-0142 or request a free quote online. 24/7 no-heat calls in heating season.",
    f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="index.html">Home</a> › Contact</div>
<h1>Book a visit or request a quote</h1>
<p class="lede">No heat right now? Call <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a>. It's the fastest way to reach us.</p>
</div></section>
<section class="block"><div class="wrap grid c2" style="align-items:start">
<form class="quote" id="quote" novalidate>
<div><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
<div><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
<div><label for="area">Neighbourhood</label><input id="area" name="area" placeholder="e.g. Barrhaven"></div>
<div><label for="need">What do you need?</label>
<select id="need" name="need"><option>Furnace repair</option><option>Heat pump quote</option><option>Furnace replacement quote</option><option>Air conditioning</option><option>Maintenance plan</option><option>Something else</option></select></div>
<div><label for="msg">Tell us a bit more</label><textarea id="msg" name="msg" rows="4"></textarea></div>
<button class="btn" type="submit">Send request</button>
<p class="form-msg note" id="form-msg" role="status">Thanks! This is a concept site, so nothing was actually sent. On a live site, this form would email the office and add the lead to a spreadsheet or CRM.</p>
</form>
<div class="card">
<h2 style="font-size:1.3rem">Reach us</h2>
<p><strong>Phone:</strong> <a href="tel:{BIZ['tel']}">{BIZ['phone']}</a><br>
<strong>Email:</strong> <a href="mailto:{BIZ['email']}">{BIZ['email']}</a></p>
<p><strong>Office hours</strong><br>{BIZ['hours'].split(' · ')[0]}<br>{BIZ['hours'].split(' · ')[1]}<br>{BIZ['hours'].split(' · ')[2]}</p>
<p><strong>Service area:</strong> all of Ottawa, including {", ".join(AREAS[:6])} and more.</p>
<p class="note">Smell gas? Leave the house first, then call your gas utility's emergency line from outside.</p>
</div>
</div></section>''',
    schemas=[crumbs_ld([("", "Home"), ("contact.html", "Contact")]), BUSINESS_LD]))

# ---------------- Blog index (posts added in Phase 4) ----------------
POSTS = [("heat-pump-vs-furnace-ottawa.html", "Heat pump or furnace? What actually makes sense in Ottawa",
          "A plain-English comparison of costs, comfort and cold-weather performance for Ottawa homes.")]
posts_html = "".join(f'<div class="card"><h2 style="font-size:1.2rem"><a href="{u}">{t}</a></h2><p>{d}</p></div>'
                     for u, t, d in POSTS if (ROOT / "posts" / u).exists())
pages.append(page("blog/index.html",
    "Home Heating & Cooling Advice for Ottawa | Ashgrove Heating & Air",
    "Plain-English advice on furnaces, heat pumps and air conditioning for Ottawa homeowners, from the Ashgrove Heating & Air team.",
    f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="../index.html">Home</a> › Advice</div>
<h1>Heating and cooling advice</h1>
<p class="lede">Straight answers to the questions Ottawa homeowners ask us most.</p>
</div></section>
<section class="block"><div class="wrap grid c2">{posts_html or '<p>Articles coming soon.</p>'}</div></section>''',
    schemas=[crumbs_ld([("", "Home"), ("blog/", "Advice")])], prefix="../"))

# Blog posts: body HTML fragments live in ./posts/<slug>.html (written in Phase 4)
for u, t, d in POSTS:
    src = ROOT / "posts" / u
    if src.exists():
        body = src.read_text(encoding="utf-8")
        pages.append(page("blog/" + u, t + " | Ashgrove Heating & Air", d,
            f'''<section class="page-hero"><div class="wrap">
<div class="crumbs"><a href="../index.html">Home</a> › <a href="index.html">Advice</a> › {t}</div>
<h1>{t}</h1></div></section>
<article class="block"><div class="wrap prose">{body}</div></article>{cta_band("../")}''',
            schemas=[crumbs_ld([("", "Home"), ("blog/", "Advice"), ("blog/" + u, t)]),
                     {"@context": "https://schema.org", "@type": "BlogPosting", "headline": t, "description": d,
                      "datePublished": TODAY, "author": {"@type": "Organization", "name": BIZ["name"]},
                      "publisher": {"@id": BASE + "/#business"}, "mainEntityOfPage": BASE + "/blog/" + u,
                      "image": BASE + "/assets/og.png"}], prefix="../"))

# ---------------- 404 ----------------
page("404.html", "Page not found | Ashgrove Heating & Air", "That page doesn't exist.",
     '''<section class="block"><div class="wrap prose"><h1>That page doesn't exist</h1>
<p>Try the <a href="/ashgrove-heating/">home page</a> or <a href="/ashgrove-heating/contact.html">contact us</a>.</p></div></section>''',
     prefix="/ashgrove-heating/")

# ---------------- Static extras ----------------
(OUT / "assets").mkdir(parents=True, exist_ok=True)
for f in (ROOT / "assets").iterdir():
    shutil.copy(f, OUT / "assets" / f.name)
(OUT / "assets" / "logo.svg").write_text(LOGO.replace(' aria-hidden="true"', ' xmlns="http://www.w3.org/2000/svg"'), encoding="utf-8")

urls = "".join(f"<url><loc>{BASE}/{'' if p == 'index.html' else p.replace('index.html', '')}</loc><lastmod>{TODAY}</lastmod></url>" for p in pages)
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                 + urls + "</urlset>\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built {len(pages)} pages to {OUT} (base {BASE})")
