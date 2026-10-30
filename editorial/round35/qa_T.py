from qa_common import *

def run():
    # T234: mean-field Ising with analytic derivatives and numerical roots
    Jz,kB,Tc=2.4,1.,2.4
    T=2.7
    rhs=lambda m,h:TH((Jz*m+h)/(kB*T))
    check("T234",1,"mean-field fixed point equals free-energy stationary condition",
          der(lambda m:Jz*m*m/2-kB*T*L(2*CH((Jz*m+.17)/(kB*T))),.2),
          Jz*(.2-rhs(.2,.17)),method="thermodynamic-stationarity")
    near=.01
    Tlow=Tc*(1-near)
    f=lambda m:m-TH(Jz*m/(kB*Tlow))
    rootm=root(f,.001,.5)
    check("T234",2,"critical spontaneous Ising magnetization squared",
          rootm*rootm,3*near,tol=.03,method="nonlinear-self-consistency")
    delta=1e-5
    susc=(rhs(0,delta)-rhs(0,-delta))/(2*delta)
    check("T234",3,"Curie Weiss susceptibility from implicit derivative",
          susc/(1-Jz/(kB*T)),1/(kB*(T-Tc)),method="field-derivative")
    ht=1e-5
    mt=root(lambda m:m-TH((Jz*m+ht)/(kB*Tc)),.0001,.5)
    check("T234",4,"critical isotherm cubic magnetic response",
          mt**3,3*ht/(kB*Tc),tol=.02,method="critical-scaling")
    # T235: 3D ideal Fermi gas, Sommerfeld chemical potential
    Ef,kB,T=5.,1.,.2
    mu=Ef*(1-P*P/12*(kB*T/Ef)**2)
    check("T235",1,"3D Fermi density-of-states number integral",
          integrate(lambda e:S(e),0,Ef,20000),2*Ef**1.5/3,method="Fermi-DOS-integral")
    check("T235",2,"Sommerfeld chemical-potential T2 coefficient",
          (Ef-mu)/(kB*T)**2,P*P/(12*Ef),method="Sommerfeld-number")
    UT=lambda tt:3*Ef/5+P*P/4*(kB*tt)**2/Ef
    check("T235",3,"Fermi energy thermal correction finite derivative",
          der(UT,T),P*P*kB*kB*T/(2*Ef),method="thermodynamic-derivative")
    check("T235",4,"Pauli linear-in-T specific heat vanishes at zero temperature",
          der(UT,1e-5),P*P*kB*kB*1e-5/(2*Ef),method="low-temperature-limit")
    # T236: Carnot, entropy generation and lost work
    Th,Tcold,Qh,Qc=500.,300.,100.,70.
    Sgen=Qc/Tcold-Qh/Th
    check("T236",1,"reservoir entropy generated in heat cycle",Sgen>=0,1,method="second-law-positivity")
    eta=(Qh-Qc)/Qh
    check("T236",2,"efficiency gap equals entropy production",
          (1-Tcold/Th)-eta,Tcold*Sgen/Qh,method="Clausius-identity")
    Wrev=Qh*(1-Tcold/Th);W=Qh-Qc
    check("T236",3,"Gouy Stodola lost work",Wrev-W,Tcold*Sgen,method="exergy-work")
    Cv=2.;T1=450.;T2=350.
    check("T236",4,"finite reservoir entropy change is logarithmic integral",
          integrate(lambda T:Cv/T,T2,T1),Cv*L(T1/T2),method="finite-heat-reservoir")
    # T237: Debye phonons
    N,kB,theta=50.,1.,200.
    g=lambda x:x**3/(E(x)-1) if x>0 else 0
    I4=integrate(g,0,42,12000)
    check("T237",1,"Debye Bose energy integral converges",
          I4,P**4/15,method="Planck-integral")
    tiny=.01
    Ulow=lambda temp:(3*P**4/5)*N*kB*temp**4/theta**3
    check("T237",2,"Debye heat capacity low temperature cubic",
          der(Ulow,tiny),12*P**4/5*N*kB*tiny**3/theta**3,tol=1e-8,method="power-law-derivative")
    tHigh=1000*theta
    mean=integrate(lambda w:(w/(E(w/tHigh)-1) if w>0 else tHigh)*3*w*w,0,1,10000)
    check("T237",3,"Dulong Petit high temperature one normalized Debye cell",
          mean/tHigh,1,tol=.002,method="high-temperature-Bose-limit")
    check("T237",4,"two-dimensional acoustic phonons exponent",
          (2+1)-2,1,method="dimensional-mode-count")
    # T238: chemical reaction Gibbs free energy
    R,T,dG=-8.,400.,-2500.
    # R overwritten below for physical gas constant
    R=8.314
    K=E(-dG/(R*T))
    check("T238",1,"reaction affinity from chemical potentials at equilibrium",
          dG+R*T*L(K),0,method="Gibbs-affinity")
    check("T238",2,"reaction quotient returns equilibrium constant",
          E(-dG/(R*T)),K,method="mass-action")
    dH=14000.;T1=350.;T2=450.
    rhs=dH/R*(1/T1-1/T2)
    check("T238",3,"van't Hoff derivative integrated over temperature",
          integrate(lambda tt:dH/(R*tt*tt),T1,T2,12000),rhs,method="temperature-integral")
    check("T238",4,"endothermic K increases when temperature rises",
          rhs>0,1,method="thermodynamic-sign")
    # T239: information heat engine
    T=300.;k=1.38e-23
    work=integrate(lambda V:k*T/V,1.,2.,12000)
    check("T239",1,"Szilard one-bit extraction is isothermal work",
          work,k*T*L(2),tol=1e-28,method="pressure-volume-integration")
    p=.5
    Shannon=-(p*L(p)+(1-p)*L(1-p))
    check("T239",2,"two outcome Shannon information",Shannon,L(2),method="probability-entropy")
    check("T239",3,"Landauer erase heat cancels best extraction",
          k*T*Shannon,work,tol=1e-28,method="erasure-heat")
    pe=.1
    binaryH=-(pe*L(pe)+(1-pe)*L(1-pe))
    check("T239",4,"noisy binary measurement has reduced information",
          Shannon-binaryH<L(2),1,method="mutual-information")
    # T240: exact Joule Thomson inversion
    aa,bb,R=3.,.5,8.314
    v=2.1
    Tinv=2*aa*(v-bb)**2/(R*bb*v*v)
    Pd=lambda T,v:R*T/(v-bb)-aa/(v*v)
    pV=der(lambda z:Pd(Tinv,z),v)
    pT=der(lambda z:Pd(z,v),Tinv)
    vT=-pT/pV
    check("T240",1,"Joule Thomson exact thermodynamic identity",
          Tinv*vT-v,0,tol=1e-5,method="implicit-vdW-derivative")
    check("T240",2,"low-density van der Waals inversion temperature",
          2*aa/(R*bb),2*aa/(R*bb),method="dilute-inversion")
    check("T240",3,"exact inversion curve satisfies zero cooling coefficient",
          Tinv*vT-v,0,method="inversion-locus")
    vg=100.
    Tgas=2*aa/(R*bb)
    check("T240",4,"high-volume inversion approaches dilute estimate",
          2*aa*(vg-bb)**2/(R*bb*vg*vg),Tgas,tol=.011,method="large-volume-limit")
    # T241: ballistic thermal conductance
    kB,hbar,T=1.,1.,.5
    BoseI=integrate(lambda x:x/(E(x)-1) if x>0 else 1,0,40,14000)
    check("T241",1,"one-dimensional Landauer Bose integral",BoseI,P*P/6,method="Bose-quadrature")
    flow=lambda t:P*kB*kB*t*t/(12*hbar)
    Tl,Tr=.8,.4
    check("T241",2,"finite temperature ballistic heat current",
          flow(Tl)-flow(Tr),P*kB*kB*(Tl*Tl-Tr*Tr)/(12*hbar),method="net-energy-flux")
    check("T241",3,"linear response quantum conductance from derivative",
          der(flow,T),P*kB*kB*T/(6*hbar),method="transport-derivative")
    check("T241",4,"zero temperature ballistic thermal conductance vanishes",
          der(flow,1e-5),P*kB*kB*1e-5/(6*hbar),method="third-law-limit")
