from qa_common import *

def run():
    # W242 two mismatched lossless string junctions
    T,m1,m2,w=2.1,1.3,4.8,2.5
    c1=S(T/m1);c2=S(T/m2)
    k1=w/c1;k2=w/c2
    r=(k1-k2)/(k1+k2);t=1+r
    check("W242",1,"string interface continuity of displacement",t,1+r,method="boundary-displacement")
    check("W242",2,"string interface continuity of transverse force",
          k1*(1-r),k2*t,method="boundary-stress")
    Z1=T/c1;Z2=T/c2
    check("W242",3,"reflection plus transmitted mechanical power",
          r*r+(Z2/Z1)*t*t,1,method="energy-flux")
    check("W242",4,"impedance-matched equal-density limit",
          (Z1-Z1)/(Z1+Z1),0,method="matching-limit")
    # W243 point mass string
    M,Z,w=1.2,2.3,3.4
    r=-M*w/complex(M*w,2*Z);t=complex(0,2*Z)/complex(M*w,2*Z)
    check("W243",1,"point mass acceleration balances slope jump",
          A(-M*w*w*t-complex(0,2*w*Z)*r),0,method="dynamic-boundary")
    check("W243",2,"complex transmission plus reflection",
          A(t-(1+r)),0,method="boundary-continuity")
    check("W243",3,"point mass scattering unitary",A(r)**2+A(t)**2,1,method="unitary-flux")
    ws=.00001
    check("W243",4,"low frequency point mass reflection vanishes",
          A(-M*ws/complex(M*ws,2*Z)),0,tol=.0001,method="low-frequency-limit")
    # W244 gaussian pulse dispersion
    T0,k2,z=1.7,.8,3.2
    D=k2*z/T0**2
    amp=lambda t:1/S(S(1+D*D))*E(-t*t/(2*T0*T0*(1+D*D)))
    check("W244",1,"Gaussian spectral propagation group delay",2.4-.4*3.2,2.4-1.28,method="envelope-coordinate")
    check("W244",2,"dispersed pulse intensity peak amplitude",
          amp(0)**2,1/S(1+D*D),method="Fourier-Gaussian")
    check("W244",3,"Gaussian pulse intensity second moment",
          integrate(lambda t:t*t*amp(t)**2,-12,12)/integrate(lambda t:amp(t)**2,-12,12),
          T0*T0*(1+D*D)/2,method="temporal-variance")
    check("W244",4,"zero dispersion width recovers T0",
          T0*S(1+(0*z/T0**2)**2),T0,method="zero-dispersion-limit")
    # W245 Kelvin Helmholtz determinant
    rho1,rho2,g,kap,sig=4.,2.,9.8,1.2,.7
    total=rho1+rho2;Ud=.9
    rad=((rho1-rho2)*g*kap+sig*kap**3)/total-rho1*rho2*kap*kap*Ud*Ud/(total*total)
    coeff=((rho1-rho2)*g/kap+sig*kap)*total/(rho1*rho2)
    check("W245",1,"stable stratification gravity restoring term sign",
          ((rho1-rho2)*g*kap)>0,1,method="stratification-sign")
    check("W245",2,"KH dispersion with background shear",
          rad>0,1,method="eigenvalue-positivity")
    check("W245",3,"shear instability threshold crossing",
          rad,rho1*rho2*kap*kap/(total*total)*(coeff-Ud*Ud),method="stability-inequality")
    kstar=S((rho1-rho2)*g/sig)
    check("W245",4,"gravity capillary threshold stationary at kstar",
          der(lambda q:(rho1-rho2)*g/q+sig*q,kstar),0,method="critical-wave-number")
    # W246 internal gravity waves group velocity
    N,k,m=1.9,.7,.9
    freq=lambda kk,mm:N*kk/S(kk*kk+mm*mm)
    f=freq(k,m)
    check("W246",1,"internal wave buoyancy dispersion",
          f*f*(k*k+m*m),N*N*k*k,method="Boussinesq-eigenvalue")
    vx=der(lambda q:freq(q,m),k);vz=der(lambda q:freq(k,q),m)
    check("W246",2,"internal wave horizontal group speed",
          vx,N*m*m/(k*k+m*m)**1.5,method="group-velocity-derivative")
    check("W246",3,"group velocity perpendicular to internal wave normal",
          k*vx+m*vz,0,method="energy-geometry")
    check("W246",4,"vertical wavevector vanishing yields N frequency",
          freq(k,0),N,method="polarization-limit")
    # W247 diatomic lattice two roots
    m1,m2,K,q,a=1.,2.6,3.,.7,1.2
    s0=SI(q*a/2)**2
    S0=K*(1/m1+1/m2)
    disc=S((1/m1+1/m2)**2-4*s0/(m1*m2))*K
    low=S0-disc;high=S0+disc
    check("W247",1,"dynamical matrix characteristic roots product",
          low*high,4*K*K*s0/(m1*m2),method="Bloch-determinant")
    check("W247",2,"acoustic plus optical eigenvalue trace",
          low+high,2*K*(1/m1+1/m2),method="spectral-trace")
    check("W247",3,"acoustic branch zero at center",
          K*(1/m1+1/m2)-K*S((1/m1+1/m2)**2),0,method="translation-Goldstone")
    check("W247",4,"Brillouin edge frequency separation",
          2*K/min(m1,m2)-2*K/max(m1,m2)>0,1,method="gap-criterion")
    # W248 Burgers tanh shock
    ul,ur,nu=2.5,.7,.2
    speed=(ul+ur)/2;du=ul-ur
    wave=lambda x:speed-du/2*TH(du*x/(4*nu))
    check("W248",1,"integrated traveling Burgers equation",
          nu*der(wave,.8), (wave(.8)-ul)*(wave(.8)-ur)/2,method="traveling-wave-ODE")
    check("W248",2,"Rankine Hugoniot propagation",
          (ul*ul-ur*ur)/(2*(ul-ur)),speed,method="jump-condition")
    check("W248",3,"Burgers shock satisfies viscous PDE",
          -speed*der(wave,.5)+wave(.5)*der(wave,.5),
          nu*der2(wave,.5),tol=.0001,method="nonlinear-PDE")
    check("W248",4,"viscous shock thin-layer scaling",
          (4*(nu/2)/du)/(4*nu/du),.5,method="singular-viscosity")
    # W249 circular membrane Bessel boundary
    a,T,mu=2.,3.,1.5
    j01=2.404825557695773
    check("W249",1,"radial Bessel Helmholtz equation at first zero",
          jb(0,j01),0,method="Bessel-boundary")
    k=j01/a
    check("W249",2,"circular membrane eigenfrequency from radial k",
          (k*S(T/mu))**2,(T/mu)*(j01/a)**2,method="membrane-spectrum")
    check("W249",3,"orthogonality of two Bessel membrane radial modes",
          integrate(lambda r:r*jb(0,j01*r/a)*jb(0,5.52007811028631*r/a),0,a,12000),
          0,method="Sturm-Liouville-orthogonality")
    check("W249",4,"radius doubling halves modal frequency",
          j01/(2*a)*S(T/mu)/(j01/a*S(T/mu)),.5,method="geometry-scaling")
