# Tailored Skydive: SEO launch guide

Prepared 12 Nov 2026 for https://tailoredskydive.com

## 1. Why Google probably isn't showing the site

I checked the code you sent: there was **no `noindex` tag anywhere**, so you were not blocking Google. The page simply had nothing helping Google find or understand it: no meta description, no canonical, no sitemap, no robots.txt, no structured data, and generic image alt text. A brand-new site with no inbound links and no Search Console submission can sit undiscovered for weeks.

Honest expectations: the files below remove the technical gaps, but **nobody can promise indexing or rankings**. Indexing normally follows within days to a few weeks of submitting in Search Console. Ranking for competitive searches like "skydive Devon" depends on content and backlinks (section 5). Searching your own brand ("Tailored Skydive") should work first.

## 2. What changed in the site files

| Request | What I did |
|---|---|
| Sitemap XML | `sitemap.xml` with the home page, today's lastmod and key images. `thank-you.html` is deliberately left out. |
| robots.txt | `robots.txt` allows everything and points to the sitemap. |
| Remove noindex | None existed. `thank-you.html` has `noindex` on purpose (it should not appear in search). |
| Canonical | `https://tailoredskydive.com/` (non-www, https). |
| Meta title / description | Title 53 chars, description 152 chars, both include "tandem skydive", Devon, Dunkeswell. |
| One H1 | Exactly one H1 per page. Added "Tandem" to it. |
| Header hierarchy | Fixed skipped levels (h3 to h2, h4 to h3). FAQ questions are now real H3 headings. Verified sequence: h1, h2s, h3s, no gaps. |
| Alt text | Every image has descriptive alt text (see caveat below). |
| Schema | JSON-LD: LocalBusiness/SportsActivityLocation with your prices, Person (Rich), WebSite, WebPage, FAQPage (the 20 FAQs). |
| Internal links | Contextual links between sections, footer navigation, back to top, skip link. |
| Broken links | Absolute `https://tailoredskydive.com/#...` links changed to clean `#anchors`. Browser-saved `_files/` paths restored to `images/`, CDN URLs for fonts, icons and Google tag restored. The WhatsApp button now URL-encodes names (`&` or `#` used to break the message) and shows "Phone not provided" correctly. |
| Compress images | Run `optimize-images.py` (section 4). I did not receive your images, so I couldn't do this myself. |
| Core Web Vitals | Removed the runtime Tailwind CDN script (not meant for production, delays first paint) in favour of a static `css/styles.css`. Lazy-loaded images, hero image preloaded, font-display swap, icon CSS loaded without blocking. |
| Mobile | Verified at 375px: no horizontal scroll, FAQ and menu work. Menu closes after tapping a link, tap targets enlarged, smaller section padding, anchor links no longer hide under the sticky nav, calculator summary no longer sticky on phones. |
| Enforce HTTPS | `upgrade-insecure-requests` and a JS redirect (http to https, www to non-www) as a safety net, plus `.htaccess` for Apache hosts. The real fix is a host setting (section 3). |
| Clean URL slugs | Single page site, so slugs are `/` and `/thank-you.html`. Kept `thank-you.html` because your form redirects to it. Use hyphenated lowercase slugs for any future pages. |
| OG image | `images/og-image.jpg` (1200x630) plus Open Graph and Twitter tags. **This is a branded placeholder. Replace it with a real jump photo of the same size** (e.g. a crop of your external-camera shot). |
| Other | Favicon set (Google shows favicons in results; replace with a proper logo when you have one), visible phone/email in the footer to match the schema, honeypot spam field on the form, `fa-hot-air-balloon` swapped for a free icon (it was a paid Font Awesome Pro icon and would not display). |

### Things you should check yourself

- **Alt text is based on your file names and captions, because I haven't seen the photos.** Open each image and correct anything inaccurate.
- **The three testimonials.** I did not mark them up as review schema, deliberately. If they are real, add the reviewer's permission and consider linking to a real Google Business Profile reviews page. If they are placeholders, replace them with genuine reviews or remove them: fake reviews are prohibited under the UK Digital Markets, Competition and Consumers Act and can also lead Google to distrust the site. The hero line "Trusted by hundreds of jumpers" should also be something you can back up.
- **Business address.** The schema uses Dunkeswell, Devon, GB with no street address, because I didn't want to guess one. Add the airfield's postal address if you are comfortable publishing it.
- **Thank-you page.** If you already have a live `thank-you.html`, keep yours and just make sure it has `<meta name="robots" content="noindex, follow">`.
- **Google Ads:** the conversion event is commented out in `thank-you.html`. Paste your conversion label from Google Ads to track bookings.

## 3. Deploy and enforce HTTPS

1. Upload everything in `site/` to your site root. Merge `images/og-image.jpg` into your existing `images/` folder (keep your own photos).
2. Run `python3 optimize-images.py images` on your real photos first (section 4).
3. Enforce HTTPS at the host (do this even though the page has a fallback):
   - **Netlify / Vercel / Cloudflare Pages:** HTTPS is automatic. In Netlify, Domain management > HTTPS > "Force HTTPS". In Cloudflare, SSL/TLS > Edge Certificates > "Always Use HTTPS" (use SSL mode Full or Full (strict), not Flexible).
   - **GitHub Pages:** Settings > Pages > tick "Enforce HTTPS".
   - **Apache / cPanel:** keep the `.htaccess` file. Not Apache? Delete it.
4. Make sure `www.tailoredskydive.com` 301-redirects to `tailoredskydive.com` (your host's domain settings).
5. Visit `https://tailoredskydive.com/robots.txt` and `/sitemap.xml` and confirm both load.

## 4. Compress images

```
pip install pillow
python3 optimize-images.py images
```

It resizes (max 1600px wide, 1920px for the hero), recompresses, strips EXIF/GPS data, and keeps your originals in `images_original/`. Aim for under 200 KB per photo. Tested on dummy files, but spot-check your results visually.

## 5. Get indexed and verified (Google Search Console)

1. Go to https://search.google.com/search-console and add a **Domain property** for `tailoredskydive.com`. Verify with the DNS TXT record at your domain registrar (the most reliable method, and it covers www and https variants). A URL-prefix property can use the HTML tag instead; there is a commented placeholder for it in `index.html`.
2. Sitemaps > submit `https://tailoredskydive.com/sitemap.xml`.
3. URL Inspection > paste `https://tailoredskydive.com/` > **Test live URL** > **Request indexing**.
4. Check "Pages" after 3 to 7 days. If it says "Discovered/Crawled, currently not indexed," that is normally a quality or links issue, not a technical one: add more unique content and links (below).
5. Also verify with **Bing Webmaster Tools** (it can import from Search Console) and create a **Bing Places** listing.
6. Test your pages:
   - Structured data: https://validator.schema.org and Google's Rich Results Test
   - Speed and mobile: https://pagespeed.web.dev (target LCP under 2.5 s, CLS under 0.1, INP under 200 ms)
   - Social preview: paste the URL into LinkedIn Post Inspector or the Facebook Sharing Debugger
7. Check `site:tailoredskydive.com` in Google weekly.

## 6. Content strategy (the biggest lever after links)

A one-page site gives Google one URL to rank. Competing for "skydive Devon" against dropzone sites needs more pages. Suggested next pages, each 400+ words of genuinely unique writing and with its own title, description, H1, canonical and sitemap entry:

- `/dunkeswell-tandem-skydive/` (the location, views, aircraft, getting there, where to stay)
- `/15000ft-tandem-skydive/` (what the extra altitude gets you, honest comparison with 10,000ft)
- `/nervous-first-time-skydive/` (fear of heights, what the briefing is like, real stories)
- `/skydive-gift-and-birthday/` (if you offer vouchers or milestone birthdays)
- A blog or guides: "What to wear for a skydive", "Skydive weight limits UK", "Is it worth paying for the video?" (reuse and expand your FAQs)

Also post regularly on Instagram, YouTube and Facebook (already linked in the schema `sameAs`) and always link back to the site.

## 7. Backlink strategy

Quality and relevance beat volume. One link from a real Devon tourism or skydiving page is worth more than hundreds from directories.

**Weeks 1 to 2: foundations (free, highest value)**
- **Google Business Profile.** Claim it and describe the service accurately (check Google's eligibility rules for your setup). Add photos, link the site, and ask happy jumpers for genuine reviews with a link/QR code.
- **Social profiles** (Instagram, Facebook, YouTube, and a LinkedIn page): website link in every bio.
- **Citations:** Bing Places, Apple Business Connect, Yell, Thomson Local, Yelp, FreeIndex. Keep name, phone and website identical everywhere.
- **Skydive South West / Dunkeswell dropzone.** You already link to them. Ask for a reciprocal mention as a partner/specialist instructor on their site or social channels.
- **British Skydiving:** check whether they have an instructor or club listing you qualify for.

**Weeks 3 to 8: local and partnership links**
- Visit Devon and local tourism sites, "things to do in Devon / East Devon / near Exeter" pages: pitch a short, factual listing.
- Hotels, B&Bs, glamping sites, and activity-gift companies near Dunkeswell: offer a referral arrangement and ask for a link on their "local activities" page.
- Local blogs, family travel and adventure bloggers: offer a free or discounted jump in exchange for an honest review (they must disclose it under ASA/CMA rules).
- Local newspapers and radio (Devon Live, Express & Echo, local BBC radio): pitch a story (e.g. milestone birthday jumps, charity jumps, a nervous first-timer's story).
- Charities: offer to run a sponsored jump and get listed on their fundraising page.

**Ongoing: earn links**
- Publish genuinely useful guides (section 6) and share them in relevant Devon and skydiving communities and Facebook groups, without spamming.
- Upload your best videos to YouTube with the site link and a descriptive title.
- Collaborate with the other sports you do (surf, kitesurf, wing foil, paragliding clubs and shops) for cross-mentions.

**Avoid:** buying links, link exchanges at scale, private blog networks, comment spam, and mass directory submissions. They risk a manual penalty. Use descriptive but natural anchor text (brand name and "tandem skydive Devon" mix), not the same keyword every time.

**Track:** Search Console > Links, plus the free tiers of Ahrefs Webmaster Tools or Bing Webmaster Tools. Target 10 to 20 relevant links in the first 90 days.

## 8. Quick checklist

- [ ] Real photos compressed, OG image replaced
- [ ] Alt text checked against the actual photos
- [ ] Testimonials confirmed genuine (or replaced)
- [ ] Uploaded and HTTPS forced at host; www redirects to non-www
- [ ] robots.txt and sitemap.xml load
- [ ] Search Console domain verified, sitemap submitted, indexing requested
- [ ] Rich Results Test and PageSpeed Insights pass
- [ ] Google Business Profile and first citations live
- [ ] 2 to 4 new content pages planned
