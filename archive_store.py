# -*- coding: utf-8 -*-
"""
매일 수집된 원본 데이터를 날짜별 JSON으로 저장하고, 전체 이력을 불러옵니다.
data/YYYY-MM-DD.json 형태로 저장되며, 이 파일들은 GitHub 저장소에
그대로 커밋되어 영구 보관됩니다 (GitHub Actions가 매번 새로 커밋).
"""
import os
import json
import csv

DATA_DIR = "data"


def save_day(items: list, date_str: str, valid_sources: set = None):
    """
    같은 날짜에 여러 번 실행되면(예: 오전에 한 번, 오후에 재시도 한 번),
    기존 데이터를 덮어쓰지 않고 겹치지 않는 것만 합쳐서 저장한다.
    (사이트 접속 성공/실패가 매번 랜덤이라, 재시도할 때마다 다른 사이트가
     추가로 잡힐 수 있어 이렇게 하는 게 실질적으로 더 도움이 됨)

    valid_sources가 주어지면, 기존에 저장돼있던 항목 중 "지금 config.py에
    더 이상 존재하지 않는 소스(예: 삭제한 정책브리핑 검색 등)"에서 온 것은
    자동으로 걸러내고 버린다. -> 소스를 삭제/교체하면 다음 실행 때 옛날
    데이터도 자동으로 정리됨.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{date_str}.json")

    existing_items = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                existing_items = json.load(f)
        except Exception as e:
            print(f"[기존 데이터 로드 오류] {path}: {e}")

    removed_stale = 0
    if valid_sources is not None:
        before = len(existing_items)
        existing_items = [
            it for it in existing_items
            if it.get("source") in valid_sources or str(it.get("source", "")).startswith("네이버뉴스 · ")
        ]
        removed_stale = before - len(existing_items)

    combined = existing_items + items
    seen = set()
    merged = []
    for it in combined:
        key = it["title"].strip()
        if key in seen:
            continue
        seen.add(key)
        merged.append(it)

    added = len(merged) - len(existing_items)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    stale_note = f", 삭제된 소스 데이터 {removed_stale}건 정리" if removed_stale else ""
    print(f"[저장] {path} (기존 {len(existing_items)}건 + 새로 {added}건 추가 = 총 {len(merged)}건{stale_note})")


def load_all_days() -> list:
    """반환: [(date_str, items), ...] 날짜 오름차순 정렬"""
    if not os.path.isdir(DATA_DIR):
        return []

    result = []
    for filename in sorted(os.listdir(DATA_DIR)):
        if not filename.endswith(".json"):
            continue
        if filename.startswith("."):  # .last_run.json 같은 특수 파일 제외
            continue
        date_str = filename[:-5]
        path = os.path.join(DATA_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
            result.append((date_str, items))
        except Exception as e:
            print(f"[로드 오류] {path}: {e}")

    result.sort(key=lambda x: x[0])
    return result


def save_cumulative_csv(all_days: list, csv_path: str = os.path.join(DATA_DIR, "전체기록.csv")):
    """
    엑셀/구글시트에서 바로 열 수 있는 누적 CSV 생성.
    구글시트에서 열려면: 새 스프레드시트 만들기 -> 파일 -> 가져오기 -> 이 csv 업로드
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["날짜", "카테고리", "출처", "제목", "요약", "링크"])
        for date_str, items in all_days:
            for it in items:
                writer.writerow([
                    date_str,
                    it.get("category", ""),
                    it.get("source", ""),
                    it.get("title", ""),
                    it.get("summary", ""),
                    it.get("link", ""),
                ])

    print(f"[저장] {csv_path} (누적 {sum(len(items) for _, items in all_days)}건)")
