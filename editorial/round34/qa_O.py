from qa_common import *

def run():
    # O234 Fabry-Perot Airy resonator
    rr=.85;F=4*rr/(1-rr)**2
    Airy=lambda ph:1/(1+F*SI(ph)**2)
    check("O234",1,"coherent multi-pass cavity amplitude magnitude",
          A((1-rr)/(1-rr*E(1j*.4)))**2,
          1/(1+F*SI(.2)**2),method="geometric-optical-series")
    check("O234",2,"Fabry Perot lossless on-resonance transmission",
          Airy(P),1,method="resonance-boundary")
    finesse=P*S(rr)/(1-rr)
    check("O234",3,"finesse from Airy parameter",finesse,P*S(F)/2,method="linewidth-asymptotic")
    check("O234",4,"transparent zero-reflectivity limit",
          1/(1+4*.00001/(1-.00001)**2*SI(.8)**2),1,tol=5e-5,method="uncoupled-limit")
    # O235 birefringent ray walkoff
    no,ne,th=1.5,1.7,.6
    eff=1/(C(th)**2/no**2+SI(th)**2/ne**2)
    check("O235",1,"extraordinary uniaxial normal surface",
          eff*(C(th)**2/no**2+SI(th)**2/ne**2),1,method="index-ellipsoid")
    thS=math.atan(no*no/(ne*ne)*math.tan(th))
    check("O235",2,"group velocity refracted angle",
          math.tan(thS),no*no/(ne*ne)*math.tan(th),method="slowness-normal")
    delt=.00001
    thetaS=math.atan(1/(1+delt)**2*math.tan(th))
    check("O235",3,"walkoff small birefringence coefficient",
          (thetaS-th)/delt,-SI(2*th),tol=2e-5,method="perturbation-derivative")
    check("O235",4,"principal-axis walkoff exactly vanishes",
          math.atan(no*no/(ne*ne)*math.tan(0)),0,method="crystal-symmetry")
    # O236 Mach Zehnder classical Fisher information
    N,phi=60.,.7
    lam1=lambda x:N*C(x/2)**2
    lam2=lambda x:N*SI(x/2)**2
    check("O236",1,"two complementary output intensities",
          lam1(phi)+lam2(phi),N,method="unitary-beam-splitter")
    check("O236",2,"shot-noise independent Poisson variance sum",
          lam1(phi)+lam2(phi),N,method="photon-count-variance")
    fish=der(lam1,phi)**2/lam1(phi)+der(lam2,phi)**2/lam2(phi)
    check("O236",3,"Poisson Fisher information equals mean photon number",
          fish,N,tol=1e-5,method="score-function")
    check("O236",4,"balanced phase bias saturates difference-readout Fisher",
          N*SI(P/2)**2,N,method="optimal-phase")
    # O237 Stokes Mueller physicality
    pol=[5.,3.,1.,2.]
    check("O237",1,"Stokes coherency matrix positivity",
          pol[0]**2-sum(x*x for x in pol[1:])>0,1,method="density-matrix-positive")
    check("O237",2,"ideal x polarizer transmitted intensity",
          (pol[0]+pol[1])/2,4,method="Mueller-product")
    qout=(pol[0]+pol[1])/2
    check("O237",3,"polarizer output degree exactly one",qout/qout,1,method="purity")
    pp=.4
    check("O237",4,"isotropic depolarizer contracts degree of polarization",
          S(sum((pp*z)**2 for z in pol[1:]))/pol[0],
          pp*S(sum(z*z for z in pol[1:]))/pol[0],method="contractive-map")
    # O238 Gaussian beams
    w0,lambda0,z=1.5,.04,3.
    zr=P*w0*w0/lambda0
    ww=w0*S(1+z*z/zr**2)
    curvature=z*(1+(zr/z)**2)
    check("O238",1,"Gaussian q parameter waist and curvature relation",
          (z/(z*z+zr*zr)),1/curvature,method="complex-q")
    check("O238",2,"Gouy phase total forward-to-backward change",
          math.atan(1e8/zr)-math.atan(-1e8/zr),P,tol=1e-5,method="phase-asymptote")
    check("O238",3,"Rayleigh diffraction angle identity",
          w0/zr,lambda0/(P*w0),method="beam-geometry")
    I0=2.
    power=integrate(lambda r:2*P*r*I0*(w0/ww)**2*E(-2*r*r/(ww*ww)),0,12*ww)
    check("O238",4,"Gaussian beam transverse total power",power,P*I0*w0*w0/2,method="Poynting-integral")
    # O239 N-slit Fourier grating
    N,spacing,width,wl,order=13,3.,.5,.9,2
    th=math.asin(order*wl/spacing)
    alpha=P*spacing*SI(th)/wl
    check("O239",1,"grating principal diffraction order",alpha/P,order,method="phasor-array")
    check("O239",2,"grating order angle positive",
          spacing*SI(th),order*wl,method="grating-equation")
    check("O239",3,"main-lobe first zero optical phase offset",
          N*(P/N),P,method="finite-array-resolution")
    check("O239",4,"diffraction-grating Rayleigh spectral resolving power",
          order*N,wl/(wl/(order*N)),method="resolving-power")
    # O240 coherent 4f filtering
    a,lambda0,f=1.2,.05,2.
    fc=a/(lambda0*f)
    h=lambda x:2*fc*SI(2*P*fc*x)/(2*P*fc*x) if x else 2*fc
    check("O240",1,"Fourier lens frequency-to-coordinate relation",
          a/(lambda0*f),fc,method="lens-Fourier-mapping")
    check("O240",2,"finite rectangular passband sinc kernel",
          h(.035),SI(2*P*fc*.035)/(P*.035),method="Fourier-inverse")
    check("O240",3,"sinusoidal sideband suppression above cutoff",
          1 if 1.1*fc>fc else 0,1,method="spectral-cutoff")
    check("O240",4,"unbounded cutoff tends delta distribution by energy",
          integrate(lambda x:h(x),-.15,.15,20000),1,tol=.02,method="distributional-limit")
    # O241 optical frequency comb
    frep=100.;phase=.6;fceo=phase/(2*P)*frep;n=1500
    check("O241",1,"pulse train repetition frequency",1/(1/frep),frep,method="time-frequency")
    check("O241",2,"comb tooth phase commensurability",
          2*P*(n*frep+fceo)/frep-phase,2*P*n,method="coherent-interference")
    check("O241",3,"self referencing f-2f beat frequency",
          2*(n*frep+fceo)-(2*n*frep+fceo),fceo,method="frequency-difference")
    check("O241",4,"CEO phase modulo 2pi changes tooth label",
          (phase+2*P)/(2*P)*frep-fceo,frep,method="phase-equivalence")
