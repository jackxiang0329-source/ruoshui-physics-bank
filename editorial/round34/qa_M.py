from qa_common import *

def run():
    # M229 rotating hoop
    a,g,m,om,th=2.,9.,3.,3.,.6
    U=lambda x:-m*g*a*C(x)-m*a*a*om*om*SI(x)**2/2
    check("M229",1,"Lagrange acceleration vs effective force",-der(U,th)/(m*a*a),(om*om*C(th)-g/a)*SI(th),method="finite-difference")
    check("M229",2,"tilted equilibrium stationarity",der(U,math.acos(g/(a*om*om))),0,method="energy-gradient")
    tilt=math.acos(g/(a*om*om))
    check("M229",3,"tilted curvature vs small-oscillation frequency",der2(U,tilt)/(m*a*a),om*om-g*g/(a*a*om*om),tol=2e-5,method="stability-Hessian")
    check("M229",4,"nonrotating linear pendulum curvature",der2(lambda t:-m*g*a*C(t),0)/(m*a*a),g/a,method="limiting-case")
    # M230 Foucault
    omE,phi,omega0=0.04,.7,2.5
    oz=omE*SI(phi)
    check("M230",1,"Coriolis vertical projection",oz,omE*SI(phi),method="geometry")
    roots=[oz+S(omega0**2+oz**2),oz-S(omega0**2+oz**2)]
    check("M230",2,"two signed circular eigenfrequencies root product",roots[0]*roots[1],-omega0*omega0,method="characteristic-polynomial")
    check("M230",3,"swing-plane rotation after one precession period",abs(oz)*2*P/abs(oz),2*P,method="angle-integral")
    check("M230",4,"equatorial Foucault precession",omE*SI(0),0,method="latitude-limit")
    # M231 J2
    mu,R,a,e,j2,i=2.,1.,8.,.22,.016,.71
    n=S(mu/a**3)
    p=a*(1-e*e)
    Vavg=lambda inc:mu*j2*R*R*(1-3*C(inc)**2)/(4*a**3*(1-e*e)**1.5)
    G=S(mu*a*(1-e*e));H=G*C(i)
    check("M231",1,"orbit-averaged quadrupole against true-anomaly integral",
        integrate(lambda f: (mu*j2*R*R/2)*((3*(SI(i)*SI(f))**2-1)/
        (p/(1+e*C(f)))**3)*((1-e*e)**1.5/(1+e*C(f))**2)/(2*P),0,2*P),
        Vavg(i),method="Kepler-time-average")
    check("M231",2,"nodal Delaunay derivative",
        der(lambda h:mu*j2*R*R*(1-3*(h/G)**2)/(4*a**3*(1-e*e)**1.5),H),
        -1.5*n*j2*(R/p)**2*C(i),tol=1e-6,method="Hamiltonian-derivative")
    F=lambda GG:mu*j2*R*R*(1-3*(H/GG)**2)/(4*a**3)*((S(mu*a)/GG)**3)
    check("M231",3,"periapsis Delaunay derivative",
        der(F,G),.75*n*j2*(R/p)**2*(5*C(i)**2-1),tol=1e-6,method="canonical-derivative")
    check("M231",4,"critical inclination roots of apsidal J2 term",5*C(math.acos(1/S(5)))**2-1,0,method="critical-condition")
    # M232 central inverse-square correction
    k,ell,mm,eps=3.,2.,1.8,.05
    alpha=S(1+2*mm*eps/ell**2)
    f=lambda th:(mm*k/(ell**2*alpha**2))*(1+.1*C(alpha*th))
    check("M232",1,"Binet differential equation residual",
        der2(f,.7,1e-4)+alpha*alpha*f(.7),mm*k/ell**2,tol=1e-5,method="ODE-residual")
    check("M232",2,"apsidal angle times radial frequency",2*P/alpha*alpha,2*P,method="orbital-period")
    de=1e-7
    check("M232",3,"first-order apsidal correction coefficient",
        ((2*P/S(1+2*mm*de/ell**2))-2*P)/de,-2*P*mm/ell**2,tol=1e-5,method="perturbation-derivative")
    rc=2*(ell*ell/(2*mm)+eps)/k
    U=lambda r:(ell**2/(2*mm)+eps)/(r*r)-k/r
    check("M232",4,"stable circular effective-potential curvature",der2(U,rc),2*(ell**2/(2*mm)+eps)/rc**4,tol=2e-5,method="Hessian-limit")
    # M233 relativistic circular geodesics, G=c=1
    M,r=1.3,13.
    hsq=M*r*r/(r-3*M)
    V=lambda x:(1-2*M/x)*(1+hsq/(x*x))
    En=(r-2*M)**2/(r*(r-3*M))
    check("M233",1,"circular effective potential equals Killing energy",V(r),En,method="first-integral")
    check("M233",2,"circular first derivative vanishes",der(V,r),0,method="stationarity")
    rI=6*M
    hI=M*rI*rI/(rI-3*M)
    vI=lambda x:(1-2*M/x)*(1+hI/(x*x))
    check("M233",3,"ISCO zero curvature",der2(vI,rI,2e-4),0,tol=5e-6,method="stability-Hessian")
    check("M233",4,"Schwarzschild weak-field precession parameter",
        (6*P*M/(10*(1-.2**2)))/(2*P),3*M/(10*(1-.2**2)),method="dimensionless-expansion")
    # M234 Lane Emden
    nn=.8
    theta=lambda x:1-x*x/6+nn*x**4/120
    check("M234",1,"regular center boundary derivative",der(theta,0),0,method="center-regularity")
    x=.02
    check("M234",2,"Lane-Emden series radial ODE",
        (der2(theta,x)+2*der(theta,x)/x)+theta(x)**nn,
        0,tol=1e-5,method="series-ODE-residual")
    nidx=3
    check("M234",3,"n=3 mass-density scaling exponent",(3-nidx)/(2*nidx),0,method="homology-exponent")
    u=lambda x:(1+x*x/3)**(-.5)
    check("M234",4,"n=5 infinite-radius analytic Lane-Emden solution",
        der2(u,1.,1e-4)+2*der(u,1.)+u(1.)**5,0,tol=2e-5,method="nonlinear-ODE")
    # M235 massive pulley with linear drag
    m1,m2,I,R,b,g=1.,3.,.7,.5,1.2,9.8
    Me=m1+m2+I/R**2;fr=(m2-m1)*g;gam=b/R**2
    speed=lambda t:fr/gam*(1-E(-gam*t/Me))
    check("M235",1,"tension difference vs rotational torque",fr-(m1+m2)*fr/Me,(I/R**2)*fr/Me,method="torque-balance",tol=1)
    check("M235",2,"velocity transient solves Newton-Ode",
        der(speed,.4)+gam/Me*speed(.4),fr/Me,method="ODE-residual")
    v=speed(.4);ad=fr/Me-gam*v/Me
    check("M235",3,"mechanical energy derivative equals friction loss",Me*v*ad-fr*v,-gam*v*v,method="work-energy")
    small=1e-7
    check("M235",4,"small-friction terminal formula finite time",
        fr/small*(1-E(-small*.5/Me)),fr*.5/Me,tol=1e-6,method="singular-limit")
    # M236 scattering coordinate transform
    mm,MT,v,chi=3.,1.5,4.,.9
    V=mm*v/(mm+MT);u=MT*v/(mm+MT)
    vx=V+u*C(chi);vy=u*SI(chi)
    check("M236",1,"laboratory outgoing speed from CM vectors",
        vx*vx+vy*vy,v*v*(mm*mm+MT*MT+2*mm*MT*C(chi))/(mm+MT)**2,method="energy-vector")
    check("M236",2,"center angle to laboratory angular transform",
        math.atan2(vy,vx),math.atan2(SI(chi),C(chi)+mm/MT),method="kinematics")
    critical=math.acos(-MT/mm)
    check("M236",3,"maximal lab scattering angle for heavy projectile",
        math.atan2(SI(critical),C(critical)+mm/MT),math.asin(MT/mm),method="extremum")
    theta=lambda x:math.atan2(SI(x),C(x)+mm/MT)
    check("M236",4,"laboratory differential angular Jacobian",
        der(theta,chi),(1+(mm/MT)*C(chi))/(1+2*(mm/MT)*C(chi)+(mm/MT)**2),method="derivative-Jacobian")
    # M237 drag-modified brachistochrone
    aa,gg,eta,mm=2.,9.,.12,1.5
    x=lambda t:aa*(t-SI(t));y=lambda t:aa*(1-C(t))
    check("M237",1,"cycloid Beltrami first-integral",y(.8)*(1+(der(y,.8)/der(x,.8))**2),2*aa,method="variational-first-integral")
    check("M237",2,"cycloid travel-time from arc speed",
        integrate(lambda t:S(der(x,t)**2+der(y,t)**2)/S(2*gg*y(t)) if t>1e-8 else S(aa/gg),0,1.4),S(aa/gg)*1.4,method="time-quadrature")
    Y=lambda s: .2*s
    w=lambda s:2*gg*E(-2*eta*s/mm)*integrate(lambda u:E(2*eta*u/mm)*.2,0,s,800)
    check("M237",3,"drag energy integral solves first-order transport",mm*der(w,1.)/2+eta*w(1.),mm*gg*.2,method="ODE-energy-residual")
    check("M237",4,"zero drag recovers gravitational potential speed",2*gg*.2*1.,2*gg*(Y(1.)-Y(0)),method="zero-drag-limit")
