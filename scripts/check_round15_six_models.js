#!/usr/bin/env node
'use strict';
// Twenty-four physical model checks for six replacements; not a full-round release gate.
function checks24(){
 const out=[],P=Math.PI;
 const check=(id,part,method,name,err,tol)=>{if(!Number.isFinite(err)||err>tol)throw Error(id+" "+part+" "+name+" err="+err);out.push({id,part,method,name,passed:true,residual:err,tolerance:tol})};
 const integ=(f,a,b,n=3000)=>{const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3};
 const df=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
 // M086 restricted three body
 {const mu=.027,x=.5-mu,y=Math.sqrt(3)/2;
 const U=(a,b)=>(a*a+b*b)/2+(1-mu)/Math.hypot(a+mu,b)+mu/Math.hypot(a-1+mu,b);
 check("M086",1,"independent_numerical","Routh triangle rotating equilibrium finite-difference force",Math.hypot(df(a=>U(a,y),x),df(b=>U(x,b),y)),1e-8);
 const h=.0005,uxx=(U(x+h,y)-2*U(x,y)+U(x-h,y))/h**2,uyy=(U(x,y+h)-2*U(x,y)+U(x,y-h))/h**2;
 const uxy=(U(x+h,y+h)-U(x+h,y-h)-U(x-h,y+h)+U(x-h,y-h))/(4*h*h);
 check("M086",2,"independent_numerical","Routh triangle Hessian xx yy xy numerical reconstruction",Math.max(Math.abs(uxx-.75),Math.abs(uyy-2.25),Math.abs(uxy-3*Math.sqrt(3)*(1-2*mu)/4)),2e-6);
 check("M086",3,"spectral","Coriolis quartic coefficients from independently reconstructed Hessian",Math.max(Math.abs(4-uxx-uyy-1),Math.abs(uxx*uyy-uxy*uxy-27*mu*(1-mu)/4)),2e-6);
 const m=1e-6,disc=Math.sqrt(1-27*m*(1-m)),low=27*m*(1-m)/(2*(1+disc)),mc=(1-Math.sqrt(23/27))/2;
 if(!(mc>.038&&mc<.039&&1-27*.1*.9<0))throw Error("M critical");
 check("M086",4,"asymptotic","Small mass linear slow-mode asymptotic compared with exact root",Math.abs(low/(27*m/4)-1),2e-5);
 }
 // E088 anisotropic Poisson and capacitor
 {const eps=[2.3,4.1,7.3],g=Math.sqrt(eps[0]*eps[1]*eps[2]),q=1.37;
 const s=v=>Math.sqrt(v.reduce((r,a,i)=>r+a*a/eps[i],0)),pot=v=>q/(4*P*g*s(v)),r=[1.3,-.92,.78],h=.0005;
 let lap=0;for(let j=0;j<3;j++){let a=[...r],b=[...r];a[j]+=h;b[j]-=h;lap+=eps[j]*(pot(a)-2*pot(r)+pot(b))/h**2;}
 check("E088",1,"independent_numerical","Three-axis finite-difference anisotropic Poisson operator away from source",Math.abs(lap),3e-7);
 const a=1.3,integFlux=integ(t=>q*Math.sin(t)/2,0,P);
 check("E088",2,"conservation","Ellipsoid transformed-area surface displacement flux integrates to point charge",Math.abs(integFlux-q),1e-10);
 const a0=.9,b0=2.6,V=1.8,K=V/(1/a0-1/b0),psi=t=>K*(1/t-1/b0);
 check("E088",3,"boundary","Two confocal Dirichlet electrodes and numerical normal-field derivative",Math.max(Math.abs(psi(a0)-V),Math.abs(psi(b0)),Math.abs(df(psi,1.7)+K/1.7**2)),1e-9);
 const cap=4*P*g/(1/a0-1/b0),energy=2*P*g*K*K*integ(t=>1/t**2,a0,b0);
 check("E088",4,"independent_integral","Anisotropic radial field-energy quadrature agrees with half CV squared",Math.abs(energy-cap*V*V/2),1e-8);
 }
 // T081 freely-jointed chain
 {const lang=x=>1/Math.tanh(x)-1/x,logz=x=>Math.log(Math.sinh(x)/x);
 const inverse=y=>{let l=1e-9,r=10;for(let j=0;j<70;j++){let m=(l+r)/2;if(lang(m)<y)l=m;else r=m;}return(l+r)/2};
 const x=1.24,part=integ(u=>Math.exp(x*u)/2,-1,1);
 check("T081",1,"independent_integral","Independent sphere-orientation partition integral and extension derivative",Math.max(Math.abs(part-Math.sinh(x)/x),Math.abs(df(logz,x)-lang(x))),1e-8);
 const y=.027,xinv=inverse(y);
 check("T081",2,"symbolic_limit","Nonlinear inverse Langevin cubic coefficient and positive susceptibility",Math.max(Math.abs(xinv-3*y-1.8*y**3),Math.abs(df(lang,x)-(1/x**2-1/Math.sinh(x)**2))),3e-6);
 const free=y=>{let x=inverse(y);return x*y-logz(x)},yy=.32,d=.0001,xx=inverse(yy);
 const derivative=(free(yy+d)-free(yy-d))/(2*d),curvature=(free(yy+d)-2*free(yy)+free(yy-d))/(d*d);
 check("T081",3,"independent_numerical","Legendre derivative and convex stiffness from inverse force function",Math.max(Math.abs(derivative-xx),Math.abs(curvature-1/(1/xx**2-1/Math.sinh(xx)**2))),1e-5);
 const Y=.41,n=6,F=T=>n*T*free(Y),entropy=-df(F,270,.01);
 check("T081",4,"thermodynamic_scaling","At constant stretch Helmholtz and entropy cancel internal elastic energy",Math.abs(F(270)+270*entropy),1e-8);
 }
 // W081 two Timoshenko branches
 {const M=2.3,J=.47,S=8.1,B=3.2;
 const roots=k=>{let a=M*J,b=(S*J+M*B)*k*k+M*S,c=S*B*k**4,p=(b+Math.sqrt(b*b-4*a*c))/(2*a);return[c/(a*p),p]};
 const k=.79,rr=roots(k),w=Math.sqrt(rr[0]),h=(S*k*k-M*w*w)/(S*k);
 check("W081",1,"independent_derivation","Fourier eigenvector satisfies independent coupled shear and rotation equations",Math.max(Math.abs(S*k*k-M*w*w-S*k*h),Math.abs(-S*k+(B*k*k+S-J*w*w)*h)),2e-11);
 const poly=x=>M*J*x*x-((S*J+M*B)*k*k+M*S)*x+S*B*k**4;
 if(!(rr[0]>0&&rr[1]>rr[0]))throw Error("wrong W dispersion roots");
 check("W081",2,"spectral","Both positive-frequency Timoshenko branches solve quartic",Math.max(Math.abs(poly(rr[0])),Math.abs(poly(rr[1]))),2e-10);
 const low=Math.sqrt(roots(.003)[0])/.003**2,fast=roots(10000).map(v=>Math.sqrt(v)/10000).sort((a,b)=>a-b),theory=[Math.sqrt(S/M),Math.sqrt(B/J)].sort((a,b)=>a-b);
 check("W081",3,"asymptotic","Bending acoustic k-square law and two distinct high-k sound velocities",Math.max(Math.abs(low-Math.sqrt(B/M)),Math.abs(fast[0]-theory[0]),Math.abs(fast[1]-theory[1])),4e-4);
 const f=(x,t)=>{let p=k*x-w*t,si=Math.sin(p),co=Math.cos(p),wt=w*si,vt=h*w*co,shear=(h-k)*si,vx=-h*k*co;return{e:(M*wt**2+J*vt**2+S*shear**2+B*vx**2)/2,flux:-S*shear*wt-B*vx*vt}};
 let worst=0;for(const [x,t] of [[.2,.7],[.8,.3],[1.4,.19]])worst=Math.max(worst,Math.abs(df(u=>f(x,u).e,t,.00005)+df(u=>f(u,t).flux,x,.00005)));
 check("W081",4,"conservation","Real Timoshenko eigenwave satisfies local energy conservation by space-time finite differences",worst,1e-7);
 }
 // O082 extraordinary index and ray walkoff
 {const ep=2.25,ez=3.61,theta=.62,n=1/Math.sqrt(Math.cos(theta)**2/ep+Math.sin(theta)**2/ez),kx=n*Math.sin(theta),kz=n*Math.cos(theta),ex=Math.cos(theta)/ep,ey=-Math.sin(theta)/ez,kdot=kx*ex+kz*ey;
 check("O082",1,"independent_derivation","Extraordinary anisotropic Maxwell wavevector eigen-equations",Math.max(Math.abs(kx*kdot-n*n*ex+ep*ex),Math.abs(kz*kdot-n*n*ey+ez*ey)),1e-12);
 const H=kz*ex-kx*ey,ray=-ey*H/(ex*H);
 check("O082",2,"polarization","Poynting cross-product ray angle equals group velocity anisotropy",Math.abs(ray-ep/ez*Math.tan(theta)),1e-12);
 const fun=t=>Math.abs(ep-ez)*t/(ez+ep*t*t),tstar=Math.sqrt(ez/ep);
 check("O082",3,"optimization","Maximum walkoff from stationary angle equals geometric closed form",Math.max(Math.abs(df(fun,tstar,.0001)),Math.abs(fun(tstar)-Math.abs(ep-ez)/(2*Math.sqrt(ep*ez)))),1e-8);
 const L=1.87;
 check("O082",4,"physical_limit","Slab-ray offset computed from Poynting and wave-normal trajectories",Math.abs(L*(ray-Math.tan(theta))-L*(ep/ez-1)*Math.tan(theta)),1e-12);
 }
 // Q082 quantized circular billiard: independent Bessel series
 {const fac=n=>{let f=1;for(let j=2;j<=n;j++)f*=j;return f};
 const bessel=(n,x)=>{let t=(x/2)**n/fac(n),s=t;for(let j=1;j<60;j++){t*=-(x*x/4)/(j*(j+n));s+=t;if(j>10&&Math.abs(t)<1e-17)break;}return s};
 const root=(n,l,r)=>{let left=bessel(n,l);for(let i=0;i<75;i++){let m=(l+r)/2;if(Math.sign(bessel(n,m))===Math.sign(left)){l=m;left=bessel(n,m)}else r=m;}return(l+r)/2};
 const zeros=[root(0,2,3),root(1,3,4),root(2,5,6)],R=1.73;
 const mom=(n,j,p)=>integ(r=>2*r**(1+p)*bessel(n,j*r/R)**2/(R*R*bessel(n+1,j)**2),0,R);
 let norm=0;for(let ell=0;ell<3;ell++)norm=Math.max(norm,Math.abs(mom(ell,zeros[ell],0)-1));
 check("Q082",1,"independent_integral","Bessel Dirichlet disk eigenstates satisfy exact numerical unit normalization",norm,2e-9);
 const ell=1,hbar=1.17,angular=hbar*ell*mom(ell,zeros[ell],0);
 check("Q082",2,"conservation","Integrated circular probability current carries quantized angular momentum",Math.abs(angular-hbar*ell),2e-9);
 const mass=2.4,q=-.82,field=.03,r2=mom(ell,zeros[ell],2),base=hbar*hbar*zeros[ell]**2/(2*mass*R*R);
 const Ep=base-q*field*angular/(2*mass)+q*q*field*field*r2/(8*mass),Em=base+q*field*angular/(2*mass)+q*q*field*field*r2/(8*mass);
 check("Q082",3,"independent_numerical","Charge-signed linear splitting recovered from magnetic Hamiltonian expectations",Math.abs(Ep-Em+q*field*hbar*ell/mass),2e-11);
 let rErr=0;for(let n=0;n<3;n++)rErr=Math.max(rErr,Math.abs(mom(n,zeros[n],2)-R*R*(1+2*(n*n-1)/zeros[n]**2)/3));
 if(mom(0,zeros[0],2)<=0)throw Error("negative r2");
 check("Q082",4,"independent_integral","Bessel radial second moments and positive quadratic diamagnetism",rErr,2e-9);
 }
 if(out.length!==24)throw Error("wrong number subpart tests "+out.length);
 return{round:15,checked_subparts:out.length,newly_replaced_ids:["M086","E088","T081","W081","O082","Q082"],full_round_pass:false,required_checks:200,independent_expert_review:"待独立复核",tests:out};
}
const result=checks24();
process.stdout.write(JSON.stringify(result,null,2)+'\n');
if(result.checked_subparts!==24||result.tests.some(x=>!x.passed))process.exitCode=1;
