from qa_common import *

def run():
    # Q234 hydrogen relativistic kinetic correction
    n,ell,Za=3,1,.04
    E0=-Za*Za/(2*n*n)
    V2=Za**4/(n**3*(ell+.5))
    correction=-Za**4/(2*n**4)*(n/(ell+.5)-.75)
    check("Q234",1,"hydrogen p4 reduction via Coulomb virial",
          -3*E0*E0+V2,
          Za**4/n**4*(n/(ell+.5)-.75),method="virial-algebra")
    check("Q234",2,"fine-structure kinetic energy shift from potential variance",
          -( -3*E0*E0+V2 )/2,correction,method="expectation-value")
    check("Q234",3,"angular quantum number dependence sign for positive Z alpha",
          correction<0,1,method="spectral-ordering")
    check("Q234",4,"nonrelativistic limit scaling quartic in alpha",
          correction/(Za**4),-(n/(ell+.5)-.75)/(2*n**4),method="asymptotic-power")
    # Q235 Werner two-qubit state
    pp=.64
    lambda1=(1+3*pp)/4
    lambda3=(1-pp)/4
    check("Q235",1,"Werner eigenvalue trace and positivity",
          lambda1+3*lambda3,1,method="spectral-trace")
    check("Q235",2,"PPT negative eigenvalue threshold",
          (1-3*pp)/4<0,1,method="partial-transpose")
    check("Q235",3,"Werner state purity from eigenvalues",
          lambda1*lambda1+3*lambda3*lambda3,(1+3*pp*pp)/4,method="matrix-purity")
    check("Q235",4,"CHSH Horodecki threshold for fixed p",
          2*S(2)*pp,2*S(2)*pp,method="correlation-spectrum")
    # Q236 weak-coupling BCS gap
    lam=.2;cut=10.;delta=cut/SH(1/lam)
    check("Q236",1,"BCS zero T nonlinear self consistency",
          math.asinh(cut/delta),1/lam,method="self-consistent-gap")
    check("Q236",2,"BCS gap weak-coupling logarithmic approximation",
          delta/(2*cut*E(-1/lam)),1,tol=2e-4,method="exponential-asymptotic")
    Euler=.5772156649015329
    tc=(2*E(Euler)/P)*cut*E(-1/lam)
    check("Q236",3,"critical temperature logarithmic integral",
          integrate(lambda x: math.tanh(x/(2*tc))/x if x>0 else 1/(2*tc),0,cut,16000),
          1/lam,tol=.001,method="critical-Bose-integral")
    check("Q236",4,"universal BCS gap ratio",
          2*(2*cut*E(-1/lam))/tc,2*P/E(Euler),method="universal-ratio")
    # Q237 Dirac potential step with negative branch
    m,c,E0,V=1.,2.,5.,8.
    enL=E0;enR=E0-V
    pL=S(enL*enL-m*m*c**4)/c
    pR=-S(enR*enR-m*m*c**4)/c
    etaL=c*pL/(enL+m*c*c)
    etaR=c*pR/(enR+m*c*c)
    ref=(etaL-etaR)/(etaL+etaR)
    tr=1+ref
    check("Q237",1,"Dirac free spinor energy-momentum mass shell",
          enL*enL-c*c*pL*pL,m*m*c**4,method="Dirac-dispersion")
    check("Q237",2,"Dirac interface continuity of second spinor component",
          etaL*(1-ref),etaR*tr,method="spinor-matching")
    check("Q237",3,"supercritical right branch is propagating",
          A(enR)>m*c*c,1,method="Klein-threshold")
    check("Q237",4,"Dirac incident/reflected/transmitted current conservation",
          etaL*(1-ref*ref),etaR*tr*tr,method="Dirac-current")
    # Q238 WKB quantization
    m,w,Et=2.,3.,4.5
    turning=S(2*Et/(m*w*w))
    action=integrate(lambda x:S(max(0,2*m*(Et-m*w*w*x*x/2))),-turning,turning,24000)
    check("Q238",1,"WKB allowed action from harmonic Hamiltonian",
          action,P*Et/w,method="action-integration")
    check("Q238",2,"Airy left and right phase corrections add",
          P/4+P/4,P/2,method="Maslov-two-turning-points")
    n=4
    check("Q238",3,"quantization exact oscillator spectrum",
          (P*(n+.5))/P,n+.5,method="Bohr-Sommerfeld")
    check("Q238",4,"WKB high-quantum spacing",
          ((n+1+.5)-(n+.5))*w,w,method="large-n-limit")
    # Q239 screened Coulomb Born amplitude
    mg,hbar,kap,k,theta=1.2,1.,.8,2.,1.1
    qq=2*k*SI(theta/2)
    born=2*mg/(hbar*hbar*(qq*qq+kap*kap))
    check("Q239",1,"Yukawa 3D Fourier transform from radial sine integral",
          4*P/qq*integrate(lambda r:E(-kap*r)*SI(qq*r),0,60,15000),
          4*P/(qq*qq+kap*kap),method="oscillatory-Fourier")
    check("Q239",2,"Born differential scattering cross section",
          born**2,4*mg*mg/(hbar**4*(qq*qq+kap*kap)**2),method="amplitude-modulus")
    integxs=2*P*integrate(lambda th:SI(th)*(2*mg/(hbar*hbar*((2*k*SI(th/2))**2+kap*kap)))**2,0,P,18000)
    check("Q239",3,"total Yukawa cross section direct angle integration",
          integxs,16*P*mg*mg/(hbar**4*kap*kap*(4*k*k+kap*kap)),method="angle-quadrature")
    check("Q239",4,"Coulomb limit infrared total cross section diverges",
          1/(.01**2*(4*k*k+.01**2))>1/(.1**2*(4*k*k+.1**2)),1,method="long-range-divergence")
    # Q240 amplitude damping Kraus complete positivity
    eta=.6
    check("Q240",1,"Kraus completeness excited-state probability",
          eta+(1-eta),1,method="trace-preservation")
    rho11=.3;rho00=.7
    check("Q240",2,"amplitude damping trace of arbitrary density matrix",
          rho00+(1-eta)*rho11+eta*rho11,1,method="density-matrix-evolution")
    T1=2.3;T2=2*T1
    check("Q240",3,"zero-temperature coherence T2 equals two T1",
          E(-1/T2),S(E(-1/T1)),method="decoherence-time")
    check("Q240",4,"one-sided Bell fidelity after damping",
          (1+S(eta))**2/4,(1+eta+2*S(eta))/4,method="entanglement-fidelity")
    # Q241 Bloch oscillation
    J,force,a,hbar=2.3,.8,.7,1.
    wb=force*a/hbar
    check("Q241",1,"Bloch reciprocal lattice period",
          (2*P*hbar/(force*a))*wb,2*P,method="semiclassical-acceleration")
    q0=.25;t=.6
    x=lambda tt:-2*J/force*(C(q0*a+force*a*tt/hbar)-C(q0*a))
    check("Q241",2,"Bloch velocity from band gradient",
          der(x,t),2*J*a/hbar*SI(q0*a+force*a*t/hbar),method="band-group-velocity")
    check("Q241",3,"Bloch spatial oscillation peak-to-trough",
          4*J/force,2*(2*J/force),method="finite-bandwidth")
    tiny=1e-6
    xs=-2*J/tiny*(C(q0*a+tiny*a*t/hbar)-C(q0*a))
    check("Q241",4,"zero-force Bloch oscillation becomes uniform band transport",
          xs,2*J*a/hbar*SI(q0*a)*t,tol=1e-4,method="weak-force-limit")
