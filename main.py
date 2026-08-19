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
    last_run = archive_store.get_last_run_time()

    if last_run is None:
        # 첫 실행: config.py 기본값(24시간) 사용
        window_hours = COLLECTION_WINDOW_HOURS
        print(f"[수집 범위] 첫 실행 - 기본값 {window_hours}시간 사용")
    else:
        elapsed_hours = (now_kst - last_run).total_seconds() / 3600
        # 여유분 1시간 추가(시각 오차 방지), 최소 1시간~최대 14일로 제한
        window_hours = max(1.0, min(elapsed_hours + 1, 24 * 14))
        print(f"[수집 범위] 지난 실행({last_run.strftime('%Y-%m-%d %H:%M')}) 이후 "
              f"약 {elapsed_hours:.1f}시간 경과 -> {window_hours:.1f}시간 범위로 수집")

    all_items = []
    all_items += collect_all_rss(RSS_SOURCES, window_hours)
    all_items += scrape_all_boards(BOARD_SOURCES, window_hours)
    all_items += collect_all_naver(NAVER_KEYWORDS, window_hours)

    print(f"\n[중복 제거 전] 총 {len(all_items)}건")
    all_items = dedupe_and_prioritize(all_items, CATEGORY_PRIORITY)
    print(f"[중복 제거 후] 총 {len(all_items)}건")

    all_items = summarize_items(all_items)

    today_str = now_kst.strftime("%Y-%m-%d")

    # 1) 오늘자 데이터를 영구 저장 (data/YYYY-MM-DD.json, 이후 git에 커밋됨)
    archive_store.save_day(all_items, today_str)

    # 2) 오늘자 메인/카테고리 페이지 생성
    generate_today_pages(all_items, today_str, "output")

    # 3) 지금까지 쌓인 전체 데이터로 아카이브 페이지 재생성
    all_days = archive_store.load_all_days()
    generate_archive_pages(all_days, "output/archive")

    # 4) 엑셀/구글시트에서 열어볼 수 있는 누적 CSV도 저장
    archive_store.save_cumulative_csv(all_days)

    # 5) 이번 실행 시각 기록 (다음 실행 때 이 시각부터 계산됨)
    archive_store.set_last_run_time(now_kst)

    print("=== 완료 ===")


if __name__ == "__main__":
    main()

