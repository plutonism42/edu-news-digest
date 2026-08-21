# -*- coding: utf-8 -*-
"""
교육/과학/정책 뉴스 다이제스트 - 소스 설정
카테고리: education(교육) / science(과학) / policy(정책)

2026-08-11: 플루토쌤이 사이트 하나씩 직접 확인해서 URL 정리/교체함.
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

# ── 게시판 크롤링이 필요한 소스 ────────────────────────────
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
        "name": "한국과학창의재단(KOSAC) 공지사항",
        "category": "science",
        "list_url": "https://www.kosac.re.kr/menus/270/boards/386/posts",
        "base_url": "https://www.kosac.re.kr",
    },
    {
        "name": "한국과학창의재단(KOSAC) 보도자료",
        "category": "science",
        "list_url": "https://www.kosac.re.kr/menus/272/boards/394/posts",
        "base_url": "https://www.kosac.re.kr",
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

# ── 정책브리핑 보도자료 - 키워드 검색 (전 부처 대상) ──
# 키워드 하나당 카테고리 하나만 지정 (중복 없음 -> 카테고리 쏠림 방지)
from urllib.parse import quote as _quote

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

for _w, _cat in KEYWORD_CATEGORY_MAP.items():
    BOARD_SOURCES.append({
        "name": f"정책브리핑 검색('{_w}')",
        "category": _cat,
        "list_url": f"https://www.korea.kr/briefing/pressReleaseList.do?srchWord={_quote(_w)}",
        "base_url": "https://www.korea.kr",
    })

# ── 네이버 뉴스 검색 키워드 (현재 비활성 - 키 미설정 시 자동 건너뜀) ──
NAVER_KEYWORDS = [(w, cat) for w, cat in KEYWORD_CATEGORY_MAP.items()]

# ── 관련 기관 홈페이지 (4번째 버튼: "관련 기관 홈페이지"용) ──
INSTITUTION_LINKS = [
    {"name": "교육부", "url": "https://www.moe.go.kr", "category": "policy"},
    {"name": "국가교육위원회", "url": "https://www.ne.go.kr", "category": "policy"},
    {"name": "정책브리핑(korea.kr)", "url": "https://www.korea.kr/briefing/pressReleaseList.do", "category": "policy"},
    {"name": "한국교육신문", "url": "https://www.hangyo.com", "category": "policy"},
    {"name": "KERIS", "url": "https://www.keris.or.kr", "category": "education"},
    {"name": "KEDI", "url": "https://www.kedi.re.kr", "category": "education"},
    {"name": "교육정책네트워크(KEDI)", "url": "https://edpolicy.kedi.re.kr", "category": "education"},
    {"name": "한국교육과정평가원(KICE)", "url": "https://www.kice.re.kr", "category": "education"},
    {"name": "전교조", "url": "https://www.eduhope.net", "category": "education"},
    {"name": "교과서민원바로처리센터", "url": "https://www.textbook114.com", "category": "education"},
    {"name": "에듀플러스뉴스", "url": "https://www.eduplusnews.com", "category": "education"},
    {"name": "한국과학창의재단(KOSAC)", "url": "https://www.kosac.re.kr", "category": "science"},
    {"name": "과학기술정보통신부", "url": "https://www.msit.go.kr", "category": "science"},
    {"name": "지능형과학실 ON", "url": "https://science-on.kosac.re.kr/", "category": "science"},
    {"name": "국립중앙과학관", "url": "https://www.science.go.kr/mps/index.do", "category": "science"},
    {"name": "한국과학교육학회", "url": "https://jkase.jams.or.kr/co/main/jmMain.kci", "category": "science"},
    {"name": "영재교육종합시스템", "url": "https://ged.kedi.re.kr/index.do", "category": "science"},
]

# 수집 시간 기준 (직전 24시간)
COLLECTION_WINDOW_HOURS = 24

# 결과 출력 파일 (참고용, 실제로는 generate_html.py가 여러 파일을 생성함)
OUTPUT_HTML = "output/index.html"
