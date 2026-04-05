# External Links Report - 2014-NHD-Submission

## Summary
All cdn2.editmysite.com references have been replaced with GitHub Pages URLs.

## ✅ CDN2 References: RESOLVED
All 10 original mappings + 8 additional mappings applied successfully.

### Additional Mappings Applied (not in original PATH_MAPPING.txt)
| Old URL | New URL |
|---------|---------|
| `var ASSETS_BASE = '//cdn2.editmysite.com/'` | `var ASSETS_BASE = 'https://avi583.github.io/2014-NHD-Submission/'` |
| `//cdn2.editmysite.com/js/old/slideshow-jq.js?buildtime=1775244635` | `https://avi583.github.io/2014-NHD-Submission/js/slideshow-jq.js` |
| `//cdn2.editmysite.com/js/lang/en/stl.js?buildTime=1775244635&` | `https://avi583.github.io/2014-NHD-Submission/js/stl.js` |
| `https://cdn2.editmysite.com/js/jquery-2.1.4.min.js` | `https://avi583.github.io/2014-NHD-Submission/js/jquery-2.1.4.min.js` |
| `//cdn2.editmysite.com/images/util/videojs/play-icon.png` | `https://avi583.github.io/2014-NHD-Submission/Images/videojs/play-icon.png` |
| `//cdn2.editmysite.com/images/util/videojs/@2x/play-icon.png` | `https://avi583.github.io/2014-NHD-Submission/Images/videojs/@2x/play-icon.png` |
| `//cdn2.editmysite.com/js/site/main-customer-accounts-site.js` | `https://avi583.github.io/2014-NHD-Submission/js/main-customer-accounts-site.js` |
| `//cdn2.editmysite.com/js/wsnbn/snowday262.js` | `https://avi583.github.io/2014-NHD-Submission/js/snowday262.js` |

---

## ⚠️ REMAINING EXTERNAL REFERENCES (Not on GitHub)

### Critical - Weebly Platform Dependencies (14 references)
These are Weebly platform scripts that may need replacement or removal:
- `//cdn1.editmysite.com/` - STATIC_BASE variable (15 files)
- `92435089.nhd.weebly.com` - securePrefix config
- `www.weebly.com/weebly/apps/generateVideo.php` - Video player scripts (7 videos)
- `www.weebly.com/Images/` - Video thumbnail images (7 images)

### Third-Party Services (May need local hosting)
| Domain | Count | Type |
|--------|-------|------|
| `www.google.com/recaptcha` | 15 | reCAPTCHA (can likely remove) |
| `embed.verite.co` | 2 | Timeline JS embeds |

### External Content Links (Bibliography/Citations - OK to keep)
| Domain | Count | Purpose |
|--------|-------|---------|
| commons.wikimedia.org | 12 | Wikipedia images |
| upload.wikimedia.org | 2 | Wikipedia images |
| www.opec.org | 6 | OPEC official sources |
| www.time.com | 7 | Time magazine citations |
| www.aljazeera.com | 5 | Al Jazeera citations |
| www.eia.gov | 2 | US Energy Info citations |
| select.nytimes.com | 3 | NYT citations |
| www.bbc.co.uk | 1 | BBC citation |
| www.youtube.com | 1 | YouTube reference |
| money.cnn.com | 1 | CNN Money reference |
| Various blog/image hosts | ~20 | Historical images |

---

## Required Additional Assets for GitHub

To fully migrate, you need to host these additional files:

### JavaScript Files Needed
```
/js/slideshow-jq.js
/js/jquery-2.1.4.min.js
/js/main-customer-accounts-site.js
/js/snowday262.js
```

### Image Files Needed
```
/Images/videojs/play-icon.png
/Images/videojs/@2x/play-icon.png
```

### Video Files (currently on Weebly)
The site has 7 embedded videos hosted on Weebly that would need to be downloaded and re-hosted:
1. opec_1990_iran_iraq_war_558.mp4
2. opec_50_years_later_1_852.mp4
3. opec_50_years_384.mp4
4. opec_4_good_959.mp4
5. opec_role_in_energy_markets_undimmed_after_50_years_1_970.mp4
6. hot_topic_-_opec_1_245.mp4
7. copy_of_20th_century_battlefields_down_flv_new_good_687.mp4

---

## Recommendations

1. **Remove reCAPTCHA** - Not needed for static GitHub Pages site
2. **Host videos on YouTube** - Embed YouTube players instead of Weebly video system
3. **Download external images** - Consider hosting citation images locally to prevent link rot
4. **Update cdn1 variable** - Change STATIC_BASE from cdn1.editmysite.com to GitHub Pages
