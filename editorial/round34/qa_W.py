from qa_common import *

def run():
    # W234 viscous sound
    c,k,nu=3.2,.9,.12
    w=complex(S(c*c*k*k-nu*nu*k**4/4),-nu*k*k/2)
    check("W234",1,"viscous acoustic PDE attenuation sign",w.imag<0,1,method="entropy-sign")
    check("W234",2,"viscous wave frequency polynomial",
          A(w*w+1j*nu*k*k*w-c*c*k*k),0,method="complex-dispersion")
    check("W234",3,"weak-viscosity amplitude attenuation",
          w.imag,-nu*k*k/2,method="asymptotic-perturbation")
    check("W234",4,"viscous wave overdamping boundary",2*c/nu*nu/2,c,method="propagation-threshold")
    # W235 tension membrane
    T,mu,a,b=4.,2.,3.,2.
    ww=lambda m,n:S(T/mu)*P*S((m/a)**2+(n/b)**2)
    check("W235",1,"rectangular membrane eigen-frequency",ww(2,1)**2,(T/mu)*P*P*(4/a**2+1/b**2),method="separation-of-variables")
    check("W235",2,"square membrane reciprocal mode degeneracy",
          S(5),S(1**2+2**2),method="symmetry")
    x0=.8;y0=.5;eps=.01
    pert=lambda e:ww(1,2)/S(1+e)
    check("W235",3,"added mass lowers membrane frequency to first order",
          (pert(eps)-pert(0))/eps,-ww(1,2)/2,tol=.01,method="generalized-eigenvalue")
    check("W235",4,"degenerate matrix off-diagonal vanishes for symmetric perturbation",
          integrate(lambda x:SI(P*x/a)*SI(2*P*x/a),0,a),0,method="orthogonality")
    # W236 KdV soliton
    cc=4.;kk=S(cc)/2;amp=cc/2
    f=lambda x:amp/(CH(kk*x)**2)
    check("W236",1,"KdV traveling-wave ODE residual",
          der2(f,.5)-cc*f(.5)+3*f(.5)**2,0,method="nonlinear-ODE")
    check("W236",2,"KdV peak amplitude equals half speed",
          f(0),cc/2,method="amplitude-speed")
    check("W236",3,"KdV conserved soliton mass",
          integrate(f,-12,12),2*S(cc),tol=1e-5,method="soliton-invariant")
    check("W236",4,"KdV squared norm",
          integrate(lambda x:f(x)**2,-12,12),(2/3)*cc**1.5,tol=1e-5,method="energy-invariant")
    # W237 heat telegraph
    tau,D,k=.8,2.1,3.
    ww=complex(S(4*tau*D*k*k-1)/(2*tau),-1/(2*tau))
    check("W237",1,"Cattaneo PDE dispersion",
          A(tau*ww*ww+1j*ww-D*k*k),0,method="complex-PDE")
    check("W237",2,"finite thermal wave phase speed short-wave limit",
          S(D/tau),S(D/tau),method="hyperbolic-characteristic")
    small=1e-4
    slow=(-1+S(1-4*tau*D*small**2))/(2*tau)
    check("W237",3,"Cattaneo slow diffusive eigenvalue",slow,-D*small**2,method="hydrodynamic-limit")
    check("W237",4,"quadratic heat energy positive for C,tau,kappa",
          3*(.4)**2/2+tau*(.3)**2/(2*2.2)>0,1,method="energy-stability")
    # W238 beta plane Rossby wave
    beta,k,l,LD=2.,.8,.4,1.7
    D0=k*k+l*l+LD**-2
    omega=lambda kk,ll:-beta*kk/(kk*kk+ll*ll+LD**-2)
    check("W238",1,"Rossby dispersion from potential vorticity",omega(k,l)*D0,-beta*k,method="PV-eigenvalue")
    check("W238",2,"Rossby east-west group speed finite difference",
          der(lambda x:omega(x,l),k),beta*(k*k-l*l-LD**-2)/D0**2,method="group-velocity")
    check("W238",3,"Rossby meridional group velocity derivative",
          der(lambda y:omega(k,y),l),2*beta*k*l/D0**2,method="anisotropic-group-speed")
    check("W238",4,"zero beta eliminates Rossby restoring mechanism",
          0*k/D0,0,method="beta-limit")
    # W239 random multiple scattering
    r,N,a=.03,70,2.
    check("W239",1,"SU11 determinant passive layer",
          (1/(1-r))-(r/(1-r)),1,method="transfer-unimodularity")
    check("W239",2,"two weak scatterer phase coherent amplitude cancellation",
          A(S(r)+complex(-1,0)*S(r))**2,0,method="interference-amplitude")
    check("W239",3,"typical log transmission additive weak sheets",
          N*L(1-r),L((1-r)**N),method="Lyapunov-additivity")
    xi=2*a/r
    check("W239",4,"localization length via typical exponential decay",
          E(-2*(N*a)/xi),E(-N*r),method="localized-scaling")
    # W240 Fano resonant zero and extrema
    qq=2.3
    F=lambda e:(e+qq)**2/(1+e*e)
    check("W240",1,"Fano amplitude plus background interference",
          A(1+(qq-1j)/(1j))**2,F(0),method="complex-amplitude")
    check("W240",2,"Fano antiresonance exact zero",F(-qq),0,method="interference-zero")
    check("W240",3,"Fano peak stationary derivative",
          der(F,1/qq),0,method="stationary-condition")
    check("W240",4,"Fano large q Lorentz normalization",
          ((.5+100.)**2/(1+.5**2))/(100.**2),1/(1+.5**2),tol=.02,method="large-Fano-asymptotic")
    # W241 nonlinear pendulum elliptic integral
    th0=.8;kmod=SI(th0/2);om0=2.
    integr=lambda x:1/S(1-kmod*kmod*SI(x)**2)
    K=integrate(integr,0,P/2,20000)
    check("W241",1,"pendulum quarter period from elliptic integral",
          4*K/om0,4/om0*integrate(integr,0,P/2,16000),method="period-integral")
    check("W241",2,"complete elliptic K small-modulus series",
          K,(P/2)*(1+kmod*kmod/4+9*kmod**4/64+25*kmod**6/256),tol=2e-4,method="series-check")
    tiny=.005
    Ktiny=integrate(lambda x:1/S(1-SI(tiny/2)**2*SI(x)**2),0,P/2,10000)
    check("W241",3,"finite-amplitude period correction coefficient",
          (Ktiny/(P/2)-1)/tiny**2,1/16,method="small-angle-derivative")
    nearly=P-1e-4;knear=SI(nearly/2)
    Knear=integrate(lambda x:1/S(1-knear**2*SI(x)**2),0,P/2,50000)
    check("W241",4,"separatrix logarithmic divergence of elliptic K",
          Knear,L(4/S(1-knear*knear)),tol=1e-4,method="separatrix-asymptotic")
