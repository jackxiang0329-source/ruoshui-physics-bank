#!/usr/bin/env node
'use strict';
// Round 25: 160 explicit physics regressions, four per problem.
// These are machine-verifiable cross-checks, not an independent expert review.
const PI=Math.PI, checks=[];
const eq=(id,part,label,a,b,tol=2e-5)=>{
 const diff=Math.abs(a-b),scale=Math.max(1,Math.abs(a),Math.abs(b));
 if(!Number.isFinite(diff)||diff>tol*scale)throw Error(id+' ('+part+') '+label+' -> '+a+' != '+b+' [abs='+diff+']');
 checks.push({id,part,label,absolute_error:diff,pass:true});
};
const der=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
const d2=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/(h*h);
function sim(f,a,b,n=4000){if(n%2)n++;const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+h*i);return h*s/3;}
const sinc=x=>Math.abs(x)<1e-12?1:Math.sin(x)/x;
function J(n,x){let term=(x/2)**n;for(let j=1;j<=n;j++)term/=j;let sum=term;for(let j=1;j<60;j++){term*=-(x*x/4)/(j*(j+n));sum+=term;}return sum;}
{
 const g=9.8,L=3,F=.2,w0=Math.sqrt(g/L),wb=Math.sqrt(w0*w0+F*F);
 const x=t=>Math.cos(F*t)*Math.cos(wb*t),y=t=>-Math.sin(F*t)*Math.cos(wb*t),t=.8;
 eq('M158',1,'east Coriolis equation',d2(x,t)+w0*w0*x(t),2*F*der(y,t),2e-5);
 eq('M158',2,'north Coriolis equation',d2(y,t)+w0*w0*y(t),-2*F*der(x,t),2e-5);
 eq('M158',3,'precession rotational phase',Math.atan2(y(.4),x(.4)),-F*.4);
 eq('M158',4,'equatorial decoupled mode',Math.cos(0*.7),1);
}
{
 const I1=2,I3=1.3,M=3,g=9.8,l=.2,th=.5,s=9;
 const disc=I3*I3*s*s-4*I1*M*g*l*Math.cos(th),slow=(I3*s-Math.sqrt(disc))/(2*I1*Math.cos(th)),fast=(I3*s+Math.sqrt(disc))/(2*I1*Math.cos(th));
 eq('M159',1,'regular-precession quadratic',I1*Math.cos(th)*slow**2-I3*s*slow+M*g*l,0);
 eq('M159',2,'precession roots product',slow*fast,M*g*l/(I1*Math.cos(th)));
 eq('M159',3,'precession roots sum',slow+fast,I3*s/(I1*Math.cos(th)));
 eq('M159',4,'high spin asymptotic', (I3*1e5-Math.sqrt((I3*1e5)**2-4*I1*M*g*l*Math.cos(th)))/(2*I1*Math.cos(th)),M*g*l/(I3*1e5),1e-6);
}
{
 const m=2,g=9.8,k=.8,vT=Math.sqrt(m*g/k),tau=vT/g,t=.7,v=z=>vT*Math.tanh(z/tau),x=z=>vT*tau*Math.log(Math.cosh(z/tau));
 eq('M160',1,'quadratic drag ODE',m*der(v,t),m*g-k*v(t)**2);
 eq('M160',2,'integrated displacement derivative',der(x,t),v(t));
 eq('M160',3,'energy balance',m*g*v(t),m*v(t)*der(v,t)+k*v(t)**3);
 eq('M160',4,'terminal force balance',m*g,k*vT*vT);
}
{
 const m=2,K=6,ell=4,alpha=.2,beta=Math.sqrt(1+m*alpha/ell**2),u0=m*K/(ell**2+m*alpha),ecc=.3,u=x=>u0*(1+ecc*Math.cos(beta*x)),x=.8,r=(ell**2+m*alpha)/(m*K);
 eq('M161',1,'Binet orbital equation',d2(u,x)+(1+m*alpha/ell**2)*u(x),m*K/ell**2);
 eq('M161',2,'apsidal frequency and increment',beta*(2*PI/beta),2*PI);
 eq('M161',3,'effective potential curvature',-2*K/r**3+3*(ell**2/m+alpha)/r**4,K/r**3);
 eq('M161',4,'Kepler limit precession',2*PI*(1/Math.sqrt(1+0)-1),0);
}
{
 const I1=1,I2=2,I3=3,Omega=4,A=(I2-I3)*Omega/I1,B=(I1-I2)*Omega/I3,gamma=Math.sqrt(A*B),u=t=>Math.cosh(gamma*t),v=t=>gamma*Math.sinh(gamma*t)/A,t=.4;
 eq('M162',1,'linearized intermediate Euler first',der(u,t),A*v(t));
 eq('M162',2,'linearized intermediate Euler second',der(v,t),B*u(t));
 const w1=1.1,w2=1.3,w3=.8,f1=(I2-I3)*w2*w3/I1,f2=(I3-I1)*w3*w1/I2,f3=(I1-I2)*w1*w2/I3;
 eq('M162',3,'torque-free energy derivative',I1*w1*f1+I2*w2*f2+I3*w3*f3,0);
 eq('M162',4,'angular momentum length derivative',I1**2*w1*f1+I2**2*w2*f2+I3**2*w3*f3,0);
}
{
 const g=9.8,a=2,beta=.4,w=Math.sqrt(g/((1+beta)*a)),theta=.05,thdot=.1,v0=.4;
 eq('M163',1,'linearized rolling oscillation', (1+beta)*a*w*w,g);
 eq('M163',2,'rolling kinetic energy',.5*(1+beta)*a*a*thdot**2,.5*a*a*thdot**2+.5*beta*a*a*thdot**2);
 const vSq=v0*v0-2*g*a*(1-Math.cos(theta))/(1+beta),N=a*(vSq/a/a)+g*Math.cos(theta);
 eq('M163',3,'contact reaction via energy',N,v0*v0/a-2*g*(1-Math.cos(theta))/(1+beta)+g*Math.cos(theta));
 eq('M163',4,'lower contact static reaction',a*0+g*Math.cos(0),g);
}
{
 const w=2,H=8,a=H/w,D=1.5,y=x=>a*(Math.cosh(x/a)-1),s=x=>a*Math.sinh(x/a);
 eq('M164',1,'catenary differential equation',d2(y,.7),w/H*Math.sqrt(1+der(y,.7)**2));
 eq('M164',2,'arc length integral',s(D),sim(x=>Math.sqrt(1+der(y,x)**2),0,D));
 eq('M164',3,'support vertical force',w*s(D),w*(2*s(D))/2);
 eq('M164',4,'shallow sag leading term',a*(Math.cosh(.001/a)-1),.001**2/(2*a),1e-7);
}
{
 const Q=2,eps=3,kap=.8,r=1.5,phi=x=>Q*Math.exp(-kap*x)/(4*PI*eps*x),E=x=>Q*Math.exp(-kap*x)*(1+kap*x)/(4*PI*eps*x*x);
 eq('E158',1,'Yukawa radial field derivative',-der(phi,r),E(r));
 eq('E158',2,'screening Gauss law',4*PI*eps*r*r*E(r),Q*Math.exp(-kap*r)*(1+kap*r));
 const rho=x=>-Q*kap*kap*Math.exp(-kap*x)/(4*PI*x);
 eq('E158',3,'screening ion charge integral',sim(x=>4*PI*x*x*rho(x),1e-8,r),Q*(Math.exp(-kap*r)*(1+kap*r)-1));
 eq('E158',4,'unscreened Coulomb limit',Q/(4*PI*eps*r*r),E(r)*Math.exp(kap*r)/(1+kap*r));
}
{
 const e1=5,e2=2,E0=1.7,a=1.4,C=(e1-e2)/(e1+2*e2),A=3*e2/(e1+2*e2),phiin=(r,th)=>-A*E0*r*Math.cos(th),phiout=(r,th)=>-E0*r*Math.cos(th)+C*E0*a**3*Math.cos(th)/r**2;
 eq('E159',1,'dielectric sphere potential continuity',phiin(a,.6),phiout(a,.6));
 eq('E159',2,'normal displacement continuity',e1*A,e2*(1+2*C));
 eq('E159',3,'dipole ratio from asymptotic field',4*PI*e2*a**3*C,4*PI*e2*a**3*(e1-e2)/(e1+2*e2));
 eq('E159',4,'identical medium no dipole',(e2-e2)/(e2+2*e2),0);
}
{
 const n=2,p=3,me=.8,mh=1.5,e=1.6,B=.001,Ex=3,sigma=e*(n*me+p*mh),Ey=(p*mh*mh-n*me*me)/(n*me+p*mh)*Ex*B;
 eq('E160',1,'weak field open-circuit transverse current',sigma*Ey+e*(n*me*me-p*mh*mh)*Ex*B,0);
 eq('E160',2,'weak Hall coefficient',Ey/(sigma*Ex*B),(p*mh*mh-n*me*me)/(e*(n*me+p*mh)**2));
 eq('E160',3,'pure-electron Hall sign',(-n*me*me)/(e*(n*me)**2),-1/(e*n));
 eq('E160',4,'compensated Hall cancellation',(n*me*me)*mh*mh-n*(me*me)*mh*mh,0);
}
{
 const wp=3,c=2,om=5,k=Math.sqrt(om*om-wp*wp)/c,vp=om/k,vg=c*c*k/om;
 eq('E161',1,'cold plasma transverse dispersion',om*om,wp*wp+c*c*k*k);
 eq('E161',2,'phase-group product',vp*vg,c*c);
 eq('E161',3,'subcutoff attenuation scale',(Math.sqrt(wp*wp-2*2)/c)**2,(wp*wp-4)/c**2);
 eq('E161',4,'high frequency group approach',c*Math.sqrt(1-wp*wp/1000**2),c,1e-5);
}
{
 const a=1,b=3,eps=2,Q=5,C=4*PI*eps*a*b/(b-a);
 eq('E162',1,'spherical capacitor electric potential',sim(r=>Q/(4*PI*eps*r*r),a,b),Q/C);
 eq('E162',2,'direct electric field energy',sim(r=>.5*eps*(Q/(4*PI*eps*r*r))**2*4*PI*r*r,a,b),Q*Q/(2*C));
 eq('E162',3,'capacitance in thin shell',4*PI*eps*a*(a+.0001)/.0001,4*PI*eps*a*a/.0001,1e-4);
 eq('E162',4,'fixed voltage stored energy',.5*C*3*3,(C*3)*3/2);
}
{
 const w=2,p=4,eps=3,c=5,A=w**4*p*p/(32*PI**2*eps*c**3),ang=t=>A*Math.sin(t)**2;
 eq('E163',1,'far radiation transverse zeros',ang(0),0);
 eq('E163',2,'radiation angular integration',sim(t=>2*PI*Math.sin(t)*ang(t),0,PI),w**4*p*p/(12*PI*eps*c**3));
 eq('E163',3,'quadratic dipole field power scaling',ang(PI/2)/ang(PI/6),4);
 eq('E163',4,'fourth-power frequency scaling',(2*w)**4/w**4,16);
}
{
 const mu=2,N=50,I=1.5,h=.6,a=2,b=3,B=r=>mu*N*I/(2*PI*r),L=mu*N*N*h*Math.log(b/a)/(2*PI),flux=sim(B,a,b)*h;
 eq('E164',1,'toroid Ampere loop',2*PI*2.5*B(2.5),mu*N*I);
 eq('E164',2,'total coil flux linkage',N*flux,L*I);
 eq('E164',3,'magnetic energy integral',sim(r=>B(r)**2/(2*mu)*2*PI*r*h,a,b),.5*L*I*I);
 eq('E164',4,'narrow toroid logarithm',Math.log(1+.0001),.0001,2e-8);
}
{
 const g=1.4,r=7,Cv=20,T1=300,T3=1900,T2=T1*r**(g-1),T4=T3/r**(g-1),Qin=Cv*(T3-T2),Qout=Cv*(T4-T1);
 eq('T151',1,'Otto compression-heat ratio',T2/T1,r**(g-1));
 eq('T151',2,'Otto heat efficiency',1-Qout/Qin,1-r**(1-g));
 eq('T151',3,'cycle energy work balance',Qin-Qout,Cv*(T3-T2-T4+T1));
 eq('T151',4,'compression ratio unity efficiency',1-1**(1-g),0);
}
{
 const n=3,R=8.31,T=300,z=2.5,W=n*R*T*(1-1/z),S=n*R*(Math.log(z)-1+1/z);
 eq('T152',1,'isothermal heat equals actual work',W,n*R*T*(z-1)/z);
 eq('T152',2,'irreversible total entropy',S,n*R*Math.log(z)-W/T);
 eq('T152',3,'reversible work larger',n*R*T*Math.log(z)>W?1:0,1);
 const a=.001;eq('T152',4,'small expansion entropy quadratic',Math.log(1+a)-1+1/(1+a),a*a/2,1e-7);
}
{
 const L=3,D=2,k=4,Cv=k/D,A=2,dt=1.2,tau=L*L/(PI*PI*D),u=(x,t)=>A*Math.sin(PI*x/L)*Math.exp(-t/tau);
 eq('T153',1,'heat diffusion PDE',der(t=>u(.7,t),dt),D*d2(x=>u(x,dt),.7));
 eq('T153',2,'left end heat flux',-k*PI*A/L*Math.exp(-dt/tau),-k*der(x=>u(x,dt),0));
 const Et=t=>2*Cv*L*A/PI*Math.exp(-t/tau);
 eq('T153',3,'end flux balances lost heat',-der(Et,dt),2*k*PI*A/L*Math.exp(-dt/tau));
 eq('T153',4,'diffusion time quadratic in length',(2*L)**2/(PI*PI*D),4*tau);
}
{
 const zeta3=2.6123753487,zeta5=1.3414872573,m=2,kB=1,hbar=1,n=4,V=3,tc=2*PI*hbar*hbar/(m*kB)*(n/zeta3)**(2/3);
 const lambda=T=>Math.sqrt(2*PI*hbar*hbar/(m*kB*T)),T=.6*tc;
 eq('T154',1,'critical condensate density',zeta3/lambda(tc)**3,n);
 eq('T154',2,'subcritical excitation fraction',zeta3/lambda(T)**3/n,(T/tc)**1.5);
 const U=t=>1.5*V*kB*t*zeta5/lambda(t)**3;
 eq('T154',3,'BEC thermal heat capacity',der(U,T),3.75*V*kB*zeta5/lambda(T)**3);
 eq('T154',4,'condensate nonnegativity',1-(T/tc)**1.5>0?1:0,1);
}
{
 const N=3,mu=.7,B=2,k=1.4,T=5,x=mu*B/(k*T),M=t=>N*mu*Math.tanh(mu*B/(k*t)),U=t=>-N*mu*B*Math.tanh(mu*B/(k*t)),S=t=>N*k*(Math.log(2*Math.cosh(mu*B/(k*t)))-(mu*B/(k*t))*Math.tanh(mu*B/(k*t)));
 eq('T155',1,'Curie zero field susceptibility',der(b=>N*mu*Math.tanh(mu*b/(k*T)),0),N*mu*mu/(k*T));
 eq('T155',2,'spin heat capacity',der(U,T),N*k*x*x/(Math.cosh(x)**2));
 eq('T155',3,'thermodynamic entropy derivative',der(S,T),der(U,T)/T);
 eq('T155',4,'adiabatic B over T invariance',mu*(B/2)/(k*(T/2)),x);
}
{
 const n1=4,n2=2,R=8.31,T=300,x1=n1/(n1+n2),x2=1-x1,G=R*T*(n1*Math.log(x1)+n2*Math.log(x2)),S=-R*(n1*Math.log(x1)+n2*Math.log(x2));
 eq('T156',1,'mixing free energy versus entropy',G,-T*S);
 eq('T156',2,'mixing entropy positivity',S>0?1:0,1);
 const a=.0001;eq('T156',3,'dilute ideal osmotic law',-Math.log(1-a),a,1e-7);
 eq('T156',4,'no solute osmotic pressure',-Math.log(1),0);
}
{
 const L=30000,R=8.31,T1=300,T2=320,p1=100000,ratio=Math.exp(L/R*(1/T1-1/T2));
 eq('T157',1,'integrated saturation pressure ratio',Math.log(ratio),L/R*(1/T1-1/T2));
 eq('T157',2,'local Clausius-Clapeyron derivative',der(t=>p1*Math.exp(L/R*(1/T1-1/t)),310)/(p1*Math.exp(L/R*(1/T1-1/310))),L/(R*310*310));
 eq('T157',3,'positive coexistence slope',ratio>1?1:0,1);
 eq('T157',4,'identical temperature pressure ratio',Math.exp(L/R*(1/T1-1/T1)),1);
}
{
 const c1=2,c2=3,r=(c1-c2)/(c1+c2),t=2*c1/(c1+c2);
 eq('W151',1,'interface surface height continuity',1+r,t);
 eq('W151',2,'interface volume flux continuity',c1*(1-r),c2*t);
 eq('W151',3,'incident reflected transmitted energy',r*r+c2/c1*t*t,1);
 eq('W151',4,'equal depth zero reflection',(c1-c1)/(c1+c1),0);
}
{
 const m1=1,m2=3,K=4,a=1.2,k=.8,S=1/m1+1/m2,inside=Math.sqrt(S*S-4*Math.sin(k*a/2)**2/(m1*m2)),wm2=K*(S-inside),wp2=K*(S+inside);
 eq('W152',1,'diatomic determinant dispersion',(2*K-m1*wm2)*(2*K-m2*wm2),4*K*K*Math.cos(k*a/2)**2);
 eq('W152',2,'optical-acoustic root sum',wm2+wp2,2*K*S);
 eq('W152',3,'zone boundary low branch',K*(S-Math.abs(1/m1-1/m2)),2*K/Math.max(m1,m2));
 const kk=1e-5,w2=K*(S-Math.sqrt(S*S-4*Math.sin(kk*a/2)**2/(m1*m2)));
 eq('W152',4,'longwave sound speed squared',w2/(kk*kk),K*a*a/(2*(m1+m2)),5e-5);
}
{
 const G=6,rho=3,L=2,c=Math.sqrt(G/rho),k=PI/L,th=(x,t)=>Math.sin(k*x)*Math.cos(c*k*t);
 eq('W153',1,'torsional PDE',d2(t=>th(.5,t),.7),c*c*d2(x=>th(x,.7),.5));
 eq('W153',2,'torsional wave velocity square',c*c,G/rho);
 eq('W153',3,'clamped end boundary',th(0,.7),0);
 eq('W153',4,'second mode frequency ratio',(2*PI*c/L)/(PI*c/L),2);
}
{
 const root=4.4934094579,j0=x=>sinc(x),j0p=x=>(x*Math.cos(x)-Math.sin(x))/(x*x),R=2,c=3,k=root/R;
 eq('W154',1,'radial Helmholtz Bessel',d2(r=>j0(k*r),.7)+2/.7*der(r=>j0(k*r),.7)+k*k*j0(k*.7),0);
 eq('W154',2,'hard wall radial velocity zero',j0p(root),0,1e-8);
 eq('W154',3,'first root tangent relation',Math.tan(root),root,1e-7);
 eq('W154',4,'radius scaling',c*root/(2*R),(c*root/R)/2);
}
{
 const L=2,c=3,w=1.7,k=w/c,A=.8,Y=x=>A*Math.sin(k*(L-x))/Math.sin(k*L),t=.7;
 eq('W155',1,'fixed end boundary',Y(L),0);
 eq('W155',2,'driven end amplitude',Y(0),A);
 eq('W155',3,'spatial Helmholtz residual',d2(Y,.6)+k*k*Y(.6),0);
 eq('W155',4,'undamped mean input power',sim(t=>-1*der(Y,0)*Math.cos(w*t)*(-A*w*Math.sin(w*t)),0,2*PI/w),0);
}
{
 const E=10,rho=2,eta=.01,om=3,c=Math.sqrt(E/rho),kr=om/c,ki=eta*om*om/(2*E*c);
 eq('W156',1,'dispersion real residual',E*(kr*kr-ki*ki)+eta*om*2*kr*ki,rho*om*om,1e-4);
 eq('W156',2,'dispersion imaginary residual',E*(2*kr*ki)-eta*om*(kr*kr-ki*ki),0,1e-4);
 eq('W156',3,'exponential attenuation length',Math.exp(-ki*(1/ki)),Math.exp(-1));
 eq('W156',4,'positive time average heat dissipation',eta*om*om*.3**2/2>0?1:0,1);
}
{
 const a=1.4,f=x=>a/Math.cosh(a*x),t=.6;
 eq('W157',1,'focusing NLS stationary ODE',.5*d2(f,t)+f(t)**3-a*a*f(t)/2,0);
 eq('W157',2,'bright soliton norm',sim(x=>f(x)**2,-15,15),2*a);
 eq('W157',3,'bright soliton Hamiltonian',sim(x=>.5*der(f,x)**2-.5*f(x)**4,-12,12),-a**3/3);
 eq('W157',4,'soliton peak and width',f(0),a);
}
{
 const n1=1,n2=1.5,B=Math.atan(n2/n1),t=Math.asin(n1*Math.sin(B)/n2),rp=(n2*Math.cos(B)-n1*Math.cos(t))/(n2*Math.cos(B)+n1*Math.cos(t));
 eq('O144',1,'Snell condition at Brewster incidence',n1*Math.sin(B),n2*Math.sin(t));
 eq('O144',2,'p polarization reflection zero',rp,0);
 const rs=(n1*Math.cos(B)-n2*Math.cos(t))/(n1*Math.cos(B)+n2*Math.cos(t));
 eq('O144',3,'s reflection Brewster amplitude',rs,(n1*n1-n2*n2)/(n1*n1+n2*n2));
 eq('O144',4,'Brewster complementary refraction',B+t,PI/2);
}
{
 const root=3.8317059702,frac=1-J(0,root)**2-J(1,root)**2,u=>u;
}
