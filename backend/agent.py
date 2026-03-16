import requests
import json
import re
import time
from typing import Iterable
from typing import List, Dict, Tuple
import xml.etree.ElementTree as ET
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
SOURCES_PATH = Path(__file__).resolve().parent / "sources.json"
REQUEST_TIMEOUT = 30
RETRY_COUNT = 2
RETRY_BACKOFF = 1.0


def _load_sources() -> Dict:
    try:
        return json.loads(SOURCES_PATH.read_text())
    except Exception:
        return {
            "rss": [
                {"name": "Hacker News", "url": "https://hnrss.org/frontpage", "enabled": True},
                {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "enabled": True},
                {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "enabled": True},
            ],
            "github": {"enabled": True},
        }


def _post_with_retry(payload: Dict) -> requests.Response:
    last_err = None
    for attempt in range(RETRY_COUNT + 1):
        try:
            resp = requests.post(
                OLLAMA_URL,
                json=payload,
                stream=True,
                timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            return resp
        except Exception as e:
            last_err = e
            if attempt < RETRY_COUNT:
                time.sleep(RETRY_BACKOFF * (attempt + 1))
                continue
            raise last_err


def _llama_generate(prompt: str) -> str:
    response = _post_with_retry({
        "model": MODEL_NAME,
        "prompt": prompt
    })

    result = ""
    for line in response.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        result += data.get("response", "")

    return result.strip()

def _llama_stream(prompt: str) -> Iterable[str]:
    response = _post_with_retry({
        "model": MODEL_NAME,
        "prompt": prompt
    })

    for line in response.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        chunk = data.get("response", "")
        if chunk:
            yield chunk


def vc_scout(goal: str) -> str:
    prompt = (
        "You are a VC analyst. Analyze the following goal.\n"
        f"Goal: {goal}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable fact or claim>\n"
        "  Inference: <what it suggests>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Final Verdict\n"
        "- Strengths: <bullets>\n"
        "- Risks: <bullets>\n"
        "- Recommendation: <one line>\n"
    )
    return _llama_generate(prompt)


def vc_scout_stream(goal: str) -> Iterable[str]:
    prompt = (
        "You are a VC analyst. Analyze the following goal.\n"
        f"Goal: {goal}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable fact or claim>\n"
        "  Inference: <what it suggests>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Final Verdict\n"
        "- Strengths: <bullets>\n"
        "- Risks: <bullets>\n"
        "- Recommendation: <one line>\n"
    )
    return _llama_stream(prompt)


def trend_detection(topic: str) -> str:
    prompt = (
        "You are a trend analyst. Analyze the following topic.\n"
        f"Topic/Sector: {topic}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the trend>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Trend Output\n"
        "- Trend: <short name>\n"
        "  Why Now: <brief>\n"
        "  Example Startup: <one idea>\n"
        "(Provide 5 trends)\n"
    )
    return _llama_generate(prompt)


def trend_detection_stream(topic: str) -> Iterable[str]:
    prompt = (
        "You are a trend analyst. Analyze the following topic.\n"
        f"Topic/Sector: {topic}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the trend>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Trend Output\n"
        "- Trend: <short name>\n"
        "  Why Now: <brief>\n"
        "  Example Startup: <one idea>\n"
        "(Provide 5 trends)\n"
    )
    return _llama_stream(prompt)


def startup_discovery(sector: str) -> str:
    prompt = (
        "You are a startup scout. Analyze the following sector.\n"
        f"Sector: {sector}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about opportunities>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Startup Concepts\n"
        "- Concept: <name>\n"
        "  Problem: <brief>\n"
        "  Solution: <brief>\n"
        "  Customer: <target user>\n"
        "  Moat: <brief>\n"
        "(Provide 6 concepts)\n"
    )
    return _llama_generate(prompt)


def startup_discovery_stream(sector: str) -> Iterable[str]:
    prompt = (
        "You are a startup scout. Analyze the following sector.\n"
        f"Sector: {sector}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about opportunities>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Startup Concepts\n"
        "- Concept: <name>\n"
        "  Problem: <brief>\n"
        "  Solution: <brief>\n"
        "  Customer: <target user>\n"
        "  Moat: <brief>\n"
        "(Provide 6 concepts)\n"
    )
    return _llama_stream(prompt)


def founder_interview(founder: str) -> str:
    prompt = (
        "You are a VC conducting a founder interview. Analyze the founder/company.\n"
        f"Founder and company: {founder}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the founder/company>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Interview Guide\n"
        "- Question: <sharp question>\n"
        "  Strong Answer: <short expected answer>\n"
        "(Provide 8 questions)\n"
    )
    return _llama_generate(prompt)


def founder_interview_stream(founder: str) -> Iterable[str]:
    prompt = (
        "You are a VC conducting a founder interview. Analyze the founder/company.\n"
        f"Founder and company: {founder}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the founder/company>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Interview Guide\n"
        "- Question: <sharp question>\n"
        "  Strong Answer: <short expected answer>\n"
        "(Provide 8 questions)\n"
    )
    return _llama_stream(prompt)


def investment_memo(company: str) -> str:
    prompt = (
        "You are a VC. Analyze the company/founder for an investment memo.\n"
        f"Company/Founder: {company}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the investment>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Investment Memo\n"
        "- Summary: <bullets>\n"
        "- Market: <bullets>\n"
        "- Product: <bullets>\n"
        "- Traction Assumptions: <bullets>\n"
        "- Risks: <bullets>\n"
        "- Recommendation: <one line>\n"
    )
    return _llama_generate(prompt)


def investment_memo_stream(company: str) -> Iterable[str]:
    prompt = (
        "You are a VC. Analyze the company/founder for an investment memo.\n"
        f"Company/Founder: {company}\n\n"
        "Provide a structured analysis WITHOUT revealing hidden chain-of-thought. "
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the investment>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Investment Memo\n"
        "- Summary: <bullets>\n"
        "- Market: <bullets>\n"
        "- Product: <bullets>\n"
        "- Traction Assumptions: <bullets>\n"
        "- Risks: <bullets>\n"
        "- Recommendation: <one line>\n"
    )
    return _llama_stream(prompt)


def _fetch_rss(url: str, limit: int = 5) -> List[Dict[str, str]]:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.text)
        items = []
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            if title:
                items.append({"title": title, "link": link})
            if len(items) >= limit:
                break
        return items
    except Exception:
        return []


def _github_search(query: str, limit: int = 5) -> List[Dict[str, str]]:
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": str(limit),
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = []
        for repo in data.get("items", [])[:limit]:
            items.append({
                "title": f"{repo.get('full_name', '').strip()} (★ {repo.get('stargazers_count', 0)})",
                "link": repo.get("html_url", "").strip(),
                "stars": repo.get("stargazers_count", 0),
            })
        return items
    except Exception:
        return []


def _strip_html(text: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _fetch_page_text(url: str, max_chars: int = 2000) -> str:
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "VC-Scout-Agent/1.0"})
        resp.raise_for_status()
        text = _strip_html(resp.text)
        return text[:max_chars]
    except Exception:
        return ""


def _extract_links(html: str, limit: int = 3) -> List[str]:
    links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html, flags=re.IGNORECASE)
    deduped = []
    seen = set()
    for link in links:
        if link in seen:
            continue
        seen.add(link)
        deduped.append(link)
        if len(deduped) >= limit:
            break
    return deduped


def _score_items(items: List[Dict[str, str]], query: str) -> List[Tuple[Dict[str, str], float]]:
    q_terms = [t.lower() for t in re.split(r"\W+", query) if t.strip()]
    scored = []
    for it in items:
        title = (it.get("title") or "").lower()
        source = it.get("source", "")
        stars = it.get("stars", 0) or 0
        score = 0.0
        if source == "GitHub":
            score += min(stars / 5000.0, 2.0)
        if source in ("Hacker News", "TechCrunch", "The Verge"):
            score += 0.6
        for term in q_terms:
            if term and term in title:
                score += 0.3
        scored.append((it, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def _forage_links(items: List[Dict[str, str]], max_items: int = 4, hop2_links: int = 2) -> List[Dict[str, str]]:
    findings = []
    for it in items[:max_items]:
        link = it.get("link", "")
        if not link:
            continue
        # Hop 1: fetch page text
        page_text = _fetch_page_text(link, max_chars=1500)
        if page_text:
            findings.append({"source": "hop1", "link": link, "snippet": page_text})
        # Hop 2: follow a couple of links from the page (best effort)
        try:
            resp = requests.get(link, timeout=10, headers={"User-Agent": "VC-Scout-Agent/1.0"})
            resp.raise_for_status()
            next_links = _extract_links(resp.text, limit=hop2_links)
            for l2 in next_links:
                text2 = _fetch_page_text(l2, max_chars=800)
                if text2:
                    findings.append({"source": "hop2", "link": l2, "snippet": text2})
        except Exception:
            continue
    return findings


def monitor_platforms(query: str) -> str:
    config = _load_sources()
    sources = {s["name"]: s["url"] for s in config.get("rss", []) if s.get("enabled")}

    collected = []
    for name, url in sources.items():
        items = _fetch_rss(url, limit=4)
        for it in items:
            collected.append({
                "source": name,
                "title": it["title"],
                "link": it["link"],
            })

    if config.get("github", {}).get("enabled", True):
        gh_items = _github_search(query, limit=5)
        for it in gh_items:
            collected.append({
                "source": "GitHub",
                "title": it["title"],
                "link": it["link"],
                "stars": it.get("stars", 0),
            })

    if not collected:
        return "No live items found. Check your internet connection."

    scored = _score_items(collected, query)
    top_items = [it for it, _ in scored[:8]]
    forage = _forage_links(top_items, max_items=4, hop2_links=2)

    scored_block = "\n".join(
        f"[{it.get('source')}] {it.get('title')} - {it.get('link')} (score: {score:.2f})"
        for it, score in scored
    )
    forage_block = "\n".join(
        f"[{f['source']}] {f['link']} :: {f['snippet'][:300]}"
        for f in forage
    )

    prompt = (
        "You are a VC analyst monitoring platforms. Based on the live items below, "
        "provide a structured analysis WITHOUT revealing hidden chain-of-thought.\n\n"
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the market>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Actionable Signals\n"
        "- Signal: <short name>\n"
        "  Why It Matters: <brief>\n"
        "  Opportunity: <actionable idea>\n"
        "(Provide 3-5 signals)\n\n"
        "LIVE ITEMS (ranked):\n"
        + scored_block
        + "\n\nFOLLOWED LINKS (multi-hop findings):\n"
        + (forage_block or "No additional links fetched.")
    )
    return _llama_generate(prompt)


def monitor_platforms_stream(query: str) -> Iterable[str]:
    config = _load_sources()
    sources = {s["name"]: s["url"] for s in config.get("rss", []) if s.get("enabled")}

    collected = []
    for name, url in sources.items():
        items = _fetch_rss(url, limit=4)
        for it in items:
            collected.append({
                "source": name,
                "title": it["title"],
                "link": it["link"],
            })

    if config.get("github", {}).get("enabled", True):
        gh_items = _github_search(query, limit=5)
        for it in gh_items:
            collected.append({
                "source": "GitHub",
                "title": it["title"],
                "link": it["link"],
                "stars": it.get("stars", 0),
            })

    if not collected:
        yield "No live items found. Check your internet connection."
        return

    scored = _score_items(collected, query)
    top_items = [it for it, _ in scored[:8]]
    forage = _forage_links(top_items, max_items=4, hop2_links=2)

    scored_block = "\n".join(
        f"[{it.get('source')}] {it.get('title')} - {it.get('link')} (score: {score:.2f})"
        for it, score in scored
    )
    forage_block = "\n".join(
        f"[{f['source']}] {f['link']} :: {f['snippet'][:300]}"
        for f in forage
    )

    prompt = (
        "You are a VC analyst monitoring platforms. Based on the live items below, "
        "provide a structured analysis WITHOUT revealing hidden chain-of-thought.\n\n"
        "Use this format:\n"
        "Header: Evidence Review\n"
        "- Data Point: <specific observable signal or claim>\n"
        "  Inference: <what it suggests about the market>\n"
        "  Confidence (0-100): <numeric>\n"
        "(Repeat 5-8 items)\n\n"
        "Header: Actionable Signals\n"
        "- Signal: <short name>\n"
        "  Why It Matters: <brief>\n"
        "  Opportunity: <actionable idea>\n"
        "(Provide 3-5 signals)\n\n"
        "LIVE ITEMS (ranked):\n"
        + scored_block
        + "\n\nFOLLOWED LINKS (multi-hop findings):\n"
        + (forage_block or "No additional links fetched.")
    )
    yield from _llama_stream(prompt)
