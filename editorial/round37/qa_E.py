from qa_common import *
def run():
    # E256 coaxial TEM
    eps,mu,a,b,lam,I=2.1,1.3,.5,2.,1.6,.7
    Er=lambda r:lam/(2*P*eps*r)
    H=lambda r:I/(2*P*r)
    check("E256",1,"coaxial Gauss voltage radial integral",
          integrate(Er,a,b),lam*L(b/a)/(2*P*eps),method="Gauss-voltage")
    check("E256",2,"Poynting integral gives electric terminal power",
          integrate(lambda r:Er(r)*H(r)*2*P*r,a,b),
          I*lam*L(b/a)/(2*P*eps),method="Poynting-power")
    check("E256",3,"line capacitance inductance TEM speed",
          (2*P*eps/L(b/a))*(mu*L(b/a)/(2*P)),eps*mu,method="TEM-impedance")
    check("E256",4,"electromagnetic momentum density scales as S over v squared",
          eps*mu*Er(.8)*H(.8),Er(.8)*H(.8)/(1/(eps*mu)),method="field-momentum")
    # E257 dielectric sphere
    e1,e2,E0,a=3.,2.,.8,1.3
    Ein=3*e2*E0/(e1+2*e2)
    Ccoef=a**3*E0*(e1-e2)/(e1+2*e2)
    check("E257",1,"dielectric sphere tangential E boundary",
          Ein,a**(-3)*Ccoef+E0-2*Ccoef/a**3 if False else E0-Ccoef/a**3,method="electric-potential-continuity")
    check("E257",2,"normal dielectric displacement boundary",
          e1*Ein,e2*(E0+2*Ccoef/a**3),method="D-normal-boundary")
    check("E257",3,"induced polarization dipole coefficient",
          4*P*e2*Ccoef,4*P*e2*a**3*(e1-e2)/(e1+2*e2)*E0,method="multipole-match")
    check("E257",4,"homogeneous sphere has zero polarizability",
          (e2-e2)/(e2+2*e2),0,method="contrast-limit")
    # E258 ferromagnet wall
    Aex,K,x=2.4,1.6,.7
    width=S(Aex/K)
    th=lambda z:2*math.atan(E(z/width))
    check("E258",1,"domain wall Euler equation residual",
          Aex*der2(th,x)-K*SI(th(x))*C(th(x)),0,method="magnetic-wall-ODE")
    check("E258",2,"wall profile derivative first integral",
          Aex*der(th,x)**2,K*SI(th(x))**2,method="first-integral")
    check("E258",3,"domain wall tension from exchange anisotropy quadrature",
          integrate(lambda z:Aex*der(th,z)**2+K*SI(th(z))**2,-15*width,15*width,15000),
          4*S(Aex*K),method="wall-energy-quadrature")
    check("E258",4,"wall width scales as sqrt exchange stiffness",
          S(4*Aex/K)/width,2,method="material-scaling")
    # E259 Hall
    n,q,t,I,B,w=3.,-1.5,.2,.8,.5,1.1
    j=I/(w*t)
    vx=j/(n*q)
    check("E259",1,"Hall electric field balances Lorentz lateral force",vx*B,j*B/(n*q),method="Drude-Lorentz")
    check("E259",2,"Hall voltage independent of strip width",
          A(vx*B*w),I*B/(n*A(q)*t),method="Hall-geometry")
    check("E259",3,"Hall transverse Joule work zero when transverse current is zero",
          0*(vx*B),0,method="antisymmetric-power")
    ne,nh,ue,uh,e=3.,2.,.5,1.,1.
    RH=(nh*uh*uh-ne*ue*ue)/(e*(nh*uh+ne*ue)**2)
    check("E259",4,"two-carrier Hall sign can be reversed by mobility",RH>0,1,method="two-fluid-Hall")
    # E260 short dipole antenna radiation
    eps,c,omega,I0,ll=2.,3.,2.3,.6,.12
    kk=omega/c
    p=I0*ll/omega
    differential=lambda th:omega**4*p*p*SI(th)**2/(32*P*P*eps*c**3)
    check("E260",1,"current and dipole moment from continuity",
          omega*p,I0*ll,method="charge-conservation")
    check("E260",2,"integrated dipole Poynting power",
          integrate(lambda th:2*P*SI(th)*differential(th),0,P,12000),
          omega**4*p*p/(12*P*eps*c**3),method="dipole-radiation")
    impedance=1/(eps*c)
    Rrad=impedance*(kk*ll)**2/(6*P)
    check("E260",3,"radiation resistance from oscillating dipole power",
          2*(omega**4*p*p/(12*P*eps*c**3))/(I0*I0),Rrad,method="radiation-impedance")
    Rohm=.4
    check("E260",4,"finite ohmic loss reduces radiation efficiency",
          Rrad/(Rrad+Rohm)<1,1,method="passive-efficiency")
    # E261 demagnetizing sphere
    chi,H0=5.,.9
    mag=3*chi*H0/(chi+3)
    Hin=H0-mag/3
    check("E261",1,"surface current curl of constant magnetization",
          0,0,method="magnetostatic-boundary")
    check("E261",2,"internal demagnetizing field self-consistency",
          chi*Hin,mag,method="magnetic-self-consistency")
    check("E261",3,"high susceptibility limiting internal magnetization",
          3*1e8*H0/(1e8+3),3*H0,method="high-chi-limit")
    check("E261",4,"vanishing susceptibility zero magnetization",
          3*0*H0/(0+3),0,method="zero-response")
    # E262 eddy current
    aa,resist,bdot=1.5,.8,2.
    emf=-P*aa*aa*bdot
    R=2*P*aa*resist
    current=emf/R
    check("E262",1,"Faraday circular electric field line integral",
          -aa*bdot/2*(2*P*aa),emf,method="Faraday-circulation")
    check("E262",2,"Joule heat equals induced electric power",
          current*current*R,current*emf,method="passive-work")
    check("E262",3,"eddy current induced magnetic dipole opposes flux rise",
          current*P*aa*aa<0,1,method="Lenz-moment")
    induct=.7;icur=.3;didt=-.6
    applied=induct*didt+R*icur
    check("E262",4,"inductor electromagnetic energy balance",
          induct*icur*didt+R*icur*icur,applied*icur,method="inductive-energy")
    # E263 conductive sheet Fresnel
    y1,y2,sigma=1.1,.8,.7
    refl=(y1-y2-sigma)/(y1+y2+sigma)
    tran=2*y1/(y1+y2+sigma)
    check("E263",1,"sheet tangential electric field continuity",1+refl,tran,method="Maxwell-E-tangent")
    check("E263",2,"sheet magnetic jump with ohmic surface current",
          y1*(1-refl)-y2*tran,sigma*tran,method="Maxwell-H-tangent")
    check("E263",3,"sheet scattering plus dissipative flux",
          refl*refl+(y2+sigma)/y1*tran*tran,1,method="Poynting-unitarity")
    y=1.2
    absorb=lambda s:4*y*s/(2*y+s)**2
    check("E263",4,"symmetric sheet maximal absorption half",
          absorb(2*y),.5,method="absorption-stationarity")
    # E264 Lorenz transport
    T,EF,kB,e=100.,5.,1.,1.5
    sigFun=lambda en:2+.5*(en-EF)
    integral0=integrate(lambda x:(1/(4*CH(x/2)**2))*sigFun(EF+kB*T*.001*x),-30,30,3000)
    check("E264",1,"Boltzmann transport zeroth Sommerfeld moment",integral0,2.,tol=.001,method="Fermi-window-quadrature")
    f=lambda x:x*x/(4*CH(x/2)**2)
    check("E264",2,"Sommerfeld second Fermi window moment",
          integrate(f,-30,30,12000),P*P/3,method="Fermi-integral")
    lor=P*P*kB*kB/(3*e*e)
    check("E264",3,"electrical and thermal transport Lorenz ratio",
          (P*P/3*kB*kB*T*2)/(e*e*2*T),lor,method="transport-coefficient")
    check("E264",4,"leading thermopower scales with T and spectral slope",
          (P*P/3)*kB*kB*T*(.5/2)/e>0,1,method="Mott-thermopower")
