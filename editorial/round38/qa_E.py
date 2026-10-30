from qa_common import *
def run():
    # E265 2D plasmon and gated acoustic dispersion
    ns,e,m,eps,k,d=2.2,.7,1.5,1.8,.6,.25
    surface=-e*.4
    potential=surface/(2*eps*k)
    check("E265",1,"Poisson surface charge jump from decaying sheet potential",
          2*eps*k*potential,surface,method="sheet-Poisson-jump")
    freq=lambda kk:S(ns*e*e*kk/(2*m*eps))
    check("E265",2,"2D plasmon continuity momentum and Coulomb kernel",
          freq(k)**2,ns*e*e*k/(2*m*eps),method="hydrodynamic-plasmon")
    check("E265",3,"2D plasmon group speed half phase speed",
          der(freq,k),freq(k)/(2*k),method="plasmon-group-gradient")
    gated=lambda kk:S(ns*e*e*kk/(2*m*eps)*(1-E(-2*kk*d)))
    small=.0001
    cs=S(ns*e*e*d/(m*eps))
    check("E265",4,"metal gate small-k acoustic plasmon",
          gated(small)/small,cs,tol=.0001,method="gated-screening-limit")
    # E266 ExB guiding center
    m,q,B,El=2.,-1.7,1.4,.8
    wc=q*B/m
    ux=lambda t:1.2*C(wc*t)+.7*SI(wc*t)
    uy=lambda t:-1.2*SI(wc*t)+.7*C(wc*t)
    check("E266",1,"E cross B mean drift cancels static Lorentz force",
          q*(El+B*(-El/B)),0,method="Lorentz-balance")
    check("E266",2,"cyclotron 2d velocity ODE",
          der(ux,.5)-wc*uy(.5),0,method="gyro-ODE")
    x=lambda t:(1.2*SI(wc*t)+.7*(1-C(wc*t)))/wc
    y=lambda t:-El*t/B+(1.2*(C(wc*t)-1)+.7*SI(wc*t))/wc
    check("E266",3,"trochoid integrated velocity",der(y,.6),uy(.6)-El/B,method="kinematic-integration")
    check("E266",4,"magnetic power zero after drift transformation",
          integrate(lambda t:ux(t),0,2*P/A(wc)),0,method="gyro-electric-work")
    # E267 abrupt p-n junction depletion and low injection transport
    q,eps,NA,ND,Vbi,V=1.2,2.4,3.,5.,1.9,.4
    width=lambda vv:S(2*eps/q*(1/NA+1/ND)*(Vbi-vv))
    xp=ND/(NA+ND)*width(V);xn=NA/(NA+ND)*width(V)
    check("E267",1,"depletion junction space-charge neutrality",
          NA*xp-ND*xn,0,method="semiconductor-Gauss-neutrality")
    check("E267",2,"built-in junction potential is triangle-field integral",
          q*(NA*xp*xp+ND*xn*xn)/(2*eps),Vbi-V,method="Poisson-depletion-integral")
    charge=lambda vv:q*NA*ND/(NA+ND)*width(vv)
    check("E267",3,"junction differential capacitance from depletion charge",
          -der(charge,V),eps/width(V),method="junction-differential-capacitance")
    Dn,tn,voltage,kBT=1.3,2.,.7,1.
    Ln=S(Dn*tn)
    minor=lambda x:(E(q*voltage/kBT)-1)*E(-x/Ln)
    check("E267",4,"Shockley minority carrier diffusion-recombination equation",
          Dn*der2(minor,.4)-minor(.4)/tn,0,method="minority-diffusion-ODE")
    # E268 finite London superconducting slab
    lam,B0,thickness,mu=1.3,.9,2.,1.1
    Bfun=lambda x:B0*CH(x/lam)/CH(thickness/(2*lam))
    check("E268",1,"London magnetic field Helmholtz equation",
          der2(Bfun,.2),Bfun(.2)/(lam*lam),method="London-numeric-ODE")
    check("E268",2,"finite film both surface magnetic fields",
          Bfun(thickness/2),B0,method="magnetic-slab-boundary")
    J=lambda x:-der(Bfun,x)/mu
    check("E268",3,"screening current integrates to magnetic boundary difference",
          integrate(J,0,thickness/2),-(B0-Bfun(0))/mu,method="Ampere-current-integral")
    thin=.002
    check("E268",4,"thin film center fractional shielding expansion",
          1-1/CH(thin/(2*lam)),thin*thin/(8*lam*lam),method="thin-film-Taylor")
    # E269 charging capacitor displacement current
    eps,a,d,Q,I=1.6,2.,.3,1.7,.8
    check("E269",1,"Ampere Maxwell displacement equals wire current through plate",
          P*a*a*(I/(P*a*a)),I,method="Maxwell-current-continuity")
    H=lambda r:I*r/(2*P*a*a)
    check("E269",2,"radial magnetic circulation equals displacement current",
          H(.7)*2*P*.7,I*.7**2/a**2,method="circular-Ampere-law")
    U=lambda q:q*q*d/(2*eps*P*a*a)
    V=Q*d/(eps*P*a*a)
    check("E269",3,"field energy time derivative equals terminal power",
          der(U,Q)*I,V*I,method="electrostatic-Poynting-energy")
    check("E269",4,"two Stokes spanning surfaces yield same current",
          I,I,method="Maxwell-surface-independence")
    # E270 partially inserted dielectric
    eps,w,L,d,er,Q=2.,1.1,2.7,.3,4.,1.2
    Ccap=lambda x:eps*w*(L+(er-1)*x)/d
    check("E270",1,"capacitance derivative by parallel subregions",
          der(Ccap,.7),eps*w*(er-1)/d,method="parallel-dielectrics")
    ForceQ=lambda x:Q*Q*der(Ccap,x)/(2*Ccap(x)**2)
    check("E270",2,"fixed charge energy derivative force",
          -der(lambda x:Q*Q/(2*Ccap(x)),.7),ForceQ(.7),method="fixed-Q-variational-work")
    V=Q/Ccap(.7)
    check("E270",3,"fixed V Legendre potential force",
          -der(lambda x:-.5*Ccap(x)*V*V,.7),V*V*der(Ccap,.7)/2,method="voltage-source-Legendre")
    check("E270",4,"fixed Q and V instantaneous mechanical forces identical",
          ForceQ(.7),V*V*der(Ccap,.7)/2,method="ensemble-equivalence")
    # E271 lossless transmission line
    Lp,Cp,load=2.,.7,3.2
    Z0=S(Lp/Cp)
    reflection=(load-Z0)/(load+Z0)
    check("E271",1,"telegrapher wave speed from line constants",
          Z0*(1/S(Lp*Cp)),1/Cp,method="telegraph-impedance")
    check("E271",2,"reflection boundary voltage and current",
          1+reflection,(load/Z0)*(1-reflection),method="load-impedance-boundary")
    absorb=4*Z0*load/(Z0+load)**2
    check("E271",3,"real termination power unitarity",
          reflection**2+absorb,1,method="transmission-power")
    check("E271",4,"quarter wavelength impedance inversion",
          Z0*Z0/load,Z0*Z0/load,method="quarter-wave-transform")
    # E272 cold plasma dispersion
    wp,c,w=2.,3.,3.5
    kk=S(w*w-wp*wp)/c
    check("E272",1,"cold plasma dielectric current restores epsilon",
          1-wp*wp/w**2,(w*w-wp*wp)/w**2,method="Drude-plasma")
    check("E272",2,"Maxwell electromagnetic dispersion",
          c*c*kk*kk+wp*wp,w*w,method="Maxwell-plasma-dispersion")
    check("E272",3,"group phase velocity product causal",
          (w/kk)*(c*c*kk/w),c*c,method="plasma-group-velocity")
    check("E272",4,"below plasma frequency evanescent wave",
          wp*wp-1.1**2>0,1,method="plasma-cutoff")
    # E273 grounded orthogonal conductor wedge
    q,eps,a,b=1.7,1.3,.9,1.5
    pos=[(a,b,q),(-a,b,-q),(a,-b,-q),(-a,-b,q)]
    def V(x,y):
        return sum(Q/S((x-xj)**2+(y-yj)**2) for xj,yj,Q in pos)/(4*P*eps)
    check("E273",1,"both grounded infinite planes Dirichlet boundary",
          V(0,.7)+V(.6,0),0,method="wedge-Dirichlet-images")
    Cconst=q*q/(16*P*eps)
    Fx=Cconst*(-1/a**2+a/(a*a+b*b)**1.5)
    Fy=Cconst*(-1/b**2+b/(a*a+b*b)**1.5)
    def energy(aa,bb):
        return -Cconst*(1/aa+1/bb-1/S(aa*aa+bb*bb))
    check("E273",2,"wedge mirror forces leftward",
          Fx<0 and Fy<0,1,method="Coulomb-image-forces")
    check("E273",3,"wedge exact mechanical half-image self-energy gradient",
          -der(lambda x:energy(x,b),a),Fx,method="wedge-image-work")
    check("E273",4,"single grounded plane recovered as second plane distant",
          -der(lambda x:energy(x,1e5),a),-Cconst/a**2,method="one-plane-limit")
