# -*- coding: utf-8 -*-
"""매일 실행되는 메인 파이프라인: 수집 -> 요약 -> 저장 -> HTML 생성(오늘자+아카이브)"""
import os
from datetime import datetime, timezone, timedelta
from config import (
    RSS_SOURCES, BOARD_SOURCES, NAVER_KEYWORDS,
    COLLECTION_WINDOW_HOURS,
)
from collectors.rss_collector import collect_all_rss
from collectors.board_scraper import scrape_all_boards
from collectors.naver_news import collect_all_naver
from summarize import summarize_items
from generate_html import generate_today_pages, generate_archive_pages
import archive_store

KST = timezone(timedelta(hours=9))


def dedupe(items: list) -> list:
    seen = set()
    result = []
    for it in items:
        key = it["title"].strip()
        if key in seen:
            continue
        seen.add(key)
        result.append(it)
    return result


def main():
    print("=== 교육·과학·정책 데일리 다이제스트 수집 시작 ===")

    all_items = []
    all_items += collect_all_rss(RSS_SOURCES, COLLECTION_WINDOW_HOURS)
    all_items += scrape_all_boards(BOARD_SOURCES, COLLECTION_WINDOW_HOURS)
    all_items += collect_all_naver(NAVER_KEYWORDS, COLLECTION_WINDOW_HOURS)

    print(f"\n[중복 제거 전] 총 {len(all_items)}건")
    all_items = dedupe(all_items)
    print(f"[중복 제거 후] 총 {len(all_items)}건")

    all_items = summarize_items(all_items)

    today_str = datetime.now(KST).strftime("%Y-%m-%d")

    # 1) 오늘자 데이터를 영구 저장 (data/YYYY-MM-DD.json, 이후 git에 커밋됨)
    archive_store.save_day(all_items, today_str)

    # 2) 오늘자 메인/카테고리 페이지 생성
    generate_today_pages(all_items, today_str, "output")

    # 3) 지금까지 쌓인 전체 데이터로 아카이브 페이지 재생성
    all_days = archive_store.load_all_days()
    generate_archive_pages(all_days, "output/archive")

    print("=== 완료 ===")


if __name__ == "__main__":
    main()

