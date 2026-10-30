from qa_common import *

def run():
    # O242 Airy diffraction circular aperture
    a,wl=2.,.4;k=2*P/wl;theta=.1
    x=k*a*SI(theta)
    airy=2*jb(1,x)/x
    numer=2/a**2*integrate(lambda r:r*jb(0,k*r*SI(theta)),0,a,12000)
    check("O242",1,"Fraunhofer circular aperture Bessel integral",airy,numer,method="radial-Fourier-Bessel")
    tiny=.00001
    check("O242",2,"Airy center intensity normalized to unity",
          2*jb(1,tiny)/tiny,1,method="Bessel-series-limit")
    jroot=3.8317059702075125
    check("O242",3,"first Airy zero J1 root",jb(1,jroot),0,method="Bessel-root")
    check("O242",4,"Rayleigh angle inverse diameter scaling",
          (jroot/(k*(2*a)))/(jroot/(k*a)),.5,method="aperture-scaling")
    # O243 quarter-wave antireflection
    n0,n2=1.,2.25;n1=S(n0*n2);delta=P/2
    r01=(n0-n1)/(n0+n1);r12=(n1-n2)/(n1+n2)
    rt=(r01+r12*complex(C(2*delta),SI(2*delta)))/(1+r01*r12*complex(C(2*delta),SI(2*delta)))
    check("O243",1,"two Fresnel interface amplitudes match",r01-r12,0,method="Fresnel-impedance")
    check("O243",2,"quarter-wave roundtrip phase equals minus unity",C(2*delta),-1,method="film-optical-phase")
    check("O243",3,"ideal single-layer AR coating zero reflection",A(rt),0,method="multiple-reflection-amplitude")
    check("O243",4,"zero-index contrast yields zero reflection", (n0-n0)/(n0+n0),0,method="index-match-limit")
    # O244 waveplate Jones and Stokes
    alpha=.7;delta=P/2;Pha=P/2
    ex=complex(C(delta/2),SI(delta/2))*C(alpha)
    ey=complex(C(delta/2),-SI(delta/2))*SI(alpha)
    stQ=A(ex)**2-A(ey)**2
    stU=2*(ex*ey.conjugate()).real
    stV=2*(ex*ey.conjugate()).imag
    check("O244",1,"lossless waveplate conserves Jones norm",A(ex)**2+A(ey)**2,1,method="Jones-unitarity")
    check("O244",2,"waveplate phase converts diagonal linear to circular",
          2*(complex(C(Pha/2),SI(Pha/2))/S(2)*
           complex(C(Pha/2),SI(Pha/2))/S(2)).imag,1,method="Stokes-circular")
    check("O244",3,"Stokes vector remains fully polarized",
          stQ*stQ+stU*stU+stV*stV,1,method="Stokes-purity")
    check("O244",4,"crossed x analyzer intensity independent retardance",A(ex)**2,C(alpha)**2,method="projection-measurement")
    # O245 Gaussian temporal coherence
    nu0,sigma,tau=2.,.3,.8
    gau=lambda nu:E(-(nu-nu0)**2/(2*sigma*sigma))
    denom=integrate(gau,nu0-9*sigma,nu0+9*sigma)
    real=integrate(lambda nu:gau(nu)*C(2*P*nu*tau),nu0-9*sigma,nu0+9*sigma)/denom
    imag=integrate(lambda nu:gau(nu)*SI(2*P*nu*tau),nu0-9*sigma,nu0+9*sigma)/denom
    gam=complex(real,imag)
    check("O245",1,"spectral Fourier transform yields complex temporal coherence",
          A(gam),E(-2*P*P*sigma*sigma*tau*tau),method="Wiener-Khinchin-quadrature")
    check("O245",2,"Gaussian coherence peak normalized at zero delay",
          integrate(gau,nu0-9*sigma,nu0+9*sigma)/denom,1,method="spectral-normalization")
    tc=1/(S(2)*P*sigma)
    check("O245",3,"Gaussian coherence 1/e time",
          E(-2*P*P*sigma*sigma*tc*tc),1/E(1),method="coherence-envelope")
    i1,i2=1.,4.
    check("O245",4,"unequal arm visibility less than unity",
          2*S(i1*i2)/(i1+i2),.8,method="fringe-visibility")
    # O246 Rayleigh optical tweezers
    em,ep,a=2.,5.,.05
    pol=lambda r:4*P*em*r**3*(ep-em)/(ep+2*em)
    check("O246",1,"Clausius-Mossotti polarizability positive contrast",
          pol(a)>0,1,method="static-polarization")
    waist=1.2
    intensity=lambda r:E(-2*r*r/(waist*waist))
    r=.2
    check("O246",2,"optical gradient force points inward toward Gaussian maximum",
          pol(a)*der(intensity,r)<0,1,method="gradient-force")
    sca=lambda r:(2*P)**4*pol(r)**2/(6*P*em*em)
    check("O246",3,"Rayleigh scattering force grows as sixth power of radius",
          sca(2*a)/sca(a),64,method="dipole-radiation-scaling")
    check("O246",4,"low-index particle polarizability changes sign",
          4*P*em*a**3*(.5*em-em)/(.5*em+2*em)<0,1,method="contrast-reversal")
    # O247 dark state and slow light
    OmP,OmC=.3,1.2
    norm=S(OmP*OmP+OmC*OmC)
    dark1=OmC/norm;dark2=-OmP/norm
    check("O247",1,"EIT dark state has no excited component",
          OmP*dark1+OmC*dark2,0,method="Hamiltonian-nullvector")
    check("O247",2,"dark state unit normalized",
          dark1*dark1+dark2*dark2,1,method="state-normalization")
    n0,omega0,slope=1.1,4.,2.3
    kfun=lambda w:(n0+slope*(w-omega0))*w
    ng=der(kfun,omega0)
    check("O247",3,"slow light group index from dispersive derivative",
          ng,n0+omega0*slope,method="group-velocity-derivative")
    check("O247",4,"large control field widens EIT transparency and decreases delay",
          1/(2*OmC)**2<1/OmC**2,1,method="control-field-scaling")
    # O248 phase modulation Fourier Bessel
    beta=.8
    js=[jb(abs(n),beta)*(1 if n>=0 else (-1)**abs(n)) for n in range(-10,11)]
    check("O248",1,"Jacobi-Anger harmonics reconstruct phase modulation at t=pi/2",
          A(sum(js[n+10]*complex(C(n*P/2),SI(n*P/2)) for n in range(-10,11))-
            complex(C(beta),SI(beta))),0,method="Fourier-reconstruction")
    check("O248",2,"first order upper and lower sideband parity",
          js[9]+js[11],0,method="Bessel-parity")
    check("O248",3,"Bessel optical phase modulation power remains one",
          sum(j*j for j in js),1,method="Parseval-power")
    check("O248",4,"Bessel sideband frequency variance beta squared over two",
          sum((n*n)*js[n+10]**2 for n in range(-10,11)),beta**2/2,method="spectrum-second-moment")
    # O249 vortex optical OAM
    ell=3
    phase=lambda phi:ell*phi
    check("O249",1,"vortex phase winding closed loop",
          phase(2*P)-phase(0),2*P*ell,method="topological-winding")
    check("O249",2,"azimuthal phase gradient winding rate",
          der(phase,.7),ell,method="phase-gradient")
    check("O249",3,"on-axis vortex intensity scales to zero for nonzero charge",
          (.00001)**(2*A(ell)),0,tol=1e-10,method="dark-core-limit")
    check("O249",4,"opposite vortex charge reverses angular momentum",
          der(lambda phi:-ell*phi,.7),-ell,method="OAM-sign")
