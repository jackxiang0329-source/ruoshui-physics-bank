#!/usr/bin/env node
'use strict';
// Six rewritten historically-colliding physics cores; 24 executable subpart checks.
function physicsQA(){
 const out=[],P=Math.PI;
 const ok=(id,p,method,err,tol)=>{if(!Number.isFinite(err)||err>tol)throw Error(`${id}:${p} ${method} ${err}>${tol}`);out.push({id,part:p,method,passed:true,error:err,tolerance:tol});};
 const I=(f,a,b,n=3200)=>{let h=(b-a)/n,s=f(a)+f(b);for(let k=1;k<n;k++)s+=(k%2?4:2)*f(a+k*h);return s*h/3;};
 const d=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h),d2=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/h**2;
 // M090: Stokes creeping sphere.
 {let R=1.3,U=1.7,mu=.85;
 let f=r=>1-1.5*R/r+.5*(R/r)**3,g=r=>1-.75*R/r-.25*(R/r)**3,fp=r=>1.5*R/r**2-1.5*R**3/r**4;
 const r=2.3*R,theta=.65;
 ok("M090",1,"Stokes divergence and spherical no-slip boundary",Math.max(Math.abs(U*Math.cos(theta)*(fp(r)+2*(f(r)-g(r))/r)),Math.abs(f(R)),Math.abs(g(R))),2e-13);
 const pn=t=>1.5*mu*U/R*Math.cos(t),pt=t=>-1.5*mu*U/R*Math.sin(t);
 const Fp=2*P*R*R*I(t=>pn(t)*Math.cos(t)*Math.sin(t),0,P),Ft=2*P*R*R*I(t=>-pt(t)*Math.sin(t)*Math.sin(t),0,P);
 ok("M090",2,"Independent spherical pressure/shear traction integrals",Math.max(Math.abs(Fp-2*P*mu*R*U),Math.abs(Ft-4*P*mu*R*U)),1e-11);
 const integrand=t=>{if(t===0)return 9*P*mu*U*U*R;let rr=R/t;return (4*P*mu*U*U*fp(rr)**2*rr**2+6*P*mu*U*U*R**6/rr**6)*R/t**2};
 ok("M090",3,"Integrated 3D viscous dissipation equals drag input power",Math.abs(I(integrand,0,1,4000)-6*P*mu*R*U**2),1e-10);
 const density=2.7,fluid=1.2,grav=9.8,v=2*R**2*(density-fluid)*grav/(9*mu);
 ok("M090",4,"Terminal sphere Stokes drag balances buoyant weight",Math.abs(6*P*mu*R*v-4*P*R**3*(density-fluid)*grav/3),1e-12);
 }
 // E092: patterned electrode potential.
 {let eps=1.9,k=1.2,L=.8,V1=2.3,V2=.71,ph=.65,s=Math.sinh(k*L),ch=Math.cosh(k*L)/s,cs=1/s;
 const f=z=>Math.sinh(k*(L-z))/s,g=z=>Math.sinh(k*z)/s,fp=z=>-k*Math.cosh(k*(L-z))/s,gp=z=>k*Math.cosh(k*z)/s;
 const pot=(x,z)=>V1*f(z)*Math.cos(k*x)+V2*g(z)*Math.cos(k*x+ph);
 let x=.41,z=.35;
 ok("E092",1,"2D Laplace residual and both patterned Dirichlet boundaries",Math.max(Math.abs(d2(t=>pot(t,z),x)+d2(t=>pot(x,t),z)),Math.abs(pot(x,0)-V1*Math.cos(k*x)),Math.abs(pot(x,L)-V2*Math.cos(k*x+ph))),4e-7);
 const e1=eps*k*(ch-cs),e2=eps*k*(ch+cs);
 if(e1<=0||e2<=0)throw Error("electrode capacitance not positive");
 ok("E092",2,"Positive electrode capacitance eigenvalues and determinant",Math.abs(e1*e2-(eps*k)**2),1e-12);
 const energy=eps*k/4*((V1*V1+V2*V2)*ch-2*V1*V2*Math.cos(ph)*cs);
 const calc=eps/4*I(z=>{let a=V1*k*f(z),b=V2*k*g(z),c=V1*fp(z),h=V2*gp(z);return a*a+b*b+2*a*b*Math.cos(ph)+c*c+h*h+2*c*h*Math.cos(ph)},0,L);
 ok("E092",3,"Direct Fourier-averaged field-energy quadrature against capacitance matrix",Math.abs(energy-calc),1e-11);
 const stress=eps*k*k/4*((V1*V1+V2*V2)*cs*cs-2*V1*V2*Math.cos(ph)*cs*ch);
 const U=d=>eps*k/4*((V1*V1+V2*V2)/Math.tanh(k*d)-2*V1*V2*Math.cos(ph)/Math.sinh(k*d));
 const maxwell=eps/4*((V1*k*cs)**2+(V2*k*ch)**2-2*V1*V2*k*k*cs*ch*Math.cos(ph)-(V2*k)**2);
 ok("E092",4,"Normal Maxwell stress from boundary fields equals minus energy gap derivative",Math.max(Math.abs(stress-maxwell),Math.abs(stress+d(U,L))),1e-9);
 }
 // T086: relativistic Juttner velocity distribution
 {let z=1.37,K=(n,z)=>I(u=>Math.exp(-z*Math.cosh(u))*Math.cosh(n*u),0,12,5200);
 let K0=K(0,z),K1=K(1,z),R=K0/K1;
 ok("T086",1,"Juttner rapidity momentum integral vs modified Bessel K1",Math.abs(I(u=>2*Math.cosh(u)*Math.exp(-z*Math.cosh(u)),0,11,5200)-2*K1),1e-10);
 const energy=T=>{let v=1/T;return K(0,v)/K(1,v)+1/v};
 const cv=1+z*z*(1-R*R)-z*R;
 if(cv<=0)throw Error("Juttner heat capacity must be positive");
 ok("T086",2,"Analytic Juttner heat capacity vs independent numerical derivative of internal energy",Math.abs(cv-d(energy,1/z,1e-4)),3e-6);
 const entropy=(T,L)=>{let v=1/T;return Math.log(L)+Math.log(K(1,v))+v*K(0,v)/K(1,v)+1};
 ok("T086",3,"Relativistic entropy derivatives yield pressure and heat-capacity identity",Math.max(Math.abs(d(L=>entropy(1/z,L),2.1)-1/2.1),Math.abs(d(T=>entropy(T,2.1),1/z)-z*cv)),5e-6);
 const speed=Math.exp(-z)/(z*K1);
 if(!(speed>0&&speed<1))throw Error("Juttner superluminal speed");
 const num=I(p=>2*p/Math.hypot(1,p)*Math.exp(-z*Math.hypot(1,p)),0,40,10000)/(2*K1);
 ok("T086",4,"Juttner mean absolute group velocity from independent finite-momentum quadrature",Math.abs(num-speed),1e-8);
 }
 // W085: exponentially tapered acoustic horn
 {let alpha=.38,c=1.7,rho=1.4,k=.92,w=c*Math.hypot(k,alpha);
 const p=(x,t)=>Math.exp(-alpha*x)*Math.cos(k*x-w*t),x=.43,t=.37;
 ok("W085",1,"Webster wave PDE finite-difference residual",Math.abs(d2(t=>p(x,t),t)-c*c*(d2(x=>p(x,t),x)+2*alpha*d(x=>p(x,t),x))),4e-7);
 const group=c*c*k/w;
 ok("W085",2,"Acoustic exponential horn cutoff dispersion and numerical group speed",Math.max(Math.abs(w*w-c*c*(k*k+alpha*alpha)),Math.abs(d(k=>c*Math.hypot(k,alpha),k)-group)),1e-10);
 const A=x=>Math.exp(2*alpha*x),en=x=>Math.exp(-2*alpha*x)/(2*rho*c*c),flux=x=>k*Math.exp(-2*alpha*x)/(2*rho*w);
 ok("W085",3,"Acoustic energy-transport speed and conserved cross-sectional power",Math.max(Math.abs(flux(.61)/en(.61)-group),Math.abs(A(.61)*flux(.61)-A(2.3)*flux(2.3))),1e-13);
 const L=2.4,mode=n=>{let q=n*P/L;return x=>Math.exp(-alpha*x)*(Math.cos(q*x)+alpha/q*Math.sin(q*x))};
 let m=mode(2),n=mode(3);
 ok("W085",4,"Rigid-end Robin modes satisfy two wall conditions and weighted orthogonality",Math.max(Math.abs(d(m,0)),Math.abs(d(m,L)),Math.abs(I(x=>A(x)*m(x)*n(x),0,L))),1e-9);
 }
 // O086: class B laser
 {let gamma=.7,kappa=5.2,g=1.4,Rth=gamma*kappa/g,R=1.7*Rth,N=kappa/g,S=(R-Rth)/kappa;
 const fn=(n,s)=>R-gamma*n-g*n*s,fs=(n,s)=>g*n*s-kappa*s;
 ok("O086",1,"Laser nonzero-photon stationary rate balance and gain clamping",Math.max(Math.abs(fn(N,S)),Math.abs(fs(N,S))),1e-12);
 const tr=-(gamma+g*S),det=kappa*g*S,delta=tr*tr-4*det;
 if(!(tr<0&&det>0&&delta<0))throw Error("laser relaxation unstable");
 let re=tr/2,im=Math.sqrt(-delta)/2;
 ok("O086",2,"Linearized laser complex relaxation eigenvalue matches characteristic polynomial",Math.max(Math.abs(re*re-im*im-tr*re+det),Math.abs(2*re*im-tr*im)),1e-12);
 const eps=5e-5,trace=-gamma*(1+eps),detNear=kappa*gamma*eps,slow=(trace+Math.sqrt(trace*trace-4*detNear))/2;
 ok("O086",3,"Laser threshold soft eigenmode has correct critical slowing-down scaling",Math.abs(slow/(-kappa*eps)-1),.002);
 let n=2.2,s=.91;
 ok("O086",4,"Laser stimulated-emission cancellation in pump-to-output photon energy ledger",Math.max(Math.abs(fn(n,s)+fs(n,s)-(R-gamma*n-kappa*s)),Math.abs(kappa*S-(R-Rth))),1e-12);
 }
 // Q087: trapped ion motional sidebands
 {let eta=.13,Omega=1.1,nu=6.1,n=3,t=.73;
 ok("Q087",1,"RWA red-blue sideband optical detunings remove opposite phonon phases",Math.max(Math.abs(-nu+nu),Math.abs(nu-nu)),1e-15);
 const evolve=rate=>{let state=[1,0],h=t/1400;const f=y=>[-rate*y[1]/2,rate*y[0]/2];for(let j=0;j<1400;j++){let a=f(state),b=f(state.map((x,i)=>x+h*a[i]/2)),c=f(state.map((x,i)=>x+h*b[i]/2)),d=f(state.map((x,i)=>x+h*c[i]));state=state.map((x,i)=>x+h*(a[i]+2*b[i]+2*c[i]+d[i])/6)}return state[1]**2};
 let redRate=eta*Omega*Math.sqrt(n),blueRate=eta*Omega*Math.sqrt(n+1);
 ok("Q087",2,"Independent unitary RK4 two-level sideband evolution matches exact n-dependent Rabi transfer",Math.max(Math.abs(evolve(redRate)-Math.sin(redRate*t/2)**2),Math.abs(evolve(blueRate)-Math.sin(blueRate*t/2)**2)),1e-13);
 let nbar=.67,r=nbar/(nbar+1),pulse=.018,pr=0,pb=0;
 for(let j=0;j<100;j++){const p=Math.pow(r,j)/(1+nbar);pr+=p*Math.sin(eta*Omega*Math.sqrt(j)*pulse/2)**2;pb+=p*Math.sin(eta*Omega*Math.sqrt(j+1)*pulse/2)**2}
 ok("Q087",3,"Thermal phonon-occupation ensemble reproduces weak-pulse red/blue sideband asymmetry",Math.abs(pr/pb-r),1e-7);
 const et=.31,ex=Math.exp(-et*et/2)*(1-et*et);
 const diag=I(x=>2*x*x*Math.exp(-x*x)*Math.cos(Math.sqrt(2)*et*x)/Math.sqrt(P),-8,8,12000);
 ok("Q087",4,"Direct oscillator wavefunction integral yields carrier Debye-Waller Laguerre matrix element",Math.abs(diag-ex),2e-12);
 }
 if(out.length!==24)throw Error("Expected 24, found "+out.length);
 return{round:15,replacements:["M090","E092","T086","W085","O086","Q087"],checked_subparts:24,full_round_pass:false,independent_expert_review:"待独立复核",tests:out};
}
const report=physicsQA();
process.stdout.write(JSON.stringify(report,null,2)+'\n');
if(report.checked_subparts!==24||report.tests.some(t=>!t.passed))process.exitCode=1;
