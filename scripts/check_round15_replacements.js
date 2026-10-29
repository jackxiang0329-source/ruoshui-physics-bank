#!/usr/bin/env node
'use strict';
// Round 15: executable independent mathematical/physical subset checks.
// 8 real subpart checks for two rewritten models only. Not the 200-check full gate.
function validate(){
  const checks=[],PI=Math.PI;
  function add(id,part,method,name,error,tolerance,details){
    if(!Number.isFinite(error)||error>tolerance)throw Error(id+" part "+part+": "+name+" error="+error+" > "+tolerance);
    checks.push({id,part,method,name,passed:true,numerical_error:error,tolerance,details});
  }
  function simpson(f,a,b,n=2000){
    if(n%2)throw Error("Simpson requires even n");
    let h=(b-a)/n,sum=f(a)+f(b);
    for(let j=1;j<n;j++)sum+=(j%2?4:2)*f(a+j*h);
    return sum*h/3;
  }
  // T080: radial reaction diffusion. Independent finite differences/integrals.
  const D=.81,k=.63,R=1.37,cs=2.17,lambda=Math.sqrt(k/D),phi=lambda*R;
  const concentration=r=>r===0?cs*phi/Math.sinh(phi):cs*R*Math.sinh(lambda*r)/(r*Math.sinh(phi));
  let maxResidual=0;
  for(const r of [.32*R,.61*R,.85*R]){
    const h=R*0.00015,cr=concentration(r),der=(concentration(r+h)-concentration(r-h))/(2*h);
    const lap=(concentration(r+h)-2*cr+concentration(r-h))/(h*h)+2*der/r;
    maxResidual=Math.max(maxResidual,Math.abs(D*lap-k*cr));
  }
  add("T080",1,"independent_numerical","Finite-difference spherical diffusion-reaction residual",maxResidual,2e-6,"Three interior radial points; regular center handled analytically");
  const flux=4*PI*R*D*cs*(phi*Math.cosh(phi)/Math.sinh(phi)-1);
  const volumeRate=4*PI*k*simpson(r=>r*r*concentration(r),0,R,3000);
  const eta=3*(phi*Math.cosh(phi)/Math.sinh(phi)-1)/(phi*phi);
  add("T080",2,"conservation","Surface diffusive flux versus independent volume reaction integral and Thiele factor",Math.max(Math.abs(flux-volumeRate),Math.abs(eta-flux/((4*PI*R**3/3)*k*cs))),3e-10,"Independent Simpson volume quadrature");
  const q=PI/R, decay=k+D*q*q,t0=.48,rr=.37*R,hx=R*0.00013,ht=.00003;
  const u=(x,t)=>Math.sin(q*x)*Math.exp(-decay*t);
  const dtu=(u(rr,t0+ht)-u(rr,t0-ht))/(2*ht);
  const dxxu=(u(rr+hx,t0)-2*u(rr,t0)+u(rr-hx,t0))/(hx*hx);
  add("T080",3,"spectral","Dirichlet first radial mode satisfies time-dependent transformed PDE",Math.abs(dtu-D*dxxu+k*u(rr,t0)),2e-6,"Central differences in time and radial coordinate");
  const amp=.92;
  function y(r,t){return r===0?amp*q*Math.exp(-decay*t):amp*Math.sin(q*r)/r*Math.exp(-decay*t)}
  function yr(r,t){if(r===0)return 0;return amp*Math.exp(-decay*t)*(q*r*Math.cos(q*r)-Math.sin(q*r))/(r*r)}
  function energy(t){return 2*PI*simpson(r=>r*r*y(r,t)**2,0,R,3000)}
  const gradIntegral=4*PI*simpson(r=>r*r*yr(r,t0)**2,0,R,3000);
  const massIntegral=4*PI*simpson(r=>r*r*y(r,t0)**2,0,R,3000);
  const hE=.00004,dedt=(energy(t0+hE)-energy(t0-hE))/(2*hE);
  add("T080",4,"energy_boundary","Lyapunov derivative agrees with independently integrated diffusion and reaction losses",Math.abs(dedt+D*gradIntegral+k*massIntegral),2e-7,"Independent radial gradients and quadratures, not a restated exponential identity");
  // E087: cold symmetric electron beams. eps0=m=e=1 in normalized units.
  const wp=2.3;
  function xroots(a){
    const root=Math.sqrt(wp**4+8*wp*wp*a*a);
    return [a*a+wp*wp/2+root/2,a*a+wp*wp/2-root/2];
  }
  const a=.57*wp,om=Math.sqrt(xroots(a)[0]);
  const eps=1-wp*wp/2*(1/(om-a)**2+1/(om+a)**2);
  add("E087",1,"independent_derivation","Longitudinal dielectric relation evaluated on the polynomial mode",Math.abs(eps),5e-13,"Two-stream rational susceptibility computed independently of polynomial");
  let quarticError=0;
  for(const aval of [.37*wp,.88*wp,1.27*wp]){
    const [xp,xm]=xroots(aval);
    for(const x of [xp,xm])quarticError=Math.max(quarticError,Math.abs((x-aval*aval)**2-wp*wp*(x+aval*aval))/wp**4);
    if(aval<wp&&xm>=0)throw Error("E087: missed unstable interval");
    if(aval>wp&&xm<=0)throw Error("E087: stable interval is wrong");
  }
  add("E087",2,"symbolic_limit","Both exact roots satisfy quartic and instability changes sign at a=wp",quarticError,4e-13,"Roots checked at two unstable and one stable wavenumber");
  function gamma2(z){return (wp/2)*Math.sqrt(wp*wp+8*z)-z-wp*wp/2}
  let left=0,right=wp*wp;
  const ratio=(Math.sqrt(5)-1)/2;
  let c=right-ratio*(right-left),d=left+ratio*(right-left);
  for(let i=0;i<95;i++){
    if(gamma2(c)>gamma2(d)){right=d;d=c;c=right-ratio*(right-left)}
    else{left=c;c=d;d=left+ratio*(right-left)}
  }
  const zfound=(left+right)/2,ztheory=3*wp*wp/8;
  const gammamax=Math.sqrt(gamma2(zfound));
  add("E087",3,"optimization","Numerical golden-section growth maximum versus derivative-derived extremum",
    Math.max(Math.abs(zfound-ztheory),Math.abs(gammamax-wp/(2*Math.sqrt(2)))),1e-7,
    "Direct 1D optimization over 0 < k^2 v0^2 < wp^2");
  // E087 local second-order disturbance balance at several points.
  const plasma=1,kx=1.2,v0=1,nb=plasma**2/2,ax=kx*v0;
  const Xhi=ax*ax+plasma*plasma/2+plasma/2*Math.sqrt(plasma*plasma+8*ax*ax);
  const omega=Math.sqrt(Xhi);
  function energyTerms(x,t){
    const theta=kx*x-omega*t,EE=Math.cos(theta),ss=Math.sin(theta);
    let W=EE*EE/2,flux=0,rhs=0;
    for(const u0 of [v0,-v0]){
      const delta=omega-kx*u0,dv=ss/delta,dn=kx*nb*ss/(delta*delta);
      W+=nb*dv*dv/2;
      flux+=nb*u0*dv*dv/2;
      rhs+=EE*u0*dn;
    }
    return {W,flux,rhs};
  }
  let maxEnergyResidual=0;
  for(const [x,t] of [[.37,.23],[1.03,.74],[.91,.19]]){
    const hh=.00002;
    const dw=(energyTerms(x,t+hh).W-energyTerms(x,t-hh).W)/(2*hh);
    const dflux=(energyTerms(x+hh,t).flux-energyTerms(x-hh,t).flux)/(2*hh);
    maxEnergyResidual=Math.max(maxEnergyResidual,Math.abs(dw+dflux-energyTerms(x,t).rhs));
  }
  add("E087",4,"energy_flux","Local quadratic field-plus-fluid energy exchange evaluated by independent finite differences",maxEnergyResidual,2e-8,
    "Three space-time points; asymmetric beam currents included");
  return {round:15,model_replacements:["T080","E087"],checked_subparts:checks.length,required_full_round_checks:200,
    full_round_pass:false,independent_expert_review:"待独立复核",
    status:"SUBSET_MODEL_TESTS_ONLY_DO_NOT_RELEASE",tests:checks};
}
const result = validate();
process.stdout.write(JSON.stringify(result, null, 2) + '\n');
if (result.checked_subparts !== 8 || result.tests.some(t => !t.passed)) process.exitCode = 1;
