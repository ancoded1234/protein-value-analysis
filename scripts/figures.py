from pathlib import Path
import pandas as pd,numpy as np,seaborn as sns,matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];F=R/'analysis/figures';F.mkdir(exist_ok=True)
c=pd.read_csv(R/'data/comparison.csv');l=pd.read_csv(R/'data/lab_2023.csv')
short={'P01':'더단백','P02':'셀렉스','P04':'그린비아','P05':'마이밀','P06':'오트몬드'};c['short']=c.product_id.map(short)
NAVY='#122523';GREEN='#527858';LIME='#B4D849';BG='#F3F5EB';GRAY='#7A8981'
plt.rcParams.update({'font.family':'Malgun Gothic','axes.unicode_minus':False,'figure.facecolor':BG,'axes.facecolor':BG,'text.color':NAVY,'axes.labelcolor':NAVY,'xtick.color':GRAY,'ytick.color':NAVY,'font.size':12,'savefig.facecolor':BG})
def save(n):plt.savefig(F/f'{n}.png',dpi=180,bbox_inches='tight');plt.savefig(F/f'{n}.svg',bbox_inches='tight');plt.close()
def bars(field,title,xlabel,name):
 d=c.sort_values(field);fig,ax=plt.subplots(figsize=(10,4.5));sns.barplot(data=d,x=field,y='short',hue='short',palette=[GREEN]+[LIME]*4,legend=False,ax=ax)
 for i,v in enumerate(d[field]):ax.text(v+max(d[field])*.02,i,f'{v:,.0f}' if 'krw' in field or field=='cost_20g' else f'{v:.1f}',va='center',fontweight='bold')
 ax.set(title=title,xlabel=xlabel,ylabel='',xlim=(0,max(d[field])*1.28));sns.despine(left=True);fig.text(.12,-.02,'2026.10.18 공개 페이지 관측 · 선택한 5개 묶음 구성만 비교 · 배송비 포함 · 결제/시장 전체 최저가 아님',fontsize=9);save(name)
bars('cost_20g','같은 단백질 20g, 비용은 최대 2.37배','표시 단백질 20g당 비용(원)','01_cost20')
bars('bottle_krw','묶음 총액을 한 팩 가격으로 바꾸면','팩당 가격(원)','02_bottle')
bars('protein_per_100kcal','열량 대비 단백질: 셀렉스가 가장 높다','100kcal당 표시 단백질(g)','03_density')
fig,ax=plt.subplots(figsize=(10,4.7));sns.scatterplot(data=c,x='cost_20g',y='kcal_per_20g',hue='short',s=180,palette=[GREEN,'#7D9769','#A8B97C','#8A6C55','#B9CA90'],ax=ax)
for r in c.itertuples():ax.annotate(r.short,(r.cost_20g,r.kcal_per_20g),xytext=(0,12),textcoords='offset points',ha='center')
ax.set(xlim=(900,2800),ylim=(90,145),xlabel='단백질 20g당 비용(원) ↓',ylabel='단백질 20g당 열량(kcal) ↓',title='가격 우선과 열량 효율 우선의 선택은 다르다');ax.legend().remove();sns.despine();fig.text(.12,-.02,'D01·D02·D04–D06·C01 | 표시 영양성분 기준. 흡수율·맛·안전성 순위가 아니다.',fontsize=9);save('04_tradeoff')
fig,ax=plt.subplots(figsize=(10,4.7));ax.barh(['11번가 재게시','쿠팡 직접 화면'],[21580,23900],color=[GRAY,GREEN]);ax.barh(['11번가 재게시'],[3000],left=[21580],color=LIME)
ax.text(24580+250,0,'24,580원',va='center',weight='bold');ax.text(23900+250,1,'23,900원',va='center',weight='bold');ax.invert_yaxis();ax.set(xlim=(0,29000),xlabel='더단백 18개 / 상품가 + 배송비(원)',title='21,580원보다 23,900원이 더 저렴한 이유');sns.despine(left=True);fig.text(.12,-.02,'D01·C01 | 공개 관측 표시가. 추가 쿠폰·적립·회원 조건을 제외한 비교, 주문 결제 검증 아님.',fontsize=9);save('05_shipping')
fig,ax=plt.subplots(figsize=(10,4.7));sns.scatterplot(data=l,x='reported_krw_per_g',y='amino_score',hue='form',s=110,palette=[GREEN,'#9EAE76'],ax=ax);ax.axhline(85,color=GRAY,ls='--',lw=1);ax.text(250,88,'85: 당시 보고서 비교 기준',fontsize=10)
ax.set(xlabel='2023년 보고서 단백질 1g당 가격(원)',ylabel='2023년 시험 아미노산스코어',title='과거 독립 시험: 가격만으로 품질 지표를 판단하기 어렵다');sns.despine();fig.text(.12,-.02,'K01, 2023.08 발표 pp.15–17 · 가격 기준 2023.02 · n=16 · 현재 판매 제품과 직접 결합하지 않음',fontsize=9);save('06_lab2023')
print('6 Seaborn/Matplotlib figures generated')
