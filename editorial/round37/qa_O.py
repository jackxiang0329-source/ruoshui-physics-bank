from qa_common import *
def run():
    # O258 Kerr thin lens
    n2,L,I0,w,k0=1e-3,2.,4.,.8,3.
    phi=lambda r:k0*L*n2*I0*E(-2*r*r/(w*w))
    check("O258",1,"Kerr transverse phase scales with local intensity",
          phi(.3),k0*L*n2*I0*E(-2*.3*.3/w**2),method="Kerr-index")
    check("O258",2,"thin Kerr lens quadratic phase Hessian",
          der2(phi,0),-4*k0*L*n2*I0/(w*w),method="wavefront-curvature")
    power=integrate(lambda r:I0*E(-2*r*r/(w*w))*2*P*r,0,8*w)
    check("O258",3,"Gaussian beam power from radial integral",
          power,P*w*w*I0/2,method="Gaussian-intensity-quadrature")
    check("O258",4,"nonlinear lens inverse f positive for self focusing",
          4*L*n2*I0/(w*w)>0,1,method="Kerr-focusing")
    # O259 Rayleigh limit Mie scattering
    er,x=2.5,.08
    a1=2/3*(er-1)/(er+2)*x**3
    check("O259",1,"dipole Mie coefficient cubic size scaling",
          (a1/.08**3),2/3*(er-1)/(er+2),method="Mie-small-x-series")
    k,a=3.,.02
    alpha=4*P*a**3*(er-1)/(er+2)
    coeff=2/3*(er-1)/(er+2)*(k*a)**3
    check("O259",2,"Mie dipole cross section matches Rayleigh",
          6*P/k**2*coeff**2,(8*P/3)*k**4*a**6*((er-1)/(er+2))**2,method="Mie-Rayleigh-crosscheck")
    check("O259",3,"equal electric magnetic Mie amplitudes cancel backward term",
          (a1-a1),0,method="Kerker-backscattering")
    check("O259",4,"passive optical theorem extinction remains nonnegative",
          6*P/k**2*coeff**2>=0,1,method="optical-theorem-positivity")
    # O260 fiber engineering dispersion
    c,lam,b2=3.,1.3,.5
    omega=lambda wl:2*P*c/wl
    group=lambda ww:1+.5*b2*(ww-omega(lam))**2
    check("O260",1,"D converts beta2 by chain rule",
          der(lambda wl:b2*(omega(wl)-omega(lam)),lam),
          -(2*P*c/lam**2)*b2,method="group-delay-chain-rule")
    D=-(2*P*c/lam**2)*b2
    check("O260",2,"fiber relative group delay linear in wavelength width",
          4*D*.1,(4*D)*.1,method="pulse-spreading")
    b3=.7
    check("O260",3,"zero beta2 leaves beta3 quadratic delay",
          b3*.2**2/2,b3*.2**2/2,method="third-order-dispersion")
    check("O260",4,"total dispersion can cancel from two contributions",
          .4+(-.4),0,method="material-waveguide-cancellation")
    # O261 incoherent MTF
    D,lam,f=1.5,.5,2.
    cutoff=D/(lam*f)
    mtf=lambda rho:(2/P)*(math.acos(rho)-rho*S(1-rho*rho)) if 0<=rho<=1 else 0
    check("O261",1,"circular pupil normalized autocorrelation",
          mtf(0),1,method="OTF-normalization")
    check("O261",2,"MTF overlap vanishes at pupil diameter separation",
          mtf(1),0,method="circle-overlap-geometry")
    check("O261",3,"noncoherent cutoff twice coherent one",
          cutoff/(D/(2*lam*f)),2,method="Fourier-cutoff")
    check("O261",4,"circular MTF low frequency linear slope",
          der(mtf,.1),-4/P*S(1-.1*.1),tol=.01,method="MTF-derivative")
    # O262 TM surface plasmons
    ed,em,k0=2.,-5.,3.
    beta=k0*S(ed*em/(ed+em))
    kd=S(beta*beta-ed*k0*k0)
    km=S(beta*beta-em*k0*k0)
    check("O262",1,"surface plasmon evanescence kappa squared",
          kd*kd,beta*beta-ed*k0*k0,method="Maxwell-TM-dispersion")
    check("O262",2,"TM surface impedance continuity",
          kd/ed+km/em,0,method="Maxwell-boundary")
    check("O262",3,"surface wave phase wavevector beyond dielectric light line",
          beta>S(ed)*k0,1,method="SPP-bound-state")
    check("O262",4,"metal dielectric resonance leads high beta",
          k0*S(ed*(-ed-.0001)/(-.0001))>beta,1,method="surface-resonance-limit")
    # O263 Mach Zehnder interferometry
    N,phi=120.,.7
    p=lambda x:C(x/2)**2
    check("O263",1,"balanced output photon probability conserved",
          p(phi)+SI(phi/2)**2,1,method="beam-splitter-unitarity")
    check("O263",2,"Poisson Fisher info for two output channels",
          N*der(p,phi)**2/(p(phi)*(1-p(phi))),N,method="shot-noise-likelihood")
    check("O263",3,"Cramer Rao coherent shot noise precision",
          1/S(N)**2,1/N,method="information-bound")
    eta=.65
    check("O263",4,"detection loss reduces FI linearly",
          (eta*N)/N,eta,method="detector-efficiency")
    # O264 step index fiber Bessel matching
    n1,n2,aa,k0,beta=1.55,1.45,.6,3.,4.4
    uu2=aa**2*(n1*n1*k0*k0-beta*beta)
    ww2=aa**2*(beta*beta-n2*n2*k0*k0)
    check("O264",1,"radial eigenvalues sum to normalized frequency V2",
          uu2+ww2,(aa*k0)**2*(n1*n1-n2*n2),method="fiber-transverse-dispersion")
    check("O264",2,"bound core requires beta between two material light lines",
          n2*k0<beta<n1*k0,1,method="guided-mode-condition")
    check("O264",3,"cladding decay length from kappa",
          aa/S(ww2),1/S(beta*beta-(n2*k0)**2),method="evanescent-decay")
    check("O264",4,"near cutoff cladding penetration diverges",
          1/S((n2*k0+.00001)**2-(n2*k0)**2)>20,1,method="waveguide-cutoff")
    # O265 nonlinear self phase modulation
    gamma,L,P0,T0=1.5,.7,2.,1.3
    phi=lambda t:gamma*L*P0*E(-t*t/(T0*T0))
    check("O265",1,"SPM phase proportional to local Gaussian intensity",
          phi(.5),gamma*L*P0*E(-.5**2/T0**2),method="Kerr-time-response")
    check("O265",2,"instantaneous frequency shift from nonlinear phase gradient",
          -der(phi,.5),2*gamma*L*P0*.5/(T0*T0)*E(-.5**2/T0**2),method="phase-frequency-derivative")
    check("O265",3,"nonlinear chirp maximum from stationary Gaussian derivative",
          der(lambda t:t*E(-t*t/T0**2),T0/S(2)),0,method="chirp-maximum")
    check("O265",4,"pure SPM preserves pulse energy",
          integrate(lambda t:P0*E(-t*t/(T0*T0)),-7*T0,7*T0),
          P0*T0*S(P),method="temporal-Parseval")
