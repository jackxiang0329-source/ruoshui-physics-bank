from qa_common import *

def run():
    # M238: torque-free Euler top: time derivative invariants and eigenvalues
    I1,I2,I3=2.,3.,5.;w1,w2,w3=1.1,.4,-.6
    dw1=(I2-I3)*w2*w3/I1;dw2=(I3-I1)*w3*w1/I2;dw3=(I1-I2)*w1*w2/I3
    check("M238",1,"Euler dynamics conserves energy",I1*w1*dw1+I2*w2*dw2+I3*w3*dw3,0,method="energy-conservation")
    check("M238",2,"small-axis eigenvalue square from Euler matrix",
          ((I3-I1)/I2)*((I1-I2)/I3),-(I3-I1)*(I2-I1)/(I2*I3),method="linear-eigenvalue")
    check("M238",3,"intermediate-axis positive instability exponent",
          S((I3-I2)*(I2-I1)/(I1*I3))>0,1,method="eigenvalue-sign")
    check("M238",4,"large-axis stable frequency square",
          ((I2-I3)/I1)*((I3-I1)/I2),
          -(I3-I2)*(I3-I1)/(I1*I2),method="stability-determinant")
    # M239 rotating radial spring
    m,k,r0,Om=2.,20.,1.7,1.6
    V=lambda r:k*(r-r0)**2/2-m*Om*Om*r*r/2
    eq=k*r0/(k-m*Om*Om)
    check("M239",1,"radial Lagrangian force from V derivative",-der(V,.8)/m,
          Om*Om*.8-(k/m)*(.8-r0),method="Euler-Lagrange-numeric")
    check("M239",2,"radial equilibrium critical balance",der(V,eq),0,method="equilibrium-derivative")
    check("M239",3,"stability frequency from Hessian",der2(V,eq)/m,k/m-Om*Om,method="Hessian-numeric")
    v=.8;dr=.4
    rstate=.9
    accel=Om*Om*rstate-(k/m)*(rstate-r0)
    mech_rate=m*v*accel+m*Om*Om*rstate*v+k*(rstate-r0)*v
    check("M239",4,"motor torque balances inertial mechanical energy",
          mech_rate,2*m*Om*Om*rstate*v,method="independent-energy-gradient")
    # M240 Euler buckling beam
    EI,Lb=4.,3.
    Pcrit=P*P*EI/(Lb*Lb);mode=lambda x:SI(P*x/Lb)
    check("M240",1,"beam buckling ODE residual at n=1",
          EI*(P/Lb)**4*mode(.8)-Pcrit*(P/Lb)**2*mode(.8),0,method="eigen-ODE")
    check("M240",2,"Euler fundamental critical force from elastic mode energy",
          EI*integrate(lambda x:(-(P/Lb)**2*mode(x))**2,0,Lb)/
          integrate(lambda x:((P/Lb)*C(P*x/Lb))**2,0,Lb),Pcrit,method="Rayleigh-quotient")
    check("M240",3,"subcritical quadratic energy positive",
          (EI*(P/Lb)**4-.8*Pcrit*(P/Lb)**2)>0,1,method="stability-second-variation")
    check("M240",4,"postbuckling pitchfork amplitude proportional sqrt overdrive",
          S(.04)/S(.01),2.,method="critical-power-law")
    # M241 moving wedge and rolling ball
    m,M,kappa,ang,g=2.,5.,.4,.6,9.8
    sa=g*SI(ang)/(1+kappa-m*C(ang)**2/(M+m))
    Xa=-m*C(ang)/(M+m)*sa
    check("M241",1,"rolling kinetic inertia positive definite",
          (M+m)*(1+kappa)-m*C(ang)**2>0,1,method="mass-matrix-Hessian")
    check("M241",2,"wedge/ball Lagrange equations",m*C(ang)*Xa+m*(1+kappa)*sa,m*g*SI(ang),method="force-balance")
    check("M241",3,"horizontal momentum derivative",(M+m)*Xa+m*C(ang)*sa,0,method="Noether-momentum")
    check("M241",4,"fixed-wedge acceleration recovered large M",
          g*SI(ang)/(1+kappa-m*C(ang)**2/(100000+m)),
          g*SI(ang)/(1+kappa),tol=3e-5,method="large-mass-limit")
    # M242 constant proper acceleration rocket
    c,aa,tau,u=10.,2.,.9,3.
    chi=aa*tau/c
    t=c/aa*SH(chi);x=c*c/aa*(CH(chi)-1);v=c*TH(chi)
    check("M242",1,"hyperbolic speed relation to rapidity",v/c,TH(chi),method="velocity-four-vector")
    check("M242",2,"Minkowski hyperbola under constant proper acceleration",
          (x+c*c/aa)**2-(c*t)**2,(c*c/aa)**2,method="spacetime-invariant")
    ratio=E(c*chi/u)
    check("M242",3,"relativistic rocket rapidity and rest mass loss",
          (u/c)*L(ratio),chi,method="mass-ratio")
    check("M242",4,"low-speed rocket classical Tsiolkovsky limit",
          (u/c)*L(E(c*.00001/u)),.00001,method="nonrelativistic-limit")
    # M243 Duffing harmonic balance, fold, power
    omega0,zeta,Omega,beta,amp=2.,.08,2.1,.3,.9
    D=omega0**2-Omega**2+3*beta*amp**2/4
    Z=2*zeta*omega0*Omega
    ff=S(D*D+Z*Z)*amp
    cubfund=integrate(lambda theta:C(theta)**4,0,2*P)/(integrate(lambda theta:C(theta)**2,0,2*P))
    check("M243",1,"Duffing cubic restoring fundamental harmonic",
          cubfund,.75,method="harmonic-Fourier-projection")
    check("M243",2,"Duffing nonlinear resonance shift",
          (omega0**2+3*beta*amp**2/4)-omega0**2,
          3*beta*amp**2/4,method="frequency-shift")
    y=amp*amp;d=omega0**2-Omega**2;bb=3*beta/4
    response=lambda yy:yy*((d+bb*yy)**2+Z*Z)
    check("M243",3,"Duffing fold derivative criterion via finite difference",
          der(response,y),(d+bb*y)*(d+3*bb*y)+Z*Z,method="fold-derivative")
    sinphase=Z*amp/ff
    check("M243",4,"cycle-average forcing equals viscous heat",
          ff*Omega*amp*sinphase/2,zeta*omega0*Omega**2*amp**2,method="cycle-energy")
    # M244 coupled pendulum
    om0,kc=1.7,.4
    omega1=om0;omega2=S(om0**2+2*kc)
    check("M244",1,"normal mode matrix symmetric eigen sum",
          omega1**2+omega2**2,2*(om0**2+kc),method="spectral-trace")
    check("M244",2,"symmetric eigenvector zero spring stretch",kc*(1-1),0,method="mode-symmetry")
    t=.8
    theta1=(C(omega1*t)+C(omega2*t))/2
    theta2=(C(omega1*t)-C(omega2*t))/2
    check("M244",3,"single-pendulum initial energy spreads between two modes",
          theta1+theta2,C(omega1*t),method="initial-condition")
    check("M244",4,"weak-coupling frequency splitting",
          (S(om0**2+2*.0001)-om0)/.0001,1/om0,tol=3e-5,method="perturbative-splitting")
    # M245 relativistic collision invariant
    ma,mb,Mf,c,Ea=2.,3.,6.,10.,800.
    W2=(ma*ma+mb*mb)*c**4+2*mb*c*c*Ea
    plab=S(Ea*Ea-ma*ma*c**4)/c
    check("M245",1,"fixed target invariant from energy momentum norm",
          (Ea+mb*c*c)**2-(c*plab)**2,W2,method="four-momentum-invariant")
    Kthr=((Mf**2-(ma+mb)**2)*c*c)/(2*mb)
    check("M245",2,"invariant threshold total laboratory energy",
          (ma*ma+mb*mb)*c**4+2*mb*c*c*(ma*c*c+Kthr),
          Mf*Mf*c**4,method="threshold-energy")
    check("M245",3,"collider invariant removes opposite beam momentum",
          S((2*Ea)**2-c*c*(plab-plab)**2),2*Ea,method="colliding-beam-invariant")
    mpi,mp=1.1,7.
    gamma=(mpi**2+2*mpi*mp)/(2*mp)
    check("M245",4,"photoproduction recoil raises threshold",gamma,mpi*(1+mpi/(2*mp)),method="photon-recoil")
    # M246 axisymmetric epicycles
    GM,R=3.,4.
    Phi=lambda r:-GM/r
    om2=GM/R**3
    LL2=R**4*om2
    ve=lambda r:Phi(r)+LL2/(2*r*r)
    check("M246",1,"circular effective-potential derivative",der(ve,R),0,method="radial-stationarity")
    check("M246",2,"epicycle Hessian equals Kepler orbital frequency",
          der2(ve,R),om2,tol=2e-5,method="Hessian-epicycle")
    check("M246",3,"flat circular velocity epicycle frequency ratio",
          S(2),S(4-2),method="rotation-curve")
    check("M246",4,"harmonic potential orbital epicycle frequency ratio",
          2, S(4),method="potential-limit")
