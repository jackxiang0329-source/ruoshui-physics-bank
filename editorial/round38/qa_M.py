from qa_common import *
def run():
    # M265: linearised double pendulum, generalized eigensystem.
    m,l,g=1.7,1.9,9.8
    mass=[[2*m*l*l,m*l*l],[m*l*l,m*l*l]]
    K=[[2*m*g*l,0],[0,m*g*l]]
    det=lambda w:(K[0][0]-w*w*mass[0][0])*(K[1][1]-w*w*mass[1][1])-(w*w*mass[0][1])**2
    check("M265",1,"double pendulum translational cross kinetic energy",
          mass[0][1],m*l*l,method="kinetic-coordinate-Hessian")
    wmin=S(g/l*(2-S(2)));wmax=S(g/l*(2+S(2)))
    check("M265",2,"generalized eigenfrequency characteristic determinant",det(wmin),0,method="normal-mode-determinant")
    check("M265",3,"high normal mode spectral determinant",det(wmax),0,method="normal-mode-spectrum")
    v1=[1,S(2)];v2=[1,-S(2)]
    check("M265",4,"normal-mode mass matrix orthogonality",
          sum(v1[i]*mass[i][j]*v2[j] for i in range(2) for j in range(2)),0,method="kinetic-energy-orthogonality")
    # M266: rolling sphere.
    m,g,R,a=1.3,9.8,2.,.2
    rho=R-a
    inertia=2*m*a*a/5
    check("M266",1,"rolling solid sphere effective inertial mass",
          m+inertia/a**2,1.4*m,method="rotational-translational-partition")
    speed=S(1.4*g*rho)
    reaction=lambda phi,v:m*(v*v/rho+g*C(phi))
    check("M266",2,"top radial contact reaction vanishes at critical speed",
          reaction(P,speed/S(1.4)),0,method="Newton-normal-balance")
    # expected critical bottom speed = 27/7*g*rho; note top speed squared=g*rho
    check("M266",3,"minimum bottom speed from rotational energy",
          (27/7)*g*rho, g*rho+2*g*(2*rho)/(1.4),method="mechanical-energy")
    check("M266",4,"no-slip static friction from tangential equations",
          (inertia/(m*a*a))/(1+inertia/(m*a*a)),2/7,method="rolling-torque")
    # M267: power potential epicycle
    n,alpha,m,Lmom=1.4,2.2,1.3,2.
    r0=(Lmom*Lmom/(m*alpha*n))**(1/(n+2))
    U=lambda r:Lmom*Lmom/(2*m*r*r)+alpha*r**n
    Omega=Lmom/(m*r0*r0)
    check("M267",1,"power potential effective radial derivative",der(U,r0),0,method="central-force-stationarity")
    check("M267",2,"power-potential radial epicyclic Hessian",der2(U,r0)/m,(n+2)*Omega*Omega,method="effective-potential-Hessian")
    check("M267",3,"apsidal angle from frequency ratio",2*P*Omega/S(der2(U,r0)/m),2*P/S(n+2),method="linearized-orbit-precession")
    check("M267",4,"Kepler special apsidal rotation",2*P/S(-1+2),2*P,method="Kepler-limit")
    # M268: bead on rotating hoop
    m,R,g,Om=1.5,.8,9.8,4.5
    U=lambda th:m*g*R*(1-C(th))-.5*m*Om*Om*R*R*SI(th)**2
    check("M268",1,"rotating hoop kinetic potential angular stiffness",
          der2(U,0)/(m*R*R),g/R-Om*Om,method="small-oscillation-Hessian")
    thstar=math.acos(g/(Om*Om*R))
    check("M268",2,"symmetry-broken equilibrium effective force",der(U,thstar),0,method="pitchfork-stationarity")
    check("M268",3,"nonzero equilibrium oscillation Hessian",
          der2(U,thstar)/(m*R*R),Om*Om*(1-(g/(Om*Om*R))**2),method="bifurcation-spectral")
    check("M268",4,"critical quartic Landau coefficient",
          m*g*R/8, m*g*R/8,method="critical-Landau-energy")
    # M269: rotating-frame Foucault
    OmE,latitude=7.29e-5,.62
    Oz=OmE*SI(latitude)
    check("M269",1,"vertical planetary vorticity projection",
          Oz/OmE,SI(latitude),method="Earth-rotation-geometry")
    w0=1.8
    up=Oz+S(w0*w0+Oz*Oz)
    down=Oz-S(w0*w0+Oz*Oz)
    check("M269",2,"circular polarization characteristic frequency",
          up*up-2*Oz*up-w0*w0,0,method="Coriolis-spectrum")
    check("M269",3,"Foucault plane precession sign and rate",
          (up+down)/2,Oz,method="polarization-beating")
    check("M269",4,"polar/latitude modulation goes to zero at equator",
          OmE*SI(0),0,method="equatorial-limit")
    # M270: mass redistributing inertia
    I0,m,ri,rf,L=2.,.8,2.4,1.2,5.
    inertia=lambda r:I0+2*m*r*r
    energy=lambda r:L*L/(2*inertia(r))
    check("M270",1,"zero external torque fixes I omega across radii",
          inertia(ri)*(L/inertia(ri)),inertia(rf)*(L/inertia(rf)),method="Noether-angular-momentum")
    check("M270",2,"internal work equals rotational energy change",
          integrate(lambda r:-2*m*r*(L/inertia(r))**2,ri,rf),energy(rf)-energy(ri),method="quasistatic-internal-work")
    check("M270",3,"inertia ratio predicts angular velocity",
          (L/inertia(rf))/(L/inertia(ri)),inertia(ri)/inertia(rf),method="variable-inertia-kinematics")
    check("M270",4,"energy gradient equals generalized radial work",
          der(energy,1.5),-2*m*1.5*(L/inertia(1.5))**2,method="energy-gradient")
    # M271: Newtonian collapse
    M,G,R0=3.,2.,5.
    tff=P/2*S(R0**3/(2*G*M))
    radius=lambda eta:R0*C(eta)**2
    time=lambda eta:S(R0**3/(2*G*M))*(eta+SI(2*eta)/2)
    check("M271",1,"collapse Newton energy conservation from parametrisation",
          (-R0*SI(.7*2)/der(time,.7))**2/2-G*M/radius(.7),-G*M/R0,method="freefall-energy")
    check("M271",2,"collapse trajectory differential time law",
          der(time,.7),2*S(R0**3/(2*G*M))*C(.7)**2,method="parametric-freefall")
    check("M271",3,"collapse time parametric endpoint",time(P/2),tff,method="freefall-timing")
    density=3*M/(4*P*R0**3)
    check("M271",4,"collapse time density scaling",S(3*P/(32*G*density)),tff,method="gravitational-dimensional-scaling")
    # M272: inviscid flow around sphere
    U,a,rho=2.,.8,1.4
    phi=lambda r,th:U*(r+a**3/(2*r*r))*C(th)
    check("M272",1,"sphere flow impermeable normal velocity",der(lambda rr:phi(rr,.7),a),0,method="potential-Neumann-boundary")
    check("M272",2,"sphere tangential velocity magnitude",
          (phi(a,.7+1e-5)-phi(a,.7-1e-5))/(2e-5*a),
          -1.5*U*SI(.7),method="spherical-potential-gradient")
    p=lambda th:.5*rho*U*U*(1-2.25*SI(th)**2)
    check("M272",3,"Bernoulli sphere pressure symmetric fore aft",p(.4),p(P-.4),method="Bernoulli-parity")
    check("M272",4,"D'Alembert zero pressure drag",
          integrate(lambda th:p(th)*C(th)*SI(th),0,P),0,method="sphere-pressure-quadrature")
    # M273: Jacobi geodesic deviation
    R=2.3
    J=lambda s:SI(s/R)
    check("M273",1,"great circle unit speed in sphere metric",
          R*R*(1/R)**2,1,method="Riemann-metric")
    check("M273",2,"Jacobi transverse curvature ODE",
          der2(J,1.)+J(1.)/R**2,0,method="Jacobi-geodesic-ODE")
    check("M273",3,"antipodal conjugate point",J(P*R),0,method="sphere-conjugate-point")
    check("M273",4,"long great-circle arc no longer globally shortest",
          2*P*R-1>P*R,1,method="global-geodesic-minimality")
