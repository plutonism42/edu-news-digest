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


BLACKLIST_KEYWORDS = [
    "소개", "연혁", "오시는길", "찾아오시는", "조직도", "조직 안내", "조직·부서",
    "사이트맵", "site map", "이용약관", "개인정보", "저작권", "채용정보", "채용실태",
    "직원검색", "업무협정기관", "CI", "슬로건", "캐릭터", "서체", "일반현황",
    "비전 및 목표", "민원", "FAQ", "자주묻는질문", "자주 묻는 질문", "국민콜",
    "영문홈페이지", "ENGLISH", "페이스북", "트위터", "유튜브", "카카오스토리",
    "네이버 블로그", "네이버 밴드", "바로가기", "홈페이지 바로가기",
    "API신청", "의견조사", "알림·참여",
]


# 제목 뒤에 흔히 따라붙는 부가정보 (이 단어가 나오면 그 이전까지만 제목으로 인정)
JUNK_MARKERS = [
    "첨부파일", "조회수", "작성자", "등록일", "작성부서", "담당부서",
    "new", "New", "NEW", "hit", "Hit", "HIT", "조회", "다운로드",
]


def _clean_title(title: str) -> str:
    t = title.strip()
    cut_positions = [t.find(marker) for marker in JUNK_MARKERS if t.find(marker) > 0]
    if cut_positions:
        t = t[:min(cut_positions)].strip()
    return t


def _is_menu_link(title: str) -> bool:
    t = title.strip()
    if len(t) < 6:  # 너무 짧은 제목은 대부분 메뉴 이름
        return True
    return any(kw in t for kw in BLACKLIST_KEYWORDS)


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
        title = _clean_title(title)
        if not title or _is_menu_link(title):
            continue

        link = urljoin(source["base_url"], a_tag["href"])
        if link in seen_links:
            continue
        seen_links.add(link)

        row_text = el.get_text(" ", strip=True)
        published_dt = _find_date_in_text(row_text)

        # 날짜를 못 찾으면 진짜 공지가 아닐 가능성이 높아 제외
        if not published_dt:
            continue
        if published_dt < cutoff:
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
