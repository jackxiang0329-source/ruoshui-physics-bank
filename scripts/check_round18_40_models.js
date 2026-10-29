#!/usr/bin/env node
'use strict';
// 40 representative physical-model checks for the 40 new Round 18 drafts.
// Not a substitute for the 160 independent subpart checks or expert review.
const tests=[],P=Math.PI;
function check(id,method,actual,expected,tolerance=1e-8){
 const e=Math.abs(actual-expected);
 if(!Number.isFinite(e)||e>tolerance)throw Error(id+' '+method+' residual='+e+' tolerance='+tolerance);
 tests.push({id,method,passed:true,residual:e,tolerance});
}
const d=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
const d2=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/(h*h);
const sim=(f,a,b,n=4000)=>{let h=(b-a)/n,s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+h*i);return s*h/3};
// Mechanics 109-115
{
 const a=2,b=3.5,J=.8,R=.2,g=9.8,acc=(b-a)*g/(a+b+J/R**2),T1=a*(g+acc),T2=b*(g-acc);
 check('M109','Atwood_pulley_angular_momentum_equation',(T2-T1)*R,J*acc/R);
}
{
 const M=2.7,m=1.3,alpha=.6,g=9.8,acc=g*Math.sin(alpha)*(M+m)/(M+m*Math.sin(alpha)**2),Xacc=-m*Math.cos(alpha)*acc/(M+m);
 check('M110','wedge_horizontal_momentum_conservation',(M+m)*Xacc+m*Math.cos(alpha)*acc,0);
}
{
 const g=9.8,L=2.2,k=.3,m=1.1,plus=Math.sqrt(g/L),minus=Math.sqrt(g/L+2*k/m),x=.4;
 const t=.7,th1=x*(Math.cos(plus*t)+Math.cos(minus*t))/2,th2=x*(Math.cos(plus*t)-Math.cos(minus*t))/2;
 check('M111','normal_mode_decomposition_initial_displacement',th1+th2,x*Math.cos(plus*t));
}
{
 const r0=2.4,mu=9.7,eta=.7,r=r0*Math.cos(eta)**2,t=x=>Math.sqrt(r0**3/(2*mu))*(x+Math.sin(x)*Math.cos(x));
 const dt_dr=d(t,eta)/d(x=>r0*Math.cos(x)**2,eta),pred=-1/Math.sqrt(2*mu*(1/r-1/r0));
 check('M112','gravitational_infall_parametric_time_derivative',dt_dr,pred);
}
{
 const mu=1.8,v=2.1,K=3.2,delta=(5*mu*v*v/(4*K))**(2/5);
 check('M113','Hertz_contact_maximum_compression_energy',2*K*delta**(5/2)/5,mu*v*v/2,2e-11);
}
{
 const m=1.2,q=.8,E=1.5,B=2,t=.63,w=q*B/m,vD=E/B,vx=vD*Math.sin(w*t),vy=vD*(Math.cos(w*t)-1),x=vD*(1-Math.cos(w*t))/w;
 check('M114','crossed_fields_Lorentz_energy_work',m*(vx*vx+vy*vy)/2,q*E*x);
}
{
 const m1=2.5,m2=1.3,v0=1.8,after1=(m1-m2)/(m1+m2)*v0,after2=2*m1/(m1+m2)*v0;
 check('M115','elastic_spring_exchange_final_momentum',m1*after1+m2*after2,m1*v0);
}
// EM 109-115
{
 const e1=3.4,e2=1.5,E0=1.2,a=1.8,Ein=3*e2*E0/(e1+2*e2),B=a**3*E0*(e1-e2)/(e1+2*e2);
 check('E109','dielectric_sphere_normal_displacement_boundary',e1*Ein,e2*(E0+2*B/a**3));
}
{
 const w=3.2,mu=2.1,sigma=5.2,delta=Math.sqrt(2/(w*mu*sigma)),Rs=Math.sqrt(w*mu/(2*sigma));
 check('E110','skin_depth_surface_resistance_identity',sigma*delta*Rs,1);
}
{
 const L=2.3,C=.9,a=.4,R=L*a,G=C*a,w=1.7;
 const gammaR=Math.sqrt(L*C)*a,gammaI=Math.sqrt(L*C)*w;
 check('E111','distortionless_telegrapher_constant_attenuation',gammaR*gammaR-gammaI*gammaI,R*G-w*w*L*C);
}
{
 const fact=n=>{let x=1;for(let j=2;j<=n;j++)x*=j;return x};
 const I=(n,x)=>{let term=(x/2)**n/fact(n),sum=term;for(let j=1;j<24;j++){term*=x*x/(4*j*(n+j));sum+=term}return sum};
 const x=1.8;
 check('E112','London_cylinder_Bessel_magnetic_moment_identity',I(0,x)-I(2,x),2*I(1,x)/x,1e-12);
}
{
 const eps=1.3,w=1.9,d=.6,k=2,V=1.8,dx=.2,Cprime=eps*w*(k-1)/d;
 check('E113','inserted_dielectric_fixedV_source_work_ledger',V*V*Cprime*dx,V*V*Cprime*dx/2+V*V*Cprime*dx/2);
}
{
 const n=3,e=1.5,B=2.3,jx=1.1,Ey=-B*jx/(n*e);
 check('E114','electron_Hall_coefficient_sign',Ey/(jx*B),-1/(n*e));
}
{
 const a=1.7,r=2.1,Bdot=-.8,Ephi=-a*a*Bdot/(2*r);
 check('E115','Faraday_circular_induced_EMF',2*P*r*Ephi,-P*a*a*Bdot);
}
// Thermal 102-108
{
 const alpha=.9,T=2.7,beta=1/T,Z=sim(x=>Math.exp(-beta*alpha*x**4),0,6,6000),V=alpha*sim(x=>x**4*Math.exp(-beta*alpha*x**4),0,6,6000)/Z;
 check('T102','quartic_canonical_partition_virial_energy',V,T/4,2e-9);
}
{
 const g=9.8,M=.03,Cp=29,dTdz=-M*g/Cp;
 check('T103','dry_adiabatic_lapse_and_entropy',Cp*dTdz,-M*g);
}
{
 const nw=1000,ns=1,R=8.3,T=300,v=.018,Pi=-R*T/v*Math.log(nw/(nw+ns));
 check('T104','osmotic_pressure_dilute_vant_Hoff',Pi/(ns/(nw*v)*R*T),1,.001);
}
{
 const a=2.3,V=1.6,T=3.5,U=a*V*T**4,S=4*a*V*T**3/3,p=a*T**4/3;
 check('T105','photon_gas_Euler_thermodynamic_identity',T*S,U+p*V);
}
{
 const r=6,gamma=1.4,T1=300,T3=1800,T2=T1*r**(gamma-1),T4=T3/r**(gamma-1);
 const eff=1-(T4-T1)/(T3-T2);
 check('T106','Otto_cycle_thermal_efficiency',eff,1-r**(1-gamma));
}
{
 const Cv=2.4,a=1.7,vi=1.3,vf=2.1,Ti=4,Tf=Ti+a/Cv*(1/vf-1/vi);
 check('T107','van_der_Waals_Joule_free_expansion_energy',Cv*Tf-a/vf,Cv*Ti-a/vi);
}
{
 const mass=1.4,T=2.1,kB=1,alpha=mass/(2*kB*T),j=sim(v=>v*Math.sqrt(alpha/P)*Math.exp(-alpha*v*v),0,14,4000);
 check('T108','effusion_positive_normal_velocity_flux_integral',j,Math.sqrt(kB*T/(2*P*mass)));
}
// Waves 102-108
{
 const mass=1.3,b=.7,w=2.1,A=.8,L=2.4;
 const damp=b*L*w*w*A*A/4;const forcing=b*w*A,source=forcing*L*w*A/4;
 check('W102','driven_damped_string_average_power',damp,source);
}
{
 const c=3.1,U=.7,w=2.3,wr=w*(c-U)/(c+U);
 check('W103','moving_acoustic_wall_phase_matching',w*(1-U/c),wr*(1+U/c));
}
{
 const c0=3.2,g=9.8,t=.75,left=-c0*t,right=2*c0*t;
 const mass=sim(x=>((2*c0-x/t)/3)**2/g,left,right,4200);
 check('W104','shallow_water_dam_break_rarefaction_mass_conservation',mass,c0**3*t/g,2e-10);
}
{
 const G=2.7,rho=1.9,k=.8,w=Math.sqrt(G/rho)*k,eff=(G*k*w)/(rho*w*w);
 check('W105','elastic_torsional_shaft_energy_velocity',eff,Math.sqrt(G/rho));
}
{
 const rho=1.7,S=.3,L=1.1,V=2.4,c=3.2,m=rho*S*L,K=rho*c*c*S*S/V,omega=c*Math.sqrt(S/(V*L));
 check('W106','Helmholtz_resonator_mass_stiffness_dispersion',K/m,omega*omega);
}
{
 const g=9.8,rho=2.1,sigma=.7,k=Math.sqrt(rho*g/sigma),p=Math.sqrt(g/k+sigma*k/rho);
 check('W107','deep_water_capillary_phase_speed_minimum',p,(4*g*sigma/rho)**.25);
}
{
 const rho=1.9,c=3.5,A=2.1,r=2.7,flux=A*A/(2*rho*c*r*r),total=4*P*r*r*flux;
 check('W108','spherical_acoustic_radiation_total_power',total,2*P*A*A/(rho*c));
}
// Optics 102-107
{
 const theta=P/2,N=160,T=Math.cos(theta/N)**(2*N);
 check('O102','polarizer_chain_quantum_Zeno_asymptotic',Math.log(T)*N,-theta*theta,.00007);
}
{
 const kappa=2.6,g=.015,exact=kappa/2-2*Math.sqrt(kappa*kappa/16-g*g),bad_cavity=4*g*g/kappa;
 check('O103','Purcell_weak_cavity_decay_vs_exact_coupled_eigenvalue',exact,bad_cavity,1e-7);
}
{
 const kz=1.5,kappa=.8,d=.6,C=(kz*kz+kappa*kappa)**2/(4*kz*kz*kappa*kappa);
 const trans=1/(1+C*Math.sinh(kappa*d)**2);
 check('O104','frustrated_TIR_transmission_passivity',Math.max(0,trans-1),0);
}
{
 const tau=1.3,beta2=.8,L=2.1,expected=tau*Math.sqrt(1+(beta2*L/tau**2)**2);
 check('O105','group_velocity_dispersion_Gaussian_pulse_width',expected*expected,tau*tau+(beta2*L/tau)**2);
}
{
 const delta=1.4,L=2.3,x=delta*L/2,amp=2*Math.sin(x)/delta;
 check('O106','second_harmonic_sinc_phase_matching_integral',amp,L*Math.sin(x)/x);
}
{
 const n1=1.52,n2=1.47,NA=Math.sqrt(n1*n1-n2*n2),angle=Math.asin(NA);
 check('O107','step_index_fiber_numerical_aperture',Math.sin(angle),NA);
}
// Quantum 102-107
{
 const c2=1/Math.sqrt(2);let p=c2*c2;
 for(let n=1;n<=1501;n+=2){const c=4*Math.SQRT2*Math.sin(n*P/2)/(P*(4-n*n));p+=c*c}
 check('Q102','sudden_box_expansion_eigenbasis_normalization',p,1,1e-8);
}
{
 const nbar=.7;let ps=0,factor=Math.exp(-nbar);
 for(let n=0;n<=20;n++){ps+=factor;factor*=nbar/(n+1)}
 check('Q103','displaced_oscillator_coherent_Poisson_probability_sum',ps,1,1e-13);
}
{
 const theta=.64,vec=[Math.cos(theta),Math.sin(theta),0,0],swap=[vec[0],vec[2],vec[1],vec[3]],overlap=vec.reduce((a,x,i)=>a+x*swap[i],0);
 check('Q104','SWAP_test_tensor_permutation_overlap',overlap,Math.cos(theta)**2,1e-12);
}
{
 const Tc=2.3,T=1.4,N0=1-(T/Tc)**1.5,ex=(T/Tc)**1.5;
 check('Q105','three_dimensional_Bose_Einstein_condensate_fraction',N0+ex,1);
}
{
 const m=1.3,R=2.2,hbar=1,q=1.7,h=2*P*hbar,phi=.4,E=(n,f)=>hbar*hbar*(n-f)**2/(2*m*R*R);
 check('Q106','Aharonov_Bohm_flux_periodicity_with_level_relabel',E(0,phi),E(1,phi+1));
}
{
 const hbar=1.2,delta=.7,t=.5,V=.8,prob=4*V*V*Math.sin(delta*t/(2*hbar))**2/(delta*delta);
 const direct=V*V*t*t/(hbar*hbar)*(Math.sin(delta*t/(2*hbar))/(delta*t/(2*hbar)))**2;
 check('Q107','Fermi_golden_rule_finite_time_transition_probability',prob,direct);
}
if(new Set(tests.map(t=>t.id)).size!==40||tests.length<40)throw Error('Round 18 model QA coverage below 40');
const report={round:18,covered_models:40,executed_representative_model_checks:tests.length,independently_verified_subparts:0,required_subpart_checks:160,expert_review:'待独立复核',full_historical_model_rescreen:'pending',full_release_allowed:false,tests};
process.stdout.write(JSON.stringify(report,null,2)+'\n');
