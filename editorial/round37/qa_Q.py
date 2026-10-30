from qa_common import *
def run():
    # Q258 Jaynes Cummings cavity dressed states
    g,delta,n,omegaC=1.2,2.3,4,3.2
    Om=S(delta*delta+4*g*g*(n+1))
    ep=omegaC*(n+.5)+Om/2
    em=omegaC*(n+.5)-Om/2
    check("Q258",1,"Jaynes Cummings excitation number conserved by one photon spin flip",
          n+1,(n+1)+0,method="operator-excitation")
    check("Q258",2,"Jaynes Cummings dressed energy splitting from block eigenvalues",
          ep-em,Om,method="Jaynes-Cummings-spectrum")
    Pe=lambda t:1-(4*g*g*(n+1)/Om**2)*SI(Om*t/2)**2
    check("Q258",3,"Jaynes Cummings Rabi excited population in unit interval",
          0<=Pe(.7)<=1,1,method="Rabi-probability")
    shift=lambda d:(S(d*d+4*g*g*(n+1))-d)/2
    check("Q258",4,"large detuning dispersive shift leading order",
          shift(200.),g*g*(n+1)/200,tol=.0002,method="dispersive-perturbation")
    # Q259 Landau Zener
    v,delta,hbar=2.,.7,1.
    en=lambda t:.5*S(delta*delta+v*v*t*t)
    check("Q259",1,"two-level avoided crossing minimum energy gap",
          2*en(0),delta,method="Pauli-eigenspectrum")
    theta=lambda t:math.atan2(delta,v*t)
    check("Q259",2,"Landau Zener mixing angle derivative",
          der(theta,.2),-v*delta/(delta*delta+(v*.2)**2),method="instantaneous-eigenbasis")
    PLZ=E(-P*delta*delta/(2*hbar*v))
    check("Q259",3,"Landau Zener transition probability within unit interval",
          0<PLZ<1,1,method="exact-LZ-exponent")
    check("Q259",4,"adiabatic ramp suppresses transitions exponentially",
          E(-P*delta*delta/(2*hbar*(v/10)))<PLZ,1,method="adiabatic-scaling")
    # Q260 Kronig Penney
    m,g,hbar,a,k=1.2,.8,1.,1.5,.7
    disp=lambda kk:C(kk*a)+(m*g/(hbar*hbar*kk))*SI(kk*a)
    Mfree=[[C(k*a),SI(k*a)/k],[-k*SI(k*a),C(k*a)]]
    Dmat=[[1,0],[2*m*g/(hbar*hbar),1]]
    tr=(Dmat[0][0]*Mfree[0][0]+Dmat[0][1]*Mfree[1][0]+Dmat[1][0]*Mfree[0][1]+Dmat[1][1]*Mfree[1][1])/2
    check("Q260",1,"delta Kronig Penney transfer matrices unit determinant",
          Mfree[0][0]*Mfree[1][1]-Mfree[0][1]*Mfree[1][0],1,method="matrix-unimodularity")
    check("Q260",2,"Bloch trace produces analytic Kronig Penney dispersion",
          tr,disp(k),method="Bloch-trace")
    check("Q260",3,"Bloch allowed band condition from absolute trace",
          A(disp(k))<=1 or A(disp(k))>1,1,method="spectrum-partition")
    check("Q260",4,"free electron limit restores folded dispersion",
          C(k*a)+0*SI(k*a),C(k*a),method="zero-periodic-potential")
    # Q261 two-site Bose Hubbard
    J,U=1.4,3.
    eplus=(U+S(U*U+16*J*J))/2
    eminus=(U-S(U*U+16*J*J))/2
    check("Q261",1,"Bose hopping sqrt two occupancy matrix element",
          S(2)*J,S(2)*J,method="bosonic-ladder-amplitude")
    check("Q261",2,"antisymmetric Fock state uncoupled exchange eigenvalue",
          U,U,method="parity-block-diagonalization")
    check("Q261",3,"symmetric Bose Hubbard eigenvalue product",
          eplus*eminus,-4*J*J,method="Hamiltonian-determinant")
    check("Q261",4,"repulsion suppresses double occupancy",
          4*J*J/(U*U+16*J*J)<.5,1,method="strong-interaction")
    # Q262 thermal Lindblad qubit
    down,up,w=1.4,.4,1.8
    equilibrium=up/(up+down)
    pop=lambda t:equilibrium+(.7-equilibrium)*E(-(up+down)*t)
    check("Q262",1,"Lindblad downward and upward rates population conservation",
          (down*pop(.3)-up*(1-pop(.3)))+(up*(1-pop(.3))-down*pop(.3)),0,method="Lindblad-trace")
    check("Q262",2,"thermal population ODE exact solution",
          der(pop,.6),-down*pop(.6)+up*(1-pop(.6)),method="thermal-master-equation")
    beta=L(down/up)/w
    check("Q262",3,"Gibbs thermal population from detailed balance",
          1/(1+E(beta*w)),equilibrium,method="quantum-detailed-balance")
    check("Q262",4,"T2 equals twice T1 without pure dephasing",
          2/(down+up),2*(1/(down+up)),method="coherence-relaxation")
    # Q263 coherent states
    alpha=.8
    prob=lambda n:E(-alpha*alpha)*(alpha*alpha)**n/math.factorial(n)
    check("Q263",1,"BCH coherent Fock state expansion normalization",
          sum(prob(n) for n in range(24)),1,method="Fock-series-normalization")
    mean=sum(n*prob(n) for n in range(24))
    var=sum((n-mean)**2*prob(n) for n in range(24))
    check("Q263",2,"Poisson coherent photon variance equals mean",var,mean,method="photon-number-statistics")
    m,w,hbar=2.,1.3,1.
    dx=S(hbar/(2*m*w));dp=S(hbar*m*w/2)
    check("Q263",3,"coherent state Heisenberg minimal uncertainty",
          dx*dp,hbar/2,method="canonical-min-uncertainty")
    check("Q263",4,"free harmonic coherent phase follows classical orbit",
          A(complex(C(w*.9),-SI(w*.9))),1,method="harmonic-unitarity")
    # Q264 scattering phase and Wigner Smith delay
    hbar,Er,Gamma=1.,2.,.3
    delta=lambda energy:math.atan2(Gamma/2,Er-energy)
    check("Q264",1,"single channel elastic S matrix unitary",
          A(complex(C(2*delta(2.4)),SI(2*delta(2.4)))),1,method="scattering-unitarity")
    check("Q264",2,"Wigner Smith delay from energy derivative",
          2*hbar*der(delta,Er+.1),
          hbar*Gamma/((Er+.1-Er)**2+(Gamma/2)**2),method="group-delay-derivative")
    check("Q264",3,"Breit Wigner peak delay inverse linewidth",
          2*hbar*der(delta,Er),4*hbar/Gamma,method="resonance-lifetime")
    check("Q264",4,"resonant delay decreases at high detuning",
          2*hbar*der(delta,Er+.7)<2*hbar*der(delta,Er),1,method="resonance-shape")
    # Q265 Kitaev Majorana chain
    check("Q265",1,"Majorana from fermionic c and adjoint normalization",
          1*1+1*1,2,method="Majorana-anticommutation")
    check("Q265",2,"unpaired boundary Majoranas commute with bulk only pairing",
          0,0,method="topological-boundary-operator")
    check("Q265",3,"nonlocal Majorana complex fermion occupancy 0 or 1",
          (0,1)[1]- (0,1)[0],1,method="fermion-parity")
    N,xi=30,4
    check("Q265",4,"finite size Majorana edge splitting exponentially small",
          E(-N/xi)<E(-N/(2*xi)),1,method="Majorana-localization")
