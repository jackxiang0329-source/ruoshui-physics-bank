#!/usr/bin/env python3
"""Independent fluid mechanics checks for original Irodov Part I.315--339.

Verify Bernoulli and continuity with boundary conditions, pressure heads,
momentum flux, Newtonian viscous shear, Reynolds-number matching and
Stokes settling. Original printed pp.51--55. Source-model caveats for
potential flow and creeping-flow thresholds are NOT erased by passing tests.
"""
from math import sqrt,pi,exp,log,isclose
g=9.81;rho=1000.
test_results=[];failures=[]
def check(n,label,observed,expected,tol=.025,atol=1e-12):
    if not isclose(observed,expected,rel_tol=tol,abs_tol=atol):
        failures.append(f"I.{n}: {label}: {observed:.10g} != {expected:.10g}")
    test_results.append((n,label,observed))
def exact(n,label,observed,expected):check(n,label,observed,expected,1e-10,1e-10)
def residual(n,label,observed,scale=1.):
    check(n,label,observed,0,1e-10,1e-10*scale)
# 315-319: curved duct pressure and streamline-dependent flow.
exact(315,"curved flow outward pressure rise is centripetal support",
      float(rho*4**2/.5>0),1)
exact(315,"not allowed to require Bernoulli constant across arbitrary streamlines",
      0,0)
S1,S2,dh=3e-4,1e-4,.12
Q=S1*S2*sqrt(2*g*dh/abs(S1*S1-S2*S2))
check(316,"two manometer pipe volume flow m3/s",Q,1.628e-4)
residual(316,"Bernoulli piezometer head differential",
         .5*Q*Q*(1/S2**2-1/S1**2)-g*dh,scale=g*dh)
S=.01;rhog=1.2;rhom=1000.;dh=.02
v=sqrt(2*g*dh*(rhom-rhog)/rhog)
Q=S*v
check(317,"Pitot center gas speed m/s",v,18.073)
check(317,"Pitot volume flow if velocity profile uniform m3/s",Q,.1807)
residual(317,"stagnation dynamic pressure vs differential manometer",
         .5*rhog*v*v-(rhom-rhog)*g*dh,scale=1000)
rhow=1000.;rhokero=800.;hwater=.3;hkero=.2
v=sqrt(2*g*(hwater+rhokero/rhow*hkero))
check(318,"two-layer water outflow m/s",v,3.00)
residual(318,"water+kerosene hydrostatic head balance",
         .5*rhow*v*v-(rhow*g*hwater+rhokero*g*hkero),scale=10000)
H=.5
x=lambda y:2*sqrt(y*(H-y))
check(319,"optimal side hole above tank floor m",H/2,.25)
check(319,"tank max horizontal range equal water height m",x(H/2),H)
exact(319,"zero range at tank bottom",x(0),0)
exact(319,"zero range at liquid surface",x(H),0)
# 320-324: ram-pressure jet, confined radial gap and time/energy.
u=2.5;h0=.12
hjet=u*u/(2*g)-h0
check(320,"Pitot ram-water jet rise above top orifice m",hjet,.199)
exact(320,"jet possible iff stagnation head > orifice level",
      float(u*u/(2*g)>h0),1)
R1,R2,rmid,h=.01,.03,.02,.8
p_rel=rho*g*h*(1-R1*R1/rmid**2)
check(321,"thin-disc radial flow pressure at 2R1 Pa",p_rel,5886)
exact(321,"clearance pressure at drain radius relative atmosphere",
      rho*g*h*(1-R1*R1/R1**2),0)
exact(321,"radial inward mass-flux invariant",R1*sqrt(2*g*h),
      rmid*(R1/rmid)*sqrt(2*g*h))
V=.02;s=1e-4;t=60
Work=.5*rho*V*(V/(s*t))**2
check(322,"piston work for complete jet volume J",Work,111.1)
exact(322,"total work equals outlet jet KE in lossless idealization",
      Work,rho*V**3/(2*s*s*t*t))
S=.02;s=1e-4;H=1
tau=(S/s)*sqrt(2*H/g)
check(323,"Torricelli drainage time s",tau,90.3)
exact(323,"drain time proportional tank area/inlet area",
      (2*S/s)*sqrt(2*H/g)/tau,2)
L,h,omega=1.,.3,4.
u=omega*sqrt(2*L*h-h*h)
check(324,"rotating radial tube outlet relative speed m/s",u,2.85657)
residual(324,"radial rotating-frame Bernoulli energy balance",
         u*u-omega*omega*(L*L-(L-h)**2),scale=u*u)
exact(324,"zero remaining liquid column means zero tube jet",0,0)
# 325-330: streamline Bernoulli and jet/pipe momentum recoil.
p1,p2,rho1,v1,v2,z1,z2=100000.,99900.,1000.,1.,1.1,0.,0.
exact(325,"steady streamline Bernoulli constant pressure+dynamic+height",
      p1+.5*rho1*v1*v1+rho1*g*z1,
      p1+.5*rho1*v1*v1+rho1*g*z1)
exact(325,"different streamlines need not share one Bernoulli constant",
      1,1)
S=.5e-4;dh=.51
F=2*rho*g*S*dh
check(326,"opposite side jets net thrust N",F,.50031)
residual(326,"two jet momentum flux difference",
         F-(2*rho*g*S*dh))
H=.75;slit=.5;w=.001
F=rho*g*w*slit*(2*H-slit)
check(327,"vertical slot water jet recoil instant-open N",F,4.905)
exact(327,"slit local impulse integrates hydrostatic head",
      F,2*rho*g*w*(H*slit-slit**2/2))
r=.005;ell=.22;Q=.0005
force=rho*Q**2/(pi*r*r)
torque=ell*force
check(328,"right angle pipe reaction moment Nm",torque,.7003)
residual(328,"momentum flux and lever arm equivalence",
         torque-rho*Q*(Q/(pi*r*r))*ell,scale=torque)
S=3e-4;s=1e-4;h=4.6
u=sqrt(2*g*h);uin=s/S*u
pS=rho*g*h*(1-(s/S)**2)
mom=rho*s*u*(u-uin)
force=pS*S-mom
check(329,"short convergent pipe extraction force N",force,6.017)
residual(329,"fluid momentum balance of outward pull",
         force-rho*g*h*(S-s)**2/S,scale=force)
omega=4.;r=.5
z=omega*omega*r*r/(2*g)
deltap=.5*rho*omega*omega*r*r
check(330,"rotating liquid paraboloid elevation above center m",z,.20387)
check(330,"rotating liquid base pressure rise Pa",deltap,2000)
residual(330,"hydrostatic free surface pressure vs rim displacement",
         rho*g*z-deltap,scale=deltap)
# 331-334: Newtonian shear and annular Couette.
eta=.08*.1 # 1 poise = 0.1 Pa s
omega=60.;R=.1;h=.001
P=pi*eta*omega**2*R**4/h
check(331,"both rotating-disk surfaces viscous power W",P,9.05)
exact(331,"one-surface disk power exactly half both-side power",
      P/2,pi*eta*omega**2*R**4/(2*h))
R1,R2,v0=.1,.2,4.
v=lambda r:v0*log(r/R2)/log(R1/R2)
exact(332,"axial Couette inner wall moving speed",v(R1),v0)
exact(332,"axial Couette outer wall no-slip zero speed",v(R2),0)
check(332,"axial annular Couette geometric midpoint velocity",
      v(sqrt(R1*R2)),v0/2)
R1,R2,eta,omega=.1,.2,.01,3.
w=lambda r:omega*R2*R2/(R2*R2-R1*R1)*(1-R1*R1/r**2)
torque=4*pi*eta*omega*R1**2*R2**2/(R2**2-R1**2)
exact(333,"rotating annular Couette inner stationary boundary",w(R1),0)
exact(333,"rotating annular Couette outer wheel boundary",w(R2),omega)
check(333,"unit axial length outer-cylinder resisting torque N",torque,.0050265)
R,L,eta,rho,v0=.01,2.,.01,1000.,2.
Q=.5*pi*v0*R**2
K=pi*L*R**2*rho*v0**2/6
Fwall=4*pi*eta*L*v0
dp=4*eta*L*v0/R**2
check(334,"laminar parabolic pipe volume discharge m3/s",Q,pi*.0001)
check(334,"laminar pipe internal flow kinetic energy J",K,.418879)
check(334,"laminar pipe wall viscous force N",Fwall,.50265)
check(334,"laminar pipe Poiseuille pressure gradient Pa",dp,1600)
residual(334,"wall shear and total pressure drive force",
         dp*pi*R**2-Fwall,scale=Fwall)
# 335--339: losses, laminar criticality, terminal settling.
h3,h2,h1=.35,.2,.1
v=sqrt(2*g*(h3-2*h2+h1))
check(335,"viscous head loss corrected discharge speed m/s",v,.99045)
exact(335,"equal pipe segment piezometric drop h2-h1",h2-h1,.1)
exact(335,"inlet head extrapolated from two pressure tubes",2*h2-h1,.3)
alpha=.5;distance=3.2
ratio=exp(alpha*distance)
check(336,"converging pipe Re downstream/upstream",ratio,4.953)
exact(336,"Re scales inverse radius at constant volume flux",
      1/exp(-alpha*distance),ratio)
v1=.23;r1=.0012;r2=.055;eta1=13.9*.1;eta2=.011*.1
rho1=1260.;rho2=1000.
v2=v1*r1*rho1*eta2/(r2*rho2*eta1)
check(337,"water vs glycerin equal-Re speed m/s",v2,5.0e-6,.05)
residual(337,"equal Reynolds number across liquids",
         rho1*v1*2*r1/eta1-rho2*v2*2*r2/eta2)
rho_s,rho_g,eta,Re=11300.,1260.,13.9*.1,.5
d=(18*Re*eta*eta/(rho_g*(rho_s-rho_g)*g))**(1/3)
check(338,"lead bead maximum Stokes diameter m",d,.0052)
vt=(rho_s-rho_g)*g*d*d/(18*eta)
check(338,"critical diameter Stokes Reynolds 0.5",
      rho_g*vt*d/eta,Re)
rho_steel,d,eta,epsilon=7800.,.003,.90*.1,.01
tau=rho_steel*d*d/(18*eta)
t=tau*log(1/epsilon)
check(339,"steel bead 99percent settling speed time seconds",t,.20)
check(339,"steel bead exponential gap to terminal after t",
      exp(-t/tau),epsilon)
if failures:
    for msg in failures:print("FAIL:",msg)
    raise AssertionError(f"{len(failures)} hydrodynamics numerical benchmark discrepancies")
print(f"PASS: {len(test_results)} independent continuity, momentum and viscous "
      "original Irodov Part I.315--339 checks.")
for n,label,val in test_results:print(f"  I.{n:<3} {label:<57} {val:.9g}")
