# -*- coding: utf-8 -*-
"""RSS 피드에서 지정된 시간 구간(window_start ~ window_end) 이내 게시물을 수집합니다."""
import feedparser
from datetime import datetime, timezone
from time import mktime


def collect_rss(source: dict, window_start: datetime, window_end: datetime) -> list:
    """
    source: {"name", "category", "url"}
    반환: [{"title", "link", "source", "category", "published"}]
    """
    items = []

    try:
        feed = feedparser.parse(source["url"])
    except Exception as e:
        print(f"[RSS 오류] {source['name']}: {e}")
        return items

    for entry in feed.entries:
        published_dt = None
        for key in ("published_parsed", "updated_parsed"):
            if getattr(entry, key, None):
                published_dt = datetime.fromtimestamp(
                    mktime(getattr(entry, key)), tz=timezone.utc
                )
                break

        # 날짜 정보가 없으면 일단 포함(안전하게), 있으면 구간(시작~끝) 필터 적용
        if published_dt and (published_dt < window_start or published_dt > window_end):
            continue

        items.append({
            "title": entry.get("title", "(제목 없음)").strip(),
            "link": entry.get("link", "").strip(),
            "source": source["name"],
            "category": source["category"],
            "published": published_dt.isoformat() if published_dt else None,
        })

    return items


def collect_all_rss(rss_sources: list, window_start: datetime, window_end: datetime) -> list:
    all_items = []
    for src in rss_sources:
        found = collect_rss(src, window_start, window_end)
        print(f"[RSS] {src['name']}: {len(found)}건 수집")
        all_items.extend(found)
    return all_items
