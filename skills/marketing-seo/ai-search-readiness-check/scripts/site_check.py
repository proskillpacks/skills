#!/usr/bin/env python3
"""site_check.py: read-only facts about public web pages, for the Client Site Fix Kit skills.

  python3 site_check.py facts URL            on-page facts of one page (JSON)
  python3 site_check.py count "text" ...     exact character and word counts
  python3 site_check.py ai URL               AI search readiness facts and a 0-100 score (JSON)
  python3 site_check.py local URL [--out FILE]   name, address, phone and hours facts across up to 5 pages (JSON);
                                             --out also saves it, for schema-check --facts
  python3 site_check.py schema-check FILE|- [--facts local.json] [--fragment]
                                             checks a LocalBusiness JSON-LD block: valid JSON, type,
                                             required fields, and (with --facts) that each value is found in
                                             the page text the checker read; --fragment checks only the
                                             values of fields to add to existing markup (one JSON object)
  python3 site_check.py gap YOUR_URL COMPETITOR_URL [COMPETITOR_URL ...] [--out gap.json]
                                             outlines, questions and text of your page and 1 to 4 competitor pages, and
                                             which competitor headings use words your page doesn't (JSON)
  python3 site_check.py find gap.json "phrase" ...   where each phrase appears in the pages read by `gap`
  python3 site_check.py article URL|FILE     an article's dates, years mentioned, stat sentences and whether a link or
                                             source sits with them, AI-sounding phrase counts, intro, headings (JSON)
  python3 site_check.py keep ORIGINAL NEW    numbers and names in NEW that ORIGINAL doesn't have (texts or files)

Standard library only. Identifies itself honestly, obeys robots.txt for its own user agent (RFC 9309:
a robots.txt that returns 5xx or can't be reached means nothing is fetched; a 4xx means no rules),
waits 1 second between requests, reads at most 5 MB per page. No forms, logins or JavaScript:
it sees the server-rendered HTML, which is also what most AI crawlers see.
"""
import gzip, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request, zlib

UA = "ProSkillPacks-SiteCheck/1.0 (read-only helper run for a user; +https://proskillpacks.github.io/helpers/)"
AI_SEARCH = ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "Claude-SearchBot", "Claude-User",
             "Googlebot", "Bingbot"]
AI_TRAINING = ["GPTBot", "ClaudeBot", "Google-Extended", "CCBot", "Applebot-Extended", "Meta-ExternalAgent"]
# schema.org Organization and every subtype (LocalBusiness and its subtypes included), taken from the
# schema.org vocabulary file (schemaorg-current-https.jsonld, rdfs:subClassOf closure, downloaded 2026-10-04).
ORG_TYPES = set("""
    AccountingService AdultEntertainment Airline AmusementPark AnimalShelter ArchiveOrganization ArtGallery
    Attorney AutoBodyShop AutoDealer AutoPartsStore AutoRental AutoRepair AutoWash AutomatedTeller
    AutomotiveBusiness Bakery BankOrCreditUnion BarOrPub BeautySalon BedAndBreakfast BikeStore BookStore
    BowlingAlley Brewery CafeOrCoffeeShop Campground Casino ChildCare ClothingStore CollegeOrUniversity
    ComedyClub ComputerStore Consortium ConvenienceStore Cooperative Corporation CovidTestingFacility
    DanceGroup DaySpa Dentist DepartmentStore DiagnosticLab Distillery DryCleaningOrLaundry
    EducationalOrganization Electrician ElectronicsStore ElementarySchool EmergencyService EmploymentAgency
    EntertainmentBusiness ExerciseGym FastFoodRestaurant FinancialService FireStation Florist
    FoodEstablishment FundingAgency FundingScheme FurnitureStore GardenStore GasStation GeneralContractor
    GolfCourse GovernmentOffice GovernmentOrganization GroceryStore HVACBusiness HairSalon HardwareStore
    HealthAndBeautyBusiness HealthClub HighSchool HobbyShop HomeAndConstructionBusiness HomeGoodsStore
    Hospital Hostel Hotel HousePainter IceCreamShop IndividualPhysician InsuranceAgency InternetCafe
    JewelryStore LegalService Library LibrarySystem LiquorStore LocalBusiness Locksmith LodgingBusiness
    MedicalBusiness MedicalClinic MedicalOrganization MensClothingStore MiddleSchool MobilePhoneStore Motel
    MotorcycleDealer MotorcycleRepair MovieRentalStore MovieTheater MovingCompany MusicGroup MusicStore NGO
    NailSalon NewsMediaOrganization NightClub Notary OfficeEquipmentStore OnlineBusiness OnlineMarketplace
    OnlineStore Optician Organization OutletStore PawnShop PerformingGroup PetStore Pharmacy Physician
    PhysiciansOffice Plumber PoliceStation PoliticalParty PostOffice Preschool ProfessionalService Project
    PublicSwimmingPool RadioStation RealEstateAgent RecyclingCenter ResearchOrganization ResearchProject
    Resort Restaurant RoofingContractor School SearchRescueOrganization SelfStorage ShoeStore ShoppingCenter
    SkiResort SportingGoodsStore SportsActivityLocation SportsClub SportsOrganization SportsTeam
    StadiumOrArena Store TattooParlor TelevisionStation TennisComplex TheaterGroup TireShop
    TouristInformationCenter ToyStore TravelAgency VacationRental VeterinaryCare WholesaleStore Winery
    WorkersUnion
""".split())


def is_org_type(t):
    """True for schema.org Organization or any subtype; also unknown extension types named like one."""
    t = t.rsplit("/", 1)[-1].rsplit(":", 1)[-1]
    return t in ORG_TYPES or t.endswith(("Business", "Store", "Organization"))


_last = [0.0]
_robots = {}
_robots_err = {}


# ---------- fetching ----------
class _CrossHostBlocked(Exception):
    pass


class _RobotsRedirect(urllib.request.HTTPRedirectHandler):
    """Before following a redirect to another host, read that host's robots.txt (RFC 9309) for our user agent."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old, new = urllib.parse.urlsplit(req.full_url), urllib.parse.urlsplit(newurl)
        if new.netloc.lower() != old.netloc.lower() and not new.path.endswith("/robots.txt"):
            ok, why = may_fetch(f"{new.scheme}://{new.netloc}", _path_q(newurl))
            if not ok:
                raise _CrossHostBlocked(f"redirected to another site ({new.netloc}); {why}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_opener = urllib.request.build_opener(_RobotsRedirect)


def _path_q(url):
    p = urllib.parse.urlsplit(url)
    return (p.path or "/") + (f"?{p.query}" if p.query else "")


def _get(url, identity=False):
    wait = 1.0 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/plain,*/*",
                                               "Accept-Encoding": "identity" if identity else "gzip, deflate"})
    try:
        with _opener.open(req, timeout=25) as r:
            raw, enc, st, final, ctype = r.read(5_000_000), r.headers.get("Content-Encoding", ""), r.status, r.geturl(), \
                r.headers.get("Content-Type", "")
            xrobots = r.headers.get("X-Robots-Tag", "")
    except urllib.error.HTTPError as e:
        return e.code, "", url, "", ""
    except _CrossHostBlocked as e:
        return None, f"blocked: {e}", url, "", ""
    except Exception as e:
        return None, f"{type(e).__name__}: {e}", url, "", ""
    enc = enc.lower().strip()
    if enc not in ("", "identity", "gzip", "deflate"):
        if not identity:
            return _get(url, identity=True)   # some servers send brotli or another encoding we did not ask for: ask once for plain text
        return None, f"unreadable: the server sent Content-Encoding '{enc}', which this helper cannot decode (Python standard library only)", url, "", ""
    try:
        raw = gzip.decompress(raw) if "gzip" in enc else (zlib.decompress(raw) if "deflate" in enc else raw)
    except Exception:
        pass
    return st, raw.decode("utf-8", "replace"), final, ctype, xrobots


def parse_robots(txt):
    groups, cur, last_agent = [], None, False
    for line in txt.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if cur is None or not last_agent:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(v.lower())
            last_agent = True
        elif k in ("allow", "disallow"):
            last_agent = False
            if cur is not None and v:
                cur["rules"].append((k == "allow", v))
        else:
            last_agent = False
    return groups


def allowed(groups, agent, path):
    a = agent.lower()
    named = [g for g in groups if any(ga != "*" and a == ga for ga in g["agents"])]  # RFC 9309: exact token, case-insensitive
    rules = [r for g in (named or [g for g in groups if "*" in g["agents"]]) for r in g["rules"]]
    best, ok = -1, True
    for is_allow, pat in rules:
        rx = "".join(".*" if c == "*" else re.escape(c) for c in pat.rstrip("$")) + ("$" if pat.endswith("$") else "")
        if re.match(rx, path) and (len(pat) > best or (len(pat) == best and is_allow)):
            best, ok = len(pat), is_allow
    return ok


def robots_for(base):
    """(status, text, groups). RFC 9309 2.3.1: 4xx = no rules (allowed); 5xx or no response = disallow everything."""
    if base not in _robots:
        st, txt, _, _, _ = _get(base + "/robots.txt")
        _robots[base] = (st, txt if st == 200 else "", parse_robots(txt) if st == 200 else [])
        if st is None:
            _robots_err[base] = txt
    return _robots[base]


def robots_blocks_all(st):
    return st is None or st >= 500


def may_fetch(base, path):
    st, _, groups = robots_for(base)
    if robots_blocks_all(st):
        return False, (f"robots.txt returned HTTP {st}" if st else
                       f"network error: the site could not be reached ({_robots_err.get(base, 'no response')})") + \
            "; under RFC 9309 that means the whole site is disallowed, so nothing was fetched"
    if groups and not allowed(groups, "ProSkillPacks-SiteCheck", path):
        return False, "robots.txt does not allow this user agent to read the page; not fetched"
    return True, ""


def base_of(url):
    p = urllib.parse.urlsplit(url)
    return f"{p.scheme}://{p.netloc}"


def fetch(url):
    """Fetch one page if robots.txt lets our user agent read it."""
    if not re.match(r"https?://", url):
        url = "https://" + url
    base = base_of(url)
    ok, why = may_fetch(base, _path_q(url))
    if not ok:
        return {"url": url, "status": None, "error": why, "html": "", "blocked_by_robots": True}
    st, body, final, ctype, xr = _get(url)
    if st is None and body.startswith("blocked: "):
        return {"url": url, "status": None, "error": body[9:], "html": "", "blocked_by_robots": True}
    return {"url": url, "final_url": final, "status": st, "content_type": ctype, "x_robots_tag": xr,
            "html": body if st == 200 else "", "error": "" if st == 200 else (body if st is None else f"HTTP {st}")}


# ---------- parsing ----------
def strip_tags(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg|template|iframe)[^>]*>.*?</\1>", " ", h or "")
    h = re.sub(r"(?is)<!--.*?-->", " ", h)
    # A tag ends at the first ">" outside quotes (attribute values like x-on:click="a > b" contain ">").
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[a-zA-Z/!](?:[^>\"']|\"[^\"]*\"|'[^']*')*>", " ", h))).strip()


def words(t):
    return len(re.findall(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9'’-]*", t or ""))


def attr(tag, name):
    m = re.search(r'(?is)\b' + name + r'\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))', tag)
    return html.unescape((m.group(2) or m.group(3) or m.group(4) or "").strip()) if m else None


def meta(h, key, val):
    for tag in re.findall(r"(?is)<meta\b[^>]*>", h):
        if (attr(tag, key) or "").lower() == val:
            return attr(tag, "content")
    return None


def jsonld(h):
    out, errors = [], 0
    for m in re.findall(r'(?is)<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', h):
        o = None
        for cand in (m.strip(), re.sub(r",\s*([}\]])", r"\1", m.strip())):
            try:
                o = json.loads(cand)
                break
            except Exception:
                pass
        if o is None:
            errors += 1
            continue
        stack = [o]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if isinstance(x.get("@graph"), list):
                    stack.extend(x["@graph"])
                    rest = {k: v for k, v in x.items() if k not in ("@graph", "@context")}
                    if rest:
                        out.append(rest)
                    continue
                out.append(x)
            elif isinstance(x, list):
                stack.extend(x)
    return out, errors


def types(o):
    t = o.get("@type", [])
    return [t] if isinstance(t, str) else [x for x in (t or []) if isinstance(x, str)]


def headings(h, n):
    return [strip_tags(x) for x in re.findall(rf"(?is)<h{n}\b[^>]*>(.*?)</h{n}>", h)]


def links(h, base):
    host = urllib.parse.urlsplit(base).netloc.lower().replace("www.", "")
    internal, external, out = 0, 0, []
    for tag, inner in re.findall(r"(?is)(<a\b[^>]*>)(.*?)</a>", h):
        href = attr(tag, "href") or ""
        if not href or href.startswith(("#", "javascript:")):
            continue
        absu = urllib.parse.urljoin(base + "/", href)
        hn = urllib.parse.urlsplit(absu).netloc.lower().replace("www.", "")
        if href.startswith(("mailto:", "tel:")):
            continue
        if hn == host:
            internal += 1
            out.append((absu, strip_tags(inner)))
        else:
            external += 1
    return internal, external, out


PHONE_RX = re.compile(r"(?<![\d/])(?:(?:\+1[\s.-]?)?\(\d{3}\)[\s.-]?\d{3}[\s.-]\d{4}|(?:\+\d{1,3}[\s.-]?)?(?:\(\d{2,5}\)[\s.-]?)?\d{2,5}[\s.-]\d{3,4}[\s.-]?\d{3,4})(?![\d/])")


def norm_phone(p):
    d = re.sub(r"\D", "", p)
    if d.startswith("44"):
        d = "0" + d[2:]
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d


def page_facts(url, keep_html=False):
    f = fetch(url)
    h = f.pop("html")
    if not h:
        return f
    final = f.get("final_url") or url
    base = base_of(final)
    head = (re.search(r"(?is)<head\b.*?</head>", h) or [h[:20000]])[0] if re.search(r"(?is)<head\b", h) else h[:20000]
    title_m = re.search(r"(?is)<title[^>]*>(.*?)</title>", h)
    title = strip_tags(title_m.group(1)) if title_m else None
    desc = meta(h, "name", "description")
    canon, canon_all = None, []
    for tag in re.findall(r"(?is)<link\b[^>]*>", h):
        if (attr(tag, "rel") or "").lower() == "canonical":
            canon_all.append(attr(tag, "href"))
    canon = canon_all[0] if canon_all else None
    desc_all = [attr(t, "content") for t in re.findall(r"(?is)<meta\b[^>]*>", h) if (attr(t, "name") or "").lower() == "description"]
    title_all = [strip_tags(x) for x in re.findall(r"(?is)<title[^>]*>(.*?)</title>", (re.search(r"(?is)<head\b.*?</head>", h) or [h])[0])]
    imgs = re.findall(r"(?is)<img\b[^>]*>", h)
    no_alt = sum(1 for t in imgs if attr(t, "alt") is None)
    no_alt_src = [attr(t, "src") or attr(t, "data-src") or "" for t in imgs if attr(t, "alt") is None][:10]
    empty_alt = sum(1 for t in imgs if attr(t, "alt") == "")
    internal, external, _ = links(h, base)
    objs, ld_errors = jsonld(h)
    text = strip_tags(h)
    body_text = strip_tags((re.search(r"(?is)<body\b.*?</body>", h) or [h])[0])
    ctas = []
    for tag, inner in re.findall(r"(?is)(<(?:a|button)\b[^>]*>)(.*?)</(?:a|button)>", h):
        cls = (attr(tag, "class") or "") + " " + (attr(tag, "role") or "")
        t = strip_tags(inner)
        if t and len(t) <= 40 and (tag.lower().startswith("<button") or re.search(r"btn|button|cta", cls, re.I)):
            if t not in ctas:
                ctas.append(t)
    zw = lambda x: re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", x).strip()
    phones = sorted({zw(p) for p in PHONE_RX.findall(body_text)})
    emails = sorted({urllib.parse.unquote(m).strip() for m in re.findall(r"(?i)mailto:([^\"'?>\s]+)", h)} |
                    set(re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", body_text)))
    img_srcs = sorted({urllib.parse.urljoin(final, attr(t, "src") or "") for t in imgs if attr(t, "src")})[:60]
    page_links = sorted({u for u, _ in links(h, base)[2]})[:200]
    tels = sorted({zw(urllib.parse.unquote((attr(t, "href") or "")[4:])) for t in re.findall(r"(?is)<a\b[^>]*href=[\"']tel:[^>]*>", h)})
    return {**f, "lang": attr((re.search(r"(?is)<html\b[^>]*>", h) or [""])[0] if re.search(r"(?is)<html\b", h) else "", "lang"),
            "title": title, "title_characters": len(title) if title else 0,
            "meta_description": desc, "meta_description_characters": len(desc) if desc else 0,
            "meta_robots": meta(h, "name", "robots"), "canonical": canon,
            "title_tags": len(title_all), "meta_description_tags": len(desc_all),
            "all_meta_descriptions": [(d, len(d or "")) for d in desc_all] if len(desc_all) > 1 else [],
            "canonical_tags": len(canon_all), "all_canonicals": canon_all if len(canon_all) > 1 else [],
            "og_title": meta(h, "property", "og:title"), "og_description": meta(h, "property", "og:description"),
            "h1": headings(h, 1), "h2": headings(h, 2)[:30], "h3": headings(h, 3)[:30],
            "words_in_body": words(body_text),
            "images": len(imgs), "images_without_alt_attribute": no_alt, "images_without_alt_src": no_alt_src, "images_with_empty_alt": empty_alt,
            "internal_links": internal, "external_links": external,
            "jsonld_types": sorted({t for o in objs for t in types(o)}), "jsonld_parse_errors": ld_errors,
            "jsonld": objs[:12], "buttons_and_ctas": ctas[:25], "phone_numbers_in_text": phones, "tel_links": tels, "emails": emails,
            "image_urls": img_srcs, "internal_link_urls": page_links,
            "visible_text": body_text[:30000], "visible_text_truncated": len(body_text) > 30000,
            "note": "Server-rendered HTML only. Content or schema added later by JavaScript is not seen.",
            **({"_html": h} if keep_html else {})}


# ---------- commands ----------
def cmd_count(texts):
    for t in texts:
        print(json.dumps({"text": t, "characters": len(t), "words": words(t)}, ensure_ascii=False))


def cmd_ai(url):
    if not re.match(r"https?://", url):
        url = "https://" + url
    pf = page_facts(url)
    base = base_of(pf.get("final_url") or url)
    rst, rtxt, groups = robots_for(base)
    if pf.get("blocked_by_robots"):
        # Not allowed to read the site: no score, nothing else fetched. The robots.txt rules already read are reported.
        agents = {} if (rst is None or rst >= 500) else {
            "ai_search_agents": {a: (allowed(groups, a, "/") if groups else True) for a in AI_SEARCH},
            "ai_training_crawlers": {a: (allowed(groups, a, "/") if groups else True) for a in AI_TRAINING}}
        print(json.dumps({"url": url, "home_status": None, "robots_txt_status": rst, "fetch_error": pf["error"], "score": None,
                          **agents,
                          "finding": (f"robots.txt returned HTTP {rst}; crawlers that follow RFC 9309 treat the whole site as blocked "
                                      "until robots.txt loads (or returns 200 or 404)") if rst and rst >= 500 else None,
                          "note": "No score: the checker only reads what robots.txt lets it read."}, indent=1, ensure_ascii=False))
        return
    search = {a: (allowed(groups, a, "/") if groups else True) for a in AI_SEARCH}
    training = {a: (allowed(groups, a, "/") if groups else True) for a in AI_TRAINING}
    if allowed(groups, "ProSkillPacks-SiteCheck", "/llms.txt") if groups else True:
        lst, ltxt, _, lct, _ = _get(base + "/llms.txt")
        llms = lst == 200 and "<html" not in ltxt[:500].lower() and len(ltxt.strip()) > 20
        llms_ev = f"/llms.txt HTTP {lst}" + ("" if llms or lst != 200 else
                   (": an HTML page, not a text file" if "<html" in ltxt[:500].lower() else ": almost empty (20 characters or fewer)"))
    else:
        llms, llms_ev = False, "/llms.txt not fetched: disallowed by robots.txt"
    sm = [l.split(":", 1)[1].strip() for l in rtxt.splitlines() if l.lower().startswith("sitemap:")]
    sm_ev = ""
    if not sm:
        if allowed(groups, "ProSkillPacks-SiteCheck", "/sitemap.xml") if groups else True:
            sst, _, _, _, _ = _get(base + "/sitemap.xml")
            sm = [base + "/sitemap.xml"] if sst == 200 else []
        else:
            sm_ev = "/sitemap.xml not fetched: disallowed by robots.txt"
    content_signals = [l.strip() for l in rtxt.splitlines() if l.strip().lower().startswith("content-signal:")]
    t = pf.get("jsonld_types", [])
    org_types = [x for x in t if is_org_type(x)]
    org = bool(org_types)
    faq = "FAQPage" in t or any(re.search(r"\?$", x) for x in pf.get("h2", []) + pf.get("h3", []))
    w = pf.get("words_in_body", 0)
    noindex = bool(re.search(r"noindex", (pf.get("meta_robots") or "") + " " + (pf.get("x_robots_tag") or ""), re.I))
    checks = [
        ("search_agents_allowed", "robots.txt lets AI search and user agents read the home page", 25,
         25 if all(search.values()) else (10 if any(search.values()) else 0),
         "blocked: " + (", ".join(a for a, ok in search.items() if not ok) or "none")),
        ("indexable", "home page is not marked noindex", 10, 0 if noindex else 10,
         f"meta robots: {pf.get('meta_robots')!r}; X-Robots-Tag: {pf.get('x_robots_tag')!r}"),
        ("server_text", "home page has readable text in the server HTML (150+ words)", 15,
         15 if w >= 150 else (7 if w >= 50 else 0), f"{w} words in the server-rendered body"),
        ("title_and_description", "home page has a title and a meta description", 10,
         (5 if pf.get("title") else 0) + (5 if pf.get("meta_description") else 0),
         f"title: {pf.get('title')!r}; description: {pf.get('meta_description')!r}"),
        ("organization_schema", "structured data says who the business is (Organization or LocalBusiness)", 15,
         15 if org else 0, "JSON-LD types: " + (", ".join(t) or "none") +
         (f" (schema.org Organization types: {', '.join(org_types)})" if org_types else "")),
        ("answer_content", "question-style headings or FAQPage structured data", 10, 10 if faq else 0,
         "FAQPage" if "FAQPage" in t else "question headings: " + str(sum(1 for x in pf.get('h2', []) + pf.get('h3', []) if x.endswith('?')))),
        ("sitemap", "a sitemap is listed in robots.txt or at /sitemap.xml", 10, 10 if sm else 0, ", ".join(sm[:3]) or sm_ev or "none found"),
        ("llms_txt", "an llms.txt file exists (optional; not a standard any engine has confirmed it uses)", 5, 5 if llms else 0,
         llms_ev),
    ]
    score = sum(c[3] for c in checks)
    fix = sorted([c for c in checks if c[3] < c[2]], key=lambda c: -(c[2] - c[3]))
    out = {"url": url, "final_url": pf.get("final_url"), "home_status": pf.get("status"), "fetch_error": pf.get("error"),
           "robots_txt_status": rst, "score": score, "checks_total": len(checks),
           "checks_passed_in_full": sum(1 for c in checks if c[3] == c[2]),
           "checks": [{"id": c[0], "check": c[1], "max": c[2], "points": c[3], "evidence": c[4]} for c in checks],
           "fix_order": [{"id": c[0], "points_lost": c[2] - c[3]} for c in fix],
           "ai_search_agents": search, "ai_training_crawlers": training,
           "content_signal_lines": content_signals,
           "note": "Training crawlers are listed for information and are not scored: blocking them is a business choice "
                   "and does not remove a site from AI search answers. Firewalls and bot protection were not tested. "
                   "robots.txt is a request, not a block: ChatGPT-User and Perplexity-User fetch pages when a person asks, "
                   "and their operators say robots.txt may not always apply to those fetches. "
                   "content_signal_lines (Cloudflare's Content-Signal, e.g. ai-input=no) are shown for information and not scored."}
    print(json.dumps(out, indent=1, ensure_ascii=False))


ADDR_HINT = re.compile(r"\b(street|st\.?|road|rd\.?|avenue|ave\.?|lane|ln\.?|drive|dr\.?|boulevard|blvd|way|place|court|suite|unit)\b", re.I)
POSTCODE = re.compile(r"\b([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2})\b|\b(\d{5})(?:-\d{4})?\b")
HOURS = re.compile(r"(?i)\b(mon(day)?|tue(s|sday)?|wed(nesday)?|thu(rs|rsday)?|fri(day)?|sat(urday)?|sun(day)?)\b[^\n]{0,25}?\d{1,2}([:.]\d{2})?\s*(am|pm)?\s*(?:-|–|—|to)\s*\d{1,2}([:.]\d{2})?\s*(am|pm)?(?:\s*[,&]\s*\d{1,2}([:.]\d{2})?\s*(am|pm)?\s*(?:-|–|—|to)\s*\d{1,2}([:.]\d{2})?\s*(am|pm)?)?(?:,?\s*closed)?")


def cmd_local(url, out_file=None):
    if not re.match(r"https?://", url):
        url = "https://" + url
    home = page_facts(url)
    pages = [home]
    if home.get("status") == 200:
        f = fetch(home.get("final_url") or url)
        _, _, ls = links(f.get("html", ""), base_of(home.get("final_url") or url))
        seen = {home.get("final_url"), url}
        for u, t in ls:
            if len(pages) >= 5:
                break
            u = u.split("#")[0]
            if u in seen:
                continue
            if re.search(r"\.(pdf|jpe?g|png|docx?)$", u, re.I):
                continue
            if re.search(r"contact|about|location|find-us|visit|hours|our-practice|practice|our-team|team", u + " " + t, re.I):
                seen.add(u)
                pages.append(page_facts(u))
    per_page, all_phones, lb = [], {}, []
    seen_blocks = set()
    for p in pages:
        txt = p.get("visible_text", "") or ""
        ph = p.get("phone_numbers_in_text", []) + p.get("tel_links", [])
        for x in ph:
            all_phones.setdefault(norm_phone(x), set()).add(x)
        addr_snips = []
        for m in POSTCODE.finditer(txt):
            s = txt[max(0, m.start() - 90): m.end() + 5]
            if ADDR_HINT.search(s) and s.strip() not in addr_snips:
                addr_snips.append(s.strip())
        hours = list(dict.fromkeys(m.group(0) for m in HOURS.finditer(txt)))[:10]
        notes = list(dict.fromkeys(m.group(0).strip() for m in re.finditer(
            r"(?i)[^.!?]{0,80}\b(closed for lunch|lunch|closed|by appointment|appointment only|bank holidays?|24/7|24 hours)\b[^!?]{0,120}", txt)
            if HOURS.search(txt[max(0, m.start() - 300): m.end() + 300])))[:6]
        for o in p.get("jsonld", []):
            t = types(o)
            if any(is_org_type(x) for x in t):
                key = json.dumps(o, sort_keys=True, default=str)
                if key in seen_blocks:
                    continue
                seen_blocks.add(key)
                lb.append({"page": p.get("final_url") or p.get("url"), "types": t, "id": o.get("@id"),
                           "fields": {k: v for k, v in o.items() if not k.startswith("@")}})
        per_page.append({"url": p.get("final_url") or p.get("url"), "status": p.get("status"), "error": p.get("error"),
                         "title": p.get("title"), "phones": ph, "emails": p.get("emails", []),
                         "address_snippets": addr_snips[:5], "hours_snippets": hours, "hours_notes": notes,
                         "jsonld_types": p.get("jsonld_types", []), "image_urls": p.get("image_urls", [])[:20],
                         "text": txt[:4000], "text_truncated": len(txt) > 4000})
    out = {"url": url, "final_url": home.get("final_url"), "pages_checked": per_page,
           "distinct_phone_numbers": {k: sorted(v) for k, v in all_phones.items()},
           "phone_formats_differ": any(len(v) > 1 for v in all_phones.values()),
           "business_schema_blocks": lb,
           "note": "Address snippets are text found near a postcode or ZIP code and a street word; read them, don't trust them blindly. "
                   "Google Business Profile, maps and directories are not checked. "
                   "Each page's text (first 4000 characters) and emails are included: use them, don't fetch pages another way."}
    txt = json.dumps(out, indent=1, ensure_ascii=False, default=list)
    print(txt)
    if out_file:
        open(out_file, "w", encoding="utf-8").write(txt)
        print(f"saved: {out_file}")


REQUIRED = ["@context", "@type", "name", "address", "telephone"]
RECOMMENDED = ["url", "openingHoursSpecification", "image"]


def flatten(o, prefix=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if not k.startswith("@"):
                yield from flatten(v, f"{prefix}{k}.")
    elif isinstance(o, list):
        for v in o:
            yield from flatten(v, prefix)
    elif isinstance(o, (str, int, float)):
        yield prefix.rstrip("."), str(o)


def cmd_schema_check(src, facts, fragment=False):
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    raw = re.sub(r'(?is)^\s*<script[^>]*>|</script>\s*$', "", raw.strip())
    fails, notes = [], []
    try:
        o = json.loads(raw)
    except Exception as e:
        print(json.dumps({"ok": False, "fails": [f"not valid JSON: {e}"]}, indent=1)); sys.exit(1)
    if not isinstance(o, dict):
        print(json.dumps({"ok": False, "fails": ["expected one JSON object"]}, indent=1)); sys.exit(1)
    t = types(o)
    if fragment:
        # Fields to add to existing markup: structure of the whole block is not checked, values are.
        notes.append("fragment mode: only the values were checked; add these fields to the existing block")
        missing_rec = []
    else:
        if "schema.org" not in str(o.get("@context", "")):
            fails.append("@context should be https://schema.org")
        for k in REQUIRED:
            if k not in o:
                fails.append(f"missing {k}")
        if not t:
            fails.append("@type missing")
        missing_rec = [k for k in RECOMMENDED if k not in o]
    # Review and rating markup is never added, whatever the site shows (Google's self-serving review rules).
    def walk(x):
        if isinstance(x, dict):
            yield x
            for v in x.values():
                yield from walk(v)
        elif isinstance(x, list):
            for v in x:
                yield from walk(v)
    for node in walk(o):
        bad_keys = [k for k in node if k in ("aggregateRating", "review", "reviews", "reviewRating", "ratingValue", "reviewCount",
                                             "ratingCount", "bestRating")]
        bad_types = [x for x in types(node) if x in ("AggregateRating", "Review", "Rating")]
        for k in bad_keys + bad_types:
            fails.append(f"{k}: never add review or rating markup")
    if facts:
        f = json.load(open(facts, encoding="utf-8"))
        # Only text the checker read on the pages: never the site's existing markup.
        parts, urls = [], set()
        for pg in f.get("pages_checked", []):
            parts += [pg.get("title") or "", pg.get("text") or "", " ".join(pg.get("phones", [])), " ".join(pg.get("emails", [])),
                      " ".join(pg.get("address_snippets", [])), " ".join(pg.get("hours_snippets", [])), " ".join(pg.get("hours_notes", []))]
            urls |= {u for u in [pg.get("url")] + pg.get("image_urls", []) if u}
        urls |= {u for u in (f.get("url"), f.get("final_url")) if u}
        corpus = re.sub(r"\s+", " ", " ".join(parts))
        corpus_n = corpus.lower()
        site_phones = set(re.findall(PHONE_RX, corpus))
        urls_n = {u.rstrip("/").lower() for u in urls}
        has = lambda needle: re.search(r"(?<![\w])" + re.escape(needle.lower()) + r"(?![\w])", corpus_n) is not None
        day_forms = {"monday": ["monday", "mon", "mondays"], "tuesday": ["tuesday", "tue", "tues", "tuesdays"],
                     "wednesday": ["wednesday", "wed", "wednesdays"], "thursday": ["thursday", "thu", "thur", "thurs", "thursdays"],
                     "friday": ["friday", "fri", "fridays"], "saturday": ["saturday", "sat", "saturdays"],
                     "sunday": ["sunday", "sun", "sundays"]}
        for path, val in flatten(o):
            v = val.strip()
            leaf = path.split(".")[-1]
            if leaf == "dayOfWeek" or re.match(r"https?://schema\.org/\w+day$", v):
                d = v.rsplit("/", 1)[-1].lower()
                forms = day_forms.get(d, [d])
                range_ok = re.search(r"(?i)\b(mon|monday)\w*\s*(?:-|–|to)\s*(fri|friday|sat|saturday|sun|sunday)\b", corpus) and \
                    d in ("tuesday", "wednesday", "thursday")
                if not any(has(x) for x in forms) and not range_ok:
                    fails.append(f"{path} = {v!r}: that day is not in the text the checker read")
                elif any(re.search(r"(?<![\w])" + re.escape(x) + r"(?![\w])[^\d\n]{0,20}?\b(closed|by appointment|appointment only)\b"
                                   r"(?!\s+(for|between|from|at|during)\b)", corpus_n) for x in forms):
                    fails.append(f"{path} = {v!r}: the site says that day is closed or by appointment; leave it out")
                continue
            if re.match(r"https?://schema\.org", v):
                continue
            if leaf in ("opens", "closes"):
                m = re.fullmatch(r"(\d{2}):(\d{2})(?::00)?", v)
                if not m:
                    fails.append(f"{path} = {v!r}: write times as HH:MM, 24-hour (for example 17:30)")
                    continue
                hh, mm = int(m.group(1)), m.group(2)
                h12 = hh - 12 if hh > 12 else (12 if hh == 0 else hh)
                ap = "pm" if hh >= 12 else "am"
                cands = [f"{hh}:{mm}", f"{hh}.{mm}", f"{hh:02d}:{mm}", f"{hh:02d}.{mm}", f"{h12}:{mm}{ap}", f"{h12}.{mm}{ap}",
                         f"{h12}:{mm} {ap}", f"{h12}.{mm} {ap}", f"{h12}:{mm}"]
                if mm == "00":
                    cands += [f"{h12}{ap}", f"{h12} {ap}", f"{h12}"] if hh >= 1 else []
                if hh == 12 and mm == "00":
                    cands += ["noon", "midday"]
                hours_txt = " ".join(" ".join(pg.get("hours_snippets", []) + pg.get("hours_notes", [])) for pg in f.get("pages_checked", [])).lower()
                pool = hours_txt or corpus_n
                wrong = "p" if hh < 12 else "a"
                if not any(re.search(r"(?<![\d:.])" + re.escape(c) + r"(?!\d|[:.]\d)" + ("" if c.endswith(("am", "pm")) else r"(?!\s*" + wrong + r"\.?m)"), pool) for c in cands):
                    fails.append(f"{path} = {v!r}: that time is not in the hours text the checker read")
                continue
            if leaf == "addressCountry":
                notes.append(f"{path} = {v!r} is a country code; confirm the address or phone shows that country")
                continue
            if leaf == "addressRegion":
                notes.append(f"{path} = {v!r}: include a region only if the site writes one (a post town is addressLocality)")
            if re.match(r"https?://", v):
                if v.rstrip("/").lower() not in urls_n and not has(v):
                    fails.append(f"{path} = {v!r} is not a page or image URL the checker read; leave it out or ask the owner")
                continue
            if path.endswith("telephone"):
                if v not in site_phones and not has(v):
                    fails.append(f"{path} = {v!r} is not written this way on the site; copy the number exactly as the site shows it")
                continue
            if leaf == "email" or "@" in v:
                if not has(v):
                    fails.append(f"{path} = {v!r} is not an email shown on the pages checked")
                continue
            if re.fullmatch(r"-?\d+(\.\d+)?", v) and len(v.replace("-", "").replace(".", "")) <= 3:
                continue  # small numbers (e.g. a count) are not checked
            if not has(v):
                fails.append(f"{path} = {v!r} was not found word for word in the text the checker read; "
                             "use the site's own wording or leave it out")
    print(json.dumps({"ok": not fails, "types": t, "fails": fails, "notes": notes, "recommended_missing": missing_rec,
                      "checked": "valid JSON, required fields present, and each value found in the text the checker read "
                                 "(not that it sits in the right field: read the notes)",
                      "note": "Confirm with the Schema Markup Validator (validator.schema.org) and Google's Rich Results Test."},
                     indent=1, ensure_ascii=False))
    sys.exit(1 if fails else 0)


# ---------- phase 2: competitor gap and article refresh ----------
STOP = set("""about above after again against also among and another any are around because been before being below
between both but can cannot could did does doing down during each few for from further had has have having her here hers
him his how into its itself just more most much must not now off once only other our ours out over own same she should
some such than that the their them then there these they this those through too under until upon very was were what
when where which while who whom why will with within without would you your yours yourself what's how's why's who's
we're you're it's can't don't won't get got make made use used using also like need needs want one two three four five
best top guide page site home welcome read learn click here more info information""".split())


def terms(s):
    out = []
    for w in re.findall(r"[a-z][a-z0-9'-]{2,}", (s or "").lower()):
        w = w.strip("'-")
        if len(w) < 4 or w in STOP:
            continue
        out.append(w)
    return list(dict.fromkeys(out))


def stem(w):
    for suf in ("ies", "es", "s", "ing", "ed"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def outline(h):
    out = []
    for lvl, inner in re.findall(r"(?is)<h([1-4])\b[^>]*>(.*?)</h\1>", h or ""):
        t = re.sub(r"[\u200b-\u200f\u2060\ufeff]", "", strip_tags(inner)).strip()
        if t:
            out.append({"level": int(lvl), "text": t})
    return out


def faq_questions(objs):
    qs = []
    for o in objs:
        if "Question" in types(o) and isinstance(o.get("name"), str):
            qs.append(o["name"].strip())
        for m in (o.get("mainEntity") or []) if isinstance(o.get("mainEntity"), list) else []:
            if isinstance(m, dict) and "Question" in types(m) and isinstance(m.get("name"), str):
                qs.append(m["name"].strip())
    return list(dict.fromkeys(qs))


def _page_for_gap(u, role):
    pf = page_facts(u, keep_html=True)
    h = pf.pop("_html", "")
    if not h:
        return {"role": role, "url": u, "status": pf.get("status"), "error": pf.get("error") or "not read", "read": False}
    body = pf.get("visible_text", "")
    ol = outline(h)
    qs = [x["text"] for x in ol if x["text"].endswith("?")] + faq_questions(pf.get("jsonld", []))
    return {"role": role, "url": pf.get("final_url") or u, "status": pf.get("status"), "read": True, "title": pf.get("title"),
            "words_in_body": pf.get("words_in_body"), "outline": ol[:80], "questions": list(dict.fromkeys(qs))[:40],
            "jsonld_types": pf.get("jsonld_types"), "text": body, "text_truncated": pf.get("visible_text_truncated")}


def cmd_gap(urls, out_file=None):
    pages = [_page_for_gap(u if re.match(r"https?://", u) else "https://" + u, "yours" if i == 0 else f"competitor {i}")
             for i, u in enumerate(urls)]
    yours = pages[0]
    ytext = (yours.get("text") or "").lower() + " " + " ".join(x["text"] for x in yours.get("outline", [])).lower()
    ystems = {stem(w) for w in terms(ytext)}
    comps = []
    for p in pages[1:]:
        if not p["read"]:
            continue
        rows = []
        items = [(x["level"], x["text"]) for x in p["outline"] if x["level"] >= 2] + \
                [(0, q) for q in p["questions"] if q not in {x["text"] for x in p["outline"]}]
        for lvl, t in items:
            ts = terms(t)
            if not ts:
                continue
            found = [w for w in ts if stem(w) in ystems]
            rows.append({"heading": t, "level": lvl or "FAQ", "terms": ts, "terms_on_your_page": found,
                         "terms_missing": [w for w in ts if w not in found], "coverage": round(len(found) / len(ts), 2)})
        comps.append({"competitor": p["url"], "headings_compared": len(rows),
                      "low_coverage": [r for r in rows if r["coverage"] < 0.5], "all": rows})
    full = {"pages": pages, "comparison": comps,
            "note": "Coverage is a word match between each competitor heading and your page's text and headings (not meaning). "
                    "A low score means 'probably not covered': confirm with `find` before calling it a gap. "
                    "No search volume, ranking or backlink data: none of these pages' rankings are known."}
    if out_file:
        open(out_file, "w", encoding="utf-8").write(json.dumps(full, indent=1, ensure_ascii=False))
    show = json.loads(json.dumps(full))
    for p in show["pages"]:
        if p.get("text") and len(p["text"]) > 6000:
            p["text"] = p["text"][:6000]
            p["text_shown_here"] = "first 6000 characters; the --out file has up to 30000"
    print(json.dumps(show, indent=1, ensure_ascii=False))
    if out_file:
        print(f"saved: {out_file}")


def cmd_find(gap_file, phrases):
    d = json.load(open(gap_file, encoding="utf-8"))
    out = []
    for ph in phrases:
        row = {"phrase": ph, "pages": []}
        rx = re.compile(r"(?<![\w])" + re.escape(ph.lower()) + r"(?![\w])")
        for p in d["pages"]:
            if not p.get("read"):
                row["pages"].append({"role": p["role"], "url": p["url"], "not_read": p.get("error")})
                continue
            txt = (p.get("text") or "") + " \n " + " \n ".join(x["text"] for x in p.get("outline", []))
            low = txt.lower()
            hits = [m.start() for m in rx.finditer(low)]
            row["pages"].append({"role": p["role"], "url": p["url"], "count": len(hits),
                                 "examples": [re.sub(r"\s+", " ", txt[max(0, i - 80): i + len(ph) + 80]).strip() for i in hits[:2]]})
        out.append(row)
    print(json.dumps({"find": out, "note": "Exact phrase, any case, whole words, in the text and headings the checker read."},
                     indent=1, ensure_ascii=False))


AI_PHRASES = ["delve", "delves", "delving", "tapestry", "testament", "realm", "embark", "navigate the", "navigating the",
              "in today's fast-paced", "in today's digital", "ever-evolving", "ever-changing", "it's important to note",
              "it is important to note", "it's worth noting", "game-changer", "game changer", "unlock", "unleash", "elevate",
              "seamless", "seamlessly", "robust", "leverage", "harness the power", "look no further", "in conclusion",
              "furthermore", "moreover", "comprehensive guide", "ultimate guide", "dive into", "dive deep", "deep dive",
              "whether you're", "when it comes to", "plays a crucial role", "crucial role", "pivotal", "landscape",
              "cutting-edge", "transformative", "foster", "bustling", "vibrant", "nestled", "myriad", "plethora",
              "streamline", "empower", "a testament to", "rest assured", "at the end of the day"]
STAT = re.compile(r"(?i)([£$€]\s?\d[\d,.]*\s*(?:k|m|bn|million|billion)?|\d[\d,.]*\s*(?:%|per ?cent|percent)|"
                  r"\d[\d,.]*\s*(?:million|billion|thousand)|\d[\d,.]*\s*(?:times|x)\b|\b\d+\s+(?:in|out of)\s+\d+\b)")
ATTRIB = re.compile(r"(?i)\b(according to|survey|study|studies|report|research|data from|source|statistics from|found that|"
                    r"published by|reported by|census|ons|office for national statistics|gov\.uk|bureau of)\b")


def _blocks(h, host):
    """Paragraph-like blocks in document order: text, links out (other hosts), links in."""
    body = (re.search(r"(?is)<body\b.*?</body>", h) or [h])[0]
    body = re.sub(r"(?is)<(script|style|noscript|svg|template|iframe|nav|footer|header|form|aside)\b[^>]*>.*?</\1>", " ", body)
    # Prefer the article itself (or the main column) over the whole page: sidebars and "latest news" lists are not the article.
    arts = re.findall(r"(?is)<article\b[^>]*>.*?</article>", body)
    main = re.findall(r"(?is)<main\b[^>]*>.*?</main>", body)
    if arts:
        body = max(arts, key=len)
    elif main:
        body = max(main, key=len)
    out = []
    for tag, inner in re.findall(r"(?is)<(p|li|blockquote|td|h[1-4])\b[^>]*>(.*?)</\1>", body):
        t = strip_tags(inner)
        if not t:
            continue
        hrefs = [attr(a, "href") or "" for a in re.findall(r"(?is)<a\b[^>]*>", inner)]
        ext = [x for x in hrefs if re.match(r"https?://", x) and urllib.parse.urlsplit(x).netloc.lower().replace("www.", "") != host]
        tg = tag.lower()
        if tg.startswith("h") and words(t) > 40:
            tg = "p"  # body text wrapped in a heading tag is still body text
        out.append({"tag": tg, "text": t, "links_out": ext[:5], "links": len(hrefs)})
    return out


def _dates(h, objs):
    d = {}
    for k in ("article:published_time", "article:modified_time", "og:updated_time"):
        v = meta(h, "property", k)
        if v:
            d[k] = v
    for o in objs:
        for k in ("datePublished", "dateModified"):
            if isinstance(o.get(k), str) and k not in d:
                d[k] = o[k]
    times = re.findall(r"(?is)<time\b[^>]*datetime=[\"']([^\"']+)", h)
    if times:
        d["time_tags"] = list(dict.fromkeys(times))[:5]
    return d


def cmd_article(src):
    now = time.gmtime().tm_year
    if os.path.isfile(src):
        text = open(src, encoding="utf-8").read()
        h, objs, info = "", [], {"source": "pasted text file", "file": src}
        blocks = [{"tag": "p", "text": re.sub(r"\s+", " ", b).strip(), "links_out": [], "links": 0}
                  for b in re.split(r"\n\s*\n", text) if b.strip()]
        body_text = " ".join(b["text"] for b in blocks)
        info.update({"words_in_body": words(body_text)})
    else:
        url = src if re.match(r"https?://", src) else "https://" + src
        pf = page_facts(url, keep_html=True)
        h = pf.pop("_html", "")
        if not h:
            print(json.dumps({"url": url, "status": pf.get("status"), "error": pf.get("error"),
                              "blocked_by_robots": pf.get("blocked_by_robots", False)}, indent=1, ensure_ascii=False))
            return
        objs = pf.get("jsonld", [])
        host = urllib.parse.urlsplit(pf.get("final_url") or url).netloc.lower().replace("www.", "")
        blocks = _blocks(h, host)
        body_text = " ".join(b["text"] for b in blocks)
        info = {"url": pf.get("final_url") or url, "status": pf.get("status"), "title": pf.get("title"),
                "title_characters": pf.get("title_characters"), "meta_description": pf.get("meta_description"),
                "h1": pf.get("h1"), "words_in_body": words(body_text), "dates_in_markup": _dates(h, objs),
                "jsonld_types": pf.get("jsonld_types"), "internal_links": pf.get("internal_links"),
                "external_links": pf.get("external_links")}
    low = body_text.lower().replace("\u2019", "'").replace("\u2018", "'")
    title = (info.get("title") or "") + " " + " ".join(info.get("h1") or [])
    years = {}
    for m in re.finditer(r"(?<![\d/.-])(19[5-9]\d|20[0-4]\d)(?![\d/])", body_text + " " + title):
        y = int(m.group(1))
        src_txt = body_text + " " + title
        years.setdefault(y, []).append(re.sub(r"\s+", " ", src_txt[max(0, m.start() - 70): m.end() + 50]).strip())
    year_rows = [{"year": y, "count": len(v), "older_than_this_year": y < now, "in_title_or_h1": str(y) in title,
                  "examples": v[:3]} for y, v in sorted(years.items())]
    stats = []
    for i, b in enumerate(blocks):
        for sent in re.split(r"(?<=[.!?])\s+", b["text"]):
            if STAT.search(sent):
                stats.append({"sentence": sent[:300], "block": i, "link_out_in_paragraph": b["links_out"][:3],
                              "attribution_words": sorted({m.group(1).lower() for m in ATTRIB.finditer(sent)})})
    phr = []
    for ph in AI_PHRASES:
        n = len(re.findall(r"(?<![\w])" + re.escape(ph) + r"(?![\w])", low))
        if n:
            phr.append({"phrase": ph, "count": n})
    w = max(1, words(body_text))
    intro = []
    for b in blocks:
        if b["tag"].startswith("h") and b["tag"] != "h1" and intro:
            break
        if not intro and words(b["text"]) < 8:
            continue  # share buttons, bylines and labels before the first real paragraph
        if b["tag"] in ("p", "li", "blockquote"):
            intro.append(b["text"])
        if words(" ".join(intro)) >= 160:
            break
    if words(" ".join(intro)) > 160:  # one long block: take whole sentences up to about 60 words
        cut = []
        for sent in re.split(r"(?<=[.!?])\s+", " ".join(intro)):
            cut.append(sent)
            if words(" ".join(cut)) >= 60:
                break
        intro = cut
    heads = [b["text"] for b in blocks if b["tag"] in ("h2", "h3", "h4")]
    out = {**info, "checked_on": time.strftime("%Y-%m-%d", time.gmtime()), "this_year": now,
           "years_mentioned": year_rows,
           "stat_sentences": stats[:40], "stat_sentences_total": len(stats),
           "stat_sentences_with_no_link_or_attribution": sum(1 for x in stats if not x["link_out_in_paragraph"] and not x["attribution_words"]),
           "ai_sounding_phrases": phr, "ai_sounding_total": sum(x["count"] for x in phr),
           "ai_sounding_per_1000_words": round(1000 * sum(x["count"] for x in phr) / w, 1),
           "em_dashes": body_text.count("—"),
           "intro": " ".join(intro), "intro_words": words(" ".join(intro)),
           "headings": heads[:60], "question_headings": [x for x in heads if x.endswith("?")],
           "faqpage_markup": "FAQPage" in (info.get("jsonld_types") or []),
           "body_text": body_text[:30000], "body_text_truncated": len(body_text) > 30000,
           "note": "The phrase list is our own list of words that often mark machine-written or padded text; a count is a signal, "
                   "not proof. 'Link or attribution' only looks inside the same paragraph. Navigation, header and footer text "
                   "are left out of the body."}
    print(json.dumps(out, indent=1, ensure_ascii=False))


NUM_WORDS = ("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
             "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion half "
             "twice double triple quarter third most majority minority").split()
HEDGES = ["up to", "about", "around", "nearly", "almost", "as many as", "may", "might", "could", "estimated",
          "approximately", "roughly", "likely", "believes", "according to"]
NUM_WORDS += "hundreds thousands millions billions dozen dozens all every many few several none".split()
HEDGES += ["some", "often", "usually", "typically", "sometimes", "generally", "say", "says", "said", "suggests", "can"]
# words that add authority, proof or results: new ones are claims, not rewording
CLAIM_WORDS = set("""written experts expert accountants accountant lawyers doctors dentists certified accredited award awards
award-winning proven guaranteed guarantee official officially licensed qualified trusted leading best fastest cheapest
number-one tested verified approved endorsed recommended research-backed scientifically clinically studies study
research survey data statistics results always never everyone nobody""".split())


def _fact_tokens(t):
    nums = set(re.findall(r"[£$€]?\d[\d,.]*%?", t))
    nums = {n.rstrip(".,") for n in nums if n.rstrip(".,")}
    low = t.lower().replace("\u2019", "'")
    nums |= {w for w in NUM_WORDS if re.search(r"(?<![\w-])" + w + r"(?![\w-])", low)}
    names = set()
    for m in re.finditer(r"(?<![.!?]\s)(?<!^)\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)", t):
        names.add(m.group(1))
    return nums, names


def cmd_keep(original, new):
    a = open(original, encoding="utf-8").read() if os.path.isfile(original) else original
    b = open(new, encoding="utf-8").read() if os.path.isfile(new) else new
    na, ca = _fact_tokens(a)
    nb, cb = _fact_tokens(b)
    al, bl = a.lower().replace("\u2019", "'"), b.lower().replace("\u2019", "'")
    has = lambda w, t: re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", t) is not None
    def hedge_in(h, t):
        if h == "can":  # a question ("Can I book...?", "can you") is not a hedge
            return re.search(r"(?<![\w-])can(?![\w-])(?!\s+(?:i|you|we|they|he|she|it|my|your|our)\b)", t) is not None
        return has(h, t)
    hedges_dropped = [h for h in HEDGES if hedge_in(h, al) and not hedge_in(h, bl)]
    new_names = sorted(x for x in cb - ca if x.lower() not in al)
    # content words the original never uses: not a failure (rewording is expected), but each must be wording, not a new claim
    stem5 = lambda w: w[:6]
    a_stems = {stem5(w) for w in re.findall(r"[a-z]{4,}", al)}
    new_words = sorted({w for w in re.findall(r"[a-z]{5,}", bl) if w not in STOP and stem5(w) not in a_stems})
    claims = sorted({w for w in re.findall(r"[a-z][a-z-]+", bl) if w in CLAIM_WORDS and not has(w, al)})
    out = {"numbers_in_new_not_in_original": sorted(nb - na), "numbers_dropped": sorted(na - nb),
           "names_in_new_not_in_original": new_names, "hedges_dropped": hedges_dropped,
           "claim_words_added": claims,
           "words_not_in_original": new_words[:40],
           "ai_sounding_in_new": [p for p in AI_PHRASES if has(p, bl)],
           "em_dashes_in_new": b.count("\u2014"),
           "words": {"original": words(a), "new": words(b)},
           "ok": not (nb - na) and not new_names and not hedges_dropped and not claims,
           "note": "Numbers (digits or words such as 'forty', 'twice', 'most'), names and hedges ('up to', 'may', 'estimated', "
                   "'according to'...) must carry over from the original, and no authority or proof word ('written by experts', "
                   "'proven', 'certified') may be added. 'words_not_in_original' is for you to read: each must be "
                   "plain rewording, never a new claim (who wrote it, results, credentials). Dropped numbers are listed so you can "
                   "say why they went."}
    print(json.dumps(out, indent=1, ensure_ascii=False))

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    c = a[0]
    if c == "facts" and len(a) >= 2:
        print(json.dumps(page_facts(a[1]), indent=1, ensure_ascii=False))
    elif c == "count" and len(a) >= 2:
        cmd_count(a[1:])
    elif c == "ai" and len(a) >= 2:
        cmd_ai(a[1])
    elif c == "local" and len(a) >= 2:
        cmd_local(a[1], a[a.index("--out") + 1] if "--out" in a else None)
    elif c == "gap" and len(a) >= 3:
        rest = [x for x in a[1:] if x != "--out"]
        out = a[a.index("--out") + 1] if "--out" in a else None
        cmd_gap([x for x in rest if x != out], out)
    elif c == "find" and len(a) >= 3:
        cmd_find(a[1], a[2:])
    elif c == "article" and len(a) >= 2:
        cmd_article(a[1])
    elif c == "keep" and len(a) >= 3:
        cmd_keep(a[1], a[2])
    elif c == "schema-check" and len(a) >= 2:
        facts = a[a.index("--facts") + 1] if "--facts" in a else None
        cmd_schema_check(a[1], facts, fragment="--fragment" in a)
    else:
        print(__doc__); sys.exit(1)


if __name__ == "__main__":
    main()
