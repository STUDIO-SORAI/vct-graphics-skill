# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import numpy as np
from PIL import Image
def rgb2hls(a):
  a=a/255.;r,g,b=a[...,0],a[...,1],a[...,2];mx=a.max(-1);mn=a.min(-1);l=(mx+mn)/2;dl=mx-mn
  s=np.where(dl==0,0,dl/(1-np.abs(2*l-1)+1e-9))
  h=np.zeros_like(l);m=dl>0
  rc=(mx==r)&m;gc=(mx==g)&m&~rc;bc=m&~rc&~gc
  h[rc]=((g-b)[rc]/dl[rc])%6;h[gc]=(b-r)[gc]/dl[gc]+2;h[bc]=(r-g)[bc]/dl[bc]+4
  return h*60,l,s
def hls2rgb(h,l,s):
  c=(1-np.abs(2*l-1))*s;hp=(h%360)/60;x=c*(1-np.abs(hp%2-1));z=np.zeros_like(c)
  conds=[hp<1,hp<2,hp<3,hp<4,hp<5,hp>=5]
  R=np.select(conds,[c,x,z,z,x,c]);G=np.select(conds,[x,c,c,x,z,z]);B=np.select(conds,[z,z,x,c,c,x])
  m=l-c/2;return np.clip(np.stack([R+m,G+m,B+m],-1)*255,0,255)
def shift(path,deg,sat=1.0):
  a=np.asarray(Image.open(path).convert('RGB')).astype(float)
  h,l,s=rgb2hls(a);return Image.fromarray(hls2rgb(h+deg,l,np.clip(s*sat,0,1)).astype('uint8'))
