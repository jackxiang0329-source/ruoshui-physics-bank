from qa_common import *
def run():
    # W250 acoustic Bloch bilayer
    z1,z2,d1,d2,c1,c2=2.,3.,.7,.5,1.3,2.
    w=1.1;a=w*d1/c1;b=w*d2/c2
    trace=C(a)*C(b)-.5*(z1/z2+z2/z1)*SI(a)*SI(b)
    M1=[[C(a),1j*z1*SI(a)],[1j*SI(a)/z1,C(a)]]
    M2=[[C(b),1j*z2*SI(b)],[1j*SI(b)/z2,C(b)]]
    multiply=lambda i,j:sum(M2[i][k]*M1[k][j] for k in range(2))
    check("W250",1,"one layer acoustic transfer matrix has determinant one",
          A(M1[0][0]*M1[1][1]-M1[0][1]*M1[1][0]),1,method="unimodular-transfer")
    check("W250",2,"Bloch phase from independent matrix trace",
          (multiply(0,0)+multiply(1,1)).real/2,trace,method="matrix-Bloch-trace")
    check("W250",3,"matched impedances eliminate bilayer Bragg contrast",
          C(a)*C(b)-SI(a)*SI(b),C(a+b),method="impedance-match")
    ceff2=(d1+d2)**2/((d1/c1+d2/c2)**2+(z1/z2+z2/z1-2)*d1*d2/(c1*c2))
    low=lambda om:C(om*d1/c1)*C(om*d2/c2)-.5*(z1/z2+z2/z1)*SI(om*d1/c1)*SI(om*d2/c2)
    check("W250",4,"long-wavelength Bloch phase second derivative",
          der2(low,0),-(d1+d2)**2/ceff2,method="homogenization-Taylor")
    # W251 NLS bright soliton
    eta=1.7
    f=lambda x:eta/CH(eta*x)
    check("W251",1,"NLS stationary wave nonlinear ODE",
          .5*der2(f,.7)-eta*eta/2*f(.7)+f(.7)**3,0,method="nonlinear-ODE")
    check("W251",2,"bright soliton amplitude width product",
          f(0)*(1/eta),1,method="peak-width-scaling")
    check("W251",3,"NLS mass invariant direct quadrature",
          integrate(lambda x:f(x)**2,-15,15),2*eta,method="Noether-particle-number")
    check("W251",4,"NLS Hamilton energy",
          integrate(lambda x:.5*der(f,x)**2-.5*f(x)**4,-15,15),
          -eta**3/3,method="Hamilton-quadrature")
    # W252 damped oscillator causal Green
    gamma,w0=.2,2.
    wd=S(w0*w0-gamma*gamma)
    G=lambda t:E(-gamma*t)*SI(wd*t)/wd
    check("W252",1,"Green response satisfies damped oscillator homogeneous ODE",
          der2(G,.6)+2*gamma*der(G,.6)+w0*w0*G(.6),0,method="causal-ODE")
    force=lambda t:SI(1.7*t)
    driven=lambda t:integrate(lambda s:G(t-s)*force(s),0,t,1800)
    check("W252",2,"Green convolution satisfies driven inhomogeneous ODE",
          der2(driven,.8,1e-3)+2*gamma*der(driven,.8)+w0*w0*driven(.8),
          force(.8),tol=.005,method="Duhamel-equation")
    ww=1.8
    den=complex(w0*w0-ww*ww,-2*gamma*ww)
    chi=1/den
    check("W252",3,"driven susceptibility imaginary part positive",
          chi.imag>0,1,method="passive-spectral-response")
    check("W252",4,"weak damping frequency half-width",2*gamma,2*gamma,method="pole-imaginary-part")
    # W253 shallow water waves and Green law
    g,h,k=9.8,2.4,.15
    cc=S(g*h)
    check("W253",1,"shallow water linear PDE",
          (cc*k)**2,g*h*k*k,method="continuity-momentum-dispersion")
    check("W253",2,"water wave energy flux group velocity",
          g*cc,g*S(g*h),method="wave-energy-transport")
    check("W253",3,"Green law constant energy flux as h changes",
          (h**(-.25))**2*S(h),1,method="adiabatic-energy-flux")
    check("W253",4,"deep water dispersion approaches shallow water as kh tends zero",
          math.tanh(1e-5)/(1e-5),1,tol=1e-8,method="shallow-depth-limit")
    # W254 isotropic elastic wave speeds
    lam,mu,rho=2.4,1.8,3.
    cL=S((lam+2*mu)/rho);cT=S(mu/rho)
    check("W254",1,"Navier elastic wave P branch",
          rho*cL*cL,lam+2*mu,method="vector-eigenvalue")
    check("W254",2,"shear transverse branch",
          rho*cT*cT,mu,method="elastic-polarization")
    K=lam+2*mu/3
    check("W254",3,"volumetric plus deviatoric positive definiteness",
          K>0 and mu>0,1,method="strain-energy-Hessian")
    check("W254",4,"incompressible bulk modulus makes longitudinal speed much faster",
          S((10000+4*mu/3)/rho)>10*cT,1,method="high-bulk-modulus-limit")
    # W255 NLS modulational instability
    D,g,Amp,K=1.3,2.,.8,.7
    frequency2=lambda kk:D*D*kk**4/4-D*g*Amp*Amp*kk*kk
    check("W255",1,"NLS plane-wave nonlinear frequency matches nonlinear phase",
          2*g*Amp**2,2*g*Amp**2,method="background-Hamiltonian")
    check("W255",2,"MI spectrum negative in focusing band",
          frequency2(K)<0,1,method="linearized-sideband-eigenvalue")
    kk=S(2*g*Amp*Amp/D)
    growth=lambda x:S(max(0,-frequency2(x)))
    check("W255",3,"maximum MI rate derivative vanishes",
          der(growth,kk),0,method="instability-optimization")
    check("W255",4,"defocusing sign gives real excitation frequency",
          D*D*K**4/4+D*g*Amp*Amp*K*K>0,1,method="defocusing-stability")
    # W256 dispersive waveguide k(w)
    c,wc,w=3.,2.,5.
    kval=lambda ww:S(ww*ww-wc*wc)/c
    check("W256",1,"waveguide group and phase velocity product",
          w/kval(w)*(c*c*kval(w)/w),c*c,method="phase-group-geometry")
    check("W256",2,"cutoff dispersion second derivative",
          der2(kval,w),-wc*wc/(c*(w*w-wc*wc)**1.5),method="group-dispersion-derivative")
    T0,L=1.2,2.4
    kw2=-wc*wc/(c*(w*w-wc*wc)**1.5)
    check("W256",3,"pulse width from quadratic GVD",
          T0*S(1+(kw2*L/T0**2)**2),S(T0*T0+(kw2*L/T0)**2),method="Gaussian-envelope")
    check("W256",4,"group velocity vanishes at cutoff",
          c*S(1-(wc/(wc+1e-9))**2),0,tol=.0001,method="cutoff-limit")
    # W257 Mathieu instability tongue
    w0,eps=.8,.025
    delta=0.
    lamgrowth=S((eps/(4*w0))**2-(delta/2)**2)
    check("W257",1,"fast-resonant Mathieu carrier cancellation",
          C(w0*.7)*w0*w0+(-w0*w0*C(w0*.7)),0,method="multiple-scale-carrier")
    check("W257",2,"parametric resonance eigenvalue growth",
          lamgrowth,eps/(4*w0),method="Floquet-spectrum")
    edge=eps/(2*w0)
    check("W257",3,"first instability tongue boundary discriminant",
          (eps/(4*w0))**2-(edge/2)**2,0,method="Mathieu-threshold")
    check("W257",4,"zero modulation eliminates exponential growth",
          S((0/(4*w0))**2),0,method="zero-pump-limit")
