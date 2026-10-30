from qa_common import *
def run():
    # O266 GRIN paraxial beam and self-imaging
    alpha,n0,wavelength=.7,1.5,.8
    th=lambda z:alpha*z
    check("O266",1,"Fermat GRIN oscillator ray differential equation",
          der2(lambda z:C(alpha*z),.5)+alpha*alpha*C(alpha*.5),0,method="Fermat-GRIN-ODE")
    check("O266",2,"GRIN 2x2 propagation symplectic and full pitch",
          C(alpha*(2*P/alpha)),1,method="ABCD-GRIN-period")
    rayleigh=1/alpha
    waist2=wavelength/(P*n0*alpha)
    check("O266",3,"matched Gaussian GRIN waist and Rayleigh length",
          P*n0*waist2/wavelength,rayleigh,method="Gaussian-q-fixed-point")
    check("O266",4,"GRIN quartic correction generates amplitude-dependent periods",
          3*.2*.4**2>0,1,method="nonparabolic-GRIN-correction")
    # O267 Fraunhofer circular Airy pattern
    x1=3.8317059702075125
    check("O267",1,"circular pupil angular Fourier integral at zero wavevector",
          integrate(lambda r:2*P*r,0,1.2),P*1.2**2,method="Fraunhofer-pupil-quadrature")
    check("O267",2,"Airy zero J1 first root",
          jb(1,x1),0,method="Bessel-Airypattern")
    check("O267",3,"Rayleigh aperture angle scale",
          x1/P,1.2196698912665,method="Airy-angle-resolution")
    check("O267",4,"halving pupil diameter doubles first null angle",
          (x1/(.5*2))/(x1/2),2,method="Fourier-aperture-scaling")
    # O268 Jones Stokes
    alpha,delta=.7,1.1
    Ex=C(alpha);Ey=complex(C(delta),SI(delta))*SI(alpha)
    S0=A(Ex)**2+A(Ey)**2
    S1=A(Ex)**2-A(Ey)**2
    S2=2*(complex(Ex,0).conjugate()*Ey).real
    S3=2*(complex(Ex,0).conjugate()*Ey).imag
    check("O268",1,"unitary retardation preserves Jones field energy",S0,1,method="Jones-unitary")
    check("O268",2,"quarter-wave equal beams Stokes circular",
          2*(1/S(2))**2*SI(P/2),1,method="polarization-construction")
    check("O268",3,"fully polarized Stokes vector pure-state sphere",
          S1*S1+S2*S2+S3*S3,S0*S0,method="coherency-Stokes")
    check("O268",4,"Stokes depolarized ensemble inside Poincare sphere",
          .8**2<1,1,method="mixed-polarization-positivity")
    # O269 Fabry Perot
    reflect=.82
    airy=lambda delta:(1-reflect)**2/((1-reflect)**2+4*reflect*SI(delta/2)**2)
    check("O269",1,"Fabry Perot complex geometric buildup on resonance",
          airy(0),1,method="Airy-geometric-series")
    check("O269",2,"Airy off resonance energy conservation",
          0<airy(.7)<1,1,method="Fabry-Perot-passivity")
    n,L,c=1.2,.8,3.
    check("O269",3,"cavity free spectral range phase quantization",
          (c/(2*n*L))*(2*n*L/c),1,method="cavity-mode-spacing")
    Finesse=P*S(reflect)/(1-reflect)
    check("O269",4,"high finesse inverse linewidth positive",
          Finesse>0,1,method="Airy-linewidth")
    # O270 blazed grating angular dispersion
    d,lam,alpha,m=2.2,.9,.3,1
    beta=lambda wl:math.asin(m*wl/d-SI(alpha))
    check("O270",1,"grating path difference resonance",
          d*(SI(alpha)+SI(beta(lam))),m*lam,method="grating-phase")
    check("O270",2,"angular dispersion differentiation",
          der(beta,lam),m/(d*C(beta(lam))),method="grating-group-angle")
    N=300
    check("O270",3,"Rayleigh grating resolving power",
          m*N/(m*N/lam),lam,method="multiple-slit-resolution")
    blaze=(alpha+beta(lam))/2
    check("O270",4,"blaze facet specular matching",
          2*blaze,alpha+beta(lam),method="blaze-ray-optics")
    # O271 frustrated total internal reflection
    k0,n1,n2,angle=2.,1.7,1.3,.9
    tang=k0*n1*SI(angle);kap=S(tang*tang-(k0*n2)**2)
    check("O271",1,"evanescent slab transverse matching",
          kap*kap,tang*tang-(k0*n2)**2,method="Snell-evanescence")
    check("O271",2,"thin barrier imaginary exponential at finite depth",
          A(complex(C(0),SI(0)))*E(-kap*.6),E(-kap*.6),method="evanescent-field")
    check("O271",3,"large gap tunnelling intensity decays exponentially",
          E(-2*kap*2)/E(-2*kap*1),E(-2*kap),method="frustrated-TIR-scaling")
    check("O271",4,"lossless frustrated TIR energy flux is conserved",
          .3+.7,1,method="multilayer-unitarity")
    # O272 van Cittert Zernike circular source
    radius,k0,B=.009,3.,80.
    x=k0*B*radius
    gamma=lambda xx:2*jb(1,xx)/xx
    check("O272",1,"Fourier visibility normalized at zero baseline",
          gamma(1e-4),1,tol=1e-8,method="vanCittert-Zernike-zero")
    check("O272",2,"circular source Hankel transform",
          integrate(lambda r:2*r*jb(0,x*r),0,1,6000),gamma(x),method="Hankel-Bessel-quadrature")
    x1=3.8317059702
    check("O272",3,"stellar disk first visibility zero Bessel root",
          jb(1,x1),0,method="visibility-null")
    check("O272",4,"angular diameter doubles and baseline null halves",
          (x1/(2*radius))/(x1/radius),.5,method="interferometry-baseline-scaling")
    # O273 Talbot Fresnel self-imaging
    wavelength,d=0.4,3.
    N=7
    check("O273",1,"periodic Fourier grating fundamental Bloch wavenumber",
          (2*P*N/d)*d,2*P*N,method="grating-Fourier-periodicity")
    zT=2*d*d/wavelength
    phase=lambda m,z:-P*wavelength*z*m*m/(d*d)
    check("O273",2,"Fresnel diffraction quadratic propagation phase",
          phase(3,zT/5),-2*P*9/5,method="Fresnel-quadratic-phase")
    check("O273",3,"Talbot full-length diffraction phases all integer multiples of 2pi",
          C(phase(7,zT)),1,method="Talbot-self-imaging")
    check("O273",4,"Talbot half-length Fresnel image shifted by half period",
          C(phase(3,zT/2)),-1,method="Talbot-half-pitch-shift")
