# 단백질 20g, 얼마면 될까? — 가성비 프로틴 찾기

**이번 관측 구성에서는 그린비아가 단백질 20g당 약 1,052원으로 가장 저렴했고, 셀렉스가 100kcal당 단백질 약 20.2g으로 열량 효율이 가장 높았다.** 시장 전체 최저가나 종합 품질 순위라는 뜻은 아니다.

발표: https://ancoded1234.github.io/protein-value-analysis/

|제품|관측 구성|배송비 포함 총액|단백질 20g당|판매처|
|---|---:|---:|---:|---|
|그린비아 프로틴밀 액티브 초코|18팩|18,940원|1,052원|옥션|
|더단백 드링크 초코|18팩|23,900원|1,328원|쿠팡(판매자 상세 미기록)|
|오트몬드 프로틴 초코 제로슈거|6팩|11,140원|1,768원|옥션|
|마이밀 퓨로틴 초코|24팩|56,800원|2,367원|11번가|
|셀렉스 프로핏 웨이프로틴 초콜릿|12팩|29,890원|2,491원|롯데ON|

수집 2026-10-18. 초콜릿 RTD 6개 후보 중 5개 판매 구성·가격 관측 54건. 쿠팡 실제 공개 화면은 computer-use로 확인, 다나와 판매처 본문은 Firecrawl 수집. 네이버페이 판매처 값은 다나와 경유로 구분했다. 셀렉스 공식 영양표, 사용자 제공 더단백 상세 라벨(C02), 2023년 한국소비자원 독립 시험 16개를 보완했다. 현재 성분표와 과거 실험값을 혼합하지 않았다. 6팩·24팩 차이와 재게시 가격 한계를 명시했다.

## 결과물

- `docs/index.html`: 13장, 16:9 웹 발표. Anime.js 막대·산점도, 예산 필터, 키보드·전체화면·출처·노트, Manim 영상 2개.
- `presentation/protein_value_analysis.pptx`: 수정 가능한 텍스트·도형·네이티브 차트 2개. PDF·발표 노트 별도.
- `data/products.csv`, `price_observations.csv`, `comparison.csv`, `sources.csv`, `exclusions.csv`: 현재 관측 데이터와 선택/제외 근거.
- `data/lab_2023.csv`: 과거 16개 독립 시험. 현재 순위와 조인하지 않음.
- `analysis/insights.md`, `data_quality_report.md`, `figures/`, `qa/`: 분석·Seaborn 차트 6종·검수.
- `data/raw/`, `data/firecrawl/`: 로컬 원문·브라우저 증거. 저작물 전문·인증 파일이어서 공개 저장소에서 제외.

## 재현

Python 3.12, Windows Office PowerPoint. requirements.txt 설치 후 기존 부모 .env의 FIRECRAWL_API_KEY를 읽기만 한다. 원문 캐시를 공개하지 않으므로 Git clone 뒤 재수집이 필요하다. collect.py URL SLUG로 수집하고 products.csv와 sources.csv의 적용 범위를 다시 확인한다. 기존 캐시가 있으면 호출하지 않는다. 브라우저 직접 관측 C01은 가격·수량·배송비를 실제 확인해 비공개 증거를 저장해야 한다. C02는 사용자가 제공한 더단백 상세 영양표이며 data/raw/bing_nutrition_user.png가 필요하다.

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
.venv/Scripts/python.exe scripts/analyze.py
.venv/Scripts/python.exe scripts/figures.py
.venv/Scripts/python.exe scripts/deck.py
.venv/Scripts/python.exe scripts/motion.py
.venv/Scripts/python.exe scripts/reports.py
.venv/Scripts/python.exe scripts/validate.py
python -m http.server 8000 --directory docs
```

공개 배포는 gh CLI로 독립 저장소를 만들고 Pages REST API의 main /docs 방식 사용. 공개 URL 검수는 환경변수 PRESENTATION_TEST_URL을 지정해 validate.py 실행. 로고·제품 사진은 발표에서 재배포하지 않고 자체 코드 그래픽을 사용했다. Anime.js MIT 라이선스는 assets에 보존했다.

## 기술·스킬

Python/pandas·Seaborn·Matplotlib·python-pptx·Manim·Playwright·Firecrawl·HTML/CSS/JS·Anime.js·GitHub CLI. computer-use 스킬로 쿠팡 페이지를 실제 확인했다. 사용자가 제공한 [k-skill](https://github.com/NomaDamas/k-skill) 쇼핑 모듈은 검토했으나 호출하지 않았다. 결제·회원가입·CAPTCHA/접근 제한 우회·계정 변경은 수행하지 않았다.
