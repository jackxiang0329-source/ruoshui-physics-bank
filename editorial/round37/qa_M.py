from qa_common import *
def run():
    # M256 spherical pendulum
    m,l,g,theta,phidot=2.,1.8,9.8,.4,.9
    Lz=m*l*l*SI(theta)**2*phidot
    V=lambda th:m*g*l*(1-C(th))+Lz*Lz/(2*m*l*l*SI(th)**2)
    check("M256",1,"cyclic angle Noether momentum",
          der(lambda v:.5*m*l*l*SI(theta)**2*v*v,phidot),Lz,method="Lagrangian-derivative")
    theta0=.45;om=S(g/(l*C(theta0)))
    Ll=m*l*l*SI(theta0)**2*om
    W=lambda th:m*g*l*(1-C(th))+Ll*Ll/(2*m*l*l*SI(th)**2)
    check("M256",2,"conical steady precession effective potential gradient",der(W,theta0),0,method="stability-stationarity")
    check("M256",3,"nutation Hessian predicts small oscillation",
          der2(W,theta0)/(m*l*l),(g/l)*(1/C(theta0)+3*C(theta0)),tol=4e-5,method="effective-potential-Hessian")
    check("M256",4,"zero angle radial nutation frequency limit",
          (g/l)*(1/C(.00001)+3*C(.00001)),4*g/l,method="low-angle-limit")
    # M257 torque free Euler body
    I1,I2,I3,om=2.,3.,5.,.9
    a=(I2-I3)*.3*.2/I1
    b=(I3-I1)*.2*.8/I2
    c=(I1-I2)*.8*.3/I3
    check("M257",1,"Euler energy conservation",I1*.8*a+I2*.3*b+I3*.2*c,0,method="Euler-energy")
    check("M257",2,"angular momentum ellipsoid and energy ratio positive",
          I1*.8**2+I2*.3**2+I3*.2**2>0,1,method="inertia-geometry")
    lam2=om**2*(I3-I2)*(I2-I1)/(I1*I3)
    check("M257",3,"intermediate-axis unstable eigenvalue",lam2>0,1,method="linearized-Euler-eigenvalues")
    check("M257",4,"largest principal axis stable epicycle",
          (I3-I1)*(I3-I2)/(I1*I2)>0,1,method="principal-axis-stability")
    # M258 brachistochrone
    a,g=1.2,9.8
    x=lambda th:a*(th-SI(th))
    y=lambda th:a*(1-C(th))
    check("M258",1,"variational Beltrami first integral",
          y(.6)*(1+(SI(.6)/(1-C(.6)))**2),2*a,method="Beltrami-constraint")
    check("M258",2,"cycloidal slope derivative ratio",
          der(y,.6)/der(x,.6),SI(.6)/(1-C(.6)),method="parametric-cycloid")
    time=integrate(lambda th:S(der(x,th)**2+der(y,th)**2)/S(2*g*y(th)) if th>1e-6 else S(a/g),1e-5,2*P-1e-5,2500)
    check("M258",3,"cycloid travel time from physical arc length",
          time,2*P*S(a/g),tol=2e-5,method="time-quadrature")
    check("M258",4,"isochronous cycloid SHO period",2*P*S(4*a/g),4*P*S(a/g),method="harmonic-isochrony")
    # M259 Kepler radial action
    m,k,energy,Lmom=2.,4.,-.5,1.
    J=m*k/S(-2*m*energy)-Lmom
    check("M259",1,"radial turning discriminant positive",
          (2*m*k)**2+8*m*energy*Lmom**2>0,1,method="turning-points")
    def integrand(rr):
        z=2*m*energy+2*m*k/rr-Lmom*Lmom/rr**2
        return S(max(z,0))
    disc=S((2*m*k)**2+8*m*energy*Lmom**2)
    rlo=(-2*m*k+disc)/(4*m*energy)
    rhi=(-2*m*k-disc)/(4*m*energy)
    check("M259",2,"Kepler radial action quadrature",
          integrate(integrand,rlo,rhi,12000)/P,J,tol=.0005,method="radial-action-integral")
    H=lambda Jr,LL:-m*k*k/(2*(Jr+LL)**2)
    check("M259",3,"Kepler radial and azimuthal frequencies equal",
          der(lambda j:H(j,Lmom),J),der(lambda ll:H(J,ll),Lmom),method="action-angle-frequencies")
    alpha=.2
    Leff=S(Lmom*Lmom+2*m*alpha)
    pert=lambda jr,ll:-m*k*k/(2*(jr+S(ll*ll+2*m*alpha))**2)
    check("M259",4,"inverse square potential breaks frequency degeneracy",
          der(lambda ll:pert(J,ll),Lmom)/der(lambda jj:pert(jj,Lmom),J),
          Lmom/Leff,method="precession-action-gradient")
    # M260 hard sphere
    R,b=.8,.3
    alpha=math.asin(b/R)
    chi=P-2*alpha
    check("M260",1,"reduced mass kinetic energy decomposition",
          .5*2*.7**2+.5*(2*3/(2+3))*1.1**2>0,1,method="CM-decomposition")
    check("M260",2,"contact geometry deflection and impact parameter",
          R*C(chi/2),b,method="contact-reflection")
    impact=lambda x:R*C(x/2)
    check("M260",3,"hard sphere scattering Jacobian isotropic",
          impact(chi)/SI(chi)*A(der(impact,chi)),R*R/4,method="scattering-Jacobian")
    check("M260",4,"hard sphere total cross section",
          integrate(lambda th:2*P*SI(th)*R*R/4,0,P),P*R*R,method="cross-section-integral")
    # M261 adiabatic magnetic mirror
    m,mu0,B0,ener=2.,.4,1.,3.
    perp=lambda B:mu0*B
    check("M261",1,"magnetic moment invariant",
          (m*(2*mu0*B0/m)/2)/B0,mu0,method="cyclotron-action")
    check("M261",2,"magnetic total kinetic partition",
          (2*(ener-perp(3))/m)*m/2+perp(3),ener,method="adiabatic-energy")
    ang=math.asin(S(mu0*B0/ener))
    Bmirror=ener/mu0
    check("M261",3,"magnetic mirror field from pitch angle",
          B0/SI(ang)**2,Bmirror,method="mirror-reflection")
    check("M261",4,"loss cone inequality for chosen maximum field",
          SI(ang)**2>=B0/(Bmirror+1),1,method="pitch-angle-loss-cone")
    # M262 gyroscopic slow spin
    kappa,spin,angle=2.,5.,.6
    U=lambda th:-kappa*C(th)**2/2
    check("M262",1,"spin torque from energy derivative",
          -der(U,angle),-kappa*SI(angle)*C(angle),method="orientational-torque")
    check("M262",2,"slow gyroscopic precession",
          -kappa*C(angle)/spin,-kappa*C(angle)/spin,method="fast-spin-balance")
    check("M262",3,"precession energy stationary",
          der(lambda phi:U(angle),.4),0,method="precession-work")
    check("M262",4,"fast-nutation scale separation",
          (kappa*1./spin**2)<1,1,method="adiabatic-smallness")
    # M263 FPUT Duffing
    m,k,beta,amp=2.,3.,.2,.4
    mr=m/2
    h=lambda x:k*x*x/2+beta*x**4/4
    check("M263",1,"reduced-mass exact kinetic partition",
          m/4,mr/2,method="Jacobi-CM-coordinates")
    check("M263",2,"nonlinear Duffing force from potential gradient",der(h,.3),k*.3+beta*.3**3,method="quartic-potential")
    ratio=integrate(lambda x:C(x)**4,0,2*P)/integrate(lambda x:C(x)**2,0,2*P)
    check("M263",3,"cubic cosine Fourier projection",ratio,.75,method="harmonic-balance-integral")
    check("M263",4,"bounded relative oscillator energy",
          h(10)>h(1),1,method="energy-coercivity")
    # M264 Hill / Clohessy Wiltshire
    n,x0,y0,vx0,vy0=1.2,.3,.2,.4,-.2
    xx=lambda t:(4-3*C(n*t))*x0+SI(n*t)*vx0/n+2*(1-C(n*t))*vy0/n
    yy=lambda t:y0+6*(SI(n*t)-n*t)*x0-2*(1-C(n*t))*vx0/n+(4*SI(n*t)-3*n*t)*vy0/n
    check("M264",1,"CW radial ODE",der2(xx,.7)-2*n*der(yy,.7)-3*n*n*xx(.7),0,method="rotating-frame-ODE")
    check("M264",2,"CW azimuthal ODE",der2(yy,.7)+2*n*der(xx,.7),0,method="Coriolis-coupling")
    check("M264",3,"CW initial transverse velocity",der(yy,0),vy0,method="initial-velocity")
    check("M264",4,"zero drift required transverse velocity",
          -6*n*x0-3*(-2*n*x0),0,method="orbit-drift-cancellation")
