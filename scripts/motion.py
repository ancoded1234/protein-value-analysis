from pathlib import Path
import shutil
import pandas as pd
from manim import *
R=Path(__file__).resolve().parents[1];A=R/'docs/assets'
config.media_dir=str(A/'manim');config.pixel_width=1280;config.pixel_height=720;config.frame_rate=24;config.background_color='#122523';config.verbosity='ERROR';config.progress_bar='none'
def t(s,size=28,c='#F3F5EB'):return Text(s,font='Malgun Gothic',font_size=size,color=c)
class ValueRanking(Scene):
 def construct(self):
  c=pd.read_csv(R/'data/comparison.csv');names={'P01':'더단백','P02':'셀렉스','P04':'그린비아','P05':'마이밀','P06':'오트몬드'}
  self.add(t('같은 단백질 20g의 비용',36).to_edge(UP),t('D01·D02·D04–D06·C01 | 수집 2026.10.18\n선택한 5개 묶음 관측 · 배송비 포함 · 전체 시장 최저가 아님',15,c='#B8C5B6').to_edge(DOWN))
  for i,r in enumerate(c.itertuples()):
   y=1.6-i*.85;w=r.cost_20g/2800*7
   b=Rectangle(width=w,height=.43,stroke_width=0,fill_color='#C8E85B' if i==0 else '#729867',fill_opacity=1).move_to([-2.5+w/2,y,0]);self.add(t(names[r.product_id],25).move_to([-4.3,y,0]));self.play(GrowFromEdge(b,LEFT),FadeIn(t(f'{r.cost_20g:,.0f}원',25).next_to(b,RIGHT,buff=.18)),run_time=.6)
  self.wait(1.6)
class Shipping(Scene):
 def construct(self):
  self.add(t('상품가보다 배송비 포함 총액',36).to_edge(UP),t('D01·C01 | 더단백 250mL 18개 | 2026.10.18 공개 표시가\n쿠폰·적립 차감 안 함 · 주문 결제 확인 아님',16,c='#B8C5B6').to_edge(DOWN))
  self.play(FadeIn(t('11번가 재게시',27).move_to([-4.2,1,0])),FadeIn(t('쿠팡 직접 화면',27).move_to([-4.2,-.7,0])))
  a=Rectangle(width=5.1,height=.7,fill_color='#729867',fill_opacity=1,stroke_width=0).move_to([.15,1,0]);b=Rectangle(width=5.65,height=.7,fill_color='#C8E85B',fill_opacity=1,stroke_width=0).move_to([.425,-.7,0]);self.play(GrowFromEdge(a,LEFT),GrowFromEdge(b,LEFT),run_time=.9)
  self.add(t('21,580원',25).next_to(a,UP),t('23,900원 / 무료배송',25).next_to(b,DOWN))
  fee=Rectangle(width=.71,height=.7,fill_color='#C8E85B',fill_opacity=1,stroke_width=0).next_to(a,RIGHT,buff=0);self.play(GrowFromEdge(fee,LEFT),FadeIn(t('+ 배송 3,000원',23).next_to(fee,UP)),run_time=.8)
  self.play(FadeIn(t('24,580원 > 23,900원',33,c='#C8E85B').move_to([0,-2.1,0])),run_time=.5);self.wait(2)
if __name__=='__main__':
 for cls in [ValueRanking,Shipping]:
  scene=cls();scene.render();shutil.copy2(scene.renderer.file_writer.movie_file_path,A/f'{cls.__name__}.mp4')
 print('Two Manim videos rendered')
