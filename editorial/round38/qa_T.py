from qa_common import *
def run():
    # T258 van der Waals critical point
    a,b,R=2.3,.7,1.2
    Pc=a/(27*b*b);Vc=3*b;Tc=8*a/(27*R*b)
    pressure=lambda v,t:R*t/(v-b)-a/v**2
    check("T258",1,"vdW critical isotherm zero first and second derivatives",
          der(lambda v:pressure(v,Tc),Vc),0,method="critical-stationary-isotherm")
    check("T258",2,"vdW critical pressure compressibility Z",
          Pc*Vc/(R*Tc),3/8,method="critical-thermodynamic-ratio")
    x=.0008
    c=lambda xx:8/(2+3*xx)-3/(1+xx)**2
    check("T258",3,"vdW critical cubic isotherm coefficient",
          (c(x)-c(-x))/(2*x**3),-1.5,tol=.0003,method="critical-cubic-series")
    ta=.03
    check("T258",4,"vdW inverse susceptibility proportional reduced T",
          -(der(lambda v:8*(1+ta)/(3*v-1)-3/v**2,1)),6*ta,method="compressibility-critical-scaling")
    # T259 Planck radiation
    def bosex(x):return x**3/(E(x)-1) if x>1e-8 else x*x
    integral=integrate(bosex,0,35,7000)
    check("T259",1,"thermal photon Planck energy density third Bose integral",
          integral,P**4/15,method="Planck-Bose-quadrature")
    kB,hbar,c,T=1.3,.8,2.4,4.
    rad=P*P*(kB*T)**4/(15*hbar**3*c**3)
    sigma=P*P*kB**4/(60*hbar**3*c**2)
    check("T259",2,"Stefan-Boltzmann power equals isotropic cu over four",
          c*rad/4,sigma*T**4,method="thermal-radiation-flux")
    xstar=root(lambda x:5*(1-E(-x))-x,3,6)
    check("T259",3,"Wien wavelength root from Planck spectral derivative",
          5*(1-E(-xstar))-xstar,0,method="Planck-wavelength-peak")
    freqroot=root(lambda x:3*(1-E(-x))-x,2,4)
    check("T259",4,"frequency and wavelength maxima are distinct",
          A(xstar-freqroot)>.5,1,method="spectral-Jacobian")
    # T260 Joule Thomson
    R,a,b,T,Cp=1.2,3.,.7,2.5,5.
    v=lambda tt,p:R*tt/p+b-a/(R*tt)
    P0=.2
    check("T260",1,"enthalpy differential gives JT numerator",
          T*der(lambda tt:v(tt,P0),T)-v(T,P0),2*a/(R*T)-b,method="enthalpy-Maxwell")
    check("T260",2,"ideal gas gives zero isenthalpic temperature change",
          T*der(lambda tt:R*tt/P0,T)-R*T/P0,0,method="ideal-gas-JT")
    check("T260",3,"vdW low pressure JT coefficient",
          (2*a/(R*T)-b)/Cp,(T*der(lambda tt:v(tt,P0),T)-v(T,P0))/Cp,method="virial-JT")
    inv=2*a/(R*b)
    check("T260",4,"van der Waals inversion temperature zero numerator",
          2*a/(R*inv)-b,0,method="JT-inversion")
    # T261 mean field Curie Weiss
    Jz,kB=2.,1.
    Tc=Jz/kB
    def selfconsistent(m,T,h=0):
        return m-TH((h+Jz*m)/(kB*T))
    check("T261",1,"mean field field derivative of single spin partition",
          der(lambda h:L(2*CH(h/(kB*2.5))),.6),
          TH(.6/(kB*2.5))/(kB*2.5),method="single-spin-partition")
    check("T261",2,"Curie Weiss critical slope at zero spin polarization",
          der(lambda m:TH(Jz*m/(kB*Tc)),0),1,method="linearized-selfconsistency")
    # use near transition and leading order, expected of m^2
    T=.998*Tc
    m2=3*((Tc/T)-1)/(Tc/T)**3
    check("T261",3,"small magnetization Landau residual scales fourth order",
          A(selfconsistent(S(m2),T))<1e-5,1,method="Landau-bifurcation")
    T=3.
    suscept=1/(kB*(T-Tc))
    check("T261",4,"Weiss paramagnetic susceptibility",
          (1/(kB*T))/(1-Jz/(kB*T)),suscept,method="susceptibility-derivative")
    # T262 two state master equation
    k01,k10,p0=1.4,.6,.3
    peq=k01/(k01+k10)
    prob=lambda t:peq+(p0-peq)*E(-(k01+k10)*t)
    check("T262",1,"Markov stationary distribution normalized",
          peq+k10/(k01+k10),1,method="stationary-master")
    check("T262",2,"two state exponential relaxation derivative",
          der(prob,.7),k01*(1-prob(.7))-k10*prob(.7),method="master-ODE")
    p=prob(.5);current=k01*(1-p)-k10*p
    entropy=current*L((k01*(1-p))/(k10*p))
    check("T262",3,"entropy production is nonnegative away from equilibrium",
          entropy>=0,1,method="KL-entropy-production")
    check("T262",4,"detailed balance net steady probability current is zero",
          k01*(1-peq)-k10*peq,0,method="two-node-no-loop")
    # T263 conduction with radiation boundary
    k,plate_length,er,sigma,Th,Ta=2.,1.4,.7,.002,12.,3.
    f=lambda ts:k*(Th-ts)/plate_length-er*sigma*(ts**4-Ta**4)
    rootT=root(f,Ta,Th)
    check("T263",1,"Fourier steady conduction temperature profile boundary",
          Th-(k*(Th-rootT)/plate_length)*plate_length/k,rootT,method="heat-flux-temperature-gradient")
    check("T263",2,"surface conduction radiation flux matching",f(rootT),0,method="nonlinear-radiation-boundary")
    check("T263",3,"radiative Robin boundary is strictly monotone",
          der(f,rootT)<0,1,method="unique-radiative-steady-state")
    hr=4*er*sigma*Ta**3
    small=1e-4; Th0=Ta+small
    fr=lambda ts:k*(Th0-ts)/plate_length-er*sigma*(ts**4-Ta**4)
    surface=root(fr,Ta,Th0)
    flux=k*(Th0-surface)/plate_length
    check("T263",4,"small delta T series thermal resistance",
          flux,small/(plate_length/k+1/hr),tol=.0002,method="radiation-linearization")
    # T264 ideal reaction dissociation
    Kp,p=1.7,.9
    alpha=S(Kp/(Kp+4*p))
    yA=2*alpha/(1+alpha);yA2=(1-alpha)/(1+alpha)
    check("T264",1,"mole balance for dissociation",
          yA+yA2,1,method="reaction-stoichiometric-normalization")
    check("T264",2,"mass action ideal gas pressure Kp",
          yA*yA/yA2*p,Kp,method="chemical-equilibrium")
    check("T264",3,"dissociation decreases as total pressure rises",
          der(lambda p0:S(Kp/(Kp+4*p0)),p)<0,1,method="LeChatelier-pressure")
    check("T264",4,"high pressure dissociation inverse square root",
          S(Kp/(Kp+4*1e7))/(S(Kp)/(2*S(1e7))),1,tol=.0001,method="mass-action-asymptotic")
    # T265 one dimensional Fermi gas
    n,m,hbar=1.3,1.5,.7
    kF=P*n/2;EF=hbar*hbar*kF*kF/(2*m)
    dos=lambda e:S(2*m)/(P*hbar*S(e))
    check("T265",1,"1D occupied Fermi sphere spin-degeneracy counting",
          2*kF/P,n,method="Fermi-momentum-counting")
    check("T265",2,"1D density of states integrated up to EF",
          integrate(lambda k:2/P,0,kF,12000),n,method="1D-mode-number")
    check("T265",3,"Fermi density of states at Fermi edge",
          dos(EF),n/(2*EF),method="Sommerfeld-DOS")
    energy=lambda length:(n*length)*(hbar*hbar*(P*(n*length)/length/2)**2/(2*m))/3
    check("T265",4,"1D ground state energy per particle",
          (hbar*hbar*kF*kF/(6*m)),EF/3,method="Fermi-ground-state-energy")
