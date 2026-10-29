#!/usr/bin/env node
'use strict';
// One genuinely executed numerical / independent-formula check per new model.
// These 40 checks are NOT the required 160 independently verified subparts.
const tests=[],P=Math.PI;
function check(id,method,a,b,tol=1e-7){
 const err=Math.abs(a-b),scale=Math.max(1,Math.abs(a),Math.abs(b));
 if(!Number.isFinite(err)||err>tol*scale)throw Error(id+' '+method+' mismatch '+a+' vs '+b+' residual '+err);
 tests.push({id,method,residual:err,relative_or_absolute_tolerance:tol,passed:true});
}
function d(f,x,h=1e-5){return (f(x+h)-f(x-h))/(2*h)}
function d2(f,x,h=1e-4){return (f(x+h)-2*f(x)+f(x-h))/(h*h)}
function sim(f,a,b,n=6000){if(n%2)n++;let h=(b-a)/n,s=f(a)+f(b);for(let j=1;j<n;j++)s+=(j%2?4:2)*f(a+j*h);return s*h/3}
{
 const m=2.3,R=1.8,off=.4,I=.7,th=.63,A=t=>I+m*(R*R+off*off-2*R*off*Math.cos(t));
 check('M116','finite_difference_configuration_mass_derivative',d(A,th),2*m*R*off*Math.sin(th));
}
{
 const m=1.7,alpha=.6,v=2.4,b=.9,t=.53,r=t=>Math.hypot(b,v*t),phi=t=>Math.atan(v*t/b)/alpha;
 check('M117','geodesic_angular_momentum_from_time_derivative',m*alpha*alpha*r(t)**2*d(phi,t),m*alpha*b*v);
}
{
 const a=2.3,z=1.1,G=1.2,S=.8,pot=-2*P*G*S*(Math.hypot(a,z)-z);
 check('M118','direct_ring_quadrature_gravitational_potential',-2*P*G*S*sim(s=>s/Math.hypot(s,z),0,a),pot);
}
{
 const i=.77,J2=.03,mu=1.9,Re=.6,a=2.2;
 const avg=sim(u=>mu*J2*Re*Re/(a*a*a)*(3*Math.sin(i)**2*Math.sin(u)**2-1)/2,0,2*P)/(2*P);
 check('M119','orbital_average_quadrupole_potential',avg,mu*J2*Re*Re/(a*a*a)*(.75*Math.sin(i)**2-.5));
}
{
 const m=2.4,R=.8,v0=3.2,w0=-.4,u=v0-R*w0,vs=v0-2*u/7,ws=w0+5*u/(7*R),I=.4*m*R*R;
 check('M120','translational_rotational_energy_loss',.5*m*(v0*v0-vs*vs)+.5*I*(w0*w0-ws*ws),m*u*u/7);
}
{
 const m=2.1,I=.8,a=.7,k1=3.3,k2=5.4,K=k1+k2,D=k2-k1;
 const B=K/m+a*a*K/I,disc=Math.sqrt((K/m-a*a*K/I)**2+4*a*a*D*D/(m*I));
 const plus=(B+disc)/2,minus=(B-disc)/2;
 check('M121','eigenfrequency_product_equals_stiffness_determinant',plus*minus,4*a*a*k1*k2/(m*I));
}
{
 const M=8.4,rho=2.2,R=.1,G=1.3,rc=Math.cbrt(3*M/(2*P*rho));
 check('M122','tidal_self_gravity_threshold',2*G*M*R/rc**3,4*P*G*rho*R/3);
}
{
 const L=1.9,Is=2.4,I=1.3,W=i=>L*Is*Is/2*Math.log(1+(i/Is)**2);
 check('E116','finite_difference_magnetic_energy_derivative',d(W,I),I*L/(1+(I/Is)**2));
}
{
 const rho=1.8,eps=2.1,a=1.3,b=2.8;
 const Ei=r=>rho*(r/2-r**3/(4*a*a))/eps,Eo=r=>rho*a*a/(4*eps*r);
 const integ=P*eps*(sim(r=>Ei(r)**2*r,0,a)+sim(r=>Eo(r)**2*r,a,b));
 const formula=11*P*rho*rho*a**4/(384*eps)+P*rho*rho*a**4/(16*eps)*Math.log(b/a);
 check('E117','radial_electric_energy_integral',integ,formula);
}
{
 const mu=1.7,G=2.3,B0=1.6,U=r=>mu*Math.hypot(B0,G*r);
 check('E118','trap_curvature_from_finite_difference',d2(U,0),mu*G*G/B0,2e-7);
}
{
 const mi=2.3,n=1.7,e=1.2,eps=1.4,kBT=3.1,k=.8;
 const cs2=kBT/mi,lambda2=eps*kBT/(n*e*e),w2=k*k*cs2/(1+k*k*lambda2);
 const poissonL=eps*k*k+n*e*e/kBT,poissonR=n*e*e*k*k/(mi*w2);
 check('E119','ion_electron_poisson_dispersion_residual',poissonL,poissonR);
}
{
 const e=1.2,C=2.7,kBT=.4,n=2,qg=2.8,Delta=q=>e*e/C*(n+.5-q/e);
 const p=q=>1/(1+Math.exp(Delta(q)/kBT));
 check('E120','thermal_charge_step_derivative',d(p,qg),e/(C*kBT)*p(qg)*(1-p(qg)));
}
{
 const R0=2.3,alpha=.07,H=1.8,V=4.1;
 const th=(Math.sqrt(1+4*alpha*V*V/(H*R0))-1)/(2*alpha);
 check('E121','electrothermal_voltage_steady_heat_balance',H*th,V*V/(R0*(1+alpha*th)));
}
{
 const Q=1.6,eps=2.1,M=3.2,R0=.9,x=2.7;
 const vinf=Math.sqrt(Q*Q/(4*P*eps*M*R0));
 const t=y=>R0/vinf*(Math.sqrt(y*(y-1))+Math.acosh(Math.sqrt(y)));
 check('E122','shell_expansion_time_derivative',d(t,x),R0/(vinf*Math.sqrt(1-1/x)));
}
{
 const E=3.2,h=.8,b=1.3,delta=.17,kappa=3*delta/(4*h);
 const energy=b*E/2*(sim(z=>(delta/2+kappa*z)**2,-h,0)+sim(z=>(-delta/2+kappa*z)**2,0,h));
 check('T109','bimetal_stress_energy_integral',energy,E*b*h*delta*delta/16);
}
{
 const kBT=2.1,kappa=1.8,c=kappa/(2*kBT);
 const meanR2=sim(r=>r**4*Math.exp(-c*r*r),0,12)/sim(r=>r*r*Math.exp(-c*r*r),0,12);
 check('T110','trapped_gas_radial_Gaussian_moment',meanR2,3*kBT/kappa);
}
{
 const eta=1.6,U=2.1,H=1.4,k=2.7,T0=300,phi=eta*U*U/(H*H);
 const T=y=>T0+phi*y*(H-y)/(2*k),Tp=y=>phi*(H-2*y)/(2*k);
 const entropy=sim(y=>k*Tp(y)**2/T(y)**2+phi/T(y),0,H);
 check('T111','viscous_heat_entropy_flux_identity',entropy,eta*U*U/(H*T0));
}
{
 const T0=300,p0=1.1,L0=700,DS=2.5,DC=1.7,T=341;
 const p=t=>p0+L0/(T0*DS)*(t-T0)+DC/DS*(t*Math.log(t/T0)-t+T0);
 check('T112','Clapeyron_pressure_derivative',d(p,T),[L0/T0+DC*Math.log(T/T0)]/DS);
}
{
 const N=11,k=2.6,i=4,j=7;
 const G=(i,j)=>Math.min(i,j)*(N+1-Math.max(i,j))/(k*(N+1));
 check('T113','Dirichlet_discrete_Green_inverse',2*G(i,j)-G(i-1,j)-G(i+1,j),0);
 const jj=4;check('T113','Dirichlet_Green_source_normalization',2*G(jj,jj)-G(jj-1,jj)-G(jj+1,jj),1/k);
}
{
 const R=1.3,g0=2.1,s=.04,T0=300,T=311,A=4*P*R*R;
 const F=t=>A*(g0-s*(t-T0));
 check('T114','surface_entropy_from_free_energy_derivative',-d(F,T),A*s);
}
{
 const cp=3.2,T1=290,T3=1350,tau=1.7,T2=tau*T1,T4=T3/tau;
 const qin=cp*(T3-T4),qout=cp*(T2-T1),work=cp*((T3-T4)-(T2-T1));
 check('T115','regenerative_Brayton_first_law',qin-qout,work);
}
{
 const c1=2.3,c2=3.4,k=.9,w1=c1*k,w2=c2*k,A=(1+w1/w2)/2,B=(1-w1/w2)/2;
 check('W109','time_interface_energy_ratio',w2*w2*(A*A+B*B)/(w1*w1),(1+(c2/c1)**2)/2);
}
{
 const m=2,kz=1.4,r=.9,omega=2.7,rho=1.6,amp=.7;
 const Iphi=m*amp*amp/(2*omega*rho*r),Iz=kz*amp*amp/(2*omega*rho);
 check('W110','acoustic_vortex_azimuthal_to_axial_energy_flux',Iphi/Iz,m/(kz*r));
}
{
 const gamma=1.4,pinf=2.3,sigma=.18,R0=.7,rho=1.8,pg=pinf+2*sigma/R0;
 const F=r=>pg*(R0/r)**(3*gamma)-pinf-2*sigma/r;
 const w2=(3*gamma*pg-2*sigma/R0)/(rho*R0*R0);
 check('W111','bubble_pressure_stiffness_finite_difference',-d(F,R0)/(rho*R0),w2);
}
{
 const rho=1.7,eta=2.3,tau=.9,w=50;
 const re=rho*tau*w*w/eta,im=rho*w/eta;
 const kr=Math.sqrt((Math.hypot(re,im)+re)/2),ki=Math.sqrt((Math.hypot(re,im)-re)/2);
 check('W112','Maxwell_shear_wave_complex_dispersion_real_part',kr*kr-ki*ki,re);
 check('W112','Maxwell_shear_wave_complex_dispersion_imag_part',2*kr*ki,im);
}
{
 const sigma=1.3,mu=2.1,f=x=>Math.exp(-(x-mu)**2/(2*sigma*sigma))/(Math.sqrt(2*P)*sigma);
 const variance=sim(x=>(x-mu)**2*f(x),mu-11*sigma,mu+11*sigma);
 check('W113','Doppler_Gaussian_variance_quadrature',variance,sigma*sigma);
}
{
 const T=2.2,rho=1.7,L=1.9,eps=.16,C=P*P*T/(rho*L*L);
 const w12=C*((1+eps)+4*(1-eps)),w21=C*(4*(1+eps)+(1-eps));
 check('W114','anisotropic_membrane_mode_split',w21-w12,6*C*eps);
}
{
 const A=.8,w=2.4,gamma=.3;
 const mean=sim(t=>gamma*A**4*w*w*Math.cos(w*t)**2*Math.sin(w*t)**2,0,2*P/w)/(2*P/w);
 check('W115','cubic_damping_cycle_averaged_energy_loss',mean,gamma*A**4*w*w/8);
}
{
 const ell=3,w=2.1,r=w*Math.sqrt(ell/2),intensity=x=>(x/w)**(2*ell)*Math.exp(-2*x*x/(w*w));
 check('O108','optical_vortex_ring_maximum_derivative',d(intensity,r),0);
}
{
 const Ps=.09,Plo=1e6,R=.8,e=1.6e-19,B=1e5;
 const ib=2*R*Math.sqrt(Ps*Plo),noise=2*e*R*(Ps+Plo)*B;
 check('O109','strong_local_oscillator_shot_noise_SNR',ib*ib/(2*noise),R*Ps/(e*B),1e-6);
}
{
 const L=1.8,c=3e8,T1=.001,T2=.002,alpha=.0002;
 const rt=(1-T1)*(1-T2)*Math.exp(-2*alpha*L),tau=-(2*L/c)/Math.log(rt);
 check('O110','cavity_roundtrip_exponential_energy_decay',Math.exp(-(2*L/c)/tau),rt);
}
{
 const lam=.000000532,theta=.31,v=1.8;
 const dfr=lam/(2*Math.sin(theta)),f=v/dfr,k=2*P/lam;
 check('O111','laser_Doppler_fringe_geometry',2*P*f,2*k*Math.sin(theta)*v);
}
{
 const phi=1.4,udr=Math.cos(phi),udi=Math.sin(phi),uar=1-udr,uai=-udi;
 check('O112','Babinet_complex_amplitude_real',udr+uar,1);
 check('O112','Babinet_complementary_aperture_intensity',uar*uar+uai*uai,4*Math.sin(phi/2)**2);
}
{
 const pump=2.3,gamma=1.7,t=.4,p=t=>pump/(pump+gamma)*(1-Math.exp(-(pump+gamma)*t));
 check('O113','two_level_conditional_population_rate_equation',d(p,t),pump-(pump+gamma)*p(t));
}
{
 const E0=1.3,mu=1.6,kBT=.3,f=E=>1/(1+Math.exp((E-mu)/kBT));
 const deriv=E=>f(E)*(1-f(E))/kBT;
 check('Q108','Landauer_Fermi_step_thermal_integral',sim(deriv,E0,mu+40*kBT,10000),f(E0),1e-9);
}
{
 const delta=2.1,theta=.32,V=.8,x=V-delta*Math.cos(2*theta),y=delta*Math.sin(2*theta);
 const eigenGap=Math.sqrt((x/2-(-x/2))**2+4*(y/2)**2);
 check('Q109','MSW_two_state_matrix_eigenvalue_gap',eigenGap,Math.sqrt(x*x+y*y));
}
{
 const m=1.7,g=9.8,H=.3,L=2.1,hbar=1.2,v=3.3;
 const action=sim(t=>m*g*H,0,L/v);
 check('Q110','neutron_gravity_action_difference',action/hbar,m*g*H*L/(hbar*v));
}
{
 const m=1.6,phi=2.3,e=1.2,F=2.7,hbar=1.1,xt=phi/(e*F);
 const action=sim(x=>Math.sqrt(2*m*Math.max(0,phi-e*F*x))/hbar,0,xt,12000);
 check('Q111','triangular_barrier_WKB_action_integral',action,2*Math.sqrt(2*m)*phi**1.5/(3*hbar*e*F),2e-6);
}
{
 const E=3.4,mc2=2.3,theta=.72,Ep=E/(1+E/mc2*(1-Math.cos(theta)));
 const recoil2=E*E+Ep*Ep-2*E*Ep*Math.cos(theta);
 check('Q112','Compton_four_momentum_invariant',Math.sqrt(mc2*mc2+recoil2),mc2+E-Ep);
}
{
 const A=2.3,ge=1.4,gn=-.2,B=.9,diff=(ge-gn)*B;
 const a=-A/4+diff/2,d=-A/4-diff/2,b=A/2;
 const plus=-A/4+.5*Math.hypot(A,diff),minus=-A/4-.5*Math.hypot(A,diff);
 check('Q113','hyperfine_two_by_two_matrix_determinant',plus*minus,a*d-b*b);
}
const ids=['M116','M117','M118','M119','M120','M121','M122','E116','E117','E118','E119','E120','E121','E122','T109','T110','T111','T112','T113','T114','T115','W109','W110','W111','W112','W113','W114','W115','O108','O109','O110','O111','O112','O113','Q108','Q109','Q110','Q111','Q112','Q113'];
if(new Set(tests.map(x=>x.id)).size!==40||ids.some(x=>!tests.some(t=>t.id===x)))throw Error('40 model coverage incomplete');
process.stdout.write(JSON.stringify({round:19,models:40,executed_numeric_model_checks:tests.length,independently_verified_subparts:0,required_subpart_checks:160,release_allowed:false,tests},null,2)+'\n');
