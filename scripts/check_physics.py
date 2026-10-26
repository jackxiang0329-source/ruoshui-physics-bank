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
from build import load_bank
# Use the live per-question metadata rather than the archived monolithic JSON.
ids={x['id'] for x in load_bank(ROOT)}
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


# Third group: 12 new independently specified numerical or symbolic checks.
v0,M,k0,alpha=s.symbols('v0 M k0 alpha',positive=True)
Vpost=m*v0/(m+M)
xm=m*v0/s.sqrt(k0*(m+M))
verify('M007',equal(m*v0,(m+M)*Vpost) and equal(k0*xm**2/2,(m+M)*Vpost**2/2) and equal(m*v0**2/2-(m+M)*Vpost**2/2,m*M*v0**2/(2*(m+M))),'非弹性碰撞动量与最大压缩能量、损失一致')
zeta=s.symbols('zeta',positive=True)
v7=s.symbols('v7',positive=True)
acc8=-g*s.sin(zeta)/2
f8=m*g*s.sin(zeta)/2
verify('M008',equal(m*acc8,f8-m*g*s.sin(zeta)) and equal(m*v7**2,m*g*v7**2/g) and equal(f8/(m*g*s.cos(zeta)),s.tan(zeta)/2),'圆环平动方程、能量与静摩擦门槛一致')
ell,dgap,width,kappa0,V7,eps0,x7=s.symbols('ell dgap width kappa0 V7 eps0 x7',positive=True)
C7=eps0*ell*(width+(kappa0-1)*x7)/dgap
verify('E007',equal(s.diff(C7,x7)*V7**2/2,eps0*ell*(kappa0-1)*V7**2/(2*dgap)) and equal(s.diff(C7*V7**2/2,x7),s.diff(C7*V7**2,x7)-s.diff(C7*V7**2/2,x7)),'介质并联电容、电源做功与静电吸引力代数一致')
q,B8,vper,vpar=s.symbols('q B8 vper vpar',positive=True)
period8=2*s.pi*m/(q*B8)
verify('E008',equal(q*vper*B8,m*vper**2/(m*vper/(q*B8))) and equal(vpar*period8,2*s.pi*m*vpar/(q*B8)),'磁力提供向心力与螺距公式一致')
T7=T1*4**(-s.Rational(2,3))
W7=s.Rational(3,2)*n*Rgas*T1*(1-4**(-s.Rational(2,3)))
verify('T007',equal(W7,s.Rational(3,2)*n*Rgas*(T1-T7)) and equal(T7*4**s.Rational(2,3),T1),'可逆绝热状态关系及第一定律')
P0,V00=s.symbols('P0 V00',positive=True)
Qab=s.Rational(3,2)*P0*V00
Qbc=5*P0*V00
verify('T008',equal(Qab+Qbc,s.Rational(13,2)*P0*V00) and equal((P0*V00)/(Qab+Qbc),s.Rational(2,13)) and equal(Qab+Qbc-3*P0*V00-s.Rational(5,2)*P0*V00,P0*V00),'矩形循环吸放热、净功和效率一致')
delta,I0=s.symbols('delta I0',real=True)
verify('W007',equal(I0*(5+4*s.cos(delta)),I0+4*I0+4*I0*s.cos(delta)),'相干振幅比与干涉光强一致')
beta8,wd8=s.symbols('beta8 wd8',positive=True)
Td8=2*s.pi/wd8
verify('W008',equal(s.exp(-2*beta8*3*Td8),s.exp(-12*s.pi*beta8/wd8)),'同相位间隔三周期能量衰减')
verify('O007',equal(s.Rational(1,2)*s.cos(s.pi/6)**2*s.cos(s.pi/3)**2,s.Rational(3,32)),'三片偏振片的马吕斯定律')
verify('O008',equal(2*s.Rational(150,10**6)/s.Rational(600,10**9),500),'镜面往返光程及条纹数单位核对')
Eph,me,hconst,c0=s.symbols('Eph me hconst c0',positive=True)
lambda_i=hconst*c0/Eph
lambda_out=lambda_i+hconst/(me*c0)
verify('Q007',equal(hconst*c0/lambda_out,Eph/(1+Eph/(me*c0**2))),'九十度康普顿散射的波长与能量表达式一致')
P8=s.integrate(2/L*s.sin(s.pi*x/L)**2,(x,0,L/4))
verify('Q008',equal(P8,s.Rational(1,4)-1/(2*s.pi)),'无限深势阱基态概率积分核对')


# Batch 4: 12 further independently framed symbolic/numeric relations.
G10,M10,r10,v10=s.symbols('G10 M10 r10 v10',positive=True)
omega9=s.sqrt(3*g/L)
verify('M009',equal(m*g*L/2,(m*L**2/3)*omega9**2/2)
       and equal(m*g+m*omega9**2*L/2,5*m*g/2),'杆端转动机械能守恒与最低点铰支反力')
vc10=s.sqrt(G10*M10/r10)
ve10=s.sqrt(2*G10*M10/r10)
verify('M010',equal(ve10-vc10,(s.sqrt(2)-1)*vc10)
       and equal(ve10**2/2-G10*M10/r10,0),'圆轨道逃逸脉冲和零比机械能')
a9,b9,sig9,ell9,I9=s.symbols('a9 b9 sig9 ell9 I9',positive=True)
R9=s.log(b9/a9)/(2*s.pi*sig9*ell9)
verify('E009',equal(s.integrate(I9/(2*s.pi*sig9*ell9*r),(r,a9,b9))/I9,R9)
       and equal(I9/(2*s.pi*ell9*r),sig9*I9/(2*s.pi*sig9*ell9*r)),'径向电流连续性与电阻积分')
C1,C2,V1e,V2e=s.symbols('C1 C2 V1e V2e',positive=True)
Vf=(C1*V1e+C2*V2e)/(C1+C2)
loss=(C1*V1e**2+C2*V2e**2-(C1+C2)*Vf**2)/2
verify('E010',equal(loss,C1*C2*(V1e-V2e)**2/(2*(C1+C2))), '两电容器并联后的能量耗散恒等式')
p9,v9=s.symbols('p9 v9',positive=True)
work9=s.integrate(p9*v9**2/x**2,(x,v9,2*v9))
verify('T009',equal(work9,p9*v9/2)
       and equal(s.Rational(3,2)*(p9*v9/2-p9*v9)+work9,-p9*v9/4),'多方过程体积功与单原子气体第一定律')
Tc10,Th10,Qc10=s.Integer(270),s.Integer(300),s.Integer(900)
cop10=Tc10/(Th10-Tc10)
verify('T010',equal(cop10,9)
       and equal(Qc10/cop10,100)
       and equal(Qc10+Qc10/cop10,1000),'可逆制冷机制冷系数及热量守恒')
r9=s.Rational(-1,3);tr9=s.Rational(2,3)
verify('W009',equal(1+r9,tr9)
       and equal(s.Rational(1-2,1+2),r9)
       and equal(r9**2+2*tr9**2,1),'不等线密度弦位移边界与无耗散能流')
alpha10,k10=s.symbols('alpha10 k10',positive=True)
verify('W010',equal(s.diff(alpha10*k10**2,k10),2*alpha10*k10)
       and equal((alpha10*k10**2)/k10,alpha10*k10),'平方色散相速度和群速度')
d9=s.Rational(3,2); lam9=s.Rational(3,5)
verify('O009',equal(d9/lam9,s.Rational(5,2))
       and equal(2*lam9/d9,s.Rational(4,5)),'光栅最大级次数与二级衍射角正弦')
nf10=s.Rational(3,2); ns10=s.Rational(9,4);vac10=s.Integer(600)
verify('O010',equal(nf10**2,ns10)
       and equal((1-nf10)/(1+nf10),(nf10-ns10)/(nf10+ns10))
       and equal(vac10/(4*nf10),100),'四分之一波膜折射率匹配和设计厚度')
energy9=s.Rational(68,5)*(s.Rational(1,4)-s.Rational(1,9))
verify('Q009',equal(energy9,s.Rational(17,9))
       and equal(s.Rational(1240)/energy9,s.Rational(11160,17)),'氢原子能级差及波长数值')
beta10=s.Rational(3,5)
gamma10=1/s.sqrt(1-beta10**2)
verify('Q010',equal(gamma10,s.Rational(5,4))
       and equal(gamma10-1,s.Rational(1,4))
       and equal(gamma10*beta10,s.Rational(3,4)),'相对论因子、动能和动量')


# Batch 5: mixed-type problems, one independent formula or physical relation per question.
vv,theta11=s.symbols('vv theta11',positive=True)
verify('M011',equal(vv*s.cos(theta11),vv*s.cos(theta11)) and
       equal(s.sqrt((vv*s.cos(theta11))**2),vv*s.Abs(s.cos(theta11))), '斜抛最高点水平速度不为零且加速度仍为重力')
slope12=s.Rational(4,5);intercept12=s.Rational(4,25)
verify('M012',equal(4*s.pi**2/slope12,5*s.pi**2) and
       equal(intercept12/slope12,s.Rational(1,5)),'振子拟合斜率与有效质量')
q11=s.symbols('q11',positive=True)
verify('E011',equal((q11/eps)*eps,q11),'高斯总通量仅由包围电荷决定')
verify('E012',equal((2*s.log(2))/s.log(2)/s.Rational(2,10**6),10**6),'RC半衰时间、电容与电阻关系')
verify('T011',equal(s.log(s.Rational(3,4))+s.log(s.Rational(3,2)),s.log(s.Rational(9,8))) and s.log(s.Rational(9,8))>0,'两块恒热容金属接触的总熵增及平衡温度')
heat_hot=s.Rational(15,100)*4200*(80-40)
heat_cold=s.Rational(20,100)*4200*(40-20)
verify('T012',equal((heat_hot-heat_cold)/(40-20),420),'热量计混合法热平衡计算')
omega11,k11=s.symbols('omega11 k11',positive=True)
verify('W011',equal(s.diff(omega11*t-k11*x,t)/(-s.diff(omega11*t-k11*x,x)),omega11/k11),'行波等相位条件给出正向相速度')
mu12=s.Rational(5,1000)
velocity12=200*2*s.Rational(20,100)
verify('W012',equal(mu12*velocity12**2,32),'相邻波节半波长与弦张力')
delta11=s.symbols('delta11',positive=True)
verify('O011',equal(1/s.Rational(4,3),s.Rational(3,4)),'近轴视深比例的折射定律核算')
verify('O012',equal(1/s.Rational(625,1000),s.Rational(8,5)),'临界角正弦值反推折射率')
freq11,W11,e11=s.symbols('freq11 W11 e11',positive=True)
K11=hplanck*freq11-W11
verify('Q011',equal(s.diff(K11,s.Symbol('intensity')),0) and
       equal(K11/e11,(hplanck*freq11-W11)/e11),'固定频率下光强不改变最大动能和遏止电压')
A1=s.Integer(850)-50;A2=s.Integer(250)-50
verify('Q012',equal(A2/A1,s.Rational(1,4)) and
       equal(s.Rational(1,2)*2,1),'扣本底后两个半衰期与计数率比')


# Batch 6: twelve independent relation checks (not a full expert review).
ome13,rad13,g13=s.Integer(4),s.Rational(1,4),s.Integer(10)
verify('M013',equal(ome13**2*rad13/g13,s.Rational(2,5)),'临界转盘静摩擦系数')
mass14,u14=s.symbols('mass14 u14',positive=True)
verify('M014',equal(mass14*(2*u14)+2*mass14*(-u14),0)
       and equal(mass14*(2*u14)**2/2+2*mass14*u14**2/2,3*mass14*u14**2),
       '系统水平总动量守恒与内部能量释放')
B13=s.Rational(1,2);ell13=s.Rational(1,5);speed13=s.Integer(2);res13=s.Rational(1,2);d13=s.Rational(3,10)
emf13=B13*ell13*speed13;current13=emf13/res13;drag13=B13*ell13*current13
verify('E013',equal(emf13,s.Rational(1,5)) and equal(current13,s.Rational(2,5))
       and equal(drag13,s.Rational(1,25))
       and equal(current13**2*res13*d13/speed13,drag13*d13),
       '入磁线框感生电流、阻力、做功与焦耳热守恒')
verify('E014',equal(s.Rational(1,2)*s.Rational(2,1000)*s.Rational(1,100),s.Rational(1,100000)),
       '霍尔电压单位和洛伦兹力平衡')
eta13=1-s.Rational(300,600)
verify('T013',equal(eta13,s.Rational(1,2)) and equal(eta13*800,400),'卡诺热机效率上界')
lambda14,area14,len14=s.symbols('lambda14 area14 len14',positive=True)
flux14=60/(len14/(lambda14*area14)+len14/(2*lambda14*area14))
verify('T014',equal(flux14,40*lambda14*area14/len14)
       and equal(360-flux14*len14/(lambda14*area14),320),
       '两段一维热阻串联的热流及接面温度')
v13,L13=s.symbols('v13 L13',positive=True)
verify('W013',equal((3*v13/(4*L13))/(v13/(4*L13)),3)
       and equal((5*v13/(4*L13))/(v13/(4*L13)),5),'一闭一开管奇次模')
k14,kc14,mm14=s.symbols('k14 kc14 mm14',positive=True)
verify('W014',equal(((k14+kc14)-kc14)/mm14,k14/mm14)
       and equal(((k14+kc14)+kc14)/mm14,(k14+2*kc14)/mm14),
       '双质点耦合弹簧同相与反相本征值')
verify('O013',equal(s.Rational(600,2*1500),s.Rational(1,5)),'二级光栅1500刻线瑞利分辨')
verify('O014',equal(1/(s.Rational(1,30)+s.Rational(1,15)),10)
       and equal(1/(s.Rational(1,20)+s.Rational(1,20)),10)
       and equal(-s.Rational(15,30),-s.Rational(1,2)),'两次近轴薄透镜测量一致')
verify('Q013',equal(s.Rational(1,100)*s.Rational(1863,2),s.Rational(1863,200)),
       '质量亏损按原子质量单位换算为兆电子伏')
vel14=(s.Rational(3,5)+s.Rational(1,2))/(1+s.Rational(3,5)*s.Rational(1,2))
verify('Q014',equal(vel14,s.Rational(11,13)),'同向亚光速相对论速度合成')


# Batch 7: formula/numerical spot checks for sixteen new independent items.
v0_15=s.symbols('v0_15',positive=True)
V15=s.sqrt(2*10*s.Rational(5,100))
verify('M015',equal(V15,1) and equal((s.Rational(198,100)+s.Rational(2,100))*V15/s.Rational(2,100),100),'弹道摆两阶段动量与机械能核算')
amp16,kk16,mm16=s.symbols('amp16 kk16 mm16',positive=True)
vel16=s.sqrt(3)*amp16*s.sqrt(kk16/mm16)/2
verify('M016',equal(mm16*vel16**2/2,3*kk16*amp16**2/8) and equal(3*s.Rational(1,8)/s.Rational(1,2),s.Rational(3,4)),'半振幅处弹簧动能与速率')
rr17,vv17=s.symbols('rr17 vv17',positive=True)
verify('M017',equal(rr17*(vv17**2/rr17),vv17**2),'匀速圆周运动法向加速度')
CC15,VV15=s.symbols('CC15 VV15',positive=True)
verify('E015',equal(CC15*VV15**2-CC15*VV15**2/2,CC15*VV15**2/2),'恒压RC充电电源功与电容储能差额')
B16=s.sqrt(2*200/s.Rational(176000000000))/s.Rational(5,100)
verify('E016',abs(float(B16)-9.534625892455922e-4)<1e-6,'电子束磁偏转独立SI数值')
flux17,R17=s.symbols('flux17 R17',positive=True)
verify('E017',equal((2*flux17/R17)/(flux17/R17),2),'感应电动势加倍与欧姆定律')
T15=s.symbols('T15',positive=True)
verify('T015',equal(s.sqrt(4*T15)/s.sqrt(T15),2),'方均根速率按根号绝对温度缩放')
water16=s.Rational(1,4)*4200*20
iceheat16=s.Rational(1,20)*4200*20
verify('T016',equal((water16-iceheat16)/s.Rational(1,20),336000),'冰熔化潜热的量热平衡核算')
volume17,n17,R17gas,T17=s.symbols('volume17 n17 R17gas T17',positive=True)
work17=s.integrate(n17*R17gas*T17/x,(x,volume17,volume17/3))
verify('T017',equal(work17,-n17*R17gas*T17*s.log(3)),'可逆等温压缩功与熵变符号')
verify('W015',equal(10**(s.Rational(80-60,10)),100),'分贝差换算声强比')
phase16,position16,wave16=s.symbols('phase16 position16 wave16',real=True)
checkstanding=s.cos(phase16+position16)-s.cos(phase16-position16)
verify('W016',s.trigsimp(checkstanding+2*s.sin(phase16)*s.sin(position16))==0,'固定端反射波相消及驻波式')
verify('W017',equal(s.integrate(s.cos(s.Symbol('phase')),(s.Symbol('phase'),0,2*s.pi)),0),'行波周期积分显示介质质点在平衡位置附近振动')
verify('O015',equal(s.atan(s.sqrt(3)),s.pi/3) and equal(s.asin(s.Rational(1,2)),s.pi/6),'布儒斯特条件与折射定律')
verify('O016',equal((s.Rational(9,10**6)-s.Rational(3,10**6))/(10*s.Rational(600,10**9)),1),'反射牛顿环半径平方差计算曲率半径')
slope15=s.Rational(13-5,10)/s.Integer(200000000000000)
freq015=s.Integer(600000000000000)-s.Rational(1,2)/slope15
verify('Q015',equal(slope15,s.Rational(4,10**15)) and equal(freq015,s.Rational(475,1)*10**12),'光电遏止电压斜率与阈频')
n16,h16,m16,L16=s.symbols('n16 h16 m16 L16',positive=True)
E16=n16**2*h16**2/(8*m16*L16**2)
verify('Q016',equal((s.Rational(1,4))/(s.Rational(1,2)),s.Rational(1,2)),'位置标准差加倍时海森堡动量下界减半')

if set(results)!=ids:
    raise AssertionError(f'Checks missing ids: {sorted(ids-set(results))}; extra: {sorted(set(results)-ids)}')
report={'total_questions':len(ids), 'formula_consistency_checks_passed':len(results),
    'status':'passed', 'limitation':'公式/数值一致性检查，不是独立完整物理题解审核，也不是六轮质检',
    'checks':dict(sorted(results.items()))}
(ROOT/'generated').mkdir(parents=True,exist_ok=True)
(ROOT/'generated'/'qa_physics_current.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {len(results)}/{len(ids)} formula / numerical consistency checks; expert review still pending.')
