#!/usr/bin/env python3
"""
Builds cbse-sample-papers.json: CBSE's Sample Question Papers (SQP) and Marking Schemes (MS) of the
newest session, for the Padhaku app's Sample Papers screen (latest syllabus only: older sessions are
dropped as soon as a newer one is published).

Sources (cbseacademic.nic.in, linked from https://www.cbse.gov.in/cbsenew/samplepaper.html):
  SQP_CLASSX_<session>.html, SQP_CLASSXII_<session>.html   main subjects, Classes 10 and 12
  skill-education-sqp.html                                 skill subjects, Classes 9-12

  python3 scripts/cbse-sqp/build.py            # writes cbse-sample-papers.json
  python3 scripts/cbse-sqp/build.py --sizes    # also asks CBSE for each file's size

cbseacademic.nic.in uses an emSign certificate some systems don't trust; emsign-root-g1.pem (the official
emSign Root CA - G1, SHA-256 40:F6:AF:03:46:A9:9A:A1:CD:1D:55:5A:4E:9C:CE:62:C7:F9:63:46:03:EE:40:66:15:83:3D:C8:C8:D0:03:67)
is added to the system's trusted roots for these requests only.
"""
import datetime
import html
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

BASE = "https://cbseacademic.nic.in/"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "cbse-sample-papers.json")


def context():
    ctx = ssl.create_default_context()
    ctx.load_verify_locations(os.path.join(HERE, "emsign-root-g1.pem"))
    if os.environ.get("SSL_CERT_FILE"):
        ctx.load_verify_locations(os.environ["SSL_CERT_FILE"])
    return ctx


CTX = context()


def fetch(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 (Padhaku sample papers list)"})
    with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
        return r.status, r.headers, (r.read() if method == "GET" else b"")


def page(name):
    try:
        status, _, body = fetch(BASE + name)
        return body.decode("utf-8", "replace") if status == 200 else None
    except Exception:
        return None


def clean(text):
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def sessions():
    """Candidate sessions, newest first: next year's, this year's and last year's (e.g. 2027-28, 2026-27, 2025-26)."""
    today = datetime.date.today()
    start = today.year if today.month >= 4 else today.year - 1
    return [f"{y}-{str(y + 1)[2:]}" for y in (start + 1, start, start - 1)]


IMPORTANT = ["English", "Hindi", "Science", "Mathematics", "Social Science", "Computer", "Informatics Practices",
             "Information Technology", "Artificial Intelligence", "Physics", "Chemistry", "Biology",
             "Applied Mathematics", "Accountancy", "Business Studies", "Economics", "History", "Political Science",
             "Geography", "Sanskrit", "Physical Education"]


def placeholder(link):
    return link.rsplit("/", 1)[-1].lower().startswith("error")


def main_papers():
    papers, used = [], None
    for session in sessions():
        found = []
        for grade, page_name in ((10, f"SQP_CLASSX_{session}.html"), (12, f"SQP_CLASSXII_{session}.html")):
            body = page(page_name)
            if not body or ".pdf" not in body:
                continue
            body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
            for row in re.findall(r"<tr[^>]*>(.*?)</tr>", body, flags=re.S | re.I):
                cells = re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S | re.I)
                if len(cells) < 3:
                    continue
                subject = clean(cells[0])
                # CBSE links a placeholder "error.pdf" for papers that are not out yet: skip those.
                sqp = [l for l in re.findall(r'href="([^"]+\.pdf)"', cells[1], flags=re.I) if not placeholder(l)]
                ms = [l for l in re.findall(r'href="([^"]+\.pdf)"', cells[2], flags=re.I) if not placeholder(l)]
                if subject and sqp:
                    found.append({"grade": grade, "subject": subject, "kind": "main",
                                  "sqp": BASE + sqp[0].lstrip("/"), "ms": (BASE + ms[0].lstrip("/")) if ms else ""})
        if found:
            papers, used = found, session
            break
    return used, papers


def skill_papers():
    body = page("skill-education-sqp.html")
    if not body:
        return None, []
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    m = re.search(r"Session\s*(\d{4}-\d{2})", body)
    session = m.group(1) if m else None
    papers = []
    for item in re.findall(r"<li>(.*?)</li>", body, flags=re.S | re.I):
        links = re.findall(r'href="([^"]+\.pdf)"', item, flags=re.I)
        if not links:
            continue
        grade_m = re.search(r"SQP_MS_(IX|XII|XI|X)/", links[0])
        if not grade_m:
            continue
        grade = {"IX": 9, "X": 10, "XI": 11, "XII": 12}[grade_m.group(1)]
        name = clean(item.split("<br")[0])
        sqp = next((l for l in links if re.search(r"SQP", l.rsplit("/", 1)[-1], re.I)), links[0])
        ms = next((l for l in links if re.search(r"_MS", l.rsplit("/", 1)[-1], re.I)), "")
        papers.append({"grade": grade, "subject": skill_name(name),
                       "kind": "skill", "sqp": BASE + sqp.lstrip("/"), "ms": (BASE + ms.lstrip("/")) if ms else ""})
    return session, papers


KEEP_UPPER = {"AI", "IT", "ITES", "NCC", "HR", "MS", "GST"}
SMALL = {"and", "of", "to", "in", "for", "the", "&"}


def skill_name(raw):
    """'402-INFORMATION TECHNOLOGY' / '817 TYPOGRAPHY & COMPUTER APPLICATIONS' -> 'Information Technology (402)'."""
    m = re.match(r"^\s*(\d{3})\s*[-–:]?\s*(.+?)\s*$", raw) or re.match(r"^\s*(.+?)\s*\(?(\d{3})\)?\s*$", raw)
    if not m:
        return raw
    code, title = (m.group(1), m.group(2)) if m.group(1).isdigit() else (m.group(2), m.group(1))
    words = []
    for i, w in enumerate(re.split(r"\s+", title.replace("-", " "))):
        if w.upper() in KEEP_UPPER:
            words.append(w.upper())
        elif i and w.lower() in SMALL:
            words.append(w.lower())
        else:
            words.append(w[:1].upper() + w[1:].lower())
    return f"{' '.join(words)} ({code})"


def mirror_name(url, grade):
    """Name of our GitHub copy: class + CBSE's file name (the same name exists for several classes)."""
    return f"c{grade}-" + re.sub(r"[^A-Za-z0-9._-]+", "_", url.rsplit("/", 1)[-1])


def main():
    with_sizes = "--sizes" in sys.argv
    session, papers = main_papers()
    skill_session, skills = skill_papers()
    if not papers and not skills:
        sys.exit("No sample papers found: cbseacademic.nic.in may be down or its pages changed.")
    items, missing = [], []
    for p in sorted(papers + skills, key=lambda p: (p["grade"], p["kind"] != "main", p["subject"].lower())):
        broken = False
        for key in ("sqp", "ms"):
            if p[key]:
                p[key + "File"] = mirror_name(p[key], p["grade"])
                if with_sizes:
                    try:
                        _, headers, _ = fetch(p[key], "HEAD")
                        p[key + "Size"] = int(headers.get("Content-Length") or 0)
                    except urllib.error.HTTPError as e:
                        if e.code in (404, 410):
                            # CBSE lists it but the file is gone: leave the paper (or just its scheme) out.
                            missing.append(p[key])
                            if key == "sqp":
                                broken = True
                            else:
                                p["ms"], p.pop("msFile", None)
                        p[key + "Size"] = 0
                    except Exception:
                        p[key + "Size"] = 0
        if not broken:
            items.append(p)
    data = {
        "session": session or skill_session,
        "skillSession": skill_session,
        "updated": datetime.date.today().isoformat(),
        "source": "CBSE Sample Question Papers and Marking Schemes, cbseacademic.nic.in",
        # The app shows these subjects first (name starts with the entry), then the rest A–Z.
        "important": IMPORTANT,
        "papers": items,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    if missing:
        print(f"Left out {len(missing)} files that CBSE lists but cannot be downloaded (404).")
    print(f"{len(items)} papers ({len(papers)} main, {len(skills)} skill), session {data['session']} → cbse-sample-papers.json")


if __name__ == "__main__":
    main()
