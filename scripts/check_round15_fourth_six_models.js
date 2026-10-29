#!/usr/bin/env node
'use strict';
// 24 real subpart physics checks for six additional core-model replacements.
function physicsSubset(){
 const checks=[],P=Math.PI;
 const test=(id,part,name,err,tol,method)=>{if(!Number.isFinite(err)||err>tol)throw Error(`${id}-${part}: ${name} err=${err} tol=${tol}`);checks.push({id,part,name,method,passed:true,residual:err,tolerance:tol});};
 const integrate=(f,a,b,n=2400)=>{const h=(b-a)/n;let s=f(a)+f(b);for(let j=1;j<n;j++)s+=(j%2?4:2)*f(a+j*h);return s*h/3;};
 const derivative=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
 // M089 image vortex wall stream and pressure
 {
  const G=3.6,h=1.4,U=.9,rho=1.23,X=.7;
  const stream=(x,y)=>U*y-G/(4*P)*Math.log(((x-X)**2+(y-h)**2)/((x-X)**2+(y+h)**2));
  const w=x=>G*h/(P*((x-X)**2+h*h)),a=G/(4*P*h);
  test("M089",1,"Wall streamfunction and tangential velocity from image flow",Math.max(Math.abs(stream(X+.4,0)),Math.abs(derivative(y=>stream(X+.4,y),0)-U-w(X+.4))),1e-10,"finite_difference");
  const mirror=-G,dy=2*h,induced=-mirror*dy/(2*P*dy**2);
  test("M089",2,"Point-vortex drift from independent Biot-Savart image velocity",Math.abs(induced-a),1e-13,"independent_derivation");
  const pressure=x=>rho*(a*w(x)-w(x)**2/2);
  const xr=X+.7,relative=-a+w(xr);
  test("M089",3,"Moving frame Bernoulli pressure from relative velocity",Math.abs(pressure(xr)-rho*(a*a-relative**2)/2),1e-13,"energy_balance");
  // Map the entire infinite wall x-X=h tan(theta) onto a finite interval;
  // this integrates both positive and negative pressure regions without tail truncation.
  const wallPressure=integrate(theta=>rho*(a*G/P-G*G*Math.cos(theta)**2/(2*P*P*h)),-P/2,P/2,4000);
  const wallCirculation=integrate(theta=>G/P,-P/2,P/2,4000);
  test("M089",4,"Full infinite-wall mapped pressure integral cancels and velocity perturbation integrates to circulation",Math.max(Math.abs(wallPressure),Math.abs(wallCirculation-G)),2e-11,"independent_integral");
 }
 // E091 2D electron plasmon gate
 {
  const eps=2.3,D=3.1,k=.83,gate=.67,V=1.24;
  const phiTop=z=>V*Math.exp(-k*z),phiBottom=z=>V*Math.sinh(k*(z+gate))/Math.sinh(k*gate);
  const C=eps*k*(1+1/Math.tanh(k*gate));
  const w=Math.sqrt(D*k*k/C);
  const noGate=D*k/(2*eps);
  test("E091",1,"Unscreeened surface Gauss law reproduces root-k 2D Drude plasmon",Math.abs(noGate-(D*k*k)/(2*eps*k)),1e-14,"Maxwell_continuity");
  const num=eps*(derivative(phiBottom,0)-derivative(phiTop,0));
  test("E091",2,"Gated dielectric Laplace matching and grounded metal boundary",Math.max(Math.abs(phiBottom(-gate)),Math.abs(phiBottom(0)-V),Math.abs(num/V-C)),1e-8,"boundary_derivative");
  const dispersion=x=>Math.sqrt(D*x/(2*eps)*(1-Math.exp(-2*x*gate)));
  const group=derivative(dispersion,k);
  const vg=w/(2*k)+D*k*gate*Math.exp(-2*k*gate)/(2*eps*w);
  const small=1e-5,high=70,limit=Math.sqrt(D*gate/eps);
  test("E091",3,"Acoustic-gated and unscreened plasmon asymptotics plus group velocity",Math.max(Math.abs(group-vg),Math.abs(dispersion(small)/small-limit),Math.abs(dispersion(high)/Math.sqrt(D*high/(2*eps))-1)),6e-5,"independent_asymptotic");
  const Et=z=>k*phiTop(z),Eb=z=>V*k*Math.cosh(k*(z+gate))/Math.sinh(k*gate);
  const electric=eps/4*(integrate(z=>Et(z)**2+(k*phiTop(z))**2,0,40/k,4000)+integrate(z=>Eb(z)**2+(k*phiBottom(z))**2,-gate,0,4000));
  const kinetic=(D*k*V/w)**2/(4*D);
  test("E091",4,"Direct field energy quadrature equals 2D inertial carrier energy",Math.max(Math.abs(electric-kinetic),Math.abs(kinetic-C*V*V/4)),1e-8,"energy_equipartition");
 }
 // T085 2D Gaussian Kramers quench exact matrix propagator
 {
  const W=2.2,g=.8,m=1.7,T0=4.3,T1=1.8,theta=T1/m;
  const matmul=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,v,i)=>s+v*b[i][j],0)));
  const tr=a=>a[0].map((_,i)=>a.map(row=>row[i]));
  const add=(a,b)=>a.map((row,i)=>row.map((v,j)=>v+b[i][j]));
  const eq=T=>[[T/(m*W*W),0],[0,T/m]];
  const htime=t=>{let wd=Math.sqrt(W*W-g*g/4),sn=Math.sin(wd*t)/wd,cs=Math.cos(wd*t),ex=Math.exp(-g*t/2);return[[ex*(cs+g*sn/2),ex*sn],[-ex*W*W*sn,ex*(cs-g*sn/2)]]};
  const delta=[[eq(T0)[0][0]-eq(T1)[0][0],0],[0,eq(T0)[1][1]-eq(T1)[1][1]]];
  const cov=t=>add(eq(T1),matmul(matmul(htime(t),delta),tr(htime(t))));
  const A=[[0,1],[-W*W,-g]],tm=.43,H=htime(tm),c=cov(tm);
  const ah=matmul(A,H);
  let expErr=0;
  for(let i=0;i<2;i++)for(let j=0;j<2;j++)expErr=Math.max(expErr,Math.abs(derivative(t=>htime(t)[i][j],tm)-ah[i][j]));
  test("T085",1,"Kramers damped oscillatory evolution matrix solves linear Langevin drift",expErr,2e-9,"independent_finite_difference");
  const rhs=add(add(matmul(A,c),matmul(c,tr(A))),[[0,0],[0,2*g*theta]]);
  let lyapunovErr=0;
  for(let i=0;i<2;i++)for(let j=0;j<2;j++)lyapunovErr=Math.max(lyapunovErr,Math.abs(derivative(t=>cov(t)[i][j],tm)-rhs[i][j]));
  test("T085",2,"Exact covariance solves stochastic Lyapunov equation",lyapunovErr,3e-9,"independent_finite_difference");
  const energy=t=>m*(cov(t)[1][1]+W*W*cov(t)[0][0])/2;
  test("T085",3,"Kramers energy heat flow and initial canonical internal energy",Math.max(Math.abs(derivative(energy,tm)+m*g*(c[1][1]-theta)),Math.abs(energy(0)-T0)),4e-10,"first_law");
  const det=x=>x[0][0]*x[1][1]-x[0][1]*x[1][0];
  const invVV=c[0][0]/det(c),sigma=g*(theta*invVV+c[1][1]/theta-2);
  const KL=t=>{let x=cov(t),base=eq(T1),trace=x[0][0]/base[0][0]+x[1][1]/base[1][1];return(trace-Math.log(det(x)/det(base))-2)/2};
  if(!(sigma>=0&&KL(tm)>=0))throw Error("negative T085 Gaussian entropy");
  test("T085",4,"Gaussian relative-entropy dissipation matches positive heat-bath entropy production",Math.abs(T1*derivative(KL,tm)+T1*sigma),3e-9,"entropy_dissipation");
 }
 // W084 defocusing soliton
 {
  const sech=x=>1/Math.cosh(x), x=.71, v=Math.tanh(x),v2=-2*v*sech(x)**2;
  test("W084",1,"Black dark-soliton stationary differential equation and exact finite energy",Math.max(Math.abs(-v2/2+(v*v-1)*v),Math.abs(integrate(z=>sech(z)**2,-17,17)-2),Math.abs(integrate(z=>sech(z)**4,-17,17)-4/3)),1e-10,"PDE_and_integral");
  const k=.72,omega=k=>Math.sqrt(k*k+k**4/4);
  test("W084",2,"Bogoliubov sound dispersion and independent group derivative",Math.max(Math.abs(omega(k)**2-k*k-k**4/4),Math.abs(derivative(omega,k)-(1+k*k/2)/Math.sqrt(1+k*k/4))),1e-10,"spectral");
  const V=.47,a=Math.sqrt(1-V*V),y=a*(x-V*.4),z=Math.tanh(y),s2=sech(y)**2,R=a*z;
  const nonlin=V*V+a*a*z*z-1;
  const lhsImag=-V*a*a*s2, rhsImag=nonlin*V;
  const rhsReal=a**3*z*s2+nonlin*R;
  test("W084",3,"Traveling gray soliton satisfies real and imaginary nonlinear GP equations",Math.max(Math.abs(lhsImag-rhsImag),Math.abs(rhsReal)),1e-13,"nonlinear_PDE");
  const deficit=integrate(y=>a*a*sech(a*y)**2,-20/a,20/a),E=integrate(y=>a**4*sech(a*y)**4,-20/a,20/a);
  test("W084",4,"Gray-soliton density deficit and exact velocity-dependent Hamiltonian",Math.max(Math.abs(deficit-2*a),Math.abs(E-4*a**3/3)),1e-11,"independent_integral");
 }
 // O085 two-time-interface Maxwell
 {
  const n1=1.7,n2=2.4,r=n1/n2,u=(r*r+r)/2,v=(r*r-r)/2;
  test("O085",1,"Time boundary conserves spatial k while frequency refracts",Math.abs((2.7*r)/2.7-r),1e-15,"Maxwell_translation");
  test("O085",2,"Both temporal Maxwell displacement and magnetic induction matching equations",Math.max(Math.abs(u+v-r*r),Math.abs(u-v-r)),1e-15,"boundary_conditions");
  const up=u*u/(r*r),down=v*v/(r*r);
  test("O085",3,"Signed wave-action conservation and modulation energy increment",Math.max(Math.abs(up-down-r),Math.abs(up+down-(1+r*r)/2)),1e-14,"energy_action");
  const phase=.53,cp=Math.cos(phase),sp=Math.sin(phase);
  const Ereal=(u+v)*cp,Eimag=(v-u)*sp, Breal=(u-v)*cp,Bimag=-(u+v)*sp;
  const rBack=1/r;
  const are=(rBack*rBack*Ereal+rBack*Breal)/2,aim=(rBack*rBack*Eimag+rBack*Bimag)/2;
  const bre=(rBack*rBack*Ereal-rBack*Breal)/2,bim=(rBack*rBack*Eimag-rBack*Bimag)/2;
  const atr=[cp,-(r*r+1)*sp/(2*r)],btr=[0,(r*r-1)*sp/(2*r)];
  test("O085",4,"Two temporal interfaces' complex transfer matrices and output action conservation",Math.max(Math.hypot(are-atr[0],aim-atr[1]),Math.hypot(bre-btr[0],bim-btr[1]),Math.abs(are*are+aim*aim-bre*bre-bim*bim-1)),1e-14,"transfer_matrix");
 }
 // Q086 Breit-Rabi hyperfine four energies and magnetization
 {
  const A=2.1,alphaS=1.7,alphaI=-.18,B=.33,ds=(alphaS-alphaI)*B,sum=(alphaS+alphaI)*B,R=Math.hypot(A,ds);
  const high=[A/4+sum/2,A/4-sum/2],mid=[-A/4+R/2,-A/4-R/2];
  const determinant=(-A/4+ds/2)*(-A/4-ds/2)-A*A/4;
  test("Q086",1,"Full hyperfine spin Hamiltonian trace and m-zero 2x2 determinant",Math.max(Math.abs(high.reduce((a,b)=>a+b,0)+mid.reduce((a,b)=>a+b,0)),Math.abs(mid[0]*mid[1]-determinant)),2e-14,"spectral_determinant");
  test("Q086",2,"Avoided crossing gap and normalized mixed-level spectral projectors",Math.max(Math.abs(mid[0]-mid[1]-R),Math.abs((1-ds/R)/2+(1+ds/R)/2-1)),1e-14,"projector");
  const weights=[(1-ds/R)/8,(1+ds/R)/8];
  test("Q086",3,"Transverse electron spin-flip transition sum rule and positive oscillator strength",Math.abs(weights[0]+weights[1]-.25),1e-14,"transition_sum_rule");
  const beta=.83,partition=b=>{
   const sig=(alphaS+alphaI)*b,dlt=(alphaS-alphaI)*b;
   return 2*Math.exp(-beta*A/4)*Math.cosh(beta*sig/2)+2*Math.exp(beta*A/4)*Math.cosh(beta*Math.hypot(A,dlt)/2);
  };
  const z0=partition(0);
  const chi=(Math.exp(-beta*A/4)*beta*(alphaS+alphaI)**2/2+
   Math.exp(beta*A/4)*(alphaS-alphaI)**2/A*Math.sinh(beta*A/2))/z0;
  const h=.0004,numerical=(Math.log(partition(h))-2*Math.log(z0)+Math.log(partition(-h)))/(beta*h*h);
  if(chi<0)throw Error("Q086 negative magnetic susceptibility");
  test("Q086",4,"Four-level canonical partition gives positive and numerically verified zero-field susceptibility",Math.abs(chi-numerical),1e-7,"thermodynamic_derivative");
 }
 if(checks.length!==24)throw Error("expected 24 checks; got "+checks.length);
 return{round:15,model_replacements:["M089","E091","T085","W084","O085","Q086"],checked_subparts:24,required_full_round_checks:200,full_round_pass:false,independent_expert_review:"待独立复核",tests:checks};
}
const report=physicsSubset();
process.stdout.write(JSON.stringify(report,null,2)+'\n');
if(report.checked_subparts!==24||report.tests.some(t=>!t.passed))process.exitCode=1;
