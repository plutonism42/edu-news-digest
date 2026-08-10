# 교육·과학·정책 데일리 다이제스트

매일 오전 10시(KST), 최근 24시간 내 올라온 교육부·KEDI·KERIS·정책브리핑 등
18개 기관의 공지/보도자료와 네이버 뉴스 검색 결과를 모아 요약된 웹페이지를 자동 생성합니다.

## 처음 설정하는 방법 (한 번만 하면 됩니다)

### 1. 이 폴더를 GitHub 저장소로 올리기
1. github.com에서 새 저장소(Repository)를 만듭니다. (이름 예: `edu-news-digest`)
2. 이 폴더의 모든 파일을 그 저장소에 업로드합니다. (GitHub 웹사이트에서 파일 드래그&드롭으로도 가능)

### 2. 네이버 API 키 발급 (2026년 8월 기준: NAVER API HUB 방식)
⚠️ 2026년 7월 31일부로 예전 개발자센터(developers.naver.com)에서는 검색 API 신규 신청이 막혔고,
**네이버 클라우드 플랫폼(NCP)의 NAVER API HUB**로 이관되었습니다.

1. console.ncloud.com 접속 → 네이버 아이디로 회원가입/로그인
2. 콘솔 우측 상단 "리전 & 플랫폼"에서 리전/플랫폼 선택 후 적용
3. 좌측 상단 Menu → All Services → Application Services → **NAVER API HUB**
4. 좌측 "Application" 메뉴 → **Application 등록**
5. 사용할 API에서 "뉴스 검색 결과 조회" 등 필요한 검색 API 선택 → 다음
6. Application 이름 입력 (예: `edu-news-digest`) → 완료
7. 등록된 Application 클릭 → API 관리 하단 **[인증 정보]** 버튼 → Client ID / Client Secret 확인

**참고**: 새 방식은 인증 헤더 이름이 예전과 다릅니다.
- API 주소: `https://naverapihub.apigw.ntruss.com`
- 헤더: `X-NCP-APIGW-API-KEY-ID` (Client ID), `X-NCP-APIGW-API-KEY` (Client Secret)
- 이 저장소의 `collectors/naver_news.py`는 이미 새 방식으로 작성되어 있습니다.
- 호출 한도도 하루 단위가 아닌 **월 최대 775,000건**(통합 관리)으로 바뀌었습니다.

### 3. GitHub 저장소에 비밀키(Secrets) 등록
저장소 페이지에서 **Settings → Secrets and variables → Actions → New repository secret**
다음 3개를 각각 등록합니다:
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`
- `ANTHROPIC_API_KEY` (Claude API 키, console.anthropic.com에서 발급)

### 4. GitHub Pages 켜기
저장소 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 설정합니다.

### 5. 첫 실행
저장소의 **Actions** 탭 → "Daily Education News Digest" → **Run workflow** 버튼을 눌러
수동으로 한 번 실행해봅니다. 성공하면 이후로는 매일 오전 10시(KST)에 자동으로 실행됩니다.

완료되면 `https://[깃허브아이디].github.io/edu-news-digest/` 에서 결과 페이지를 볼 수 있어요.

## 주의할 점 (1차 버전 한계)

- **RSS 소스** (KEDI, 정책브리핑, 과기정통부)는 안정적으로 수집됩니다.
- **게시판 크롤링 소스** (교육부, KERIS, KOSAC 등)는 사이트 구조가 각각 달라서,
  1차 버전은 "날짜 패턴이 붙은 링크"를 찾는 범용 방식으로 동작합니다.
  일부 사이트에서는 관련 없는 메뉴 링크가 섞여 들어올 수 있어요.
  → 실행해보고 결과를 보면서 사이트별로 하나씩 정확도를 높여가면 됩니다.
- 요약은 **제목만 보고** Claude가 핵심을 1줄로 정리하는 방식입니다.
  본문까지 가져와 더 정확하게 요약하려면 추가 개발이 필요합니다 (다음 단계로 가능).

## 파일 구조
```
config.py              소스 목록 (RSS, 게시판, 네이버 키워드)
collectors/
  rss_collector.py      RSS 수집
  board_scraper.py       게시판 크롤링
  naver_news.py           네이버 뉴스 검색
summarize.py            Claude로 요약
generate_html.py        HTML 페이지 생성
main.py                  전체 실행
.github/workflows/daily.yml   매일 자동 실행 설정
```
