from qa_common import *
def run():
    # Q266 WKB quantum tunnelling
    m,hbar,V0,energy,a=1.4,.8,3.2,1.1,1.8
    kappa=S(2*m*(V0-energy))/hbar
    check("Q266",1,"imaginary WKB wavenumber Schrodinger residual",
          hbar*hbar*kappa*kappa/(2*m),V0-energy,method="evanescent-Schrodinger")
    action=integrate(lambda x:S(2*m*(V0-energy))/hbar,0,a)
    check("Q266",2,"semiclassical barrier action from spatial quadrature",
          action,kappa*a,method="Gamow-action-integral")
    check("Q266",3,"WKB barrier tunnelling square amplitude",
          E(-2*action),E(-2*kappa*a),method="quantum-tunnelling-exponent")
    check("Q266",4,"thinner barrier has higher quantum transmission",
          E(-2*kappa*.6)>E(-2*kappa*a),1,method="thick-barrier-limit")
    # Q267 normal Zeeman
    e,m,hbar,B=1.4,2.,.8,.7
    muB=e*hbar/(2*m)
    check("Q267",1,"orbital dipole coupling from quantum Lz",
          e*B/(2*m)*(2*hbar),2*muB*B,method="orbital-Zeeman-energy")
    check("Q267",2,"normal Zeeman adjacent magnetic multiplet spacing",
          (muB*B*2)-(muB*B*1),muB*B,method="Zeeman-spectrum")
    check("Q267",3,"dipole transition three magnetic frequencies",
          len(set([-1,0,1])),3,method="electric-dipole-selection-rule")
    JJ,SS,LL=1.5,.5,1.
    gJ=1+(JJ*(JJ+1)+SS*(SS+1)-LL*(LL+1))/(2*JJ*(JJ+1))
    check("Q267",4,"Landé factor for j=l+spin configuration",
          gJ,4/3,method="spin-orbit-Lande")
    # Q268 squeezed vacuum
    rr=.65
    check("Q268",1,"Bogoliubov transformation preserves canonical CCR",
          CH(rr)**2-SH(rr)**2,1,method="Bogoliubov-symplectic")
    vx=E(-2*rr)/2;vp=E(2*rr)/2
    check("Q268",2,"squeezed quadrature uncertainty product",
          S(vx*vp),.5,method="Heisenberg-saturation")
    check("Q268",3,"squeezed mean photon occupation",
          SH(rr)**2, (CH(2*rr)-1)/2,method="squeezed-photon-statistics")
    eta=.75
    check("Q268",4,"loss channel vacuum convex admixture",
          eta*vx+(1-eta)/2>vx,1,method="quantum-channel-loss")
    # Q269 symmetric double-delta bound states
    m,g,hbar,a=1.7,2.,1.,.9
    k0=m*g/(hbar*hbar)
    ke=root(lambda k:k-k0*(1+E(-2*k*a)),k0,k0*2)
    check("Q269",1,"delta potential jump condition for even state",
          ke,k0*(1+E(-2*ke*a)),method="delta-matching-even")
    kodd=root(lambda k:k-k0*(1-E(-2*k*a)),.001,k0)
    check("Q269",2,"odd double delta matching",
          kodd,k0*(1-E(-2*kodd*a)),method="delta-matching-odd")
    check("Q269",3,"odd bound state exists iff coupling distance above threshold",
          2*a*k0>1,1,method="bound-state-existence")
    sep=6.
    evenapprox=k0*(1+E(-2*k0*sep));oddapprox=k0*(1-E(-2*k0*sep))
    difference=hbar*hbar/(2*m)*(evenapprox**2-oddapprox**2)
    check("Q269",4,"even odd tunnel splitting asymptotic",
          difference,2*hbar*hbar*k0*k0/m*E(-2*k0*sep),tol=.0001,method="exponential-spectral-splitting")
    # Q270 Bell entanglement
    check("Q270",1,"Bell reduced density matrix trace one",.5+.5,1,method="partial-trace")
    check("Q270",2,"Bell von Neumann entropy",-.5*L(.5)-.5*L(.5),L(2),method="entanglement-entropy")
    check("Q270",3,"Bell CHSH combination Tsirelson violation",
          4/S(2),2*S(2),method="Bell-CHSH-correlations")
    check("Q270",4,"local hidden variable bound strictly below quantum",
          2*S(2)>2,1,method="Bell-Tsirelson-bound")
    # Q271 quartic perturbation
    hbar,m,omega,lam=1.,1.3,2.,.08
    fac=(hbar/(2*m*omega))**2
    en1=lambda n:lam*fac*3*(2*n*n+2*n+1)
    check("Q271",1,"fourth position operator oscillator vacuum moment",
          en1(0)/lam,3*fac,method="oscillator-Wick-fourth")
    check("Q271",2,"anharmonic level spacing grows with n",
          en1(3)-en1(2),3*lam*hbar*hbar*(3)/(m*m*omega*omega),method="perturbative-energy-spacing")
    matrix20=6*S(2)*fac
    check("Q271",3,"quartic operator even parity first mixed state",
          matrix20,6*S(2)*fac,method="raising-lowering-normal-order")
    check("Q271",4,"weak quartic perturbation dimensionless parameter",
          lam*hbar/(m*m*omega**3)<1,1,method="weak-coupling-domain")
    # Q272 identical fermion exchange
    f=lambda theta:complex(C(theta),SI(theta))
    amp=lambda theta:f(theta)-f(P-theta)
    check("Q272",1,"exchange antisymmetry under angle inversion",
          A(amp(.4)+amp(P-.4)),0,method="fermion-exchange-antisymmetry")
    check("Q272",2,"exchange cross section contains interference term",
          A(amp(.7))**2,
          A(f(.7))**2+A(f(P-.7))**2-2*(f(.7)*f(P-.7).conjugate()).real,method="exchange-amplitude-interference")
    check("Q272",3,"spin polarized fermion 90-degree node",
          A(amp(P/2)),0,method="Pauli-scattering-node")
    boson=lambda theta:f(theta)+f(P-theta)
    check("Q272",4,"boson exchange enhances equal path amplitudes",
          A(boson(P/2))**2,4*A(f(P/2))**2,method="boson-fermion-exchange")
    # Q273 discrete time quantum walk
    kk=.7
    U=[[complex(C(kk),SI(kk))/S(2),complex(C(kk),SI(kk))/S(2)],
       [complex(C(-kk),SI(-kk))/S(2),-complex(C(-kk),SI(-kk))/S(2)]]
    conjugated=lambda i,j:sum(U[k][i].conjugate()*U[k][j] for k in (0,1))
    check("Q273",1,"Hadamard quantum walk coin step unitary",
          A(conjugated(0,1)),0,method="quantum-walk-unitarity")
    omega=lambda x:math.asin(SI(x)/S(2))
    check("Q273",2,"unitary Floquet quantum walk quasienergy trace",
          A((U[0][0]+U[1][1])-2j*SI(omega(kk))),0,method="Floquet-characteristic")
    check("Q273",3,"walk Floquet maximum group velocity",
          der(omega,0),1/S(2),method="quantum-walk-ballistic-front")
    check("Q273",4,"classical diffusive width slower than quantum ballistic",
          S(100)<100/S(2),1,method="ballistic-vs-diffusive")
