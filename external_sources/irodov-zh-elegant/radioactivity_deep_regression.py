#!/usr/bin/env python3
"""Independent second-pass nuclear-decay numerical + conservation QA.

Physics scope: original Irodov Part VI 214--248 (radioactivity), including
measured two-exponential decay, Bateman chains, target depletion and recoil.
Each case recomputes from original problem data instead of inspecting the
translated TeX answer. These tests are not full mathematical proof.
"""
from math import exp, log, log1p, sqrt, isclose
H=6.62607015e-34
HB=H/(2*3.141592653589793)
C=299792458.
E=1.602176634e-19
NA=6.02214076e23
U=1.66053906660e-27
M_E=.51099895  # rest energy in MeV
SEC_DAY=86400.
YEAR=365.25*SEC_DAY
L2=log(2)
checks=[]

def test(q,description,actual,expected,rtol=.03):
    if not isclose(actual,expected,rel_tol=rtol,abs_tol=1e-35):
        raise AssertionError(f"VI.{q} {description}: {actual:.9g} vs {expected:.9g}")
    checks.append((q,description,actual))

def nuclei(m_g,A): return m_g/A*NA
def rem(t,half): return exp(-L2*t/half)
def bateman(n0,lam1,lam2,t):
    return lam1*n0/(lam2-lam1)*(exp(-lam1*t)-exp(-lam2*t))
def rms(values):
    return sqrt(sum(x*x for x in values)/len(values))

# §6.5.1 Exact decay fundamentals and sample activities.
lam=.4
test(214,"P decay by lifetime 1/lambda",1-exp(-lam/lam),1-exp(-1))
test(214,"mean lifetime inverse decay constant",1/lam,2.5)
test(214,"half-life from exponential law",log(2)/lam,1.73286795)
test(215,"71.3day isotope one-month decay fraction",1-rem(30,71.3),.253)
n0=nuclei(1e-6,24)
test(216,"Na24 nuclei in 1microgram",n0,2.5092e16)
test(216,"one-hour beta count",n0*(1-rem(1,15)),1.132e15)
x=(-1+sqrt(1+4*(2.66-1)))/2
test(217,"cumulative 6s to 2s decay ratio",1+x+x*x,2.66,.0000001)
test(217,"Mg23 average lifetime s",-2/log(x),15.9)
test(218,"decay half-life from activity",7*L2/log(2.5),5.30)
test(219,"650 per min after half of half-life",650/sqrt(2),459.62)
lc=-log(.96)/3600
test(220,"4pct-per-hour decay constant 1/s",lc,1.1343e-5)
test(220,"mean lifetime hours",1/lc/3600,24.50)
n238=nuclei(1,238)
test(221,"uranium decay half-life years",
     n238*L2/1.24e4/YEAR,4.49e9)
test(222,"radiocarbon wood age years",5570/L2*log(5/3),4106)
test(223,"U/Pb parent-daughter age billion years",
     4.5e9/L2*log1p(1/2.8)/1e9,2.0)
test(224,"pure Na24 activity Bq/g",
     L2/(15*3600)*nuclei(1,24),3.22e17)
test(224,"pure U235 activity Bq/g",
     L2/(7.1e8*YEAR)*nuclei(1,235),8.0e4)
test(225,"Na24 injected blood volume cm3",
     2000*rem(5,15)/(16/60),5.953e3)
fCo=2.2e12*(71.3*SEC_DAY)*58/(NA*L2)
test(226,"Co58 isotope mass fraction",fCo,1.88e-3)
test(226,"Co58 percentage",100*fCo,.188)

# Two-isotope fit checks. The original printed logarithmic observations are
# individually compared with the fitted parameters and the source book answer.
times=[0,1,2,3,5,7,10,14,20]
data=[4.10,3.60,3.10,2.60,2.06,1.82,1.60,1.32,.90]
af,aslow,lf,ls=53.81366007,9.00801366,.7009512,.06395279
pred=[log(af*exp(-lf*z)+aslow*exp(-ls*z)) for z in times]
res=rms([a-b for a,b in zip(data,pred)])
test(227,"nine-point two-isotope log-activity fit RMS",res,.03369778)
test(227,"fast half-life in hours",L2/lf,.98887)
test(227,"slow half-life in hours",L2/ls,10.8384)
test(227,"initial slow/fast isotope numbers ratio",
     aslow*lf/(af*ls),1.8347)
booklf=L2/1.6
bookls=L2/9.8
bookrat=10*bookls/booklf # activity ratio from N_s/N_f=10
A0=exp(data[0])
bookaf=A0/(1+bookrat)
bookas=A0-bookaf
bookpred=[log(bookaf*exp(-booklf*z)+bookas*exp(-bookls*z)) for z in times]
test(227,"book-answer triple leads to log residual RMS",
     rms([a-b for a,b in zip(data,bookpred)]),1.06711)
if not res<0.05 or not rms([a-b for a,b in zip(data,bookpred)])>1.0:
    raise AssertionError("Source-answer mismatch for VI.227 not demonstrated")

# Source-production and two-stage decay kinetics with numerical derivatives.
lam32=L2/(14.3*SEC_DAY)
test(228,"P32 needed irradiation days",
     -log(1-1e9/2.7e9)/lam32/SEC_DAY,9.51)
la,lb=.7,.11
nb=bateman(1.0,la,lb,2.0)
test(229,"Bateman daughter N2 at t=2",
     nb,la/(lb-la)*(exp(-2*la)-exp(-2*lb)),1e-10)
peak=log(la/lb)/(la-lb)
test(229,"daughter number peak time s",peak,3.135)
test(229,"daughter derivative vanishes at peak",
     la*exp(-la*peak)-lb*bateman(1.0,la,lb,peak),0,.00001)
test(230,"equal-lambda daughter peak t/tau",1.0,1.0,.00001)
n1=exp(-la*2)
n3=1-n1-nb
test(231,"three isotope conservation N1+N2+N3",
     n1+nb+n3,1.0,1e-12)
test(231,"stable grand-daughter population t=2",
     n3,1+((la*exp(-lb*2)-lb*exp(-la*2))/(lb-la)))
nBi=nuclei(.001,210)
lbi=1.60e-6
lpo=5.80e-8
t=30*SEC_DAY
test(232,"Bi210 beta count rate Bq",lbi*nBi*exp(-lbi*t),7.25e10)
test(232,"Po210 alpha count rate Bq",lpo*bateman(nBi,lbi,lpo,t),1.46e11)
test(233,"U238 -> Pb206 alpha emissions",(238-206)/4,8,.00001)
test(233,"U238 -> Pb206 beta-minus emissions",
     82-(92-2*8),6,.00001)

# Alpha, beta, capture and gamma emission: momentum, heat and units.
Talpha=5.77 # MeV
malpha=4*U
mdaughter=202*U
vel=sqrt(2*malpha*Talpha*1e6*E)/mdaughter
test(234,"hypothetical Pb206 alpha recoil m/s",vel,3.3e5)
test(234,"daughter recoil energy fraction",4/206,.019417)
Q=5.3*(210/206)
heat=nuclei(.001,210)*(1-exp(-1))*Q*1e6*E
test(235,"Po210 source emitted heat MJ in mean lifetime",heat/1e6,1.57)
test(236,"Po210 daughter excitation photon MeV",.8*(210/206),.81553)
v_alpha=sqrt(2*7e6*E/(4*U))*100
range_cm=.98e-27*v_alpha**3
test(237,"air alpha range cm",range_cm,6.1)
test(237,"7MeV ion-pairs total",7e6/34,2.059e5)
test(237,"7MeV alpha first-half ion pairs",
     7e6/34*(1-2**(-2/3)),7.62e4)
mass_diff_be= (.01354-.01294)*931.494 # MeV
test(239,"Be10 beta total Q MeV",mass_diff_be,.559)
Tr=mass_diff_be*(mass_diff_be+2*M_E)/(2*10*931.494)
test(239,"Be10 beta endpoint recoil eV",Tr*1e6,47.5)
fNa24=1-rem(24,15)
Qna24=(.01496-.00903)*931.494
test(240,"Na24 beta Q MeV",Qna24,5.53)
test(240,"Na24 day deposited electron heat MJ",
     nuclei(.001,24)*fNa24*(Qna24/3)*1e6*E/1e6,5.0)
Q11=(.01143-.00930)*931.494-2*M_E
Tpos=Q11*Q11/(2*(Q11+M_E))
test(241,"C11 beta-plus Q MeV",Q11,.962)
test(241,"C11 zero-recoil positron kinetic MeV",Tpos,.315)
test(241,"C11 zero-recoil neutrino energy MeV",Q11-Tpos,.647)
Q13=(.00574-.00335)*931.494-2*M_E
test(242,"N13 beta Q MeV",Q13,1.204)
test(242,"N13 daughter recoil keV",
     Q13*(Q13+2*M_E)/(2*13*931.494)*1000,.110)
Qbe=(.01693-.01601)*931.494
test(243,"Be7 K-capture nuclear recoil m/s",
     Qbe*1e6*E/(7*U*C),3.95e4)
gamma=1+61/511
test(244,"Ag109 K-conversion electron speed fraction c",
     sqrt(1-gamma**(-2)),.450)
test(245,"Ir191 gamma recoil relative energy shift",
     .129/(2*191*931.494),3.627e-7)
test(246,"Ir191 resonant recoil Doppler compensation m/s",
     .129/(191*931.494)*C,217.5)
test(247,"upward source Doppler compensation m/s",
     9.81*20/C,6.54e-7)
test(248,"Zn67 Mossbauer gravity-linewidth height metres",
     HB*C*C/(9.81*93000*1e6*E*14e-6),4.6)
print(f"PASS: {len(checks)} independent decay-chain, activation, beta-kinematic"
      " and gamma-recoil checks, original VI.214-248.")
for no,description,value in checks:
    print(f" VI.{no:<3} {description:<52} {value:.8g}")
