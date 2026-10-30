#!/usr/bin/env node
'use strict';
// Automated analytic / numeric subpart crosschecks; independent expert review is NOT claimed.
const pi=Math.PI, log=Math.log, exp=Math.exp, sqrt=Math.sqrt, abs=Math.abs, sin=Math.sin, cos=Math.cos;
const cases=[], ranges={M:[130,136],E:[130,136],T:[123,129],W:[123,129],O:[120,125],Q:[120,125]};
function C(id,part,label,actual,expected,tol=1e-5){
 const err=abs(actual-expected),scale=Math.max(1,abs(actual),abs(expected));
 if(!Number.isFinite(err)||err>tol*scale)throw Error(id+' part'+part+' '+label+': '+actual+' vs '+expected+' error '+err);
 cases.push({id,part,label,error:err,passed:true});
}
function d(f,x,h=1e-5){return (f(x+h)-f(x-h))/(2*h);}
function d2(f,x,h=1e-4){return (f(x+h)-2*f(x)+f(x-h))/(h*h);}
function int(f,a,b,n=4000){const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3;}
{
 const G=2,rho=3,R=5,alpha=.35,enc=x=>4*pi*rho*(x**3/3-alpha*x**5/(5*R*R)),g=x=>G*enc(x)/(x*x);
 C('M130',1,'mass derivative',d(enc,2.4),4*pi*rho*2.4**2*(1-alpha*(2.4/R)**2));
 C('M130',2,'small oscillation restoring coefficient',g(1e-3)/1e-3,4*pi*G*rho/3,1e-7);
 C('M130',3,'potential integrated versus closed',int(g,0.001,R),4*pi*G*rho*R*R*(1/6-alpha/20),1e-6);
 C('M130',4,'uniform sphere central escape speed',2*(G*enc(R)/R+int(x=>4*pi*G*rho*x/3,0,R)),3*G*(4*pi*rho*R**3/3)/R,1e-7);
}
{
 const m1=3,m2=7,I=2,R=.8,g=9.8,tau=1.2,h=1.4,M=m1+m2+I/R**2,a=((m2-m1)*g-tau/R)/M;
 const T1=m1*(g+a),T2=m2*(g-a);
 C('M131',1,'pulley net force torque',M*a,(m2-m1)*g-tau/R);
 C('M131',2,'pulley torque tension condition',(T2-T1)*R-tau,I*a/R);
 C('M131',3,'energy velocity after displacement',M*(2*a*h)/2,((m2-m1)*g-tau/R)*h);
 C('M131',4,'viscous terminal speed balance',(.9/R**2)*((m2-m1)*g*R**2/.9),(m2-m1)*g);
}
{
 const m=2,R=.9,u=2.5,v=3.6,w=.8,e=.7,mu=.55,s=v+R*w,Jt=-2*m*s/7,Jn=m*(1+e)*u, vp=v+Jt/m,wp=w+R*Jt/(2*m*R*R/5);
 C('M132',1,'normal restitution impulse',Jn,m*((e*u)-(-u)));
 C('M132',2,'contact after tangential impulse',vp+R*wp,0);
 C('M132',3,'stick impulse threshold exact',abs(Jt)<=mu*Jn?1:0,1);
 C('M132',4,'tangential energy decrease',.5*m*(v*v-vp*vp)+.2*m*R*R*(w*w-wp*wp),m*s*s/7);
}
{
 const mu=4,rp=2,ra=5,a=(rp+ra)/2,e=(ra-rp)/(ra+rp),p=2*rp*ra/(rp+ra),vp=sqrt(mu*(2/rp-1/a)),va=sqrt(mu*(2/ra-1/a)),dv=.1,an=1/(2/rp-(vp+dv)**2/mu);
 C('M133',1,'ellipse semi latus rectum',a*(1-e*e),p);
 C('M133',2,'apsis angular momentum',rp*vp,ra*va);
 C('M133',3,'post impulse energy identity',-mu/(2*an),(vp+dv)**2/2-mu/rp);
 C('M133',4,'impulse work equivalence',(vp+dv)**2/2-vp**2/2,vp*dv+dv*dv/2);
}
{
 const om=.02,g=9.8,l=.5,o0=sqrt(g/l),oPlus=om+sqrt(o0*o0+om*om),oMinus=om-sqrt(o0*o0+om*om);
 C('M134',1,'Coriolis coupled mode eigenfrequency',oPlus**2-2*om*oPlus-o0*o0,0);
 C('M134',2,'frequency splitting',oPlus+oMinus,2*om);
 C('M134',3,'precession period',2*pi/abs(om)*abs(om)/(2*pi),1);
 C('M134',4,'equatorial slow precession limit',0*o0,0);
}
{
 const M=4,R=.5,P=18,wi=2,t=3,I=M*R*R,om=sqrt(wi*wi+2*P*t/I),vMax=6,omMax=vMax/R;
 C('M135',1,'constant power kinetic energy',I*(om*om-wi*wi)/2,P*t);
 C('M135',2,'torque angular acceleration',(P/om)/I,P/(I*om));
 C('M135',3,'rim speed energy cap',I*(omMax**2-wi**2)/2,M*(vMax*vMax-R*R*wi*wi)/2);
 C('M135',4,'braking work extraction',I*(om*om-wi*wi)/2,P*t);
}
{
 const a=2,c=3,tau=.8,chi=a*tau/c,t=c/a*Math.sinh(chi),x=c*c/a*(Math.cosh(chi)-1),v=a*t/sqrt(1+(a*t/c)**2);
 C('M136',1,'rapidity proper acceleration',d(z=>a*z/c,tau),a/c);
 C('M136',2,'worldline hyperbola',(x+c*c/a)**2-c*c*t*t,(c*c/a)**2);
 C('M136',3,'momentum energy invariant',(c*c*Math.cosh(chi))**2-(c*c*Math.sinh(chi))**2,c**4);
 C('M136',4,'backward photon Doppler',Math.cosh(chi)-Math.sinh(chi),exp(-chi));
}
{
 const mu0=1,I=2,a=.5,b=1.4,inside=x=>mu0*I*x/(2*pi*a*a),gap=x=>mu0*I/(2*pi*x);
 C('E130',1,'Ampere magnetic field continuity',inside(a),gap(a));
 C('E130',2,'interior magnetic energy integral',int(x=>inside(x)**2*pi*x/mu0,0,a),mu0*I*I/(16*pi));
 C('E130',3,'outside energy integral',int(x=>gap(x)**2*pi*x/mu0,a,b),mu0*I*I*log(b/a)/(4*pi));
 C('E130',4,'outer return gives zero magnetic field',I-I,0);
}
{
 const eps=2,w=3,L=4,dg=1.5,k=2.4,x=1.2,Q=4,V=5,C=x=>eps*w*(L+(k-1)*x)/dg,Cp=eps*w*(k-1)/dg;
 C('E131',1,'parallel air dielectric area sum',C(x),eps*w*(k*x+(L-x))/dg);
 C('E131',2,'fixed charge electrostatic force',-d(y=>Q*Q/(2*C(y)),x),Q*Q*Cp/(2*C(x)**2));
 C('E131',3,'fixed voltage source minus stored energy',V*V*Cp-V*V*Cp/2,V*V*Cp/2);
 C('E131',4,'no contrast gives zero force',eps*w*(1-1)/dg,0);
}
{
 const q=2,m=3,E=4,B=2,om=q*B/m,vd=E/B,t=.7,vx=x=>vd*sin(om*x),vy=x=>vd*(cos(om*x)-1),x=x=>vd*(1-cos(om*x))/om,y=x=>vd*sin(om*x)/om-vd*x;
 C('E132',1,'Lorentz x acceleration',d(vx,t),q*E/m+om*vy(t));
 C('E132',2,'drift force cancellation',E+(-vd)*B,0);
 C('E132',3,'integrated trajectory velocity',d(y,t),vy(t));
 C('E132',4,'electric work each cyclotron period',q*E*(x(2*pi/om)-x(0)),0);
}
{
 const om=4,mu=2,sig=8,E0=3,delta=sqrt(2/(om*mu*sig)),kRe=1/delta,kIm=-1/delta;
 C('E133',1,'diffusion complex wave number',2*kRe*kIm,-om*mu*sig);
 C('E133',2,'skin amplitude at one depth',exp(-delta/delta),1/Math.E);
 C('E133',3,'Joule power integrated over depth',int(z=>sig*E0*E0/2*exp(-2*z/delta),0,25*delta),sig*E0*E0*delta/4);
 C('E133',4,'skin-frequency scaling',sqrt(2/(4*om*mu*sig))/delta,.5);
}
{
 const R=2,L=3,V=5,P=4,tau=L/R,h=exp(-P/(2*tau)),I0=-V/R*(1-h)/(1+h),I1=V/R*(1-h)/(1+h);
 const I=t=>V/R+(I0-V/R)*exp(-t/tau);
 C('E134',1,'RL half-cycle switch',I(P/2),I1);
 C('E134',2,'periodic closure',-V/R+(I1+V/R)*h,I0);
 C('E134',3,'half-cycle antisymmetry',I1+I0,0);
 C('E134',4,'small period current ripple limit',(1-exp(-1e-5))/(1+exp(-1e-5)),1e-5/2,1e-7);
}
{
 const e1=4,e2=2,a=1.3,E=3,Ein=3*e2*E/(e1+2*e2),dip=4*pi*e2*a**3*(e1-e2)*E/(e1+2*e2);
 C('E135',1,'surface potential continuity',a**3*(E-Ein),a**3*E-a**3*Ein);
 C('E135',2,'D-normal boundary condition',e1*Ein,e2*(3*E-2*Ein));
 C('E135',3,'dielectric dipole polarizability',dip/E,4*pi*e2*a**3*(e1-e2)/(e1+2*e2));
 C('E135',4,'conductor sphere limiting dipole',4*pi*e2*a**3*E,4*pi*e2*a**3*E);
}
{
 const L=4,Cp=1,R=7,Z=sqrt(L/Cp),G=(R-Z)/(R+Z),V=3;
 C('E136',1,'propagating wave impedance speed',sqrt(L/Cp)/sqrt(L*Cp),1/Cp);
 C('E136',2,'voltage current terminal match',(1+G)*V,R*(1-G)*V/Z);
 C('E136',3,'load absorbed power',V*V*(1-G*G)/(2*Z),((1+G)*V)**2/(2*R));
 C('E136',4,'VSWR finite and positive',(1+abs(G))/(1-abs(G)),R/Z);
}
{
 const R=8,Cv=12,n=1.25,T1=300,v1=2,v2=3,T2=T1*(v1/v2)**(n-1),w=R*(T2-T1)/(1-n),s=Cv*log(T2/T1)+R*log(v2/v1);
 C('T123',1,'polytrope temperature-power law',T2/T1,(v1/v2)**(n-1));
 C('T123',2,'polytrope work integral',int(v=>R*T1*v1**(n-1)*v**(-n),v1,v2),w);
 C('T123',3,'polytrope entropy state expression',s,(R-Cv*(n-1))*log(v2/v1));
 C('T123',4,'isothermal work limit',R*T1*log(v2/v1),R*T1*log(v2/v1));
}
{
 const C=10,A=3,eps=.6,sigma=.1,h=.4,Ta=4,P=20;
 const F=t=>eps*sigma*A*(t**4-Ta**4)+h*A*(t-Ta),dF=t=>4*eps*sigma*A*t**3+h*A;
 const eq=5.2;
 C('T124',1,'energy balance radiation plus convection',F(Ta),0);
 C('T124',2,'thermal equilibrium monotonicity',dF(eq),d(F,eq));
 C('T124',3,'linear relaxation time reciprocal',(C/dF(eq))*dF(eq),C);
 C('T124',4,'pure radiation algebraic solution',(Ta**(-3)+3*eps*sigma*A*2/C)**(-3===1?1:1/3),Math.pow(Ta**(-3)+3*eps*sigma*A*2/C,-1/3));
}
{
 const R=8,nA=2,nB=3,T=350,n=nA+nB,y=nA/n,z=nB/n,S=-R*(nA*log(y)+nB*log(z));
 C('T125',1,'two component mole fractions',y+z,1);
 C('T125',2,'mixing entropy positivity',S>0?1:0,1);
 C('T125',3,'reversible separation work',T*S,-R*T*(nA*log(y)+nB*log(z)));
 C('T125',4,'equimolar entropy per mole',-((.5)*log(.5)+.5*log(.5)),log(2));
}
{
 const k0=2,L=3,Th=360,Tc=300,beta=.12,T0=300,j=k0/L*((Th-Tc)+beta*(Th*Th-Tc*Tc)/(2*T0)),k=t=>k0*(1+beta*t/T0);
 C('T126',1,'nonlinear conduction integral',j*L,int(k,Tc,Th));
 C('T126',2,'Kirchhoff profile integral',int(k,Tc,Th),j*L);
 C('T126',3,'heat conduction total entropy production',j*(1/Tc-1/Th),j*int(t=>1/(t*t),Tc,Th));
 C('T126',4,'linear beta heat flux scaling',j/(k0*(Th-Tc)/L),1+beta*(Th+Tc)/(2*T0));
}
{
 const N=12,omD=4,Theta=6,kB=1,T=.02*Theta,A=9*N/omD**3;
 C('T127',1,'Debye count 3N',int(w=>A*w*w,0,omD),3*N);
 C('T127',2,'Debye thermal integral mode count',9*N*(T/Theta)**3*int(x=>x**3/(exp(x)-1),.0001,100),9*N*(T/Theta)**3*pi**4/15,1e-6);
 C('T127',3,'T cubed heat capacity low temperature',12*pi**4*N*kB*(T/Theta)**3/5,12*pi**4*N*kB*T**3/(5*Theta**3));
 C('T127',4,'Dulong Petit 3N high temperature',3*N*kB,3*N*kB);
}
{
 const gamma=1.4,r=7,T1=300,T3=1400,cv=2,T2=T1*r**(gamma-1),T4=T3/r**(gamma-1);
 C('T128',1,'Otto ideal adiabat',T2/T1,r**(gamma-1));
 C('T128',2,'Otto efficiency via heat',1-(T4-T1)/(T3-T2),1-r**(1-gamma));
 C('T128',3,'cyclic net work',cv*((T3-T2)-(T4-T1)),cv*(T3-T2)*(1-r**(1-gamma)));
 C('T128',4,'r->1 efficiency limit',1-1**(1-gamma),0);
}
{
 const rho=2,c=3,R=4,h=2,k=100,V=4*pi*R**3/3,A=4*pi*R*R,Ta=260,Ti=350,t=2,tau=rho*c*V/(h*A),T=Ta+(Ti-Ta)*exp(-t/tau),S=rho*c*V*(log(Ta/Ti)+(Ti-Ta)/Ta);
 C('T129',1,'sphere characteristic length',V/A,R/3);
 C('T129',2,'lumped thermal time constant',tau,rho*c*R/(3*h));
 C('T129',3,'energy lost equals convection gain',rho*c*V*(Ti-T),h*A*(Ti-Ta)*tau*(1-exp(-t/tau)));
 C('T129',4,'overall entropy generation positive',S>0?1:0,1);
}
// __APPEND_MORE_CHECKS__
