# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os as _os
ROOT=_os.environ.get('VCT_ROOT',_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import _assets
_assets.preflight('reg',ROOT)
from PIL import Image,ImageDraw,ImageFont
import sys,math,os
REG=os.environ.get('REG','pac')
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
CFG={'pac':dict(bg='bg_pac',lock='pacific_kickoff_white.png',name='PACIFIC',LIME=(198,244,50),TINT=(6,18,30),LCQC=(24,92,120),LCO=(120,200,225),coord="13°45'N  ·  GLOBAL TOUR: ACTIVE",zone='ZONE: PACIFIC  ·  LEADERBOARD: CALIBRATING'),
 'emea':dict(bg='bg_eu',lock='europe_kickoff_white.png',name='EMEA',LIME=(205,245,40),TINT=(16,6,40),LCQC=(88,52,170),LCO=(176,150,255),coord="52°31'N  ·  GLOBAL TOUR: ACTIVE",zone='ZONE: EMEA  ·  LEADERBOARD: CALIBRATING'),
 'amer':dict(bg='bg_euam',lock='americas_kickoff_white.png',name='AMERICAS',LIME=(255,122,26),TINT=(22,10,4),LCQC=(128,50,12),LCO=(255,166,96),coord="23°33'S  ·  GLOBAL TOUR: ACTIVE",zone='ZONE: AMERICAS  ·  LEADERBOARD: CALIBRATING')}[REG]
LIME=CFG['LIME'];INK=(22,22,22);WHT=(255,255,255);MUT=(160,170,176);LCQC=CFG['LCQC'];LCO=CFG['LCO'];TINT=CFG['TINT'];GREY=(222,226,228);CY=(0,190,214);RN=CFG['name']
im=Image.open(ROOT+'/assets/'+CFG['bg']+('@2x' if S==2 else '')+'.png').convert('RGB');d=ImageDraw.Draw(im)
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
  parts=[p for p in re.split(r'(Cup(?: \d)?|CUP|Kickoff)',t) if p!='']
  runs=[]
  for i,p in enumerate(parts):
    if re.fullmatch(r'Cup(?: \d)?|CUP|Kickoff',p):runs.append((p.replace(' ','  '),fl,True))
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
PFX='VCT '+RN+' 2027 · '
if REG=='pac':
  if MODE=='slots':TITLE='Cup 名額分配';KICK=PFX+'CUP SLOTS';TSZ=84
  elif MODE=='path':TITLE='公開資格賽晉級 Cup 路線';KICK=PFX+'PATH TO CUPS';TSZ=66
  elif MODE=='lcq':TITLE='Cup 最終資格賽';KICK=PFX+'CUP LCQ';TSZ=84
  elif MODE=='overview':TITLE='2027 賽季全貌';KICK=PFX+'SEASON MAP'
  else:TITLE='合作夥伴隊伍';KICK=PFX+'PARTNER TEAMS'
else:
  BRT={'br_eu':('歐洲區賽制','EUROPE QUALIFIERS'),'br_tr':('土耳其區賽制','TÜRKIYE QUALIFIERS'),'br_mena':('中東北非區賽制','MENA QUALIFIERS'),
       'br_na':('北美區賽制','NORTH AMERICA QUALIFIERS'),'br_br':('巴西區賽制','BRAZIL QUALIFIERS'),'br_latam':('拉丁美洲區賽制','LATAM QUALIFIERS')}
  if MODE in BRT:TITLE=BRT[MODE][0];KICK=PFX+BRT[MODE][1];TSZ=84
  elif MODE=='slots':TITLE='Kickoff 名額分配';KICK=PFX+'KICKOFF SLOTS';TSZ=84
  elif MODE=='path':TITLE='公開資格賽晉級 Kickoff 路線';KICK=PFX+'PATH TO KICKOFF';TSZ=62
  elif MODE=='lcq':TITLE='Kickoff 最終資格賽';KICK=PFX+'KICKOFF LCQ';TSZ=84
  elif MODE=='overview':TITLE='2027 賽季全貌';KICK=PFX+'SEASON MAP'
  else:TITLE='合作夥伴隊伍';KICK=PFX+'PARTNER TEAMS'
panel(0,250,1080,252,(255,255,255),0.0)
_lk=Lg(ROOT+'/assets/'+CFG['lock'],P(64));im.paste(_lk,(P(40),P(40)),_lk)
d.text((P(1040),P(84)),KICK,font=F(CL,17),fill=WHT,anchor='rs')
T(37,206,TITLE,TSZ or (84 if len(TITLE)<9 else 66),WHT,'ls')
d.line([P(24),P(118),P(1056),P(118)],fill=WHT,width=max(1,S))
for x in (24,1056):d.line([P(x),P(110),P(x),P(126)],fill=WHT,width=max(1,S))
d.text((P(1056),P(140)),CFG['coord'],font=FMN(12),fill=WHT,anchor='rs')
d.text((P(1056),P(30)),CFG['zone'],font=FMN(12),fill=WHT,anchor='rs')
def chip(x,y,w,h,t,fs,bg=LIME,fg=INK,font=None):
  blk(x,y,x+w,y+h,bg);ct(x+w/2,y+h/2+1,t,font or F(CL,fs),fg)
def pill(cx,cy,w,t,kind,h=34,fs=17):
  bg,fg=(LIME,INK) if kind=='cup' else (LCQC,WHT)
  blk(cx-w/2,cy-h/2,cx+w/2,cy+h/2,bg);ct(cx,cy+1,t,F(CL,fs),fg)
  if kind!='cup':d.rectangle([P(cx-w/2),P(cy-h/2),P(cx+w/2),P(cy+h/2)],outline=LCO,width=max(1,S))
REGN={'KR':'韓國','JP':'日本','SEA':'東南亞','TH':'泰國','ID':'印尼','VN':'越南','LCQ':'最終資格賽','SA':'南亞','OCE':'大洋洲'}
def corners(x1,y1,x2,y2,c=WHT,L=14):
  for X,sx in ((x1,1),(x2,-1)):
    for Y,sy in ((y1,1),(y2,-1)):
      d.line([P(X),P(Y),P(X+sx*L),P(Y)],fill=c,width=max(1,S));d.line([P(X),P(Y),P(X),P(Y+sy*L)],fill=c,width=max(1,S))
def CUPB(x,y,so,sn):
  if OLD:d.text((P(x),P(y)),'盃賽',font=F(CB,so),fill=WHT,anchor='lm')
  else:d.text((P(x),P(y)),'CUP',font=F(CL,sn),fill=WHT,anchor='lm')
def PT():
  LD=ROOT+'/assets/logos/pac/'
  Wc=(255,255,255);Kc=(12,12,12)
  if REG=='emea':
    LD=ROOT+'/assets/logos/pac/';Wc=(255,255,255);Kc=(12,12,12)
    T=[('Team_Heretics_2024_allmode.png',(15,15,15),None,.78,'Team Heretics','EU'),('Fnatic_2020_allmode.png',(255,89,0),Wc,.72,'Fnatic','EU'),
       ('Team_Vitality_2023_darkmode.png',(254,255,0),Kc,.74,'Team Vitality','EU'),('Team_Liquid_2024_darkmode.png',(0,21,56),None,.78,'Team Liquid','EU'),
       ('Gentle_Mates_2024_lightmode.png',(239,160,225),None,.76,'Gentle Mates','EU'),('Karmine_Corp_2024_darkmode.png',(1,200,254),Kc,.74,'Karmine Corp','EU'),
       ('BBL_Esports_2022_darkmode.png',(203,152,3),Wc,.72,'BBL Esports','TR'),('Futbolist_2021_darkmode.png',(237,26,58),Wc,.74,'FUT Esports','TR')]
  elif REG=='amer':
    LD=ROOT+'/assets/logos/am/';Wc=(255,255,255);Kc=(12,12,12)
    T=[('100_Thieves_darkmode.png',(234,49,49),Wc,.74,'100 Thieves','NA'),('G2_Esports_2020_lightmode.png',(15,15,15),None,.74,'G2 Esports','NA'),
       ('NRG_2024_allmode.png',(246,61,10),Wc,.74,'NRG','NA'),('Sentinels_V_white.png',(231,1,44),None,.62,'Sentinels','NA'),
       ('LOUD_allmode.png',(31,250,2),Kc,.74,'LOUD','BR'),('MIBR_2018_darkmode.png',(16,24,32),None,.74,'MIBR','BR'),
       ('Leviatan_2023_icon_allmode.png',(106,171,220),Wc,.74,'LEVIATÁN','LATAM'),('KRU_Esports_allmode.png',(255,25,143),Kc,.74,'KRÜ Esports','LATAM')]
  else:
   T=[('Rex_Regum_Qeon_allmode.png',(244,163,55),Wc,.78,'Rex Regum Qeon','ID'),('ZETA_DIVISION_darkmode.png',(12,12,12),None,.78,'ZETA DIVISION','JP'),
      ('Gen.G_Esports_2026_allmode.png',(170,138,87),Wc,.74,'Gen.G','KR'),('T1_2019_allmode.png',(226,1,45),Wc,.80,'T1','KR'),
      ('GAM_Esports_2021_full_allmode.png',(250,183,23),Kc,.80,'GAM Esports','VN'),('Crazy_Raccoon_2021_allmode.png',(227,6,19),None,.82,'Crazy Raccoon','JP'),
      ('FULL_SENSE_2025_allmode.png',(247,71,10),Wc,.74,'FULL SENSE','TH'),('Paper_Rex_darkmode.png',(0,0,0),None,.74,'Paper Rex','SEA')]
  return LD,T
if REG=='pac' and MODE=='slots':
  # strip
  panel(0,262,1080,382,TINT,0.62)
  d.text((P(40),P(352)),'12',font=F(CL,104),fill=LIME,anchor='ls');d.text((P(40+F(CL,104).getlength('12')/S+10),P(350)),'隊',font=F(CB,40),fill=WHT,anchor='ls')
  T(300,318,'Cup 1・Cup 2 參賽隊伍',28,WHT,'ls')
  d.text((P(300),P(354)),'KR 3 + JP 3 + SEA 2 + TH 1 + ID 1 + VN 1 + LCQ 1',font=FMN(15),fill=LIME,anchor='ls')
  panel(20,404,1060,1184,TINT,0.6)
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
elif REG=='pac' and MODE=='path':
  panel(20,270,1060,1244,TINT,0.6)
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
  blk(590,by,1040,by+66,LCQC);d.rectangle([P(590),P(by),P(1040),P(by+66)],outline=LCO,width=max(1,S))
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
  blk(180,1218,204,1230,LCQC);d.rectangle([P(180),P(1218),P(204),P(1230)],outline=LCO,width=max(1,S));d.text((P(214),P(1224)),'LCQ 晉級',font=F(CB,16),fill=WHT,anchor='lm')
  d.text((P(1040),P(1224)),'南亞、大洋洲直接進 Playoffs，無 Play-ins',font=F(CB,16),fill=WHT,anchor='rm')
elif REG=='pac' and MODE=='lcq':
  panel(20,270,1060,1196,TINT,0.6)
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

def lp(cx,cy,w,h,t,sz,bg=LIME,fg=INK,ol=None,x=None):
  blk(cx-w/2,cy-h/2,cx+w/2,cy+h/2,bg)
  if ol:d.rectangle([P(cx-w/2),P(cy-h/2),P(cx+w/2),P(cy+h/2)],outline=ol,width=max(1,S))
  T(cx,cy+1,t,sz,fg,'mm')
def step(x,y,w,h,title,subs,tsz=21,ssz=15):
  blk(x,y,x+w,y+h,GREY)
  n=len(subs);lh=ssz+9;tot=tsz+(8+n*lh if n else 0);yy=y+h/2-tot/2+tsz/2+2
  T(x+w/2,yy,title,tsz,INK,'mm')
  for i,t in enumerate(subs):
    yy2=yy+tsz/2+8+lh*i+lh/2
    T(x+w/2,yy2,t,ssz,(55,55,55),'mm')
def kbox(x,y,w,h,l1,l2=None,l3=None):
  blk(x,y,x+w,y+h,INK);d.rectangle([P(x+6),P(y+6),P(x+w-6),P(y+h-6)],outline=WHT,width=max(1,S))
  d.text((P(x+30),P(y+38)),'KICKOFF',font=F(CL,38),fill=WHT,anchor='lm');mark(x+240,y+38,38)
  T(x+30,y+h-30,l1,22,LIME,'lm')
def lbox(x,y,w,h,l1,l2=None,l3=None):
  blk(x,y,x+w,y+h,LCQC);d.rectangle([P(x),P(y),P(x+w),P(y+h)],outline=LCO,width=max(1,S))
  d.text((P(x+30),P(y+38)),'AMERICAS LCQ',font=F(CL,32),fill=WHT,anchor='lm')
  T(x+30,y+h-30,l1,22,WHT,'lm')
def tick(x,y,L=10):
  for X,sx in ((x,1),):pass
def pn(x1,y1,x2,y2):
  panel(x1,y1,x2,y2,TINT,0.6)
  for (x,y) in [(x1,y1),(x2,y1),(x1,y2),(x2,y2)]:
    d.line([P(x-10),P(y),P(x+10),P(y)],fill=WHT,width=max(1,S));d.line([P(x),P(y-10),P(x),P(y+10)],fill=WHT,width=max(1,S))
if REG!='pac' and MODE=='slots':
  panel(0,262,1080,382,TINT,0.62)
  d.text((P(40),P(352)),'12',font=F(CL,104),fill=LIME,anchor='ls');d.text((P(40+F(CL,104).getlength('12')/S+10),P(350)),'隊',font=F(CB,40),fill=WHT,anchor='ls')
  T(300,318,'Kickoff 參賽隊伍',28,WHT,'ls')
  d.text((P(300),P(354)),'PARTNER 8 + EU 2 + TR 1 + MENA 1' if REG=='emea' else 'PARTNER 8 + NA 1 + BR 1 + LATAM 1 + LCQ 1',font=FMN(15),fill=LIME,anchor='ls')
  pn(20,404,1060,1184)
  chip(50,424,150,28,'PARTNER',16);d.text((P(214),P(439)),'合作夥伴隊　8 隊直接入選',font=F(CB,18),fill=WHT,anchor='lm')
  LD,TL=PT();tw,th,pl=232,72,30;gx=18
  for i,(f,bgc,fg,sc,nm,rg) in enumerate(TL):
    x=50+(i%4)*(tw+gx);y=462+(i//4)*(th+pl+12)
    blk(x,y,x+tw,y+th,bgc)
    lg_=Image.open(LD+f).convert('RGBA');lg_=lg_.crop(lg_.getbbox())
    if fg:
      m_=Image.new('RGBA',lg_.size,fg+(255,));m_.putalpha(lg_.getchannel('A'));lg_=m_
    r_=min(tw*sc*0.5/lg_.width,th*sc/lg_.height)
    lg_=lg_.resize((max(1,round(lg_.width*r_*S)),max(1,round(lg_.height*r_*S))),Image.LANCZOS)
    im.paste(lg_,(P(x+tw/2)-lg_.width//2,P(y+th/2)-lg_.height//2),lg_)
    blk(x,y+th,x+tw,y+th+pl,GREY);d.text((P(x+12),P(y+th+pl/2+1)),nm,font=F(CL,15),fill=INK,anchor='lm')
  chip(50,692,220,28,'OPEN QUALIFIERS',16);d.text((P(284),P(707)),'公開資格賽名額',font=F(CB,18),fill=WHT,anchor='lm')
  if REG=='emea':rows=[('EU','歐洲',2),('TR','土耳其',1),('MENA','中東與北非',1)];pitch=108;ch=90;cf=40
  else:rows=[('NA','北美',1),('BR','巴西',1),('LATAM','拉丁美洲',1),('LCQ','最終資格賽',1)];pitch=90;ch=72;cf=40
  y0=734
  for i,(c,zh,n) in enumerate(rows):
    y=y0+i*pitch
    chip(50,y,132,46 if REG=='amer' else 58,c,cf if len(c)<4 else 32 if len(c)==4 else 28)
    d.text((P(116),P(y+(62 if REG=='amer' else 82))),zh,font=F(CB,16 if len(zh)<5 else 13),fill=WHT,anchor='mm')
    d.text((P(204),P(y+37)),f'{n}',font=F(CL,40),fill=LIME,anchor='ls');d.text((P(234),P(y+37)),'席',font=F(CB,20),fill=WHT,anchor='ls')
    for k in range(n):
      x=290+k*250
      blk(x,y,x+236,y+ch,INK);d.rectangle([P(x+5),P(y+5),P(x+231),P(y+ch-5)],outline=WHT,width=max(1,S))
      mark(x+40,y+ch/2,48 if ch>80 else 40)
      d.text((P(x+78),P(y+ch/2+1)),f'#{k+1}',font=F(CL,34),fill=LIME,anchor='lm')
      d.text((P(x+222),P(y+ch/2+1)),('LCQ' if c=='LCQ' else '公開資格賽'),font=F(CB,15) if c!='LCQ' else F(CL,22),fill=GREY,anchor='rm')
  if REG=='amer':d.text((P(1036),P(1108)),'LCQ：北美、巴西、拉丁美洲亞軍爭奪最後 1 席',font=F(CB,18),fill=WHT,anchor='rm')
  _o=(0,0) if REG=='emea' else (-10,-12)
  T(1036,1120+(14 if REG=='amer' else 0)+(0),'Kickoff 前 3 名晉級 Masters 首爾',18,WHT,'rm')
  T(1036,1148+(12 if REG=='amer' else 0),'合作夥伴隊不保證 Cup 席次，需與公開資格賽隊伍競爭',18,WHT,'rm')
if REG=='emea' and MODE=='path':
  pn(20,270,1060,1244)
  X0=[40,380,720];W3=320
  heads=[('EUROPE','歐洲　2 席'),('TÜRKIYE','土耳其　1 席'),('MENA','中東與北非　1 席')]
  for x,(h_,z_) in zip(X0,heads):
    chip(x,292,W3,48,h_,28);d.text((P(x+W3/2),P(358)),z_,font=F(CB,16),fill=GREY,anchor='mm')
  A,Bq,C=380,574,768;SH=150
  def qq(x,t1,d1,t2,d2,extra):
    for k,(t,dd) in enumerate(((t1,d1),(t2,d2))):
      bx=x+k*(154+12);step(bx,A,154,SH,t,([dd] if dd else [])+extra,tsz=22,ssz=14)
    mid=x+W3/2
    for k in range(2):
      cx=x+77+k*166;ln([(cx,A+SH),(cx,A+SH+22),(mid,A+SH+22)])
    arrow([(mid,A+SH+22),(mid,Bq-6)])
  qq(X0[0],'Qualifier 1','','Qualifier 2','',[])
  qq(X0[1],'Qualifier 1','','Qualifier 2','',[])
  qq(X0[2],'Qualifier 1','','Qualifier 2','',[])
  step(X0[0],Bq,W3,SH,'Qualifier Playoffs',['16 隊'],tsz=24,ssz=17)
  step(X0[1],Bq,W3,SH,'Qualifier Playoffs',['8 隊'],tsz=24,ssz=17)
  step(X0[2],Bq,W3,SH,'Bo5 決勝賽',[],tsz=24,ssz=17)
  step(X0[0],C,W3,SH,'雙敗淘汰',[],tsz=24,ssz=17)
  step(X0[1],C,W3,SH,'GSL 小組賽 → 雙敗淘汰',[],tsz=24,ssz=17)
  step(X0[2],C,W3,SH,'MENA Final',[],tsz=24,ssz=17)
  for x in X0:arrow([(x+W3/2,Bq+SH),(x+W3/2,C-6)]);arrow([(x+W3/2,C+SH),(x+W3/2,C+SH+36)])
  for x,t in zip(X0,['前 2 名晉級 Kickoff','冠軍晉級 Kickoff','冠軍晉級 Kickoff']):
    lp(x+W3/2,C+SH+58,W3,44,t,20)
  ky=1080
  for x in X0:arrow([(x+W3/2,C+SH+80),(x+W3/2,ky-8)])
  kbox(40,ky,1000,110,'柏林 ・ 德國　　前 3 名晉級 Masters 首爾')
  d.text((P(1040),P(1214)),'合作夥伴隊直接入選 Kickoff，不需參加公開資格賽',font=F(CB,16),fill=WHT,anchor='rm')
if REG=='amer' and MODE=='path':
  pn(20,270,1060,1244)
  X0=[40,380,720];W3=320
  heads=[('NORTH AMERICA','北美　1 席'),('BRAZIL','巴西　1 席'),('LATAM','拉丁美洲　1 席')]
  for x,(h_,z_) in zip(X0,heads):
    chip(x,292,W3,48,h_,28);d.text((P(x+W3/2),P(358)),z_,font=F(CB,16),fill=GREY,anchor='mm')
  A,Bq,C=380,574,768;SH=150
  def qq(x,t1,d1,t2,d2,extra):
    for k,(t,dd) in enumerate(((t1,d1),(t2,d2))):
      bx=x+k*(154+12);step(bx,A,154,SH,t,([dd] if dd else [])+extra,tsz=22,ssz=14)
    mid=x+W3/2
    for k in range(2):
      cx=x+77+k*166;ln([(cx,A+SH),(cx,A+SH+22),(mid,A+SH+22)])
    arrow([(mid,A+SH+22),(mid,Bq-6)])
  qq(X0[0],'Qualifier 1','','Qualifier 2','',[])
  qq(X0[1],'Qualifier 1','','Qualifier 2','',[])
  qq(X0[2],'North 北區','','South 南區','',[])
  step(X0[0],Bq,W3,SH,'Qualifier Playoffs',['16 隊 ・ 瑞士制'],tsz=24,ssz=17)
  step(X0[1],Bq,W3,SH,'Qualifier Playoffs',['16 隊 ・ 瑞士制'],tsz=24,ssz=17)
  step(X0[2],Bq,W3,SH,'南、北各自 Playoffs',['各區 8 隊'],tsz=24,ssz=17)
  step(X0[0],C,W3,SH,'雙敗淘汰 ・ 8 隊',[],tsz=24,ssz=17)
  step(X0[1],C,W3,SH,'雙敗淘汰 ・ 8 隊',[],tsz=24,ssz=17)
  step(X0[2],C,W3,SH,'LATAM Final',['Bo5 ・ LAN'],tsz=24,ssz=17)
  P1=C+SH+56;P2=P1+52
  for x in X0:
    arrow([(x+W3/2,Bq+SH),(x+W3/2,C-6)]);arrow([(x+W3/2,C+SH),(x+W3/2,P1-22-2)])
    lp(x+W3/2,P1,W3,44,'冠軍晉級 Kickoff',20)
    lp(x+W3/2,P2,W3,44,'亞軍進 LCQ',20,bg=LCQC,fg=WHT,ol=LCO)
  ky=1086
  kbox(40,ky,580,100,'各區冠軍晉級 ・ 聖保羅 ・ 巴西')
  lbox(640,ky,400,100,'各區亞軍進入')
  blk(40,1214,64,1226,LIME);T(74,1220,'Kickoff 晉級',16,WHT,'lm')
  blk(200,1214,224,1226,LCQC);d.rectangle([P(200),P(1214),P(224),P(1226)],outline=LCO,width=max(1,S));d.text((P(234),P(1220)),'LCQ 晉級',font=F(CB,16),fill=WHT,anchor='lm')
if REG=='amer' and MODE=='lcq':
  pn(20,270,1060,1130)
  rows=[('NA','北美'),('BR','巴西'),('LATAM','拉丁美洲')]
  BX=720;ys=[]
  for i,(c,zh) in enumerate(rows):
    cy=334+i*134
    w=150
    blk(40,cy-30,380,cy+30,GREY);blk(40,cy-30,40+w,cy+30,INK);ct(40+w/2,cy+1,c,F(CL,32),LIME);ct(40+w+(340-w)/2,cy+1,zh+' 亞軍',F(CB,24),INK)
    lp(540,cy,170,44,'亞軍  '+c,22) if False else None
    pill(540,cy,170,'#2  '+c,'cup',h=44,fs=24)
    arrow([(388,cy),(447,cy)])
    ln([(633,cy),(BX,cy)]);ys.append(cy)
  ln([(BX,min(ys)),(BX,690)])
  arrow([(BX,max(ys)),(BX,706)])
  step(BX-170,712,340,110,'Americas LCQ',['聖保羅'],tsz=26,ssz=17)
  arrow([(BX,822),(BX,880)])
  pill(BX,910,170,'#1  LCQ','cup',h=48,fs=28)
  cupy=1000
  arrow([(BX,934),(BX,cupy-8)])
  blk(BX-170,cupy,BX+170,cupy+96,INK);d.rectangle([P(BX-164),P(cupy+6),P(BX+164),P(cupy+90)],outline=WHT,width=max(1,S))
  d.text((P(BX-130),P(cupy+48)),'KICKOFF',font=F(CL,44),fill=WHT,anchor='lm');mark(BX+120,cupy+48,56)

if MODE.startswith('br_'):
  pn(20,270,1060,1244)
  SUBC=(190,196,200)
  def bxx(x,y,w,h,t,sub=None,fill=INK,fg=WHT,bar=None,fs=17,ss=12,sc=SUBC,ol=None):
    blk(x,y,x+w,y+h,fill)
    if ol:d.rectangle([P(x),P(y),P(x+w),P(y+h)],outline=ol,width=max(1,S))
    if bar:blk(x,y,x+4,y+h,bar)
    if sub:
      tot=fs+ss+8;t0=y+h/2-tot/2+fs/2;T(x+w/2,t0,t,fs,fg,'mm');T(x+w/2,t0+fs/2+4+ss/2,sub,ss,sc,'mm')
    else:T(x+w/2,y+h/2+1,t,fs,fg,'mm')
  def dsh(x1,y1,x2,y2,c=LIME,w=2,dl=7,gp=5):
    L=math.hypot(x2-x1,y2-y1);n=int(L//(dl+gp))+1
    for k in range(n):
      a=k*(dl+gp)/L;b=min(1,(k*(dl+gp)+dl)/L)
      ln([(x1+(x2-x1)*a,y1+(y2-y1)*a),(x1+(x2-x1)*b,y1+(y2-y1)*b)],c,w)
  def stg(x,y,t):d.text((P(x),P(y)),t,font=FMN(12),fill=LIME,anchor='ls')
  def legend(lcq=False):
    blk(40,1214,64,1226,LIME);T(74,1220,'Kickoff 晉級',16,WHT,'lm')
    if lcq:
      blk(200,1214,224,1226,LCQC);d.rectangle([P(200),P(1214),P(224),P(1226)],outline=LCO,width=max(1,S));d.text((P(234),P(1220)),'LCQ 晉級',font=F(CB,16),fill=WHT,anchor='lm')
  def flow(y,items,h=104,W=306,G=41,fs=21,ss=15):
    xs=[40+i*(W+G) for i in range(len(items))]
    for k,(x,(t,sb)) in enumerate(zip(xs,items)):
      step(x,y,W,h,t,sb,tsz=fs,ssz=ss)
      if k<len(items)-1:arrow([(x+W+6,y+h/2),(x+W+G-6,y+h/2)])
    return xs
  def dpath(pts,c=LIME,arrowhead=True):
    for (xa,ya),(xb,yb) in zip(pts[:-1],pts[1:]):dsh(xa,ya,xb,yb,c)
    if arrowhead:
      (x0,y0),(x1,y1)=pts[-2],pts[-1];a=math.atan2(y1-y0,x1-x0);k=9
      d.polygon([(P(x1),P(y1)),(P(x1-k*math.cos(a-0.45)),P(y1-k*math.sin(a-0.45))),(P(x1-k*math.cos(a+0.45)),P(y1-k*math.sin(a+0.45)))],fill=c)
  # ---- 8-team double elimination (Americas NA / BR)
  # all stacks: 40px boxes on a 48px pitch (8px gaps). Dashed lime = drop from upper bracket; every drop line
  # runs in a gutter / corridor and ends on a box edge with an arrow, never across a box.
  def de8(oy):
    cw=156;CX=[64+i*204 for i in range(5)];bh=20
    QF=[oy+20+48*i for i in range(4)];SF=[oy+44,oy+140];UF=oy+92
    LA,LBc=oy+250,oy+330;LS=oy+290;GF=oy+191
    def b(c,y,t,low=False):bxx(CX[c],y-bh,cw,2*bh,t,bar=LIME if low else None,fs=16)
    def jn(c,ya,yb,yo):
      xm=CX[c]+cw+14;ln([(CX[c]+cw,ya),(xm,ya),(xm,yb),(CX[c]+cw,yb)]);ln([(xm,yo),(CX[c+1],yo)])
    for y in QF:b(0,y,'勝部首輪')
    for y in SF:b(1,y,'勝部準決賽')
    b(2,UF,'勝部決賽')
    for y in (LA,LBc):b(0,y,'敗部第一輪',True)
    for y in (LA,LBc):b(1,y,'敗部第二輪',True)
    b(2,LS,'敗部準決賽',True);b(3,LS,'敗部決賽',True)
    bxx(CX[4],GF-34,cw,68,'總決賽','GRAND FINAL',fill=GREY,fg=INK,sc=(60,60,60),fs=20)
    jn(0,QF[0],QF[1],SF[0]);jn(0,QF[2],QF[3],SF[1]);jn(1,SF[0],SF[1],UF)
    for y in (LA,LBc):ln([(CX[0]+cw,y),(CX[1],y)])
    jn(1,LA,LBc,LS)
    ln([(CX[2]+cw,LS),(CX[3],LS)])
    xg=CX[3]+cw+16
    ln([(CX[3]+cw,LS),(xg,LS),(xg,GF+10),(CX[4],GF+10)])
    ln([(CX[2]+cw,UF),(xg,UF),(xg,GF-10),(CX[4],GF-10)])
    lx1,lx2=CX[0]-16,CX[0]-32
    dpath([(CX[0],QF[2]),(lx1,QF[2]),(lx1,LA),(CX[0]-2,LA)])
    dsh(CX[0],QF[3],lx1,QF[3])
    dpath([(CX[0],QF[0]),(lx2,QF[0]),(lx2,LBc),(CX[0]-2,LBc)])
    dsh(CX[0],QF[1],lx2,QF[1])
    cx1=CX[1]+cw/2
    dpath([(cx1,SF[1]+bh),(cx1,LA-bh-2)])
    chn=CX[1]-14;cor=(LA+LBc)/2
    dpath([(cx1,SF[0]+bh),(cx1,oy+92),(chn,oy+92),(chn,cor),(cx1,cor),(cx1,LBc-bh-2)])
    cx2=CX[2]+cw/2;cx3=CX[3]+cw/2;yb=oy+232
    dpath([(cx2,UF+bh),(cx2,yb),(cx3,yb),(cx3,LS-bh-2)])
    return CX[4]+cw/2,GF+34
  # ---- 4-team double elimination (TR / LATAM)
  def de4(x0,y0,cw=140,st=170,bh=18,labs=True):
    CX=[x0+i*st for i in range(3)]
    S1,S2=y0,y0+60;UF=y0+30;LB1=y0+150;LBF=y0+150;GF=y0+90
    def b(c,y,t,low=False):bxx(CX[c],y-bh,cw,2*bh,t,bar=LIME if low else None,fs=15)
    b(0,S1,'勝部準決賽');b(0,S2,'勝部準決賽');b(1,UF,'勝部決賽')
    b(0,LB1,'敗部首輪',True);b(1,LBF,'敗部決賽',True)
    bxx(CX[2],GF-bh-4,cw,2*bh+8,'總決賽',None,fill=GREY,fg=INK,fs=16)
    xm=CX[0]+cw+14;ln([(CX[0]+cw,S1),(xm,S1),(xm,S2),(CX[0]+cw,S2)]);ln([(xm,UF),(CX[1],UF)])
    ln([(CX[0]+cw,LB1),(CX[1],LBF)])
    xg=CX[1]+cw+14
    ln([(CX[1]+cw,UF),(xg,UF),(xg,GF-8),(CX[2],GF-8)]);ln([(CX[1]+cw,LBF),(xg,LBF),(xg,GF+8),(CX[2],GF+8)])
    lx=CX[0]-16;dsh(CX[0],S2,lx,S2);dpath([(CX[0],S1),(lx,S1),(lx,LB1),(CX[0]-2,LB1)])
    dpath([(CX[1]+cw/2,UF+bh),(CX[1]+cw/2,LBF-bh-2)])
    return CX[2]+cw/2,GF+bh+4
  # ============ Americas NA / BR
  if MODE in('br_na','br_br'):
    na=MODE=='br_na'
    stg(40,298,'STAGE 1 · QUALIFIERS')
    
    step(40,310,306,56,'Qualifier #1',[],tsz=20,ssz=14)
    step(40,374,306,56,'Qualifier #2',[],tsz=20,ssz=14)
    bxx(386,310,306,120,'Bo3 單敗淘汰',None,fill=INK,fs=22,ss=15)
    step(732,310,308,120,'晉級隊',[],tsz=22,ssz=15)
    ln([(346,338),(366,338),(366,370),(386,370)]);ln([(346,402),(366,402),(366,370)]);arrow([(366,370),(380,370)])
    arrow([(692,370),(726,370)])
    arrow([(886,430),(886,462)])
    stg(40,454,'STAGE 2 · QUALIFIER PLAYOFFS')
    step(40,462,1000,68,'Qualifier Playoffs ・ 16 隊',['資格賽晉級隊 ＋ 受邀隊（2026 未續約的 VCT Americas 隊伍、頂尖 Challengers 與 Game Changers 隊伍）'],tsz=22,ssz=14)
    arrow([(540,530),(540,554)])
    stg(40,554,'STAGE 2A · SWISS STAGE')
    step(40,562,1000,68,'瑞士制 ・ 16 隊',['取得 2 勝晉級 ・ 剩餘 8 隊進入雙敗淘汰'],tsz=22,ssz=15)
    arrow([(540,630),(540,654)])
    stg(40,654,'STAGE 2B · DOUBLE ELIMINATION')
    gx,gy=de8(668)
    ry=1090;mid=ry-24;kx,lx=40,560;bw=480
    ln([(gx,gy),(gx,mid),(lx+bw/2,mid)]);ln([(kx+bw/2,mid),(gx,mid)])
    arrow([(kx+bw/2,mid),(kx+bw/2,ry-4)]);arrow([(lx+bw/2,mid),(lx+bw/2,ry-4)])
    kbox(kx,ry,bw,100,'冠軍晉級 ・ 聖保羅 ・ 巴西')
    lbox(lx,ry,bw,100,'亞軍進入')
    if na:
      T(330,1220,'冠、亞軍同時取得 Red Bull Home Ground World Final 資格（洛杉磯）',14,WHT,'lm')
    T(1040,648,'賽程樹狀為示意，各場對陣以官方公布為準',13,MUT,'rm')
    legend(True)
  # ============ LATAM
  if MODE=='br_latam':
    stg(40,298,'STAGE 01 · QUALIFIERS')
    flow(310,[('公開資格賽 Qualifier #1 ＋ #2',[]),
              ('Bo3 單敗淘汰',[]),
              ('Playoffs',['每區 8 隊 ＝ 晉級隊 ＋ 受邀隊'])],h=116,fs=20,ss=14)
    regs=[('LATAM NORTH','北區',40,['','']),('LATAM SOUTH','南區',560,['',''])]
    outs=[]
    for c,zh,x,dts in regs:
      chip(x,456,300,40,c,24);d.text((P(x+316),P(477)),zh,font=F(CB,20),fill=WHT,anchor='lm')
      step(x,508,480,76,'瑞士制 ・ 8 隊',['2 勝晉級'],tsz=22,ssz=15)
      arrow([(x+240,584+4),(x+240,610)])
      step(x,616,480,76,'雙敗淘汰 ・ 4 隊',[],tsz=22,ssz=15)
      gx_,gy_=de4(x+10,762,cw=140,st=170)
      outs.append((gx_,gy_))
    fy=964;fw=420;fx=330
    for gx_,gy_ in outs:
      ln([(gx_,gy_),(gx_,fy-30)]);ln([(gx_,fy-30),(540,fy-30)])
    arrow([(540,fy-30),(540,fy-4)])
    bxx(fx,fy,fw,80,'LATAM Final','Bo5 ・ LAN',fill=GREY,fg=INK,sc=(55,55,55),fs=26,ss=16)
    ry=1092;mid=ry-22;kx,lx=40,560;bw=480
    ln([(540,fy+80),(540,mid)]);ln([(kx+bw/2,mid),(lx+bw/2,mid)])
    arrow([(kx+bw/2,mid),(kx+bw/2,ry-4)]);arrow([(lx+bw/2,mid),(lx+bw/2,ry-4)])
    kbox(kx,ry,bw,100,'冠軍晉級 ・ 聖保羅 ・ 巴西')
    lbox(lx,ry,bw,100,'亞軍進入')
    legend(True)
  # ============ Europe
  if MODE=='br_eu':
    stg(40,298,'STAGE 01 · 02 · 03')
    flow(310,[('Qualifier 1 ＋ Qualifier 2',['Bo3 單敗淘汰 ・ 各取前 4 名']),
              ('Qualifier Playoffs',['16 隊 ＝ 8 晉級 ＋ 8 受邀']),
              ('雙敗淘汰',['Bo3 ・ 總決賽 Bo5','前 2 名晉級 Kickoff'])],h=104,fs=19,ss=14)
    k=1.8;OX=40-430*k;OY=450-116*k
    X=lambda v:OX+v*k;Y=lambda v:OY+v*k
    IX=(430,536);SX=(565,670);FX=(698,803);PX=(832,964)
    inv=[141+30*i for i in range(8)];semi=[156,216,276,336];fin=[186,306];bh=11*k
    def box(xr,yc,t,low=False,fill=INK,fg=WHT,sc=SUBC):
      x1=X(xr[0]);bxx(x1,Y(yc)-bh,X(xr[1])-x1,2*bh,t,bar=LIME if low else None,fill=fill,fg=fg,fs=16)
    stg(40,462-10,'STAGE 03 · DOUBLE ELIMINATION')
    for y in inv:box(IX,y,'受邀隊伍')
    for y in semi:box(SX,y,'勝部準決賽')
    for y in fin:box(FX,y,'勝部決賽')
    def jn(xa,xb,ya,yb,yo,xo):
      xm=(X(xa)+X(xo))/2 if False else X(xa)+16
      ln([(X(xa),Y(ya)),(xm,Y(ya)),(xm,Y(yb)),(X(xa),Y(yb))]);ln([(xm,Y(yo)),(X(xo),Y(yo))])
    for i in range(0,8,2):jn(IX[1],0,inv[i],inv[i+1],(inv[i]+inv[i+1])/2,SX[0])
    for i in range(0,4,2):jn(SX[1],0,semi[i],semi[i+1],(semi[i]+semi[i+1])/2,FX[0])
    jn(FX[1],0,fin[0],fin[1],245,PX[0])
    # slot boxes
    for yc,t1,t2 in ((245,'第 1 席','勝部決賽勝者'),(424,'第 2 席','敗部決賽勝者')):
      x1=X(PX[0]);x2=X(PX[1]);hh=26*k
      blk(x1,Y(yc)-hh,x2,Y(yc)+hh,LIME);T((x1+x2)/2,Y(yc)-14,t1,24,INK,'mm');T((x1+x2)/2,Y(yc)+18,t2,16,INK,'mm')
    # lower row
    x1_=X(430);bxx(x1_,Y(424)-30,X(536)-x1_,60,'8 支晉級隊伍','來自 Kickoff 資格賽',bar=LIME,fs=16,ss=12)
    box((565,670),424,'敗部第二至五輪',True);box((698,803),424,'敗部決賽',True)
    ln([(X(536),Y(424)),(X(565),Y(424))]);ln([(X(670),Y(424)),(X(698),Y(424))]);arrow([(X(803),Y(424)),(X(832)-3,Y(424))])
    # drops
    for xr,y0_ in ((IX,inv[7]),(SX,semi[3]),(FX,fin[1])):
      cx=(X(xr[0])+X(xr[1]))/2;dsh(cx,Y(y0_)+bh,cx,Y(424)-bh)
    arrow([(X(803)+10,Y(245)),(X(832)-3,Y(245))]) if False else None
    ln([(X(FX[1])+16+0,Y(245)),(X(PX[0])-3,Y(245))])
    None
    kbox(40,1096,1000,100,'前 2 名晉級 ・ 柏林 ・ 德國')
    legend(False)
  # ============ Türkiye
  if MODE=='br_tr':
    stg(40,298,'STAGE 1 · KICKOFF QUALIFIERS')
    step(40,310,306,60,'Qualifier 1',[],tsz=20,ssz=14)
    step(40,378,306,60,'Qualifier 2',[],tsz=20,ssz=14)
    bxx(386,310,306,128,'Bo3 單敗淘汰','每場資格賽各取前 2 名晉級',fill=INK,fs=22,ss=15)
    step(732,310,308,128,'4 支晉級隊',[],tsz=22,ssz=15)
    ln([(346,340),(366,340),(366,374),(386,374)]);ln([(346,408),(366,408),(366,374),(366,374)]);arrow([(366,374),(380,374)])
    arrow([(692,374),(726,374)])
    arrow([(886,438),(886,472)])
    stg(40,472,'STAGE 2 · KICKOFF TÜRKIYE QUALIFIER PLAYOFFS')
    step(40,482,1000,62,'Qualifier Playoffs ・ 8 隊',['4 支晉級隊（來自 Stage 1）＋ 4 支受邀隊（依 2026 年表現）'],tsz=22,ssz=15)
    arrow([(540,544),(540,574)])
    stg(40,574,'STAGE 2A · GSL GROUP STAGE')
    for x,g in ((40,'Group A'),(560,'Group B')):
      bxx(x,584,480,76,g+'　4 隊','GSL 小組賽 ・ Bo3 ・ 各組前 2 名晉級',fill=INK,fs=24,ss=15)
    ln([(280,660),(280,680),(540,680)]);ln([(800,660),(800,680),(540,680)]);arrow([(540,680),(540,710)])
    stg(40,710,'STAGE 2B · DOUBLE ELIMINATION')
    step(290,720,500,62,'雙敗淘汰 ・ 4 隊',['Bo3 ・ 總決賽 Bo5'],tsz=22,ssz=15)
    arrow([(540,782),(540,806)])
    gx_,gy_=de4(265,826,cw=170,st=220,bh=20)
    ln([(gx_,gy_),(gx_,1066)]);arrow([(gx_,1066),(gx_,1082)])
    kbox(40,1086,1000,100,'冠軍晉級 ・ 柏林 ・ 德國')
    legend(False)
  # ============ MENA
  if MODE=='br_mena':
    stg(40,298,'STAGE 01 · QUALIFIERS')
    lanes=[('MIDDLE EAST','中東',326),('NORTH AFRICA','北非',676)]
    mids=[]
    for c,zh,y in lanes:
      chip(40,y,260,34,c,20);d.text((P(312),P(y+18)),zh,font=F(CB,18),fill=WHT,anchor='lm')
      sh_=124;c1=y+46+sh_/2;c2=c1+sh_+12
      step(40,y+46,260,sh_,'Qualifier 1',[],tsz=22,ssz=15);step(40,y+46+sh_+12,260,sh_,'Qualifier 2',[],tsz=22,ssz=15)
      ym=(c1+c2)/2;mids.append(ym)
      ln([(300,c1),(340,c1),(340,c2)]);ln([(300,c2),(340,c2)]);arrow([(340,ym),(374,ym)])
      bxx(380,ym-60,250,120,'Bo5 決勝賽',None,fill=INK,fs=24,ss=14)
      ln([(630,ym),(680,ym)])
    ym=(mids[0]+mids[1])/2
    ln([(680,mids[0]),(680,mids[1])]);arrow([(680,ym),(726,ym)])
    step(732,ym-100,308,200,'MENA Final',['兩區勝者飛往同一地點對戰'],tsz=26,ssz=16)
    arrow([(886,ym+100),(886,ym+150)]);lp(886,ym+172,308,44,'冠軍晉級 Kickoff',20)
    kbox(40,1096,1000,100,'冠軍晉級 ・ 柏林 ・ 德國')
    T(40,1062,'部分非合作夥伴隊伍將獲得較高種子排位',16,MUT,'lm')
    legend(False)

if MODE=='overview':
  # Reusable season-map layout: 3 large REGIONAL cards (left) each followed by 1 small INTERNATIONAL card (right).
  # For other regions, only EVENTS (and TITLE/KICK in the header) need to change.
  panel(20,262,1060,1252,TINT,0.6);corners(20,262,1060,1252)
  import numpy as np
  PH=ROOT+'/assets/photos/'
  _I=[dict(kind='Masters',city='Seoul',zh='首爾',dt='02.20 – 03.03',ph='seo',fo=(50,60)),
      dict(kind='Masters',city='Valencia',zh='瓦倫西亞',dt='06.05 – 06.20',ph='vlc',fo=(50,50)),
      dict(kind='Champions',city='Austin',zh='奧斯汀',dt='09.16 – 10.10',ph='aus',fo=(50,55))]
  _B={'pac':[dict(name='Kickoff',zh='曼谷 · 泰國',dt='01.14 – 02.07',ph='bkk',fo=(50,50),note='8 合作夥伴隊 ＋ 4 公開資格賽隊'),
              dict(name='Cup 1',zh='馬尼拉 · 菲律賓',dt='04.29 – 05.23',ph='mnl',fo=(50,50)),
              dict(name='Cup 2',zh='東京 · 日本',dt='08.05 – 08.29',ph='tyo',fo=(50,50))],
      'emea':[dict(name='Kickoff',zh='柏林 · 德國',dt='01.14 – 02.07',ph='ber',fo=(50,12),note='8 合作夥伴隊 ＋ 4 公開資格賽隊'),
              dict(name='Cup 1',zh='華沙 · 波蘭',dt='04.29 – 05.23',ph='war',fo=(50,40)),
              dict(name='Cup 2',zh='伊斯坦堡 · 土耳其',dt='08.05 – 08.29',ph='ist',fo=(50,50))],
      'amer':[dict(name='Kickoff',zh='聖保羅 · 巴西',dt='01.14 – 02.07',ph='sao',fo=(40,50),note='8 合作夥伴隊 ＋ 4 公開資格賽隊'),
              dict(name='Cup 1',zh='墨西哥城 · 墨西哥',dt='04.29 – 05.23',ph='mex',fo=(50,40)),
              dict(name='Cup 2',zh='里約熱內盧 · 巴西',dt='08.05 – 08.29',ph='rio',fo=(50,50))]}[REG]
  EVENTS=[dict(big=b,intl=i_) for b,i_ in zip(_B,_I)]
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
  panel(20,262,1060,1252,TINT,0.6);corners(20,262,1060,1252)
  LD,T=PT()
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
    if rg:_cw=72 if len(rg)<4 else 100;chip(x+tw-22-_cw,y+th+pl/2-15,_cw,30,rg,18,bg=INK,fg=LIME)
  KC={'pac':'曼谷','emea':'柏林','amer':'聖保羅'}[REG]
  d.text((P(40),P(1234)),'Kickoff '+KC+'　8 隊全數保證參賽',font=F(CB,22),fill=LIME,anchor='lm')

d.line([P(40),P(1278),P(1040),P(1278)],fill=WHT,width=max(1,S))
lg=Lg(ROOT+'/assets/sorai_logo_on_dark.png',P(34));lg=Image.merge('RGBA',(*[Image.new('L',lg.size,255)]*3,lg.getchannel('A')));im.paste(lg,(P(40),P(1296)),lg)
d.text((P(1040),P(1328)),'VCT '+RN+' 2027',font=FMN(14),fill=WHT,anchor='rs')
_a,_b=F(CB,13),F(CL,13);_t='Riot  Games';_x=P(1040)-round(_b.getlength(_t))
d.text((_x,P(1304)),_t,font=_b,fill=WHT,anchor='ls');d.text((_x,P(1304)),'來源：',font=_a,fill=WHT,anchor='rs')
im.save(OUT)
