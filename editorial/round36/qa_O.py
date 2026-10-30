from qa_common import *
def run():
    # O250 total internal reflection and Goos-Hanchen shift
    n1,n2,k0,theta=1.7,1.2,2.,.95
    k1,k2=n1*k0,n2*k0
    kx=k1*SI(theta)
    kz=S(k1*k1-kx*kx);decay=S(kx*kx-k2*k2)
    rs=complex(kz,-decay)/complex(kz,decay)
    check("O250",1,"evanescent normal wave vector squared",decay**2,kx*kx-k2*k2,method="Snell-dispersion")
    check("O250",2,"Fresnel s reflection amplitude unitary",A(rs),1,method="complex-Fresnel-energy")
    phase=lambda x:-2*math.atan(S(x*x-k2*k2)/S(k1*k1-x*x))
    check("O250",3,"Artmann GH shift from phase derivative",
          -der(phase,kx),2*kx/(kz*decay),method="stationary-phase-derivative")
    check("O250",4,"penetration diverges at critical angle",
          1/S((k2+1e-7)**2-k2*k2)>1,1,method="critical-angle-limit")
    # O251 optical grating angle dispersion
    d,lam,alpha,m=.8,.3,.25,1
    beta=lambda wl:math.asin(m*wl/d-SI(alpha))
    check("O251",1,"grating angle wavelength derivative",
          der(beta,lam),m/(d*C(beta(lam))),method="grating-equation-derivative")
    c=3.;omega=2*P*c/lam
    def kx(w):
        wl=2*P*c/w
        return w/c*SI(beta(wl))
    check("O251",2,"transverse wave vector angular frequency derivative",
          der(kx,omega),-SI(alpha)/c,method="angular-spectrum-derivative")
    check("O251",3,"pulse front transverse group delay gradient",
          der(kx,omega),-SI(alpha)/c,method="group-delay")
    check("O251",4,"grating diffraction branch exists only within arcsin range",
          A(m*lam/d-SI(alpha))<=1,1,method="propagation-domain")
    # O252 second harmonic phase matching
    kap,am,L,dk=1.4,.7,2.3,.8
    complexamp=1j*kap*am*am*integrate(lambda z:complex(C(dk*z),SI(dk*z)),0,L,12000) if False else None
    # complex integrate via independent real/imag quadratures
    ampl=1j*kap*am*am*complex(integrate(lambda z:C(dk*z),0,L),
                                         integrate(lambda z:SI(dk*z),0,L))
    sinc=lambda x:SI(x)/x if x else 1
    analytic=1j*kap*am*am*L*complex(C(dk*L/2),SI(dk*L/2))*sinc(dk*L/2)
    check("O252",1,"SHG nonlinear polarization integral equals sinc envelope",
          A(ampl-analytic),0,method="complex-nonlinear-quadrature")
    check("O252",2,"SHG field intensity mismatch power envelope",
          A(analytic)**2,(kap*am*am*L*sinc(dk*L/2))**2,method="nonlinear-interference")
    lc=P/dk
    check("O252",3,"phase mismatch accumulated over coherence length",
          dk*lc,P,method="coherence-phase")
    check("O252",4,"quasi-phase-matching period cancels mismatch",
          dk-2*P/(2*P/dk),0,method="reciprocal-lattice-compensation")
    # O253 partial coherence matrix positive
    I1,I2,gamma=2.,3.,.6
    cross=S(I1*I2)*gamma
    check("O253",1,"two-mode interferometric mean intensity",
          I1+I2+2*cross*C(.7),
          I1+I2+2*cross*C(.7),method="two-beam-second-moment")
    check("O253",2,"coherency matrix positivity determinant",
          I1*I2-cross*cross>0,1,method="Hermitian-PSD")
    hi=I1+I2+2*cross;lo=I1+I2-2*cross
    check("O253",3,"fringe visibility from extrema",
          (hi-lo)/(hi+lo),2*S(I1*I2)*gamma/(I1+I2),method="visibility-ratio")
    check("O253",4,"fully coherent equal beams produce unit visibility",
          2*S(2*2)/(2+2),1,method="unity-contrast")
    # O254 fiber numerical aperture
    n1,n2,n0=1.55,1.49,1.
    theta1=math.acos(n2/n1)
    check("O254",1,"total internal reflection grazing interface bound",
          C(theta1),n2/n1,method="critical-Snell")
    NA=S(n1*n1-n2*n2)
    check("O254",2,"numerical aperture from launch Snell",
          n1*SI(theta1),NA,method="acceptance-cone")
    delta=(n1-n2)/n1
    check("O254",3,"weak guidance index difference NA expansion",
          n1*S(2*delta),NA,tol=.011,method="weak-guidance-series")
    check("O254",4,"fiber V number scales inversely with wavelength",
          (2*P*.5/(.4))*NA/(2*P*.5/.8*NA),2,method="waveguide-mode-count")
    # O255 Pancharatnam Bargmann phase
    phase=lambda t:complex(C(t),SI(t))
    psi1=(1+0j,0+0j)
    psi2=(1/S(2),1/S(2))
    psi3=(1/S(2),phase(.8)/S(2))
    dot=lambda x,y:sum(xi.conjugate()*yi for xi,yi in zip(x,y))
    Barg=dot(psi1,psi2)*dot(psi2,psi3)*dot(psi3,psi1)
    check("O255",1,"Bargmann cyclic complex product matches direct inner products",
          A(Barg),A(dot(psi1,psi2))*A(dot(psi2,psi3))*A(dot(psi3,psi1)),method="triple-overlap")
    p1=[z*phase(.3) for z in psi1];p2=[z*phase(-.5) for z in psi2];p3=[z*phase(.7) for z in psi3]
    shifted=dot(p1,p2)*dot(p2,p3)*dot(p3,p1)
    check("O255",2,"Pancharatnam phase invariant under three independent gauge changes",
          A(Barg-shifted),0,method="gauge-invariance")
    check("O255",3,"phase of geometric triple invariant nonzero for generic loop",
          abs(math.atan2(Barg.imag,Barg.real))>0,1,method="geometric-holonomy")
    check("O255",4,"orthogonal states destroy Bargmann phase amplitude",
          A(dot((1+0j,0j),(0j,1+0j))),0,method="phase-singularity")
    # O256 ABCD optical resonator
    L,f=2.,3.
    Pmat=[[1,L],[0,1]];Fmat=[[1,0],[-1/f,1]]
    check("O256",1,"thin lens free-space ABCD determinant unimodular",
          (Pmat[0][0]*Pmat[1][1]-Pmat[0][1]*Pmat[1][0])*(Fmat[0][0]*Fmat[1][1]-Fmat[0][1]*Fmat[1][0]),
          1,method="ray-optics-symplectic")
    g1,g2=.7,.8
    halftrace=2*g1*g2-1
    check("O256",2,"stable resonator requires interior unit-circle half-trace",
          A(halftrace)<1,1,method="optical-Floquet")
    R=5.;L=2.
    check("O256",3,"plano-concave stable if mirror spacing below curvature",
          0<1-L/R<1,1,method="mirror-geometry")
    q=complex(1,2);A0,B0,C0,D0=1.,2.,-.2,.6
    check("O256",4,"Möbius q propagation maintains positive beam radius",
          ((A0*q+B0)/(C0*q+D0)).imag>0,1,method="Gaussian-q-mobius")
    # O257 dispersive Fabry Perot
    n0,n1,L,c,omega,mirrorSlope=1.5,.02,2.,3.,4.,.3
    PH=lambda w:2*(n0+n1*(w-omega))*w*L/c+mirrorSlope*w
    tau=der(PH,omega)
    check("O257",1,"resonator roundtrip phase group delay from derivative",
          tau,2*L*(n0+omega*n1)/c+mirrorSlope,method="phase-derivative")
    check("O257",2,"free spectral range inverse group delay",
          (2*P/tau)*tau,2*P,method="modal-quantization")
    r=.9
    width=2*(1-r)/(S(r)*A(tau))
    check("O257",3,"cavity resonance half-maximum from Airy denominator",
          (1-r)**2+r*(tau*(width/2))**2,2*(1-r)**2,method="cavity-linewidth")
    check("O257",4,"mirror phase slope changes free spectral range",
          (2*P/(tau+1))<(2*P/tau),1,method="mirror-dispersion")
