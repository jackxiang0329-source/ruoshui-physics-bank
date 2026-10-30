from qa_common import *

def run():
    # T226 Maxwell area and van der Waals critical point
    aa,b,R=3.,.8,8.
    vc=3*b;tc=8*aa/(27*R*b);pc=aa/(27*b*b)
    press=lambda v,t:R*t/(v-b)-aa/(v*v)
    check("T226",1,"critical vdW isotherm first derivative",
          der(lambda v:press(v,tc),vc),0,method="critical-stationarity")
    check("T226",2,"critical vdW second derivative",
          der2(lambda v:press(v,tc),vc),0,method="critical-inflection")
    tl=.91*tc;pl=2.*b;pg=7.*b
    integral=integrate(lambda v:press(v,tl),pl,pg,12000)
    check("T226",3,"Maxwell equal-area antiderivative verified",
          integral,R*tl*L((pg-b)/(pl-b))+aa*(1/pg-1/pl),method="thermodynamic-integration")
    check("T226",4,"vdW critical compressibility factor",pc*vc/(R*tc),3/8,method="critical-exponent-constraint")
    # T227 Sackur Tetrode thermodynamics
    N,V,T,h,k,m=50.,100.,3.,1.,1.,1.5
    lt=lambda temp:h/S(2*P*m*k*temp)
    F=lambda temp,volume:-N*k*temp*(L(volume/(N*lt(temp)**3))+1)
    check("T227",1,"ideal canonical logarithm and Stirling free energy",F(T,V),-N*k*T*(L(V/(N*lt(T)**3))+1),method="partition-function")
    check("T227",2,"entropy from finite derivative",
          -der(lambda t:F(t,V),T),N*k*(L(V/(N*lt(T)**3))+2.5),method="thermodynamic-derivative")
    check("T227",3,"ideal reversible adiabatic exponent",
          (3/2)*(2/3),1,method="entropy-invariant")
    check("T227",4,"twofold identical gas coalescence no mixing entropy",
          2*N*k*L((2*V)/(2*N))-2*N*k*L(V/N),0,method="Gibbs-indistinguishability")
    # T228 Planck mode variance
    x=.7;occup=1/(E(x)-1);M=100.;hnu=2.
    check("T228",1,"Bose geometrical occupation variance",
          occup*(1+occup),E(x)/(E(x)-1)**2,method="partition-fluctuation")
    mean=M*hnu*occup;variance=M*hnu*hnu*occup*(1+occup)
    check("T228",2,"Einstein wave plus particle fluctuation",variance,hnu*mean+mean*mean/M,method="two-term-decomposition")
    check("T228",3,"relative thermal energy noise for many modes",
          S(variance)/mean,S((1+occup)/(M*occup)),method="statistical-scaling")
    check("T228",4,"high-occupation single mode relative fluctuations",
          S(1+1/1e8),1,tol=1e-7,method="Rayleigh-Jeans-limit")
    # T229 Onsager energy machine
    L11,L22,L12,X2=2.,3.,1.5,.7
    q2=L12*L12/(L11*L22)
    check("T229",1,"positive determinant guarantees squared coupling less one",q2<1,1,method="positive-Hessian")
    X1=-L12*X2/(2*L11);power=lambda x:-x*(L11*x+L12*X2)
    check("T229",2,"maximum power via derivative",der(power,X1),0,method="load-optimization")
    yopt=1/(1+S(1-q2))
    eff=lambda y:q2*y*(1-y)/(1-q2*y)
    check("T229",3,"maximum Onsager efficiency formula",
          eff(yopt),(1-S(1-q2))/(1+S(1-q2)),method="nonlinear-optimization")
    check("T229",4,"power-matched linear efficiency",eff(.5),q2/(2*(2-q2)),method="power-versus-efficiency")
    # T230 magnetic Maxwell relation
    Ccur,mu0,H,T,Cp=2.,1.3,.4,3.,7.
    M=lambda h,t:Ccur*h/t
    check("T230",1,"free-energy cross derivative reciprocity",
          mu0*der(lambda t:M(H,t),T),-mu0*Ccur*H/(T*T),method="Maxwell-cross-derivative")
    Sdiff=lambda h:-mu0*Ccur*h/(T*T)
    check("T230",2,"magnetic entropy field derivative",der(lambda h:-mu0*Ccur*h*h/(2*T*T),H),Sdiff(H),method="entropy-field-derivative")
    check("T230",3,"adiabatic field temperature response",
          -mu0*T/Cp*der(lambda t:M(H,t),T),mu0*Ccur*H/(Cp*T),method="isentropic-identity")
    check("T230",4,"Curie magnetization decreases with temperature",
          M(H,T)-M(H,T+.3)>0,1,method="thermodynamic-sign")
    # T231 trapped Bose density
    z3=1.202056903159594;z4=P**4/90
    omx,omy,omz=1.,2.,3.;N=300.;hb=1.;kb=1.
    Tc=(N*omx*omy*omz/z3)**(1/3)
    check("T231",1,"harmonic trap excited-mode DOS integral",
          integrate(lambda x:x*x/2,0,3),3**3/6,method="phase-space-volume")
    check("T231",2,"trapped Bose critical excited population",
          z3*Tc**3/(omx*omy*omz),N,method="Bose-number")
    t=.7*Tc
    check("T231",3,"trapped BEC heat capacity temperature derivative",
          der(lambda tt:3*z4*tt**4/(omx*omy*omz),t),12*z4*t**3/(omx*omy*omz),method="Bose-thermal-energy")
    check("T231",4,"condensed fraction power below Tc",
          1-(t/Tc)**3,1-.7**3,method="critical-scaling")
    # T232 temperature-dependent conduction
    kap0,Temp0,n,Lx,Th,Tc=2.,1.7,1.2,3.,8.,4.
    kap=lambda T:kap0*(T/Temp0)**n
    J=integrate(kap,Tc,Th)/Lx
    check("T232",1,"Fourier temperature profile integrated flux",
          J,kap0/(Temp0**n)*(Th**(n+1)-Tc**(n+1))/((n+1)*Lx),method="nonlinear-flux-integral")
    check("T232",2,"n=-1 logarithmic Fourier flux",
          integrate(lambda t:kap0*Temp0/t,Tc,Th)/Lx,kap0*Temp0/Lx*L(Th/Tc),method="special-exponent")
    check("T232",3,"entropy production equals reservoir entropy increase",
          J*(1/Tc-1/Th),J/Th*(Th/Tc-1),method="entropy-balance")
    hh=.00001
    check("T232",4,"small temperature interval effective conductivity",
          integrate(kap,Th-hh,Th+hh)/(2*hh),kap(Th),method="linear-response-limit")
    # T233 binary mixture stability
    Rg,T,Om=8.,3.,30.
    f=lambda x:Rg*T*(x*L(x)+(1-x)*L(1-x))+Om*x*(1-x)
    x=.27
    check("T233",1,"binary chemical potential difference from free energy",
          der(f,x),Rg*T*L(x/(1-x))+Om*(1-2*x),method="Gibbs-derivative")
    check("T233",2,"binary stability Hessian",
          der2(f,x),Rg*T/(x*(1-x))-2*Om,tol=2e-5,method="Gibbs-curvature")
    Tc=Om/(2*Rg)
    check("T233",3,"critical mixture spinodal composition",
          Rg*Tc/(.5*.5)-2*Om,0,method="critical-condition")
    rootx=root(lambda z:Rg*(.7*Tc)*L(z/(1-z))+Om*(1-2*z),.0001,.49)
    check("T233",4,"symmetric binodal common tangent",
          f(rootx)-f(1-rootx),0,method="two-phase-symmetry")
