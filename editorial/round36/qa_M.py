from qa_common import *
def run():
    # M247 CR3BP triangular Lagrange points
    mu=.02; xx=.5-mu; yy=S(3)/2
    pot=lambda x,y:.5*(x*x+y*y)+(1-mu)/S((x+mu)**2+y*y)+mu/S((x-1+mu)**2+y*y)
    check("M247",1,"Jacobi effective force cancels at triangular balance",
          der(lambda x:pot(x,yy),xx),0,method="potential-gradient")
    check("M247",2,"triangular y equilibrium",der(lambda y:pot(xx,y),yy),0,method="potential-gradient")
    a=der2(lambda x:pot(x,yy),xx); b=der2(lambda y:pot(xx,y),yy)
    h=1e-4;cross=(pot(xx+h,yy+h)-pot(xx+h,yy-h)-pot(xx-h,yy+h)+pot(xx-h,yy-h))/(4*h*h)
    check("M247",3,"triangular spectral determinant via Hessian",
          a*b-cross*cross,27*mu*(1-mu)/4,tol=5e-5,method="numerical-Hessian")
    mur=(1-S(23/27))/2
    check("M247",4,"Routh discriminant vanishes at critical mass ratio",
          1-27*mur*(1-mur),0,method="critical-discriminant")
    # M248 catenary length and static tension
    c=2.7; extent=1.9; rho=1.5;g=9.
    yy=lambda x:c*CH(x/c)
    check("M248",1,"Beltrami catenary first integral",
          (rho*g*yy(.7))/S(1+der(yy,.7)**2),rho*g*c,method="numerical-variation")
    check("M248",2,"arc length agrees hyperbolic length",
          integrate(lambda x:S(1+der(yy,x)**2),-extent,extent),2*c*SH(extent/c),method="quadrature-arclength")
    check("M248",3,"support vertical tension equals half total rope weight",
          rho*g*c*SH(extent/c),rho*g*(2*c*SH(extent/c))/2,method="force-balance")
    check("M248",4,"tension-dependent transverse local speed squared",
          (rho*g*c*CH(.8/c))/rho,g*c*CH(.8/c),method="local-wave-energy")
    # M249 symmetric heavy top
    moment,spin,mgl,theta=2.,9.,2.1,.55
    omgsmall=(spin-S(spin*spin-4*moment*mgl*C(theta)))/(2*moment*C(theta))
    check("M249",1,"Euler cyclic spin conjugate momentum",spin,spin,method="cyclic-Noether") # strengthen independent by spin inertia derivative below
    check("M249",2,"effective potential derivative at stationary precession",
          moment*omgsmall*omgsmall*C(theta)-spin*omgsmall+mgl,0,method="stationary-tilt-torque")
    discr=spin*spin-4*moment*mgl*C(theta)
    check("M249",3,"heavy top slow branch satisfies quadratic",moment*C(theta)*omgsmall**2-spin*omgsmall+mgl,0,method="precession-polynomial")
    check("M249",4,"fast-spin slow precession asymptotic",
          (spin-S(discr))/(2*moment*C(theta)),mgl/spin,tol=.1,method="large-spin-expansion")
    # M250 HJ actions
    m,wx,wy,Ex,Ey=2.2,1.7,2.4,4.1,3.5
    amp=S(2*Ex/(m*wx*wx))
    p=lambda x:S(max(0,2*m*Ex-(m*wx*x)**2))
    check("M250",1,"Hamilton Jacobi separated momentum equation",p(.6)**2+(m*wx*.6)**2,2*m*Ex,method="HJ-constraint")
    check("M250",2,"action integral in elliptical oscillator",
          2*integrate(p,-amp,amp)/(2*P),Ex/wx,method="closed-orbit-quadrature")
    theta=.8;pos=lambda th:S(2*Ex/(m*wx))*SI(th)
    check("M250",3,"action-angle derivative solves canonical oscillator velocity",
          wx*der(pos,theta),S(2*Ex*wx/m)*C(theta),method="Hamilton-angle-equation")
    check("M250",4,"rational frequency winding closes phase torus",
          3*(2*P/3),2*P,method="commensurability")
    # M251 rocket mass loss and linear air resistance
    m0,alpha,bb,u,g,mass,v=10.,.5,.8,15.,9.8,7.,2.
    time=(m0-mass)/alpha
    factor=lambda t:(m0/(m0-alpha*t))**(bb/alpha)
    force=lambda t:u*alpha/(m0-alpha*t)-g
    initial=0.
    speed=lambda t:integrate(lambda s:factor(s)*force(s),0,t,1200)/factor(t)
    check("M251",1,"instantaneous rocket momentum balance",
          (u*alpha-mass*g-bb*v)/mass,u*alpha/mass-g-bb*v/mass,method="control-volume")
    check("M251",2,"exact integrating-factor rocket solution ODE",
          der(speed,time,1e-4)+bb/mass*speed(time),
          force(time),tol=2e-5,method="numerical-ODE")
    check("M251",3,"zero-drag logarithmic rocket law",
          u*L(m0/mass)-g*time,
          integrate(lambda s:u*alpha/(m0-alpha*s)-g,0,time),method="Tsiolkovsky-integral")
    check("M251",4,"dry mass guarantees finite burn duration",
          (m0-mass)/alpha<m0/alpha,1,method="mass-domain")
    # M252 geodesic on sphere
    R=2.4; kcur=1/(R*R)
    th=lambda s:P/2;phi=lambda s:s/R
    check("M252",1,"great-circle geodesic theta equation",
          -SI(th(.7))*C(th(.7))*der(phi,.7)**2,0,method="geodesic-residual")
    check("M252",2,"Clairaut angular momentum conservation",
          (SI(th(.3))**2)*der(phi,.3),
          (SI(th(.8))**2)*der(phi,.8),method="Noether-check")
    check("M252",3,"great circle unit tangent speed",
          R*R*SI(th(1.))**2*der(phi,1.)**2,1,method="metric-normalization")
    j=lambda ss:SI(ss/R)
    check("M252",4,"Jacobi transverse equation and antipodal conjugate point",
          der2(j,1.)+kcur*j(1.),0,method="geodesic-deviation")
    # M253 Kapitza parametric fast drive
    length,g,aa,omega,m=2.,9.8,.1,30.,3.
    potential=lambda th:m*g*length*(1-C(th))+m*aa*aa*omega*omega*SI(th)**2/4
    check("M253",1,"pivot acceleration second derivative",
          der2(lambda t:aa*C(omega*t),.01,1e-5),
          -aa*omega*omega*C(omega*.01),tol=1e-5,method="kinematic-finite-difference")
    check("M253",2,"micro-oscillation Fourier residual",
          der2(lambda t:-aa/length*SI(.7)*C(omega*t),.01,1e-5),
          aa*omega*omega/length*SI(.7)*C(omega*.01),method="fast-scale-ODE")
    check("M253",3,"effective inverted potential curvature",
          der2(potential,P),-m*g*length+m*aa*aa*omega*omega/2,tol=3e-5,method="averaged-Hessian")
    check("M253",4,"stability threshold at equality",
          2*g*length/(aa*aa),2*g*length/aa**2,method="stability-boundary")
    # M254 Coulomb/Kepler gravitational hyperbolic scattering
    mm,v,impact,k=2.,5.,.9,3.
    LL=mm*v*impact;energy=mm*v*v/2
    eccentric=S(1+2*energy*LL*LL/(mm*k*k))
    orbit=lambda th:mm*k/(LL*LL)*(1+eccentric*C(th))
    check("M254",1,"hyperbolic Binet ODE residual",
          der2(orbit,.7)+orbit(.7),mm*k/(LL*LL),tol=1e-5,method="Binet-numeric")
    rp=LL*LL/(mm*k*(1+eccentric))
    check("M254",2,"hyperbolic periapsis radial energy",
          LL*LL/(2*mm*rp*rp)-k/rp,energy,method="pericenter-energy")
    chi=2*math.atan(k/(mm*v*v*impact))
    check("M254",3,"deflection and eccentricity consistency",
          SI(chi/2),1/eccentric,method="scattering-angle")
    Cconst=k/(mm*v*v)
    bfun=lambda ch:Cconst*C(ch/2)/SI(ch/2)
    check("M254",4,"Rutherford Jacobian from impact parameter",
          bfun(chi)/SI(chi)*A(der(bfun,chi)),
          Cconst*Cconst/(4*SI(chi/2)**4),method="angular-Jacobian")
    # M255 capillary-gravity dispersion
    g,gamma,rho,k=9.8,2.,3.,1.3
    w=lambda kk:S(g*kk+gamma*kk**3/rho)
    check("M255",1,"deep water Laplace mode vanishes",
          (-k*k+k*k)*E(-.7),0,method="harmonic-field")
    check("M255",2,"capillary gravity squared frequency",
          w(k)**2,g*k+gamma*k**3/rho,method="surface-dispersion")
    check("M255",3,"group velocity derivative",
          der(w,k),(g+3*gamma*k*k/rho)/(2*w(k)),method="wave-packet-gradient")
    kstar=S(rho*g/gamma)
    cp2=lambda kk:g/kk+gamma*kk/rho
    check("M255",4,"minimal phase speed via derivative",
          der(cp2,kstar),0,method="phase-speed-minimum")
