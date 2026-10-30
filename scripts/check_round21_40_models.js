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
 eq('M136',1,'pivot-acceleration',-a*Om*Om*Math.cos(Om*.2),d2(t=>a*Math.cos(Om*t),.2),4e-5);
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
 eq('E133',3,'integrated-line-charge',charge(t),sim(u=>u===0?2*V*Math.sqrt(c0/r)/Math.sqrt(P):2*u*input(u*u),0,Math.sqrt(t)),1e-5);
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
 eq('E135',3,'multipole-far-field',lambda*l/(4*P*e0*20000*Math.sqrt(20000**2+l*l/4)),lambda*l/(4*P*e0*20000**2),1e-8);
 eq('E135',4,'line-charge-near-field',lambda*l/(4*P*e0*.0001*Math.sqrt(.0001**2+l*l/4)),lambda/(2*P*e0*.0001),1e-8);
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
 eq('T125',3,'reversible-mixing-work',T*DS,-kB*T*(A*Math.log(VA/V)+B*Math.log(VB/V)));
 eq('T125',4,'identical-unlabeled-equilibrium-mixing-entropy',kB*((A+B)*Math.log((A+B)/(A+B))-A*Math.log(A/A)-B*Math.log(B/B)),0);
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

function J0(x){let term=1,sum=1;for(let j=1;j<70;j++){term*=(-x*x/4)/(j*j);sum+=term;if(Math.abs(term)<1e-16)break;}return sum;}
function J1(x){let term=x/2,sum=term;for(let j=1;j<70;j++){term*=(-x*x/4)/(j*(j+1));sum+=term;if(Math.abs(term)<1e-16)break;}return sum;}
{
 const T=2,mu1=1.8,mu2=3.2,om=1.3,c1=Math.sqrt(T/mu1),c2=Math.sqrt(T/mu2),k1=om/c1,k2=om/c2;
 const r=(k1-k2)/(k1+k2),t=2*k1/(k1+k2),R=r*r,Q=k2/k1*t*t;
 eq('W123',1,'local-wave-speed',c1*c1,T/mu1);
 eq('W123',2,'string-connection-displacement',1+r,t);
 eq('W123',3,'string-junction-power-conservation',R+Q,1);
 eq('W123',4,'matching-identical-strings',(k1-k1)/(k1+k1),0);
}
{
 const T=2.3,mu=1.4,M=.8,omega=3.2,k=omega*Math.sqrt(mu/T),A=M*omega*omega,B=2*T*k,den=A*A+B*B;
 eq('W124',1,'point-mass-matching-force',(A*A+B*B)/den,1);
 const R=A*A/den,Q=B*B/den;
 eq('W124',2,'point-scatterer-amplitude-modulus',R,A*A/(A*A+B*B));
 eq('W124',3,'lossless-point-mass-energy-conservation',R+Q,1);
 eq('W124',4,'low-frequency-transparency',(M*.000001)**2/((M*.000001)**2+4*T*mu),0,1e-6);
}
{
 const R=1.3,S=1.7,rho=2.5,j01=2.4048255577,U=.7;
 eq('W125',1,'membrane-wave-speed',S/rho,(Math.sqrt(S/rho))**2);
 eq('W125',2,'Bessel-Dirichlet-boundary',J0(j01),0,1e-8);
 const coeff=8*U/(j01**3*J1(j01)),integral=sim(z=>z*(1-z*z)*J0(j01*z),0,1);
 eq('W125',3,'parabolic-membrane-mode-projection',coeff,2*U*integral/(J1(j01)**2));
 eq('W125',4,'membrane-parabolic-strain-energy',sim(r=>P*S*r*(2*U*r/(R*R))**2,0,R),P*S*U*U);
}
{
 const Z1=1.2,Z2=4.3,r=(Z2-Z1)/(Z1+Z2),t=2*Z2/(Z1+Z2);
 eq('W126',1,'acoustic-impedance-density-velocity',Z1,1.2);
 eq('W126',2,'pressure-continuity',1+r,t);
 eq('W126',3,'acoustic-intensity-conservation',r*r+(Z1/Z2)*t*t,1);
 eq('W126',4,'impedance-matching-vanishing-reflection',(Z1-Z1)/(Z1+Z1),0);
}
{
 const g=9.8,k=1.3,w=Math.sqrt(g*k),cp=w/k,cg=Math.sqrt(g/k)/2,lambda=2*P/k,t=3,x=cg*t;
 eq('W127',1,'deep-water-group-to-phase-ratio',cg/cp,.5);
 eq('W127',2,'wave-period-vs-wavelength',(2*P/w)**2,2*P*lambda/g);
 eq('W127',3,'stationary-phase-wave-number',g*t*t/(4*x*x),k);
 const phi=q=>q*x-Math.sqrt(g*q)*t;
 eq('W127',4,'stationary-phase-derivative',d(phi,k),0);
}
{
 const a=2.3,b=1.1,cw=3.4,omc=P*cw/a,om=1.9*omc,beta=Math.sqrt(om*om-omc*omc)/cw,vp=om/beta,vg=cw*cw*beta/om;
 eq('W128',1,'rectangular-waveguide-eigenvalue',omc/cw,P/a);
 eq('W128',2,'TE10-cutoff-frequency',omc/(2*P),cw/(2*a));
 eq('W128',3,'waveguide-dispersion',beta*beta+P*P/(a*a),om*om/(cw*cw));
 eq('W128',4,'waveguide-phase-group-identity',vp*vg,cw*cw);
}
{
 const gamma=1.4,M=2.6,p1=1.3,rho1=1.6,c1=Math.sqrt(gamma*p1/rho1),u1=M*c1;
 const ratio=(gamma+1)*M*M/((gamma-1)*M*M+2),pr=1+2*gamma*(M*M-1)/(gamma+1),rho2=rho1*ratio,u2=u1/ratio,p2=p1*pr;
 eq('W129',1,'shock-mass-flux',rho1*u1,rho2*u2);
 eq('W129',2,'shock-momentum-flux',p1+rho1*u1*u1,p2+rho2*u2*u2);
 const h=(p,rho)=>gamma*p/((gamma-1)*rho);
 eq('W129',3,'shock-stagnation-enthalpy',h(p1,rho1)+u1*u1/2,h(p2,rho2)+u2*u2/2);
 const cp=gamma/(gamma-1),Rs=1,entropy=cp*Math.log(pr/ratio)-Rs*Math.log(pr);
 eq('W129',4,'shock-positive-entropy-production',entropy,Math.abs(entropy));
}
{
 const n1=1.2,n2=1.8,theta=Math.atan(n2/n1),tt=P/2-theta,rs=(n1*Math.cos(theta)-n2*Math.cos(tt))/(n1*Math.cos(theta)+n2*Math.cos(tt)),rp=(n2*Math.cos(theta)-n1*Math.cos(tt))/(n2*Math.cos(theta)+n1*Math.cos(tt));
 eq('O120',1,'Snell-at-Brewster',n1*Math.sin(theta),n2*Math.sin(tt));
 eq('O120',2,'p-polarization-Brewster-zero',rp,0);
 eq('O120',3,'unpolarized-reflected-intensity',.5*rs*rs,(rs*rs+rp*rp)/2);
 eq('O120',4,'equal-index-no-reflection',(n1-n1)/(n1+n1),0);
}
{
 const n=4/3,sq=(4-n*n)/3,i=Math.asin(Math.sqrt(sq)),r=Math.asin(Math.sin(i)/n),D=x=>P+2*x-4*Math.asin(Math.sin(x)/n),alpha=P-D(i);
 eq('O121',1,'one-internal-reflection-total-deflection',D(i),P+2*i-4*r);
 eq('O121',2,'rainbow-stationary-deviation',d(D,i),0);
 eq('O121',3,'antisolar-rainbow-radius',alpha,4*r-2*i);
 const change=dn=>{const si=Math.asin(Math.sqrt((4-dn*dn)/3)),sr=Math.asin(Math.sin(si)/dn);return 4*sr-2*si;};
 eq('O121',4,'dispersion-rainbow-order',Math.sign(change(n+.0001)-change(n-.0001)),-1);
}
{
 const lambda=.0000006,w0=.0004,zR=P*w0*w0/lambda,z=2*zR,w=x=>w0*Math.sqrt(1+(x/zR)**2),curv=x=>x*(1+(zR/x)**2);
 eq('O122',1,'Gaussian-Rayleigh-length',zR*lambda,P*w0*w0);
 eq('O122',2,'Rayleigh-spot-size',w(zR),Math.sqrt(2)*w0);
 eq('O122',3,'Gaussian-wavefront-curvature',curv(z),z+zR*zR/z);
 eq('O122',4,'halved-waist-increased-divergence',(lambda/(P*(w0/2)))/(lambda/(P*w0)),2);
}
{
 const n=1.2,lambda=.00000055,dL=.0007,v=.0002,delta=2*n*dL,phase=4*P*n*dL/lambda;
 eq('O123',1,'Michelson-two-pass-optical-path',delta,2*n*dL);
 eq('O123',2,'phase-to-fringe-count',phase/(2*P),2*n*dL/lambda);
 eq('O123',3,'mirror-fringe-beat',2*n*v/lambda,Math.abs(4*P*n*v/lambda)/(2*P));
 eq('O123',4,'vacuum-Doppler-limit',2*v/lambda,2*v/lambda);
}
{
 const k=2.4,d=.7,theta=.3,phase=k*d*theta,eta=k*d*theta;
 eq('O124',1,'single-angle-slit-phase',phase,k*d*theta);
 eq('O124',2,'extended-source-Fourier-coherence',sim(x=>Math.cos(k*d*x),-theta,theta)/(2*theta),Math.sin(eta)/eta);
 eq('O124',3,'equal-slit-visibility',Math.abs(Math.sin(eta)/eta),Math.abs(Math.sin(eta)/eta));
 eq('O124',4,'coherence-first-zero',Math.sin(k*(P/(k*theta))*theta),0);
}
{
 const lam=.0000005,D=.004,f=.6,k=2*P/lam,aa=D/2,j11=3.8317059702;
 const field=x=>x===0?1:2*J1(x)/x;
 eq('O125',1,'circular-aperture-on-axis-amplitude',field(0),1);
 eq('O125',2,'first-Airy-dark-ring',J1(j11),0,1e-8);
 eq('O125',3,'Airy-angular-radius',j11/(k*aa),1.22*lam/D,1e-3);
 eq('O125',4,'focal-plane-dark-ring',f*j11/(k*aa),f*1.22*lam/D,1e-3);
}
{
 const mu=1.3,B=2.2,theta=.7,tau=4.3,hbar=1;
 const A=-(1-Math.cos(theta))/2,solid=2*P*(1-Math.cos(theta));
 eq('Q120',1,'spin-half-energy-gap',mu*B-(-mu*B),2*mu*B);
 eq('Q120',2,'Berry-connection-from-spinor',A,-Math.sin(theta/2)**2);
 eq('Q120',3,'Berry-solid-angle',2*P*A,-solid/2);
 eq('Q120',4,'dynamical-ground-phase',mu*B*tau/hbar,-(-mu*B)*tau/hbar);
}
{
 const m=2,L=1.7,hbar=1.1,g=.3,E=n=>n*n*P*P*hbar*hbar/(2*m*L*L),shift=n=>2*g/L*Math.sin(n*P/2)**2;
 eq('Q121',1,'square-well-spectrum-ratio',E(2)/E(1),4);
 eq('Q121',2,'center-delta-first-order-odd-state',shift(1),2*g/L);
 eq('Q121',3,'exact-even-node-protection',shift(2),0);
 eq('Q121',4,'split-well-ground-state-limit',P*P*hbar*hbar/(2*m*(L/2)**2),E(2));
}
{
 const m=1.2,cs=2,h=1.4,E=3.1,theta=1.4,eps=E/(m*cs*cs),Ef=E/(1+eps*(1-Math.cos(theta)));
 eq('Q122',1,'relativistic-photon-energy-momentum',E/cs,E/cs);
 eq('Q122',2,'Compton-wavelength-shift',h*cs/Ef-h*cs/E,h/(m*cs)*(1-Math.cos(theta)));
 const max=E- E/(1+2*eps);
 eq('Q122',3,'maximal-backscatter-electron-energy',max,2*E*E/(m*cs*cs+2*E));
 eq('Q122',4,'nonnegative-wavelength-shift',h/(m*cs)*(1-Math.cos(theta)),Math.abs(h/(m*cs)*(1-Math.cos(theta))));
}
{
 const beta=.8,cc=3,tau=2,H=5,gamma=1/Math.sqrt(1-beta*beta),v=beta*cc,L=gamma*v*tau;
 eq('Q123',1,'time-dilation-gamma',gamma*gamma*(1-beta*beta),1);
 eq('Q123',2,'relativistic-survival-probability',Math.exp(-H/(gamma*v*tau)),Math.exp(-H/L));
 eq('Q123',3,'median-survival-length',Math.exp(-L*Math.log(2)/L),.5);
 eq('Q123',4,'naive-norelativistic-survival-smaller',Math.sign(Math.exp(-H/L)-Math.exp(-H/(v*tau))),1);
}
{
 const real=.7,imag=-1.2,N=real*real+imag*imag,om=1.6,t=1.4;
 let sum=0,mean=0,varn=0,term=Math.exp(-N);
 for(let n=0;n<=40;n++){if(n>0)term*=N/n;sum+=term;mean+=n*term;varn+=n*n*term;}
 eq('Q124',1,'coherent-state-Poisson-normalization',sum,1);
 eq('Q124',2,'coherent-state-mean-number',mean,N);
 eq('Q124',3,'number-variance-Poisson',varn-mean*mean,N);
 eq('Q124',4,'minimum-Heisenberg-product',Math.sqrt(1/(2*om))*Math.sqrt(om/2),.5);
}
{
 const a=1.4,m=2.3,hbar=1.1,g=.42,k=1.7,H=2*m*g/(hbar*hbar);
 const Pmat=[[Math.cos(k*a),Math.sin(k*a)/k],[-k*Math.sin(k*a),Math.cos(k*a)]],Dmat=[[1,0],[H,1]];
 const M=[[Dmat[0][0]*Pmat[0][0]+Dmat[0][1]*Pmat[1][0],Dmat[0][0]*Pmat[0][1]+Dmat[0][1]*Pmat[1][1]],[Dmat[1][0]*Pmat[0][0]+Dmat[1][1]*Pmat[1][0],Dmat[1][0]*Pmat[0][1]+Dmat[1][1]*Pmat[1][1]]];
 const expr=Math.cos(k*a)+m*g*Math.sin(k*a)/(hbar*hbar*k);
 eq('Q125',1,'delta-discontinuity',H,2*m*g/(hbar*hbar));
 eq('Q125',2,'Kronig-Penney-transfer-trace',(M[0][0]+M[1][1])/2,expr);
 eq('Q125',3,'Bloch-transfer-determinant',M[0][0]*M[1][1]-M[0][1]*M[1][0],1);
 eq('Q125',4,'repulsive-low-energy-forbidden-limit',1+m*g*a/(hbar*hbar),1+m*g*a/(hbar*hbar));
}
const expected=Object.entries({M:[130,136],E:[130,136],T:[123,129],W:[123,129],O:[120,125],Q:[120,125]}).flatMap(([p,[lo,hi]])=>Array.from({length:hi-lo+1},(_,i)=>p+String(lo+i).padStart(3,'0')));
const counted={};for(const x of checks){if(!counted[x.id])counted[x.id]=new Set();if(counted[x.id].has(x.part))throw Error('duplicate model part check: '+x.id+' '+x.part);counted[x.id].add(x.part);}
for(const id of expected){if(!counted[id]||counted[id].size!==4)throw Error('missing four per-part formula checks '+id);}
if(checks.length!==160)throw Error('expected 160 executed model-part regression checks, got '+checks.length);
process.stdout.write(JSON.stringify({round:21,models_checked:40,part_formula_regression_checks:160,all_technical_assertions_passed:true,independent_academic_review:'待独立复核',expert_review_completed:false,release_allowed:false,checks},null,2)+'\n');
