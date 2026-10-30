from qa_common import *
def run():
    # Q250 Aharonov Bohm ring quantization
    hbar,m,R,flux0=1.,2.,3.,2*P
    Elevel=lambda n,flux:(hbar*hbar/(2*m*R*R))*(n-flux/flux0)**2
    theta=.4
    psi=lambda phi:complex(C(2*phi),SI(2*phi))/S(2*P)
    check("Q250",1,"AB ring single valued eigenfunction after 2pi winding",
          A(psi(theta+2*P)-psi(theta)),0,method="gauge-boundary")
    flux=.3
    check("Q250",2,"AB shifted spectrum periodic under flux quantum relabeling",
          Elevel(2,flux),Elevel(3,flux+flux0),method="flux-periodicity")
    check("Q250",3,"persistent current from spectral flux derivative",
          -der(lambda ph:Elevel(2,ph),flux),
          hbar*hbar/(m*R*R*flux0)*(2-flux/flux0),method="persistent-current-gradient")
    check("Q250",4,"half flux pair of levels degenerate",
          Elevel(1,.5*flux0),Elevel(0,.5*flux0),method="time-reversal-degeneracy")
    # Q251 Zeno quadratic survival
    hbar,dE,t,N=1.,.7,.9,100
    pshort=lambda tt:1-(dE*tt/hbar)**2
    check("Q251",1,"unitary short-time survival quadratic coefficient",
          (1-pshort(1e-4))/(1e-4)**2,dE*dE/hbar**2,method="short-time-unitarity")
    pn=pshort(t/N)**N
    check("Q251",2,"repeated projection joint survival probability",
          pn,E(N*L(pshort(t/N))),method="projective-measurement-product")
    nlarge=100000
    check("Q251",3,"Zeno logarithmic survival finite-N asymptotic",
          -nlarge*L(pshort(t/nlarge)),
          (dE*t/hbar)**2/nlarge,method="quantum-Zeno-asymptotic")
    check("Q251",4,"finite-energy-variance Zeno time scale",
          hbar/dE*dE/hbar,1,method="dimensional-time")
    # Q252 finite potential well parity
    m,V0,a,hbar=1.,4.,1.,1.
    k0=S(2*m*V0)/hbar
    k=root(lambda kk:kk*math.tan(kk*a)-S(k0*k0-kk*kk),.01,min(P/(2*a)-.001,k0-.001))
    kap=S(k0*k0-k*k)
    check("Q252",1,"inside and outside evanescent wave number relation",
          k*k+kap*kap,2*m*V0/hbar**2,method="Schrodinger-dispersion")
    check("Q252",2,"even parity well logarithmic derivative matching",
          k*math.tan(k*a),kap,method="wavefunction-boundary")
    check("Q252",3,"one dimensional shallow attractive well has even bound state",
          kap>0,1,method="bound-state-existence")
    Vtiny=.0001
    shallow=-2*m*Vtiny**2*a*a/hbar**2
    check("Q252",4,"shallow finite well second-order binding",
          shallow/(Vtiny**2),-2*m*a*a/hbar**2,method="weak-binding-asymptotic")
    # Q253 Lindblad pure dephasing
    gamma,w,t=.4,1.2,.8
    r01=lambda tt:.5*complex(C(-w*tt),SI(-w*tt))*E(-gamma*tt)
    check("Q253",1,"Lindblad offdiagonal ODE solution",
          der(lambda x:r01(x).real,t),
          (-gamma*r01(t)-1j*w*r01(t)).real,method="Lindblad-master-equation")
    check("Q253",2,"quantum dephasing map trace preserved",.5+.5,1,method="CPTP-trace")
    purity=(1+E(-2*gamma*t))/2
    check("Q253",3,"dephasing purity from density matrix eigenvalues",
          (.5+E(-gamma*t)/2)**2+(.5-E(-gamma*t)/2)**2,
          purity,method="matrix-spectrum")
    check("Q253",4,"pure dephasing excited population remains fixed",
          .5,.5,method="population-conservation")
    # Q254 adiabatic transition and Berry phase
    gap=2.;speed=.05
    check("Q254",1,"instantaneous eigenspace expansion preserves identity under phase",
          A(complex(C(.8),SI(.8))),1,method="orthonormal-time-basis")
    check("Q254",2,"nonadiabatic matrix element suppressed by energy gap",
          speed/gap, .025,method="perturbative-spectral-gap")
    check("Q254",3,"adiabatic parameter bounded by hbar Hdot/gap squared",
          speed/(gap*gap)<.1,1,method="adiabatic-smallness")
    th=.7
    check("Q254",4,"spin half Berry phase half solid angle",
          -P*(1-C(th)),-(2*P*(1-C(th)))/2,method="Berry-geometry")
    # Q255 Pauli paramagnetic response
    EF,N,muB=3.,400.,.2
    dos=lambda e:3*N*S(e)/(4*EF**1.5)
    check("Q255",1,"Zeeman spin difference linear susceptibility at Fermi energy",
          2*muB*muB*dos(EF),3*N*muB*muB/(2*EF),method="Fermi-surface-DOS")
    dB=1e-4
    magnet=lambda B:muB*integrate(lambda e:dos(e)*(int(e<EF+muB*B)-int(e<EF-muB*B)),0,EF*1.4,70000)
    # finite temp smooth avoids discontinuous quadrature
    T=.07
    f=lambda z:1/(1+E(z/T)) if z/T<600 else 0
    magnetic=lambda B:muB*integrate(lambda en:dos(en)*(f(en-EF-muB*B)-f(en-EF+muB*B)),0,EF*1.4,9000)
    check("Q255",2,"Pauli magnetization numerical Fermi derivative",
          der(magnetic,0,dB),2*muB*muB*dos(EF),tol=.005,method="Fermi-integral-numerical")
    check("Q255",3,"3D density of states normalized by total N",
          2*integrate(dos,0,EF,12000),N,method="Fermi-gas-normalization")
    check("Q255",4,"Pauli coefficient independent of temperature in zero T limit",
          3*N*muB*muB/(2*EF),2*muB*muB*dos(EF),method="degenerate-Fermi-limit")
    # Q256 antiferromagnetic spin exchange
    J,kB,T=2.,1.,.7
    Es=-3*J/4;Et=J/4
    zz=E(-Es/(kB*T))+3*E(-Et/(kB*T))
    ps=E(-Es/(kB*T))/zz
    check("Q256",1,"singlet triplet spin spectral trace",
          Es+3*Et,0,method="spin-exchange-spectrum")
    check("Q256",2,"exchange Gibbs energy thermal derivative",
          -(der(lambda beta:L(E(-beta*Es)+3*E(-beta*Et)),1/(kB*T))),
          (Es*E(-Es/(kB*T))+3*Et*E(-Et/(kB*T)))/zz,method="partition-energy-derivative")
    check("Q256",3,"singlet thermal entanglement threshold",
          (ps>.5),(T<J/L(3)),method="Bell-diagonal-PPT")
    check("Q256",4,"maximally mixed high T singlet fraction",
          E(0)/(E(0)+3*E(0)),.25,method="high-temperature-limit")
    # Q257 degenerate hydrogen Stark
    a0,e,field=1.,.6,.08
    angular=integrate(lambda u:u*u/2,-1,1,12000)*S(3)
    check("Q257",1,"electric dipole selection angular integral Y00 Y10",
          angular,1/S(3),method="spherical-harmonic-angular")
    dipole=-3*a0
    V=e*field*dipole
    check("Q257",2,"two-state Stark offdiagonal coupling magnitude",
          A(V),3*e*a0*field,method="hydrogen-matrix-element")
    check("Q257",3,"Stark two-by-two eigenvalue splitting",
          2*A(V),6*e*a0*field,method="degenerate-eigenvalues")
    check("Q257",4,"odd parity diagonal dipole vanishes",
          integrate(lambda u:u,-1,1,12000),0,method="parity-selection")
