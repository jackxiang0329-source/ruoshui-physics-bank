#!/usr/bin/env node
'use strict';
// 24 executable physics checks. Includes full-coherence relative entropy for Q084.
function verifySixCores(){
 const results=[],pi=Math.PI;
 const pass=(id,part,method,description,error,tolerance)=>{
  if(!Number.isFinite(error)||error>tolerance)throw Error(`${id}-${part} ${description}: ${error} > ${tolerance}`);
  results.push({id,part,method,description,passed:true,error,tolerance});
 };
 const int=(f,a,b,n=3200)=>{let h=(b-a)/n,sum=f(a)+f(b);for(let i=1;i<n;i++)sum+=(i%2?4:2)*f(a+h*i);return sum*h/3};
 const diff=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
 const dot=(a,b)=>a.reduce((v,x,i)=>v+x*b[i],0);
 // M088: potential cylinder with circulation and integrated pressure
 {let U=1.43,R=1.2,rho=1.6,G=5.13;
 const ur=(r,t)=>U*(1-R*R/r**2)*Math.cos(t),ut=(r,t)=>-U*(1+R*R/r**2)*Math.sin(t)+G/(2*pi*r);
 const phi=(r,t)=>U*(r+R*R/r)*Math.cos(t)+G*t/(2*pi);
 pass("M088",1,"independent_finite_difference","Potential derivatives yield radial/tangential velocities and no penetration",Math.max(Math.abs(diff(r=>phi(r,.39),2*R)-ur(2*R,.39)),Math.abs(diff(t=>phi(2*R,t),.39)/(2*R)-ut(2*R,.39)),Math.abs(ur(R,.39))),1e-9);
 const Gc=4*pi*U*R,theta=Math.asin(.4);
 pass("M088",2,"critical_boundary","Stagnation roots and merging at critical circulation",Math.max(Math.abs(-2*U*Math.sin(theta)+.4*Gc/(2*pi*R)),Math.abs(-2*U+Gc/(2*pi*R))),2e-14);
 const p=t=>rho*(U*U-ut(R,t)**2)/2;
 const Fx=-R*int(t=>p(t)*Math.cos(t),0,2*pi),Fy=-R*int(t=>p(t)*Math.sin(t),0,2*pi);
 pass("M088",3,"independent_integral","Numerically integrated pressure has zero drag and Kutta-Joukowski lift",Math.max(Math.abs(Fx),Math.abs(Fy+rho*U*G)),1e-11);
 let rr=4*R,flux=int(t=>rr*ur(rr,t),0,2*pi),circ=int(t=>rr*ut(rr,t),0,2*pi);
 pass("M088",4,"conservation","Outer mass flux vanishes, circulation and surface mechanical power conserved",Math.max(Math.abs(flux),Math.abs(circ-G),Math.abs(int(t=>R*p(t)*ur(R,t),0,2*pi))),1e-11);
 }
 // E090: SQUID
 {let i1=2.1,i2=.83,ph=.74;
 const I=(x,p)=>i1*Math.sin(x+p/2)+i2*Math.sin(x-p/2);
 const V=(x,p)=>-i1*Math.cos(x+p/2)-i2*Math.cos(x-p/2);
 const Ic=p=>Math.hypot(i1+i2*Math.cos(p),i2*Math.sin(p));
 pass("E090",1,"independent_finite_difference","Dual Josephson energy differentiates to exact supercurrent",Math.abs(diff(x=>V(x,ph),.42)-I(.42,ph)),6e-10);
 let max=0;for(let j=0;j<50000;j++)max=Math.max(max,Math.abs(I(2*pi*j/50000,ph)));
 pass("E090",2,"optimization","Dense global phase scan confirms flux-periodic asymmetric critical current",Math.max(Math.abs(max-Ic(ph)),Math.abs(Ic(ph+2*pi)-Ic(ph)),Math.abs(Ic(pi)-Math.abs(i1-i2))),2e-8);
 let eff=Ic(ph),r=.63,bias=eff*r,minimum=Math.asin(r),saddle=pi-minimum,energy=x=>-eff*Math.cos(x)-bias*x;
 let barrier=energy(saddle)-energy(minimum),exact=2*eff*(Math.sqrt(1-r*r)-r*Math.acos(r));
 let e=1e-4,near=2*eff*(Math.sqrt(1-(1-e)**2)-(1-e)*Math.acos(1-e)),asym=4*Math.sqrt(2)/3*eff*e**1.5;
 pass("E090",3,"energy_asymptotic","Direct washboard barrier and critical three-halves power-law match",Math.max(Math.abs(barrier-exact),Math.abs(near/asym-1)),5e-5);
 pass("E090",4,"thermodynamic_derivative","SQUID equilibrium circulating current obtained by flux derivative",Math.abs(-diff(p=>-Ic(p),ph)+i1*i2*Math.sin(ph)/Ic(ph)),5e-10);
 }
 // T083: finite-N constrained ideal gas
 {const N=5,m=1.7,E=13.2,V=3.1,dim=3*(N-1),alpha=dim/2;
 const fac=x=>{let f=1;for(let j=2;j<=x;j++)f*=j;return f};
 let R=Math.sqrt(2*m*E),area=2*pi**alpha/fac(alpha-1);
 let ball=pi**alpha*R**dim/fac(alpha);
 pass("T083",1,"independent_integral","Numerical constrained 12D momentum-ball radial volume",Math.abs(area*int(r=>r**(dim-1),0,R,4000)/ball-1),2e-6);
 let seed=70234267;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return(seed+.5)/4294967296};
 const gaussian=()=>Math.sqrt(-2*Math.log(rand()))*Math.cos(2*pi*rand());
 let m2=0,m4=0,mc=0,M=125000;
 for(let j=0;j<M;j++){
  let p=Array.from({length:N},()=>[gaussian(),gaussian(),gaussian()]);
  let avg=[0,1,2].map(k=>p.reduce((a,v)=>a+v[k],0)/N),size=0;
  for(const v of p)for(let k=0;k<3;k++){v[k]-=avg[k];size+=v[k]*v[k]}
  let scale=Math.sqrt(2*m*E/size);
  for(const v of p)for(let k=0;k<3;k++)v[k]*=scale;
  m2+=p[0][0]**2;m4+=p[0][0]**4;mc+=dot(p[0],p[1]);
 }
 m2/=M;m4/=M;mc/=M;
 pass("T083",2,"seeded_shell_monte_carlo","Total-momentum constraint produces negative two-particle covariance and finite variance",Math.max(Math.abs(m2/(2*m*E/(3*N))-1),Math.abs(mc/(-2*m*E/(N*(N-1)))-1)),.055);
 const S=(energy,vol)=>N*Math.log(vol)+alpha*Math.log(energy);
 pass("T083",3,"thermodynamic_derivative","Gibbs finite-system temperature and ideal pressure from entropy differentiation",Math.max(Math.abs(diff(z=>S(z,V),E,1e-4)-alpha/E),Math.abs(diff(z=>S(E,z),V,1e-4)-N/V)),2e-9);
 const expected4=3*(2*m*E)**2*(1-1/N)**2/(dim*(dim+2)),kurt=3*dim/(dim+2);
 pass("T083",4,"seeded_shell_monte_carlo","Projected microcanonical fourth moment has finite-size non-Gaussian kurtosis",Math.max(Math.abs(m4/expected4-1),Math.abs(m4/m2**2/kurt-1)),.055);
 }
 // W083: incompressible inertial helical wave
 {let Om=1.73,k=2.1,theta=.68,rho=2.4,A=.81,c=Math.cos(theta),s=Math.sin(theta);
 let e1=[c,0,-s],e2=[0,1,0],kh=[s,0,c],K=kh.map(x=>k*x),w=2*Om*c;
 let vr=e1.map(x=>A*x),vi=e2.map(x=>-A*x),press=-2*rho*Om*A*s/k;
 const cross=(u,v)=>[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
 let cr=cross([0,0,2*Om],vr),ci=cross([0,0,2*Om],vi);
 let resR=vi.map((z,i)=>w*z+cr[i]),resI=vr.map((z,i)=>-w*z+ci[i]+K[i]*press/rho);
 pass("W083",1,"independent_vector_residual","Three-dimensional Euler helical plane wave satisfies real/imaginary components",Math.max(...resR.map(Math.abs),...resI.map(Math.abs)),2e-12);
 pass("W083",2,"polarization","Incompressible circular transverse polarization and orthogonal polarization vectors",Math.max(Math.abs(dot(K,vr)),Math.abs(dot(K,vi)),Math.abs(dot(vr,vi)),Math.abs(dot(vr,vr)-dot(vi,vi))),2e-12);
 const disp=X=>2*Om*X[2]/Math.hypot(...X);
 const grad=K.map((_,i)=>{let x=[...K],y=[...K];x[i]+=1e-5;y[i]-=1e-5;return(disp(x)-disp(y))/2e-5;});
 const group=kh.map((v,j)=>2*Om/k*((j===2?1:0)-c*v));
 pass("W083",3,"spectral_group_velocity","Independent three-axis numerical dispersion derivative is perpendicular to wavevector",Math.max(...grad.map((x,i)=>Math.abs(x-group[i])),Math.abs(dot(K,grad))),1e-9);
 let energy=rho*A*A/2,flow=e1.map(x=>-rho*Om*A*A*s*x/k);
 pass("W083",4,"energy_flux","Cycle-averaged pressure/velocity flux equals energy times group speed",Math.max(...flow.map((x,i)=>Math.abs(x-energy*group[i]))),2e-12);
 }
 // O084: resonance fluorescence
 {const gamma=1.3,om=.91,mu=Math.sqrt(om*om-gamma*gamma/16);
 const w=-gamma*gamma/(gamma*gamma+2*om*om),v=-2*om*gamma/(gamma*gamma+2*om*om),pe=om*om/(gamma*gamma+2*om*om);
 pass("O084",1,"Lindblad_stationarity","Resonant optical Bloch stationary excitation and dipole satisfy both equations",Math.max(Math.abs(-gamma*v/2+om*w),Math.abs(-gamma*(w+1)-om*v),Math.abs((1+w)/2-pe)),3e-13);
 const g2=t=>1-Math.exp(-.75*gamma*t)*(Math.cos(mu*t)+(.75*gamma/mu)*Math.sin(mu*t));
 const f=y=>[-gamma*y[0]/2+om*y[1],-gamma*(y[1]+1)-om*y[0]];
 const rk=(y,h)=>{let a=f(y),b=f(y.map((v,i)=>v+h*a[i]/2)),c=f(y.map((v,i)=>v+h*b[i]/2)),d=f(y.map((v,i)=>v+h*c[i]));return y.map((v,i)=>v+h*(a[i]+2*b[i]+2*c[i]+d[i])/6)};
 let y=[0,-1],worst=0,dt=.001;
 for(let i=0;i<7000;i++){if(i%233===0)worst=Math.max(worst,Math.abs((y[1]+1)/(2*pe)-g2(i*dt)));y=rk(y,dt);}
 pass("O084",2,"independent_ode_integration","Photon-jump reset to ground propagated with independent RK4 matches analytic g2",worst,2e-11);
 const h=.0001,expected=(gamma*gamma+2*om*om)*h*h/4;
 pass("O084",3,"short_time_asymptotic","Antibunching g2(0) zero and finite short-time quadratic coefficient",Math.max(Math.abs(g2(0)),Math.abs(g2(h)/expected-1)),2e-4);
 const integral=int(t=>g2(t)-1,0,36/gamma,16000),exact=-3*gamma/(gamma*gamma+2*om*om);
 const F=1+2*gamma*pe*integral,closed=1-6*gamma*gamma*om*om/(gamma*gamma+2*om*om)**2;
 pass("O084",4,"independent_integral","Numerically integrated photon antibunching correlation gives sub-Poisson Fano",Math.max(Math.abs(integral-exact),Math.abs(F-closed)),3e-11);
 }
 // Q084: quantum Otto nonadiabatic engine. Full density-matrix entropy preserved under strokes.
 {const wc=1,wh=2,Tc=1,Th=3,xi=.01,tc=Math.tanh(wc/(2*Tc)),th=Math.tanh(wh/(2*Th)),b=1-2*xi;
 const EA=-wc*tc/2,EB=-wh*b*tc/2,EC=-wh*th/2,ED=-wc*b*th/2,Qh=EC-EB,Qc=EA-ED,W=Qh+Qc,Win=(EB-EA)+(ED-EC);
 pass("Q084",1,"first_law","Quantum engine four corner internal energies close cycle energy balance",Math.abs(Win+Qh+Qc),3e-13);
 const ideal=(wh-wc)*(tc-th)/2,loss=xi*(wh*tc+wc*th),eff=W/Qh;
 if(!(W>0&&Qh>0))throw Error("Q084 incorrect engine regime");
 pass("Q084",2,"energy_boundary","Heat engine finite-time friction lowers net work by predicted exact amount",Math.max(Math.abs(ideal-W-loss),Math.abs(eff-(1-wc*(tc-b*th)/(wh*(b*tc-th))))),3e-13);
 const entropy=t=>{const p=(1-t)/2;return -p*Math.log(p)-(1-p)*Math.log(1-p)};
 const logZ=(w,T)=>Math.log(2*Math.cosh(w/(2*T)));
 // D(rho_B || rho_Ceq) = -S(rho_B) + beta_h U_B + log Z_h.
 // Since B is unitary transformation of A, entropy B is entropy of A.
 const entropyProd=(-entropy(tc)+EB/Th+logZ(wh,Th))+(-entropy(th)+ED/Tc+logZ(wc,Tc));
 const thermo=-Qh/Th-Qc/Tc;
 if(!(entropyProd>0&&thermo>0))throw Error("Q084 second law sign");
 pass("Q084",3,"quantum_relative_entropy","Full quantum relative entropies with unitary-preserved coherences equal Clausius entropy production",Math.abs(entropyProd-thermo),4e-13);
 const out=x=>{let a=1-2*x;return(wh*(a*tc-th)+wc*(a*th-tc))/2};
 const critical=(wh-wc)*(tc-th)/(2*(wh*tc+wc*th));
 const linear=(1-wc/wh)-2*wc/wh*xi*(tc+th)/(tc-th);
 pass("Q084",4,"optimization_asymptotic","Nonadiabatic work slope, exact work cutoff and weak-loss efficiency",Math.max(Math.abs(diff(out,xi)+(wh*tc+wc*th)),Math.abs(out(critical)),Math.abs(eff-linear)),.004);
 }
 if(results.length!==24)throw Error("wrong result count "+results.length);
 return{round:15,model_replacements:["M088","E090","T083","W083","O084","Q084"],checked_subparts:24,required_full_round_checks:200,full_round_pass:false,independent_expert_review:"待独立复核",tests:results};
}
const report=verifySixCores();
process.stdout.write(JSON.stringify(report,null,2)+'\n');
if(report.checked_subparts!==24||report.tests.some(x=>!x.passed))process.exitCode=1;
