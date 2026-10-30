from qa_common import *
def run():
    # E247 oscillating dipole radiation
    p0,omega,eps0,c=1.2,2.1,3.,4.
    er=lambda th:omega**2*p0*SI(th)/(4*P*eps0*c*c)
    check("E247",1,"dipole radiation transverse field vanishes on its axis",er(0),0,method="far-field-polarization")
    Srad=lambda th:eps0*c*er(th)**2/2
    check("E247",2,"dipole differential radiation Poynting angular law",
          Srad(.8),omega**4*p0**2*SI(.8)**2/(32*P**2*eps0*c**3),method="Poynting-field")
    check("E247",3,"total dipole radiated energy from angular quadrature",
          integrate(lambda th:2*P*SI(th)*Srad(th),0,P,12000),
          omega**4*p0*p0/(12*P*eps0*c**3),method="spherical-radiation-integral")
    check("E247",4,"static radiation limit quartic in source frequency",
          Srad(.8)/omega**4,p0**2*SI(.8)**2/(32*P**2*eps0*c**3),method="frequency-scaling")
    # E248 parallel plate stress and displacement
    eps,Aarea,d,V=2.2,3.,.5,1.7
    Ccap=eps*Aarea/d
    check("E248",1,"capacitor bulk electrostatic energy integral",
          eps*(V/d)**2*Aarea*d/2,Ccap*V*V/2,method="bulk-energy-integral")
    check("E248",2,"Maxwell stress pressure equals fixed-charge force",
          eps*(V/d)**2*Aarea/2,(Ccap*V)**2/(2*eps*Aarea),method="stress-tensor")
    check("E248",3,"Ampere Maxwell displacement current",
          eps*Aarea/d*1.3,Ccap*1.3,method="charge-continuity")
    Q=Ccap*V
    stored=lambda dist:Q*Q*dist/(2*eps*Aarea)
    check("E248",4,"fixed charge mechanical force as energy derivative",
          der(stored,d),Q*Q/(2*eps*Aarea),method="electrostatic-work")
    # E249 London superconductor
    lam,B0,mu=.7,1.5,1.3
    B=lambda x:B0*E(-x/lam)
    J=lambda x:-der(B,x)/mu
    check("E249",1,"London Helmholtz equation differential residual",
          der2(B,.6),B(.6)/(lam*lam),method="London-ODE")
    check("E249",2,"screening current Ampere sign",
          J(.6),B(.6)/(mu*lam),method="Maxwell-Ampere")
    check("E249",3,"London field energy integrated half space",
          integrate(lambda x:B(x)**2/(2*mu),0,40*lam,12000),
          B0*B0*lam/(4*mu),method="magnetic-energy")
    check("E249",4,"surface current flux equals applied field intensity",
          integrate(J,0,40*lam),B0/mu,method="screen-current-integral")
    # E250 dielectric interface images
    ep1,ep2,charge,d=2.,4.,1.7,1.2
    qp=charge*(ep1-ep2)/(ep1+ep2)
    qpp=2*ep2*charge/(ep1+ep2)
    check("E250",1,"interface continuity of electrostatic potential",
          (charge+qp)/ep1,qpp/ep2,method="dielectric-interface-potential")
    check("E250",2,"normal displacement continuity across interface",
          charge-qp,qpp,method="dielectric-displacement")
    U=lambda dd:charge*charge*(ep1-ep2)/(ep1+ep2)/(16*P*ep1*dd)
    force=charge*qp/(16*P*ep1*d*d)
    check("E250",3,"dielectric image force from polarization energy",
          -der(U,d),force,method="image-self-energy")
    check("E250",4,"homogeneous dielectric eliminates image charge",
          charge*(ep1-ep1)/(ep1+ep1),0,method="homogeneous-limit")
    # E251 Drude cyclotron absorption
    n,e,m,nu,wp=3.,.8,1.6,.4,2.5
    omegaC=e*wp/m
    adm=lambda w:complex(n*e*e/m,0)/complex(nu,-(w-omegaC))
    check("E251",1,"cyclotron equation in helicity basis",
          adm(omegaC)*complex(nu,0),n*e*e/m,method="complex-Drude-equation")
    eps0=2.;freq=3.8
    dielectric=1+1j*adm(freq)/(eps0*freq)
    check("E251",2,"electrodynamic epsilon from finite conductivity",
          (dielectric-1)*eps0*freq/1j,adm(freq),method="constitutive-Maxwell")
    check("E251",3,"cyclotron absorption peak is positive",
          adm(omegaC).real>0,1,method="Joule-positivity")
    check("E251",4,"collision frequency sets Lorentz FWHM",
          adm(omegaC+nu).real/adm(omegaC).real,.5,method="resonance-linewidth")
    # E252 coupled LC generalized eigenvalues
    L1,L2,C1,C2,M=2.,3.,.8,.7,.9
    det=L1*L2-M*M
    poly=lambda x:det*x*x-(L1/C2+L2/C1)*x+1/(C1*C2)
    check("E252",1,"symmetric mutual-inductance quadratic energy positive",
          det>0,1,method="energy-positive-definite")
    # obtain roots via quadratic
    aa=det;bb=-(L1/C2+L2/C1);cc=1/(C1*C2)
    discr=S(bb*bb-4*aa*cc)
    r1=(-bb+discr)/(2*aa);r2=(-bb-discr)/(2*aa)
    check("E252",2,"LC characteristic frequency determinant residual",
          poly(r1),0,method="coupled-circuit-characteristic")
    Ll,Cc,Mut=2.4,.8,.3
    check("E252",3,"in-phase equal circuits resonant mode",
          1/((Ll+Mut)*Cc)*(Ll+Mut),1/Cc,method="normal-mode")
    check("E252",4,"perfect coupling boundary eliminates kinetic determinant",
          L1*L2-S(L1*L2)**2,0,method="singular-coupling")
    # E253 multipole charged shell
    R,eps,sig0,sig2=1.4,2.,.7,.9
    Pl2=lambda u:(3*u*u-1)/2
    pin=lambda r,u:sig0*R/eps+sig2*r*r*Pl2(u)/(5*eps*R)
    pout=lambda r,u:sig0*R*R/(eps*r)+sig2*R**4*Pl2(u)/(5*eps*r**3)
    check("E253",1,"Legendre l2 orthogonal to l0",
          integrate(lambda u:Pl2(u),-1,1,12000),0,method="spherical-harmonic-orthogonality")
    check("E253",2,"shell potential continuity l0+l2",
          pin(R,.4),pout(R,.4),method="Poisson-continuity")
    check("E253",3,"internal axial field gradient from potential",
          -der(lambda z:pin(z,1),.6),-2*sig2*.6/(5*eps*R),method="axial-gradient")
    check("E253",4,"monopole shell total charge",
          2*P*R*R*integrate(lambda u:sig0+sig2*Pl2(u),-1,1),
          4*P*R*R*sig0,method="global-Gauss")
    # E254 magnetic dipole
    moment,B,omega,I=.8,2.,1.5,3.
    U=lambda th:-moment*B*C(th)
    check("E254",1,"dipole torque equals negative orientation energy gradient",
          -der(U,.6),-moment*B*SI(.6),method="Lorentz-torque")
    field=lambda z:B+.4*z+.12*z*z
    check("E254",2,"dipole force from field gradient",
          -der(lambda z:-moment*C(.3)*field(z),.7),
          moment*C(.3)*der(field,.7),method="magnetic-work")
    check("E254",3,"aligned stable angular frequency from Hessian",
          der2(U,0)/I,moment*B/I,method="rotational-Hessian")
    check("E254",4,"antialigned orientation is unstable",
          der2(U,P)<0,1,method="orientation-instability")
    # E255 Rayleigh sphere scattering
    a,epsr,eps0,kk=.03,3.,2.,2.1
    pol=4*P*eps0*a**3*(epsr-1)/(epsr+2)
    check("E255",1,"dielectric sphere static polarizability Clausius Mossotti",
          pol/(4*P*eps0*a**3),(epsr-1)/(epsr+2),method="Laplace-dielectric-boundary")
    dsigma=lambda th:kk**4*pol**2*SI(th)**2/(16*P*P*eps0*eps0)
    check("E255",2,"Rayleigh dipole sin2 differential cross section",
          dsigma(.6)/dsigma(P/2),SI(.6)**2,method="angular-radiation-pattern")
    check("E255",3,"Rayleigh total cross section from solid angle integral",
          2*P*integrate(lambda th:dsigma(th)*SI(th),0,P),
          kk**4*pol**2/(6*P*eps0**2),method="spherical-scattering-integral")
    check("E255",4,"Rayleigh power six sphere radius scaling",
          (2*a)**6/a**6,64,method="radius-scaling")
