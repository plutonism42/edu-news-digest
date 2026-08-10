# -*- coding: utf-8 -*-
"""매일 실행되는 메인 파이프라인: 수집 -> 요약 -> HTML 생성"""
import os
from config import (
    RSS_SOURCES, BOARD_SOURCES, NAVER_KEYWORDS,
    COLLECTION_WINDOW_HOURS, OUTPUT_HTML,
)
from collectors.rss_collector import collect_all_rss
from collectors.board_scraper import scrape_all_boards
from collectors.naver_news import collect_all_naver
from summarize import summarize_items
from generate_html import generate_html


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

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    generate_html(all_items, OUTPUT_HTML)

    print("=== 완료 ===")


if __name__ == "__main__":
    main()
