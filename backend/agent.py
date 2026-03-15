import requests
import json
from typing import Iterable
from typing import List, Dict
import xml.etree.ElementTree as ET

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def _llama_generate(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt
        },
        stream=True
    )

    result = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            result += data.get("response", "")

    return result.strip()

def _llama_stream(prompt: str) -> Iterable[str]:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
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
            })
        return items
    except Exception:
        return []


def monitor_platforms(query: str) -> str:
    sources = {
        "Hacker News": "https://hnrss.org/frontpage",
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
    }

    collected = []
    for name, url in sources.items():
        items = _fetch_rss(url, limit=4)
        for it in items:
            collected.append(f"[{name}] {it['title']} - {it['link']}")

    gh_items = _github_search(query, limit=5)
    for it in gh_items:
        collected.append(f"[GitHub] {it['title']} - {it['link']}")

    if not collected:
        return "No live items found. Check your internet connection."

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
        "LIVE ITEMS:\n"
        + "\n".join(collected)
    )
    return _llama_generate(prompt)


def monitor_platforms_stream(query: str) -> Iterable[str]:
    sources = {
        "Hacker News": "https://hnrss.org/frontpage",
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
    }

    collected = []
    for name, url in sources.items():
        items = _fetch_rss(url, limit=4)
        for it in items:
            collected.append(f"[{name}] {it['title']} - {it['link']}")

    gh_items = _github_search(query, limit=5)
    for it in gh_items:
        collected.append(f"[GitHub] {it['title']} - {it['link']}")

    if not collected:
        yield "No live items found. Check your internet connection."
        return

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
        "LIVE ITEMS:\n"
        + "\n".join(collected)
    )
    yield from _llama_stream(prompt)
