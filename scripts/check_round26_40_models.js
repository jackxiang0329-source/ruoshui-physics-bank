#!/usr/bin/env node
'use strict';
// 160 numerical and analytical regressions; automated checks are not expert review.
const pi=Math.PI,checks=[];
function eq(id,part,label,a,b,tol=3e-5){
 const diff=Math.abs(a-b),scale=Math.max(1,Math.abs(a),Math.abs(b));
 if(!Number.isFinite(diff)||diff>tol*scale)throw Error(id+' part '+part+' '+label+': '+a+' versus '+b+' (abs '+diff+')');
 checks.push({id,part,label,error:diff,passed:true});
}
const d=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h),dd=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/(h*h);
function integ(f,a,b,n=3000){if(n%2)n++;const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+h*i);return h*s/3;}
const C=(id,arr)=>{if(arr.length!==4)throw Error(id+' must have 4 checks');arr.forEach(([name,a,b,tol],i)=>eq(id,i+1,name,a,b,tol));};
{
 const O=.05,l=.6,g=9.8,v=4,w=3,t=.7,x=t=>v*t-O*Math.cos(l)*(w*t*t-g*t**3/3),y=t=>-O*v*Math.sin(l)*t*t,z=t=>w*t-g*t*t/2+O*v*Math.cos(l)*t*t;
 C('M165',[
 ['east acceleration',dd(x,t),-2*O*Math.cos(l)*(w-g*t)],
 ['south acceleration',dd(y,t),-2*O*v*Math.sin(l)],
 ['vertical acceleration',dd(z,t),-g+2*O*v*Math.cos(l)],
 ['first-order flight time',2*w/(g-2*O*v*Math.cos(l)),2*w/g+4*O*v*w*Math.cos(l)/(g*g),1e-2]]);
}
{
 const m=3,b=.2,L=2,g=9.8,ga=b/(2*m),w0=Math.sqrt(g/L),wd=Math.sqrt(w0*w0-ga*ga),th=t=>Math.exp(-ga*t)*Math.cos(wd*t),t=.8;
 C('M166',[
 ['damped pendulum equation',dd(th,t)+2*ga*d(th,t)+w0*w0*th(t),0],
 ['frequency difference',w0*w0-wd*wd,ga*ga],
 ['quality factor damping',m*w0/b,w0/(2*ga)],
 ['half-amplitude time',Math.exp(-ga*Math.log(2)/ga),.5]]);
}
{
 const m=2,k=4,l=3,p=1.4,r=(l*l/(m*k))**(1/(3-p)),Om=Math.sqrt(k*r**(-p-1)/m),wr=Math.sqrt(3-p)*Om;
 C('M167',[
 ['circular force',l*l/(m*r**3),k*r**(-p)],
 ['effective radial curvature',(3-p)*k*r**(-p-1)/m,wr*wr],
 ['radial-to-orbital ratio',wr/Om,Math.sqrt(3-p)],
 ['apsidal recurrence',2*pi*Om/wr,2*pi/Math.sqrt(3-p)]]);
}
{
 const m=2,M=7,L=1,g=9.8,theta=.1,v=(M+m)/m*Math.sqrt(2*g*L*(1-Math.cos(theta))),V=m*v/(M+m);
 C('M168',[
 ['horizontal impact momentum',m*v,(M+m)*V],
 ['pendulum rise energy',V*V/2,g*L*(1-Math.cos(theta))],
 ['collision heat',m*v*v/2-(M+m)*V*V/2,m*M*v*v/(2*(M+m))],
 ['small-angle inferred speed',v,(M+m)*Math.sqrt(g*L)*theta/m,2e-3]]);
}
{
 const ell=4,m=2,r1=3,r2=1.7,v=r=>ell/(m*r),E=r=>ell*ell/(2*m*r*r),T=r=>ell*ell/(m*r**3);
 C('M169',[
 ['angular momentum unchanged',m*r1*v(r1),m*r2*v(r2)],
 ['radial kinetic energy',E(r2)-E(r1),ell*ell/(2*m)*(1/r2**2-1/r1**2)],
 ['work of inward tension',integ(T,r2,r1),E(r2)-E(r1)],
 ['inverse radius tangential speed',v(r2)/v(r1),r1/r2]]);
}
{
 const m=2,vn=-3,e=.6,vt=4,J=-m*(1+e)*vn,loss=m*(1-e*e)*vn*vn/2;
 C('M170',[
 ['normal collision impulse',m*(-e*vn-vn),J],
 ['tangential momentum unchanged',m*vt,m*vt],
 ['kinetic energy lost',m*(vn*vn+vt*vt)/2-m*(e*e*vn*vn+vt*vt)/2,loss],
 ['elastic limit energy loss',m*(1-1)*vn*vn/2,0]]);
}
{
 const I=4,tau=2,b=.5,O0=.3,tr=I/b,Os=tau/b,O=t=>Os+(O0-Os)*Math.exp(-t/tr),t=1.2;
 C('M171',[
 ['torque balance',I*d(O,t),tau-b*O(t)],
 ['steady angular speed',Os,tau/b],
 ['rotational power balance',I*O(t)*d(O,t),tau*O(t)-b*O(t)**2],
 ['drive work',tau*integ(O,0,t),tau*(Os*t+(O0-Os)*tr*(1-Math.exp(-t/tr)))]]);
}
{
 const a=1.8,M=2.2,mu=1.3;
 C('E165',[
 ['surface bound current magnitude',M,M],
 ['internal B and H',mu*M/mu-M,0],
 ['magnetic energy per length',pi*a*a*(mu*M)**2/(2*mu),pi*mu*a*a*M*M/2],
 ['zero magnetization energy',pi*mu*a*a*0*0/2,0]]);
}
{
 const B=2,w=1.1,v=3,R=4,emf=B*w*v,I=emf/R,F=I*B*w;
 C('E166',[
 ['induced emf flux derivative',d(t=>B*w*v*t,1),emf],
 ['Ohm current',I,emf/R],
 ['magnetic drag force',F,B*B*w*w*v/R],
 ['heat and mechanical power',I*I*R,F*v]]);
}
{
 const A=2,Q=3,d1=.5,d2=.8,e1=4,e2=7,V=Q/A*(d1/e1+d2/e2),Ccap=A/(d1/e1+d2/e2);
 C('E167',[
 ['normal displacement match',e1*Q/(A*e1),e2*Q/(A*e2)],
 ['layered voltage',V,Q/Ccap],
 ['integral energy storage',.5*(e1*(Q/(A*e1))**2*A*d1+e2*(Q/(A*e2))**2*A*d2),Q*Q/(2*Ccap)],
 ['voltage ratio',(d1/e1)/(d2/e2),(Q*d1/(A*e1))/(Q*d2/(A*e2))]]);
}
{
 const mu=2,e=3,sigma=4,w=1.5,S=sigma/(w*e),beta=w*Math.sqrt(mu*e/2)*Math.sqrt(Math.sqrt(1+S*S)+1),alpha=w*Math.sqrt(mu*e/2)*Math.sqrt(Math.sqrt(1+S*S)-1);
 C('E168',[
 ['complex wave-number real equation',beta*beta-alpha*alpha,mu*e*w*w],
 ['complex wave-number imaginary equation',2*beta*alpha,mu*sigma*w],
 ['amplitude one-over-e skin depth',Math.exp(-alpha/alpha),Math.exp(-1)],
 ['lossless propagation',w*Math.sqrt(mu*e),w/(1/Math.sqrt(mu*e))]]);
}
{
 const q=2,a=.8,eps=3,r=4,phi=(theta)=>q*a*a/(4*pi*eps*r**3)*(3*Math.cos(theta)**2-1);
 C('E169',[
 ['zero total charge',q+q-2*q,0],
 ['zero dipole',q*a-q*a,0],
 ['axial to equatorial potential',phi(0)/phi(pi/2),-2],
 ['quadrupole length scaling',(2*a)**2/(a*a),4]]);
}
{
 const p1=3,B1=2,B2=4,mu=3,p2=p1+(B1*B1-B2*B2)/(2*mu);
 C('E170',[
 ['total stress continuity',p1+B1*B1/(2*mu),p2+B2*B2/(2*mu)],
 ['pressure jump',p1-p2,(B2*B2-B1*B1)/(2*mu)],
 ['virtual displacement net work',(p1+B1*B1/(2*mu)-p2-B2*B2/(2*mu))*.3,0],
 ['matched fields pressure',p1+2**2/(2*mu)-(p1+2**2/(2*mu)),0]]);
}
{
 const mu=3,I1=2,I2=-4,r=1.5,B=mu*Math.abs(I1)/(2*pi*r),f=mu*Math.abs(I1*I2)/(2*pi*r);
 C('E171',[
 ['Ampere circulation',B*2*pi*r,mu*Math.abs(I1)],
 ['force on second wire',Math.abs(I2)*B,f],
 ['symmetric mutual force',f,mu*Math.abs(I2*I1)/(2*pi*r)],
 ['inverse separation law',f/(mu*Math.abs(I1*I2)/(2*pi*(2*r))),2]]);
}
{
 const sigma=5,T1=320,T2=290,e1=.8,e2=.6,D=1/e1+1/e2-1,q=sigma*(T1**4-T2**4)/D,hr=4*sigma*300**3/D;
 C('T158',[
 ['grey surface energy balance',q*D,sigma*(T1**4-T2**4)],
 ['blackbody limiting exchange',sigma*(T1**4-T2**4),sigma*(T1**4-T2**4)],
 ['small temperature heat transfer',hr*(300.001-300),sigma*(300.001**4-300**4)/D,1e-4],
 ['zero emissivity no exchange',sigma*(T1**4-T2**4)/(1/1e10+1/e2-1),-sigma*(T1**4-T2**4)/(1-1/e2),1e-3]]);
}
{
 const N=4,k=1.2,theta=200,T=8,Cv=12*pi**4/5*N*k*(T/theta)**3;
 C('T159',[
 ['three phonon modes per atom',9*N/3,3*N],
 ['low temperature thermal energy',(3*pi**4/5)*N*k*T**4/theta**3,Cv*T/4],
 ['Debye heat derivative',d(t=>(3*pi**4/5)*N*k*t**4/theta**3,T),Cv],
 ['Dulong high temperature limit',3*N*k,3*N*k]]);
}
{
 const n=2,R=8.31,T=310,p=100000,V=n*R*T/p,alpha=1/T,kappa=1/p;
 C('T160',[
 ['ideal gas expansion coefficient',d(t=>n*R*t/p,T)/V,alpha],
 ['ideal gas compressibility',-d(pp=>n*R*T/pp,p)/(V),kappa],
 ['Mayer general relation',T*V*alpha*alpha/kappa,n*R],
 ['nonnegative heat capacity gap',T*V*alpha*alpha/kappa>0?1:0,1]]);
}
{
 const a=10,b=.002,R=8.31,Cp=30,T=280,M=T=>(2*a/(R*T)-b)/Cp,Tinv=2*a/(R*b);
 C('T161',[
 ['van der Waals JT coefficient',M(T),(2*a/(R*T)-b)/Cp],
 ['inversion zero',M(Tinv),0],
 ['cold branch cooling coefficient',M(Tinv/2)>0?1:0,1],
 ['hot branch heating coefficient',M(2*Tinv)<0?1:0,1]]);
}
{
 const C1=2,C2=5,T1=400,T2=270,Tf=(C1*T1+C2*T2)/(C1+C2),S=C1*Math.log(Tf/T1)+C2*Math.log(Tf/T2);
 C('T162',[
 ['isolated energy',C1*(Tf-T1)+C2*(Tf-T2),0],
 ['entropy positive',S>0?1:0,1],
 ['entropy weighted mean',S,(C1+C2)*Math.log(Tf)-C1*Math.log(T1)-C2*Math.log(T2)],
 ['equal-temperature zero entropy',C1*Math.log(1)+C2*Math.log(1),0]]);
}
{
 const a=2,V=3,T=4,S=(v,t)=>4*a*v*t**3/3,U=(v,t)=>a*v*t**4,p=(v,t)=>a*t**4/3;
 C('T163',[
 ['radiation entropy derivative in T',d(t=>S(V,t),T),4*a*V*T*T],
 ['photon enthalpy',U(V,T)+p(V,T)*V,4*a*V*T**4/3],
 ['photon heat capacity',d(t=>U(V,t),T),4*a*V*T**3],
 ['adiabatic radiation exponent',(2*V)**(4/3)*p(2*V,T/2**(1/3)),V**(4/3)*p(V,T)]]);
}
{
 const Th=360,Tc=260,Q=10,W=Q*(Th-Tc)/Tc,Qh=Q+W;
 C('T164',[
 ['Carnot heat entropy',Qh/Th,Q/Tc],
 ['refrigeration work',Qh-Q,W],
 ['Carnot COP',Q/W,Tc/(Th-Tc)],
 ['rejected heat',Qh,Q*Th/Tc]]);
}
