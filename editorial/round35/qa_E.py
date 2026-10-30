from qa_common import *

def run():
    # E238 coaxial TEM transmission line
    eps,mu,aa,bb,lam,I=2.8,1.3,.5,2.1,1.7,.9
    Er=lambda r:lam/(2*P*eps*r)
    H=lambda r:I/(2*P*r)
    V=integrate(Er,aa,bb)
    Cline=2*P*eps/L(bb/aa);Lline=mu*L(bb/aa)/(2*P)
    check("E238",1,"coaxial Gauss voltage integral",V,lam/Cline,method="radial-electric-field")
    check("E238",2,"coaxial magnetic energy per length",
          integrate(lambda r:mu*H(r)**2/2*2*P*r,aa,bb),Lline*I**2/2,method="magnetic-energy-integral")
    check("E238",3,"TEM Poynting integral equals VI",
          integrate(lambda r:Er(r)*H(r)*2*P*r,aa,bb),V*I,method="Poynting-flux")
    check("E238",4,"TEM line product LC equals dielectric mu epsilon",
          Lline*Cline,mu*eps,method="geometry-cancellation")
    # E239 TE10 waveguide
    eps,mu,aa,omega=2.,1.4,3.,3.
    kc=P/aa;beta=S(omega*omega*eps*mu-kc*kc)
    check("E239",1,"Neumann transverse magnetic field derivative zero at wall",
          -(P/aa)*SI(P*aa/aa),0,method="boundary-condition")
    check("E239",2,"TE10 waveguide dispersion",
          beta*beta+kc*kc,omega*omega*mu*eps,method="Maxwell-eigenvalue")
    v=1/S(eps*mu);vp=omega/beta;vg=v*v*beta/omega
    check("E239",3,"waveguide phase group product",vp*vg,v*v,method="group-velocity")
    below=.5*kc/S(mu*eps)
    check("E239",4,"below TE cutoff longitudinal wavenumber imaginary",
          omega*0+kc*kc-below*below*mu*eps>0,1,method="cutoff-sign")
    # E240 moving bar
    m,R,Lc,B,ell,v,I,force=3.,2.,.8,1.1,1.3,2.,.5,1.4
    dv=(force-B*ell*I)/m;dI=(B*ell*v-R*I)/Lc
    check("E240",1,"motional emf Faraday circuit balance",Lc*dI+R*I,B*ell*v,method="Kirchhoff-Faraday")
    iss=B*ell*v/R
    check("E240",2,"steady motional power equals Joule power",
          B*ell*iss*v,R*iss*iss,method="generator-energy")
    check("E240",3,"freely damped bar e-fold time",
          m*R/(B*B*ell*ell),m/(B*B*ell*ell/R),method="zero-inductance-limit")
    check("E240",4,"mechanical plus magnetic energy rate",
          m*v*dv+Lc*I*dI,force*v-R*I*I,method="coupled-energy")
    # E241 cold plasma gyrotropic wave
    wp,Omega,w,c=.7,.25,5.,3.
    nplus=S(1-wp*wp/(w*(w-Omega)))
    nminus=S(1-wp*wp/(w*(w+Omega)))
    check("E241",1,"plasma cold R/L propagation at selected frequency",
          (nplus*nplus-1)*w*(w-Omega),-wp*wp,method="linear-electron-response")
    check("E241",2,"circular wave index splitting from two eigenvalues",
          nplus*nplus-nminus*nminus,
          -wp*wp/(w*(w-Omega))+wp*wp/(w*(w+Omega)),method="polarization-spectrum")
    kdiff=w*(nplus-nminus)/c
    check("E241",3,"high-frequency Faraday rotation leading expansion",
          kdiff,-wp*wp*Omega/(c*w*w),tol=.001,method="high-frequency-asymptotic")
    check("E241",4,"reversing B swaps circular branches",
          S(1-wp*wp/(w*(w+Omega))),nminus,method="magnetic-field-reversal")
    # E242 grounded sphere electrostatic image charge
    a,d,q,eps=1.2,3.,2.,2.4
    imageq=-q*a/d;zimg=a*a/d
    pot=lambda z:q/A(z-d)+imageq/A(z-zimg)
    check("E242",1,"image charges cancel grounded potential at sphere pole",
          pot(a),0,method="Dirichlet-boundary")
    force=-q*q*a*d/(4*P*eps*(d*d-a*a)**2)
    U=lambda dd:(q*(-q*a/dd)/(dd-a*a/dd))/(8*P*eps)
    check("E242",2,"image force from energy derivative",-der(U,d),force,tol=1e-6,method="image-energy-gradient")
    check("E242",3,"induced spherical total charge by Gauss flux",
          imageq,-q*a/d,method="Gauss-charge")
    d_far=50.*a
    force_far=-q*q*a*d_far/(4*P*eps*(d_far*d_far-a*a)**2)
    check("E242",4,"large separation attractive induced dipole force",
          force_far*d_far**3,-q*q*a/(4*P*eps),tol=.002,method="far-field-limit")
    # E243 one-band Drude Hall conductivity and resistivity
    density,q,tau,m,B=4.,-2.,.7,1.6,.8
    sigma0=density*q*q*tau/m
    mut=A(q)*tau/m;sg=-1.
    D=1+(mut*B)**2
    sigma_xx=sigma0/D;sigma_xy=sg*sigma0*mut*B/D
    # test conductivity inverse Hall rho
    det=sigma_xx*sigma_xx+sigma_xy*sigma_xy
    rho_xx=sigma_xx/det;rho_yx=sigma_xy/det
    check("E243",1,"Drude tensor derived from Lorentz mobility",sigma_xy/sigma_xx,sg*mut*B,method="velocity-response")
    check("E243",2,"single-band longitudinal magnetoresistance is zero",rho_xx,1/sigma0,method="tensor-inversion")
    check("E243",3,"Hall coefficient from inverse tensor",
          rho_yx/B,1/(density*q),method="Hall-sign")
    check("E243",4,"zero magnetic field restores scalar conductivity",
          sigma0/(1+0*B),sigma0,method="zero-field-limit")
    # E244 skin effect
    mu,sig,w=1.3,4.6,8.
    delt=S(2/(mu*sig*w))
    gamma=complex(1,-1)/delt
    check("E244",1,"diffusive conductor complex wave number",
          A(gamma*gamma-complex(0,-mu*sig*w)),0,method="complex-Maxwell")
    check("E244",2,"skin depth amplitude decay",
          A(math.e**(-3/delt*delt)),math.e**(-3),method="evanescence")
    rs=1/(sig*delt)
    check("E244",3,"surface resistance equals integrated Joule loss",
          sig*integrate(lambda z:E(-2*z/delt),0,30*delt)/2,
          sig*delt/4,method="Joule-depth-integral")
    check("E244",4,"skin depth decreases with square root frequency",
          S(2/(mu*sig*(4*w)))/delt,.5,method="high-frequency-scaling")
    # E245 depletion PN junction
    eps,q,NA,ND,Vbi,Vr=3.,2.,5.,8.,1.1,.6
    W=S(2*eps*(Vbi+Vr)/q*(1/NA+1/ND))
    xp=ND*W/(NA+ND);xn=NA*W/(NA+ND)
    check("E245",1,"depletion ion charge neutrality",NA*xp-ND*xn,0,method="charge-neutrality")
    peak=q*NA*xp/eps
    check("E245",2,"PN triangular Poisson potential drop",peak*W/2,Vbi+Vr,method="Poisson-field-integration")
    cap=lambda vol:eps/S(2*eps*(Vbi+vol)/q*(1/NA+1/ND))
    check("E245",3,"junction capacitance relates depletion charge derivative",
          der(lambda vol:q*NA*ND/(NA+ND)*S(2*eps*(Vbi+vol)/q*(1/NA+1/ND)),Vr),
          cap(Vr),method="differential-capacitance")
    check("E245",4,"reverse bias quadruples depletion voltage width doubles",
          S(2*eps*(4*(Vbi+Vr))/q*(1/NA+1/ND))/W,2,method="bias-scaling")
    # E246 Lorentz boost electromagnetic field invariants
    c=5.;EE=3.;BB=.9;u=2.
    gamma=1/S(1-u*u/(c*c))
    ep=gamma*(EE-u*BB);bp=gamma*(BB-u*EE/(c*c))
    check("E246",1,"boost transverse field transformations",
          ep/gamma,EE-u*BB,method="Lorentz-transform")
    check("E246",2,"Lorentz scalar E2-c2B2 invariant",
          ep*ep-c*c*bp*bp,EE*EE-c*c*BB*BB,method="field-tensor-invariant")
    Bdom=1.2;Eweak=2.;uc=Eweak/Bdom
    check("E246",3,"magnetic-dominant rest frame annihilates E",Eweak-uc*Bdom,0,method="magnetic-rest-frame")
    Estrong=7.;Bweak=.4;ue=c*c*Bweak/Estrong
    check("E246",4,"electric-dominant rest frame annihilates B",
          Bweak-ue*Estrong/(c*c),0,method="electric-rest-frame")
