from qa_common import *

def run():
    # Q242 double attractive delta level splitting
    kappa0,a=1.3,3.
    even=root(lambda k:k-kappa0*(1+E(-2*k*a)),kappa0,2*kappa0)
    odd=root(lambda k:k-kappa0*(1-E(-2*k*a)),.0001,kappa0)
    check("Q242",1,"symmetric double-delta even derivative matching",
          even/kappa0-1,E(-2*even*a),method="point-interaction-boundary")
    check("Q242",2,"odd state derivative matching",
          1-odd/kappa0,E(-2*odd*a),method="antisymmetric-boundary")
    check("Q242",3,"double-well tunneling splitting exponential order",
          (even*even-odd*odd)/(4*kappa0*kappa0*E(-2*kappa0*a)),1,tol=.002,method="asymptotic-level-splitting")
    check("Q242",4,"odd bound state exists for 2a kappa0 above unity",
          2*a*kappa0>1,1,method="critical-bound-state")
    # Q243 spin Berry geometric phase
    theta=.8
    berry=-SI(theta/2)**2
    check("Q243",1,"adiabatic spin eigenenergies for normalized field",
          S(C(theta)**2+SI(theta)**2),1,method="spin-Pauli-spectrum")
    h=1e-5
    spin=lambda phi:(C(theta/2),complex(C(phi),SI(phi))*SI(theta/2))
    u=spin(.3)
    du=tuple((spin(.3+h)[i]-spin(.3-h)[i])/(2*h) for i in range(2))
    connection=(1j*(u[0].conjugate()*du[0]+u[1].conjugate()*du[1])).real
    check("Q243",2,"Berry connection from eigenstate finite derivative",connection,berry,method="spinor-derivative")
    check("Q243",3,"closed loop Berry phase equals half solid angle",
          2*P*connection,-P*(1-C(theta)),method="geometric-holonomy")
    check("Q243",4,"north pole loop vanishes",
          -P*(1-C(0)),0,method="pole-limit")
    # Q244 Ramsey dephasing
    Gam,t,phi=.4,1.2,.9
    V=E(-Gam*t)
    check("Q244",1,"dephased Ramsey density eigenvalues",
          (1+V)/2+(1-V)/2,1,method="density-trace")
    prob=lambda x:(1+V*C(x))/2
    check("Q244",2,"Ramsey fringe complementary outcomes",
          prob(phi)+1-prob(phi),1,method="POVM-probability")
    phi0=P/2
    fisher=(der(prob,phi0)**2)/(prob(phi0)*(1-prob(phi0)))
    check("Q244",3,"optimal phase Fisher information from Bernoulli likelihood",
          fisher,V*V,method="likelihood-information")
    check("Q244",4,"frequency information optimal time for fixed shot",
          der(lambda tt:tt*tt*E(-2*Gam*tt),1/Gam),0,method="time-optimization")
    # Q245 harmonic oscillator thermal partition
    hbar,om,kB,T=1.,2.4,1.,1.8
    x=hbar*om/(kB*T)
    z=1/(2*SH(x/2))
    check("Q245",1,"harmonic thermal partition exact geometric sum",
          sum(E(-x*(n+.5)) for n in range(80)),z,method="quantum-partition-sum")
    U=lambda temp:hbar*om/2*(CH(hbar*om/(2*kB*temp))/SH(hbar*om/(2*kB*temp)))
    Cv=der(U,T)
    check("Q245",2,"oscillator heat capacity from Bose occupations",
          Cv,kB*x*x*E(x)/(E(x)-1)**2,method="heat-capacity-derivative")
    nB=1/(E(x)-1)
    check("Q245",3,"energy fluctuation canonical heat capacity identity",
          (hbar*om)**2*nB*(1+nB),kB*T*T*Cv,method="canonical-fluctuation")
    m=2.
    varx=hbar*(2*nB+1)/(2*m*om);varp=hbar*m*om*(2*nB+1)/2
    check("Q245",4,"thermal Heisenberg product",
          S(varx*varp),hbar*(2*nB+1)/2,method="uncertainty-product")
    # Q246 Landau states and Hall effect
    ee,B,m,hbar,area=1.4,2.3,3.,.8,8.
    wc=ee*B/m
    check("Q246",1,"Landau harmonic spacing",hbar*wc*(2.5-1.5),hbar*wc,method="Landau-ladder")
    h=2*P*hbar;Nphi=ee*B*area/h
    check("Q246",2,"Landau degeneracy from magnetic length",
          area/(2*P*(hbar/(ee*B))),Nphi,method="magnetic-flux-counting")
    nu=3
    density=lambda BB:nu*ee*BB/h
    check("Q246",3,"Streda Hall conductance from density derivative",
          ee*der(density,B),nu*ee*ee/h,method="Streda-density-derivative")
    check("Q246",4,"Landau gap vanishes when B goes to zero",
          ee*.0000001/m,0,tol=1e-6,method="zero-field-spectrum")
    # Q247 Helstrom state discrimination
    s=.6
    delta=S(1-s*s)
    check("Q247",1,"equal-prior difference of two pure state projectors has trace zero",
          (1-s*s- (1-s*s))/2,0,method="operator-trace")
    check("Q247",2,"Helstrom two eigenvalues give trace norm",
          2*(delta/2),delta,method="trace-norm-spectrum")
    check("Q247",3,"orthogonal state minimal error goes to zero",
          (1-S(1-0*0))/2,0,method="orthogonal-limit")
    n=5
    check("Q247",4,"n-copy state overlap yields exponentially smaller error",
          (1-S(1-s**(2*n)))/2 < (1-S(1-s*s))/2,1,method="tensor-product-overlap")
    # Q248 SSH band topology
    v,w,a=.5,1.2,1.
    Es=lambda k:S(v*v+w*w+2*v*w*C(k*a))
    check("Q248",1,"SSH gap at zone edge",
          2*Es(P/a),2*A(v-w),method="Bloch-eigenvalues")
    # compute winding from argument increments with phase unwrap
    angles=[]
    for j in range(4001):
        k=-P/a+2*P/a*j/4000
        z=complex(v+w*C(k*a),w*SI(k*a))
        angles.append(math.atan2(z.imag,z.real))
    total=0
    for left,right in zip(angles,angles[1:]):
        delta=right-left
        if delta>P:delta-=2*P
        elif delta<-P:delta+=2*P
        total+=delta
    check("Q248",2,"SSH winding from discretized complex Bloch loop",total/(2*P),1,method="topological-angle-unwrapping")
    ratio=v/w
    check("Q248",3,"SSH edge state decays normally with geometric ratio",
          (1-ratio*ratio)*sum(ratio**(2*n) for n in range(100)),1,method="edge-normalization")
    check("Q248",4,"edge state localization length diverges near critical v=w",
          1/L(1/.999)>1/L(1/.5),1,method="topological-criticality")
    # Q249 sudden oscillator quench
    wi,wf=2.,3.7
    alpha=(S(wf/wi)+S(wi/wf))/2
    beta=(S(wf/wi)-S(wi/wf))/2
    check("Q249",1,"Bogoliubov canonical commutator preserved",
          alpha*alpha-beta*beta,1,method="canonical-transformation")
    check("Q249",2,"sudden quench created excitation count",
          beta*beta,(wf/wi+wi/wf-2)/4,method="squeezing-occupation")
    check("Q249",3,"new Hamiltonian energy after instantaneous quench",
          wf*(beta*beta+.5),(wf*wf+wi*wi)/(4*wi),method="sudden-energy")
    check("Q249",4,"quench injected work equals stiffness change in old ground state",
          wf*(beta*beta+.5)-wi/2,(wf*wf-wi*wi)/(4*wi),method="quench-work")
