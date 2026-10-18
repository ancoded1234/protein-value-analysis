"""Reproduce a small, source-linked retail observation study. No invented quality scores."""
from pathlib import Path
import re,json,datetime
import pandas as pd,numpy as np
R=Path(__file__).resolve().parents[1];DATE='2026-10-18'
for d in ['analysis','analysis/figures','presentation','docs/assets']: (R/d).mkdir(parents=True,exist_ok=True)
SPECS=[
 ('P01','빙그레','더단백 드링크 초코','bing_correct',18,250,20,105,None,True,'당류 수치는 채택한 상품 요약에 없어 비워둠'),
 ('P02','매일유업','셀렉스 프로핏 웨이프로틴 초콜릿','selex_price',12,330,20,99,0,True,'제조사 330mL·20g·99kcal와 교차 확인'),
 ('P03','오리온','닥터유 프로 드링크 초코 24g','doctor_price',12,250,24,151,1,False,'공식 2026년 24g→27g 리뉴얼 안내와 가격비교 24g 표기 충돌. 판매 옵션의 세대 미확정으로 순위 제외'),
 ('P04','정식품','그린비아 프로틴밀 액티브 초코','green_price',18,250,20,120,1,True,'영양성분은 가격비교 재게시 자료; 독립 시험값 아님'),
 ('P05','대상웰라이프','마이밀 퓨로틴 초코','mymil_price',24,250,20,130,None,True,'분리대두·완두·귀리 단백질 표기. 당류 요약 근거 미확보'),
 ('P06','롯데칠성음료','오트몬드 프로틴 초코 제로슈거','oat_six',6,250,21,107,0,True,'6팩 관측. 배송비 영향이 크며 대용량 묶음 최저가를 대표하지 않음'),
]
sources=[];products=[];offers=[];exclusions=[]
def source(sid,url,kind,title,path,when=DATE,pub='게시일 미표기'):
    sources.append(dict(source_id=sid,url=url,type=kind,title=title,collected=when,published=pub,local_evidence=path))
for pid,brand,name,slug,qty,ml,protein,kcal,sugar,include,note in SPECS:
    j=json.loads((R/f'data/firecrawl/{slug}.json').read_text(encoding='utf-8'));assert j['success']
    md=j['data']['markdown'];title=j['data']['metadata'].get('title','')
    assert brand in title or name.split()[0] in title,(name,title)
    assert str(ml)+'ml' in title and f'({qty}개)' in title,title
    sid='D'+pid[-2:];source(sid,j['url'],'가격비교 재게시',title,f'data/firecrawl/{slug}.md',j['collected_at'])
    a=md.index('상세 스펙');spec=md[a:].split('- [관심]',1)[0]
    assert re.search(r'단백질\s*:\s*'+str(protein)+r'g',spec),spec
    assert str(kcal)+'kcal' in spec
    products.append(dict(product_id=pid,brand=brand,name=name,flavor='초콜릿 계열',form='RTD 음료',pack_count=qty,volume_ml=ml,protein_g=protein,kcal=kcal,sugar_g=sugar,nutrition_status='verified' if pid=='P02' else 'reported',included=include,source_id=sid,note=note))
    a=md.find('쇼핑몰별 최저가',a)
    if a<0:exclusions.append(dict(source=slug,reason='판매처별 가격 영역 없음'));continue
    section=md[a:];section=re.split(r'#### 최저가 추이|\[\*\*상품리뷰|#### 상품 상세정보',section)[0]
    for block in re.split(r'\n- ',section)[1:]:
        lines=[x.strip() for x in block.splitlines() if x.strip()]
        merchant=re.sub(r'!\[([^]]+)\]\([^)]*\)',r'\1',lines[0]).strip()
        link=re.search(r'\[상품보기\]\((https://[^)]+)\)',block)
        if not link:continue
        visible=block[:block.index('[상품보기]')]
        amounts=re.findall(r'(?<!\d)(\d[\d,]*)\s*원',visible)
        if not amounts:continue
        price=int(amounts[0].replace(',',''))
        shipping=0 if '무료배송' in visible else int(amounts[1].replace(',','')) if len(amounts)>1 else None
        offers.append(dict(product_id=pid,merchant=merchant,price_krw=price,shipping_krw=shipping,total_krw=price+shipping if shipping is not None else None,source_id=sid,url=link.group(1),source_type='가격비교 재게시',observed=j['collected_at'],condition='비회원 일반 표시가·본토 1묶음, 결제 확인 아님',included=include))
# A visible, logged-out browser observation, saved separately from comparison-site observations.
assert (R/'data/raw/coupang_bing_ui.txt').exists()
cu='https://www.coupang.com/vp/products/7411095382?itemId=13466502453&vendorItemId=76137436686'
source('C01',cu,'computer-use 판매 화면','더단백 초코 250mL 18개 / 23,900원·무료배송','data/raw/coupang_bing_ui.txt')
offers.append(dict(product_id='P01',merchant='쿠팡(판매자 상세 미기록)',price_krw=23900,shipping_krw=0,total_krw=23900,source_id='C01',url=cu,source_type='computer-use 직접 화면',observed=DATE,condition='로그아웃 표시가, 18개 선택·배송비 포함·결제 확인 아님',included=True))
for sid,slug,title in [('M01','selex_official','매일유업 공식 제품 영양정보'),('M02','doctor_2026_change','오리온 공식 24g→27g 리뉴얼 게시물'),('N01','oat_launch','오트몬드 250mL·21g 출시 보도')]:
    p=R/f'data/firecrawl/{slug}.json'
    if p.exists():
        j=json.loads(p.read_text(encoding='utf-8'))
        if j['success']:source(sid,j['url'],'제조사' if sid.startswith('M') else '언론',title,f'data/firecrawl/{slug}.md',j['collected_at'])
KCA='https://isafe.go.kr/DATA/bbs/85/20230808024444967.pdf'
if not any(s['source_id']=='M02' for s in sources):
    from bs4 import BeautifulSoup
    p=R/'data/raw/doctor_change.html'
    if p.exists():
        body=BeautifulSoup(p.read_bytes(),'html.parser').get_text(' ',strip=True)
        assert '27g' in body and '24g' in body
        (R/'data/raw/doctor_change.txt').write_text(body,encoding='utf-8')
        source('M02','https://www.orionworld.com/sns/snsList/89?page=9','공식 웹 HTTP 본문','2026-05-13 닥터유PRO 24g→27g 게시물 제목 확인','data/raw/doctor_change.txt',pub='2026-05-13')
source('K01',KCA,'공공기관 독립 시험','한국소비자원 단백질 보충 일반식품 16개 시험·평가, pp.6·15–17','data/raw/kca_2023.pdf',pub='2023-08-08 (가격 기준 2023-02)')
pd.DataFrame(products).to_csv(R/'data/products.csv',index=False,encoding='utf-8-sig')
o=pd.DataFrame(offers);o['eligible']=o.included&o.total_krw.notna();o.to_csv(R/'data/price_observations.csv',index=False,encoding='utf-8-sig')
best=o[o.eligible].sort_values('total_krw').drop_duplicates('product_id')
c=pd.DataFrame(products).query('included').merge(best[['product_id','merchant','total_krw','shipping_krw','source_id','url']],on='product_id',suffixes=('_nutrition','_price'),validate='one_to_one')
c['bottle_krw']=c.total_krw/c.pack_count;c['cost_20g']=c.bottle_krw*20/c.protein_g;c['protein_per_100kcal']=c.protein_g/c.kcal*100;c['kcal_per_20g']=c.kcal*20/c.protein_g
c['bottle_rank']=c.bottle_krw.rank(method='min').astype(int);c['protein_rank']=c.cost_20g.rank(method='min').astype(int)
c['pareto_cost_energy']=[not any((c.cost_20g<=r.cost_20g)&(c.kcal_per_20g<=r.kcal_per_20g)&((c.cost_20g<r.cost_20g)|(c.kcal_per_20g<r.kcal_per_20g))) for r in c.itertuples()]
c=c.sort_values('cost_20g');c.to_csv(R/'data/comparison.csv',index=False,encoding='utf-8-sig')
# Transcribed from the official 2023 tables, not joined to 2026 listings.
lab=[
 ['건강앤 MBP 유단백추출물 분말','분말',12,113,8.6,118,132],['국민프로틴 WPI웨이 초코','분말',13,241,5.5,114,166],['NS포대유청 WPC 오리지널','분말',23,116,1.3,127,32],['뉴욕웨이 WPC 리치초콜릿','분말',21,119,.7,136,33],['뉴트리원 초유 콜라겐 프로틴','분말',21,115,3.5,77,102],['닥터유 프로 파우더 아이솔레이트 초코','분말',29,160,.3,100,72],['셀렉스 프로핏 웨이프로틴 초콜릿(분말)','분말',20,115,.9,113,102],['칼로바이 파워쉐이크 아이솔레이트 초코','분말',26,166,.2,107,68],
 ['뉴케어 액티브 골든밸런스','음료',14,198,6.8,118,157],['닥터유 단백질 드링크 초코 240mL','음료',12,165,20.9,136,167],['더단백 드링크 초코','음료',20,115,.5,118,145],['셀렉스 프로틴 음료 오리지널','음료',7,130,7.3,91,148],['아몬드브리즈 뉴트리플러스 프로틴','음료',4,67,4.8,45,375],['칼로바이 파워쉐이크 20G 초코바나나','음료',19,126,9.5,141,93],['파스퇴르 이지프로틴 저당 초코','음료',21,110,1.5,123,119],['하이뮨 프로틴 밸런스','음료',9,165,12.2,100,356]]
l=pd.DataFrame(lab,columns=['name','form','protein_g','kcal','sugar_g','amino_score','reported_krw_per_g']);l['approx_cost_20g']=l.reported_krw_per_g*20;l['source_id']='K01';l['basis']='2023-02 가격·2023-08 발표 시험, 현재 제품·시세에 전용 불가';l.to_csv(R/'data/lab_2023.csv',index=False,encoding='utf-8-sig')
exclusions += [dict(source='bing_price',reason='검색 VS 코드와 실제 상품 불일치. 오트몬드 140mL 혼합 구성으로 연결되어 제외'),dict(source='oat_price',reason='24개 구성 현재 판매처 가격 미확보. 검색 캐시 43,650원을 사용하지 않음'),dict(source='doctor_price',reason=products[2]['note'])]
pd.DataFrame(exclusions).to_csv(R/'data/exclusions.csv',index=False,encoding='utf-8-sig');pd.DataFrame(sources).to_csv(R/'data/sources.csv',index=False,encoding='utf-8-sig')
m=dict(collected=DATE,candidates=6,ranked=len(c),offers=len(o),sources=len(sources),winner=c.iloc[0]['name'],winner_cost20=float(c.iloc[0].cost_20g),highest_cost20=float(c.cost_20g.max()),ratio=float(c.cost_20g.max()/c.cost_20g.min()),historical_lab_products=len(l),historical_above85=int((l.amino_score>=85).sum()),label_sugar_available=int(c.sugar_g.notna().sum()))
(R/'analysis/metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'docs/data.json').write_text(json.dumps(dict(products=c.astype(object).where(pd.notna(c),None).to_dict('records'),offers=o.astype(object).where(pd.notna(o),None).to_dict('records'),lab=l.to_dict('records'),sources=sources,metrics=m),ensure_ascii=False,indent=2),encoding='utf-8')
assert len(c)==5 and c.product_id.is_unique and (c.cost_20g>0).all()
assert len(l)==16 and (l.amino_score>=85).sum()==14
print(json.dumps(m,ensure_ascii=False,indent=2));print(c[['name','merchant','pack_count','total_krw','cost_20g']].to_string(index=False))
