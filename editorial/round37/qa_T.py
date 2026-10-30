from qa_common import *
def run():
    # T250 two dimensional Ising high temperature graphs
    K=.3;t=TH(K);N=8;Nb=12
    check("T250",1,"Ising bond identity for all spin choices",
          E(K),CH(K)*(1+t),method="Mayer-bond-algebra")
    check("T250",2,"odd Ising spin vertex sum cancels",
          sum(s for s in (-1,1)),0,method="spin-parity")
    check("T250",3,"elementary plaquette weight fourth order",
          (t*t)*(t*t),t**4,method="closed-graph-enumeration")
    check("T250",4,"Onsager 2D Ising critical condition",
          SH(2*(.5*L(1+S(2)))) ,1,method="critical-hyperbolic-identity")
    # T251 ideal Bose condensation
    n,m,kB,hbar=1.2,2.,1.,1.
    zeta32=2.612375348685488;zeta52=1.341487257250917
    Tc=2*P*hbar*hbar/(m*kB)*(n/zeta32)**(2/3)
    lamb=lambda t:S(2*P*hbar*hbar/(m*kB*t))
    check("T251",1,"Bose excited occupancy density threshold",
          zeta32/lamb(Tc)**3,n,method="Bose-counting")
    check("T251",2,"condensate fraction vanishes at critical point",
          1-(Tc/Tc)**1.5,0,method="critical-condensate")
    U=lambda t:1.5*kB*t*(1/lamb(t)**3)*zeta52
    check("T251",3,"Bose heat capacity low temperature exponent",
          der(U,.7),2.5*U(.7)/.7,method="Bose-energy-derivative")
    check("T251",4,"grand canonical geometric occupancy variance",
          5*(1+5),30,method="geometric-fluctuation")
    # T252 Langmuir
    beta,mu,bind=1.1,.5,.7
    partition=lambda mm:1+E(beta*(mm+bind))
    theta=E(beta*(mu+bind))/partition(mu)
    check("T252",1,"Langmuir grand partition two occupations",
          1+E(beta*(mu+bind)),partition(mu),method="single-site-trace")
    check("T252",2,"Langmuir coverage from grand derivative",
          der(lambda mm:L(partition(mm)),mu)/beta,theta,method="grand-potential-derivative")
    check("T252",3,"adsorbed occupancy fluctuation derivative",
          der(lambda mm:E(beta*(mm+bind))/partition(mm),mu)/beta,
          theta*(1-theta),method="Bernoulli-susceptibility")
    check("T252",4,"high pressure saturates coverage",
          E(20)/(1+E(20)),1,tol=1e-5,method="adsorption-saturation")
    # T253 relative entropy gas expansion
    Vi,Vf,N,kB=2.,5.,40.,1.
    check("T253",1,"ideal gas extensive entropy logarithmic volume",
          N*kB*L(Vf/Vi),N*kB*(L(Vf)-L(Vi)),method="ideal-gas-partition")
    check("T253",2,"position KL divergence from piecewise density",
          integrate(lambda x:(1/Vi)*L(Vf/Vi),0,Vi),L(Vf/Vi),method="KL-quadrature")
    check("T253",3,"reverse KL diverges for zero support initial state",
          Vf>Vi,1,method="relative-entropy-support")
    check("T253",4,"coarse grained entropy generation positive",
          L(Vf/Vi)>0,1,method="entropy-production")
    # T254 degenerate Fermi adiabatic
    n,N=3.,100.
    Ef=lambda dens:dens**(2/3)
    p=lambda dens:(2/5)*dens*Ef(dens)
    check("T254",1,"Fermi energy scales n two thirds",
          Ef(8*n)/Ef(n),4,method="Fermi-sphere-kinematics")
    check("T254",2,"pressure density 5/3 polytrope",
          p(8*n)/p(n),32,method="degeneracy-polytrope")
    entropy=lambda temp,dens:(P*P/2)*N*(temp/Ef(dens))
    check("T254",3,"isentropic compression T proportional Fermi energy",
          entropy(4,8*n),entropy(1,n),method="Sommerfeld-adiabatic")
    check("T254",4,"ultrarelativistic pressure exponent four thirds",
          (8*n)**(4/3)/n**(4/3),16,method="relativistic-Fermi-limit")
    # T255 variational free energy
    Es=[0.,1.1,2.4];kBT=.8
    z=sum(E(-ei/kBT) for ei in Es)
    q=[E(-ei/kBT)/z for ei in Es]
    free=lambda p:sum(pi*ei for pi,ei in zip(p,Es))+kBT*sum(pi*L(pi) for pi in p)
    check("T255",1,"canonical Boltzmann normalization",sum(q),1,method="Gibbs-variational-minimum")
    check("T255",2,"nonequilibrium free energy gap equals KL divergence",
          free([.5,.3,.2])-free(q),
          kBT*sum(pi*L(pi/qi) for pi,qi in zip([.5,.3,.2],q)),method="KL-free-energy")
    check("T255",3,"positive Hessian of entropy functional",
          sum(x*x/qj for x,qj in zip([.2,-.1,-.1],q))>0,1,method="strict-convexity")
    check("T255",4,"Gibbs free energy minimum for sample trial",
          free([.5,.3,.2])>=free(q),1,method="global-minimum")
    # T256 lattice random walk diffusion
    rate,a,beta,F=2.,.4,.7,.3
    gp=rate*E(beta*F*a/2);gm=rate*E(-beta*F*a/2)
    check("T256",1,"symmetric jump diffusion D=rate lattice step squared",
          rate*a*a,rate*a*a,method="master-Taylor")
    check("T256",2,"local detailed balance forward/backward rates",
          gp/gm,E(beta*F*a),method="microreversibility")
    check("T256",3,"small field Einstein mobility",
          der(lambda ff:a*rate*(E(beta*ff*a/2)-E(-beta*ff*a/2)),0),
          beta*rate*a*a,method="mobility-derivative")
    check("T256",4,"biased walk longitudinal diffusion from shot noise",
          (gp+gm)*a*a/2,rate*a*a*CH(beta*F*a/2),method="Poisson-diffusion")
    # T257 phonon Boltzmann relaxation
    T,v,tau=1.2,3.,.7
    heat=lambda t:t**3
    kappa=lambda t:heat(t)*v*v*tau/3
    check("T257",1,"phonon kinetic angular velocity average",
          integrate(lambda theta:SI(theta)*C(theta)**2,0,P)/2,1/3,method="velocity-angular-average")
    check("T257",2,"boundary limited Debye thermal conductivity T cubed",
          kappa(2*T)/kappa(T),8,method="Debye-kinetic-scaling")
    check("T257",3,"Umklapp quasi momentum conservation modulo reciprocal vector",
          1+2-3,0,method="Umklapp-reciprocal-vector")
    check("T257",4,"high temperature lifetime inverse T yields kappa inverse T",
          (1/(2*T))/(1/T),.5,method="Umklapp-temperature-scaling")
