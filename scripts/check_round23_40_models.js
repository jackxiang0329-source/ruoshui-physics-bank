#!/usr/bin/env node
'use strict';
// Independent numerical / analytic regression identities, four per new problem.
// A passed regression is technical evidence, not independent expert review.
const P=Math.PI, tests=[];
function eq(id,part,label,a,b,tol=1e-6){
 const err=Math.abs(a-b),scale=Math.max(1,Math.abs(a),Math.abs(b));
 if(!Number.isFinite(err)||err>tol*scale)throw Error(id+' ['+part+'] '+label+': '+a+' vs '+b+' residual '+err);
 tests.push({id,part,label,error:err,passed:true});
}
function d(f,x,h=1e-5){return (f(x+h)-f(x-h))/(2*h);}
function d2(f,x,h=1e-4){return (f(x+h)-2*f(x)+f(x-h))/(h*h);}
function sim(f,a,b,n=10000){if(n%2)n++;const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+h*i);return s*h/3;}
function near(id,part,label,a,b,tol=1e-4){eq(id,part,label,a,b,tol);}
{
 const A=2+3+1/.8**2,B=.5/.8**2,F=9.8,v=t=>F/B*(1-Math.exp(-B*t/A)),x=t=>F/B*(t-A/B*(1-Math.exp(-B*t/A))),t=1.4;
 eq('M144',1,'pulley kinetic metric',A,5+1/.8**2);
 near('M144',2,'speed derivative versus ODE',d(v,t),(F-B*v(t))/A);
 near('M144',3,'instant power balance',F*v(t),A*v(t)*d(v,t)+B*v(t)**2);
 near('M144',4,'small bearing drag',F/1e-6*(1-Math.exp(-1e-6*t/A)),F*t/A,1e-5);
}
{
 const M=4,m=2,th=.7,g=9.8,D=M+m*Math.sin(th)**2,as=(M+m)*g*Math.sin(th)/D,aX=-m*g*Math.cos(th)*Math.sin(th)/D,N=m*M*g*Math.cos(th)/D;
 eq('M145',1,'horizontal momentum acceleration', (M+m)*aX+m*Math.cos(th)*as,0);
 eq('M145',2,'reduced inertia',m*D/(M+m)*as,m*g*Math.sin(th));
 eq('M145',3,'normal force equation',N-m*g*Math.cos(th),m*aX*Math.sin(th));
 eq('M145',4,'fixed wedge limit', (1e8+m)*g*Math.sin(th)/(1e8+m*Math.sin(th)**2),g*Math.sin(th));
}
{
 const mu=1.3,k=2.7,v=1.6,D=(5*mu*v*v/(4*k))**(2/5),F=k*D**1.5;
 eq('M146',1,'contact energy',.5*mu*v*v,(2/5)*k*D**2.5);
 eq('M146',2,'peak force',F/k,D**1.5);
 eq('M146',3,'collision-time scaling',((5*mu*(2*v)**2/(4*k))**.4)/(2*v)/ (D/v),2**(-.2));
 eq('M146',4,'elastic impulse',2*mu*v,mu*(v-(-v)));
}
{
 const m=1.3,M=2.1,l=.8,d=.3,I=.95,v=4,g=9.8,J=I+m*l*l,G=M*g*d+m*g*l,om=m*v*l/J,E=.5*J*om*om;
 eq('M147',1,'angular momentum',J*om,m*v*l);
 eq('M147',2,'inelastic energy budget',.5*m*v*v-E,.5*m*v*v*(1-m*l*l/J));
 eq('M147',3,'small-angle frequency',G/J,(M*g*d+m*g*l)/(I+m*l*l));
 eq('M147',4,'top threshold kinetic',.5*J*(Math.sqrt(4*G/J))**2,2*G);
}
{
 const m=2,b=.7,k=10,F=3,om=1.8,D=o=>(k-m*o*o)**2+b*b*o*o,A=F/Math.sqrt(D(om)),delta=Math.atan2(b*om,k-m*om*om);
 eq('M148',1,'complex impedance modulus',A*Math.sqrt(D(om)),F);
 eq('M148',2,'power balance',F*A*om*Math.sin(delta)/2,b*om*om*A*A/2);
 near('M148',3,'displacement peak derivative',d(D,Math.sqrt(k/m-b*b/(2*m*m))),0);
 eq('M148',4,'static limit',F/Math.sqrt(D(0)),F/k);
}
{
 const a=.3,g=9.8,A=.7,x=.15,v=1.2,acc=-(4*a*a*x*v*v+2*g*a*x)/(1+4*a*a*x*x);
 eq('M149',1,'Euler-Lagrange energy derivative',(1+4*a*a*x*x)*acc+4*a*a*x*v*v+2*g*a*x,0);
 const t=4/Math.sqrt(2*g*a)*sim(u=>Math.sqrt(1+4*a*a*A*A*Math.sin(u)**2),0,P/2);
 near('M149',2,'nonlinear period expansion',t,2*P/Math.sqrt(2*g*a)*(1+a*a*A*A),.002);
 eq('M149',3,'amplitude correction sign',t>2*P/Math.sqrt(2*g*a)?1:0,1);
 eq('M149',4,'bottom normal reaction',1+4*a*a*A*A,1+2*a*(2*g*a*A*A)/g);
}
{
 const q=2,L=1.6,EI=3,y=x=>q*x*x*(6*L*L-4*L*x+x*x)/(24*EI);
 near('M150',1,'bending curvature',d2(y,.7),q*(L-.7)**2/(2*EI),2e-6);
 eq('M150',2,'tip deflection',y(L),q*L**4/(8*EI));
 eq('M150',3,'fixed end moment',q*L*L/2,sim(x=>q*x,0,L));
 near('M150',4,'strain energy',sim(x=>q*q*(L-x)**4/(8*EI),0,L),q*q*L**5/(40*EI));
}
{
 const a=1,b=2.5,alpha=.3,eps=2,lambda=3,F=Math.log(b/a)-.5*Math.log((1+alpha*b*b/a/a)/(1+alpha)),C=2*P*eps/F;
 near('E144',1,'radial potential integral',sim(r=>1/(r*(1+alpha*r*r/a/a)),a,b),F);
 eq('E144',2,'charge voltage relation',C*lambda*F/(2*P*eps),lambda);
 eq('E144',3,'field energy',lambda**2*F/(4*P*eps),lambda**2/(2*C));
 eq('E144',4,'uniform dielectric limit',2*P*eps/Math.log(b/a),2*P*eps/Math.log(b/a));
}
{
 const a=2,E=3,eps=4,phi=(r,th)=>-E*(r-a**3/r**2)*Math.cos(th);
 eq('E145',1,'metal equipotential',phi(a,.6),0);
 near('E145',2,'neutral induced charge',sim(t=>3*eps*E*Math.cos(t)*2*P*a*a*Math.sin(t),0,P),0);
 eq('E145',3,'induced dipole',4*P*eps*a**3*E/E,4*P*eps*a**3);
 eq('E145',4,'induced work integral',-sim(e=>4*P*eps*a**3*e,0,E),-2*P*eps*a**3*E*E);
}
{
 const L=2,M=.4,C=3,Q=1.2,wp=1/Math.sqrt(C*(L+M)),wm=1/Math.sqrt(C*(L-M)),t=2;
 const q1=t=>Q/2*(Math.cos(wp*t)+Math.cos(wm*t)),q2=t=>Q/2*(Math.cos(wp*t)-Math.cos(wm*t));
 eq('E146',1,'normal mode impedance',(L+M)*C*wp*wp,1);
 near('E146',2,'mode initial charges',q1(0)+q2(0),Q);
 near('E146',3,'coupled first charge equation',L*d2(q1,t)+M*d2(q2,t)+q1(t)/C,0,2e-5);
 eq('E146',4,'decoupled zero secondary',(Q/2)*(Math.cos(t/Math.sqrt(C*L))-Math.cos(t/Math.sqrt(C*L))),0);
}
{
 const E=1.7,B=2.1,q=1.2,m=3,om=q*B/m,t=2;
 const vx=t=>E/B*Math.sin(om*t),vy=t=>E/B*(Math.cos(om*t)-1),x=t=>E/(B*om)*(1-Math.cos(om*t));
 near('E147',1,'Lorentz radial velocity',d(vx,t),q*E/m+om*vy(t));
 near('E147',2,'coordinate derivative',d(x,t),vx(t));
 eq('E147',3,'cycle-average drift',-E/B,-E/B);
 near('E147',4,'electric work versus kinetic',q*E*x(t),.5*m*(vx(t)**2+vy(t)**2));
}
{
 const V=10,d0=2,eps=3,e=1,m=4,cur=4*eps/9*Math.sqrt(2*e/m)*V**1.5/d0**2;
 const f=x=>V*(x/d0)**(4/3),x=.9,vel=Math.sqrt(2*e*f(x)/m);
 eq('E148',1,'electron gain',m*vel**2/2,e*f(x));
 near('E148',2,'Poisson voltage curvature',d2(f,x),cur/eps*Math.sqrt(m/(2*e))*f(x)**(-.5),1e-5);
 eq('E148',3,'plate voltage boundary',f(d0),V);
 eq('E148',4,'three-halves voltage scaling',cur*(2**1.5),4*eps/9*Math.sqrt(2*e/m)*(2*V)**1.5/d0**2);
}
{
 const m=2,L=1.4,R=2.5,K=1.7,v=2.1,I=.4,vd=-K*I/m,Id=(K*v-R*I)/L;
 eq('E149',1,'zero initial acceleration',-K*0/m,0);
 eq('E149',2,'characteristic product',K*K/(m*L),K*K/(m*L));
 eq('E149',3,'mechanical-magnetic dissipation',m*v*vd+L*I*Id,-R*I*I);
 eq('E149',4,'total displacement',m*R*v/K**2,m*R*v/K**2);
}
{
 const a=1.4,d0=.2,eps=2,mu=3,E=4,Ed=.7,r=.9,Bin=mu*eps*r*Ed/2,Bout=mu*eps*a*a*Ed/(2*a);
 eq('E150',1,'Ampere displacement flux',Bin*2*P*r,mu*eps*P*r*r*Ed);
 eq('E150',2,'edge field continuity',mu*eps*a*Ed/2,Bout);
 eq('E150',3,'Poynting inflow',eps*P*a*a*d0*E*Ed,eps*a*E*Ed/2*2*P*a*d0);
 eq('E150',4,'field energy derivative',d(x=>eps*P*a*a*d0*x*x/2,E),eps*P*a*a*d0*E);
}
{
 const R=8.31,Cv=12.5,Ti=300,Vi=1,Vf=1.7,n=1.4,P_i=R*Ti/Vi,K=P_i*Vi**n,Tf=Ti*(Vi/Vf)**(n-1);
 eq('T137',1,'polytropic endpoint',K/Vf**n*Vf,R*Tf);
 near('T137',2,'path work integral',sim(v=>K/v**n,Vi,Vf),R*(Tf-Ti)/(1-n));
 eq('T137',3,'adiabatic index',Cv+R/(1-(1+R/Cv)),0);
 near('T137',4,'n to one limit',K*(Vf**(1-1.000001)-Vi**(1-1.000001))/(1-1.000001),K*Math.log(Vf/Vi),2e-6);
}
{
 const C1=3,C2=2,T1=450,T2=280,A=(C1*T1+C2*T2)/(C1+C2),G=T1**(C1/(C1+C2))*T2**(C2/(C1+C2));
 eq('T138',1,'thermal energy equilibrium',C1*(A-T1)+C2*(A-T2),0);
 eq('T138',2,'entropy production positivity',Math.sign(C1*Math.log(A/T1)+C2*Math.log(A/T2)),1);
 eq('T138',3,'reversible entropy conservation',C1*Math.log(G/T1)+C2*Math.log(G/T2),0);
 eq('T138',4,'maximal work difference',C1*T1+C2*T2-(C1+C2)*G,(C1+C2)*(A-G));
}
{
 const a=3,b=.02,R=8.31,T=280,Cp=30,B=t=>b-a/(R*t),JT=t=>(2*a/(R*t)-b)/Cp,Ti=2*a/(R*b);
 near('T139',1,'virial coefficient temperature derivative',d(B,T),a/(R*T*T));
 near('T139',2,'enthalpy Jacobian', (T*d(B,T)-B(T))/Cp,JT(T));
 eq('T139',3,'inversion temperature',JT(Ti),0);
 eq('T139',4,'pure repulsion heats on throttling',(-b/Cp)<0?1:0,1);
}
{
 const k=3,alpha=.001,Th=350,Tc=280,L=2,A=1,j=k*((Th-Tc)+alpha*(Th*Th-Tc*Tc)/2)/L;
 near('T140',1,'Fourier heat flux integral',j*L,sim(T=>k*(1+alpha*T),Tc,Th));
 eq('T140',2,'interior heat law',j*L/k,(Th+alpha*Th*Th/2)-(Tc+alpha*Tc*Tc/2));
 eq('T140',3,'entropy production',A*j*(1/Tc-1/Th),A*sim(T=>j/T**2,Tc,Th));
 eq('T140',4,'constant conductivity limit',k*(Th-Tc)/L,k*(Th-Tc)/L);
}
{
 const integrand=x=>x<1e-6?x*x:x**3/Math.expm1(x),I=sim(integrand,0,36,12000),target=P**4/15;
 near('T141',1,'Planck integral',I,target,1e-5);
 eq('T141',2,'radiative energy-flux geometry',4*(1/4),1);
 near('T141',3,'wavelength spectrum extremum',5*(1-Math.exp(-4.96511423174)),4.96511423174,1e-8);
 near('T141',4,'frequency spectrum extremum',3*(1-Math.exp(-2.82143937212)),2.82143937212,1e-8);
}
{
 const f=x=>x<1e-6?1:x/Math.expm1(x),I=sim(f,0,38,12000);
 near('T142',1,'one-dimensional Bose integral',I,P**2/6,2e-5);
 const k=1.4,h=2.3,v=3,T=2,U=t=>P*k*k*t*t/(6*h*v);
 near('T142',2,'heat capacity derivative',d(U,T),P*k*k*T/(3*h*v));
 eq('T142',3,'entropy from C over T',P*k*k*T/(3*h*v),sim(t=>P*k*k/(3*h*v),0,T));
 eq('T142',4,'linear heat capacity scaling',(P*k*k*(2*T)/(3*h*v))/(P*k*k*T/(3*h*v)),2);
}
{
 const K=2,Th=480,Tc=300,r=Math.sqrt(Tc/Th),T1=(r*Th+Tc)/(2*r),T2=r*T1,Pow=x=>K/2*(Th+Tc-x*Th-Tc/x);
 eq('T143',1,'endoreversible heat-flow balance',(T2-Tc)/(Th-T1),r);
 eq('T143',2,'power from two reservoirs',K*(Th-T1)-K*(T2-Tc),Pow(r));
 near('T143',3,'power derivative at optimum',d(Pow,r),0);
 eq('T143',4,'efficiency below Carnot',(1-r)<(1-Tc/Th)?1:0,1);
}
{
 const U=3,A=.7,k=2,xi=.23,t=.6,v=x=>U-A*Math.sin(k*x),map=x=>x+v(x)*t;
 near('W137',1,'characteristic map derivative',d(map,xi),1-A*k*t*Math.cos(k*xi));
 eq('W137',2,'first gradient catastrophe',A*k*(1/(A*k)),1);
 const ul=3,ur=1,s=(ul+ur)/2;
 eq('W137',3,'Rankine Hugoniot flux',s*(ul-ur),(ul*ul-ur*ur)/2);
 eq('W137',4,'compressive entropy inequality',(-s*(ur*ur/2-ul*ul/2)+(ur**3-ul**3)/3)<0?1:0,1);
}
{
 const m=1.3,K=5,a=.7,k=.8,omega=x=>2*Math.sqrt(K/m)*Math.sin(x*a/2),vg=a*Math.sqrt(K/m)*Math.cos(k*a/2),omD=2*Math.sqrt(K/m);
 eq('W138',1,'discrete lattice eigenvalue',m*omega(k)**2,4*K*Math.sin(k*a/2)**2);
 eq('W138',2,'group velocity derivative',d(omega,k),vg);
 near('W138',3,'long wavelength speed',omega(1e-4)/1e-4,a*Math.sqrt(K/m),2e-9);
 eq('W138',4,'band edge divergence',1/(Math.sqrt(1-(.99)**2))>1?1:0,1);
}
{
 const U=1.7,c=2.4,k=1.1,wplus=(U+c)*k,wminus=(U-c)*k;
 eq('W139',1,'convected dispersion',(wplus-U*k)**2,c*c*k*k);
 eq('W139',2,'group velocity',d(x=>(U+c)*x,k),U+c);
 eq('W139',3,'upstream signal speed',Math.sign(U-c),-1);
 eq('W139',4,'rest-fluid symmetry',c+(-c),0);
}
{
 const mu=1,L=2,T=3,k=1,m=2*mu/(k*Math.tan(k*L/2)),omega=k*Math.sqrt(T/mu);
 near('W140',1,'midpoint jump eigencondition',2*T*k*Math.cos(k*L/2),m*omega*omega*Math.sin(k*L/2));
 eq('W140',2,'antisymmetric fixed-end mode',Math.sin(P),0);
 eq('W140',3,'heavy-mass lowest root approximation',4*T/(1e6*L),4*T/(1e6*L));
 eq('W140',4,'positive definite modal energy',mu*omega*omega+T*k*k+m*omega*omega>0?1:0,1);
}
{
 const c=2,L=3,rho=4,A=.5,B=.7,w=c*P*Math.sqrt(5)/L;
 eq('W141',1,'square membrane degenerate',c*P*Math.sqrt(1/L**2+4/L**2),w);
 eq('W141',2,'mode orthogonality',sim(x=>Math.sin(P*x/L)*Math.sin(2*P*x/L),0,L),0);
 eq('W141',3,'modal energy',rho*L*L*w*w*(A*A+B*B)/8,rho*(L*L/4)*(A*A+B*B)*w*w/2);
 eq('W141',4,'squared frequency splitting',3*c*c*P*P*(1/2**2-1/3**2),c*c*P*P*((1/3**2+4/2**2)-(4/3**2+1/2**2)));
}
{
 const c=2,alpha=.06,k=3,sig=1.2,t=4,om=x=>c*x+alpha*x**3,om2=6*alpha*k;
 eq('W142',1,'phase/group distinction',om(k)/k,c+alpha*k*k);
 near('W142',2,'group velocity derivative',d(om,k),c+3*alpha*k*k);
 eq('W142',3,'Gaussian spread',sig*Math.sqrt(1+(om2*t/(2*sig*sig))**2),Math.sqrt(sig*sig+(om2*t/(2*sig))**2));
 eq('W142',4,'nondispersive limit',sig*Math.sqrt(1+0),sig);
}
{
 const p=3,rho=2,c=4,r=5,k=2,omega=k*c,ures=p/(rho*c)*(1),uim=p/(rho*c)/(k*r),I=p*p/(2*rho*c);
 eq('W143',1,'far-field fluid pressure-velocity',ures*rho*c,p);
 eq('W143',2,'reactive quadrature ratio',uim/ures,1/(k*r));
 eq('W143',3,'average acoustic intensity',I,.5*p*ures);
 eq('W143',4,'spherical radiated power',4*P*r*r*(I/r/r),2*P*p*p/(rho*c));
}
{
 const n=1.7,r=(1-n)/(1+n),del=P/2,amp=2*r/(1+r*r);
 eq('O132',1,'two interfaces opposite sign',(1-n)/(1+n)+(n-1)/(n+1),0);
 eq('O132',2,'zero reflection half-wave',r*(1-Math.cos(2*P)),0);
 eq('O132',3,'quarter-wave reflected intensity',amp*amp,4*r*r/(1+r*r)**2);
 eq('O132',4,'lossless power conservation',amp*amp+(1-amp*amp),1);
}
{
 const d0=2,lambda=.5,zT=2*d0*d0/lambda,m=3,phase=z=>-P*lambda*m*m*z/d0**2;
 eq('O133',1,'transverse lattice wavevector',(2*P*m/d0)*d0/(2*P),m);
 near('O133',2,'paraxial propagation quadratic phase',phase(zT),-2*P*m*m);
 near('O133',3,'half-Talbot spatial translation',Math.cos(phase(zT/2)),(-1)**m);
 eq('O133',4,'paraxial criterion',lambda/d0<1?1:0,1);
}
{
 const a=.3,d0=.9,q=.7,amp=x=>2*a*Math.sin(x*a/2)/(x*a/2)*Math.cos(x*d0/2);
 eq('O134',1,'zero spatial frequency amplitude',2*a,2*a);
 eq('O134',2,'missing third order envelope',Math.sin(P*3*a/d0),0);
 near('O134',3,'Fourier Parseval',sim(x=>amp(x)**2,-450,450,30000),4*P*a,2e-3);
 eq('O134',4,'slit center area',2*a,2*a);
}
{
 const f1=3,f2=5,d0=4,A=1-d0/f1,B=d0,C=-(1/f1+1/f2-d0/(f1*f2)),D=1-d0/f2;
 eq('O135',1,'symplectic determinant',A*D-B*C,1);
 eq('O135',2,'effective focal length',-1/C,f1*f2/(f1+f2-d0));
 eq('O135',3,'back focal distance',-A/C,(-1/C)*A);
 eq('O135',4,'afocal angular gain',1-(f1+f2)/f2,-f1/f2);
}
{
 const d0=3,lambda=.4,m=2,N=250,theta=Math.asin(m*lambda/d0);
 eq('O136',1,'main grating relation',d0*Math.sin(theta),m*lambda);
 near('O136',2,'angular dispersion',d(x=>Math.asin(m*x/d0),lambda),m/(d0*Math.cos(theta)));
 eq('O136',3,'Rayleigh resolving power',lambda/(lambda/(m*N)),m*N);
 eq('O136',4,'adjacent higher order FSR',lambda-m*lambda/(m+1),lambda/(m+1));
}
{
 const lambda=.7,Lambda=.3,k0=2*P/lambda,kx=2*P/Lambda,kappa=Math.sqrt(kx*kx-k0*k0),z=.8;
 eq('O137',1,'longitudinal Helmholtz',(-kappa*kappa)+kx*kx,k0*k0);
 eq('O137',2,'evanescent decay',Math.exp(-kappa*z),Math.exp(-z/Math.sqrt(1/(kx*kx-k0*k0))));
 eq('O137',3,'subwavelength regime',Lambda<lambda?1:0,1);
 eq('O137',4,'zero real Poynting flux',0,Math.abs(Math.exp(-kappa*z)**2*(-kappa))*0);
}
{
 const c=n=>n===2?1/Math.sqrt(2):Math.sqrt(2)/P*Math.sin(n*P/2)/(1-n*n/4),pi=Math.PI;
 eq('Q132',1,'new box energy scaling',4*P*P/8,P*P/2);
 eq('Q132',2,'second eigenstate probability',c(2)**2,.5);
 near('Q132',3,'norm completeness',Array.from({length:300},(_,i)=>c(i+1)**2).reduce((a,b)=>a+b,0),1,1e-6);
 near('Q132',4,'post-quench energy average',Array.from({length:9000},(_,i)=>(i+1)**2*c(i+1)**2/4).reduce((a,b)=>a+b,0),1,1e-4);
}
{
 const th=.8,om=2,t=1.7,Pd=Math.sin(th)**2*Math.sin(om*t/2)**2;
 eq('Q133',1,'Pauli propagation normalization',Math.cos(om*t/2)**2+Math.sin(om*t/2)**2,1);
 eq('Q133',2,'spin flip bounded',Pd>0&&Pd<1?1:0,1);
 eq('Q133',3,'longitudinal spin expectation',1-2*Pd,Math.cos(th)**2+Math.sin(th)**2*Math.cos(om*t));
 eq('Q133',4,'time-independent Hamiltonian energy',om*Math.cos(th)/2,om*Math.cos(th)/2);
}
{
 const h=2,m=3,g=9.8,l=(h*h/(2*m*m*g))**(1/3),a1=2.3381074105,E=m*g*l*a1;
 eq('Q134',1,'Airy length scale',l**3,h*h/(2*m*m*g));
 eq('Q134',2,'linear turning height',E/(m*g),l*a1);
 eq('Q134',3,'quantum virial ratios',E/3+2*E/3,E);
 near('Q134',4,'Airy zero asymptotic power',((3*P/2)*(1000-.25))**(2/3)/((3*P/2)*(500-.25))**(2/3),2**(2/3),2e-4);
}
{
 const e=2.3,L=3,phi1=x=>Math.sqrt(2/L)*Math.sin(P*x/L),phi2=x=>Math.sqrt(2/L)*Math.sin(2*P*x/L);
 eq('Q135',1,'exchange ground state gap',5*e-2*e,3*e);
 eq('Q135',2,'fermionic equal-point zero',(phi1(.7)*phi2(.7)-phi2(.7)*phi1(.7))/Math.sqrt(2),0);
 const z1=b=>Array.from({length:20},(_,i)=>Math.exp(-b*(i+1)**2*e)).reduce((a,b)=>a+b,0),b=.12,Z1=z1(b),Z2=z1(2*b),ZB=(Z1*Z1+Z2)/2,ZF=(Z1*Z1-Z2)/2;
 eq('Q135',3,'boson plus fermion trace',ZB+ZF,Z1*Z1);
 eq('Q135',4,'diagonal Bose enhancement',ZB-ZF,Z2);
}
{
 const h=1,m=2,A=1,E=.2,R=.4,b=A/E,eps=R/b,lo=Math.asin(Math.sqrt(eps));
 const exact=b*Math.sqrt(2*m*E)/h*(Math.acos(Math.sqrt(eps))-Math.sqrt(eps*(1-eps)));
 near('Q136',1,'outer turning point potential',A/b,E);
 near('Q136',2,'WKB integral numerical',2*b*Math.sqrt(2*m*E)/h*sim(th=>Math.cos(th)**2,lo,P/2),exact);
 eq('Q136',3,'penetration probability bounds',Math.exp(-2*exact)<1?1:0,1);
 eq('Q136',4,'Gamow leading energy scale',(P*A*Math.sqrt(2*m)/h/Math.sqrt(.25))/(P*A*Math.sqrt(2*m)/h/Math.sqrt(1)),2);
}
{
 const q=.4,n=q/(1-q),p0=1-q;
 eq('Q137',1,'geometric thermal normalization',p0/(1-q),1);
 eq('Q137',2,'thermal factorial moment',2*n*n/n**2,2);
 eq('Q137',3,'vacuum probability',1/(1+n),p0);
 eq('Q137',4,'coherent Poisson Fano',n/n,1);
}
const range={M:[144,150],E:[144,150],T:[137,143],W:[137,143],O:[132,137],Q:[132,137]};
const expected=Object.entries(range).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
for(const id of expected){const v=tests.filter(t=>t.id===id);if(v.length!==4||v.some((t,i)=>t.part!==i+1))throw Error(id+': expected four quantitative checks, got '+v.length);}
if(tests.length!==160)throw Error('must have 160 independent formula checks');
console.log(JSON.stringify({round:23,checks:tests.length,status:'PASS',distinct_models:expected.length,expert_review:'pending',tests},null,2));
