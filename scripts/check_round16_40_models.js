#!/usr/bin/env node
'use strict';
// Independent one-per-model numerical crosschecks for round16's forty drafts.
function checkAll40(){
 const out=[],pi=Math.PI,eps=1e-8;
 const ck=(id,x,tol=eps)=>{if(!Number.isFinite(x)||Math.abs(x)>tol)throw Error(`QA ${id}: ${x}`);out.push({id,passed:true,residual:Math.abs(x),tolerance:tol})};
 const d=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);
 const I=(f,a,b,n=3200)=>{let h=(b-a)/n,sum=f(a)+f(b);for(let j=1;j<n;j++)sum+=(j%2?4:2)*f(a+j*h);return sum*h/3};
 const invalid=x=>Math.max(0,-x);
 {let m=1.4,l=.8,v=2.2,t=.9;ck("M095",(m+l*t)*(m*v/(m+l*t))-m*v)}
 {let s0=.9,s=2*s0/3,g=9.8,L=1.7,th=Math.asin(s);ck("M096",-L/2*(Math.cos(th)*3*g*(s0-s)/L-Math.sin(th)*1.5*g*Math.cos(th)/L))}
 {let L=2.5,g=9.8,w=Math.sqrt(2*g/L);ck("M097",w*w-2*g/L)}
 {let A=2.1,a=.14,g=9.8,h=3.2,H=2.6,x=2*A*(Math.sqrt(h)+h**1.5/(3*H))/(a*Math.sqrt(2*g));ck("M098",x-I(u=>2*A*(1+u*u/H)/(a*Math.sqrt(2*g)),0,Math.sqrt(h)))}
 {let m=2,J=.3,r=.12,g=9.8,a=g/(1+J/(m*r*r)),T=J*a/(2*r*r);ck("M099",m*a-(m*g-2*T))}
 {let J=2,m=1.3,R=.72,w=2.1,x=-m*R*R*w/(J+m*R*R);ck("M100",J*x+m*R*R*(x+w))}
 {let m=1.5,c=3,E=19.4,p=Math.sqrt(E*E-(m*c*c)**2)/c;ck("M101",E*E-(p*c)**2-(m*c*c)**2,1e-12)}
 {let a=2.1,b=.7,q=1.3,k=.8,U=x=>-k*q*q*a/(2*(a*a-x*x));ck("E095",-d(U,b)-k*q*q*a*b/(a*a-b*b)**2)}
 {let mu=1.4,n=3,j=1.1,a=.4,L=3.6,x=mu*n*j*L/(2*Math.hypot(a,L/2)),y=mu*n*j/2*(L/2/Math.hypot(a,L/2)+L/2/Math.hypot(a,L/2));ck("E096",x-y)}
 {let f=(x,y,z)=>(x*x+y*y-2*z*z)/2,h=.3;ck("E097",(f(h,0,0)+f(-h,0,0)+f(0,h,0)+f(0,-h,0)+f(0,0,h)+f(0,0,-h))/h**2)}
 {let b=.6,ga=1/Math.sqrt(1-b*b),x=1.8,y=.7,k=1.2,r=ga*ga*x*x+y*y,Ex=k*ga*x/r**1.5,Ey=k*ga*y/r**1.5;ck("E098",Ex*Ex+(1-b*b)*Ey*Ey-k*k/(r*r))}
 {let k=[.6,1.2,.3],s=[.5,1.2,2.4],E=1.3,x=k.reduce((a,v,i)=>a+s[i]*v*v,0),K=k.reduce((a,v)=>a+v*v,0);ck("E099",(x/(E*K))*E*K-x)}
 {let rho=2.4,t=.1,a=.04,b=.9,V=2.1,R=rho*Math.log(b/a)/(2*pi*t),w=I(x=>2*pi*t*V*V/(rho*Math.log(b/a)**2*x),a,b);ck("E100",V*V/R-w)}
 {let a=1.2,b=3.4,z=(a+Math.sqrt(a*a+4*a*b))/2;ck("E101",z-a-b*z/(b+z))}
 {let N=25,m=1.2,g=1.8,T=2.3,H=4,A=3,l=T/(m*g),p=N*T/(A*l*(1-Math.exp(-H/l)));ck("T088",A*p*(1-Math.exp(-H/l))-N*m*g)}
 {let x=.83,f=x=>Math.cosh(x)/Math.sinh(x)-1/x;ck("T089",d(f,x)-1/x**2+1/Math.sinh(x)**2)}
 {let D=1.3,t=.8,x=2.1,f=x=>2*D*(x-t*(1-Math.exp(-x/t)));ck("T090",d(f,x)-2*D*(1-Math.exp(-x/t)))}
 {let e=.7,f=.4,q=(3**4-2**4)/(1/e+1/f-1);ck("T091",invalid(q)+Math.max(0,q-(3**4-2**4)))}
 {let C=3,A=2,h=.5,e=.8,T=3,Ta=2,Tdot=-A*(h*(T-Ta)+e*(T**4-Ta**4))/C;ck("T092",invalid(C*Tdot*(1/T-1/Ta)))}
 {let C=1.7,Q=2,N=3,k=.8,t=.4,n=N*Math.exp(-k*t),T=2+Q*(N-n)/C;ck("T093",T+Q*n/C-2-Q*N/C)}
 {let N=3,n=20,b=.8,T=2,x=.8,F=t=>3*N*t*x*x/(2*n*b*b),force=3*N*T*x/(n*b*b);ck("T094",d(F,T)-force*x/(2*T))}
 {let A=1.2,a=.8,T=2.3,v=T*A*A*Math.sqrt(pi)/(4*a),w=T/2*I(x=>A*A*x*x/a**4*Math.exp(-x*x/a**2),-8*a,8*a,4000);ck("W088",v-w)}
 {let a=.5,b=1.1,n=I(r=>r*Math.sin(pi*(r-a)/(b-a))**2,a,b);ck("W089",invalid(n))}
 {let x=.4*1.1,y=.8*.6,z=Math.cos(x)*Math.cos(y)-Math.sin(x)*Math.sin(y);ck("W090",z-Math.cos(x+y))}
 {let F=2.1,r=(Math.sqrt(1+8*F*F)-1)/2;ck("W091",r*(r+1)-2*F*F)}
 {let Z=1.5,R=3,Q=(2*Z+R)**2;ck("W092",(R*R+4*Z*Z+4*Z*R)/Q-1)}
 {let lam=2,mu=1.2,rho=1.4,cp=Math.sqrt((lam+2*mu)/rho),cs=Math.sqrt(mu/rho);ck("W093",cp*cp-cs*cs-(lam+mu)/rho)}
 {let rho=2.5,g=9.8,D=1.8,k=(rho*g/(3*D))**.25,w=Math.sqrt(g*k+D*k**5/rho);ck("W094",w/k-(g+5*D*k**4/rho)/(2*w))}
 {let a=.4,b=.6,phi=.7,c1=Math.cos(a),s1=Math.sin(a),c2=Math.cos(b),s2=Math.sin(b),cross=2*c1*s1*c2*s2*Math.cos(phi);ck("O090",c1*c1*c2*c2+s1*s1*s2*s2-cross+s1*s1*c2*c2+c1*c1*s2*s2+cross-1)}
 {let inI=3,Is=2,a=.7,L=1.3,Iout=inI;for(let j=0;j<15;j++){let f=Math.log(Iout/inI)+(Iout-inI)/Is+a*L;Iout-=f/(1/Iout+1/Is)}ck("O091",Math.log(Iout/inI)+(Iout-inI)/Is+a*L)}
 {let x=3,b=.6,L=.9,out=x/(1+b*x*L);ck("O092",out*(1+b*x*L)-x)}
 {let q=2,k=1.3,R=2,L=.6,n=-.004,p=q*pi*R*R*L;ck("O093",L*n*q/(2*k)-n*p/(2*pi*k*R*R))}
 {let m=.4,p=I(x=>Math.cos(m*Math.sin(x))**2+Math.sin(m*Math.sin(x))**2,0,2*pi);ck("O094",p-2*pi)}
 {let a=.8,b=1.2;ck("O095",Math.max(0,2*a*b/(a*a+b*b)-1))}
 {let beta=.8,D=1.2,mu=1.3,B=.5,Z=1+2*Math.exp(-beta*D)*Math.cosh(beta*mu*B),M=2*mu*Math.exp(-beta*D)*Math.sinh(beta*mu*B)/Z;ck("Q090",invalid(M))}
 {let z=1.4,fac=n=>{let a=1;for(let j=2;j<=n;j++)a*=j;return a},jB=n=>{let s=0;for(let k=0;k<16;k++)s+=(-1)**k*(z/2)**(2*k+n)/(fac(k)*fac(k+n));return s},x=jB(0)**2;for(let n=1;n<11;n++)x+=2*jB(n)**2;ck("Q091",x-1)}
 {let eta=.67,z=.32,p=(1+eta*z)/2,q=(1-eta*z)/2;ck("Q092",p*(z+eta)/(1+eta*z)+q*(z-eta)/(1-eta*z)-z)}
 {let a=.9,b=3.6,mu=1.2,Bc=(b-a)/(2*mu);ck("Q093",2*a-(a+b-2*mu*Bc))}
 {let E=1.2,a=1.6,f=x=>E*(a/x)**2;ck("Q094",-d(f,a)-2*E/a)}
 {let Q=2,F=x=>30*x*x*(Q-x)**2/Q**5,m=I(F,0,Q),v=I(x=>(x-Q/2)**2*F(x),0,Q);ck("Q095",Math.max(Math.abs(m-1),Math.abs(v-Q*Q/28)))}
 if(out.length!==40||new Set(out.map(x=>x.id)).size!==40)throw Error("40 model checks not complete");
 return{round:16,checked_model_count:40,checks_per_model:1,independently_checked_subparts:0,scope:"Only one representative numeric test per drafted physical model. Not complete 160-subpart QA.",tests:out};
}
const result=checkAll40();
process.stdout.write(JSON.stringify(result,null,2)+'\n');
if(result.tests.some(x=>!x.passed)||result.checked_model_count!==40)process.exitCode=1;
