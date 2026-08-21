# -*- coding: utf-8 -*-
"""매일 실행되는 메인 파이프라인: 수집 -> 요약 -> 저장 -> HTML 생성(오늘자+아카이브)"""
import os
import sys
from datetime import datetime, timezone, timedelta
from config import (
    RSS_SOURCES, BOARD_SOURCES, NAVER_KEYWORDS,
    COLLECTION_WINDOW_HOURS, INSTITUTION_LINKS,
)
from collectors.rss_collector import collect_all_rss
from collectors.board_scraper import scrape_all_boards
from collectors.naver_news import collect_all_naver
from summarize import summarize_items
from generate_html import generate_today_pages, generate_archive_pages, generate_links_page
import archive_store

KST = timezone(timedelta(hours=9))
COLLECTION_ANCHOR_HOUR = 10  # 매일 오전 10시 기준


# 겹치는 기사의 우선순위 (앞에 있을수록 우선순위 높음)
CATEGORY_PRIORITY = ["science", "education", "policy"]


def dedupe_and_prioritize(items: list, priority_order: list) -> list:
    """
    같은 제목의 기사가 여러 카테고리 소스에서 동시에 잡히면:
    - priority_order 기준으로 가장 우선순위 높은 카테고리 하나에만 배정
    - 나머지 겹치는 카테고리는 'related_categories'에 기록 (화면에 작은 배지로 표시됨)
    """
    groups = {}
    order = []  # 최초 등장 순서 보존
    for it in items:
        key = it["title"].strip()
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(it)

    result = []
    for key in order:
        group = groups[key]
        categories_present = set(it["category"] for it in group)
        primary = next((c for c in priority_order if c in categories_present), group[0]["category"])
        related = sorted(categories_present - {primary})

        base = dict(group[0])
        base["category"] = primary
        base["related_categories"] = related
        result.append(base)

    return result


def main():
    print("=== 교육·과학·정책 데일리 다이제스트 수집 시작 ===")

    now_kst = datetime.now(KST)

    # 매일 오전 10시(KST)를 기준선으로 고정. 언제 실행하든(오전이든 오후든,
    # 하루에 여러 번이든) 항상 "전날 10시 ~ 가장 최근 10시" 구간을 본다.
    # -> 같은 날 여러 번 실행해도 결과가 항상 동일함(멱등성)
    anchor_today = now_kst.replace(hour=COLLECTION_ANCHOR_HOUR, minute=0, second=0, microsecond=0)
    window_end = anchor_today if now_kst >= anchor_today else anchor_today - timedelta(days=1)
    window_start = window_end - timedelta(days=1)

    print(f"[수집 범위] {window_start.strftime('%Y-%m-%d %H:%M')} ~ "
          f"{window_end.strftime('%Y-%m-%d %H:%M')} (고정 24시간)")

    all_items = []
    rss_items, rss_failed = collect_all_rss(RSS_SOURCES, window_start, window_end)
    board_items, board_failed = scrape_all_boards(BOARD_SOURCES, window_start, window_end)
    naver_items = collect_all_naver(NAVER_KEYWORDS, window_start, window_end)
    all_items = rss_items + board_items + naver_items
    failed_sources = rss_failed + board_failed

    print(f"\n[중복 제거 전] 총 {len(all_items)}건")
    all_items = dedupe_and_prioritize(all_items, CATEGORY_PRIORITY)
    print(f"[중복 제거 후] 총 {len(all_items)}건")

    # ── 안전장치: 0건이면 "오늘 진짜 소식이 없는 날"이 아니라
    # 네트워크 차단 등으로 전면 수집 실패했을 가능성이 훨씬 높음.
    # 이 경우 기존 데이터/페이지를 절대 덮어쓰지 않고 실패로 종료한다.
    # (last_run_time도 갱신 안 해서, 다음 성공 실행 때 놓친 구간을 자동으로 다시 수집함)
    if len(all_items) == 0:
        print("\n[경고] 수집된 항목이 0건입니다. 네트워크 차단/타임아웃으로 인한 "
              "전면 실패로 판단하여 기존 데이터를 보존하고 실패로 종료합니다.")
        print("       (Actions 화면에 실패로 표시되며, 이후 단계는 건너뜁니다.)")
        sys.exit(1)

    all_items = summarize_items(all_items)

    today_str = window_end.strftime("%Y-%m-%d")

    # 1) 오늘자 데이터를 영구 저장 (data/YYYY-MM-DD.json, 이후 git에 커밋됨)
    archive_store.save_day(all_items, today_str)

    # 2) 오늘자 메인/카테고리 페이지 생성
    generate_today_pages(all_items, today_str, "output", failed_sources=failed_sources)

    # 2-1) 관련 기관 홈페이지 링크 모음 페이지 생성
    generate_links_page(INSTITUTION_LINKS, "output")

    # 3) 지금까지 쌓인 전체 데이터로 아카이브 페이지 재생성
    all_days = archive_store.load_all_days()
    generate_archive_pages(all_days, "output/archive")

    # 4) 엑셀/구글시트에서 열어볼 수 있는 누적 CSV도 저장
    archive_store.save_cumulative_csv(all_days)

    print("=== 완료 ===")


if __name__ == "__main__":
    main()

