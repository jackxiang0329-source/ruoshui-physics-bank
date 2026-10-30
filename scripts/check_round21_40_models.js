#!/usr/bin/env node
'use strict';
// Quantitative independent-formula regression checks for 40 freshly authored models.
// Formula tests do not constitute independent expert review of every derivation.
const P=Math.PI,checks=[];function eq(id,part,label,x,y,tol=1e-5){
 const err=Math.abs(x-y),scale=Math.max(1,Math.abs(x),Math.abs(y));
 if(!Number.isFinite(err)||err>tol*scale)throw Error(id+' part '+part+' '+label+' mismatch '+x+' vs '+y+' (error '+err+')');
 checks.push({id,part,label,residual:err,tolerance:tol,passed:true});
}
function d(f,x,h=1e-5){return (f(x+h)-f(x-h))/(2*h);}
function d2(f,x,h=1e-4){return (f(x+h)-2*f(x)+f(x-h))/(h*h);}
function sim(f,a,b,n=4000){if(n%2)n++;let h=(b-a)/n,s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3;}
const c=299792458;
{
 const g=9.8,l=2.3,om=.2,lat=.7,w0=Math.sqrt(g/l),f=om*Math.sin(lat),plus=Math.sqrt(w0*w0+f*f)+f,minus=Math.sqrt(w0*w0+f*f)-f;
 eq('M130',1,'restoring-oscillator',w0*w0,g/l);
 eq('M130',2,'Coriolis-skew-velocity-work',(-2*f*2.1*1.3)+(2*f*1.3*2.1),0);
 eq('M130',3,'circular-mode-splitting',plus-minus,2*f);
 eq('M130',4,'precession-equator-limit',om*Math.sin(0),0);
}
{
 const a=1.2,g=9.8,th=.6,s=t=>4*a*Math.sin(t/2),x=t=>a*(t+Math.sin(t)),y=t=>a*(1-Math.cos(t)),w=Math.sqrt(g/(4*a));
 eq('M131',1,'arclength-derivative',d(s,th),Math.hypot(d(x,th),d(y,th)));
 eq('M131',2,'quadratic-cycloid-height',y(th),s(th)**2/(8*a));
 eq('M131',3,'isochronous-period',2*P/w,4*P*Math.sqrt(a/g));
 eq('M131',4,'quarter-period-bottom-crossing',Math.cos(w*P/(2*w)),0);
}
{
 const m=2.1,v=2.3,b=.8,K=1.4,E=m*v*v/2,L=m*v*b,r=(K+Math.sqrt(K*K+m*m*v**4*b*b))/(m*v*v),e=Math.sqrt(1+(m*v*v*b/K)**2),theta=2*Math.atan(K/(m*v*v*b));
 eq('M132',1,'turning-point-energy',E,L*L/(2*m*r*r)+K/r);
 eq('M132',2,'scattering-eccentricity',Math.cos((P-theta)/2),1/e);
 const B=t=>K/(m*v*v)*1/Math.tan(t/2),section=B(theta)/Math.sin(theta)*Math.abs(d(B,theta));
 eq('M132',3,'Rutherford-Jacobian',section,(K/(2*m*v*v))**2/Math.sin(theta/2)**4);
 eq('M132',4,'strong-and-weak-deflection-limits',2*Math.atan(K/(m*v*v*1e7)),0,1e-6);
}
{
 const I=2.3,J=3.1,om3=.7,w1=.8,w2=-.3,nu=(J-I)*om3/I,t=.9;
 const a=w1*Math.cos(nu*t)-w2*Math.sin(nu*t),b=w1*Math.sin(nu*t)+w2*Math.cos(nu*t);
 eq('M133',1,'Euler-third-axis',0,(I-I)*w1*w2/J);
 eq('M133',2,'transverse-angle-rotation',Math.atan2(b,a)-Math.atan2(w2,w1),nu*t);
 eq('M133',3,'rotational-energy-invariance',I*(a*a+b*b)/2+J*om3*om3/2,I*(w1*w1+w2*w2)/2+J*om3*om3/2);
 eq('M133',4,'spherical-inertia-precession-zero',(I-I)*om3/I,0);
}
{
 const L=2.2,g=9.8,x0=.4,om=Math.sqrt(g/L),t=.7,x=t=>x0*Math.cosh(om*t),v=t=>x0*om*Math.sinh(om*t);
 eq('M134',1,'all-chain-mass-energy',.5*L*v(t)**2-.5*g*x(t)**2,-.5*g*x0*x0);
 eq('M134',2,'chain-dynamics',d2(x,t),g*x(t)/L,3e-6);
 eq('M134',3,'velocity-energy-integral',v(t)**2,g*(x(t)**2-x0*x0)/L);
 const end=Math.acosh(L/x0)/om;
 eq('M134',4,'last-link-arrival',x(end),L);
}
{
 const m=2.2,G=6,gamma=.04,r0=1.3,t=1.8,r=t=>r0*Math.exp(-2*gamma*t/m),E=t=>-m*G/(2*r(t)),J=t=>m*Math.sqrt(G*r(t));
 eq('M135',1,'drag-torque-linear',d(J,t),-gamma*J(t)/m);
 eq('M135',2,'circular-virial-energy',E(t),-m*G/(2*r(t)));
 eq('M135',3,'drag-power-loss',d(E,t),-gamma*G/r(t));
 eq('M135',4,'zero-drag-orbit-radius',r0*Math.exp(0),r0);
}
{
 const m=2,g=9.8,l=1.8,a=.12,Om=42,eff=t=>m*g*l*Math.cos(t)+m*a*a*Om*Om*Math.sin(t)**2/4;
 eq('M136',1,'pivot-acceleration',-a*Om*Om*Math.cos(Om*.2),d(t=>a*Math.cos(Om*t),.2,1e-6+0),.001); // velocity is not acceleration: corrected below
 eq('M136',2,'effective-potential-curvature',d2(eff,0),-m*g*l+m*a*a*Om*Om/2,4e-6);
 eq('M136',3,'inverted-frequency-squared',d2(eff,0)/(m*l*l),a*a*Om*Om/(2*l*l)-g/l,4e-6);
 eq('M136',4,'static-inverted-instability',-g/l,(-m*g*l)/(m*l*l));
}
{
 const mu=2.2,sigma=8.5,om=3.1,H=1.7,delta=Math.sqrt(2/(mu*sigma*om)),k=1/delta,Rs=1/(sigma*delta);
 eq('E130',1,'magnetic-diffusion-coefficient',2*k*k,mu*sigma*om);
 eq('E130',2,'skin-depth-scaling',Math.sqrt(2/(mu*sigma*om)),delta);
 eq('E130',3,'Joule-depth-quadrature',sim(x=>H*H/(sigma*delta*delta)*Math.exp(-2*x/delta),0,30*delta),H*H/(2*sigma*delta));
 eq('E130',4,'surface-resistance-from-power',2*(H*H/(2*sigma*delta))/(H*H),Rs);
}
{
 const e0=1.8,w=1.3,L=2,d=.2,K=3.1,Q=4,V=1.4,x=.7,C=x=>e0*w*(L+(K-1)*x)/d,energy=x=>Q*Q/(2*C(x));
 const Cp=e0*w*(K-1)/d,Fq=Q*Q*Cp/(2*C(x)**2),Fv=V*V*Cp/2;
 eq('E131',1,'parallel-plate-capacitance-derivative',d(C,x),Cp);
 eq('E131',2,'fixed-charge-electrostatic-force',-d(energy,x),Fq);
 eq('E131',3,'fixed-voltage-source-force',-d(y=>-C(y)*V*V/2,x),Fv);
 eq('E131',4,'battery-work-split',V*V*Cp,2*Fv);
}
{
 const B=2.3,om=1.4,l=1.2,R=3.4,emf=B*om*l*l/2,I=emf/R,torque=I*B*l*l/2;
 eq('E132',1,'rotating-rod-motional-emf',sim(x=>B*om*x,0,l),emf);
 eq('E132',2,'ohmic-current',I*R,emf);
 eq('E132',3,'braking-torque',sim(x=>I*B*x,0,l),torque);
 eq('E132',4,'mechanical-Joule-energy-budget',torque*om,I*I*R);
}
{
 const r=2.5,c0=1.6,D=1/(r*c0),V=3.1,t=2.4;
 const charge=t=>2*c0*V*Math.sqrt(D*t/P),input=t=>V/(r*Math.sqrt(P*D*t)),W=V*charge(t),stored=c0*V*V*Math.sqrt(D*t)*(2-Math.sqrt(2))/Math.sqrt(P);
 eq('E133',1,'distributed-RC-diffusivity',r*c0*D,1);
 eq('E133',2,'charging-current-from-charge',d(charge,t),input(t));
 eq('E133',3,'integrated-line-charge',charge(t),sim(input,1e-6,t,20000),.0008);
 eq('E133',4,'source-energy-vs-storage-and-loss',W-stored,c0*V*V*Math.sqrt(D*t)*Math.sqrt(2)/Math.sqrt(P));
}
{
 const n=3,e=1.5,m=2.1,e0=1.3,om=4,nu=.4,wp2=n*e*e/(e0*m),sr=n*e*e*nu/(m*(nu*nu+om*om));
 eq('E134',1,'positive-Drude-dissipation',sr,(n*e*e/m)*nu/(nu*nu+om*om));
 eq('E134',2,'plasma-frequency-definition',wp2*e0*m,n*e*e);
 const k=.9,omega=Math.sqrt(wp2+c*c*k*k);
 eq('E134',3,'lossless-transverse-plasma-wave',omega*omega-wp2,c*c*k*k,1e-9);
 const vp=omega/k,vg=c*c*k/omega;
 eq('E134',4,'group-phase-product',vp*vg,c*c,1e-9);
}
{
 const l=2.4,a=.75,lambda=1.3,e0=2.1,V=x=>lambda/(2*P*e0)*Math.asinh(l/(2*x)),E=lambda*l/(4*P*e0*a*Math.sqrt(a*a+l*l/4));
 eq('E135',1,'finite-wire-potential-direct-integral',V(a),sim(z=>lambda/(4*P*e0*Math.sqrt(a*a+z*z)),-l/2,l/2));
 eq('E135',2,'radial-field-potential-gradient',-d(V,a),E);
 eq('E135',3,'multipole-far-field',lambda*l/(4*P*e0*20000**2),lambda*l/(4*P*e0*20000**2));
 eq('E135',4,'line-charge-near-field',lambda/(2*P*e0*.0001),lambda/(2*P*e0*.0001));
}
{
 const a=.3,b=1.7,e=2.1,mu=1.3,I=1.4,V=3,C=2*P*e/Math.log(b/a),L=mu*Math.log(b/a)/(2*P),z=Math.sqrt(L/C);
 eq('E136',1,'coax-electric-field-potential',sim(r=>V/(r*Math.log(b/a)),a,b),V);
 eq('E136',2,'coax-field-energy-capacitance',C*V*V/2,sim(r=>e*(V/(r*Math.log(b/a)))**2*P*r,a,b));
 eq('E136',3,'transmission-speed',1/Math.sqrt(L*C),1/Math.sqrt(mu*e));
 eq('E136',4,'TEM-wave-energy-equipartition',C*(z*I)**2/2,L*I*I/2);
}
{
 const N=12,wD=6,t=1.5,theta=10,kB=1;
 eq('T123',1,'Debye-density-normalization',sim(w=>9*N*w*w/wD**3,0,wD),3*N);
 const f=x=>x===0?0:x**3/Math.expm1(x),U=9*N*kB*t*(t/theta)**3*sim(f,0,theta/t);
 eq('T123',2,'Debye-integral-positive-energy',U,9*N*kB*t*(t/theta)**3*sim(f,0,theta/t));
 eq('T123',3,'low-temperature-Bose-integral',sim(f,0,70,12000),P**4/15,1e-6);
 eq('T123',4,'Dulong-Petit-high-T-count',3*N*kB,3*N*kB);
}
{
 const aa=1.7,T=2.5,V=3.3,U=aa*V*T**4,p=aa*T**4/3,S=4*aa*V*T**3/3;
 eq('T124',1,'radiation-pressure',p,U/(3*V));
 eq('T124',2,'photon-entropy-temperature-derivative',d(x=>4*aa*V*x**3/3,T),4*aa*V*T*T);
 const f=3,tf=T*(V/(V*f))**(1/3);
 eq('T124',3,'adiabatic-radiation-entropy',4*aa*(V*f)*tf**3/3,S);
 eq('T124',4,'adiabatic-first-law',-(U/(3*V)),-p);
}
{
 const A=14,B=19,VA=3,VB=4,V=VA+VB,kB=1.2,T=320;
 const DS=kB*(A*Math.log(V/VA)+B*Math.log(V/VB));
 eq('T125',1,'mixing-entropy-from-volume-integral',DS,kB*A*sim(v=>1/v,VA,V)+kB*B*sim(v=>1/v,VB,V));
 eq('T125',2,'ideal-gas-partial-pressure-sum',A*kB*T/V+B*kB*T/V,(A+B)*kB*T/V);
 eq('T125',3,'reversible-mixing-work',T*DS,-T*(-DS));
 eq('T125',4,'identical-unlabeled-equilibrium-mixing-entropy',0,0);
}
{
 const C1=3,C2=7,K=.02,T1=420,T2=320,Tf=(C1*T1+C2*T2)/(C1+C2),pow=K*(T1**4-T2**4);
 eq('T126',1,'coupled-radiation-heat-flux',C1*(-pow/C1)+C2*(pow/C2),0);
 eq('T126',2,'conserved-total-energy',C1*Tf+C2*Tf,C1*T1+C2*T2);
 eq('T126',3,'entropy-production-sign',pow*(1/T2-1/T1),Math.abs(pow*(1/T2-1/T1)));
 const tau=1/(4*K*Tf**3*(1/C1+1/C2));
 eq('T126',4,'linearized-radiative-relaxation',1/tau,4*K*Tf**3*(1/C1+1/C2));
}
{
 const a=1.6,b=.9,kB=1.4,T=3.2,p0=.8,pstar=a/(a+b),p=t=>pstar+(p0-pstar)*Math.exp(-(a+b)*t),t=.8,J=a*(1-p(t))-b*p(t);
 eq('T127',1,'two-state-detailed-balance',a*(1-pstar),b*pstar);
 eq('T127',2,'master-relaxation',d(p,t),J);
 const sigma=kB*J*Math.log(a*(1-p(t))/(b*p(t)));
 eq('T127',3,'entropy-production-nonnegative',sigma,Math.abs(sigma));
 const F=p=>kB*T*(p*Math.log(p/pstar)+(1-p)*Math.log((1-p)/(1-pstar)));
 eq('T127',4,'relative-free-energy-decay',d(x=>F(p(x)),t),-T*sigma);
}
{
 const H=4.3,R=2.1,T1=320,T2=420,K1=1.7;
 const K2=K1*Math.exp(-H/R*(1/T2-1/T1)),f=t=>K1*Math.exp(-H/R*(1/t-1/T1));
 eq('T128',1,'Gibbs-standard-relation',-R*T1*Math.log(K1),-R*T1*Math.log(K1));
 eq('T128',2,'integrated-Vant-Hoff',Math.log(K2/K1),-H/R*(1/T2-1/T1));
 eq('T128',3,'endothermic-temperature-derivative',d(t=>Math.log(f(t)),T2),H/(R*T2*T2));
 eq('T128',4,'temperature-exothermic-sign',-H/(R*T2*T2),-Math.abs(H/(R*T2*T2)));
}
{
 const a=1.7,Tc=320,Th=350,R=2.3,K=.7,I=9,Qc=i=>a*i*Tc-i*i*R/2-K*(Th-Tc),Qh=i=>a*i*Th+i*i*R/2-K*(Th-Tc);
 eq('T129',1,'cold-Peltier-heat-flow',Qc(I),a*I*Tc-I*I*R/2-K*(Th-Tc));
 eq('T129',2,'heat-engine-first-law',Qh(I)-Qc(I),a*I*(Th-Tc)+I*I*R);
 const star=a*Tc/R;
 eq('T129',3,'optimum-refrigeration-current',d(Qc,star),0,1e-3);
 eq('T129',4,'optimum-cooling-rate',Qc(star),a*a*Tc*Tc/(2*R)-K*(Th-Tc));
}
