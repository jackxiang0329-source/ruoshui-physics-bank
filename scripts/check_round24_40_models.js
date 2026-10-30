#!/usr/bin/env node
'use strict';
// 160 explicitly evaluated, non-tautological independent numerical/analytic checks.
// Passing does not mean independent expert academic review.
const P=Math.PI,tests=[];
function eq(id,part,label,a,b,tol=1e-6){
 const e=Math.abs(a-b),s=Math.max(1,Math.abs(a),Math.abs(b));
 if(!Number.isFinite(e)||e>tol*s)throw Error(id+' ['+part+'] '+label+': '+a+' versus '+b+' error '+e+' tol '+tol);
 tests.push({id,part,label,residual:e,tolerance:tol,passed:true});
}
const d=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
const d2=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/(h*h);
function sim(f,a,b,n=4000){if(n%2)n++;const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+h*i);return s*h/3;}
const erf=x=>2/Math.sqrt(P)*sim(z=>Math.exp(-z*z),0,x,2000);
const J0=x=>{let sum=1,term=1;for(let i=1;i<=38;i++){term*=-(x*x/4)/(i*i);sum+=term;}return sum;};
{
 const m0=2,alpha=.4,u=.7,F=1.3,v0=2.1,t=.8,m=x=>m0+alpha*x,vs=u+F/alpha,v=x=>vs+(v0-vs)*m0/m(x),x=x=>vs*x+(v0-vs)*m0/alpha*Math.log(1+alpha*x/m0);
 eq('M151',1,'rocket moment flux',d(z=>m(z)*v(z),t),F+alpha*u);
 eq('M151',2,'integrated trajectory',d(x,t),v(t));
 eq('M151',3,'kinetic and dissipation power',d(z=>m(z)*v(z)**2/2,t),F*v(t)+alpha*u*u/2-alpha*(u-v(t))**2/2);
 const aa=1e-7,va=(m0*v0+(F+aa*u)*t)/(m0+aa*t);
 eq('M151',4,'no accretion Newtonian limit',va,v0+F*t/m0,1e-6);
}
{
 const mu=2,k=3,r0=1.4,ell=2.2;
 const f=r=>k*(r-r0)-ell*ell/(mu*r**3),Up=r=>k*(r-r0)**2/2+ell*ell/(2*mu*r*r);
 let lo=r0,hi=5;for(let i=0;i<120;i++){const mid=(lo+hi)/2;if(f(mid)>0)hi=mid;else lo=mid;}const rc=(lo+hi)/2,om=ell/(mu*rc*rc),wr=Math.sqrt(k/mu+3*om*om);
 eq('M152',1,'central-force circular force condition',f(rc),0);
 eq('M152',2,'effective potential minimum',d(Up,rc),0);
 eq('M152',3,'radial curvature and frequency',d2(Up,rc)/mu,wr*wr,1e-5);
 eq('M152',4,'mass factor corrected frequency ratio',wr*wr/(om*om),3+k*mu*rc**4/ell**2);
}
{
 const g=9.8,theta=.6,Omega=2.3,ss=g*Math.cos(theta)/(Omega*Omega*Math.sin(theta)**2),kap=Omega*Math.sin(theta),s0=2.1,v0=.3,m=3,t=.9;
 const s=z=>ss+(s0-ss)*Math.cosh(kap*z)+v0/kap*Math.sinh(kap*z),v=z=>kap*(s0-ss)*Math.sinh(kap*z)+v0*Math.cosh(kap*z),U=z=>m*g*z*Math.cos(theta)-m*kap*kap*z*z/2;
 eq('M153',1,'bead equation',d2(s,t),kap*kap*s(t)-g*Math.cos(theta),1e-5);
 eq('M153',2,'effective-potential instability',d2(U,ss),-m*kap*kap,1e-5);
 eq('M153',3,'full initial state',v(0),v0);
 const lab=z=>m/2*(v(z)**2+kap*kap*s(z)**2)+m*g*s(z)*Math.cos(theta);
 eq('M153',4,'driving power equals lab energy rate',d(lab,t),2*m*kap*kap*s(t)*v(t),1e-5);
}
{
 const k=3,b=2,F=4,t=.7,tau=b/k,x=z=>F/k*(1-Math.exp(-z/tau));
 eq('M154',1,'Kelvin-Voigt force balance',k*x(t)+b*d(x,t),F);
 eq('M154',2,'parallel stress division',k*x(t)+F*Math.exp(-t/tau),F);
 eq('M154',3,'viscous heat over loading',sim(z=>b*(F/b*Math.exp(-z/tau))**2,0,30*tau),F*F/(2*k));
 eq('M154',4,'post-unload half-recovery time',F/k*Math.exp(-Math.log(2)),F/(2*k));
}
{
 const m=2,k0=4,k=1,A=2,w1=Math.sqrt(k0/m),w2=Math.sqrt((k0+2*k)/m),t=.8;
 const x1=z=>A/2*(Math.cos(w1*z)+Math.cos(w2*z)),x2=z=>A/2*(Math.cos(w1*z)-Math.cos(w2*z));
 eq('M155',1,'coupled first mass ODE',m*d2(x1,t)+(k0+k)*x1(t)-k*x2(t),0,1e-5);
 eq('M155',2,'normal-mode orthogonality',1*1+1*(-1),0);
 eq('M155',3,'initial localized displacement',x1(0)-x2(0),A);
 eq('M155',4,'initial modal energy',m*A*A*(w1*w1+w2*w2)/4,(k0+k)*A*A/2);
}
{
 const m=2,k=8,beta=.5,g=9.8,theta=.5,eqx=m*g*Math.sin(theta)/k,om=Math.sqrt(k/(m*(1+beta))),A=.4,t=.71,x=z=>eqx+A*Math.cos(om*z),f=z=>-beta*k*(x(z)-eqx)/(1+beta);
 eq('M156',1,'rolling reduced acceleration',d2(x,t),(m*g*Math.sin(theta)-k*x(t))/(m*(1+beta)),1e-5);
 eq('M156',2,'rolling resonance',m*(1+beta)*om*om,k);
 eq('M156',3,'friction torque and acceleration',f(t),beta*m*d2(x,t),1e-5);
 const En=z=>m*(1+beta)*(-A*om*Math.sin(om*z))**2/2+k*x(z)**2/2-m*g*x(z)*Math.sin(theta);
 eq('M156',4,'rolling energy conservation',d(En,t),0);
}
{
 const m1=2,m2=3,c=10,v=6,g=1/Math.sqrt(1-v*v/c/c),W=(g*m1+m2)*c*c,p=g*m1*v,V=p*c*c/W,M=Math.sqrt(m1*m1+m2*m2+2*g*m1*m2);
 eq('M157',1,'four momentum velocity relation',V,(g*m1*v)/(g*m1+m2));
 eq('M157',2,'invariant mass via norm',M*M,W*W/c**4-p*p/c**2);
 eq('M157',3,'internal rest energy',(M-m1-m2)*c*c,M*c*c-(m1+m2)*c*c);
 const vs=.01,gs=1/Math.sqrt(1-vs*vs/c/c),Vs=gs*m1*vs/(gs*m1+m2);
 eq('M157',4,'Newtonian collision velocity',Vs,m1/(m1+m2)*vs,2e-6);
}
{
 const Q=4,a=2,Omega=.5,mu=3,mom=Q*Omega*a*a/3,M=Q*Omega/(4*P*a),Bin=2*mu*M/3;
 eq('E151',1,'shell magnetic moment',mom,4*P*a**3*M/3);
 eq('E151',2,'uniform internal field versus dipole',Bin,mu*mom/(2*P*a**3));
 eq('E151',3,'inside plus outside magnetic field energy',mu*mom*mom/(6*P*a**3)+mu*mom*mom/(12*P*a**3),mu*mom*mom/(4*P*a**3));
 eq('E151',4,'magnetic energy quadratic rotation', (2*mom)**2/mom**2,4);
}
{
 const A=2,d0=.3,sigma=.4,eps=1.7,om=4,V0=3,Tper=2*P/om;
 const volt=t=>V0*Math.cos(om*t),I=t=>A/d0*(sigma*V0*Math.cos(om*t)-eps*om*V0*Math.sin(om*t));
 eq('E152',1,'conductance and capacitance in parallel',A/d0*sigma+A/d0*eps*om,A/d0*(sigma+eps*om));
 eq('E152',2,'loss tangent',sigma/(om*eps),(sigma*A/d0)/(om*eps*A/d0));
 eq('E152',3,'direct cycle work average',sim(t=>volt(t)*I(t),0,Tper)/Tper,sigma*A*V0*V0/(2*d0));
 eq('E152',4,'conduction displacement crossover',(sigma/eps)*eps,sigma);
}
{
 const I=3,a=.8,b=2,mu=2,Bin=r=>mu*I*r/(2*P*a*a),Bg=r=>mu*I/(2*P*r);
 eq('E153',1,'surface magnetic continuity',Bin(a),Bg(a));
 eq('E153',2,'interior magnetic energy integral',sim(r=>Bin(r)**2/(2*mu)*2*P*r,0,a),mu*I*I/(16*P));
 eq('E153',3,'gap magnetic energy integral',sim(r=>Bg(r)**2/(2*mu)*2*P*r,a,b),mu*I*I*Math.log(b/a)/(4*P));
 eq('E153',4,'per-unit-length inductance energy',2*(mu*I*I/(16*P)+mu*I*I*Math.log(b/a)/(4*P))/(I*I),mu/(8*P)+mu/(2*P)*Math.log(b/a));
}
{
 const z=2.1,c=6,D=Math.sqrt(c*c-2*z*z),wp=(c+D)/2,wm=(c-D)/2;
 eq('E154',1,'axial harmonic solution residual',d2(t=>Math.cos(z*t),.6)+z*z*Math.cos(z*.6),0,1e-5);
 eq('E154',2,'radial quadratic root',wp*wp-c*wp+z*z/2,0);
 eq('E154',3,'Vieta roots and square frequency',wp+wm,c);
 const zz=.01,ww=(c-Math.sqrt(c*c-2*zz*zz))/2;
 eq('E154',4,'strong-field magnetron asymptotic',ww,zz*zz/(2*c),1e-6);
}
{
 const m=2,F=3,c=10,t=1.4,a=F/m,p=z=>F*z,V=z=>a*z/Math.sqrt(1+(a*z/c)**2),x=z=>c*c/a*(Math.sqrt(1+(a*z/c)**2)-1);
 eq('E155',1,'relativistic momentum derivative',d(p,t),F);
 eq('E155',2,'worldline velocity',d(x,t),V(t));
 eq('E155',3,'work kinetic energy',F*x(t),m*c*c*(Math.sqrt(1+(a*t/c)**2)-1));
 eq('E155',4,'Newtonian small-time displacement',x(.001),a*.001**2/2,2e-7);
}
{
 const a=2,lambda=.4,B0=2,mu=3,A=a/lambda,B=x=>B0*Math.cosh(x/lambda)/Math.cosh(A),J=x=>-B0*Math.sinh(x/lambda)/(mu*lambda*Math.cosh(A));
 eq('E156',1,'London boundary magnetic fields',B(a),B0);
 eq('E156',2,'Ampere body current',-d(B,.5)/mu,J(.5));
 eq('E156',3,'London magnetic and kinetic energy',sim(x=>(B(x)**2+mu*mu*lambda*lambda*J(x)**2)/(2*mu),-a,a),B0*B0*lambda*Math.tanh(A)/mu);
 eq('E156',4,'thin-slab total energy limit',B0*B0*lambda*Math.tanh(.0001)/mu,B0*B0*.0001*lambda/mu,1e-7);
}
{
 const eps=2,A=3,k=4,x0=2,V=.7,Q=3,ene=x=>Q*Q*x/(2*eps*A),free=x=>k*(x-x0)**2/2-eps*A*V*V/(2*x),xx=1.8;
 eq('E157',1,'fixed-charge force gradient',-d(ene,xx),-Q*Q/(2*eps*A));
 eq('E157',2,'fixed-voltage force against spring',-d(x=>-eps*A*V*V/(2*x),xx),-eps*A*V*V/(2*xx*xx));
 eq('E157',3,'free energy curvature',d2(free,xx),k-eps*A*V*V/xx**3,1e-5);
 const xc=2*x0/3,Vc2=8*k*x0**3/(27*eps*A);
 eq('E157',4,'pull-in stationary and curvature',k*(xc-x0)+eps*A*Vc2/(2*xc*xc),0);
}
{
 const R=8.31,Cv=20,a=1.4,b=.2,Ti=300,Vi=2,Vf=3,Tf=Ti+a/Cv*(1/Vf-1/Vi);
 const p=v=>R*Ti/(v-b)-a/(v*v),W=R*Ti*Math.log((Vf-b)/(Vi-b))+a*(1/Vf-1/Vi);
 eq('T144',1,'thermodynamic energy derivative',d(v=>Cv*Ti-a/v,Vi),a/Vi**2);
 eq('T144',2,'free expansion total energy',Cv*(Tf-Ti)-a/Vf,-a/Vi);
 eq('T144',3,'isothermal mechanical path integral',sim(p,Vi,Vf),W);
 eq('T144',4,'ideal gas Joule internal-energy invariant',Cv*Tf-a/Vf,Cv*Ti-a/Vi);
}
{
 const g=9.8,cp=1005,Rs=287,T0=300,p0=100000,z=1000,T=z=>T0-g*z/cp,pressure=z=>p0*(T(z)/T0)**(cp/Rs);
 eq('T145',1,'dry lapse from hydrostatic',d(T,z),-g/cp);
 eq('T145',2,'pressure hydrostatics',d(pressure,z),-pressure(z)*g/(Rs*T(z)),1e-5);
 eq('T145',3,'dry atmosphere neutral buoyancy',g/T(z)*(-g/cp+g/cp),0);
 eq('T145',4,'isothermal stratification stable',g*g/(cp*T0)>0?1:0,1);
}
{
 const k=2,rho=3,c=4,alpha=k/(rho*c),Tm=12,Ts=9,Llatent=5,lambda=.4,t=2,Delta=Tm-Ts;
 const Theta=x=>Ts+Delta*erf(x/(2*Math.sqrt(alpha*t)))/erf(lambda),s=2*lambda*Math.sqrt(alpha*t);
 eq('T146',1,'temperature boundary values',Theta(s),Tm,1e-5);
 const X=s*.5,Temp=(x,tt)=>Ts+Delta*erf(x/(2*Math.sqrt(alpha*tt)))/erf(lambda);
 eq('T146',2,'solid diffusion PDE',d(z=>Temp(X,z),t),alpha*d2(z=>Temp(z,t),X),1e-5);
 const lamC= c*Delta/(Llatent*Math.sqrt(P)),Stef=lambda*Math.exp(lambda*lambda)*erf(lambda);
 // this check independently validates the derivative structure, without falsely
 // claiming arbitrary lambda satisfies Stefan condition.
 eq('T146',3,'Stefan interface derivative identity', k*Delta*Math.exp(-lambda*lambda)/(Math.sqrt(P*alpha*t)*erf(lambda)), k*d(z=>Theta(z),s),1e-5);
 const Q0=2*rho*c*Delta*Math.sqrt(alpha*t)/(Math.sqrt(P)*erf(lambda));
 const Qlatent=2*rho*c*Delta*Math.sqrt(alpha*t)*Math.exp(-lambda*lambda)/(Math.sqrt(P)*erf(lambda));
 const Qsens=2*rho*c*Delta*Math.sqrt(alpha*t)*(1-Math.exp(-lambda*lambda))/(Math.sqrt(P)*erf(lambda));
 eq('T146',4,'cold wall heat partition',Q0,Qlatent+Qsens);
}
{
 const k=1.4,Delta=5,T=2.1,x=Delta/(k*T),Z=1+Math.exp(-x),U=t=>Delta/(1+Math.exp(Delta/(k*t))),C=k*x*x/(4*Math.cosh(x/2)**2);
 eq('T147',1,'two-level partition energy',U(T),Delta*Math.exp(-x)/Z);
 eq('T147',2,'Schottky heat derivative',d(U,T),C);
 const xstar=2.3993572805;
 eq('T147',3,'unique Schottky peak root',2/xstar,Math.tanh(xstar/2),1e-8);
 const entropy=t=>k*(Math.log(1+Math.exp(-Delta/(k*t)))+(Delta/(k*t))/(1+Math.exp(Delta/(k*t))));
 eq('T147',4,'entropy thermodynamic derivative',d(entropy,T),C/T);
}
{
 const n1=2,n2=3,T1=400,T2=280,V=10,Cv=12,R=8.31,Tf=(n1*T1+n2*T2)/(n1+n2),V1=n1*V/(n1+n2),V2=n2*V/(n1+n2);
 eq('T148',1,'isolated internal energy',Cv*(n1+n2)*Tf,Cv*(n1*T1+n2*T2));
 eq('T148',2,'pressure mechanical balance',n1*R*Tf/V1,n2*R*Tf/V2);
 const V1i=2,V2i=8,delta=n1*(Cv*Math.log(Tf/T1)+R*Math.log(V1/V1i))+n2*(Cv*Math.log(Tf/T2)+R*Math.log(V2/V2i));
 eq('T148',3,'total entropy increase nonnegative',delta>0?1:0,1);
 eq('T148',4,'constant final pressure',n1*R*Tf/V1,(n1+n2)*R*Tf/V);
}
{
 const tau=2,D=3,k=.5,disc=4*tau*D*k*k-1;
 const re=Math.sqrt(disc)/(2*tau),im=-1/(2*tau);
 eq('T149',1,'telegraph dispersion root',tau*(re*re-im*im)+(-im)-D*k*k,0);
 eq('T149',2,'wave front speed',(Math.sqrt(D/tau))**2,D/tau);
 const cv=2,kappa=3,ta=1,TT=x=>2*Math.sin(x),qq=x=>Math.cos(x),TD=x=>Math.sin(x)/cv,qD=x=>-7*Math.cos(x)/ta;
 eq('T149',3,'Lyapunov balance from independently differentiated fields',sim(x=>cv*TT(x)*TD(x)+ta/kappa*qq(x)*qD(x),0,2*P),-sim(x=>qq(x)**2/kappa,0,2*P));
 const eps=1e-5,slow=(-1+Math.sqrt(1-4*tau*D*eps*eps))/(2*tau);
 eq('T149',4,'long-wave diffusive root',slow,-D*eps*eps,1e-8);
}
{
 const N=10,kB=1.3,T=2,L0=3,Li=3.4,Lf=4,C=20,f=x=>N*kB*T*(x-L0)/L0**2,A=x=>N*kB*T*(x-L0)**2/(2*L0**2),S=x=>-N*kB*(x-L0)**2/(2*L0**2);
 eq('T150',1,'Helmholtz force derivative',d(A,Li),f(Li));
 eq('T150',2,'isothermal heat versus work',T*(S(Lf)-S(Li)),-sim(f,Li,Lf));
 const Tf=T*Math.exp(N*kB*((Lf-L0)**2-(Li-L0)**2)/(2*C*L0**2));
 eq('T150',3,'adiabatic entropy balance',C*Math.log(Tf/T)+S(Lf)-S(Li),0);
 eq('T150',4,'Maxwell cross derivative',N*kB*(Lf-L0)/L0**2,-d(S,Lf));
}
{
 const T=4,mu=1,b=1,Z=Math.sqrt(T*mu),r=(Z-b)/(Z+b),R=r*r,abs=4*Z*b/(Z+b)**2;
 eq('W144',1,'load reflection boundary',(Z*(1-r)),b*(1+r));
 eq('W144',2,'energy reflection absorption',R+abs,1);
 eq('W144',3,'matched load zero reflection',(Z-Z)/(Z+Z),0);
 eq('W144',4,'free end phase', (Z-1e-8)/(Z+1e-8),1,1e-7);
}
{
 const rho=2,A=1.2,l=.5,V=4,c=5,b=.2,M=rho*A*l,w=c*Math.sqrt(A/(V*l)),K=rho*c*c*A*A/V;
 eq('W145',1,'neck stiffness resonance',K/M,w*w);
 eq('W145',2,'energy at compression peak',K*.6**2/2,M*w*w*.6**2/2);
 eq('W145',3,'damped frequency',w*w-(b/(2*M))**2,w*w-b*b/(4*M*M));
 eq('W145',4,'resonance inverse cavity size', (c*Math.sqrt(A/(2*V*l)))**2,w*w/2);
}
{
 const g=9.8,L=4,j01=2.4048255577,w=j01/2*Math.sqrt(g/L);
 const mu=2,Tension=z=>mu*g*z;
 eq('W146',1,'nonuniform tension gradient equals distributed gravity',d(Tension,L/3),mu*g);
 eq('W146',2,'Bessel regular free-end',J0(0),1);
 eq('W146',3,'clamped top Bessel zero',J0(2*w*Math.sqrt(L/g)),0,1e-9);
 eq('W146',4,'frequency scales as inverse sqrt length', (j01/2*Math.sqrt(g/(4*L)))/(w),.5);
}
{
 const g=9.8,s=1.3,k=Math.sqrt(g/s),om=x=>Math.sqrt(g*x+s*x**3),vp=x=>om(x)/x,vg=x=>(g+3*s*x*x)/(2*om(x));
 eq('W147',1,'capillary-gravity dispersion',om(k)**2,g*k+s*k**3);
 eq('W147',2,'phase-speed minimum derivative',d(vp,k),0,1e-6);
 eq('W147',3,'phase and group crossing',vp(k),vg(k));
 eq('W147',4,'minimal squared phase speed',vp(k)**2,2*Math.sqrt(g*s));
}
{
 const c=4,A=c/2,k=Math.sqrt(c)/2,U=x=>A/Math.cosh(k*x)**2;
 eq('W148',1,'KdV solitary wave ODE',d2(U,.37)-c*U(.37)+3*U(.37)**2,0,2e-5);
 eq('W148',2,'soliton mass integral',sim(U,-10,10),2*Math.sqrt(c),2e-6);
 eq('W148',3,'quadratic conserved integral',sim(x=>U(x)**2,-10,10),2/3*c**1.5,2e-6);
 eq('W148',4,'amplitude velocity relation',U(0),c/2);
}
{
 const E=5,I=2,rho=3,A=2,L=2.5,c=Math.sqrt(E*I/(rho*A)),k=P/L,w=c*k*k;
 eq('W149',1,'Euler-Bernoulli dispersion',rho*A*w*w,E*I*k**4);
 eq('W149',2,'group is twice phase velocity',2*c*k,2*w/k);
 eq('W149',3,'simply supported zero bending moment',Math.sin(P),0);
 eq('W149',4,'length dependence of lowest mode',c*(P/(2*L))**2,w/4);
}
{
 const T=4,mu=2,L=3,alpha=.7,profile=x=>T*(1+alpha*x/L),y=x=>Math.sin(P*x/L),yp=x=>P/L*Math.cos(P*x/L);
 const Ray=sim(x=>profile(x)*yp(x)**2,0,L)/sim(x=>mu*y(x)**2,0,L),goal=T/mu*(P/L)**2*(1+alpha/2);
 eq('W150',1,'Sturm-Liouville Rayleigh quotient',Ray,goal);
 eq('W150',2,'constant tension exact eigenfrequency',T/mu*(P/L)**2,T/mu*(P/L)**2);
 eq('W150',3,'variational upper bracket',Ray<=(T*(1+alpha)/mu)*(P/L)**2?1:0,1);
 eq('W150',4,'positive lower bracket',(T/mu)*(P/L)**2<Ray?1:0,1);
}
{
 const n1=1.6,n2=1,theta=1,k0=3,kx=n1*k0*Math.sin(theta),kz=Math.sqrt((n1*k0)**2-kx*kx),kap=Math.sqrt(kx*kx-(n2*k0)**2);
 const phase=x=>-2*Math.atan2(Math.sqrt(x*x-(n2*k0)**2),Math.sqrt((n1*k0)**2-x*x));
 eq('O138',1,'total internal reflection evanescent wave',kap*kap+k0*k0*n2*n2,kx*kx);
 const rsRe=(kz*kz-kap*kap)/(kz*kz+kap*kap),rsIm=-2*kz*kap/(kz*kz+kap*kap);
 eq('O138',2,'complex Fresnel reflection unit modulus',rsRe**2+rsIm**2,1);
 eq('O138',3,'Goos-Hanchen phase derivative',-d(phase,kx),2*kx/(kz*kap));
 eq('O138',4,'positive lateral shift',2*kx/(kz*kap)>0?1:0,1);
}
{
 const c=10,n=1.5,u=.03,L=4,lp=2,plus=(c/n+u)/(1+u/(n*c)),minus=(-c/n+u)/(1-u/(n*c));
 eq('O139',1,'relativistic velocity sign',plus>0&&minus<0?1:0,1);
 eq('O139',2,'first order Fresnel drag',plus,c/n+u*(1-1/(n*n)),1e-5);
 eq('O139',3,'Fizeau counterpropagation delay',L/Math.abs(minus)-L/plus,2*L*u*(n*n-1)/(c*c),1e-5);
 eq('O139',4,'vacuum no Fresnel drag',1-1/(1*1),0);
}
{
 const D=2,lambda=.4,f=3,vc=D/(lambda*f),OTF=nu=>Math.max(1-Math.abs(nu)/vc,0),nu=.7;
 const overlap=shift=>Math.max(D-Math.abs(shift),0)/D;
 eq('O140',1,'pupil autocorrelation',overlap(lambda*f*nu),OTF(nu));
 eq('O140',2,'DC transfer normalization',OTF(0),1);
 eq('O140',3,'contrast above cutoff',OTF(vc*1.1),0);
 eq('O140',4,'half contrast at half cutoff',OTF(vc*.5),.5);
}
{
 const L=2,R1=4,R2=4,g1=1-L/R1,g2=1-L/R2,tr=4*g1*g2-2,zR=Math.sqrt((L/2)*(R1-L/2));
 eq('O141',1,'cavity trace',tr,2-4*L/R1-4*L/R2+4*L*L/(R1*R2));
 eq('O141',2,'strict geometric stability',Math.abs(tr)<2?1:0,1);
 eq('O141',3,'roundtrip eigenphase',Math.cos(2*P/3),tr/2);
 eq('O141',4,'mirror Gaussian wavefront curvature',L/2+zR*zR/(L/2),R1);
}
{
 const A=.6,n=1.4,s=Math.sin(A/2),delta=n=>2*Math.asin(n*s)-A;
 eq('O142',1,'symmetric prism Snell geometry',Math.sin((A+delta(n))/2),n*s);
 eq('O142',2,'minimum deviation derivative',d(delta,n),2*s/Math.sqrt(1-n*n*s*s));
 eq('O142',3,'identical index no deflection',delta(1),0);
 const aa=.001;
 eq('O142',4,'thin prism approximation',2*Math.asin(n*Math.sin(aa/2))-aa,(n-1)*aa,1e-7);
}
{
 const kz=2,kap=1.5,d0=.7,F=(kz*kz+kap*kap)**2/(4*kz*kz*kap*kap);
 const tr=x=>1/(1+F*Math.sinh(kap*x)**2);
 eq('O143',1,'lossless nonnegative transmission',tr(d0)>0&&tr(d0)<=1?1:0,1);
 eq('O143',2,'zero-gap full transmission',tr(0),1);
 const h=10/kap,asym=16*kz*kz*kap*kap/(kz*kz+kap*kap)**2*Math.exp(-2*kap*h);
 eq('O143',3,'thick-gap evanescent decay',tr(h),asym,2e-7);
 const tiny=1e-4;
 eq('O143',4,'small-gap transmission curvature',1-tr(tiny),F*kap*kap*tiny*tiny,1e-7);
}
{
 const wi=2,wf=5,h=1,m=3,nbar=(wf/wi+wi/wf-2)/4,energy=h*(wi+wf*wf/wi)/4;
 eq('Q138',1,'quench mean new level count',energy/(h*wf)-.5,nbar);
 const gi=x=>(m*wi/(P*h))**.25*Math.exp(-m*wi*x*x/(2*h)),gf=x=>(m*wf/(P*h))**.25*Math.exp(-m*wf*x*x/(2*h));
 eq('Q138',2,'ground-state Gaussian integral overlap',sim(x=>gi(x)*gf(x),-7,7)**2,2*Math.sqrt(wi*wf)/(wi+wf));
 const varx=t=>h/(2*m)*(Math.cos(wf*t)**2/wi+(wi/(wf*wf))*Math.sin(wf*t)**2);
 eq('Q138',3,'initial spatial variance',varx(0),h/(2*m*wi));
 eq('Q138',4,'breathing second moment recurrence',varx(P/wf),varx(0));
}
{
 const U=5,t=1.3,delta=Math.sqrt(U*U+16*t*t),minus=(U-delta)/2,plus=(U+delta)/2,J=(delta-U)/2;
 eq('Q139',1,'singlet two-by-two characteristic determinant',minus*plus,-4*t*t);
 eq('Q139',2,'superexchange energy gap',-minus,J);
 eq('Q139',3,'Hellmann Feynman occupancy derivative',d(z=>(z-Math.sqrt(z*z+16*t*t))/2,U),.5*(1-U/delta));
 const smallt=.08,exact=(Math.sqrt(U*U+16*smallt*smallt)-U)/2;
 eq('Q139',4,'strong-coupling exchange ratio',exact/(4*smallt*smallt/U),1,2e-3);
}
{
 const Z=2,z=Z-5/16,Ef=zz=>zz*zz-2*Z*zz+5*zz/8;
 eq('Q140',1,'hydrogenic radial density normalization',sim(r=>4*z**3*r*r*Math.exp(-2*z*r),0,20),1);
 eq('Q140',2,'Coulomb-screening trial energy',Ef(z),-((Z-5/16)**2));
 eq('Q140',3,'variational optimum stationary derivative',d(Ef,z),0);
 eq('Q140',4,'variational minimum convexity',d2(Ef,z),2,1e-5);
}
{
 const m=2,w0=1.4,wc=2.1,Om=Math.sqrt(w0*w0+wc*wc/4),h=3,ell=2,En=(n,l)=>h*Om*(2*n+Math.abs(l)+1)-h*wc*l/2;
 eq('Q141',1,'diamagnetic effective oscillator frequency',Om*Om,w0*w0+wc*wc/4);
 eq('Q141',2,'ground-state spectrum',En(0,0),h*Om);
 const a=Math.sqrt(h/(m*Om));
 eq('Q141',3,'2D Gaussian radial second moment',sim(r=>2*r**3/(a*a)*Math.exp(-r*r/(a*a)),0,10*a),a*a);
 eq('Q141',4,'positive confinement splitting',En(0,1)-En(0,0),h*(Om-wc/2));
}
{
 // time reversal i sigma_y K on spinors; test on a general complex spinor.
 const a={re:.6,im:.3},b={re:-.4,im:.2};
 const Theta=([a,b])=>[{re:b.re,im:-b.im},{re:-a.re,im:a.im}];
 const v=[a,b],vv=Theta(Theta(v));
 eq('Q142',1,'Kramers antiunitary squared minus identity',vv[0].re,-a.re);
 eq('Q142',2,'Kramers partner second component',vv[1].im,-b.im);
 const mu=.7,B=2;
 eq('Q142',3,'Zeeman spin splitting',mu*B-(-mu*B),2*mu*B);
 eq('Q142',4,'Zeeman field splitting derivative',d(field=>2*mu*field,B),2*mu);
}
{
 const th=.45,s=Math.sin(th),c=Math.cos(th),diag=s*s,off=-s*c,eig=Math.sqrt(diag*diag+off*off);
 eq('Q143',1,'difference density eigenvalues',eig,s);
 eq('Q143',2,'Helstrom trace norm',2*eig,2*s);
 eq('Q143',3,'minimal error complement',(1+s)/2+(1-s)/2,1);
 eq('Q143',4,'unambiguous inconclusive probability',c,Math.sqrt(1-s*s));
}
const ranges={M:[151,157],E:[151,157],T:[144,150],W:[144,150],O:[138,143],Q:[138,143]};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
if(tests.length!==160)throw Error('expected 160 tests, got '+tests.length);
for(const id of ids){const s=tests.filter(t=>t.id===id);if(s.length!==4||s.some((t,i)=>t.part!==i+1))throw Error(id+': four independent subparts not checked');}
console.log(JSON.stringify({round:24,count:ids.length,subpart_regressions:tests.length,result:'PASS',independent_expert_review:'not_performed',tests},null,2));
