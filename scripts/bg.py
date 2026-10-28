# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# usage: python3 bg.py <pac|eu|euam> <S 1|2> <out.png>   (procedural layered background)
import numpy as np,sys
from PIL import Image,ImageDraw,ImageFilter,ImageFont
S=int(sys.argv[2]);W,H=1080*S,1350*S;rng=np.random.default_rng(7)
yy,xx=np.mgrid[0:H,0:W].astype(float)/S
def ramp(v,st):
  out=np.zeros(v.shape+(3,))
  for (t0,c0),(t1,c1) in zip(st,st[1:]):
    m=(v>=t0)&(v<=t1);u=((v-t0)/(t1-t0))[...,None];out[m]=(np.array(c0)*(1-u)+np.array(c1)*u)[m]
  out[v>st[-1][0]]=st[-1][1];return out
def blob(cx,cy,rx,ry,a=1,rot=0):
  c,s=np.cos(rot),np.sin(rot);dx,dy=xx-cx,yy-cy
  u=(dx*c+dy*s)/rx;w=(-dx*s+dy*c)/ry;return a*np.exp(-(u*u+w*w))
def grain(a,amt):
  n=rng.normal(0,amt,(H,W,1));return np.clip(a+n,0,255)
def blurarr(a,r):return np.asarray(Image.fromarray(np.clip(a,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(r*S)),dtype=float)
AMP=sys.argv[1]=='euam';PAC=sys.argv[1]=='pac'
if sys.argv[1] in('eu','euam','pac'):
  heat=(blob(1060,40,330,260,1.0,0.5)+blob(860,-40,200,150,0.6)+blob(-40,1240,380,300,1.05,-0.4)+blob(160,1380,260,180,0.5)
        +blob(-60,420,170,330,0.85,0.2)+blob(1140,820,190,300,0.8,-0.3)+blob(1000,1330,260,140,0.7)+blob(920,230,140,90,0.5,0.9)+blob(80,760,120,200,0.45)+blob(420,1350,200,90,0.55,0.3)+blob(1080,560,90,160,0.4)+blob(250,1100,150,110,0.5,1.1))
  # organic wobble
  wob=blurarr(rng.normal(128,60,(H//(8*S)+1,W//(8*S)+1)).repeat(8*S,0).repeat(8*S,1)[:H,:W],40)
  heat=heat*(0.85+0.3*(wob/255))
  st=[(0,(58,28,114)),(0.24,(58,28,114)),(0.33,(36,20,46)),(0.43,(84,25,201)),(0.58,(147,124,205)),(0.7,(221,206,235)),(0.82,(201,227,61)),(1.0,(217,255,36))]
  if AMP: st=[(0,(58,22,8)),(0.24,(58,22,8)),(0.33,(26,12,6)),(0.43,(173,62,16)),(0.58,(248,138,12)),(0.7,(255,178,122)),(0.82,(255,110,20)),(1.0,(255,88,13))]
  if PAC: st=[(0,(0,100,178)),(0.24,(0,100,178)),(0.33,(6,24,40)),(0.43,(0,130,232)),(0.58,(0,192,226)),(0.7,(165,242,240)),(0.82,(150,238,110)),(1.0,(198,244,50))]
  img=ramp(np.clip(heat,0,1.2),st)
  # diagonal bands (avatar)
  t=(xx*0.6-yy*0.8)
  band=np.exp(-((t-(330))/70)**2)*0.95+np.exp(-((t-(520))/45)**2)*0.7
  m=np.clip(1-yy/520,0,1)
  bandc=np.array([84,25,201]);lime=np.array([212,232,58])
  if AMP: bandc=np.array([173,62,16]);lime=np.array([255,88,13])
  if PAC: bandc=np.array([0,130,232]);lime=np.array([198,244,50])
  img=img*(1-band[...,None]*0.7*m[...,None])+bandc*(band[...,None]*0.7*m[...,None])
  lb=np.exp(-((t-(430))/26)**2)*m*0.8;img=img*(1-lb[...,None])+lime*lb[...,None]
  img=blurarr(img,16)
  # dark top
  top=np.clip(1-yy/300,0,1)[...,None]**1.5*0.35;img=img*(1-top)+(np.array([24,12,6]) if AMP else (np.array([6,18,30]) if PAC else np.array([30,20,36])))*top
  # chromatic shift
  sh=3*S;img[:,sh:,0]=img[:,:-sh,0].copy();img[:,:-sh,2]=img[:,sh:,2].copy()
  img=img*(1-0.06*((np.arange(H)//(2*S))%2==0)[:,None,None])
  img=grain(img,9)
else:
  sys.exit('bg.py: unknown background %r (use pac, eu or euam)'%sys.argv[1])
Image.fromarray(np.clip(img,0,255).astype('uint8')).save(sys.argv[3])
