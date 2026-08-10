# -*- coding: utf-8 -*-
"""
교육/과학/정책 뉴스 다이제스트 - 소스 설정
카테고리: education(교육) / science(과학) / policy(정책)
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
    {
        "name": "과학기술정보통신부 보도자료",
        "category": "science",
        "url": "https://www.msit.go.kr/bbs/rss.do?sCode=user&mPid=112&mId=113",
    },
]

# ── 게시판 크롤링이 필요한 소스 (URL + CSS 선택자 필요) ───────
# selector 정보는 실제 GitHub Actions 실행 환경에서 사이트 구조를
# 확인하며 하나씩 채워나갑니다. 우선 뼈대만 등록해둡니다.
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
        "list_url": "https://www.moe.go.kr/boardCnts/list.do?boardID=294&m=0204&s=moe",
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
        "name": "NIA 보도자료",
        "category": "science",
        "list_url": "https://www.nia.or.kr/site/nia_kor/ex/bbs/List.do?cbIdx=90549",
        "base_url": "https://www.nia.or.kr",
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
        "name": "한국교육과정평가원(KICE)",
        "category": "education",
        "list_url": "https://www.kice.re.kr/boardCnts/list.do?boardID=1500234&m=030105&s=kice",
        "base_url": "https://www.kice.re.kr",
    },
    {
        "name": "한국연구재단(NRF)",
        "category": "policy",
        "list_url": "https://www.nrf.re.kr/biz/notice/list?menu_no=372",
        "base_url": "https://www.nrf.re.kr",
    },
    {
        "name": "한국교총(KFTA)",
        "category": "policy",
        "list_url": "https://www.kfta.or.kr",
        "base_url": "https://www.kfta.or.kr",
    },
    {
        "name": "전교조 보도자료",
        "category": "policy",
        "list_url": "https://www.eduhope.net",
        "base_url": "https://www.eduhope.net",
    },
    {
        "name": "충남교육연수원",
        "category": "education",
        "list_url": "https://www.ceti.or.kr",
        "base_url": "https://www.ceti.or.kr",
    },
    {
        "name": "한국교과서연구재단",
        "category": "education",
        "list_url": "https://www.textbook114.com/index.jsp",
        "base_url": "https://www.textbook114.com",
    },
    {
        "name": "교육정책네트워크 정보센터(KEDI)",
        "category": "education",
        "list_url": "https://edpolicy.kedi.re.kr/",
        "base_url": "https://edpolicy.kedi.re.kr",
    },
]

# ── 네이버 뉴스 검색 키워드 ────────────────────────────────
NAVER_KEYWORDS = [
    ("AI 교육", "education"),
    ("디지털교과서", "education"),
    ("2028 수능", "education"),
    ("교육부 정책", "policy"),
    ("과학기술정보통신부", "science"),
]

# 수집 시간 기준 (직전 24시간)
COLLECTION_WINDOW_HOURS = 24

# 결과 출력 파일
OUTPUT_HTML = "output/index.html"
