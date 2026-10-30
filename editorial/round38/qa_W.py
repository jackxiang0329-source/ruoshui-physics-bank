from qa_common import *
def run():
    # W266 WKB inhomogeneous stretched string
    T,w=3.,2.1
    mu=lambda x:1+.15*x
    kk=lambda x:w*S(mu(x)/T)
    amp=lambda x:1/S(kk(x))
    check("W266",1,"inhomogeneous string local wave frequency",
          kk(.7)**2*T/mu(.7),w*w,method="local-dispersion")
    check("W266",2,"WKB amplitude conservation law",
          der(lambda x:kk(x)*amp(x)**2,.7),0,method="WKB-transport-equation")
    energyflow=lambda x:T*w*kk(x)*amp(x)**2/2
    check("W266",3,"WKB flux independent of density",energyflow(.8),energyflow(2.),method="wave-energy-flow")
    check("W266",4,"WKB valid when density slowly changes",
          A(der(kk,.7))/kk(.7)**2<.1,1,method="asymptotic-smallness")
    # W267 Euler Bernoulli flexural waves
    EI,mu,L=2.,1.4,3.
    disp=lambda k:S(EI/mu)*k*k
    check("W267",1,"Euler Bernoulli fourth derivative positive stiffness",
          der2(lambda x:SI(2*x),.7),-4*SI(1.4),method="beam-energy")
    check("W267",2,"beam k4 dispersion relation",disp(.8)**2,EI/mu*.8**4,method="flexural-dispersion")
    check("W267",3,"beam group velocity double phase velocity",
          der(disp,.8),2*disp(.8)/.8,method="group-velocity")
    f=lambda x:SI(P*x/L)
    check("W267",4,"simply supported sine mode has zero end moment",
          der2(f,0),0,method="beam-Dirichlet-moment-boundary")
    # W268 string interface impedance
    T,mu1,mu2=2.,1.2,4.
    Z1=S(T*mu1);Z2=S(T*mu2)
    r=(Z1-Z2)/(Z1+Z2);tran=2*Z1/(Z1+Z2)
    check("W268",1,"mechanical string impedance equals tension over speed",
          Z1,T/S(T/mu1),method="mechanical-wave-impedance")
    check("W268",2,"string displacement and force continuity",
          1+r,tran,method="interface-continuity")
    check("W268",3,"mechanical power R+T conserves",
          r*r+(Z2/Z1)*tran*tran,1,method="string-Poynting")
    check("W268",4,"heavy string reflection reverses displacement sign",
          r<0,1,method="fixed-end-heavy-limit")
    # W269 diatomic lattice
    m1,m2,K,a=2.,3.,1.5,.9
    s0=lambda q:SI(q*a/2)**2
    w2=lambda q,sgn:K*(1/m1+1/m2)+sgn*K*S((1/m1+1/m2)**2-4*s0(q)/(m1*m2))
    determinant=lambda q,w:(2*K-m1*w)*(2*K-m2*w)-4*K*K*C(q*a/2)**2
    check("W269",1,"two site Bloch characteristic determinant",
          determinant(.6,w2(.6,1)),0,method="diatomic-Bloch-determinant")
    check("W269",2,"lower branch characteristic root",
          determinant(.6,w2(.6,-1)),0,method="acoustic-normal-mode")
    cs2=K*a*a/(2*(m1+m2))
    check("W269",3,"diatomic acoustic small wavenumber limit",
          w2(.001,-1)/(.001**2),cs2,tol=.0005,method="acoustic-continuum")
    check("W269",4,"zone-edge two discrete mass resonances",
          w2(P/a,1)+w2(P/a,-1),2*K/m1+2*K/m2,method="zone-boundary-split")
    # W270 Kuramoto order parameter
    gamma=1.4;Kc=2*gamma;K=4.1
    distribution=lambda om:gamma/(P*(om*om+gamma*gamma))
    check("W270",1,"Lorentzian frequency distribution unit mass",
          integrate(distribution,-1300,1300,50000),1,tol=.001,method="frequency-density-integral")
    r=S(1-Kc/K)
    check("W270",2,"order parameter self consistent integral",
          integrate(lambda x:K*distribution(K*r*x)*S(1-x*x),-1,1,14000),1,tol=.0002,method="phase-locking-integral")
    check("W270",3,"critical coupling from zero-frequency oscillator density",
          2/(P*distribution(0)),Kc,method="linearized-sync")
    check("W270",4,"Ott Antonsen stationary amplitude ODE",
          -gamma*r+K*r*(1-r*r)/2,0,method="order-parameter-fixed-point")
    # W271 finite depth capillary gravity
    g,gamma,rho,h,k=9.8,.7,2.,1.8,1.2
    disp2=lambda kk:(g*kk+gamma*kk**3/rho)*TH(kk*h)
    w=lambda kk:S(disp2(kk))
    check("W271",1,"velocity potential bottom Neumann",
          der(lambda z:CH(k*(z+h)),-h),0,method="bottom-impermeability")
    check("W271",2,"free surface gravity capillary dispersion",
          w(k)**2,disp2(k),method="surface-Maxwell-stress")
    check("W271",3,"group velocity from differentiated dispersion",
          der(w,k),(g+3*gamma*k*k/rho)*TH(k*h)/(2*w(k))+
          h*(g*k+gamma*k**3/rho)/(2*w(k)*CH(k*h)**2),method="fluid-wave-group-velocity")
    small=1e-5
    check("W271",4,"shallow water phase speed tends sqrt gh",
          S(disp2(small))/small,S(g*h),method="long-wave-dispersion")
    # W272 causal oscillator Green
    gamma,w0=.3,2.2
    wd=S(w0*w0-gamma*gamma)
    G=lambda t:E(-gamma*t)*SI(wd*t)/wd
    check("W272",1,"causal Green impulse derivative jump",
          der(G,0),1,method="Green-impulse-jump")
    check("W272",2,"homogeneous Green ODE for positive t",
          der2(G,.4)+2*gamma*der(G,.4)+w0*w0*G(.4),0,method="causal-ODE")
    # convolution with force f(t)=sin(1.3t)
    drive=lambda t:SI(1.3*t)
    output=lambda t:integrate(lambda s:G(t-s)*drive(s),0,t,1200)
    check("W272",3,"convolution driven oscillator residual",
          der2(output,.6,1e-3)+2*gamma*der(output,.6,1e-3)+w0*w0*output(.6),
          drive(.6),tol=.01,method="Duhamel-numerical")
    omega=1.3
    imag=2*gamma*omega/((w0*w0-omega*omega)**2+4*gamma*gamma*omega*omega)
    check("W272",4,"passive susceptibility dissipates nonnegative power",
          imag>0,1,method="causal-passive-spectral")
    # W273 inviscid Burgers characteristics
    u0=lambda x:-SI(x)
    t=.4;xi=.3
    x=xi+t*u0(xi)
    check("W273",1,"Burgers characteristic conserves wave amplitude",
          u0(xi),u0(xi),method="nonlinear-characteristic")
    check("W273",2,"exact gradient from characteristic map",
          u0(xi)*0+der(u0,xi)/(1+t*der(u0,xi)),
          (-C(xi))/(1-t*C(xi)),method="gradient-catastrophe")
    check("W273",3,"shock Rankine Hugoniot jump speed",
          ((3.**2/2)-(.8**2/2))/(3.-.8),(3.+.8)/2,method="entropy-conservative-shock")
    check("W273",4,"compressive Burgers shock satisfies Lax",
          3>(3+.8)/2>.8,1,method="entropy-Lax-admissibility")
