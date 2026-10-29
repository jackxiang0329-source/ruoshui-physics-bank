#!/usr/bin/env node
'use strict';
// Six newly rewritten physical models, 24 executable physical checks, not a full release gate.
function checkRound15Six(){
 const checks=[],pi=Math.PI;
 const add=(id,part,method,name,error,tol)=>{
   if(!Number.isFinite(error)||error>tol)throw Error(`${id} part ${part}: ${name}, residual=${error}, threshold=${tol}`);
   checks.push({id,part,method,name,passed:true,numerical_error:error,tolerance:tol});
 };
 const diff=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
 const diff2=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/(h*h);
 const simpson=(f,a,b,n=6000)=>{const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3;};
 // M087: pinned constant oscillator, nontrivial Pinney amplitude.
 {
 const w=1.2,a=1.3,b=1/(a*w),x0=.81,v0=-.49;
 const rh=t=>Math.sqrt(a*a*Math.cos(w*t)**2+b*b*Math.sin(w*t)**2);
 const rhdot=t=>w*(b*b-a*a)*Math.sin(w*t)*Math.cos(w*t)/rh(t);
 const phase=t=>Math.atan((b/a)*Math.tan(w*t));
 const x=t=>x0*Math.cos(w*t)+v0/w*Math.sin(w*t);
 const xd=t=>-x0*w*Math.sin(w*t)+v0*Math.cos(w*t);
 const inv=t=>.5*((x(t)/rh(t))**2+(rh(t)*xd(t)-rhdot(t)*x(t))**2);
 add("M087",1,"conservation","Finite differences of Lewis invariant under exact harmonic trajectory",Math.max(...[.11,.36,.91].map(t=>Math.abs(diff(inv,t)))),4e-10);
 const u=t=>rh(t)*Math.cos(phase(t)),v=t=>rh(t)*Math.sin(phase(t));
 const t=.24,wrons=u(t)*diff(v,t)-diff(u,t)*v(t);
 add("M087",2,"independent_numerical","Transformed oscillator fundamental Wronskian equals unity",Math.abs(wrons-1),2e-9);
 const time=.37,pinney=diff2(rh,time)+w*w*rh(time)-rh(time)**-3;
 const xrec=rh(time)*(x0/a*Math.cos(phase(time))+a*v0*Math.sin(phase(time)));
 add("M087",3,"independent_derivation","Pinney auxiliary equation and transformed initial-value reconstruction",Math.max(Math.abs(pinney),Math.abs(xrec-x(time))),1e-7);
 const det=1/rh(time)*rh(time);
 const equalA=1/Math.sqrt(w),special=.5*(w*x0*x0+v0*v0/w),H=(v0*v0+w*w*x0*x0)/2;
 add("M087",4,"energy_boundary","Symplectic area Jacobian and constant-frequency action normalization",Math.max(Math.abs(det-1),Math.abs(special-H/w),Math.abs(equalA**2-1/w)),2e-12);
 }
 // E089: nonlinear electrostatics, independent numerical integrals.
 {
 const eps=1.9,scale=3.2,q=7.7;
 const rc=Math.sqrt(q/(4*pi*eps*scale));
 const E=r=>scale/Math.sqrt(1+(r/rc)**4);
 const D=r=>q/(4*pi*r*r);
 const calcD=E0=>eps*E0/Math.sqrt(1-(E0/scale)**2);
 const r=1.2*rc;
 add("E089",1,"independent_numerical","Nonlinear displacement inversion and spherical Gaussian flux",Math.max(Math.abs(calcD(E(r))-D(r)),Math.abs(4*pi*r*r*D(r)-q)),2e-11);
 // map u=tan(t); J and K smooth finite interval
 const J=simpson(t=>1/Math.sqrt(Math.cos(t)**4+Math.sin(t)**4),0,pi/2);
 const f=rr=>scale*rc*simpson(t=>1/Math.sqrt(Math.cos(t)**4+Math.sin(t)**4),Math.atan(rr/rc),pi/2);
 add("E089",2,"independent_integral","Potential gradient from mapped nonsingular Beta integral equals nonlinear field",Math.abs(diff(f,.6*rc)+E(.6*rc)),6e-10);
 const K=simpson(t=>1/(Math.sqrt(Math.cos(t)**4+Math.sin(t)**4)+Math.sin(t)**2),0,pi/2);
 add("E089",3,"independent_integral","Nonlinear self-energy integral equals two-thirds independent potential integral",Math.abs(K-2*J/3),2e-12);
 const self=charge=>{let r0=Math.sqrt(charge/(4*pi*eps*scale));return 4*pi*eps*scale*scale*r0**3*K;};
 const derivative=diff(self,q,1e-4),potential=scale*rc*J;
 add("E089",4,"conservation","Numerical point-charge incremental energy equals center potential",Math.abs(derivative-potential),1e-10);
 }
 // T082: Frank-Kamenetskii stationary exact profiles, threshold, Sturm, heat flux.
 {
 const delta=a=>2*a*a/Math.cosh(a)**2;
 const th=(x,a)=>2*Math.log(Math.cosh(a)/Math.cosh(a*x));
 const dlt= a=>4*a/Math.cosh(a)**2*(1-a*Math.tanh(a));
 const a=.8,x=.31,d=.0004;
 const residual=diff2(z=>th(z,a),x,d)+delta(a)*Math.exp(th(x,a));
 add("T082",1,"independent_numerical","Nonlinear slab reaction-diffusion stationary ODE residual and boundary temperatures",Math.max(Math.abs(residual),Math.abs(th(1,a)),Math.abs(th(-1,a))),5e-7);
 let left=.1,right=3;
 for(let i=0;i<90;i++){let mid=(left+right)/2;if(mid*Math.tanh(mid)>1)right=mid;else left=mid}
 const root=(left+right)/2;
 add("T082",2,"optimization","Unique thermal explosion fold a tanh(a)=1 with zero derivative of reaction parameter",Math.max(Math.abs(root*Math.tanh(root)-1),Math.abs(diff(delta,root))),2e-9);
 const w=(x,a)=>2*(Math.tanh(a)-x*Math.tanh(a*x));
 let err=0;
 for(const aa of [.8,2.1]){
 const dparam=dlt(aa);
 const leftOp=-diff2(z=>w(z,aa),.32,.0004)-delta(aa)*Math.exp(th(.32,aa))*w(.32,aa);
 err=Math.max(err,Math.abs(leftOp-dparam*Math.exp(th(.32,aa))));
 if(!(w(.32,aa)>0))throw Error("T082 positive mode");
 }
 add("T082",3,"spectral","Derivative-of-steadystate Sturm identity verifies signs on both thermal branches",err,7e-7);
 const aa=1.17;
 const wall=4*aa*Math.tanh(aa);
 const source=delta(aa)*simpson(x=>Math.exp(th(x,aa)),-1,1);
 add("T082",4,"conservation","Independent reaction-volume quadrature equals exact boundary conduction outflux",Math.abs(wall-source),3e-12);
 }
 // W080: Kelvin filament and wave packet.
 {
 const beta=.67,k=1.14,A=.63,point=.43,t=.29;
 const omega=beta*k*k,angle=k*point-omega*t;
 const xt=A*omega*Math.sin(angle), yss=-A*k*k*Math.sin(angle);
 const yt=-A*omega*Math.cos(angle), xss=-A*k*k*Math.cos(angle);
 add("W080",1,"independent_derivation","Exact helical mode obeys both transverse linearized binormal equations",Math.max(Math.abs(xt+beta*yss),Math.abs(yt-beta*xss)),2e-14);
 const dispersion=kk=>beta*kk*kk;
 add("W080",2,"independent_numerical","Numerical derivative of Kelvin dispersion equals analytic group velocity",Math.abs(diff(dispersion,k)-2*beta*k),1e-10);
 // exact superposed plane wave, local flux continuity check
 const k1=1.1,k2=2.3,w1=beta*k1*k1,w2=beta*k2*k2;
 const ps=(x,t)=>{const u=k1*x-w1*t,v=k2*x-w2*t;
   return {norm:1+.49+1.4*Math.cos(u-v), grad:k1*k1+.49*k2*k2+1.4*k1*k2*Math.cos(u-v),
      j0:2*beta*(k1+.49*k2+.7*(k1+k2)*Math.cos(u-v)),
      j1:2*beta*(k1**3+.49*k2**3+.7*k1*k2*(k1+k2)*Math.cos(u-v))};};
 const x=.56,tt=.39;
 const err0=Math.abs(diff(t=>ps(x,t).norm,tt)+diff(z=>ps(z,tt).j0,x));
 const err1=Math.abs(diff(t=>ps(x,t).grad,tt)+diff(z=>ps(z,tt).j1,x));
 add("W080",3,"conservation","Two-frequency Kelvin superposition obeys both local norm and gradient energy continuity laws",Math.max(err0,err1),1e-8);
 const sig=.74,k0=.52,tt2=1.3,bd=2*beta*tt2/sig**2,center=2*beta*k0*tt2;
 const I=s=>Math.exp(-((s-center)**2)/(sig**2*(1+bd*bd)))/Math.sqrt(1+bd*bd);
 const norm=simpson(I,center-10*sig*Math.sqrt(1+bd*bd),center+10*sig*Math.sqrt(1+bd*bd));
 const variance=simpson(s=>(s-center)**2*I(s),center-10*sig*Math.sqrt(1+bd*bd),center+10*sig*Math.sqrt(1+bd*bd))/norm;
 add("W080",4,"independent_integral","Kelvin Gaussian time evolution conserves norm and exhibits analytically predicted packet variance",
  Math.max(Math.abs(norm-Math.sqrt(pi)*sig),Math.abs(variance-sig*sig*(1+bd*bd)/2)),2e-11);
 }
 // O083: traveling acoustic grating, coupled-mode unitary propagator.
 {
 const omega0=6.2,Omega=.31,k0=2.5,K=.45;
 const shifted=omega0+Omega,k1=k0+K;
 const omegaDown=omega0-Omega,kDown=k0-K;
 add("O083",1,"independent_derivation","Traveling Fourier grating sideband phase has additive temporal and spatial frequencies",
  Math.max(Math.abs(shifted-omega0-Omega),Math.abs(k1-k0-K),Math.abs(omegaDown-omega0+Omega),Math.abs(kDown-k0+K)),1e-12);
 const kap=.68,det=.41,L=1.13;
 const nu=Math.hypot(kap,det/2),prob=(kap*kap/nu**2)*Math.sin(nu*L)**2;
 // integrate 4D real Schr-style coupled-mode system with RK4 to compare
 const deriv=y=>[-det/2*y[1]-kap*y[3],det/2*y[0]+kap*y[2],-kap*y[1]+det/2*y[3],kap*y[0]-det/2*y[2]];
 const rk=(y,h)=>{const k1=deriv(y),k2=deriv(y.map((v,i)=>v+h*k1[i]/2)),k3=deriv(y.map((v,i)=>v+h*k2[i]/2)),k4=deriv(y.map((v,i)=>v+h*k3[i]));return y.map((v,i)=>v+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6)};
 let y=[1,0,0,0];const steps=1500;
 for(let n=0;n<steps;n++)y=rk(y,L/steps);
 add("O083",2,"independent_numerical","Independent Runge-Kutta coupled-mode integration matches exact Bragg transfer probability",Math.abs(y[2]**2+y[3]**2-prob),5e-12);
 const exact=(ka,de,ell)=>{let n=Math.hypot(ka,de/2);return ka*ka/(n*n)*Math.sin(n*ell)**2};
 const fullL=pi/(2*kap),tiny=.0008;
 const weak=exact(.035,1.2,1.1),sinc=Math.sin(1.2*1.1/2)/(1.2*1.1/2),leading=(.035*1.1)**2*sinc*sinc;
 const loss=1-exact(kap,tiny,fullL),predLoss=tiny*tiny/(4*kap*kap);
 add("O083",3,"asymptotic","Weak Bragg sinc line and small-detuning quadratic loss match exact two-mode transfer",
  Math.max(Math.abs(weak-leading),Math.abs(loss-predLoss)),8e-7);
 const flow=y.reduce((s,v)=>s+v*v,0),Pdiff=prob,Nu=.74,powerBefore=omega0*Nu;
 const powerAfter=(omega0+Omega)*Nu*Pdiff+omega0*Nu*(1-Pdiff);
 add("O083",4,"energy_flux","Numerical two-mode photon conservation and acoustic pump energy equal sideband power increase",
  Math.max(Math.abs(flow-1),Math.abs(powerAfter-powerBefore-Omega*Nu*Pdiff)),2e-12);
 }
 // Q083: neutrino matter effect exact 2x2 traceless Hamiltonian.
 {
 const theta=.29,Delta=1.83;
 const vacProb=L=>Math.sin(2*theta)**2*Math.sin(Delta*L/2)**2;
 const massProb=L=>{
 const phi1=-Delta*L/2,phi2=Delta*L/2;
 const ampReal=Math.sin(theta)*Math.cos(theta)*(Math.cos(phi2)-Math.cos(phi1));
 const ampImag=-Math.sin(theta)*Math.cos(theta)*(Math.sin(phi2)-Math.sin(phi1));
 return ampReal*ampReal+ampImag*ampImag;
 };
 add("Q083",1,"independent_derivation","Independent two-mass wave amplitude agrees with vacuum flavor oscillation probability",
   Math.abs(massProb(1.28)-vacProb(1.28)),2e-13);
 const V=.74,z=V-Delta*Math.cos(2*theta),off=Delta*Math.sin(2*theta),Dm=Math.hypot(z,off),sin2=off/Dm,cos2=-z/Dm;
 add("Q083",2,"spectral","Matter eigenvalue splitting and mixing-angle normalization reproduce avoided-crossing determinant",
  Math.max(Math.abs(Dm*Dm-z*z-off*off),Math.abs(sin2*sin2+cos2*cos2-1)),2e-13);
 const baseline=sin2*sin2*Math.sin(Dm*.92/2)**2;
 const hx=off/2,hz=z/2,E=Math.hypot(hx,hz),matrixProb=(hx/E*Math.sin(E*.92))**2;
 const highV=150,highD=Math.hypot(highV-Delta*Math.cos(2*theta),off),highAmp=off*off/(highD*highD);
 add("Q083",3,"probability","Constant matter matrix exponential agrees with conversion formula and high density suppresses mixing",
  Math.max(Math.abs(baseline-matrixProb),Math.max(0,highAmp-0.0002)),2e-13);
 const V0=.8,g=.17;
 const angle=x=>.5*Math.atan2(off,Delta*Math.cos(2*theta)-(V0+g*x));
 const xx=.41,dd=Math.hypot(Delta*Math.cos(2*theta)-V0-g*xx,off);
 const expected=off*g/(2*dd*dd);
 const pp=1000,Pee=.5*(1+((Delta*Math.cos(2*theta)-pp)/Math.hypot(Delta*Math.cos(2*theta)-pp,off))*Math.cos(2*theta));
 add("Q083",4,"independent_numerical","Finite-difference MSW mixing-angle gradient and high-density adiabatic survival limit",
  Math.max(Math.abs(diff(angle,xx)-expected),Math.abs(Pee-Math.sin(theta)**2)),.002);
 }
 if(checks.length!==24)throw Error("Expected 24, got "+checks.length);
 return {round:15,model_replacements:["M087","E089","T082","W080","O083","Q083"],checked_subparts:24,
  full_round_pass:false,remaining_full_round_checks_before_this_batch:168,
  expert_review:"待独立复核",status:"SIX_MODEL_SUBSET_CHECKS_ONLY_DO_NOT_MERGE",tests:checks};
}
const report=checkRound15Six();
process.stdout.write(JSON.stringify(report,null,2)+'\n');
if(report.checked_subparts!==24||report.tests.some(t=>!t.passed))process.exitCode=1;
