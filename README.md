# Ashgrove Heating & Air: local service business website template

**Concept project by Liam Curran. Ashgrove is a fictional business. Phone numbers, reviews, ratings and prices are illustrative.**

Live: https://liampcurran.github.io/ashgrove-heating/

A fast, conversion-focused static website for a local home-services company (HVAC, Ottawa). Its layout follows the patterns used by top-ranking Ottawa HVAC sites: an emergency top bar, a click-to-call header, a photo hero with an instant quote form, action callouts, trust stats, service cards, rebate and financing messaging, a booking process, reviews, maintenance plans, service areas, an FAQ and an emergency call band.

- **Local SEO:** service-area `HVACBusiness` schema, dedicated service pages ("furnace repair Ottawa", "heat pump installation Ottawa"), neighbourhood coverage, FAQ schema and breadcrumbs. Review ratings are shown visually but deliberately *not* added as schema, because the business is fictional.
- **Technical SEO:** unique titles and meta descriptions, canonical URLs, Open Graph tags, an XML sitemap, robots.txt and a clean heading structure.
- **Performance:** no frameworks. One self-hosted variable font, responsive WebP photos with lazy loading, and a preloaded hero image.
- **Conversion:** click-to-call everywhere, quote forms in the hero and sidebar, a sticky mobile Call / Quote bar, and maintenance-plan pricing.

## Build

```
python make_photos.py      # crops and compresses the stock photos (from ../_stock) into assets/img/
python make_og.py          # social preview image
python build.py https://liampcurran.github.io/ashgrove-heating
```

The generated site goes into `docs/`, which GitHub Pages serves.

## Credits

- Photos: [Unsplash](https://unsplash.com/license) (free to use). Photo IDs: L5sEqpQukJI, AlhRs3I8f7M, kblddocwPa0, -nbWCvUiFJA, 3_nf1qKJGf4, 8RbiLgfqoqQ, BsHycOlU6Bg, Tnx-t6CTg5o, mk9kC-klh5o.
- Font: Plus Jakarta Sans (SIL Open Font License).
