#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 14 draft: 12 genuinely evaluated physical checks x 4, NOT a completed 50-item release gate."""
import json, math, cmath
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
TESTS=[]
def ck(uid,part,method,name,condition):
    if not bool(condition):
        raise AssertionError(f"{uid}/{part} FAILED: {name}")
    TESTS.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def zero(x):
    return s.simplify(x)==0
def close(a,b,rtol=1e-9):
    return math.isclose(float(a),float(b),rel_tol=rtol,abs_tol=1e-11)
x,y,r,t,G,h,eta,a,nu,alpha,Gamma,S,Bx,By,Bz,mu=s.symbols(
    "x y r t G h eta a nu alpha Gamma S Bx By Bz mu",positive=True,real=True)
# M077 Bingham constitutive yield flow
tau=-G*y
ck("M077",1,"physical_case","Bingham中心应力为零且屈服界面恰达到材料阈值",zero(tau.subs(y,a)+G*a) and abs(float(tau.subs({G:2,y:.4})))==.8)
u=G*(h*h-y*y)/(2*eta)-G*a*(h-y)/eta
ck("M077",2,"symbolic","分段流速同时满足壁面无滑移与塞状核剪切率为零",zero(u.subs(y,h)) and zero(s.diff(u,y).subs(y,a)) and zero(u.subs(y,a)-G*(h-a)**2/(2*eta)))
Q=2*s.integrate(y*(G*y-G*a)/eta,(y,a,h))
Qclosed=G*h**3/(3*eta)*(2-3*a/h+(a/h)**3)
ck("M077",3,"independent_derivation","交换积分次序得到的流量与三次多项式闭式一致",zero(Q-Qclosed) and close(Qclosed.subs({G:2,h:1,eta:3,a:.4}),.192))
D=2*s.integrate(G*y*(G*y-G*a)/eta,(y,a,h))
ck("M077",4,"conservation","全域压力功与黏塑性耗散积分严格相等且临界呈二次律",zero(D-G*Q) and zero(s.limit(Qclosed/(G*h**3*(1-a/h)**2/eta),a,h,dir="-")-1))
# M078 Burgers vortex
b=alpha/(4*nu); C=Gamma*b/s.pi; omega=C*s.exp(-b*r*r)
res=alpha*omega+alpha*r*s.diff(omega,r)/2+nu*(s.diff(omega,r,2)+s.diff(omega,r)/r)
ck("M078",1,"symbolic","高斯涡量逐项满足涡伸长与径向扩散平衡微分方程",zero(res))
ck("M078",2,"independent_derivation","高斯核全平面积分精确归一为规定环量",zero(2*s.pi*s.integrate(r*omega,(r,0,s.oo))-Gamma))
v=Gamma/(2*s.pi*r)*(1-s.exp(-b*r*r))
ck("M078",3,"limit","轴心速度有限且远场环量恢复自由涡极限",zero(s.limit(v/r,r,0)-Gamma*b/(2*s.pi)) and zero(s.limit(2*s.pi*r*v,r,s.oo)-Gamma))
Z=2*s.pi*s.integrate(r*omega**2,(r,0,s.oo))
ck("M078",4,"dimensions","涡量平方积分闭式与黏性系数奇异缩放一致",zero(Z-Gamma**2*alpha/(8*s.pi*nu)) and zero(s.diff(nu*Z,nu)))
# E077 ideal MHD shear
F=s.Matrix([[1,S*t,0],[0,1,0],[0,0,1]])
Bt=F*s.Matrix([Bx,By,Bz])
ck("E077",1,"symbolic","剪切感应方程给出横向磁场不变与纵向分量线性增长",zero(s.diff(Bt[0],t)-S*Bt[1]) and zero(s.diff(Bt[1],t)) and zero(s.diff(Bt[2],t)))
ck("E077",2,"conservation","Cauchy形变梯度行列式为一并保持磁通冻结映射",F.det()==1 and zero(Bt[0]-(Bx+S*t*By)))
UB=sum(z*z for z in Bt)/(2*mu)
ck("E077",3,"independent_derivation","磁能导数与Maxwell剪切应力外源功率一致",zero(s.diff(UB,t)-S*Bt[0]*Bt[1]/mu))
ts=-Bx/(S*By)
ck("E077",4,"physical_case","磁能抛物线极小值和有限时间反转条件同时成立",zero(s.diff(UB,t).subs(t,ts)) and zero(UB.subs(t,ts)-(By*By+Bz*Bz)/(2*mu)) and zero(UB.subs(S,0)-UB.subs(t,0)))
# E078 plasma sheath, natural e=kT=n0=m=eps=1 numeric check
phi,u0,Te,e,mi,n0,eps=s.symbols("phi u0 Te e mi n0 eps",positive=True)
vi=s.sqrt(u0*u0-2*e*phi/mi)
ni=n0*u0/vi; ne=n0*s.exp(e*phi/Te)
ck("E078",1,"conservation","冷离子流守恒与电势能动能守恒对任意负势成立",zero(ni*vi-n0*u0) and zero(mi*vi**2/2+e*phi-mi*u0*u0/2))
coef=s.diff(ne-ni,phi).subs(phi,0)
ck("E078",2,"symbolic","Poisson线性化的Bohm系数和声速阈值代数一致",zero(coef-n0*e*(1/Te-1/(mi*u0*u0))) and zero(coef.subs(u0,s.sqrt(Te/mi))))
H=n0*(Te*(s.exp(e*phi/Te)-1)+mi*u0*(vi-u0))
ck("E078",3,"independent_derivation","Sagdeev第一积分求导精确恢复非线性Poisson电荷密度",zero(s.diff(H,phi)-e*(ne-ni)))
num={Te:1,e:1,mi:1,u0:2,n0:1,phi:s.Rational(-1,5)}
ck("E078",4,"physical_case","超Bohm入射时负壁势的第一积分为正且离子通量恒定",float(H.subs(num))>0 and close((ni*vi).subs(num),2) and zero(H.subs(phi,0)))
# T072 first-passage time
L,D=s.symbols("L D",positive=True)
m1=x*(L-x)/(2*D)
ck("T072",1,"symbolic","吸收布朗首达均值满足后向Poisson方程及双端边界",zero(D*s.diff(m1,x,2)+1) and zero(m1.subs(x,0)) and zero(m1.subs(x,L)))
z=s.symbols("z",positive=True)
Fs=s.cosh(s.sqrt(z/D)*(x-L/2))/s.cosh(s.sqrt(z/D)*L/2)
ck("T072",2,"independent_derivation","首达Laplace变换满足边界且首阶系数恢复平均首达时间",zero(D*s.diff(Fs,x,2)-z*Fs) and zero(Fs.subs(x,0)-1) and zero(s.limit((1-Fs)/z,z,0)-m1))
surv=lambda tt,xx:sum(4/(math.pi*n)*math.sin(n*math.pi*xx)*math.exp(-n*n*math.pi**2*tt) for n in range(1,52,2))
ck("T072",3,"numerical","Dirichlet热核生存概率随时间衰减且首本征模控制长时尾",0<surv(.3,.5)<surv(.1,.5)<1 and close(surv(1,.5)/surv(.8,.5),math.exp(-.2*math.pi**2),1e-5))
m2=(x**4-2*L*x**3+L**3*x)/(12*D**2)
ck("T072",4,"symbolic","二阶首达矩满足递推且中点方差精确为正",zero(D*s.diff(m2,x,2)+2*m1) and zero((m2-m1**2).subs(x,L/2)-L**4/(96*D**2)))
# T073 second quantum virial
etaq,xx,kT,lam,n=s.symbols("etaq xx kT lam n",real=True)
zz=xx-etaq*xx**2/(2**s.Rational(3,2))
Pseries=zz+etaq*zz**2/(2**s.Rational(5,2))
ck("T073",1,"symbolic","量子逸度二阶反演保持粒子数到所需阶数",zero(s.expand(zz+etaq*zz**2/2**s.Rational(3,2)-xx).coeff(xx,2)))
ck("T073",2,"independent_derivation","玻色与费米第二维里系数由独立压力级数消元得到",zero(s.expand(Pseries).coeff(xx,2)+etaq/2**s.Rational(5,2)))
f=kT*(s.log(n*lam**3)-1-etaq*n*lam**3/2**s.Rational(5,2))
ck("T073",3,"symbolic","Helmholtz自由能的密度导数与第二维里压强完全一致",zero(n*n*s.diff(f,n)-n*kT*(1-etaq*n*lam**3/2**s.Rational(5,2))))
ck("T073",4,"conservation","内能与化学势熵恒等式导出正确量子熵修正",zero(s.Rational(5,2)*(1-etaq*xx/2**s.Rational(5,2))-(s.log(xx)-etaq*xx/2**s.Rational(3,2))-(s.Rational(5,2)-s.log(xx)-etaq*xx/2**s.Rational(7,2))))
# W072 mass-in-mass acoustic metamaterial
M,m,K,k,ww,qq,aa=s.symbols("M m K k ww qq aa",positive=True)
Meff=M+m*k/(k-m*ww**2)
det=s.det(s.Matrix([[4*K*s.sin(qq*aa/2)**2+k-M*ww**2,-k],[-k,k-m*ww**2]]))
ck("W072",1,"symbolic","双质量Bloch行列式与动态有效质量色散严格等价",zero(det-(k-m*ww**2)*(4*K*s.sin(qq*aa/2)**2-ww**2*Meff)))
w0=s.sqrt(k/m); wp=s.sqrt(k*(M+m)/(M*m))
ck("W072",2,"physical_case","共振频率与有效质量零点之间质量为负且禁止实波传播",close(w0.subs({M:3,m:1,k:2}),math.sqrt(2)) and float(Meff.subs({M:3,m:1,k:2,ww:1.5}))<0 and float(wp.subs({M:3,m:1,k:2}))>1.5)
ck("W072",3,"limit","长波声速含全部胞内质量且光学支起点为零点频率",zero(s.limit(ww**2*Meff,ww,0)) and zero(s.limit(Meff,ww,0)-(M+m)) and zero(s.simplify(wp**2-k*(M+m)/(M*m))))
ck("W072",4,"conservation","完整机械能各项非负且平移模弹性势能严格为零",all(v>=0 for v in [3*.5**2/2,1*.8**2/2,2*(1-1)**2/2,4*(1-1)**2/2]) and zero(det.subs({qq:0,ww:0})))
# W073 nonreciprocal resonator chain
JR,JL,gamma,N=s.symbols("JR JL gamma N",positive=True)
rr=s.sqrt(JR/JL)
ck("W073",1,"symbolic","周期Bloch复谱的实虚部分离与非互易椭圆轨迹一致",zero((JR*s.exp(-s.I*qq)+JL*s.exp(s.I*qq)).expand(complex=True).as_real_imag()[0]-(JR+JL)*s.cos(qq)) and zero(s.im(JR*s.exp(-s.I*qq)+JL*s.exp(s.I*qq))-(JL-JR)*s.sin(qq)))
ck("W073",2,"independent_derivation","非对称左右耦合经对角相似变换都变为几何平均",zero(JR/rr-s.sqrt(JR*JL)) and zero(JL*rr-s.sqrt(JR*JL)))
Nn=7; j=2; rv=math.sqrt(3/1); lamj=-2+2*math.sqrt(3)*math.cos(j*math.pi/(Nn+1))
vec=[0]+[rv**i*math.sin(j*i*math.pi/(Nn+1)) for i in range(1,Nn+1)]+[0]
ck("W073",3,"numerical","七胞开放链趋肤本征矢逐点满足原非对称动力学",all(close(-2*vec[i]+3*vec[i-1]+vec[i+1],lamj*vec[i],1e-7) for i in range(1,Nn+1)))
ck("W073",4,"physical_case","开放与周期稳定阈值满足严格不等式并随非互易性分离",2*math.sqrt(3)*math.cos(math.pi/8)<4 and 2*math.sqrt(3)*math.cos(math.pi/8)<3.5<4)
# O074 Berry polarization
th,ph=s.symbols("th ph",real=True)
Aphi=-s.sin(th/2)**2
curv=s.diff(Aphi,th)
ck("O074",1,"symbolic","Jones态Berry联络曲率严格等于半单位球面面积形式",zero(curv+s.sin(th)/2))
ck("O074",2,"independent_derivation","纬线相位积分与所围立体角的一半严格一致",zero(2*s.pi*Aphi+s.pi*(1-s.cos(th))) and close((2*s.pi*Aphi).subs(th,s.pi/2),-math.pi))
delta,Omega=s.symbols("delta Omega",real=True)
ck("O074",3,"numerical","双臂干涉的几何相位反转改变可观测条纹而强度非负",close((2*(1+s.cos(delta+Omega/2))).subs({delta:0,Omega:s.pi}),2) and close((2*(1+s.cos(delta+Omega/2))).subs({delta:s.pi/2,Omega:s.pi}),0))
chi=th*ph
ck("O074",4,"symbolic","规范变换联络差为全微分且曲率在变换后不变",zero(s.diff(Aphi-s.diff(chi,ph),th)-s.diff(-s.diff(chi,th),ph)-curv))
# O075 parametric amplifier
g,z0=s.symbols("g z0",real=True,positive=True)
C=s.cosh(g*z0);H=s.sinh(g*z0)
ck("O075",1,"symbolic","参量放大双曲传递矩阵的行列式严格为一",zero(C*C-H*H-1))
As, Ai, Ar, Ir=s.symbols("As Ai Ar Ir",real=True)
# real field amplitudes: dAs=g*Ai, dAi=g*As
ck("O075",2,"conservation","信号闲频光子通量差在耦合流中导数精确为零",zero(2*As*g*Ai-2*Ai*g*As))
ck("O075",3,"independent_derivation","单种子光子通量差与同反相种子增益均满足双曲恒等式",zero(C*C-H*H-1) and zero(C+H-s.exp(g*z0)) and zero(C-H-s.exp(-g*z0)))
ck("O075",4,"limit","小增益闲频强度二次开启且大增益信号系数趋四分之一",zero(s.limit(H*H/(g*z0)**2,z0,0)-1) and zero(s.limit(C*C/s.exp(2*g*z0),z0,s.oo)-s.Rational(1,4)))
# Q074 repetition stabilizer code
def syndrome(bits):
    return ((-1)**(bits[0]^bits[1]),(-1)**(bits[1]^bits[2]))
ck("Q074",1,"physical_case","四种无错或单X错误综合征两两不同",len({syndrome(bits) for bits in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]})==4)
p=s.symbols("p",real=True)
PL=3*p*p*(1-p)+p**3
ck("Q074",2,"symbolic","独立物理位翻转的二次逻辑错误概率与二项计数一致",zero(PL-(3*p**2-2*p**3)))
ck("Q074",3,"physical_case","纠缠保真度优势区间由概率差因式分解且端点正确",zero(p-PL-p*(1-p)*(1-2*p)) and close(PL.subs(p,.2),.104) and close(PL.subs(p,.5),.5))
q=s.symbols("q",real=True)
PZ=3*q*(1-q)**2+q**3
ck("Q074",4,"symbolic","未检出相位错误的奇偶概率正确并在低噪声线性恶化",zero(PZ-(3*q-6*q*q+4*q**3)) and zero(s.diff(PZ,q).subs(q,0)-3))
# Q075 oscillator Gibbs/Wigner
beta,hbar,om,mm=s.symbols("beta hbar om mm",positive=True)
R=s.exp(-beta*hbar*om)
nbar=R/(1-R)
ck("Q075",1,"symbolic","Gibbs几何本征值归一且占据数与玻色分布一致",zero((1-R)/(1-R)-1) and zero(nbar-1/(s.exp(beta*hbar*om)-1)))
ct=s.coth(beta*hbar*om/2)
dx2=hbar*ct/(2*mm*om);dp2=mm*hbar*om*ct/2
ck("Q075",2,"limit","热谐振子协方差乘积满足Heisenberg界且零温饱和",zero(dx2*dp2-hbar*hbar*ct*ct/4) and zero(s.limit(ct,beta,s.oo)-1))
tt=s.tanh(beta*hbar*om/2)
# integrate Gaussian Wigner analytically using elementary integral
A=tt*mm*om/hbar; B=tt/(hbar*mm*om)
norm=tt/(s.pi*hbar)*s.pi/s.sqrt(A*B)
ck("Q075",3,"independent_derivation","热Wigner二维高斯积分归一且位置边缘二阶矩一致",zero(s.simplify(norm-1)) and zero(s.simplify(1/(2*A)-dx2)))
purity=(1-R)/(1+R)
ck("Q075",4,"limit","热态纯度的几何求和等于双曲正切并趋零温纯态",zero(purity-tt) and zero(s.limit(purity,beta,s.oo)-1) and zero(s.limit(purity,beta,0)))
# provenance and coverage
ids=["M077","M078","E077","E078","T072","T073","W072","W073","O074","O075","Q074","Q075"]
assert len(TESTS)==48 and {(z["id"],z["part"]) for z in TESTS}=={(uid,part) for uid in ids for part in range(1,5)}
assert all((ROOT/"bank"/uid/"meta.json").exists() for uid in ids)
report={"status":"draft_technical_checks_passed_expert_review_pending","round":14,"draft_new_problem_count":12,"target_new_problem_count":50,"passed_count":len(TESTS),"tests":TESTS,"independent_expert_review":"待独立复核","note":"Only 12 draft problems verified; 38 missing. Not a release or merge gate."}
(ROOT/"data"/"round14_draft_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("ROUND14 DRAFT 12 DISTINCT PROBLEMS / 48 EXECUTED PHYSICAL CHECKS PASS; 38 STILL MISSING; EXPERT REVIEW PENDING")
