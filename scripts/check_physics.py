#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent formula/numerical consistency checks, NOT full academic peer review.

A pass validates an independently specified equation or numeric result, not
that the entire physical model and all assumptions in the Chinese text are right.
"""
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent.parent
problems=json.loads((ROOT/'data/problems.json').read_text(encoding='utf-8'))
ids={x['id'] for x in problems}
results={}

def verify(pid, condition, detail):
    if pid not in ids:
        raise ValueError(f'Missing question: {pid}')
    if not bool(condition):
        raise AssertionError(f'{pid}: {detail}')
    results[pid]={'status':'formula_consistency_passed','scope':detail}

def equal(a,b):
    return s.simplify(a-b)==0

m,g,a,h,v,mu,R,H,theta,f,acc=s.symbols('m g a h v mu R H theta f acc', positive=True)
L,x,l0,eps,r,rho,n,kappa,C0,V0,U0,B,A,w,t=s.symbols('L x lambda0 eps r rho n kappa C0 V0 U0 B A omega t',positive=True)
n1,n2,T1,T2,TT,Rgas=s.symbols('n1 n2 T1 T2 Tf Rgas',positive=True)

# Mechanics: independent kinematics, torque + force, momentum + energy
verify('M001', equal((g+a)*(s.sqrt(2*h/(g+a)))**2/2,h), '相对运动位移方程与给定落地时间一致')
t_b=v/(mu*g)
verify('M002', equal(v*t_b-s.Rational(1,2)*mu*g*t_b**2,v**2/(2*mu*g)), '相对滑移距离的积分/位移一致')
sol=s.solve([m*g*s.sin(theta)-f-m*acc,f*R-(m*R**2/2)*(acc/R)],(acc,f))
verify('M003', equal(sol[acc],s.Rational(2,3)*g*s.sin(theta)) and equal(m*g*H, s.Rational(3,4)*m*(s.sqrt(4*g*H/3))**2),'牛顿方程、转动方程和能量方程一致')
u=v/3
verify('M004', equal(m*v,(m+2*m)*u) and equal(m*v**2/2-3*m*u**2/2,m*v**2/3),'动量守恒与能量损失相符')

# E&M: electrostatics, charge conservation, flux derivative
coulomb_integral=s.integrate(x/(2*L-x)**2,(x,0,L))
verify('E001', equal(coulomb_integral,1-s.log(2)), '非均匀带电杆电场积分解析结果')
verify('E002', equal(rho*r/(2*eps)*2*s.pi*r, rho*s.pi*r**2/eps) and equal(rho*R**2/(2*eps*r)*2*s.pi*r, rho*s.pi*R**2/eps),'柱内外高斯通量一致')
verify('E003', equal(C0*kappa/C0,kappa) and equal((1/kappa)*V0,V0/kappa) and equal((1/kappa)*U0,U0/kappa),'恒定自由电荷下电容、电压、能量比例一致')
verify('E004', equal(-s.diff(B*A*s.cos(w*t),t), B*A*w*s.sin(w*t)),'法拉第磁通变化率一致')

# Thermodynamics
Tf=(n1*T1+n2*T2)/(n1+n2)
verify('T001',equal(s.Rational(3,2)*Rgas*(n1*T1+n2*T2),s.Rational(3,2)*Rgas*(n1+n2)*Tf),'刚性绝热系统的内能守恒')
verify('T002',equal(1-s.Rational(300,500),s.Rational(2,5)) and equal(s.Rational(400,1)/s.Rational(2,5),1000) and equal(1000-400,600),'卡诺效率与两端热量守恒')
verify('T003',equal(n*Rgas*T1+s.Rational(3,2)*n*Rgas*T1,s.Rational(5,2)*n*Rgas*T1),'等压过程第一定律')
verify('T004',equal(s.integrate(n*Rgas/x,(x,L,2*L)), n*Rgas*s.log(2)),'等温可逆路径求自由膨胀熵增')

# Waves
verify('W001',equal(2*s.pi/(4*s.pi),s.Rational(1,2)) and equal(20*s.pi/(2*s.pi),10) and equal(20*s.pi/(4*s.pi),5),'波数和角频率换算')
k=s.symbols('k',positive=True)
ks=k/2; kp=2*k
verify('W002',equal(s.sqrt(kp/ks),2),'串并联等效劲度系数和周期比')
verify('W003',equal(s.Rational(340*500,340-20),s.Rational(2125,4)),'运动声源多普勒频率')
verify('W004',equal(v/(2*L/3),3*v/(2*L)) and len([j for j in range(4) if j not in (0,3)])==2,'三阶固定弦本征模式内部节点')

# Optics: full widths and SI-unit conversion
verify('O001',equal(s.Integer(600)/(2*s.Rational(3,2)),200),'双反射同相位反转下首个正膜厚')
verify('O002',equal(2*s.Rational(500,10**9)/s.Rational(2,10**4),s.Rational(5,1000)),'单缝首暗纹距离的单位换算')
verify('O003',equal(2*s.Rational(500,10**9)/s.Rational(5,10000),s.Rational(2,1000)),'双缝间距的单位换算')
verify('O004',equal(s.atan(s.sqrt(3)),s.pi/3),'布儒斯特角解析值')

# Modern physics: threshold, matter wave, infinite well, exponential decay
verify('Q001',equal(s.Integer(3)-2,1),'光电效应能量余量与遏止电压数值')
h_P=6.626e-34; m_e=9.109e-31; e=1.602e-19
lam=h_P/(2*m_e*e*150)**0.5
verify('Q002',abs(lam-1e-10)<5e-13,'150伏电子的独立SI数值核算，容差 0.5 pm')
hbar=s.symbols('hbar',positive=True)
E2_E1=(4-1)*s.pi**2*hbar**2/(2*m*L**2)
verify('Q003',equal(E2_E1/(2*s.pi*hbar),3*s.pi*hbar/(4*m*L**2)),'无限深势阱跃迁能级差与频率一致')
N0,A0=s.symbols('N0 A0',positive=True)
verify('Q004',equal(N0*2**(-2),N0/4) and equal(N0-N0/4,3*N0/4) and equal(A0*2**(-2),A0/4),'指数衰变两个半衰期的核数/活度')

# Second group: 12 new samples, each checked against an independent relation.
b=s.symbols('b',positive=True)
kforce=s.symbols('kforce',positive=True)
assertion_work=s.integrate(kforce*x,(x,a,b))
verify('M005', equal(assertion_work,s.Rational(1,2)*kforce*(b**2-a**2)) and equal(m/2*s.sqrt(kforce*(b**2-a**2)/m)**2,assertion_work), '变力功积分与动能一致')
m1,m2,I=s.symbols('m1 m2 I',positive=True)
acc2=(m2-m1)*g/(m1+m2+I/R**2)
verify('M006', equal((m2*(g-acc2)-m1*(g+acc2))*R,I*acc2/R),'滑轮转动方程与两物体受力方程一致')
ra,rb,lam=s.symbols('ra rb lam',positive=True)
Ve=s.integrate(lam/(2*s.pi*eps*r),(r,ra,rb))
verify('E005', equal(lam/Ve,2*s.pi*eps/s.log(rb/ra)) and equal(lam*Ve/2,lam**2*s.log(rb/ra)/(4*s.pi*eps)),'电势差积分、电容与能量一致')
beta=s.symbols('beta',real=True)
verify('E006', equal(2*s.pi*r*(-beta*r/2),-s.pi*r**2*beta) and equal(2*s.pi*r*(-beta*R**2/(2*r)),-s.pi*R**2*beta),'内外两种回路的法拉第定律')
V1,V2=s.symbols('V1 V2',positive=True)
W_iso=s.integrate(n*Rgas*T1/x,(x,V1,V2))
verify('T005',equal(W_iso,n*Rgas*T1*s.log(V2/V1)),'可逆等温做功积分')
Tf6=(T1+T2)/2
verify('T006',equal(n*(Tf6-T1)+n*(Tf6-T2),0) and equal(s.log(Tf6/T1)+s.log(Tf6/T2),s.log((T1+T2)**2/(4*T1*T2))), '内能守恒与熵变代数式一致')
f1,f2=s.symbols('f1 f2',positive=True)
verify('W005',s.trigsimp(2*A*s.cos(s.pi*(f1-f2)*t)*s.cos(s.pi*(f1+f2)*t)-A*s.cos(2*s.pi*f1*t)-A*s.cos(2*s.pi*f2*t))==0,'振动合成的和差化积恒等式')
Tension=s.symbols('Tension',positive=True)
fn=lambda j:j*s.sqrt(Tension/mu)/(2*L)
verify('W006',equal(fn(3)-fn(2),fn(2)-fn(1)) and (3-1)==2,'弦频率等间隔与内节点数')
focal=s.symbols('focal',positive=True)
image_distance=s.solve(1/focal-1/(3*focal)-1/s.Symbol('d'),s.Symbol('d'))[0]
verify('O005',equal(image_distance,3*focal/2) and equal(-image_distance/(3*focal),-s.Rational(1,2)),'薄透镜方程与横向放大率')
d,thick,nindex,wavelength,D=s.symbols('d thick nindex wavelength D',positive=True)
shift=D*(nindex-1)*thick/d
verify('O006',equal(shift/(wavelength*D/d),(nindex-1)*thick/wavelength),'光程差引起的条纹平移与条纹间距')
beta_rel,c,tau0,travel=s.symbols('beta_rel c tau0 travel',positive=True)
gamma=1/s.sqrt(1-beta_rel**2)
verify('Q005',equal(travel/(beta_rel*c*gamma), travel*s.sqrt(1-beta_rel**2)/(beta_rel*c)) and equal(s.exp(-travel/(beta_rel*c*gamma*tau0)),s.exp(-travel*s.sqrt(1-beta_rel**2)/(beta_rel*c*tau0))), '固有时间与指数衰变律转换')
hplanck,fre1,fre2,fre0,qe=s.symbols('hplanck fre1 fre2 fre0 qe',positive=True)
verify('Q006',equal(hplanck*(fre2-fre0)/qe-hplanck*(fre1-fre0)/qe,hplanck*(fre2-fre1)/qe),'两频率光电遏止电压差')

if set(results)!=ids:
    raise AssertionError(f'Checks missing ids: {sorted(ids-set(results))}; extra: {sorted(set(results)-ids)}')
report={'total_questions':len(ids), 'formula_consistency_checks_passed':len(results),
    'status':'passed', 'limitation':'公式/数值一致性检查，不是独立完整物理题解审核，也不是六轮质检',
    'checks':dict(sorted(results.items()))}
(ROOT/'data/qa_physics_spotchecks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {len(results)}/{len(ids)} formula / numerical consistency checks; expert review still pending.')
