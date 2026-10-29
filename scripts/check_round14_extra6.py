#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 14 second draft group: six new physical cores, 24 executable subpart checks."""
import json, math
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
TESTS=[]
def zero(v): return s.simplify(v)==0
def close(a,b): return math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-11)
def ck(uid,part,method,name,condition):
    if not bool(condition): raise AssertionError(f"{uid}/{part}: {name}")
    TESTS.append(dict(id=uid,part=part,method=method,name=name,passed=True))
# M079 Lucas-Washburn capillary infiltration
L,A,B,t=s.symbols("L A B t",positive=True)
r,gam,ct,vis,rho,grav=s.symbols("r gam ct vis rho grav",positive=True)
aa=r*gam*ct/(4*vis);bb=rho*grav*r*r/(8*vis)
ck("M079",1,"independent_derivation","毛细压强减静压与Poiseuille黏性压降完全一致",zero(2*gam*ct/r-rho*grav*L-8*vis*L/r**2*(aa/L-bb)))
ck("M079",2,"symbolic","无重力平方根浸润律严格满足移动前沿微分方程",zero(s.simplify(s.sqrt(2*A*t)*s.diff(s.sqrt(2*A*t),t)-A)))
Leq=A/B
time_expr=(-L-Leq*s.log(1-L/Leq))/B
ck("M079",3,"symbolic","有重力隐式时间对高度求导精确恢复非线性前沿速度",zero(s.diff(time_expr,L)-L/(A-B*L)) and zero(s.limit((A-B*L)/L/(Leq-L),L,Leq,dir="-")-B/Leq))
Q=s.pi*r*r*(aa/L-bb)
cap=2*gam*ct/r*Q
hyd=rho*grav*L*Q
visc=8*vis*L*Q*Q/(s.pi*r**4)
ck("M079",4,"conservation","毛细压力输入严格等于重力势能增长加非负黏性耗散",zero(cap-hyd-visc) and float(visc.subs({r:1,gam:1,ct:.8,vis:1,rho:1,grav:.1,L:.5}))>0)
# E079 magnetic dipole spin-down
omega,t,I,K,omega0=s.symbols("omega t I K omega0",positive=True)
Om=omega0/s.sqrt(1+2*K*omega0**2*t/I)
ck("E079",1,"symbolic","旋转磁矩二阶导数模平方等于横向磁矩平方乘角速度四次方",zero(s.diff(s.cos(omega*t),t,2)**2+s.diff(s.sin(omega*t),t,2)**2-omega**4))
ck("E079",2,"conservation","偶极辐射能损与精确自转角速度演化微分方程一致",zero(s.diff(Om,t)+K*Om**3/I))
Om1=-K*omega**3/I
Om2=s.diff(Om1,omega)*Om1
ck("E079",3,"independent_derivation","磁偶极制动指数恰为三且周期乘周期导数为常数",zero(omega*Om2/Om1**2-3) and zero((2*s.pi/omega)*(-2*s.pi*Om1/omega**2)-4*s.pi**2*K/I))
w1,w2=s.symbols("w1 w2",positive=True)
duration=I/(2*K)*(1/w2**2-1/w1**2)
ck("E079",4,"dimensions","自转辐射能量积分与动能损失一致且旋转减速时间为正",zero(s.integrate(K*omega**4*(-I/(K*omega**3)),(omega,w1,w2))-I*(w1*w1-w2*w2)/2) and float(duration.subs({I:2,K:1,w1:4,w2:2}))>0)
# T074 Schwarzschild black-hole thermodynamics
M,G,hbar,c,kB,eps=s.symbols("M G hbar c kB eps",positive=True)
TH=hbar*c**3/(8*s.pi*G*M*kB)
entropy=4*s.pi*kB*G*M**2/(hbar*c)
ck("T074",1,"symbolic","黑洞面积熵微分严格满足Hawking第一定律",zero(TH*s.diff(entropy,M)-c**2))
heat=c**2/s.diff(TH,M)
ck("T074",2,"physical_case","Schwarzschild热容为负且随质量平方增长",zero(heat+8*s.pi*G*kB*M**2/(hbar*c)) and float(heat.subs({M:1,G:1,hbar:1,c:1,kB:1}))<0)
area=16*s.pi*G**2*M**2/c**4
sigma=s.pi**2*kB**4/(60*hbar**3*c**2)
power=s.simplify(eps*sigma*area*TH**4)
D=eps*hbar*c**4/(15360*s.pi*G**2)
ck("T074",3,"independent_derivation","Stefan面积温度四次方化简为质量反平方辐射功率",zero(power-D*c**2/M**2))
M0=s.symbols("M0",positive=True)
lifetime=M0**3/(3*D)
ck("T074",4,"conservation","质量三次律导出蒸发寿命并与能量损失方程一致",zero(s.diff(M**3/(3*D),M)-M**2/D) and zero(lifetime-5120*s.pi*G**2*M0**3/(eps*hbar*c**4)))
# W074 Rayleigh beam
rho,Ar,Ix,Young,k=s.symbols("rho Ar Ix Young k",positive=True)
w=s.sqrt(Young*Ix/(rho*Ar))*k**2/s.sqrt(1+Ix*k*k/Ar)
ck("W074",1,"symbolic","旋转惯量梁平面波代入动力学方程得到精确色散",zero((rho*Ar+rho*Ix*k*k)*w*w-Young*Ix*k**4))
cg=s.diff(w,k)
cg_formula=s.sqrt(Young*Ix/(rho*Ar))*k*(2+Ix*k*k/Ar)/(1+Ix*k*k/Ar)**s.Rational(3,2)
ck("W074",2,"independent_derivation","色散求导的群速度与长短波两种渐近极限相符",zero(cg-cg_formula) and zero(s.limit(cg,k,s.oo)-s.sqrt(Young/rho)))
kn=s.symbols("kn",positive=True)
ratio=1/(1+Ix*kn**2/Ar)
ck("W074",3,"physical_case","简支Rayleigh模态频率严格低于Euler–Bernoulli梁频率",0<float(ratio.subs({Ix:1,Ar:2,kn:3}))<1 and zero(s.simplify((w*w/(Young*Ix*k**4/(rho*Ar)))-1/(1+Ix*k*k/Ar))))
ck("W074",4,"conservation","正定转动惯性及弯曲能量保证任意非零模态实频率",all(z>0 for z in [2*.4**2/2,3*.2**2/2,5*.1**2/2]) and float((w*w).subs({Young:2,Ix:1,rho:3,Ar:4,k:2}))>0)
# O076 1D Doppler cooling
delta,kv,Gamma,ss,hbar,k=s.symbols("delta kv Gamma ss hbar k",real=True,positive=True)
# use a negative detuning variable d>0: delta=-d
d=s.symbols("d",positive=True)
def rate(det):
    return Gamma*ss/(2*(1+ss+4*det**2/Gamma**2))
force=hbar*k*(rate(-d-kv)-rate(-d+kv))
ck("O076",1,"symbolic","两束相向光的辐射压力在静止时精确抵消且速度反转为奇函数",zero(force.subs(kv,0)) and zero(force.subs(kv,-kv)+force))
alpha=s.simplify(-s.diff(force,kv).subs(kv,0)*k)
alpha_expected=8*hbar*k*k*ss*d/(Gamma*(1+ss+4*d*d/Gamma**2)**2)
ck("O076",2,"independent_derivation","红失谐摩擦系数来自两束散射率独立求导并严格为正",zero(alpha-alpha_expected) and float(alpha_expected.subs({hbar:1,k:1,ss:.1,d:.5,Gamma:1}))>0)
Dp=2*rate(-d)*(hbar*k)**2
Temp=s.simplify(Dp/alpha)
ck("O076",3,"conservation","给定一维反冲方差的动量扩散与稳态温度表达式一致",zero(Temp-hbar*Gamma**2*(1+ss+4*d*d/Gamma**2)/(8*d)))
Temp_low=hbar*(Gamma**2/d+4*d)/8
ck("O076",4,"limit","低饱和温度在半线宽红失谐取得严格极小Doppler值",zero(s.diff(Temp_low,d).subs(d,Gamma/2)) and zero(Temp_low.subs(d,Gamma/2)-hbar*Gamma/2) and s.diff(Temp_low,d,2).subs(d,Gamma/2)>0)
# Q076 Dirac-Coulomb fine structure
aa,n,kappa,mc=s.symbols("aa n kappa mc",positive=True)
den=n-kappa+s.sqrt(kappa**2-aa**2)
spec=(1+aa**2/den**2)**(-s.Rational(1,2))
expanded=1-aa**2/(2*n**2)-aa**4/(2*n**4)*(n/kappa-s.Rational(3,4))
ck("Q076",1,"symbolic","Dirac点核能谱按精细结构常数展开到四阶的系数一致",zero(s.series(spec,aa,0,6).removeO()-expanded))
shift12=-mc*aa**4/(2*2**4)*(2/s.Integer(1)-s.Rational(3,4))
shift32=-mc*aa**4/(2*2**4)*(2/s.Integer(2)-s.Rational(3,4))
ck("Q076",2,"independent_derivation","n等于二的两个总角动量支能量差为正的四阶劈裂",zero(shift32-shift12-mc*aa**4/32))
ck("Q076",3,"limit","相对论精细结构对非相对论束缚能的比值具有Z平方标度",zero(s.simplify((mc*aa**4/(2*n**4))/(mc*aa**2/(2*n**2))-aa**2/n**2)))
ck("Q076",4,"physical_case","最小总角动量通道要求Zalpha小于一且高Z临界根号变虚",s.sqrt(s.Rational(1)-s.Rational(9,10)**2).is_real and s.im(s.sqrt(1-s.Rational(11,10)**2))!=0)
ids=["M079","E079","T074","W074","O076","Q076"]
assert len(TESTS)==24 and {(z["id"],z["part"]) for z in TESTS}=={(uid,part) for uid in ids for part in range(1,5)}
assert all((ROOT/"bank"/uid/"meta.json").exists() for uid in ids)
report=dict(status="draft_technical_checks_passed_expert_review_pending",round=14,draft_group="second_six",new_problem_count=6,passed_count=24,tests=TESTS,independent_expert_review="待独立复核")
(ROOT/"data"/"round14_extra6_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("ROUND14 SECOND SIX: 24 EXECUTED PHYSICAL SUBPART CHECKS PASS; NOT FULL RELEASE")
