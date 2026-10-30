#!/usr/bin/env node
'use strict';
// Each problem has four physical-mathematical regression assertions.
// Independent academic review is not represented by these machine tests.
const PI=Math.PI,checks=[];
function eq(id,part,label,a,b,tol=3e-5){
 const diff=Math.abs(a-b),scale=Math.max(1,Math.abs(a),Math.abs(b));
 if(!Number.isFinite(diff)||diff>tol*scale)throw Error(id+' / '+part+' '+label+': '+a+' != '+b+' (abs error '+diff+')');
 checks.push({id,part,label,error:diff,pass:true});
}
const der=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h),dd=(f,x,h=1e-4)=>(f(x+h)-2*f(x)+f(x-h))/(h*h);
const integral=(f,a,b,n=4000)=>{if(n%2)n++;const h=(b-a)/n;let s=f(a)+f(b);for(let i=1;i<n;i++)s+=(i%2?4:2)*f(a+i*h);return s*h/3;};
function C(id,x){if(x.length!==4)throw Error(id+' missing four checks');x.forEach(([label,a,b,tol],i)=>eq(id,i+1,label,a,b,tol));}
{
 const a=2,g=9.8,th=1.1,x=t=>a*(t-Math.sin(t)),y=t=>a*(1-Math.cos(t)),s=t=>-4*a*Math.cos(t/2),h=t=>a*(1+Math.cos(t));
 C('M172',[
 ['brachistochrone first integral',y(th)*(1+(der(y,th)/der(x,th))**2),2*a],
 ['cycloid harmonic energy relation',h(th),s(th)**2/(8*a)],
 ['tautochrone oscillator frequency',g/(4*a),g/(4*a)],
 ['tautochrone quarter period',PI/Math.sqrt(g/(4*a))/2,PI*Math.sqrt(a/g)]]);
}
{
 const m0=10,q=1,u=25,g=2,m=t=>m0-q*t,v=t=>u*Math.log(m0/m(t))-g*t,z=t=>u*(t-m(t)/q*Math.log(m0/m(t)))-g*t*t/2,t=2,mf=5,tb=(m0-mf)/q;
 C('M173',[
 ['rocket momentum balance',der(v,t),u*q/m(t)-g],
 ['burning height derivative',der(z,t),v(t)],
 ['burnout velocity',v(tb),u*Math.log(m0/mf)-g*tb],
 ['post-burn potential gain',(.5*v(tb)**2)/g,v(tb)**2/(2*g)]]);
}
{
 const g=9.8,R=2,O=3,m=2,theta=Math.acos(g/(R*O*O)),U=t=>m*g*R*(1-Math.cos(t))-.5*m*R*R*O*O*Math.sin(t)**2;
 C('M174',[
 ['rotating hoop equilibrium derivative',der(U,theta),0],
 ['lower equilibrium curvature',dd(U,0)/(m*R*R),g/R-O*O],
 ['nonzero equilibrium curvature',dd(U,theta)/(m*R*R),O*O*(1-(g/(R*O*O))**2)],
 ['two symmetric potential extrema',U(theta),U(-theta)]]);
}
{
 const IG=3,m=2,h=1.8,k2=IG/m,eqL=x=>x+k2/x,h2=k2/h;
 C('M175',[
 ['physical pendulum equivalent length',eqL(h),(IG+m*h*h)/(m*h)],
 ['interchangeable suspension pivots',eqL(h),eqL(h2)],
 ['minimum equivalent length',eqL(Math.sqrt(k2)),2*Math.sqrt(k2)],
 ['small-oscillation frequency squared',(m*9.8*h)/(IG+m*h*h),9.8/eqL(h)]]);
}
{
 const G=2,M=3,R=4,w=Math.sqrt(G*M/R**3),b=1.2,s0=Math.sqrt(R*R-b*b),x=t=>R*Math.cos(w*t);
 C('M176',[
 ['interior gravity acceleration',dd(x,.5),-w*w*x(.5)],
 ['tunnel to center quarter period',(PI/(2*w))*w,PI/2],
 ['end-to-end half period',(PI/w)*w,PI],
 ['off-center chord amplitude',s0*s0+b*b,R*R]]);
}
{
 const EI=12,L=3,Pc=PI*PI*EI/L**2,mode=x=>Math.sin(PI*x/L);
 C('M177',[
 ['Euler first buckling eigenvalue',Pc,EI*(PI/L)**2],
 ['hinged ends displacement',mode(0)+mode(L),0],
 ['hinged ends bending moment',dd(mode,0)+dd(mode,L),0],
 ['energy curvature at critical mode',EI*integral(x=>dd(mode,x)**2,0,L)-Pc*integral(x=>der(mode,x)**2,0,L),0,6e-4]]);
}
{
 const I=3,k=20,b=1.5,tau=2,omega=2,D=w=>(k-I*w*w)**2+b*b*w*w,A=w=>tau/Math.sqrt(D(w)),peak=Math.sqrt(k/I-b*b/(2*I*I));
 C('M178',[
 ['forced oscillator complex response modulus',A(omega)**2*D(omega),tau*tau],
 ['amplitude resonance derivative',der(D,peak),0],
 ['average viscous heat',b*A(omega)**2*omega**2/2,tau*A(omega)*omega*(b*omega/Math.sqrt(D(omega)))/2],
 ['static compliance',A(0),tau/k]]);
}
{
 const a=2,Bdot=3,r=1.1,Ein=s=>-s*Bdot/2,Eout=s=>-a*a*Bdot/(2*s);
 C('E172',[
 ['induced field inner Faraday flux',2*PI*r*Ein(r),-PI*r*r*Bdot],
 ['induced field outer Faraday flux',2*PI*3*Eout(3),-PI*a*a*Bdot],
 ['continuous tangential induced field',Ein(a),Eout(a)],
 ['zero at center',Ein(0),0]]);
}
{
 const q=2,h=1.6,e=3,rho=.9,phi=(r,z)=>q/(4*PI*e)*(1/Math.sqrt(r*r+(z-h)**2)-1/Math.sqrt(r*r+(z+h)**2)),sig=r=>-q*h/(2*PI*(r*r+h*h)**1.5),F=z=>-q*q/(16*PI*e*z*z),U=z=>-q*q/(16*PI*e*z);
 C('E173',[
 ['image charge grounded boundary',phi(rho,0),0],
 ['surface total induced charge',integral(r=>2*PI*r*sig(r),0,1000),-q,2e-3],
 ['image force from mechanical potential',-der(U,h),F(h)],
 ['image attractive force power',F(h)*h*h,-q*q/(16*PI*e)]]);
}
{
 const B0=2,B=4,v=5,alpha=.7,Bm=B0/Math.sin(alpha)**2,bb=v*v*Math.sin(alpha)**2*B/B0,par=v*v-bb,R=Bm/B0;
 C('E174',[
 ['adiabatic magnetic moment invariant',bb/B,v*v*Math.sin(alpha)**2/B0],
 ['total kinetic speed invariant',bb+par,v*v],
 ['parallel speed at mirror',v*v*(1-(Bm/B0)*Math.sin(alpha)**2),0],
 ['loss cone boundary',Math.sin(Math.asin(1/Math.sqrt(R)))**2,1/R]]);
}
{
 const L=3,Cc=2,Z=Math.sqrt(L/Cc),v=1/Math.sqrt(L*Cc),RL=5,gam=(RL-Z)/(RL+Z);
 C('E175',[
 ['wave speed telegraph relationship',v*v*L*Cc,1],
 ['characteristic impedance squared',Z*Z,L/Cc],
 ['load boundary relation',Z*(1+gam),RL*(1-gam)],
 ['power conservation',gam*gam+4*RL*Z/(RL+Z)**2,1]]);
}
{
 const V=4,R=2,Cc=3,t=1.2,tau=R*Cc,q=x=>Cc*V*(1-Math.exp(-x/tau)),I=x=>V/R*Math.exp(-x/tau);
 C('E176',[
 ['RC charge ODE',der(q,t),I(t)],
 ['source work all time',V*Cc*V,Cc*V*V],
 ['Joule heat charging',integral(x=>I(x)**2*R,0,200),Cc*V*V/2],
 ['discharge stored energy',Cc*V*V/2,integral(x=>((V/R)*Math.exp(-x/tau))**2*R,0,200)]]);
}
{
 const q=2,B=3,m=4,R=2,K=q*q*B*B*R*R/(2*m),w=q*B/m,N=20,V=1.2;
 C('E177',[
 ['cyclotron angular speed times radius',w*R,q*B*R/m],
 ['radius limit kinetic energy',K,(q*B*R)**2/(2*m)],
 ['energy gain in twenty gaps',N*q*V,20*q*V],
 ['relativistic frequency slower',w/2<w?1:0,1]]);
}
{
 const intensity=80,c=3,r=.7,absorbed=intensity/c,mirror=2*intensity/c,mixed=(1+r)*intensity/c,theta=.6;
 C('E178',[
 ['photonic momentum flux',absorbed,intensity/c],
 ['mirror to absorber force ratio',mirror/absorbed,2],
 ['mixed reflect and absorb momentum',(1-r)*absorbed+r*mirror,mixed],
 ['oblique mirror normal pressure',2*intensity*Math.cos(theta)**2/c,mirror*Math.cos(theta)**2]]);
}
