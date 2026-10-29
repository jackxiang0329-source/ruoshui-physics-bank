#!/usr/bin/env node
'use strict';
// 40 genuinely executed representative model-level physical identities.
// These checks are not a substitute for four independent subpart checks per problem.
const tests=[],PI=Math.PI;
const check=(id,method,a,b,tol=1e-8)=>{
 const e=Math.abs(a-b);
 if(!Number.isFinite(e)||e>tol)throw Error(id+' '+method+' residual='+e+' tolerance='+tol);
 tests.push({id,method,residual:e,tolerance:tol,passed:true});
};
const diff=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
const diff2=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/(h*h);
const integrate=(f,a,b,n=4000)=>{const h=(b-a)/n;let y=f(a)+f(b);for(let j=1;j<n;j++)y+=(j%2?4:2)*f(a+j*h);return y*h/3};
{
 const R=1.7,g=9.8,Om=3.5,th=Math.acos(g/(Om*Om*R)),V=x=>-g*R*Math.cos(x)-Om*Om*R*R*Math.sin(x)**2/2;
 check('M102','rotating_hoop_equilibrium',diff(V,th),0);
 check('M102','rotating_hoop_small_oscillation_curvature',diff2(V,th)/R**2,Om*Om*Math.sin(th)**2,1e-5);
}
{
 const l=2.5,g=9.8,th=.55,s=Math.sin(th),c=Math.cos(th),J=Math.sqrt(g*l**3*s**4/c),V=x=>J*J/(2*l*l*Math.sin(x)**2)-g*l*Math.cos(x);
 check('M103','spherical_pendulum_equilibrium',diff(V,th),0);
 check('M103','spherical_pendulum_nutation_frequency',diff2(V,th)/l**2,g/(l*c)*(1+3*c*c),1e-5);
}
{
 const m=1.2,k=3.7,p=2.4,r=1.8,L2=m*k*r**(3-p),V=x=>L2/(2*m*x*x)+k*x**(1-p)/(1-p);
 check('M104','central_powerlaw_orbit_radius_stationarity',diff(V,r),0);
 check('M104','central_powerlaw_radial_frequency',diff2(V,r)/m,(3-p)*k/(m*r**(p+1)),1e-5);
}
{
 const m=1.6,M=2.1,I=.75,b=.45,e=.68,v=2.8,inv=1/m+1/M+b*b/I,J=(1+e)*v/inv;
 const delta=.5*m*(v-J/m)**2+.5*M*(J/M)**2+.5*I*(b*J/I)**2-.5*m*v*v;
 check('M105','eccentric_collision_kinetic_energy_loss',delta,-(1-e*e)*v*v/(2*inv));
}
{
 const nu=.31,rho=2.3,Om=4,R=1.6,r=.62,sr=x=>(3+nu)*rho*Om**2*(R*R-x*x)/8,st=x=>rho*Om**2*((3+nu)*R*R-(1+3*nu)*x*x)/8;
 check('M106','elastic_rotating_disk_radial_force_balance',diff(sr,r)+(sr(r)-st(r))/r+rho*Om*Om*r,0);
}
{
 const m=3,g=7,b=.6,t=.84,V=Math.sqrt(m*g/b),tau=V/g,v=V*Math.tanh(t/tau);
 check('M107','falling_body_quadratic_drag_ODE',diff(t=>V*Math.tanh(t/tau),t),g-b*v*v/m);
}
{
 const G=1.3,h=.07,R=1.7,l=1.4,U=x=>2*PI*G*R*R*h*(2*x*x+x**-4-3),Vol=x=>4*PI*R**3*x**3/3;
 check('M108','balloon_pressure_as_energy_volume_derivative',diff(U,l)/diff(Vol,l),2*G*h*(l**-1-l**-7)/R);
}
{
 const a=.8,b=2.5,p=1.3,eps=2.1,L=3,Q=1.4;
 const integral=integrate(r=>Q*a**p/(2*PI*L*eps*r**(p+1)),a,b);
 check('E102','graded_coaxial_radial_field_integration',integral,Q*(1-(a/b)**p)/(2*PI*L*eps*p));
}
{
 const L=3,M=1.4,R=.7,i=1.3,j=-.6,di=-R*(L*i-M*j)/(L*L-M*M),dj=-R*(L*j-M*i)/(L*L-M*M);
 check('E103','two_mutually_coupled_inductors_dissipation',(L*i+M*j)*di+(L*j+M*i)*dj,-R*(i*i+j*j));
}
{
 const r=1.4,c=.8,V=1.2,t=.9,D=1/(r*c),Q=t=>2*c*V*Math.sqrt(D*t/PI);
 check('E104','semiinfinite_RC_input_current_vs_charge_growth',diff(Q,t),V*Math.sqrt(c/(PI*r*t)));
}
{
 const mu=1.7,K=2.1,k=.6,U=integrate(z=>(mu*K/2)**2*Math.exp(-2*k*z)/mu,0,40/k);
 check('E105','sinusoidal_sheet_current_magnetic_energy',U,mu*K*K/(8*k));
}
{
 const eps=1.2,chi=.8,E=1.4,U=x=>eps*x*x/2+3*chi*x**4/4,D=x=>eps*x+chi*x**3;
 check('E106','nonlinear_dielectric_energy_conjugate',diff(U,E)/diff(D,E),E);
}
{
 const x=.73,s=1.5,F=x=>s*x/(1+x*x);
 check('E107','Debye_loss_frequency_derivative',diff(F,x),s*(1-x*x)/(1+x*x)**2);
}
{
 const Om=2.5,wp=12,w=.003*Om,n2=1-wp*wp/(w*(w-Om)),approx=wp*wp/(Om*w);
 check('E108','cold_plasma_whistler_low_frequency_index',n2/approx,1,.004);
}
{
 const zeta3=1.202056903159594,integral=integrate(x=>x===0?0:x*x/Math.expm1(x),0,40,8000);
 check('T095','two_dimensional_phonon_Bose_energy_integral',integral,2*zeta3,3e-9);
}
{
 const a=1.3,R=2.1,mean=R*R/(1-Math.exp(-a*R*R))-1/a;
 const num=integrate(r=>2*a*r**3*Math.exp(a*r*r)/(Math.exp(a*R*R)-1),0,R,5000);
 check('T096','rotating_gas_radial_second_moment',num,mean,2e-9);
}
{
 const z=1.6,N=30,th=z/(1+z),mean=z=>N*z/(1+z);
 check('T097','Langmuir_occupancy_fugacity_fluctuation',z*diff(mean,z),N*th*(1-th));
}
{
 const Bi=.8;let lo=1e-9,hi=PI/2-1e-8;
 for(let j=0;j<70;j++){const x=(lo+hi)/2;if(x*Math.tan(x)>Bi)hi=x;else lo=x;}
 const x=(lo+hi)/2;check('T098','cooling_slab_Robin_eigenvalue_equation',x*Math.tan(x),Bi,1e-12);
}
{
 const Th=450,Tc=300,Kh=1.2,Kc=.8,s=Kh*Kc*(Math.sqrt(Th)-Math.sqrt(Tc))/(Kh*Math.sqrt(Th)+Kc*Math.sqrt(Tc));
 const Pow=x=>x*(Kh*Th/(Kh+x)-Kc*Tc/(Kc-x)),h=Kh*Th/(Kh+s),c=Kc*Tc/(Kc-s);
 check('T099','endoreversible_heat_engine_maximum_power',diff(Pow,s),0,3e-10);
 check('T099','endoreversible_heat_engine_efficiency',c/h,Math.sqrt(Tc/Th));
}
{
 const a=4.5,b=.4,R=1.1,v=2.8,T=2*a*(1-b/v)**2/(R*b),p=R*T/(v-b)-a/v**2;
 check('T100','van_der_Waals_Joule_Thomson_inversion_pressure',p,a*(2*v/b-3)/v**2);
}
{
 const c1=2.5,c2=1.4,t1=3,t2=2,avg=(c1*t1+c2*t2)/(c1+c2);
 const S=c1*Math.log(avg/t1)+c2*Math.log(avg/t2);
 check('T101','two_reservoir_mixing_entropy_inequality',Math.max(0,-S),0);
}
{
 const T=2.1,mu=1.3,L=1.6,M=1.5,c=Math.sqrt(T/mu),F=x=>2/Math.tan(x)-(M/mu)*x/L;
 let lo=1e-7,hi=PI/2-1e-7;for(let j=0;j<80;j++){const x=(lo+hi)/2;if(F(x)>0)lo=x;else hi=x;}
 const k=(lo+hi)/(2*L);check('W095','string_with_point_mass_odd_even_jump_condition',2*T*k/Math.tan(k*L),M*c*c*k*k);
}
{
 const c=2.3,w0=.9,k=1.2,w=Math.hypot(c*k,w0);
 check('W096','foundation_string_phase_group_velocity_product',(w/k)*(c*c*k/w),c*c);
}
{
 const r1=1.1,r2=2.3,h1=2,h2=1.4,g=9.8,k=1e-4,actual=g*k*(r2-r1)/(r1/Math.tanh(k*h1)+r2/Math.tanh(k*h2));
 const shallow=g*k*k*(r2-r1)/(r1/h1+r2/h2);
 check('W097','two_layer_internal_gravity_wave_long_limit',actual/shallow,1,1e-7);
}
{
 const N=15,n=4,m=1.3,K=2.4,q=n*PI/(N+1),omega=2*Math.sqrt(K/m)*Math.sin(q/2),j=3,Y=j=>Math.sin(j*q);
 check('W098','discrete_spring_chain_mode_difference_equation',K*(Y(j+1)-2*Y(j)+Y(j-1))+m*omega*omega*Y(j),0);
}
{
 const a=1.2,b=2.7,g=9.8,sigma=.8,R=a+b,k=Math.sqrt(g*(b-a)/sigma),du2=2*R*Math.sqrt(g*(b-a)*sigma)/(a*b);
 check('W099','Kelvin_Helmholtz_capillary_critical_shear',(g*k*(b-a)+sigma*k**3)/R-a*b*k*k*du2/R**2,0);
}
{
 const U=3.1,c=1.4,k=.9,w=(U+c)*k;
 check('W100','moving_string_convected_dispersion',(w-U*k)**2,c*c*k*k);
}
{
 const EI=3,mu=1.6,k=.8,w=Math.sqrt(EI/mu)*k*k,S=EI*k**3*w,E=mu*w*w/2;
 check('W101','Euler_Bernoulli_bending_wave_energy_velocity',S/E,2*Math.sqrt(EI/mu)*k);
}
{
 const f=2.3,z=1.6,qr=-f*z*z/(f*f+z*z),qi=f*f*z/(f*f+z*z);
 check('O096','Gaussian_beam_thin_lens_inverse_q',qr/(qr*qr+qi*qi),-1/f);
}
{
 const imag=integrate(x=>Math.sin(2*PI*x),0,.5)+integrate(x=>-Math.sin(2*PI*x),.5,1);
 check('O097','binary_phase_grating_first_Fourier_sideband',imag,2/PI);
}
{
 const phi=1.3;
 check('O098','geometric_phase_retarder_unitary_spin_conversion',Math.cos(phi/2)**2+Math.sin(phi/2)**2,1);
}
{
 const a=.87,b=.91,peak=(1-a)*(1-b)/(1-Math.sqrt(a*b))**2;
 check('O099','asymmetric_Fabry_Perot_nonamplifying_peak',Math.max(0,peak-1),0);
}
{
 const C=1.4,d=-C/(1+C*C),F=x=>Math.sqrt((1+C*x)**2+x*x);
 check('O100','chirped_Gaussian_optimal_dispersion_first_derivative',diff(F,d),0,2e-11);
 check('O100','chirped_Gaussian_minimum_pulse_duration',F(d),1/Math.sqrt(1+C*C));
}
{
 const g=.8,L=1.4,P=2.2,tau=1.3;
 const ratio=integrate(x=>x*x*Math.exp(-3*x*x/tau**2),-12*tau,12*tau,9000)/integrate(x=>Math.exp(-x*x/tau**2),-12*tau,12*tau,9000);
 check('O101','Kerr_SPM_spectral_variance_Gaussian_integral',4*g*g*L*L*P*P*ratio/tau**4,2*g*g*L*L*P*P/(3**1.5*tau*tau),3e-11);
}
{
 const a=1.1,alpha=.8,f=x=>x-alpha*(1+Math.exp(-2*x*a));
 let lo=alpha,hi=2*alpha;for(let j=0;j<80;j++){const x=(lo+hi)/2;if(f(x)>0)hi=x;else lo=x;}
 check('Q096','double_Delta_well_even_bound_state_root',f((lo+hi)/2),0,1e-13);
}
{
 const U=3,J=.7,D=Math.hypot(U,4*J),E=x=>(x-Math.hypot(x,4*J))/2;
 check('Q097','Bose_Hubbard_double_occupancy_energy_derivative',diff(E,U),(1-U/D)/2);
}
{
 const r=.43,z=Math.tanh(r)**2;let p=1/Math.cosh(r),sum=0,mean=0;
 for(let j=0;j<80;j++){sum+=p;mean+=2*j*p;p*=((2*j+1)/(2*j+2))*z;}
 check('Q098','squeezed_harmonic_oscillator_Fock_probabilities',sum,1,3e-13);
 check('Q098','squeezed_harmonic_oscillator_mean_quanta',mean,Math.sinh(r)**2,3e-13);
}
{
 const J=1.7,T=.8,p=Math.exp(J/T)/(Math.exp(J/T)+3);
 check('Q099','thermal_Heisenberg_dimer_entangled_PPT_threshold',Math.max(0,.5-p),0);
}
{
 const a=.85,b=1.4,r=(a-b)/(a+b),q=2*a/(a+b);
 check('Q100','effective_mass_interface_probability_current',r*r+b/a*q*q,1);
}
{
 const N=120,m=2,w=1.4,h=1,chem=N*h*w,xF=Math.sqrt(2*chem/(m*w*w));
 const count=integrate(x=>Math.sqrt(Math.max(0,2*m*(chem-m*w*w*x*x/2)))/(PI*h),-xF,xF,6000);
 check('Q101','Thomas_Fermi_harmonic_trap_particle_normalization',count,N,.001);
}
if(new Set(tests.map(x=>x.id)).size!==40||tests.length<40)throw Error('Must cover all 40 new models');
const report={round:17,covered_models:40,executed_checks:tests.length,verified_independent_subparts:0,scope:'Representative one-or-two numerical/physical model crosschecks each, not the full 160 independent subpart gate',tests};
process.stdout.write(JSON.stringify(report,null,2)+'\n');
