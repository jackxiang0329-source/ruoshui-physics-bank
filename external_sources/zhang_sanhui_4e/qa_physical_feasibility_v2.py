#!/usr/bin/env python3
"""Seven substantive candidate-model feasibility checks; no source scan certification."""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def close(x,y,rtol=.005):
    assert math.isclose(x,y,rel_tol=rtol),f"{x} != {y}"
def audit_15_3():
    R1,r0,R2=.1,.14,.18
    assert R1<r0<R2<2*R1
    close((1/(2*r0))/(1/(4*R1)),2*R1/r0)
    assert r0/(2*R1)<1
def audit_17_11():
    R=1.
    for r0 in (.1,.5,1/math.sqrt(2)):
        rm=math.sqrt(2)*r0
        assert rm<=R+1e-12
        close(math.pi*r0**2,.5*math.pi*rm**2)
    assert math.sqrt(2)*.8>R
def audit_18_27():
    a,r,L,m,v=.012,.067,5.,.317,4200.
    assert a<2*r
    close(a/(2*r),.0895522388)
    current=math.sqrt(2*math.pi*m*v*v/(2*L)/(4*math.pi*1e-7*math.log((a+r)/r)))
    close(current,4.12e6)
    assert current>0  # A number exists, but rails geometrically overlap.
def audit_19_11():
    i_on=2*math.pi*.00025*2
    i_all=2*math.pi*.0004*2
    close(i_on,.00314159265)
    close(i_all,.00502654825)
    assert i_on<i_all
def audit_21_7():
    e=1.602176634e-19
    eps=8.8541878128e-12
    c=299792458.
    mass=9.1093837139e-31
    E=.0039
    a=e*E/mass
    N=8.5e28*math.pi*(.0026/2)**2*.05
    P1=e*e*a*a/(6*math.pi*eps*c**3)
    p_ohmic=12*E*.05
    close(N*N*P1,1.3675e9)
    close(p_ohmic,.00234)
    assert N*N*P1/p_ohmic>5e11
def audit_25_21():
    s=-6.
    sp=18.
    f2=1/(1/s+1/sp)
    close(f2,-9.)
    magnification=-sp/s
    close(magnification*20,60.)
    close(magnification*20/.2,300.)
def audit_30_17():
    phi=2e12
    intake=phi*(6*2**2)/4
    close(intake,1.2e13)
    lm=math.log(2)/(5.27*365.25*86400)
    activity=intake*(-math.expm1(-lm*21600))
    close(activity/3.7e10,.0291961)
    thin=(8*8.858/59)*6.02214076e23*120e-24*phi
    assert thin>intake>phi*4
checks=[("15.3",audit_15_3),("17.11",audit_17_11),
 ("18.27",audit_18_27),("19.11",audit_19_11),
 ("21.7",audit_21_7),("25.21",audit_25_21),
 ("30.17",audit_30_17)]
def main():
    assert len(checks)==7
    for question,fn in checks:
        ch=int(question.split(".")[0])
        tag=rf"\paragraph{{习题 {question}}}"
        for kind in ("questions","solutions"):
            file=ROOT/f"chapters/{ch:02d}/{kind}.tex"
            assert tag in file.read_text(encoding="utf-8"),str(file)
        fn()
        print("PASS model-domain audit",question)
    print("Seven case-level checks on existing 943 candidates; no original scan checks.")
if __name__=="__main__":main()
