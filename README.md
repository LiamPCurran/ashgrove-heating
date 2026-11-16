# Ashgrove Heating & Air: local-SEO concept site

**Concept project by Liam Curran. Ashgrove is a fictional business; phone numbers, prices and details are illustrative.**

Live: https://liampcurran.github.io/ashgrove-heating/

A fast, static website for a local home-services company (HVAC, Ottawa), built to show what a well-optimized small-business site looks like.

- **Local SEO:** service-area `HVACBusiness` schema, dedicated service pages ("furnace repair Ottawa", "heat pump installation Ottawa"), neighbourhood coverage, FAQ schema and breadcrumbs.
- **Technical SEO:** unique titles and meta descriptions, canonical URLs, Open Graph tags, an XML sitemap, robots.txt and a clean heading structure.
- **Performance:** no frameworks, system fonts and inline SVG illustrations. Lighthouse scores 100 for Performance, Accessibility, Best Practices and SEO on mobile and desktop.
- **Conversion:** click-to-call everywhere, a short quote form and a clear three-step "how a visit works".

## Build

```
python make_og.py          # social preview image
python build.py https://liampcurran.github.io/ashgrove-heating
```

The generated site goes into `docs/`, which GitHub Pages serves.
