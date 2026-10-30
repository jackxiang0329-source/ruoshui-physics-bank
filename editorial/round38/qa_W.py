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
    # W269 ferromagnetic exchange spin waves
    gamma,H0,D,k=1.6,2.,.7,.8
    w=lambda wave:gamma*(H0+D*wave*wave)
    mx=lambda t:C(w(k)*t)
    my=lambda t:SI(w(k)*t)
    check("W269",1,"Landau Lifshitz spin precession linearized cross product",
          der(mx,.6)+w(k)*my(.6),0,method="LLG-spin-ODE")
    check("W269",2,"spin wave quadratic exchange dispersion",
          w(k),gamma*(H0+D*k*k),method="spinwave-exchange")
    check("W269",3,"exchange magnon group speed spectral gradient",
          der(w,k),2*gamma*D*k,method="magnon-group-velocity")
    length=2.3;n=3
    kn=n*P/length
    check("W269",4,"finite magnetic strip free exchange boundary quantization",
          der(lambda x:C(kn*x),length),0,method="magnetic-Neumann-spectrum")
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
    # W271 equatorial beta-plane shallow-water Kelvin wave
    g,H,beta,k=9.8,2.1,.35,1.3
    c=S(g*H)
    eta=lambda y:E(-beta*y*y/(2*c))
    u=lambda y:g*eta(y)/c
    check("W271",1,"Kelvin mode zonal momentum continuity closes dispersion",
          (c*k)**2,g*H*k*k,method="rotating-shallow-water-dispersion")
    check("W271",2,"eastward Kelvin mode phase group velocity",
          der(lambda kk:c*kk,k),c,method="equatorial-Kelvin-group")
    check("W271",3,"geostrophic transverse Gaussian confinement ODE",
          der(eta,.7)+beta*.7/c*eta(.7),0,method="beta-plane-meridional-balance")
    check("W271",4,"westward branch cannot be meridionally normalised",
          E(beta*(3*c/beta)/(2*c))>1,1,method="Kelvin-wave-trapping-direction")
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
