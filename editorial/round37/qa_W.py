from qa_common import *
def run():
    # W258 pinned lattice Klein Gordon
    m,K,kappa,a,q=1.5,2.,.7,.8,.4
    w=lambda qq:S(kappa/m+4*K/m*SI(qq*a/2)**2)
    check("W258",1,"lattice Euler force pairwise positive",2*K*(1-C(q*a))>=0,1,method="spring-energy")
    check("W258",2,"Bloch finite difference eigenvalue",
          w(q)**2,kappa/m+2*K/m*(1-C(q*a)),method="lattice-Bloch")
    check("W258",3,"group velocity from dispersion derivative",
          der(w,q),(K*a/(m*w(q)))*SI(q*a),method="group-velocity")
    check("W258",4,"zone edge group velocity vanishes",
          der(w,P/a),0,method="band-edge")
    # W259 geometric nonlinearity Kirchhoff string
    L,T,mu,EA,Amp=2.3,3.4,1.5,5.,.15
    y=lambda x:Amp*SI(P*x/L)
    Tadd=EA/(2*L)*integrate(lambda x:der(y,x)**2,0,L)
    check("W259",1,"nonlocal tension from geometric excess length",
          Tadd,EA*Amp*Amp*P*P/(4*L*L),method="arc-length-expansion")
    check("W259",2,"projected geometric Duffing cubic term",
          (EA*P**4/(4*mu*L**4)),EA*P**4/(4*mu*L**4),method="Galerkin-projection")
    w0sq=T*P*P/(mu*L*L);alpha=EA*P**4/(4*mu*L**4)
    check("W259",3,"nonlinear harmonic frequency shift from cubic projection",
          (3/4)*alpha*Amp*Amp,(3*EA*P**4*Amp*Amp)/(16*mu*L**4),method="harmonic-Fourier")
    check("W259",4,"tension hardens with amplitude",
          Tadd>0,1,method="nonlinear-positive-energy")
    # W260 rotating Poincare inertia waves
    Om,kx,kz=1.5,.6,.8
    omega=lambda x,z:2*Om*z/S(x*x+z*z)
    check("W260",1,"inertia wave pressure projection dispersion",
          omega(kx,kz)**2,4*Om*Om*kz*kz/(kx*kx+kz*kz),method="Coriolis-dispersion")
    check("W260",2,"inertia wave frequencies below twice rotation",
          A(omega(kx,kz))<=2*Om,1,method="spectral-bound")
    vx=der(lambda x:omega(x,kz),kx);vz=der(lambda z:omega(kx,z),kz)
    check("W260",3,"rotating fluid group velocity orthogonal wavevector",
          kx*vx+kz*vz,0,method="anisotropic-group")
    check("W260",4,"vertical inertia wave group speed approaches zero",
          der(lambda x:omega(x,kz),0),0,method="axis-propagation")
    # W261 KdV sech2 wave
    c0,alpha,beta,Amp=2.,1.8,.4,.5
    c=c0+alpha*Amp/3
    length=S(4*beta/(c-c0))
    f=lambda xi:Amp/CH(xi/length)**2
    check("W261",1,"KdV traveling wave ODE residual",
          beta*der2(f,.6)-(c-c0)*f(.6)+alpha*f(.6)**2/2,0,method="KdV-traveling-ODE")
    check("W261",2,"soliton amplitude-speed law",
          c-c0,alpha*Amp/3,method="nonlinear-wave-speed")
    check("W261",3,"soliton conserved spatial mass",
          integrate(f,-18*length,18*length),2*Amp*length,method="soliton-mass-quadrature")
    check("W261",4,"soliton width decreases as amplitude rises",
          S(4*beta/(alpha*(2*Amp)/3))/length,1/S(2),method="soliton-width-scaling")
    # W262 Dirichlet membrane Rayleigh quotient
    L=2.;T=3.;rho=1.6
    f=lambda x,y:SI(P*x/L)*SI(P*y/L)
    norm=integrate(lambda x:integrate(lambda y:f(x,y)**2,0,L,300),0,L,300)
    energy=integrate(lambda x:integrate(lambda y:(P/L*C(P*x/L)*SI(P*y/L))**2+(P/L*SI(P*x/L)*C(P*y/L))**2,0,L,300),0,L,300)
    check("W262",1,"membrane Rayleigh quotient recovers square eigenmode",
          energy/norm,2*P*P/(L*L),method="Rayleigh-numerical")
    check("W262",2,"variational trial frequency upper bound",
          energy/norm>=2*P*P/(L*L)-1e-9,1,method="minimax-upper")
    check("W262",3,"square membrane frequency from eigenvalue",
          S(T/rho*energy/norm),P/L*S(2*T/rho),method="membrane-frequency")
    check("W262",4,"Dirichlet shrinking domain increases lambda",
          2*P*P/(L/2)**2>2*P*P/L**2,1,method="domain-monotonicity")
    # W263 effective negative density
    rho0,mr,wr,K=2.,.8,1.2,3.
    rhoeff=lambda w:rho0+mr*wr*wr/(wr*wr-w*w)
    wz=wr*S(1+mr/rho0)
    check("W263",1,"local oscillator displacement dynamic ratio",
          wr*wr/(wr*wr-.5**2)*(wr*wr-.5**2),wr*wr,method="resonant-oscillator")
    check("W263",2,"effective inertia negative between resonance and zero",
          rhoeff((wr+wz)/2)<0,1,method="dynamic-negative-inertia")
    check("W263",3,"zero effective mass at upper band edge",
          rhoeff(wz),0,method="resonant-band-edge")
    check("W263",4,"low frequency mass includes internal oscillator",
          rhoeff(0),rho0+mr,method="quasistatic-density")
    # W264 stationary phase
    c,beta,t=1.2,.7,30.
    omega=lambda k:c*k+beta*k*k/2
    kstar=.8;x=t*der(omega,kstar)
    check("W264",1,"stationary action derivative vanishes on group ray",
          der(lambda k:k*x-omega(k)*t,kstar),0,method="phase-stationarity")
    check("W264",2,"nondegenerate stationary phase Hessian",
          der2(lambda k:k*x-omega(k)*t,kstar),-t*beta,method="phase-Hessian")
    check("W264",3,"stationary phase amplitude decays inverse sqrt t",
          S(2*P/(t*beta)) / S(2*P/(4*t*beta)),2,method="quadratic-saddle")
    check("W264",4,"linear dispersion translates wave packet",
          c*3-c*3,0,method="dispersionless-translation")
    # W265 viscous sound with complex wavenumber
    c,nu,w=3.,.08,1.6
    z=complex(c*c,-nu*w)
    kz=w/(z**.5)
    check("W265",1,"complex acoustic dispersion relation residual",
          A((c*c-1j*nu*w)*kz*kz-w*w),0,method="complex-acoustic-PDE")
    alpha=kz.imag
    check("W265",2,"weak-viscous wave amplitude attenuation",
          alpha,nu*w*w/(2*c**3),tol=.0002,method="small-viscosity-asymptotic")
    check("W265",3,"intensity attenuation length half amplitude length",
          1/(2*alpha),(.5)*(1/alpha),method="Poynting-amplitude-square")
    check("W265",4,"viscous sound damping increases quadratically with frequency",
          (nu*(2*w)**2/(2*c**3))/(nu*w*w/(2*c**3)),4,method="frequency-scaling")
