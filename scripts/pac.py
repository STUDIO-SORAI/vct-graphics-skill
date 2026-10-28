# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os as _os
ROOT=_os.environ.get('VCT_ROOT',_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import _assets
_assets.preflight('pac',ROOT)
from PIL import Image,ImageDraw,ImageFont
import sys,math
MODE=sys.argv[1];S=int(sys.argv[2]);OUT=sys.argv[3];W,H=1080*S,1350*S
CB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';CR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FD=ROOT+'/assets/fonts/ClashDisplay/';CL=FD+'ClashDisplay-Bold.otf';CS=FD+'ClashDisplay-Semibold.otf'
MONO='/usr/share/fonts/truetype/sand-box/google/JetBrains Mono/JetBrainsMono-VariableFont_wght.ttf'
def F(p,s):return ImageFont.truetype(p,round(s*S),index=3 if p.endswith('ttc') else 0)
def FMN(s_):
  f=ImageFont.truetype(MONO,round(s_*S))
  try:f.set_variation_by_axes([500])
  except Exception:pass
  return f
P=lambda v:round(v*S)
LIME=(198,244,50);INK=(22,22,22);WHT=(255,255,255);MUT=(160,170,176);LCQC=(24,92,120);GREY=(222,226,228);CY=(0,190,214)
im=Image.open(ROOT+'/assets/bg_pac'+('@2x' if S==2 else '')+'.png').convert('RGB');d=ImageDraw.Draw(im)
def panel(x1,y1,x2,y2,c,a):
  global im,d
  ov=Image.new('RGBA',im.size,(0,0,0,0));ImageDraw.Draw(ov).rectangle([P(x1),P(y1),P(x2),P(y2)],fill=c+(int(255*a),));im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB');d=ImageDraw.Draw(im)
def Lg(p,h):
  m=Image.open(p).convert('RGBA');m=m.crop(m.getbbox());return m.resize((round(m.width*h/m.height),round(h)),Image.LANCZOS)
def blk(x1,y1,x2,y2,c):d.rectangle([P(x1),P(y1),P(x2),P(y2)],fill=c)
def ct(cx,cy,t,f,c):d.text((P(cx),P(cy)),t,font=f,fill=c,anchor='mm')
def ln(pts,c=WHT,w=2):d.line([(P(x),P(y)) for x,y in pts],fill=c,width=P(w),joint='curve')
def arrow(pts,c=WHT,w=2):
  ln(pts,c,w);(x0,y0),(x1,y1)=pts[-2],pts[-1];a=math.atan2(y1-y0,x1-x0);k=9
  d.polygon([(P(x1),P(y1)),(P(x1-k*math.cos(a-0.45)),P(y1-k*math.sin(a-0.45))),(P(x1-k*math.cos(a+0.45)),P(y1-k*math.sin(a+0.45)))],fill=c)
def dots(x1,y1,x2,y2,c=WHT):
  n=int(math.hypot(x2-x1,y2-y1)/6)
  for i in range(n+1):
    t=i/max(n,1);x=x1+(x2-x1)*t;y=y1+(y2-y1)*t;d.ellipse([P(x-1.3),P(y-1.3),P(x+1.3),P(y+1.3)],fill=c)
MK=Lg(ROOT+'/assets/vct_white.png',100)
def mark(cx,cy,h,c=WHT):
  m=Lg(ROOT+'/assets/vct_white.png',P(h));
  if c!=WHT:
    m=Image.merge('RGBA',(*[Image.new('L',m.size,v) for v in c],m.getchannel('A')))
  im.paste(m,(P(cx)-m.width//2,P(cy)-m.height//2),m)
import re,os
OLD=os.environ.get('OLDWORD')=='1'
OLDMAP={'Cup 名額分配':'盃賽名額分配','公開資格賽晉級 Cup 路線':'公開資格賽晉級盃賽路線','Cup 最終資格賽':'盃賽最終資格賽','Cup 1・Cup 2 參賽隊伍':'盃賽 1・盃賽 2 參賽隊伍',
 '合作夥伴隊不保證 Cup 席次，需與公開資格賽隊伍競爭':'合作夥伴隊不保證盃賽席次，需與公開資格賽隊伍競爭','直接晉級 Cup ・ 11 隊':'直接晉級盃賽 ・ 11 隊','CUP':'盃賽',
 '12 隊晉級 Cup':'12 隊晉級盃賽','Cup 晉級':'盃賽晉級','只有 #1 LCQ 能晉級 Cup':'只有 #1 LCQ 能晉級盃賽'}
def T(x,y,t,sz,fill,anchor='ls',lat=None,cjk=None):
  """mixed text: 'Cup'/'CUP' runs in Clash Display, everything else Noto Sans CJK Bold"""
  if OLD:t=OLDMAP.get(t,t)
  fc=F(cjk or CB,sz);fl=F(lat or CL,sz)
  parts=[p for p in re.split(r'(Cup(?: \d)?|CUP)',t) if p!='']
  runs=[]
  for i,p in enumerate(parts):
    if re.fullmatch(r'Cup(?: \d)?|CUP',p):runs.append((p.replace(' ','  '),fl,True))
    else:
      q=p
      if i>0:q=q.lstrip(' ')
      if i<len(parts)-1:q=q.rstrip(' ')
      if q:runs.append((q,fc,False))
  gap=round(0.12*sz*S)
  segs=[];tot=0
  for i,(s_,f_,lt) in enumerate(runs):
    if i>0:
      pr=runs[i-1];g=gap
      if '・' in (s_[:1] if not lt else '') or '・' in (pr[0][-1:] if not pr[2] else ''):g=0
      tot+=g;segs.append(g)
    else:segs.append(0)
    tot+=f_.getlength(s_)
  tot=round(tot)
  X=P(x)
  if anchor[0]=='r':X-=tot
  elif anchor[0]=='m':X-=tot//2
  Y=P(y)
  if anchor[1]=='m':
    a_,d_=fc.getmetrics();Y=Y+round((a_-d_)/2)
  cx=X
  for (s_,f_,lt),g in zip(runs,segs):
    cx+=g;d.text((cx,Y),s_,font=f_,fill=fill,anchor='ls');cx+=f_.getlength(s_)
# ---------- header
TSZ=None
if MODE=='slots':TITLE='Cup 名額分配';KICK='VCT PACIFIC 2027 · CUP SLOTS';TSZ=84
elif MODE=='path':TITLE='公開資格賽晉級 Cup 路線';KICK='VCT PACIFIC 2027 · PATH TO CUPS';TSZ=66
elif MODE=='lcq':TITLE='Cup 最終資格賽';KICK='VCT PACIFIC 2027 · CUP LCQ';TSZ=84
elif MODE=='overview':TITLE='2027 賽季全貌';KICK='VCT PACIFIC 2027 · SEASON MAP'
else:TITLE='合作夥伴隊伍';KICK='VCT PACIFIC 2027 · PARTNER TEAMS'
panel(0,250,1080,252,(255,255,255),0.0)
_lk=Lg(ROOT+'/assets/pacific_kickoff_white.png',P(64));im.paste(_lk,(P(40),P(40)),_lk)
d.text((P(1040),P(84)),KICK,font=F(CL,17),fill=WHT,anchor='rs')
T(37,206,TITLE,TSZ or (84 if len(TITLE)<9 else 66),WHT,'ls')
d.line([P(24),P(118),P(1056),P(118)],fill=WHT,width=max(1,S))
for x in (24,1056):d.line([P(x),P(110),P(x),P(126)],fill=WHT,width=max(1,S))
d.text((P(1056),P(140)),"13°45'N  ·  GLOBAL TOUR: ACTIVE",font=FMN(12),fill=WHT,anchor='rs')
d.text((P(1056),P(30)),'ZONE: PACIFIC  ·  LEADERBOARD: CALIBRATING',font=FMN(12),fill=WHT,anchor='rs')
def chip(x,y,w,h,t,fs,bg=LIME,fg=INK,font=None):
  blk(x,y,x+w,y+h,bg);ct(x+w/2,y+h/2+1,t,font or F(CL,fs),fg)
def pill(cx,cy,w,t,kind,h=34,fs=17):
  bg,fg=(LIME,INK) if kind=='cup' else (LCQC,WHT)
  blk(cx-w/2,cy-h/2,cx+w/2,cy+h/2,bg);ct(cx,cy+1,t,F(CL,fs),fg)
  if kind!='cup':d.rectangle([P(cx-w/2),P(cy-h/2),P(cx+w/2),P(cy+h/2)],outline=(120,200,225),width=max(1,S))
REGN={'KR':'韓國','JP':'日本','SEA':'東南亞','TH':'泰國','ID':'印尼','VN':'越南','LCQ':'最終資格賽','SA':'南亞','OCE':'大洋洲'}
def corners(x1,y1,x2,y2,c=WHT,L=14):
  for X,sx in ((x1,1),(x2,-1)):
    for Y,sy in ((y1,1),(y2,-1)):
      d.line([P(X),P(Y),P(X+sx*L),P(Y)],fill=c,width=max(1,S));d.line([P(X),P(Y),P(X),P(Y+sy*L)],fill=c,width=max(1,S))
def CUPB(x,y,so,sn):
  if OLD:d.text((P(x),P(y)),'盃賽',font=F(CB,so),fill=WHT,anchor='lm')
  else:d.text((P(x),P(y)),'CUP',font=F(CL,sn),fill=WHT,anchor='lm')
if MODE=='slots':
  # strip
  panel(0,262,1080,382,(6,18,30),0.62)
  d.text((P(40),P(352)),'12',font=F(CL,104),fill=LIME,anchor='ls');d.text((P(40+F(CL,104).getlength('12')/S+10),P(350)),'隊',font=F(CB,40),fill=WHT,anchor='ls')
  T(300,318,'Cup 1・Cup 2 參賽隊伍',28,WHT,'ls')
  d.text((P(300),P(354)),'KR 3 + JP 3 + SEA 2 + TH 1 + ID 1 + VN 1 + LCQ 1',font=FMN(15),fill=LIME,anchor='ls')
  panel(20,404,1060,1184,(6,18,30),0.6)
  for (x,y) in [(20,404),(1060,404),(20,1184),(1060,1184)]:
    d.line([P(x-10),P(y),P(x+10),P(y)],fill=WHT,width=max(1,S));d.line([P(x),P(y-10),P(x),P(y+10)],fill=WHT,width=max(1,S))
  rows=[('KR',3),('JP',3),('SEA',2),('TH',1),('ID',1),('VN',1),('LCQ',1)]
  pitch=108;y0=424
  for i,(c,n) in enumerate(rows):
    y=y0+i*pitch
    chip(50,y,132,58,c,40);d.text((P(116),P(y+82)),REGN[c] if c!='LCQ' else '最終資格賽',font=F(CB,16 if c!='LCQ' else 13),fill=WHT,anchor='mm')
    d.text((P(204),P(y+37)),f'{n}',font=F(CL,40),fill=LIME,anchor='ls')
    d.text((P(234),P(y+37)),'席',font=F(CB,20),fill=WHT,anchor='ls')
    for k in range(n):
      x=290+k*250
      blk(x,y,x+236,y+90,INK);d.rectangle([P(x+5),P(y+5),P(x+231),P(y+85)],outline=WHT,width=max(1,S))
      mark(x+40,y+45,48)
      d.text((P(x+78),P(y+46)),f'#{k+1}',font=F(CL,34),fill=LIME,anchor='lm')
      d.text((P(x+222),P(y+46)),('LCQ' if c=='LCQ' else '公開資格賽'),font=F(CB,15) if c!='LCQ' else F(CL,22),fill=GREY,anchor='rm')
  d.text((P(1036),P(1120)),'南亞、大洋洲無直通名額，須經 LCQ 爭取',font=F(CB,18),fill=WHT,anchor='rm')
  T(1036,1148,'合作夥伴隊不保證 Cup 席次，需與公開資格賽隊伍競爭',18,WHT,'rm')
elif MODE=='path':
  panel(20,270,1060,1244,(6,18,30),0.6)
  for (x,y) in [(20,270),(1060,270),(20,1244),(1060,1244)]:
    d.line([P(x-10),P(y),P(x+10),P(y)],fill=WHT,width=max(1,S));d.line([P(x),P(y-10),P(x),P(y+10)],fill=WHT,width=max(1,S))
  cw=108;cx0=46;codes=['KR','JP','SEA','TH','VN','ID','SA','OCE']
  X=[cx0+i*(cw+14)+(26 if i>=6 else 0) for i in range(8)]
  cyc=292
  for c,x in zip(codes,X):
    chip(x,cyc,cw,48,c,28);d.text((P(x+cw/2),P(cyc+66)),REGN[c],font=F(CB,14),fill=GREY,anchor='mm')
  # play-ins
  pi1,pi2=394,470;px1,px2=X[0],X[5]+cw
  blk(px1,pi1,px2,pi2,GREY);ct((px1+px2)/2,pi1+30,'Play-ins 外圍賽',F(CB,28),INK);ct((px1+px2)/2,pi1+57,'每區 8 隊',F(CB,16),(60,60,60))
  for c,x in list(zip(codes,X))[:6]:arrow([(x+cw/2,cyc+80),(x+cw/2,pi1-8)])
  # playoffs
  po1,po2=520,596
  blk(X[0],po1,X[7]+cw,po2,GREY);ct((X[0]+X[7]+cw)/2,po1+30,'Playoffs 季後賽',F(CB,28),INK);ct((X[0]+X[7]+cw)/2,po1+57,'每區 8 隊',F(CB,16),(60,60,60))
  for x in (X[0]+cw/2,X[5]+cw/2):pass
  arrow([((px1+px2)/2,pi2+8),((px1+px2)/2,po1-8)])
  for c,x in list(zip(codes,X))[6:]:arrow([(x+cw/2,cyc+80),(x+cw/2,po1-8)])
  # outputs
  ly=630
  arrow([(300,po2+8),(300,ly-8)]);arrow([(790,po2+8),(790,ly-8)])
  blk(40,ly,560,ly+40,LIME);T(300,ly+21,'直接晉級 Cup ・ 11 隊',22,INK,'mm')
  blk(590,ly,1040,ly+40,LCQC);ct(815,ly+21,'進入 LCQ ・ 8 隊',F(CB,22),WHT)
  cup=[('KR',[1,2,3]),('JP',[1,2,3]),('SEA',[1,2]),('TH',[1]),('VN',[1]),('ID',[1])]
  lcq=[('TH',[2,3]),('ID',[2,3]),('VN',[2]),('SA',[1,2]),('OCE',[1])]
  rp=46
  for i,(c,ns) in enumerate(cup):
    y=ly+40+34+i*47
    d.text((P(106),P(y)),c,font=F(CL,24),fill=WHT,anchor='rm')
    for k,n in enumerate(ns):pill(180+k*118,y,104,f'#{n}  {c}','cup')
  for i,(c,ns) in enumerate(lcq):
    y=ly+40+34+i*47
    d.text((P(654),P(y)),c,font=F(CL,24),fill=WHT,anchor='rm')
    for k,n in enumerate(ns):pill(728+k*118,y,104,f'#{n}  {c}','lcq')
  # LCQ box
  by=934
  blk(590,by,1040,by+66,LCQC);d.rectangle([P(590),P(by),P(1040),P(by+66)],outline=(120,200,225),width=max(1,S))
  ct(815,by+24,'LAST CHANCE QUALIFIER',F(CL,22),WHT);ct(815,by+49,'最終資格賽',F(CB,16),GREY)
  arrow([(815,by+74),(815,by+88)])
  pill(815,by+113,130,'#1  LCQ','cup',h=34,fs=19)
  cupy=1106;cb2=1186
  arrow([(815,by+66+61),(815,cupy+4),(815,cupy)]) if False else None
  # CUP block
  blk(40,cupy,1040,cb2,INK);d.rectangle([P(46),P(cupy+6),P(1034),P(cb2-6)],outline=WHT,width=max(1,S))
  CUPB(80,cupy+38,54,50);mark(250,cupy+40,52)
  T(300,cupy+28,'12 隊晉級 Cup',26,LIME,'lm');d.text((P(300),P(cupy+58)),'11 隊直接晉級 ＋ LCQ 第 1 名',font=F(CB,17),fill=GREY,anchor='lm')
  arrow([(300,ly+40+34+5*47+14+0),(300,cupy)]) if False else None
  # connectors into CUP
  ybot=ly+40+34+6*47-12
  arrow([(300,ybot),(300,cupy-8)])
  arrow([(815,by+138),(815,cupy-8)])
  d.text((P(40),P(1226)),'',font=F(CB,1))
  # legend
  blk(40,1218,64,1230,LIME);T(74,1224,'Cup 晉級',16,WHT,'lm')
  blk(180,1218,204,1230,LCQC);d.rectangle([P(180),P(1218),P(204),P(1230)],outline=(120,200,225),width=max(1,S));d.text((P(214),P(1224)),'LCQ 晉級',font=F(CB,16),fill=WHT,anchor='lm')
  d.text((P(1040),P(1224)),'南亞、大洋洲直接進 Playoffs，無 Play-ins',font=F(CB,16),fill=WHT,anchor='rm')
elif MODE=='lcq':
  panel(20,270,1060,1196,(6,18,30),0.6)
  for (x,y) in [(20,270),(1060,270),(20,1196),(1060,1196)]:
    d.line([P(x-10),P(y),P(x+10),P(y)],fill=WHT,width=max(1,S));d.line([P(x),P(y-10),P(x),P(y+10)],fill=WHT,width=max(1,S))
  rows=[('TH',[2,3]),('ID',[2,3]),('SA',[1,2]),('VN',[2]),('OCE',[1])]
  BX=720;ys=[]
  for i,(c,ns) in enumerate(rows):
    cy=334+i*134
    w=96 if c!='OCE' else 118
    blk(40,cy-30,380,cy+30,GREY);blk(40,cy-30,40+w+14,cy+30,INK);ct(40+(w+14)/2,cy+1,c,F(CL,32),LIME);ct(40+w+14+(340-w-14)/2,cy+1,'Playoffs',F(CL,28),INK)
    n=len(ns);pys=[cy] if n==1 else [cy-27,cy+27]
    for n_,py in zip(ns,pys):
      pill(540,py,170,f'#{n_}  {c}','cup',h=44,fs=24);arrow([(380+((cy-cy)if 1 else 0),cy),(455,py)]) if False else None
      ln([(633,py),(BX,py)]);ys.append(py)
    if n==1:arrow([(388,cy),(447,cy)])
    else:
      ln([(388,cy),(410,cy),(410,pys[0]),(447,pys[0])]) ;ln([(410,cy),(410,pys[1]),(447,pys[1])])
      d.polygon([(P(447),P(pys[0])),(P(438),P(pys[0]-4)),(P(438),P(pys[0]+4))],fill=WHT);d.polygon([(P(447),P(pys[1])),(P(438),P(pys[1]-4)),(P(438),P(pys[1]+4))],fill=WHT)
  ln([(BX,min(ys)),(BX,998)])
  arrow([(BX,max(ys)),(BX,998)])
  pill(BX,1030,170,'#1  LCQ','cup',h=48,fs=28)
  cupy=1084
  arrow([(BX,1062),(BX,cupy-8)])
  blk(380,cupy,1040,cupy+96,INK);d.rectangle([P(386),P(cupy+6),P(1034),P(cupy+90)],outline=WHT,width=max(1,S))
  CUPB(430,cupy+45,58,54);mark(640,cupy+48,56)
  d.text((P(690),P(cupy+36)),'取得最後 1 席',font=F(CB,26),fill=LIME,anchor='lm');d.text((P(690),P(cupy+68)),'12 隊之一',font=F(CB,18),fill=GREY,anchor='lm')
  d.text((P(40),P(1040)),'8 隊爭 1 席',font=F(CB,34),fill=LIME,anchor='lm')
  T(40,1086,'只有 #1 LCQ 能晉級 Cup',18,WHT,'lm')
  d.text((P(40),P(1116)),'南亞、大洋洲須經此路線',font=F(CB,18),fill=WHT,anchor='lm')

if MODE=='overview':
  # Reusable season-map layout: 3 large REGIONAL cards (left) each followed by 1 small INTERNATIONAL card (right).
  # For other regions, only EVENTS (and TITLE/KICK in the header) need to change.
  panel(20,262,1060,1252,(6,18,30),0.6);corners(20,262,1060,1252)
  import numpy as np
  PH=ROOT+'/assets/photos/'
  EVENTS=[
    dict(big=dict(name='Kickoff',zh='曼谷 · 泰國',dt='01.14 – 02.07',ph='bkk',fo=(50,50),note='8 合作夥伴隊 ＋ 4 公開資格賽隊'),
         intl=dict(kind='Masters',city='Seoul',zh='首爾',dt='02.20 – 03.03',ph='seo',fo=(50,60))),
    dict(big=dict(name='Cup 1',zh='馬尼拉 · 菲律賓',dt='04.29 – 05.23',ph='mnl',fo=(50,50)),
         intl=dict(kind='Masters',city='Valencia',zh='瓦倫西亞',dt='06.05 – 06.20',ph='vlc',fo=(50,50))),
    dict(big=dict(name='Cup 2',zh='東京 · 日本',dt='08.05 – 08.29',ph='tyo',fo=(50,50)),
         intl=dict(kind='Champions',city='Austin',zh='奧斯汀',dt='09.16 – 10.10',ph='aus',fo=(50,55)))]
  def photo(x,y,w,h,ph,fo,a0=0.30,mx=0.88,dim=0.0):
    a=Image.open(PH+f'p_{ph}.jpg').convert('RGB');w_,h_=P(w),P(h)
    r=max(w_/a.width,h_/a.height);a=a.resize((round(a.width*r)+1,round(a.height*r)+1),Image.LANCZOS)
    ox=round((a.width-w_)*fo[0]/100);oy=round((a.height-h_)*fo[1]/100);a=a.crop((ox,oy,ox+w_,oy+h_))
    g=np.linspace(0,1,h_)[:,None];al=np.clip(np.clip((g-a0)/(1-a0),0,1)**1.2*mx+dim,0,0.92)
    im.paste(Image.fromarray((np.asarray(a).astype(float)*(1-al[:,:,None])).astype('uint8')),(P(x),P(y)))
  BW,BH,GAP=660,290,24;SX,SW=740,300
  for i,ev in enumerate(EVENTS):
    y=286+i*(BH+GAP);b=ev['big'];s=ev['intl']
    photo(40,y,BW,BH,b['ph'],b['fo'])
    chip(40,y,150,30,'REGIONAL  區域賽',14,bg=LIME,fg=INK,font=F(CB,14))
    if b.get('note'):chip(40+BW-246,y,246,30,b['note'],14,bg=INK,fg=LIME,font=F(CB,14))
    d.text((P(64),P(y+BH-84)),b['name'].replace(' ','  '),font=F(CL,64),fill=WHT,anchor='ls')
    d.text((P(64),P(y+BH-28)),b['zh'],font=F(CB,28),fill=LIME,anchor='ls')
    d.text((P(40+BW-24),P(y+BH-28)),b['dt'],font=F(CL,34),fill=WHT,anchor='rs')
    sh_=BH;sy=y
    photo(SX,sy,SW,sh_,s['ph'],s['fo'],a0=0.25,mx=0.9,dim=0.25)
    chip(SX,sy,168,26,'INTERNATIONAL  國際賽',12,bg=WHT,fg=INK,font=F(CB,12))
    d.text((P(SX+18),P(sy+sh_-88)),s['kind'].upper(),font=F(CL,16),fill=LIME,anchor='ls')
    d.text((P(SX+18),P(sy+sh_-50)),s['city'],font=F(CL,36),fill=WHT,anchor='ls')
    d.text((P(SX+18),P(sy+sh_-16)),s['zh'],font=F(CB,18),fill=GREY,anchor='ls')
    d.text((P(SX+SW-16),P(sy+sh_-16)),s['dt'],font=F(CL,19),fill=WHT,anchor='rs')
    arrow([(40+BW+8,y+BH/2),(SX-8,y+BH/2)])
    if i<2:arrow([(SX+SW/2,sy+sh_+8),(SX+SW/2,sy+sh_+8)]) if False else None
  d.text((P(40),P(1236)),'PHOTOS  ·  WIKIMEDIA COMMONS  ·  CC BY / CC BY-SA / CC0',font=FMN(11),fill=GREY,anchor='lm')
elif MODE=='partners':
  panel(20,262,1060,1252,(6,18,30),0.6);corners(20,262,1060,1252)
  LD=ROOT+'/assets/logos/pac/'
  Wc=(255,255,255);Kc=(12,12,12)
  T=[('Rex_Regum_Qeon_allmode.png',(244,163,55),Wc,.78,'Rex Regum Qeon','ID'),('ZETA_DIVISION_darkmode.png',(12,12,12),None,.78,'ZETA DIVISION','JP'),
     ('Gen.G_Esports_2026_allmode.png',(170,138,87),Wc,.74,'Gen.G','KR'),('T1_2019_allmode.png',(226,1,45),Wc,.80,'T1','KR'),
     ('GAM_Esports_2021_full_allmode.png',(250,183,23),Kc,.80,'GAM Esports','VN'),('Crazy_Raccoon_2021_allmode.png',(227,6,19),None,.82,'Crazy Raccoon','JP'),
     ('FULL_SENSE_2025_allmode.png',(247,71,10),Wc,.74,'FULL SENSE','TH'),('Paper_Rex_darkmode.png',(0,0,0),None,.74,'Paper Rex','SEA')]
  tw,th,pl=488,160,54;gx,gy=24,16;ty0=286
  for i,(f,bgc,fg,sc,nm,rg) in enumerate(T):
    x=40+(i%2)*(tw+gx);y=ty0+(i//2)*(th+pl+gy)
    blk(x,y,x+tw,y+th,bgc)
    lg_=Image.open(LD+f).convert('RGBA');lg_=lg_.crop(lg_.getbbox())
    if fg:
      m_=Image.new('RGBA',lg_.size,fg+(255,));m_.putalpha(lg_.getchannel('A'));lg_=m_
    r_=min(tw*sc*0.62/lg_.width,th*sc/lg_.height)
    lg_=lg_.resize((max(1,round(lg_.width*r_*S)),max(1,round(lg_.height*r_*S))),Image.LANCZOS)
    im.paste(lg_,(P(x+tw/2)-lg_.width//2,P(y+th/2)-lg_.height//2),lg_)
    blk(x,y+th,x+tw,y+th+pl,GREY)
    d.text((P(x+22),P(y+th+pl/2+1)),nm,font=F(CL,26),fill=INK,anchor='lm')
    chip(x+tw-22-72,y+th+pl/2-15,72,30,rg,18,bg=INK,fg=LIME)
  d.text((P(40),P(1234)),'Kickoff 曼谷　8 隊全數保證參賽',font=F(CB,22),fill=LIME,anchor='lm')

d.line([P(40),P(1278),P(1040),P(1278)],fill=WHT,width=max(1,S))
lg=Lg(ROOT+'/assets/sorai_logo_on_dark.png',P(34));lg=Image.merge('RGBA',(*[Image.new('L',lg.size,255)]*3,lg.getchannel('A')));im.paste(lg,(P(40),P(1296)),lg)
d.text((P(1040),P(1328)),'VCT PACIFIC 2027',font=FMN(14),fill=WHT,anchor='rs')
_a,_b=F(CB,13),F(CL,13);_t='Riot  Games';_x=P(1040)-round(_b.getlength(_t))
d.text((_x,P(1304)),_t,font=_b,fill=WHT,anchor='ls');d.text((_x,P(1304)),'來源：',font=_a,fill=WHT,anchor='rs')
im.save(OUT)
