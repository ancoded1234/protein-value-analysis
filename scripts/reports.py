from pathlib import Path
import json
import pandas as pd
R=Path(__file__).resolve().parents[1];C=pd.read_csv(R/'data/comparison.csv');O=pd.read_csv(R/'data/price_observations.csv');S=pd.read_csv(R/'data/sources.csv');M=json.loads((R/'analysis/metrics.json').read_text(encoding='utf-8'))
table='|제품|관측 구성|배송비 포함 총액|단백질 20g당|판매처|\n|---|---:|---:|---:|---|\n'+'\n'.join(f'|{r.name}|{r.pack_count}팩|{r.total_krw:,}원|{r.cost_20g:,.0f}원|{r.merchant}|' for r in C.itertuples())
insights=f'''# 가성비 프로틴 찾기 — 분석 결과

수집 2026-10-18. 초콜릿 계열 RTD 음료 6개 후보 중 제품 세대가 불명확한 닥터유를 제외한 5개 판매 구성을 분석했다. 분말형과 음료형을 현재 순위에서 섞지 않았다.

## 결론

이번 관측 구성에서 **그린비아 프로틴밀 액티브 초코가 단백질 20g당 약 1,052원으로 가장 저렴**했다. **셀렉스는 100kcal당 단백질 약 20.2g으로 표시 성분상 열량 효율이 가장 높았다.** 즉 비용 우선과 열량 효율 우선은 다른 기준이다. 시장 전체 최저가·맛·흡수율·안전성·종합 품질 1위라는 결론은 아니다.

{table}

계산식: (상품가 + 배송비) ÷ (팩 수 × 팩당 표시 단백질 g) × 20. 20g은 비교 분모이며 개인 섭취 권장량이 아니다. 소수점은 계산 중 유지하고 발표 때 원 단위로 반올림했다. 최고/최저는 {M['ratio']:.2f}배다.

## 수집과 정제

쿠팡의 더단백 초코 250mL 18개를 computer-use로 실제 확인했다. 로그인 없는 화면의 가격은 23,900원, 무료배송이었다. 구매하지 않았다. 증거 화면·선택 영역 텍스트는 비공개 data/raw에 보존했다. 그 외 판매처 가격은 Firecrawl로 다나와 본문을 수집하여 판매처별 상품가·배송비를 각각 추출했다. 네이버페이 판매처도 포함하지만 네이버 직접 확인·결제 가격이 아니다. 총 {len(O)}개 관측 중 닥터유는 비교에서 제외했고, 나머지 제품별로 배송비가 확인된 최저 관측값을 선택했다.

검색 VS 코드 70677317은 실제로 오트몬드 140mL 혼합구성에 연결돼 더단백 근거에서 제외했다. 검색 캐시가 보여준 오트몬드 24개 가격은 실제 페이지에서 판매처 가격이 없어 채택하지 않았다. 0원이나 과거 검색 가격으로 채우지 않았다. 닥터유는 오리온 공식 2026-05-13 게시물의 24g→27g 안내와 가격비교 24g 제품의 연결이 불분명해 순위에서 제외했다. Firecrawl이 이 공식 페이지를 가져오지 못해 공개 HTTP 원문과 웹 도구로 보완했고 방법을 구분했다.

## 배송비 때문에 달라지는 선택

더단백 18개는 11번가 재게시 상품가 21,580원 + 배송비 3,000원 = 24,580원이다. 쿠팡 직접 화면 23,900원보다 680원 높다. 상품가만 보아서는 실제 비교 순서를 잘못 판단할 수 있다. 회원가·적립·카드 할인·쿠폰은 일반 가격에서 차감하지 않았다.

## 성분과 품질 근거

현재 5개 중 셀렉스의 330mL·20g·99kcal·당류 0g은 매일유업 공식 제품 자료와 교차 확인했다. 나머지 제품 성분은 이번 채택 근거에서 가격비교 재게시 상태인 reported로 유지했다. 당류 수치 확보는 3/5이며 나머지는 미확보다. 셀렉스 WPI와 마이밀 대두·완두·귀리 원료 표기를 성분 특성으로 기록하되 임의의 우열 점수를 부여하지 않았다.

한국소비자원 2023년 시험 원본 PDF를 확보해 16개 제품의 단백질·열량·당류·아미노산스코어와 당시 1g당 가격을 따로 전사했다. 14/16이 당시 비교 기준 85 이상, 단백질 1g당 보고 가격 32–375원이다. 가장 저렴한 NS포대유청의 아미노산스코어는 127이었다. **이 과거 시험을 현재 판매 제품의 품질 보증이나 현재 가격과 결합한 순위로 사용하지 않았다.** 보고 가격은 반올림돼 20배한 과거 비용은 근사치다.

## 해석 한계

소규모 목적 표본이고 전체 판매처·제품·묶음을 수집하지 않았다. 특히 오트몬드 6팩과 마이밀 24팩은 구매 부담·배송비·재고 위험이 다르다. 다른 묶음 구성에서는 순위가 달라질 수 있다. 최신 수집일은 재게시 가격의 정확한 갱신 시점이나 결제 가능 여부와 다르다. 수도권/일반 배송 기준이며 도서산간 추가 비용은 반영하지 않았다. 실제 함량·맛·흡수율·안전성을 측정하지 않았고 리뷰 평점을 품질 대리 지표로 쓰지 않았다.
'''
(R/'analysis/insights.md').write_text(insights,encoding='utf-8')
(R/'analysis/data_quality_report.md').write_text(f'''# 데이터 품질과 검수

- 후보 6개 → 비교 5개. 동일 맛 계열 RTD만 현재 비교. 닥터유 리뉴얼 세대 미확정 제외.
- 관측 {len(O)}건, 출처 {len(S)}개. 판매처별 상품가·배송비·URL·수집시각·직접/재게시 구분. 배송비 미확인 값은 총액 순위에서 제외.
- 표시가와 결제액 구분. 네이버페이 판매처는 다나와 경유, 네이버 직접 API 수집 성공으로 표현하지 않음.
- 검색 잘못된 제품 연결 및 품절/가격 누락 항목은 exclusions.csv에 보존.
- 제조사 공식 영양표와 연결한 현재 제품은 셀렉스 1개. 다른 제품의 성분은 reported. 당류 미확보 2개를 0g으로 처리하지 않음.
- 2023년 독립 시험 16개는 당시 제품·가격 데이터로 별도 파일. 현재 가격과 조인하지 않음. 1g당 가격은 원문 반올림값으로 유지.
- 원본 PDF pp.6·15–17 전사. 분말 8개·음료 8개, 아미노산스코어 85 이상 14개 일치.
- k-skill 3개 쇼핑 모듈은 문서를 검토했으나 스킬의 데이터베이스 구축 제한/API 용도 때문에 실행하지 않음. 별도 스킬 설치·인증 변경 없음. computer-use 스킬과 공개 본문 수집 사용.
- 기존 .env를 python-dotenv로 읽기만 함. 키 출력·저장·업로드 없음. raw/ 및 firecrawl/ 전문은 Git 제외.
- 검수: scripts/validate.py가 실제 PowerPoint 열기·PDF/PNG 내보내기·재열기·네이티브 차트와 CSV 값 일치, HTML 13장 데스크톱/모바일·예산 필터·방향키·출처·노트·모션·전체화면을 확인. 결과는 analysis/qa에 기록.
''',encoding='utf-8')
readme=f'''# 단백질 20g, 얼마면 될까? — 가성비 프로틴 찾기

**이번 관측 구성에서는 그린비아가 단백질 20g당 약 1,052원으로 가장 저렴했고, 셀렉스가 100kcal당 단백질 약 20.2g으로 열량 효율이 가장 높았다.** 시장 전체 최저가나 종합 품질 순위라는 뜻은 아니다.

발표: https://ancoded1234.github.io/protein-value-analysis/

{table}

수집 2026-10-18. 초콜릿 RTD 6개 후보 중 5개 판매 구성·가격 관측 {len(O)}건. 쿠팡 실제 공개 화면은 computer-use로 확인, 다나와 판매처 본문은 Firecrawl 수집. 네이버페이 판매처 값은 다나와 경유로 구분했다. 셀렉스 공식 영양표 1개와 2023년 한국소비자원 독립 시험 16개를 보완했다. 현재 성분표와 과거 실험값을 혼합하지 않았다. 6팩·24팩 차이와 재게시 가격 한계를 명시했다.

## 결과물

- `docs/index.html`: 13장, 16:9 웹 발표. Anime.js 막대·산점도, 예산 필터, 키보드·전체화면·출처·노트, Manim 영상 2개.
- `presentation/protein_value_analysis.pptx`: 수정 가능한 텍스트·도형·네이티브 차트 2개. PDF·발표 노트 별도.
- `data/products.csv`, `price_observations.csv`, `comparison.csv`, `sources.csv`, `exclusions.csv`: 현재 관측 데이터와 선택/제외 근거.
- `data/lab_2023.csv`: 과거 16개 독립 시험. 현재 순위와 조인하지 않음.
- `analysis/insights.md`, `data_quality_report.md`, `figures/`, `qa/`: 분석·Seaborn 차트 6종·검수.
- `data/raw/`, `data/firecrawl/`: 로컬 원문·브라우저 증거. 저작물 전문·인증 파일이어서 공개 저장소에서 제외.

## 재현

Python 3.12, Windows Office PowerPoint. requirements.txt 설치 후 기존 부모 .env의 FIRECRAWL_API_KEY를 읽기만 한다. 원문 캐시를 공개하지 않으므로 Git clone 뒤 재수집이 필요하다. collect.py URL SLUG로 수집하고 products.csv와 sources.csv의 적용 범위를 다시 확인한다. 기존 캐시가 있으면 호출하지 않는다. 브라우저 직접 관측 C01은 가격·수량·배송비를 실제 확인해 비공개 증거를 저장해야 한다.

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

公開 배포는 gh CLI로 독립 저장소를 만들고 Pages REST API의 main /docs 방식 사용. 공개 URL 검수는 환경변수 PRESENTATION_TEST_URL을 지정해 validate.py 실행. 로고·제품 사진은 발표에서 재배포하지 않고 자체 코드 그래픽을 사용했다. Anime.js MIT 라이선스는 assets에 보존했다.

## 기술·스킬

Python/pandas·Seaborn·Matplotlib·python-pptx·Manim·Playwright·Firecrawl·HTML/CSS/JS·Anime.js·GitHub CLI. computer-use 스킬로 쿠팡 페이지를 실제 확인했다. 사용자가 제공한 [k-skill](https://github.com/NomaDamas/k-skill) 쇼핑 모듈은 검토했으나 호출하지 않았다. 결제·회원가입·CAPTCHA/접근 제한 우회·계정 변경은 수행하지 않았다.
'''
(R/'README.md').write_text(readme.replace('公開','공개'),encoding='utf-8')
print('Research reports and README generated')
