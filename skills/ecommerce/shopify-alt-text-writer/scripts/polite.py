"""Polite, honest fetching for this skill's helper scripts (standard library only).

Every request:
  - sends one honest user agent that names this helper (no browser user agent, ever);
  - obeys the site's robots.txt for that agent, read the way RFC 9309 says:
      2xx            -> follow the rules (the group naming this helper, else "*")
      4xx (incl 404) -> no rules: everything allowed
      5xx, timeout, DNS or TLS failure -> treat the whole site as disallowed
    Group matching is by exact product token, ignoring case; the longest matching rule wins and
    Allow wins a tie; "*" and "$" work as in RFC 9309;
  - waits at least 1 second between requests to the same host, and backs off on 429 and 5xx.

A blocked URL raises RobotsDisallowed. Scripts print it as an error that tells the model to stop
and ask the merchant to paste the text instead. Nothing here may be bypassed by fetching some other way.

This file is identical in every skill that ships it (checked by ops/audits/check_polite.py).
"""
import re
import time
import urllib.error
import urllib.parse
import urllib.request

INFO_URL = "https://proskillpacks.github.io"
_robots = {}      # "scheme://host" -> list of (allow, pattern) for this agent, or "CLOSED"
_last = {}        # host -> time of the last request


class RobotsDisallowed(Exception):
    pass


def user_agent(tool, version="1.0"):
    return f"{tool}/{version} (read-only helper run for a user; +{INFO_URL}; python-urllib)"


def _wait(host, gap=1.0):
    dt = time.time() - _last.get(host, 0)
    if dt < gap:
        time.sleep(gap - dt)
    _last[host] = time.time()


def _raw(url, ua, accept, timeout=30):
    host = urllib.parse.urlsplit(url).netloc
    _wait(host)
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": accept})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace"), r.geturl()


def parse_groups(txt):
    """[(agents, rules)], agents lower-case product tokens, rules [(allow, pattern)]."""
    groups, cur, in_rules = [], None, False
    for line in txt.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = (x.strip() for x in line.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            if cur is None or in_rules:
                cur = ([], [])
                groups.append(cur)
                in_rules = False
            cur[0].append(v.lower())
        elif k in ("allow", "disallow") and cur is not None:
            in_rules = True
            if v:
                cur[1].append((k == "allow", v))
    return groups


def rules_for(groups, token):
    token = token.lower()
    named = [r for agents, rules in groups if token in agents for r in rules]
    if any(token in agents for agents, _ in groups):
        return named
    return [r for agents, rules in groups if "*" in agents for r in rules]


def _match(pattern, path):
    end = pattern.endswith("$")
    p = pattern[:-1] if end else pattern
    rx = "".join(".*" if c == "*" else re.escape(c) for c in p)
    return re.match(rx + ("$" if end else ""), path) is not None


def allowed_by(rules, path):
    best, allow = -1, True
    for is_allow, pat in rules:
        if _match(pat, path):
            n = len(pat)
            if n > best or (n == best and is_allow):
                best, allow = n, is_allow
    return allow


def robots_rules(base, tool):
    if base in _robots:
        return _robots[base]
    ua = user_agent(tool)
    try:
        status, body, _ = _raw(base + "/robots.txt", ua, "text/plain", timeout=20)
        rules = rules_for(parse_groups(body), tool) if 200 <= status < 300 else []
    except urllib.error.HTTPError as e:
        rules = [] if 400 <= e.code < 500 else "CLOSED"
    except Exception:
        rules = "CLOSED"
    _robots[base] = rules
    return rules


def check(url, tool):
    sp = urllib.parse.urlsplit(url)
    base = f"{sp.scheme}://{sp.netloc}"
    rules = robots_rules(base, tool)
    path = (sp.path or "/") + ("?" + sp.query if sp.query else "")
    if rules == "CLOSED":
        raise RobotsDisallowed(f"{base}/robots.txt could not be read (server error or no connection); "
                               f"under RFC 9309 that means the site is closed to {tool}. Don't fetch it another way: "
                               "ask the merchant to paste the text.")
    if not allowed_by(rules, path):
        raise RobotsDisallowed(f"robots.txt on {base} does not allow {tool} to read {path}. Don't fetch it another way: "
                               "ask the merchant to paste the text.")


def fetch(url, tool, accept="application/json", tries=4, timeout=30, owner=False):
    """(body, final_url). Raises RobotsDisallowed, urllib.error.HTTPError or URLError.

    owner=True skips the robots.txt check (never the honest user agent). Use it only when the user has said
    the site is their own store, or they have the owner's permission: robots.txt rules address crawlers,
    and a store owner may read their own pages."""
    if not owner:
        check(url, tool)
    ua = user_agent(tool)
    last = None
    for i in range(tries):
        try:
            status, body, final = _raw(url, ua, accept, timeout)
            if not owner and urllib.parse.urlsplit(final).netloc != urllib.parse.urlsplit(url).netloc:
                check(final, tool)
            return body, final
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503, 504) and i < tries - 1:
                ra = e.headers.get("Retry-After", "") if e.headers else ""
                time.sleep(min(int(ra), 30) if ra.isdigit() else 2 * (i + 1))
                continue
            raise
        except urllib.error.URLError as e:
            last = e
            time.sleep(1 + i)
    raise last
