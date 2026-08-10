# -*- coding: utf-8 -*-
"""
NAVER API HUB(네이버 클라우드 플랫폼)의 뉴스 검색 API로
키워드 기반 최신 기사를 수집합니다.

2026년 7월 31일부로 기존 개발자센터(openapi.naver.com) 신규 신청이 막히고
NAVER API HUB(naverapihub.apigw.ntruss.com)로 이관되었습니다.
인증 헤더 이름이 예전과 다르니 주의하세요.
"""
import os
import re
import requests
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

NAVER_API_URL = "https://naverapihub.apigw.ntruss.com/search/v1/news"


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").replace("&quot;", '"').strip()


def collect_naver_news(keyword: str, category: str, window_hours: int, display: int = 20) -> list:
    client_id = os.environ.get("NAVER_CLIENT_ID")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("[네이버 API] 키가 설정되지 않아 건너뜁니다. (NAVER_CLIENT_ID / NAVER_CLIENT_SECRET)")
        return []

    # NAVER API HUB 인증 헤더 (예전 X-Naver-Client-Id 방식과 이름이 다름)
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
    }
    params = {
        "query": keyword,
        "display": display,
        "start": 1,
        "sort": "date",  # 최신순
        "format": "json",
    }

    try:
        resp = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[네이버 API 오류] '{keyword}': {e}")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    items = []
    for entry in data.get("items", []):
        try:
            pub_dt = parsedate_to_datetime(entry.get("pubDate", ""))
            if pub_dt.tzinfo is None:
                pub_dt = pub_dt.replace(tzinfo=timezone.utc)
        except Exception:
            pub_dt = None

        if pub_dt and pub_dt < cutoff:
            continue

        items.append({
            "title": _strip_tags(entry.get("title")),
            "link": entry.get("originallink") or entry.get("link"),
            "source": f"네이버뉴스 · '{keyword}'",
            "category": category,
            "published": pub_dt.isoformat() if pub_dt else None,
        })

    return items


def collect_all_naver(keywords: list, window_hours: int) -> list:
    all_items = []
    for keyword, category in keywords:
        found = collect_naver_news(keyword, category, window_hours)
        print(f"[네이버] '{keyword}': {len(found)}건 수집")
        all_items.extend(found)
    return all_items
