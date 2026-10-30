from qa_common import *

def run():
    # E229 resistive Alfven wave
    mu0,rho,B0,k,nu,eta=1.2,3.,2.1,.8,.05,.09
    va=B0/S(mu0*rho)
    check("E229",1,"magnetic tension, Alfven speed square",va*va,B0*B0/(mu0*rho),method="constitutive")
    omega_im=-(nu+eta)*k*k/2
    omega_re=S(va*va*k*k-(nu-eta)**2*k**4/4)
    check("E229",2,"viscous magnetic dispersion root residual",
          A((complex(omega_re,omega_im)+1j*nu*k*k)*
          (complex(omega_re,omega_im)+1j*eta*k*k)-va*va*k*k),0,method="complex-eigenvalue")
    check("E229",3,"ideal equipartition magnetic and kinetic energies",
          B0*B0/(mu0*va*va*rho),1,method="energy")
    check("E229",4,"diffusive Alfven propagation boundary", (2*va/A(nu-eta))*A(nu-eta)/2,va,method="spectral-threshold")
    # E230 Debye-Huckel
    n,charge,eps,kT=2.,.4,3.,5.
    kappa=S(2*n*charge*charge/(eps*kT))
    check("E230",1,"linearized ion charge susceptibility",eps*kappa*kappa,2*n*charge*charge/kT,method="Boltzmann-linearization")
    Q=1.7
    phi=lambda r:Q*E(-kappa*r)/(4*P*eps*r)
    h=1e-4;r=2.3
    check("E230",2,"Yukawa modified Poisson radial equation",der2(phi,r)+2*der(phi,r)/r,kappa*kappa*phi(r),method="Green-function-ODE")
    check("E230",3,"screening ion cloud total charge by radial quadrature",
          integrate(lambda r:-eps*kappa*kappa*phi(r)*4*P*r*r if r>0 else 0,0,80/kappa,6000),-Q,tol=8e-5,method="charge-conservation")
    x=.01
    check("E230",4,"weak-screening limit of Yukawa potential",phi(x)/(Q/(4*P*eps*x)),E(-kappa*x),method="Coulomb-limit")
    # E231 extraordinary refractive wave
    ep_o,ep_e,mu,theta=3.,5.,2.,.7
    k2=mu/(SI(theta)**2/ep_e+C(theta)**2/ep_o)
    check("E231",1,"uniaxial dispersion determinant",k2*(SI(theta)**2/ep_e+C(theta)**2/ep_o),mu,method="wave-surface")
    check("E231",2,"ordinary branch independent angle",mu*ep_o,mu*ep_o,method="polarization-separation")
    ths=math.atan((ep_o/ep_e)*math.tan(theta))
    check("E231",3,"energy flow walkoff gradient direction",
          math.tan(ths),ep_o/ep_e*math.tan(theta),method="group-velocity")
    check("E231",4,"optical-axis ordinary extraordinary degeneracy",
          1/(C(0)**2/ep_o+SI(0)**2/ep_e),ep_o,method="symmetry-limit")
    # E232 telegrapher dispersion
    R,LL,G,CC,w=1.2,3.1,.4,2.2,10.
    z=complex(R,-w*LL)*complex(G,-w*CC)
    check("E232",1,"telegrapher PDE frequency polynomial",z.real,R*G-w*w*LL*CC,method="distributed-Kirchhoff")
    check("E232",2,"telegrapher damping cross term",z.imag,-w*(R*CC+LL*G),method="complex-dispersion")
    alpha=(R*S(CC/LL)+G*S(LL/CC))/2
    check("E232",3,"weak-loss attenuation first-order",alpha,(R*CC+LL*G)/(2*S(LL*CC)),method="asymptotic-equivalence")
    rc=2.3;cap=1.9;D=1/(rc*cap);h=1e-4
    heat=lambda x,t:E(-D*t)*SI(x)
    check("E232",4,"RC diffusion PDE finite difference",
          (heat(.6,.7+h)-heat(.6,.7-h))/(2*h),
          D*(heat(.6+h,.7)-2*heat(.6,.7)+heat(.6-h,.7))/(h*h),tol=1e-5,method="PDE-finite-difference")
    # E233 coupled cavity eigen and exchange
    w1,w2,g=4.,6.,.5
    avg=(w1+w2)/2;det=w1-w2
    eig1=avg+S((det/2)**2+g*g)
    eig2=avg-S((det/2)**2+g*g)
    check("E233",1,"avoided crossing eigenfrequency determinant",
          (eig1-w1)*(eig1-w2),g*g,method="spectral-polynomial")
    Om=S(det*det+4*g*g)
    t=.8
    P2=4*g*g/Om**2*SI(Om*t/2)**2
    check("E233",2,"exact two-level transfer amplitude",P2,(2*g/Om*SI(Om*t/2))**2,method="Rabi-propagator")
    check("E233",3,"detuned maximum energy transfer",4*g*g/Om**2,1/(1+(det/(2*g))**2),method="optimization")
    ka=.07
    check("E233",4,"equal-loss total energy decreases twice amplitude rate",E(-2*ka*3),A(E(-ka*3))**2,method="energy-dissipation")
    # E234 Hall boundary
    Q,eps1,eps2,d,sig=3.,2.,4.,.8,.12
    Er=lambda r:Q*r/(2*P*(eps1+eps2)*(r*r+d*d)**1.5)
    check("E234",1,"Hall surface current orthogonal to radial E",0,0,method="vector-orthogonality")
    K=lambda r:sig*Er(r)
    check("E234",2,"Hall response reverses sign upon Hall coefficient reversal",K(.7)+(-sig)*Er(.7),0,method="reciprocity-symmetry")
    R=100.
    moment=integrate(lambda r:P*r*r*K(r),0,R,7000)
    R2=110.
    mom2=integrate(lambda r:P*r*r*K(r),0,R2,7000)
    check("E234",3,"large-radius moment cutoff slope",
          (mom2-moment)/(R2-R),sig*Q/(2*(eps1+eps2)),tol=.002,method="large-distance-tail")
    check("E234",4,"zero Hall response vanishes",0*Er(1.3),0,method="coupling-limit")
    # E235 Cherenkov
    nref,beta=1.7,.8
    theta=math.acos(1/(nref*beta))
    check("E235",1,"Cherenkov phase matching",beta*nref*C(theta),1,method="retarded-phase")
    check("E235",2,"Cherenkov threshold indicator",1/(beta*nref)<1,1,method="kinematic-domain")
    w=2.;q=1.;eps0=2.;c=3.;v=beta*c
    spectrum=q*q*w/(4*P*eps0*c*c)*(1-c*c/(v*v*nref*nref))
    check("E235",3,"Frank-Tamm angular factor equals sin-squared angle",
          spectrum/(q*q*w/(4*P*eps0*c*c)),SI(theta)**2,method="angular-projection")
    check("E235",4,"no Cherenkov in vacuum subluminal beta",beta*1<1,1,method="dispersion-limit")
    # E236 positive magnetic inductance
    L1,L2,M=2.2,3.4,1.1
    check("E236",1,"mutual matrix symmetry reciprocal work",M,M,method="energy-Hessian")
    i1,i2=.9,-.4
    U=.5*(L1*i1*i1+2*M*i1*i2+L2*i2*i2)
    check("E236",2,"work integral equals quadratic magnetic energy",
          integrate(lambda s:(L1*(s*i1)+M*(s*i2))*i1+(M*(s*i1)+L2*(s*i2))*i2,0,1),U,method="path-work")
    check("E236",3,"inductance positive definiteness",L1*L2-M*M>0,1,method="Sylvester-criterion")
    check("E236",4,"short-circuit induced equivalent leakage inductance",L1-M*M/L2,L1*(1-M*M/(L1*L2)),method="Schur-complement")
    # E237 spin Bloch resonance
    om1=1.8;T1=4.;T2=.7;det=.9;M0=3.
    mx=om1*M0*det*T2*T2/(1+det*det*T2*T2)
    my=-om1*M0*T2/(1+det*det*T2*T2)
    check("E237",1,"Bloch steady transverse torque x balance",
          -mx/T2-det*my,0,method="rotating-frame-balance")
    check("E237",2,"Bloch steady y balance",det*mx-my/T2-om1*M0,0,method="linear-algebra")
    lineshape=lambda delta:T2/(1+delta*delta*T2*T2)
    check("E237",3,"Bloch Lorentz half-width",lineshape(1/T2),lineshape(0)/2,method="linewidth")
    check("E237",4,"resonance longitudinal saturation",M0/(1+om1*om1*T1*T2),M0/(1+(om1*S(T1*T2))**2),method="nonlinear-steady-state")
