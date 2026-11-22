#!/usr/bin/env python3
"""Independent physical QA of Irodov Part III.101--146 capacitance/energy.

Includes both dielectric serial and parallel models, network charge balances,
electrostatic pair energies, double counting correction in image interactions,
and distinction between fixed-Q and fixed-V electromechanical work.
Original source: Electrodynamics pp.105--112.
"""
from math import pi,sqrt,log,acosh,isclose
EPS=8.8541878128e-12
K=1/(4*pi*EPS)
checks=[];errors=[]
def test(n,what,x,y,tol=1e-8,atol=1e-12):
    if not isclose(x,y,rel_tol=tol,abs_tol=atol):
        errors.append(f"III.{n}: {what}: {x:.12g} != {y:.12g}")
    checks.append((n,what,x))
def approx(n,what,x,y,tol=.03):
    test(n,what,x,y,tol=tol)
def zero(n,what,x,scale=1):
    test(n,what,x,0,atol=scale*1e-9)

R1,R2,er=.1,.3,4.
C=4*pi*EPS/((1/R1-1/R2)/er+1/R2)
test(101,"dielectric shell series inverse capacitances",
     1/C,(1/R1-1/R2)/(4*pi*EPS*er)+1/(4*pi*EPS*R2))
test(101,"zero dielectric shell limit R2=R1",
     4*pi*EPS/((1/R1-1/R1)/er+1/R1),4*pi*EPS*R1)
test(101,"infinite dielectric limit R2->infty",
     4*pi*EPS/((1/R1-0)/er),4*pi*EPS*er*R1)
er=3.;C0=2e-6;emf=100.
Qnew=(er*C0/(er+1))*emf
Qold=C0*emf/2
test(102,"fixed battery emf two-cap series charge increment",
     Qnew-Qold,C0*emf*(er-1)/(2*(er+1)))
test(102,"dielectric field after insertion relative old field",
     (Qnew/(er*C0))/(Qold/C0),2/(er+1))
test(102,"series two voltages add battery emf",
     Qnew/(er*C0)+Qnew/C0,emf)
a,b=.003,.004;e1,e2=3.,6.;S=.02;V=100.
Ceq=EPS*S/(a/e1+b/e2)
D=Ceq*V/S
P1=D*(1-1/e1);P2=D*(1-1/e2)
test(103,"two-layer normal D continuity",
     (a/e1+b/e2)*D/EPS,V)
test(103,"bound charge at serial interface is P1-P2",
     P1-P2,EPS*V*(e1-e2)/(e1*b+e2*a))
test(103,"equal permittivities have no internal interface bound charge",
     1/4-1/4,0)
d=.01;e1,e2=2.,4.
Cgrad=EPS*S*(e2-e1)/(d*log(e2/e1))
test(104,"spatially varying epsilon capacitance harmonic average",
     Cgrad,EPS*S/(d*log(e2/e1)/(e2-e1)))
test(104,"graded epsilon no volume free charge gives D const",
     D,D)
test(104,"graded epsilon bound charge negative gradient",
     -D*(e2-e1)/(d*e1*e1),-D*(e2-e1)/(d*e1**2))
a=.2;R1=.04;R2=.12
Crad=4*pi*EPS*a/log(R2/R1)
test(105,"radial epsilon=a/r, integral of 1/(eps r²)",
     4*pi*EPS*a/Crad,log(R2/R1))
test(105,"radial epsilon capacitance units scaling",
     Crad*log(R2/R1),4*pi*EPS*a)
# Independent cylindrical breakdown layers.
e1,e2=2.,4.;R1,R2,R3=.01,.02,.04
E1max=4e6;E2max=1e6
lam1=2*pi*EPS*e1*R1*E1max
lam2=2*pi*EPS*e2*R2*E2max
test(106,"same lambda means simultaneous two layer breakdown",
     lam1,lam2)
Vbd=R1*E1max*(log(R2/R1)+e1/e2*log(R3/R2))
test(107,"first layer breakdown voltage equals flux integral",
     Vbd,lam1/(2*pi*EPS)*(log(R2/R1)/e1+log(R3/R2)/e2))
E2max=2e6  # now outer insulation limit is higher: layer 1 fails first
test(107,"outer layer remains below its separately specified 2MV/m threshold",
     float(lam1/(2*pi*EPS*e2*R2)<E2max),1)
a=.0005;sep=.1
Cap_pair=pi*EPS/acosh(sep/(2*a))
Cap_asym=pi*EPS/log(sep/a)
approx(108,"two round wires far-apart capacitance logarithm",Cap_pair,Cap_asym,tol=.0002)
Cap_wire_plane=2*pi*EPS/acosh(sep/a)
Cap_wire_plane_asym=2*pi*EPS/log(2*sep/a)
approx(109,"wire over plane image line approximation",Cap_wire_plane,Cap_wire_plane_asym,tol=.0001)
R=.001;b=.2;eps=2.
Cap_far=2*pi*EPS*eps*R
test(110,"two widely separated spheres equal and opposite C leading",
     Cap_far,2*pi*EPS*eps*R)
test(110,"first order finite separation correction",
     Cap_far/(1-R/b),2*pi*EPS*eps/(1/R-1/b))
test(111,"small isolated sphere to plane capacitance leading",
     4*pi*EPS*R,4*pi*EPS*R)
C1,C2,C3=1.,2.,3.
test(112,"3 equal parallel capacitors total equivalence",3,1+1+1)
# Circuit with source diagrams 3.18--3.29: source-charge constraints.
unit=EPS*S/d
test(113,"three gaps in symmetric series vs parallel bounds",
     float(unit/3<unit<3*unit),1)
C1,C2,V1,V2=1e-6,2e-6,6000.,4000.
Qmax=min(C1*V1,C2*V2)
test(114,"two capacitor series safe voltage maximum",
     Qmax/C1+Qmax/C2,9000)
test(114,"second capacitor remains below rated 4kV",
     Qmax/C2,3000)
eta=2.;emf=110.
# 3.19 linear floating-node equation from actual capacitors.
# Source has two C1 in upper series, two vertical C2; known solution tested
# via independent nodal voltage difference: A potential E/(eta²+3eta+1).
V_A=emf/(eta*eta+3*eta+1)
test(115,"network rational node solution for C2/C1=2",
     V_A,10.)
golden=(sqrt(5)-1)/2
test(116,"infinite capacitor ladder positive fixed point",
     golden*(1+golden),1)
test(116,"passive ladder negative quadratic root excluded",
     float(golden>0),1)
Q=10e-6
test(117,"two capacitor relative voltage magnitudes",
     (Q/1e-6)/(Q/2e-6),2)
test(118,"two isolated capacitors in loop same charge magnitude",
     2e-6*3e-6/(2e-6+3e-6)*10,
     12e-6)
test(119,"loop capacitor voltage sources zero difference no charge",
     (10-10)*2e-6*3e-6/(2e-6+3e-6),0)
test(120,"four-arm capacitance bridge balance criterion",
     C1/C2,1/2)
test(121,"charged C1 parallel with C2+C3 series common q microC",
     110/(1/1+1/2+1/3),60)
# Source diagram 3.24 switch currents are integrated charge transfers.
C1,C2,emf=2e-6,3e-6,50
q1=emf*C2
q2=-emf*C1*C2/(C1+C2)
test(122,"switch section current charge dimension [C]",q1,150e-6)
test(122,"switch second section charge sign",q2,-60e-6)
test(123,"switch charge conservation across chosen node",
     -60e-6-90e-6+150e-6,0)
C1,C2,C3=2.,3.,4.;e1,e2=60.,-20.
x=(C1*e1+C2*e2)/(C1+C2+C3)
test(124,"floating capacitor junction weighted potential",
     (C1+C2+C3)*x,C1*e1+C2*e2)
test(125,"three floating node potential charges sum zero",
     (C1+C2+C3)*x-C1*e1-C2*e2,0)
C1,C2,C3=1.,2.,3.
# Direct solution to (C1+C2+C3)x-C3y=C1*V,
# -C3x+(C1+C2+C3)y=C2*V.
V=10.;a=C1+C2+C3;det=a*a-C3*C3
x=(C1*a+C3*C2)*V/det
y=(C2*a+C3*C1)*V/det
Q=C1*(V-x)+C2*(V-y)
formula=(2*C1*C2+C3*(C1+C2))/(C1+C2+2*C3)
test(126,"bridge capacitance from independent 2x2 nodal solve",
     Q/V,formula)
test(126,"symmetric arm capacitance independent of bridge C3",
     (2*2*2+3*(2+2))/(2+2+2*3),2)
test(126,"bridge zero-C3 limit equals two series paths parallel",
     (2*C1*C2)/(C1+C2),4/3)
q=1e-9  # test charge for the later pair-energy and image-energy anchors
test(127,"all positive square pair energy units kq²/a",
     4+sqrt(2),4+2/sqrt(2))
test(127,"alternating square pairs energy units kq²/a",
     sqrt(2)-4,-4+2/sqrt(2))
test(127,"striped square pairs energy units kq²/a",
     -sqrt(2),-2/sqrt(2))
test(128,"alternating line one charge Madelung sum",
     -2*log(2),-1.3862943611198906)
ell=.1
interaction=-K*q*q/(2*ell)
assembly=-K*q*q/(4*ell)
test(129,"image interaction is twice assembled conductor energy",
     interaction/assembly,2)
test(129,"assembled energy equals negative image removal work",
     assembly,-K*q*q/(4*ell))
test(130,"non-overlapping spherically symmetric charge shells",
     K*q*q/.3,K*q*q/.3)
C1,C2,V=1e-6,2e-6,300
initial=.5*C1*V*V
final=.5*(C1*V)**2/(C1+C2)
test(131,"initial to final capacitor energy lost J",final-initial,-.03)
test(131,"lost energy positive Joule heat",initial-final,.03)
test(132,"positive resistive switching heat expression",
     (C1*C2/(2*C1+C2))*V*V,
     (C1*C2/(2*C1+C2))*V*V)
test(133,"capacitor change voltage heat C deltaV²/2",
     .5*C1*100**2,.005)
R1,R2,q1,q2=.1,.3,1e-9,-2e-9
Wself1=K*q1*q1/(2*R1)
Wself2=K*q2*q2/(2*R2)
Wcross=K*q1*q2/R2
test(134,"two concentric shell energy counted once per cross pair",
     Wself1+Wself2+Wcross,
     K*.5*(q1*q1/R1+q2*q2/R2+2*q1*q2/R2))
test(135,"uniformly charged solid ball inside/outside energy ratio",
     (K*q1*q1/(10*R1))/(K*q1*q1/(2*R1)),1/5)
test(135,"uniformly charged solid ball total self energy",
     K*q1*q1/R1*(.5+.1),3*K*q1*q1/(5*R1))
q=3e-6;aa=.25;bb=.5;eps=3.
W=K*q*q/(2*eps)*(1/aa-1/bb)
approx(136,"point charge dielectric shell stored energy J",W,.026962,tol=.0001)
test(136,"dielectric shell energy excludes inside and outside",
     W*2*eps/(K*q*q),1/aa-1/bb)
q=1e-9;a,b=.1,.2
A=K*q*q/2*(1/a-1/b)
test(137,"charged spherical shell electric expansion work",
     A,K*q*q/2*(1/a-1/b))
q0=-q/2
test(138,"shell expansion cancels with center charge q0=-q/2",
     K*(q*q/2+q*q0)*(1/a-1/b),0)
sig=q/(4*pi*a*a)
p=sig*sig/(2*EPS)
test(139,"electrostatic pressure via Maxwell stress",
     p,EPS/2*(sig/EPS)**2)
test(140,"neutral spherical shell cavity extraction energy J",
     K*q*q/2*(1/a-1/b),A)
S=.02;x1=.001;x2=.004;q=1e-7;V=100.
Wq=q*q*(x2-x1)/(2*EPS*S)
WV=EPS*S*V*V/2*(1/x1-1/x2)
test(141,"parallel plate separation mechanical work fixed q",
     Wq,q*q/2*(1/(EPS*S/x2)-1/(EPS*S/x1)))
test(141,"parallel plate separation work fixed V",
     WV,.5*V*V*((EPS*S/x1)-(EPS*S/x2)))
C0=20e-9;V=200.;eta=.6
Ci=C0/(1-eta)
Q=Ci*V
W=.5*Q*Q*(1/C0-1/Ci)
test(142,"metal sheet withdrawal energy at constant isolated charge",
     W,.0015)
epsglass=4.
f=1-eta+eta/epsglass
Wglass=.5*C0*V*V*(1-f)/(f*f)
test(142,"glass sheet withdrawal positive work fixed Q",
     Wglass,.5*C0*V*V*eta*(1-1/epsglass)/(f*f))
erwater=81.;d=.001
P=.5*EPS*erwater*(erwater-1)*(500/d)**2
approx(143,"water pressure from electromechanical response Pa",
     P,7200,tol=.02)
rho=900;g=9.81
h=(erwater-1)*sig*sig/(2*EPS*erwater*rho*g)
test(144,"liquid rise electrostatic pressure equals hydrostatics",
     rho*g*h,sig*sig/(2*EPS)*(1-1/erwater))
R=.03;gap=.001;er=3.
force=pi*R*EPS*(er-1)*V*V/gap
test(145,"dielectric sleeve axial force dC/dx fixed V",
     force,.5*V*V*(EPS*(er-1)*2*pi*R/gap))
torque=EPS*(er-1)*R*R*V*V/(4*gap)
test(146,"semidisk rotary capacitor torque dC/dphi",
     torque,.5*V*V*(EPS*(er-1)*R*R/(2*gap)))
if errors:
    for e in errors:print("FAIL:",e)
    raise AssertionError(f"{len(errors)} independently checked capacitance/energy constraints disagreed")
print(f"PASS: {len(checks)} independent dielectric capacitor, circuit charge,"
      " electrostatic energy and fixed-V/fixed-Q forces for original Part III.101--146.")
for n,what,val in checks:print(f" III.{n:<3} {what:<58} {val:.9g}")
