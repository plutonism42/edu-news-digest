# -*- coding: utf-8 -*-
"""
교육/과학/정책 뉴스 다이제스트 - 소스 설정
카테고리: education(교육분야) / policy(국가정책) / science(과학교육)

변경 이력:
- 2026-08-11: 플루토쌤이 사이트 하나씩 직접 확인해서 URL 정리/교체함.
- 2026-08-18: 전교조를 policy -> education으로 이동. 카테고리별 키워드 검색 시도.
- 2026-08-21: korea.kr의 srchWord 파라미터가 실제 필터링을 하지 않는 것이 확인되어
  키워드 검색 16개 소스를 BOARD_SOURCES에서 제거함. NIA, KOSAC은 자바스크립트로
  목록을 그리는 방식이라 자동 수집이 불가능 -> 링크 모음(INSTITUTION_LINKS)으로만 제공.
"""

# ── RSS로 수집 가능한 소스 (가장 안정적) ─────────────────────
RSS_SOURCES = [
    {
        "name": "정책브리핑(교육부 뉴스)",
        "category": "policy",
        "url": "https://www.korea.kr/rss/dept_moe.xml",
    },
    {
        "name": "정책브리핑(과기정통부 뉴스)",
        "category": "science",
        "url": "https://www.korea.kr/rss/dept_msit.xml",
    },
    {
        "name": "KEDI 보도자료",
        "category": "education",
        "url": "https://www.kedi.re.kr/khome/main/announce/rssAnnounceData.do?board_sq_no=3",
    },
    {
        "name": "KEDI 공고",
        "category": "education",
        "url": "https://www.kedi.re.kr/khome/main/announce/rssAnnounceData.do?board_sq_no=2",
    },
]

# ── 게시판 크롤링이 필요한 소스 (기관 직접, 키워드 검색 아님) ──
BOARD_SOURCES = [
    {
        "name": "교육부 공지사항",
        "category": "policy",
        "list_url": "https://www.moe.go.kr/boardCnts/listRenew.do?boardID=333&m=020501&s=moe",
        "base_url": "https://www.moe.go.kr",
    },
    {
        "name": "교육부 보도자료",
        "category": "policy",
        "list_url": "https://www.moe.go.kr/boardCnts/listRenew.do?boardID=294&m=020402&s=moe",
        "base_url": "https://www.moe.go.kr",
    },
    {
        "name": "국가교육위원회 보도자료",
        "category": "policy",
        "list_url": "https://www.ne.go.kr/user/bbs/BD_selectBbsList.do?q_bbsSn=1004",
        "base_url": "https://www.ne.go.kr",
    },
    {
        "name": "KERIS 공지/보도자료",
        "category": "education",
        "list_url": "https://www.keris.or.kr/main/na/ntt/selectNttList.do?mi=1088&bbsId=1090",
        "base_url": "https://www.keris.or.kr",
    },
    {
        "name": "한국교육과정평가원(KICE) 보도자료",
        "category": "education",
        "list_url": "https://www.kice.re.kr/boardCnts/list.do?boardID=10024&m=050102&s=kice&searchStr=",
        "base_url": "https://www.kice.re.kr",
    },
    {
        "name": "KEDI 연구보고서",
        "category": "education",
        "list_url": "https://www.kedi.re.kr/khome/main/research/listPubForm.do",
        "base_url": "https://www.kedi.re.kr",
    },
    {
        "name": "KEDI 교육정책포럼(브리프)",
        "category": "education",
        "list_url": "https://www.kedi.re.kr/khome/main/research/listPubForm.do",
        "base_url": "https://www.kedi.re.kr",
    },
    {
        "name": "전교조 보도자료",
        "category": "education",
        "list_url": "https://www.eduhope.net/bbs/board.php?bo_table=maybbs_eduhope_4&menu_id=2010",
        "base_url": "https://www.eduhope.net",
    },
    {
        "name": "한국교육신문(정책) - 헤드라인",
        "category": "policy",
        "list_url": "https://www.hangyo.com/news/section_list_all.html?sec_no=1648",
        "base_url": "https://www.hangyo.com",
    },
    {
        "name": "과학기술정보통신부 보도자료",
        "category": "science",
        "list_url": "https://www.msit.go.kr/bbs/list.do?sCode=user&mPid=208&mId=307",
        "base_url": "https://www.msit.go.kr",
    },
    {
        "name": "교과서민원바로처리센터 뉴스",
        "category": "education",
        "list_url": "https://www.textbook114.com/portal.jsp?req_PAGE=content&menu=4&sub=7&sidemenu=1&sub=1",
        "base_url": "https://www.textbook114.com",
    },
    {
        "name": "교육정책네트워크 월간 교육정책포럼(KEDI)",
        "category": "education",
        "list_url": "https://edpolicy.kedi.re.kr/edpolicy/webzine/list1",
        "base_url": "https://edpolicy.kedi.re.kr",
    },
    {
        "name": "에듀플러스뉴스",
        "category": "education",
        "list_url": "https://www.eduplusnews.com/news/articleList.html?sc_sub_section_code=S2N4&view_type=sm",
        "base_url": "https://www.eduplusnews.com",
    },
]

# ── 관련 기관 홈페이지 링크 모음 (자동 수집 아님, 클릭해서 직접 확인용) ──
# NIA, KOSAC처럼 자바스크립트로 목록을 그리는 사이트라 자동 수집이 안 되거나,
# 참고용으로 링크만 있으면 되는 곳들을 여기에 모아둠.
INSTITUTION_LINKS = [
    {"name": "교육부", "url": "https://www.moe.go.kr", "category": "policy"},
    {"name": "국가교육위원회", "url": "https://www.ne.go.kr", "category": "policy"},
    {"name": "정책브리핑(korea.kr)", "url": "https://www.korea.kr", "category": "policy"},
    {"name": "한국교육신문", "url": "https://www.hangyo.com", "category": "policy"},
    {"name": "한국교육개발원(KEDI)", "url": "https://www.kedi.re.kr", "category": "education"},
    {"name": "한국교육학술정보원(KERIS)", "url": "https://www.keris.or.kr", "category": "education"},
    {"name": "한국교육과정평가원(KICE)", "url": "https://www.kice.re.kr", "category": "education"},
    {"name": "전교조", "url": "https://www.eduhope.net", "category": "education"},
    {"name": "교과서민원바로처리센터", "url": "https://www.textbook114.com", "category": "education"},
    {"name": "교육정책네트워크(KEDI)", "url": "https://edpolicy.kedi.re.kr", "category": "education"},
    {"name": "에듀플러스뉴스", "url": "https://www.eduplusnews.com", "category": "education"},
    {"name": "한국과학창의재단(KOSAC)", "url": "https://www.kosac.re.kr", "category": "science"},
    {"name": "과학기술정보통신부", "url": "https://www.msit.go.kr", "category": "science"},
    {"name": "지능형과학실 ON", "url": "https://science-on.kosac.re.kr/", "category": "science"},
    {"name": "국립중앙과학관", "url": "https://www.science.go.kr/mps/index.do", "category": "science"},
    {"name": "한국과학교육학회", "url": "https://jkase.jams.or.kr/co/main/jmMain.kci", "category": "science"},
    {"name": "영재교육종합시스템", "url": "https://ged.kedi.re.kr/index.do", "category": "science"},
]

# ── 정책브리핑 보도자료 - 키워드 검색 (현재 비활성화) ──
# 2026-08-21: korea.kr의 srchWord 파라미터가 실제로 필터링을 하지 않는다는 것이
# 확인됨 (어떤 키워드를 넣어도 그냥 "최신 보도자료 전체 목록"이 나옴 - 같은 기사가
# 서로 다른 키워드 카테고리에 동일하게 잡히는 것으로 확인됨). 관련 없는 기사로
# 화면을 어지럽히는 문제가 있어 BOARD_SOURCES에는 추가하지 않음.
# 나중에 data.go.kr의 "문화체육관광부_정책브리핑_보도자료_API"(정식 API, 키 발급 필요)로
# 교체하면 진짜 키워드 검색이 가능함.
KEYWORD_CATEGORY_MAP = {
    # 교육분야: 학교 현장/교사 실무 일반
    "학교": "education",
    "교육": "education",
    "교사": "education",
    "교과서": "education",
    "민원": "education",
    "교권": "education",
    "수능": "education",
    # 국가정책: 정부 정책 발표 성격이 뚜렷한 키워드
    "AI교육": "policy",
    "디지털": "policy",
    # 과학교육: 연구회/공모/참여활동 성격
    "AI": "science",
    "과학실": "science",
    "연구회": "science",
    "공모": "science",
    "연구": "science",
    "지능형": "science",
    "STEAM": "science",
}

# ── 네이버 뉴스 검색 키워드 (현재 비활성 - 키 미설정 시 자동 건너뜀) ──
# 네이버 API는 진짜 키워드 검색이 되므로 이 목록은 그대로 유지
NAVER_KEYWORDS = [(w, cat) for w, cat in KEYWORD_CATEGORY_MAP.items()]

# 수집 시간 기준 (참고용 기본값. 실제로는 main.py가 매일 오전 10시를 기준선으로
# "전날 10시 ~ 오늘 10시" 24시간 고정 구간을 계산해서 사용함)
COLLECTION_WINDOW_HOURS = 24
