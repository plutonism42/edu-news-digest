# -*- coding: utf-8 -*-
"""
RSS가 없는 기관 게시판을 크롤링합니다.
사이트마다 HTML 구조가 달라서, 우선은 '날짜 패턴이 붙은 링크'를 찾는
범용(휴리스틱) 방식으로 동작합니다. 정확도가 필요한 사이트는
SITE_SPECIFIC 안에 개별 파서를 추가해서 덮어씁니다.
"""
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EduNewsDigestBot/1.0; +for personal use)"
}

DATE_PATTERNS = [
    (r"(20\d{2})[.\-/](\d{1,2})[.\-/](\d{1,2})", "%Y-%m-%d"),  # 2026.08.09 / 2026-08-09
    (r"(\d{2})[.\-/](\d{1,2})[.\-/](\d{1,2})", "%y-%m-%d"),    # 26.08.09
]


def _find_date_in_text(text: str):
    for pattern, _ in DATE_PATTERNS:
        m = re.search(pattern, text)
        if m:
            try:
                y, mo, d = m.groups()
                y = int(y) if len(y) == 4 else 2000 + int(y)
                return datetime(y, int(mo), int(d), tzinfo=timezone.utc)
            except Exception:
                continue
    return None


def scrape_board_generic(source: dict, window_hours: int, max_items: int = 15) -> list:
    """
    source: {"name", "category", "list_url", "base_url"}
    게시판 목록 페이지에서 제목+링크+(있으면)날짜를 긁어옵니다.
    """
    items = []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)

    try:
        resp = requests.get(source["list_url"], headers=HEADERS, timeout=15)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
    except Exception as e:
        print(f"[크롤링 오류] {source['name']}: {e}")
        return items

    soup = BeautifulSoup(resp.text, "html.parser")

    # 게시판은 보통 목록이 <li> 또는 <tr> 단위로 구성됨
    candidates = soup.select("li, tr")

    seen_links = set()
    for el in candidates:
        a_tag = el.find("a")
        if not a_tag or not a_tag.get("href"):
            continue

        title = a_tag.get_text(strip=True)
        if not title or len(title) < 4:
            continue

        link = urljoin(source["base_url"], a_tag["href"])
        if link in seen_links:
            continue
        seen_links.add(link)

        row_text = el.get_text(" ", strip=True)
        published_dt = _find_date_in_text(row_text)

        # 날짜를 못 찾으면 일단 포함(추후 확인 필요 항목으로 표시)
        if published_dt and published_dt < cutoff:
            continue

        items.append({
            "title": title,
            "link": link,
            "source": source["name"],
            "category": source["category"],
            "published": published_dt.isoformat() if published_dt else None,
        })

        if len(items) >= max_items:
            break

    return items


def scrape_all_boards(board_sources: list, window_hours: int) -> list:
    all_items = []
    for src in board_sources:
        found = scrape_board_generic(src, window_hours)
        print(f"[크롤링] {src['name']}: {len(found)}건 수집 (휴리스틱 - 검증 필요)")
        all_items.extend(found)
    return all_items
