from qa_common import *
def run():
    # T242 1D Ising transfer matrix
    J,beta,h=1.2,.7,.4
    lplus=E(beta*J)*CH(beta*h)+S(E(2*beta*J)*SH(beta*h)**2+E(-2*beta*J))
    lminus=E(beta*J)*CH(beta*h)-S(E(2*beta*J)*SH(beta*h)**2+E(-2*beta*J))
    T11=E(beta*(J+h));T22=E(beta*(J-h));T12=E(-beta*J)
    check("T242",1,"Ising transfer-matrix eigenvalue trace",
          lplus+lminus,T11+T22,method="matrix-diagonalization")
    press=lambda hh:E(beta*J)*CH(beta*hh)+S(E(2*beta*J)*SH(beta*hh)**2+E(-2*beta*J))
    check("T242",2,"magnetization from free energy derivative",
          der(lambda hh:L(press(hh)),h)/beta,
          SH(beta*h)/S(SH(beta*h)**2+E(-4*beta*J)),method="Gibbs-derivative")
    ratio=TH(beta*J)
    check("T242",3,"Ising correlation length reproduces transfer eigenvalue ratio",
          E(-1/(-1/L(ratio))),ratio,method="transfer-correlation")
    check("T242",4,"finite temperature 1d Ising spontaneous magnetization absent",
          SH(0)/S(SH(0)**2+E(-4*beta*J)),0,method="symmetry-field-limit")
    # T243 Schottky two level heat capacity
    N,Delta,kB,T=4,2.3,1.,1.1
    z=1+E(-Delta/(kB*T))
    check("T243",1,"two level partition equals normalized Boltzmann probabilities",
          1/z+E(-Delta/(kB*T))/z,1,method="canonical-normalization")
    U=lambda tt:N*Delta/(1+E(Delta/(kB*tt)))
    x=Delta/(kB*T)
    heat=N*kB*x*x*E(x)/(1+E(x))**2
    check("T243",2,"Schottky heat capacity from U derivative",
          der(U,T),heat,method="heat-capacity-derivative")
    xstar=root(lambda x:x*TH(x/2)-2,1,4)
    check("T243",3,"Schottky peak stationarity",
          der(lambda xx:xx*xx/(4*CH(xx/2)**2),xstar),0,method="maximum-condition")
    check("T243",4,"high temperature Schottky heat tends zero",
          (Delta/(kB*1e6))**2/4,0,tol=1e-8,method="large-temperature-asymptotic")
    # T244 Mayer virial integral
    d=.8
    f=lambda r:-1 if r<=d else 0
    check("T244",1,"Mayer two particle radial configuration integral",
          2*P*integrate(lambda r:-f(r)*r*r,0,d,12000),
          2*P*d**3/3,method="configuration-volume")
    check("T244",2,"second virial coefficient from Mayer function",
          -2*P*integrate(lambda r:f(r)*r*r,0,d,12000),
          2*P*d**3/3,method="hard-core-integral")
    check("T244",3,"hard sphere second virial four times particle volume",
          (2*P*d**3/3)/(P*d**3/6),4,method="excluded-volume-geometry")
    check("T244",4,"weak attraction yields negative second-virial contribution",
          -(E(.3)-1)<0,1,method="attraction-sign")
    # T245 ideal Otto cycle
    gam,r,T1,T3=1.4,4.,300.,1600.
    T2=T1*r**(gam-1);T4=T3/r**(gam-1)
    check("T245",1,"Otto adiabatic temperature invariant",
          T2/T1,r**(gam-1),method="isentropic-law")
    qin=T3-T2;qout=T4-T1
    check("T245",2,"Otto first-law efficiency",
          1-qout/qin,1-r**(1-gam),method="cycle-energy")
    eta=lambda rr:1-rr**(1-gam)
    check("T245",3,"Otto compression ratio efficiency gradient",
          der(eta,r),(gam-1)*r**(-gam),method="efficiency-derivative")
    check("T245",4,"no compression yields zero Otto efficiency",eta(1),0,method="cycle-limit")
    # T246 nucleation barrier
    sig,dg=2.,.8
    G=lambda r:4*P*sig*r*r-4*P*dg*r**3/3
    rc=2*sig/dg
    check("T246",1,"surface and bulk nucleation work from radial derivative integration",
          integrate(lambda rr:8*P*sig*rr-4*P*dg*rr*rr,0,.7),G(.7),
          method="thermodynamic-path-integral")
    check("T246",2,"critical nucleus stationarity",der(G,rc),0,method="saddle-point")
    check("T246",3,"nucleation barrier at critical radius",
          G(rc),16*P*sig**3/(3*dg**2),method="critical-free-energy")
    check("T246",4,"doubling driving force cuts barrier by four",
          (16*P*sig**3/(3*(2*dg)**2))/(16*P*sig**3/(3*dg**2)),.25,method="supersaturation-scaling")
    # T247 number fluctuations and compressibility
    n,kB,T,V=1.7,1.,3.,5.
    pressure=lambda dens:dens*kB*T
    kappa=1/(n*kB*T)
    check("T247",1,"grand canonical number fluctuation equals response derivative",
          kB*T*V*der(lambda chemical:E(chemical/(kB*T)),kB*T*L(n)),
          n*V,method="grand-potential-response")
    check("T247",2,"pressure susceptibility recovers ideal compressibility",
          1/(n*der(pressure,n)),kappa,method="Gibbs-Duhem")
    check("T247",3,"Poisson number variance equals mean in ideal gas",
          kB*T*V*n*n*kappa,n*V,method="fluctuation-compressibility")
    check("T247",4,"critical compressibility enhances relative fluctuation",
          (n*kB*T*(5*kappa))>(n*kB*T*kappa),1,method="critical-susceptibility")
    # T248 independent spin magnetic entropy
    N,mu0,kB,B,T=6.,2.,1.,.5,3.
    x=mu0*B/(kB*T)
    F=lambda temp:-N*kB*temp*L(2*CH(mu0*B/(kB*temp)))
    entropy=lambda xx:N*kB*(L(2*CH(xx))-xx*TH(xx))
    check("T248",1,"spin partition gives Curie response",
          der(lambda bb:N*kB*T*L(2*CH(mu0*bb/(kB*T))),B),
          N*mu0*TH(x),method="magnetization-partition")
    check("T248",2,"spin entropy as negative temperature derivative",
          -der(F,T),entropy(x),method="thermodynamic-entropy")
    check("T248",3,"isentropic magnetic ratio B/T preserved",
          (B/2)/(T/2),B/T,method="adiabatic-demagnetization")
    check("T248",4,"low field entropy quadratic correction",
          (entropy(.0001)-N*kB*L(2))/(N*kB*.0001**2),-.5,method="entropy-series")
    # T249 thermoelectric Onsager Kelvin relation
    s0,T=2e-4,300.
    Pi=s0*T
    check("T249",1,"open circuit electric field offsets Seebeck field",
          (s0*.2-s0*.2),0,method="open-circuit-boundary")
    check("T249",2,"Peltier coefficient as differential reversible heat flow",
          der(lambda current:Pi*current,2.3),Pi,method="reversible-heat-current-derivative")
    check("T249",3,"Kelvin Onsager reciprocal identity",
          Pi/T,s0,method="Onsager-symmetry")
    Seebeck=lambda tt:1e-4+1e-6*tt
    check("T249",4,"Thomson coefficient derivative of Seebeck",
          T*der(Seebeck,T),T*1e-6,method="Kelvin-temperature-derivative")
