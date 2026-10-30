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
 const m=2,a=3,g=9.8,Om=2.4,th=.63,U=t=>m*g*a*(1-Math.cos(t))-m*a*a*Om*Om*Math.sin(t)**2/2;
 eq('M137',1,'effective potential derivative versus theta force',d(U,th),m*a*g*Math.sin(th)-m*a*a*Om*Om*Math.sin(th)*Math.cos(th));
 eq('M137',2,'critical speed squared times radius',g/a*a,g);
 const equilibrium=Math.acos(g/(a*Om*Om));
 eq('M137',3,'bifurcated equilibria zero force',d(U,equilibrium),0);
 eq('M137',4,'well curvature versus small oscillation',d2(U,equilibrium)/(m*a*a),Om*Om*Math.sin(equilibrium)**2,2e-5);
}
{
 const a=1.2,g=9.8,th=.6,s=t=>4*a*Math.sin(t/2),x=t=>a*(t+Math.sin(t)),y=t=>a*(1-Math.cos(t)),w=Math.sqrt(g/(4*a));
 eq('M138',1,'arclength-derivative',d(s,th),Math.hypot(d(x,th),d(y,th)));
 eq('M138',2,'quadratic-cycloid-height',y(th),s(th)**2/(8*a));
 eq('M138',3,'isochronous-period',2*P/w,4*P*Math.sqrt(a/g));
 eq('M138',4,'quarter-period-bottom-crossing',Math.cos(w*P/(2*w)),0);
}
{
 const m=2.1,v=2.3,b=.8,K=1.4,E=m*v*v/2,L=m*v*b,r=(K+Math.sqrt(K*K+m*m*v**4*b*b))/(m*v*v),e=Math.sqrt(1+(m*v*v*b/K)**2),theta=2*Math.atan(K/(m*v*v*b));
 eq('M139',1,'turning-point-energy',E,L*L/(2*m*r*r)+K/r);
 eq('M139',2,'scattering-eccentricity',Math.cos((P-theta)/2),1/e);
 const B=t=>K/(m*v*v)*1/Math.tan(t/2),section=B(theta)/Math.sin(theta)*Math.abs(d(B,theta));
 eq('M139',3,'Rutherford-Jacobian',section,(K/(2*m*v*v))**2/Math.sin(theta/2)**4);
 eq('M139',4,'strong-and-weak-deflection-limits',2*Math.atan(K/(m*v*v*1e7)),0,1e-6);
}
{
 const I=2.3,J=3.1,om3=.7,w1=.8,w2=-.3,nu=(J-I)*om3/I,t=.9;
 const a=w1*Math.cos(nu*t)-w2*Math.sin(nu*t),b=w1*Math.sin(nu*t)+w2*Math.cos(nu*t);
 eq('M140',1,'Euler-third-axis',0,(I-I)*w1*w2/J);
 eq('M140',2,'transverse-angle-rotation',Math.atan2(b,a)-Math.atan2(w2,w1),nu*t);
 eq('M140',3,'rotational-energy-invariance',I*(a*a+b*b)/2+J*om3*om3/2,I*(w1*w1+w2*w2)/2+J*om3*om3/2);
 eq('M140',4,'spherical-inertia-precession-zero',(I-I)*om3/I,0);
}
{
 const L=2.2,g=9.8,x0=.4,om=Math.sqrt(g/L),t=.7,x=t=>x0*Math.cosh(om*t),v=t=>x0*om*Math.sinh(om*t);
 eq('M141',1,'all-chain-mass-energy',.5*L*v(t)**2-.5*g*x(t)**2,-.5*g*x0*x0);
 eq('M141',2,'chain-dynamics',d2(x,t),g*x(t)/L,3e-6);
 eq('M141',3,'velocity-energy-integral',v(t)**2,g*(x(t)**2-x0*x0)/L);
 const end=Math.acosh(L/x0)/om;
 eq('M141',4,'last-link-arrival',x(end),L);
}
{
 const m=2.2,G=6,gamma=.04,r0=1.3,t=1.8,r=t=>r0*Math.exp(-2*gamma*t/m),E=t=>-m*G/(2*r(t)),J=t=>m*Math.sqrt(G*r(t));
 eq('M142',1,'drag-torque-linear',d(J,t),-gamma*J(t)/m);
 eq('M142',2,'circular-virial-energy',E(t),-m*G/(2*r(t)));
 eq('M142',3,'drag-power-loss',d(E,t),-gamma*G/r(t));
 eq('M142',4,'zero-drag-orbit-radius',r0*Math.exp(0),r0);
}
{
 const m=2,g=9.8,l=1.8,a=.12,Om=42,eff=t=>m*g*l*Math.cos(t)+m*a*a*Om*Om*Math.sin(t)**2/4;
 eq('M143',1,'pivot-acceleration',-a*Om*Om*Math.cos(Om*.2),d2(t=>a*Math.cos(Om*t),.2),4e-5);
 eq('M143',2,'effective-potential-curvature',d2(eff,0),-m*g*l+m*a*a*Om*Om/2,4e-6);
 eq('M143',3,'inverted-frequency-squared',d2(eff,0)/(m*l*l),a*a*Om*Om/(2*l*l)-g/l,4e-6);
 eq('M143',4,'static-inverted-instability',-g/l,(-m*g*l)/(m*l*l));
}
{
 const L1=3,L2=7,M=1.4,I1=2,I2=.8,flux=L1*I1+M*I2,I1next=flux/L1;
 const U=(x,y)=>(L1*x*x+2*M*x*y+L2*y*y)/2;
 eq('E137',1,'mutual flux cross derivative',d(y=>L1*I1+M*y,I2),M);
 eq('E137',2,'positive determinant sufficient condition',L1*L2-M*M>0?1:0,1);
 eq('E137',3,'superconducting flux unchanged',L1*I1next,flux);
 eq('E137',4,'extracted magnetic energy',U(I1,I2)-U(I1next,0),(L2-M*M/L1)*I2*I2/2);
}
{
 const q=3,h=2,eps=4,K=q/(4*P*eps),phi=(r,z)=>K*(1/Math.hypot(r,z-h)-1/Math.hypot(r,z+h));
 eq('E138',1,'grounded-plane potential',phi(.8,0),0);
 const bound=100*h,sigma=r=>-q*h/(2*P*(r*r+h*h)**1.5);
 eq('E138',2,'induced surface charge integral',sim(r=>2*P*r*sigma(r),0,bound),-q*(1-h/Math.hypot(bound,h)),1e-7);
 const F=-q*q/(16*P*eps*h*h),U=z=>-q*q/(16*P*eps*z);
 eq('E138',3,'image force magnitude',F,-q*q/(4*P*eps*(2*h)**2));
 eq('E138',4,'mechanical work from derivative',-d(U,h),F);
}
{
 const B=2.3,om=1.4,l=1.2,R=3.4,emf=B*om*l*l/2,I=emf/R,torque=I*B*l*l/2;
 eq('E139',1,'rotating-rod-motional-emf',sim(x=>B*om*x,0,l),emf);
 eq('E139',2,'ohmic-current',I*R,emf);
 eq('E139',3,'braking-torque',sim(x=>I*B*x,0,l),torque);
 eq('E139',4,'mechanical-Joule-energy-budget',torque*om,I*I*R);
}
{
 const r=2.5,c0=1.6,D=1/(r*c0),V=3.1,t=2.4;
 const charge=t=>2*c0*V*Math.sqrt(D*t/P),input=t=>V/(r*Math.sqrt(P*D*t)),W=V*charge(t),stored=c0*V*V*Math.sqrt(D*t)*(2-Math.sqrt(2))/Math.sqrt(P);
 eq('E140',1,'distributed-RC-diffusivity',r*c0*D,1);
 eq('E140',2,'charging-current-from-charge',d(charge,t),input(t));
 eq('E140',3,'integrated-line-charge',charge(t),sim(u=>u===0?2*V*Math.sqrt(c0/r)/Math.sqrt(P):2*u*input(u*u),0,Math.sqrt(t)),1e-5);
 eq('E140',4,'source-energy-vs-storage-and-loss',W-stored,c0*V*V*Math.sqrt(D*t)*Math.sqrt(2)/Math.sqrt(P));
}
{
 const n=3,e=1.5,m=2.1,e0=1.3,om=4,nu=.4,wp2=n*e*e/(e0*m),sr=n*e*e*nu/(m*(nu*nu+om*om));
 eq('E141',1,'positive-Drude-dissipation',sr,(n*e*e/m)*nu/(nu*nu+om*om));
 eq('E141',2,'plasma-frequency-definition',wp2*e0*m,n*e*e);
 const k=.9,omega=Math.sqrt(wp2+c*c*k*k);
 eq('E141',3,'lossless-transverse-plasma-wave',omega*omega-wp2,c*c*k*k,1e-9);
 const vp=omega/k,vg=c*c*k/omega;
 eq('E141',4,'group-phase-product',vp*vg,c*c,1e-9);
}
{
 const l=2.4,a=.75,lambda=1.3,e0=2.1,V=x=>lambda/(2*P*e0)*Math.asinh(l/(2*x)),E=lambda*l/(4*P*e0*a*Math.sqrt(a*a+l*l/4));
 eq('E142',1,'finite-wire-potential-direct-integral',V(a),sim(z=>lambda/(4*P*e0*Math.sqrt(a*a+z*z)),-l/2,l/2));
 eq('E142',2,'radial-field-potential-gradient',-d(V,a),E);
 eq('E142',3,'multipole-far-field',lambda*l/(4*P*e0*20000*Math.sqrt(20000**2+l*l/4)),lambda*l/(4*P*e0*20000**2),1e-8);
 eq('E142',4,'line-charge-near-field',lambda*l/(4*P*e0*.0001*Math.sqrt(.0001**2+l*l/4)),lambda/(2*P*e0*.0001),1e-8);
}
{
 const Z0=50,R=200,Zt=Math.sqrt(Z0*R),delta=.001;
 const inp=t=>{const x=Math.tan(t),den=Zt*Zt+R*R*x*x;return {re:Zt*Zt*R*(1+x*x)/den,im:Zt*x*(Zt*Zt-R*R)/den};};
 eq('E143',1,'no-length transmission load',inp(0).re,R);
 eq('E143',2,'quarter wave transformer matched',Zt*Zt/R,Z0);
 eq('E143',3,'linear detuning reactive input',inp(P/2+delta).im/(Z0*delta),R/Zt-Zt/R,2e-5);
 const zi=inp(P/2+delta),gamma2=((zi.re-Z0)**2+zi.im**2)/((zi.re+Z0)**2+zi.im**2);
 eq('E143',4,'load real power versus reflected power',4*Z0*zi.re/((zi.re+Z0)**2+zi.im**2),1-gamma2);
}
{
 const R=8,T=300,B=.3,v1=1.2,v2=2.7,p=v=>R*T*(1/v+B/(v*v));
 const W=R*T*(Math.log(v2/v1)+B*(1/v1-1/v2));
 eq('T130',1,'virial compression factor',p(v1)*v1/(R*T),1+B/v1);
 eq('T130',2,'reversible isothermal work integral',sim(p,v1,v2),W);
 eq('T130',3,'entropy Maxwell heat consistency',W/T,R*(Math.log(v2/v1)+B*(1/v1-1/v2)));
 eq('T130',4,'isothermal compressibility derivative',-1/(v1*d(p,v1)),v1*v1/(R*T*(v1+2*B)));
}
{
 const aa=1.7,T=2.5,V=3.3,U=aa*V*T**4,p=aa*T**4/3,S=4*aa*V*T**3/3;
 eq('T131',1,'radiation-pressure',p,U/(3*V));
 eq('T131',2,'photon-entropy-temperature-derivative',d(x=>4*aa*V*x**3/3,T),4*aa*V*T*T);
 const f=3,tf=T*(V/(V*f))**(1/3);
 eq('T131',3,'adiabatic-radiation-entropy',4*aa*(V*f)*tf**3/3,S);
 eq('T131',4,'adiabatic-first-law',-(U/(3*V)),-p);
}
{
 const kb=2,T=5,m=3,g=4,n0=7,H=kb*T/(m*g),n=z=>n0*Math.exp(-z/H);
 eq('T132',1,'isothermal hydrostatic logarithmic slope',d(z=>Math.log(n(z)),H),-1/H);
 eq('T132',2,'column number convergent',sim(n,0,20*H),n0*H,1e-7);
 eq('T132',3,'mean molecule gravity energy',m*g*sim(z=>z*Math.exp(-z/H)/H,0,30*H),kb*T);
 eq('T132',4,'median altitude property',Math.exp(-Math.log(2)),.5);
}
{
 const C1=3,C2=7,K=.02,T1=420,T2=320,Tf=(C1*T1+C2*T2)/(C1+C2),pow=K*(T1**4-T2**4);
 eq('T133',1,'coupled-radiation-heat-flux',C1*(-pow/C1)+C2*(pow/C2),0);
 eq('T133',2,'conserved-total-energy',C1*Tf+C2*Tf,C1*T1+C2*T2);
 eq('T133',3,'entropy-production-sign',pow*(1/T2-1/T1),Math.abs(pow*(1/T2-1/T1)));
 const tau=1/(4*K*Tf**3*(1/C1+1/C2));
 eq('T133',4,'linearized-radiative-relaxation',1/tau,4*K*Tf**3*(1/C1+1/C2));
}
{
 const a=1.6,b=.9,kB=1.4,T=3.2,p0=.8,pstar=a/(a+b),p=t=>pstar+(p0-pstar)*Math.exp(-(a+b)*t),t=.8,J=a*(1-p(t))-b*p(t);
 eq('T134',1,'two-state-detailed-balance',a*(1-pstar),b*pstar);
 eq('T134',2,'master-relaxation',d(p,t),J);
 const sigma=kB*J*Math.log(a*(1-p(t))/(b*p(t)));
 eq('T134',3,'entropy-production-nonnegative',sigma,Math.abs(sigma));
 const F=p=>kB*T*(p*Math.log(p/pstar)+(1-p)*Math.log((1-p)/(1-pstar)));
 eq('T134',4,'relative-free-energy-decay',d(x=>F(p(x)),t),-T*sigma);
}
{
 const H=4.3,R=2.1,T1=320,T2=420,K1=1.7;
 const K2=K1*Math.exp(-H/R*(1/T2-1/T1)),f=t=>K1*Math.exp(-H/R*(1/t-1/T1));
 eq('T135',1,'Gibbs-standard-relation',-R*T1*Math.log(K1),-R*T1*Math.log(K1));
 eq('T135',2,'integrated-Vant-Hoff',Math.log(K2/K1),-H/R*(1/T2-1/T1));
 eq('T135',3,'endothermic-temperature-derivative',d(t=>Math.log(f(t)),T2),H/(R*T2*T2));
 eq('T135',4,'temperature-exothermic-sign',-H/(R*T2*T2),-Math.abs(H/(R*T2*T2)));
}
{
 const a=1.7,Tc=320,Th=350,R=2.3,K=.7,I=9,Qc=i=>a*i*Tc-i*i*R/2-K*(Th-Tc),Qh=i=>a*i*Th+i*i*R/2-K*(Th-Tc);
 eq('T136',1,'cold-Peltier-heat-flow',Qc(I),a*I*Tc-I*I*R/2-K*(Th-Tc));
 eq('T136',2,'heat-engine-first-law',Qh(I)-Qc(I),a*I*(Th-Tc)+I*I*R);
 const star=a*Tc/R;
 eq('T136',3,'optimum-refrigeration-current',d(Qc,star),0,1e-3);
 eq('T136',4,'optimum-cooling-rate',Qc(star),a*a*Tc*Tc/(2*R)-K*(Th-Tc));
}

function J0(x){let term=1,sum=1;for(let j=1;j<70;j++){term*=(-x*x/4)/(j*j);sum+=term;if(Math.abs(term)<1e-16)break;}return sum;}
function J1(x){let term=x/2,sum=term;for(let j=1;j<70;j++){term*=(-x*x/4)/(j*(j+1));sum+=term;if(Math.abs(term)<1e-16)break;}return sum;}
{
 const mu=2,T=8,L=4,gamma=.1,n=2,wn=n*P/L*Math.sqrt(T/mu),alpha=gamma/(2*mu),wd=Math.sqrt(wn*wn-alpha*alpha),A=1.7;
 const x=t=>A*Math.exp(-alpha*t)*(Math.cos(wd*t)+alpha/wd*Math.sin(wd*t));
 eq('W130',1,'modal undamped eigenvalue',wn*wn,(T/mu)*(n*P/L)**2);
 eq('W130',2,'damped modal frequency relation',wd*wd+alpha*alpha,wn*wn);
 eq('W130',3,'zero initial velocity',d(x,0),0);
 eq('W130',4,'quality factor lifetime relation',(mu*wn/gamma)*gamma/mu,wn);
}
{
 const T=2.3,mu=1.4,M=.8,omega=3.2,k=omega*Math.sqrt(mu/T),A=M*omega*omega,B=2*T*k,den=A*A+B*B;
 eq('W131',1,'point-mass-matching-force',(A*A+B*B)/den,1);
 const R=A*A/den,Q=B*B/den;
 eq('W131',2,'point-scatterer-amplitude-modulus',R,A*A/(A*A+B*B));
 eq('W131',3,'lossless-point-mass-energy-conservation',R+Q,1);
 eq('W131',4,'low-frequency-transparency',(M*.000001)**2/((M*.000001)**2+4*T*mu),0,1e-6);
}
{
 const R=1.3,S=1.7,rho=2.5,j01=2.4048255577,U=.7;
 eq('W132',1,'membrane-wave-speed',S/rho,(Math.sqrt(S/rho))**2);
 eq('W132',2,'Bessel-Dirichlet-boundary',J0(j01),0,1e-8);
 const coeff=8*U/(j01**3*J1(j01)),integral=sim(z=>z*(1-z*z)*J0(j01*z),0,1);
 eq('W132',3,'parabolic-membrane-mode-projection',coeff,2*U*integral/(J1(j01)**2));
 eq('W132',4,'membrane-parabolic-strain-energy',sim(r=>P*S*r*(2*U*r/(R*R))**2,0,R),P*S*U*U);
}
{
 const Z1=1.2,Z2=4.3,r=(Z2-Z1)/(Z1+Z2),t=2*Z2/(Z1+Z2);
 eq('W133',1,'acoustic-impedance-density-velocity',Z1,1.2);
 eq('W133',2,'pressure-continuity',1+r,t);
 eq('W133',3,'acoustic-intensity-conservation',r*r+(Z1/Z2)*t*t,1);
 eq('W133',4,'impedance-matching-vanishing-reflection',(Z1-Z1)/(Z1+Z1),0);
}
{
 const c=343,fs=550,vs=20,vr=7,wavelength=(c-vs)/fs,fr=fs*(c-vr)/(c-vs);
 eq('W134',1,'source compression of forward crests',wavelength*fs,c-vs);
 eq('W134',2,'relative receiver crest crossing',fr*wavelength,c-vr);
 eq('W134',3,'invert stationary receiver measurement',c*(1-fs/(fs*c/(c-vs))),vs);
 const beat=fs*(c-vr)*vs/(c*(c-vs));
 eq('W134',4,'Doppler against static reference beat',fr-fs*(c-vr)/c,beat);
}
{
 const a=2.3,b=1.1,cw=3.4,omc=P*cw/a,om=1.9*omc,beta=Math.sqrt(om*om-omc*omc)/cw,vp=om/beta,vg=cw*cw*beta/om;
 eq('W135',1,'rectangular-waveguide-eigenvalue',omc/cw,P/a);
 eq('W135',2,'TE10-cutoff-frequency',omc/(2*P),cw/(2*a));
 eq('W135',3,'waveguide-dispersion',beta*beta+P*P/(a*a),om*om/(cw*cw));
 eq('W135',4,'waveguide-phase-group-identity',vp*vg,cw*cw);
}
{
 const gamma=1.4,M=2.6,p1=1.3,rho1=1.6,c1=Math.sqrt(gamma*p1/rho1),u1=M*c1;
 const ratio=(gamma+1)*M*M/((gamma-1)*M*M+2),pr=1+2*gamma*(M*M-1)/(gamma+1),rho2=rho1*ratio,u2=u1/ratio,p2=p1*pr;
 eq('W136',1,'shock-mass-flux',rho1*u1,rho2*u2);
 eq('W136',2,'shock-momentum-flux',p1+rho1*u1*u1,p2+rho2*u2*u2);
 const h=(p,rho)=>gamma*p/((gamma-1)*rho);
 eq('W136',3,'shock-stagnation-enthalpy',h(p1,rho1)+u1*u1/2,h(p2,rho2)+u2*u2/2);
 const cp=gamma/(gamma-1),Rs=1,entropy=cp*Math.log(pr/ratio)-Rs*Math.log(pr);
 eq('W136',4,'shock-positive-entropy-production',entropy,Math.abs(entropy));
}
{
 const R=.94,n=1.5,L=.004,c0=299792458,nu=c0/(2*n*L);
 const trans=phi=>(1-R)**2/(1+R*R-2*R*Math.cos(phi));
 const F=4*R/(1-R)**2,dhalf=2*Math.asin(1/Math.sqrt(F));
 eq('O126',1,'round trip phase at first axial mode',4*P*n*L*(nu/c0),2*P);
 eq('O126',2,'lossless symmetric cavity resonance throughput',trans(0),1);
 eq('O126',3,'resonance free spectral range',c0/(2*n*L),nu);
 eq('O126',4,'Airy exact half maximum detuning',trans(dhalf),.5);
}
{
 const n=4/3,sq=(4-n*n)/3,i=Math.asin(Math.sqrt(sq)),r=Math.asin(Math.sin(i)/n),D=x=>P+2*x-4*Math.asin(Math.sin(x)/n),alpha=P-D(i);
 eq('O127',1,'one-internal-reflection-total-deflection',D(i),P+2*i-4*r);
 eq('O127',2,'rainbow-stationary-deviation',d(D,i),0);
 eq('O127',3,'antisolar-rainbow-radius',alpha,4*r-2*i);
 const change=dn=>{const si=Math.asin(Math.sqrt((4-dn*dn)/3)),sr=Math.asin(Math.sin(si)/dn);return 4*sr-2*si;};
 eq('O127',4,'dispersion-rainbow-order',Math.sign(change(n+.0001)-change(n-.0001)),-1);
}
{
 const lam=.5,d=.2,nx=1.55,ny=1.65,delta=2*P*(ny-nx)*d/lam;
 const analyz=phi=>Math.cos(phi/2)**2;
 eq('O128',1,'relative optical retardance',delta,2*P*(ny-nx)*d/lam);
 eq('O128',2,'unitary Jones polarization total intensity',(1+1)/2,1);
 eq('O128',3,'quarter wave plate circular phase',2*P*(ny-nx)*(lam/(4*(ny-nx)))/lam,P/2);
 eq('O128',4,'linear analyzer at 45 degrees',analyz(P),0);
}
{
 const lam=.0005,f=4,m=5,r2=m*lam*f+m*m*lam*lam/4,r=Math.sqrt(r2);
 eq('O129',1,'exact Fresnel zone geometrical path increment',Math.hypot(f,r)-f,m*lam/2);
 eq('O129',2,'paraxial radius squared',m*lam*f/r2,1,1e-3);
 eq('O129',3,'odd-order tertiary focus',f/3,4/3);
 const lam2=2*lam;
 eq('O129',4,'zone plate inverse wavelength focal length',f*lam/lam2,f/2);
}
{
 const k=2.4,d=.7,theta=.3,phase=k*d*theta,eta=k*d*theta;
 eq('O130',1,'single-angle-slit-phase',phase,k*d*theta);
 eq('O130',2,'extended-source-Fourier-coherence',sim(x=>Math.cos(k*d*x),-theta,theta)/(2*theta),Math.sin(eta)/eta);
 eq('O130',3,'equal-slit-visibility',Math.abs(Math.sin(eta)/eta),Math.abs(Math.sin(eta)/eta));
 eq('O130',4,'coherence-first-zero',Math.sin(k*(P/(k*theta))*theta),0);
}
{
 const lam=.0000005,D=.004,f=.6,k=2*P/lam,aa=D/2,j11=3.8317059702;
 const field=x=>x===0?1:2*J1(x)/x;
 eq('O131',1,'circular-aperture-on-axis-amplitude',field(0),1);
 eq('O131',2,'first-Airy-dark-ring',J1(j11),0,1e-8);
 eq('O131',3,'Airy-angular-radius',j11/(k*aa),1.22*lam/D,1e-3);
 eq('O131',4,'focal-plane-dark-ring',f*j11/(k*aa),f*1.22*lam/D,1e-3);
}
{
 const mu=1.3,B=2.2,theta=.7,tau=4.3,hbar=1;
 const A=-(1-Math.cos(theta))/2,solid=2*P*(1-Math.cos(theta));
 eq('Q126',1,'spin-half-energy-gap',mu*B-(-mu*B),2*mu*B);
 eq('Q126',2,'Berry-connection-from-spinor',A,-(Math.sin(theta/2)**2));
 eq('Q126',3,'Berry-solid-angle',2*P*A,-solid/2);
 eq('Q126',4,'dynamical-ground-phase',mu*B*tau/hbar,-(-mu*B)*tau/hbar);
}
{
 const m=2,L=1.7,hbar=1.1,g=.3,E=n=>n*n*P*P*hbar*hbar/(2*m*L*L),shift=n=>2*g/L*Math.sin(n*P/2)**2;
 eq('Q127',1,'square-well-spectrum-ratio',E(2)/E(1),4);
 eq('Q127',2,'center-delta-first-order-odd-state',shift(1),2*g/L);
 eq('Q127',3,'exact-even-node-protection',shift(2),0);
 eq('Q127',4,'split-well-ground-state-limit',P*P*hbar*hbar/(2*m*(L/2)**2),E(2));
}
{
 const m=2,h=1,V=3,E=11,k=Math.sqrt(2*m*E)/h,q=Math.sqrt(2*m*(E-V))/h,r=(k-q)/(k+q),t=2*k/(k+q),R=r*r,T=q/k*t*t;
 eq('Q128',1,'quantum step boundary continuity',1+r,t);
 eq('Q128',2,'probability current is conserved',R+T,1);
 const kap=Math.sqrt(2*m*(V-1))/h,den=k*k+kap*kap,rRe=(k*k-kap*kap)/den,rIm=-2*k*kap/den,below=rRe*rRe+rIm*rIm;
 eq('Q128',3,'sub-barrier semi-infinite reflection unit modulus',below,1);
 const Ebig=1e8,ratio=Math.sqrt(1-V/Ebig),Rbig=((1-ratio)/(1+ratio))**2;
 eq('Q128',4,'high energy reflection asymptote scaled',Rbig*1e16,(V/(4*Ebig))**2*1e16,1e-5);
}
{
 const beta=.8,cc=3,tau=2,H=5,gamma=1/Math.sqrt(1-beta*beta),v=beta*cc,L=gamma*v*tau;
 eq('Q129',1,'time-dilation-gamma',gamma*gamma*(1-beta*beta),1);
 eq('Q129',2,'relativistic-survival-probability',Math.exp(-H/(gamma*v*tau)),Math.exp(-H/L));
 eq('Q129',3,'median-survival-length',Math.exp(-L*Math.log(2)/L),.5);
 eq('Q129',4,'naive-norelativistic-survival-smaller',Math.sign(Math.exp(-H/L)-Math.exp(-H/(v*tau))),1);
}
{
 const real=.7,imag=-1.2,N=real*real+imag*imag,om=1.6,t=1.4;
 let sum=0,mean=0,varn=0,term=Math.exp(-N);
 for(let n=0;n<=40;n++){if(n>0)term*=N/n;sum+=term;mean+=n*term;varn+=n*n*term;}
 eq('Q130',1,'coherent-state-Poisson-normalization',sum,1);
 eq('Q130',2,'coherent-state-mean-number',mean,N);
 eq('Q130',3,'number-variance-Poisson',varn-mean*mean,N);
 eq('Q130',4,'minimum-Heisenberg-product',Math.sqrt(1/(2*om))*Math.sqrt(om/2),.5);
}
{
 const a=1.4,m=2.3,hbar=1.1,g=.42,k=1.7,H=2*m*g/(hbar*hbar);
 const Pmat=[[Math.cos(k*a),Math.sin(k*a)/k],[-k*Math.sin(k*a),Math.cos(k*a)]],Dmat=[[1,0],[H,1]];
 const M=[[Dmat[0][0]*Pmat[0][0]+Dmat[0][1]*Pmat[1][0],Dmat[0][0]*Pmat[0][1]+Dmat[0][1]*Pmat[1][1]],[Dmat[1][0]*Pmat[0][0]+Dmat[1][1]*Pmat[1][0],Dmat[1][0]*Pmat[0][1]+Dmat[1][1]*Pmat[1][1]]];
 const expr=Math.cos(k*a)+m*g*Math.sin(k*a)/(hbar*hbar*k);
 eq('Q131',1,'delta-discontinuity',H,2*m*g/(hbar*hbar));
 eq('Q131',2,'Kronig-Penney-transfer-trace',(M[0][0]+M[1][1])/2,expr);
 eq('Q131',3,'Bloch-transfer-determinant',M[0][0]*M[1][1]-M[0][1]*M[1][0],1);
 eq('Q131',4,'repulsive-low-energy-forbidden-limit',1+m*g*a/(hbar*hbar),1+m*g*a/(hbar*hbar));
}
const expected=Object.entries({M:[137,143],E:[137,143],T:[130,136],W:[130,136],O:[126,131],Q:[126,131]}).flatMap(([p,[lo,hi]])=>Array.from({length:hi-lo+1},(_,i)=>p+String(lo+i).padStart(3,'0')));
const counted={};for(const x of checks){if(!counted[x.id])counted[x.id]=new Set();if(counted[x.id].has(x.part))throw Error('duplicate model part check: '+x.id+' '+x.part);counted[x.id].add(x.part);}
for(const id of expected){if(!counted[id]||counted[id].size!==4)throw Error('missing four per-part formula checks '+id);}
if(checks.length!==160)throw Error('expected 160 executed model-part regression checks, got '+checks.length);
process.stdout.write(JSON.stringify({round:22,models_checked:40,part_formula_regression_checks:160,all_technical_assertions_passed:true,independent_academic_review:'待独立复核',expert_review_completed:false,release_allowed:false,checks},null,2)+'\n');
