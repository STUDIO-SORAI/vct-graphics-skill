# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# VCT 2027 mega-thread covers. usage: python3 cover.py cover1|cover2 S OUT
import sys,os,re,math
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from hue import shift
MODE=sys.argv[1];S=int(sys.argv[2]);OUT=sys.argv[3];W,H=1080*S,1350*S
R=os.environ.get('VCT_ROOT',os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/'
import _assets;_assets.preflight('cover',R.rstrip('/'))
CB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';CR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FD=R+'assets/fonts/ClashDisplay/';CL=FD+'ClashDisplay-Bold.otf'
MONO='/usr/share/fonts/truetype/sand-box/google/JetBrains Mono/JetBrainsMono-VariableFont_wght.ttf'
def F(p,s):return ImageFont.truetype(p,round(s*S),index=3 if p.endswith('ttc') else 0)   # index 3 = Noto Sans CJK TC
def FMN(s_):
  f=ImageFont.truetype(MONO,round(s_*S))
  try:f.set_variation_by_axes([500])
  except Exception:pass
  return f
P=lambda v:round(v*S)
WHT=(255,255,255);GREY=(240,222,220);INK=(22,22,22);LIME=(205,245,40);TINT=(40,0,0)
# background: existing Pacific layered bg (layers + grain + chromatic shift kept), HSL hue-rotated to red
im=shift(R+'assets/bg_pac'+('@2x' if S==2 else '')+'.png',-206);d=ImageDraw.Draw(im)
def panel(x1,y1,x2,y2,c,a):
  global im,d
  ov=Image.new('RGBA',im.size,(0,0,0,0));ImageDraw.Draw(ov).rectangle([P(x1),P(y1),P(x2),P(y2)],fill=c+(int(255*a),));im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB');d=ImageDraw.Draw(im)
def Lg(p,h):
  m=Image.open(p).convert('RGBA');m=m.crop(m.getbbox());return m.resize((round(m.width*h/m.height),round(h)),Image.LANCZOS)
def corners(x1,y1,x2,y2,c=WHT,L=14):
  for X,sx in ((x1,1),(x2,-1)):
    for Y,sy in ((y1,1),(y2,-1)):
      d.line([P(X),P(Y),P(X+sx*L),P(Y)],fill=c,width=max(1,S));d.line([P(X),P(Y),P(X),P(Y+sy*L)],fill=c,width=max(1,S))
def chip(x,y,w,h,t,fs,bg=WHT,fg=INK,font=None):
  d.rectangle([P(x),P(y),P(x+w),P(y+h)],fill=bg);d.text((P(x+w/2),P(y+h/2+1)),t,font=font or F(CL,fs),fill=fg,anchor='mm')
def T(x,y,t,sz,fill,center=False):
  cx=P(x)
  if center:
    tot=0
    for p in re.split(r'(Kickoff|Cup)',t):
      if p:
        L=p in('Kickoff','Cup');tot+=F(CL if L else CB,sz).getlength(p)+(2*round(0.12*sz*S) if L else 0)
    cx=P(x)-round(tot/2)
  for p in re.split(r'(Kickoff|Cup)',t):
    if not p:continue
    f_=F(CL,sz) if p in('Kickoff','Cup') else F(CB,sz)
    g=round(0.12*sz*S) if p in('Kickoff','Cup') else 0
    cx+=g;d.text((cx,P(y)),p,font=f_,fill=fill,anchor='ls');cx+=f_.getlength(p)+g
# ---- header (same HUD as the set)
def header(kick,zone,coord,title=None,tsz=84):
  mk=Lg(R+'assets/vct_white.png',P(64));im.paste(mk,(P(40),P(40)),mk)
  d.text((P(120),P(72)),'VALORANT CHAMPIONS TOUR',font=F(CL,17),fill=WHT,anchor='ls')
  d.text((P(1040),P(84)),kick,font=F(CL,17),fill=WHT,anchor='rs')
  d.line([P(24),P(118),P(1056),P(118)],fill=WHT,width=max(1,S))
  for x in (24,1056):d.line([P(x),P(110),P(x),P(126)],fill=WHT,width=max(1,S))
  d.text((P(1056),P(140)),coord,font=FMN(12),fill=WHT,anchor='rs')
  d.text((P(1056),P(30)),zone,font=FMN(12),fill=WHT,anchor='rs')
  if title:
    x_=P(37)
    for p in re.split(r'(\d+)',title):
      if not p:continue
      f_=F(CL,tsz) if p.isdigit() else F(CB,tsz)
      d.text((x_,P(206)),p,font=f_,fill=WHT,anchor='ls');x_+=f_.getlength(p)
def footer(credit=True):
  d.line([P(40),P(1278),P(1040),P(1278)],fill=WHT,width=max(1,S))
  lg=Lg(R+'assets/sorai_logo_on_dark.png',P(34));lg=Image.merge('RGBA',(*[Image.new('L',lg.size,255)]*3,lg.getchannel('A')));im.paste(lg,(P(40),P(1296)),lg)
  d.text((P(1040),P(1328)),'VCT 2027',font=FMN(14),fill=WHT,anchor='rs')
  if not credit:return
  _a,_b=F(CB,13),F(CL,13);_t='Riot  Games';_x=P(1040)-round(_b.getlength(_t))
  d.text((_x,P(1304)),_t,font=_b,fill=WHT,anchor='ls');d.text((_x,P(1304)),'來源：',font=_a,fill=WHT,anchor='rs')

if MODE=='cover1':
  header('MEGA THREAD','THREAD: VCT 2027  ·  REGIONS: 3','PACIFIC  ·  EMEA  ·  AMERICAS')
  # title, set flush left, huge
  def fit(t,f_,wmax):
    sz=400
    while ImageFont.truetype(f_,round(sz*S),index=3 if f_.endswith('ttc') else 0).getlength(t)>wmax*S:sz-=2
    return sz
  s1=fit('VCT 2027',CL,1000);s2=fit('賽制全解析',CB,1000)
  d.text((P(34),P(560)),'VCT 2027',font=F(CL,s1),fill=WHT,anchor='ls')
  d.text((P(40),P(560+s2*0.98)),'賽制全解析',font=F(CB,s2),fill=WHT,anchor='ls')
  yb=560+s2*0.98
  T(540,yb+58,'往下查看各賽區訊息',28,GREY,True)
  TW=176*S;GP=P(64);LBL=['PACIFIC','EMEA','AMERICAS']
  # unified tile: card (emblem) cropped from the lockup asset + redrawn, fully closed label frame
  def card_of(n):
    m=Image.open(R+'assets/cover/logo_'+n+'.png').convert('RGBA');m=m.crop(m.getbbox());a_=np.asarray(m)[...,3]>128;occ=a_.sum(1)/a_.shape[1]
    ch=next(i for i in range(len(occ)//3,len(occ)) if occ[i]<0.2)   # first row below the card
    return m.crop((0,0,m.width,ch))
  CARDS=[card_of(n) for n in ('pac','emea','amer')]
  CH=round(TW*154/221);LHT=round(TW*84/221)
  lf=ImageFont.truetype(CL,10);fs=60
  while ImageFont.truetype(CL,fs).getlength('AMERICAS')>TW*0.80:fs-=1
  lf=ImageFont.truetype(CL,fs);FR=(250,248,248);lw=max(2,round(TW*1.5/176))
  tiles=[]
  for c_,lb in zip(CARDS,LBL):
    t=Image.new('RGBA',(TW,CH+LHT),(0,0,0,0));td=ImageDraw.Draw(t)
    td.rounded_rectangle([0,CH-14,TW-1,CH+LHT-1],radius=round(TW*0.04),outline=FR,width=lw)
    t.paste((0,0,0,0),(0,0,TW,CH-3*S));cc=c_.resize((TW,CH),Image.LANCZOS);t.alpha_composite(cc,(0,0))
    td.text((TW/2,CH+LHT*0.52),lb,font=lf,fill=FR,anchor='mm')
    tiles.append(t)
  tw=sum(t.width for t in tiles)+2*GP;x=(W-tw)//2;ly=P(1000)
  for t in tiles:
    im.paste(t,(x,ly),t);x+=t.width+GP
  footer(False)
elif MODE=='cover2':
  header('INTERNATIONAL EVENTS','THREAD: VCT 2027  ·  EVENTS: 3','INTERNATIONAL  ·  2027','2027 國際賽',84)
  panel(20,262,1060,1252,TINT,0.35);corners(20,262,1060,1252)
  PH=R+'assets/photos/'
  EV=[dict(kind='Masters',city='Seoul',zh='首爾',dt='02.20 – 03.03',ph='seo',fo=(50,62)),
      dict(kind='Masters',city='Valencia',zh='瓦倫西亞',dt='06.05 – 06.20',ph='vlc',fo=(50,55)),
      dict(kind='Champions',city='Austin',zh='奧斯汀',dt='09.16 – 10.10',ph='aus',fo=(50,58))]
  def photo(x,y,w,h,ph,fo):
    a=Image.open(PH+f'p_{ph}.jpg').convert('RGB');w_,h_=P(w),P(h)
    r=max(w_/a.width,h_/a.height);a=a.resize((round(a.width*r)+1,round(a.height*r)+1),Image.LANCZOS)
    ox=round((a.width-w_)*fo[0]/100);oy=round((a.height-h_)*fo[1]/100);a=a.crop((ox,oy,ox+w_,oy+h_))
    gy=np.linspace(0,1,h_)[:,None];gx=np.linspace(0,1,w_)[None,:]
    al=np.clip(np.maximum(0.82*np.clip(1-gx/0.75,0,1)**1.3,np.clip((gy-0.45)/0.55,0,1)**1.2*0.8)+0.12,0,0.9)
    im.paste(Image.fromarray((np.asarray(a).astype(float)*(1-al[:,:,None])).astype('uint8')),(P(x),P(y)))
  BH,GAP=296,24
  for i,e in enumerate(EV):
    y=286+i*(BH+GAP)
    photo(40,y,1000,BH,e['ph'],e['fo'])
    chip(40,y,150 if e['kind']=='Masters' else 170,32,e['kind'].upper(),16)
    d.text((P(1040-24),P(y+BH-26)),e['dt'],font=F(CL,50),fill=WHT,anchor='rs')
    d.text((P(64),P(y+BH-82)),e['city'],font=F(CL,104),fill=WHT,anchor='ls')
    d.text((P(64),P(y+BH-28)),e['zh'],font=F(CB,30),fill=WHT,anchor='ls')
  d.text((P(40),P(1237)),'PHOTOS  ·  WIKIMEDIA COMMONS  ·  CC BY / CC BY-SA / CC0',font=FMN(11),fill=GREY,anchor='lm')
  footer()
im.save(OUT)
