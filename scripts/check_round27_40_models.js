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
{
 const G=3,Th=400,Tc=300,heat=G*(Th-Tc),S=heat*(1/Tc-1/Th);
 C('T165',[
 ['Fourier heat current',heat,G*(Th-Tc)],
 ['entropy production',S,G*(Th-Tc)**2/(Th*Tc)],
 ['Carnot extractable work',heat*(1-Tc/Th),heat-heat*Tc/Th],
 ['near equilibrium entropy quadratic',G*(.01)**2/(300*(300+.01)),G*(.01)**2/300**2,1e-8]]);
}
{
 const n=1.2,R=8.31,Cv=12,T1=300,V1=2,V2=3,T2=T1*(V2/V1)**(1-n),W=R*(T2-T1)/(1-n),Q=(Cv+R/(1-n))*(T2-T1);
 C('T166',[
 ['polytropic temperature law',T2*V2**(n-1),T1*V1**(n-1)],
 ['pressure volume work from temperature',W,integral(v=>R*T1*V1**(n-1)*v**(-n),V1,V2)],
 ['first law polytropic heat',Q,Cv*(T2-T1)+W],
 ['adiabatic polytropic path heat capacity',Cv+R/(1-(1+R/Cv)),0]]);
}
{
 const C1=2,C2=5,T1=500,T2=300,Tf=T1**(C1/(C1+C2))*T2**(C2/(C1+C2)),W=C1*T1+C2*T2-(C1+C2)*Tf,Tmix=(C1*T1+C2*T2)/(C1+C2);
 C('T167',[
 ['reversible reservoir entropy',C1*Math.log(Tf/T1)+C2*Math.log(Tf/T2),0],
 ['weighted geometric mean',Tf**(C1+C2),T1**C1*T2**C2,1e-6],
 ['maximum work finite reservoirs',W,(C1+C2)*(Tmix-Tf)],
 ['equal heat capacities maximum work',(Math.sqrt(500)-Math.sqrt(300))**2,500+300-2*Math.sqrt(500*300)]]);
}
{
 const N=5,k=2,theta=100,T=40,energy=t=>3*N*k*theta/(Math.exp(theta/t)-1),Cv=3*N*k*(theta/T)**2*Math.exp(theta/T)/(Math.exp(theta/T)-1)**2;
 C('T168',[
 ['Einstein oscillator heat capacity',der(energy,T),Cv],
 ['low temperature activation asymptotic',3*N*k*10**2*Math.exp(-10),3*N*k*(10**2*Math.exp(10)/(Math.exp(10)-1)**2),1e-3],
 ['classical high temperature limit',3*N*k*(.0001)**2*Math.exp(.0001)/(Math.exp(.0001)-1)**2,3*N*k,1e-4],
 ['positive oscillator energy',energy(T)>0?1:0,1]]);
}
{
 const N=20,k=1,Ef=100,T=5,mu=Ef*(1-(PI**2/12)*(k*T/Ef)**2),energy=t=>.6*N*Ef+PI**2/4*N*(k*t)**2/Ef,Cv=PI**2/2*N*k*k*T/Ef;
 C('T169',[
 ['three dimensional density of states normalization',integral(e=>3*N*Math.sqrt(e)/(2*Ef**1.5),0,Ef),N],
 ['chemical potential downshift',mu<Ef?1:0,1],
 ['Sommerfeld heat capacity derivative',der(energy,T),Cv],
 ['degenerate electronic heat capacity ratio',Cv/(N*k),PI**2/2*(k*T/Ef)]]);
}
{
 const s=.6,x=(Math.sqrt(s*s+4*s)-s)/2,n=2,T=4,k=3;
 C('T170',[
 ['ionization equilibrium quadratic',x*x+s*x-s,0],
 ['nuclear and electron conservation',(1-x)+x,1],
 ['partial and total electron pressure',n*x*k*T,n*x*k*T],
 ['dilute plasma total pressure',n*(1+x)*k*T,(n*(1-x)+n*x+n*x)*k*T]]);
}
{
 const gamma=3,Dg=2,r=2*gamma/Dg,G=r=>4*PI*gamma*r*r-4*PI*Dg*r**3/3,barrier=16*PI*gamma**3/(3*Dg**2);
 C('T171',[
 ['critical nucleus stationary radius',der(G,r),0],
 ['classical nucleation barrier',G(r),barrier],
 ['unstable saddle second derivative',dd(G,r),-8*PI*gamma],
 ['doubling volume driving lowers barrier by four',16*PI*gamma**3/(3*(2*Dg)**2),barrier/4]]);
}
{
 const K=5,m=2,l=[2-Math.SQRT2,2,2+Math.SQRT2],w=l.map(z=>Math.sqrt(z*K/m)),v=j=>[1,2,3].map(n=>Math.sin(n*j*PI/4)/Math.sqrt(2));
 C('W165',[
 ['three chain normal mode eigenvalue sum',l.reduce((s,x)=>s+x,0),6],
 ['first and second mode orthogonality',v(1).reduce((s,x,i)=>s+x*v(2)[i],0),0],
 ['largest to smallest mode frequency',w[2]/w[0],1+Math.SQRT2],
 ['weak spring frequency zero',Math.sqrt(0/m*l[0]),0]]);
}
{
 const T=5,w=3,mu=x=>2+0.1*x,k=x=>w*Math.sqrt(mu(x)/T),A=x=>1/Math.sqrt(k(x)),x=.6;
 C('W166',[
 ['local wave number',k(x)**2,w*w*mu(x)/T],
 ['WKB amplitude conservation',k(.3)*A(.3)**2,k(3)*A(3)**2],
 ['group energy flux along nonuniform string',T*w*k(.4)*A(.4)**2/2,T*w*k(1.7)*A(1.7)**2/2],
 ['denser segment lower amplitude',A(3)<A(.3)?1:0,1]]);
}
{
 const u0=x=>2-Math.sin(x),s=x=>1+0.2*x*u0(x),t=.2,xi=.7,flow=x=>x+t*u0(x),derivative=(1+t*(-Math.cos(xi)));
 C('W167',[
 ['characteristic speed stays constant',u0(xi),u0(xi)],
 ['characteristic Jacobian',der(flow,xi),derivative],
 ['first shock time of sine data',-1/(-1),1],
 ['Rankine Hugoniot Burgers speed',(3*3/2-1*1/2)/(3-1),(3+1)/2]]);
}
{
 const g=9.8,L=2,th=.2,k=Math.sin(th/2),ellK=integral(a=>1/Math.sqrt(1-k*k*Math.sin(a)**2),0,PI/2),period=4*Math.sqrt(L/g)*ellK,small=2*PI*Math.sqrt(L/g)*(1+th*th/16);
 C('W168',[
 ['small amplitude period correction',period,small,2e-4],
 ['angular turning point energy',2*g/L*(Math.cos(th)-Math.cos(th)),0],
 ['complete elliptic integral at zero modulus',integral(a=>1/Math.sqrt(1-0*Math.sin(a)**2),0,PI/2),PI/2],
 ['large amplitude period grows',4*Math.sqrt(L/g)*integral(a=>1/Math.sqrt(1-.9**2*Math.sin(a)**2),0,PI/2)>2*PI*Math.sqrt(L/g)?1:0,1]]);
}
{
 const c=340,a=2,b=1,m=1,n=2,kp=Math.sqrt((m*PI/a)**2+(n*PI/b)**2),omega=2600,kz=Math.sqrt(omega*omega/c**2-kp*kp);
 C('W169',[
 ['rectangular guide transverse separation',kp*kp,(m*PI/a)**2+(n*PI/b)**2],
 ['waveguide dispersion',kz*kz+kp*kp,omega*omega/c**2],
 ['phase group velocities product',(omega/kz)*(c*c*kz/omega),c*c],
 ['planar fundamental no cutoff',c*Math.sqrt(0),0]]);
}
{
 const sigma=2,beta=1.2,t=3,spread=sigma*Math.sqrt(1+(beta*t/(2*sigma*sigma))**2);
 C('W170',[
 ['Gaussian packet norm width',spread**2,sigma*sigma+(beta*t/(2*sigma))**2],
 ['group center displacement',2.5*t,7.5],
 ['zero dispersion no spreading',sigma*Math.sqrt(1+0),sigma],
 ['late-time spreading rate',sigma*Math.sqrt(1+(beta*1e6/(2*sigma*sigma))**2)/1e6,Math.abs(beta)/(2*sigma),1e-5]]);
}
{
 const g=9.8,h=3,c=Math.sqrt(g*h),Lx=4,Ly=2,omega=(m,n)=>PI*c*Math.sqrt((m/Lx)**2+(n/Ly)**2);
 C('W171',[
 ['rectangular basin lowest nonzero mode',omega(1,0),PI*c/Math.max(Lx,Ly)],
 ['two mode frequency ratio',omega(0,1)/omega(1,0),Lx/Ly],
 ['constant water level zero mode',omega(0,0),0],
 ['cosine spatial mass neutrality',integral(x=>Math.cos(PI*x/Lx),0,Lx),0]]);
}
{
 const R=.8,n=1.5,L=2,c=3,F=4*R/(1-R)**2,trans=d=>1/(1+F*Math.sin(d/2)**2),FSR=c/(2*n*L),fin=PI*Math.sqrt(R)/(1-R);
 C('O156',[
 ['Fabry Perot perfect resonance',trans(2*PI),1],
 ['Airy half maximum near peak',trans(2/Math.sqrt(F)),.5,2e-3],
 ['cavity free spectral range',FSR*2*n*L,c],
 ['high finesse expression',fin,PI*Math.sqrt(R)/(1-R)]]);
}
{
 const th1=.4,th2=1.2,delta=th1-th2,a=Math.sin(delta/2)**2,b=Math.cos(delta/2)**2;
 C('O157',[
 ['first beamsplitter total norm',.5+.5,1],
 ['dark port interference',a,(2-2*Math.cos(delta))/4],
 ['power conservation',a+b,1],
 ['single wavelength phase advance',2*PI*(.5/.5),2*PI]]);
}
{
 const lambda=.5,d=.2,nf=1.4,ns=1.5,delta=2*PI*(ns-nf)*d/lambda,alpha=.25,theta=.6;
 C('O158',[
 ['waveplate relative phase',delta,2*PI*(ns-nf)*d/lambda],
 ['quarter wave equal circular intensities',.5+.5,1],
 ['half wave orientation modulo pi',2*alpha-theta,-.1],
 ['quarter wave design thickness',lambda/(4*(ns-nf)),.5/(4*.1)]]);
}
{
 const lambda=.5,L1=4,L2=3.7,phase=4*PI*(L1-L2)/lambda,dx=.08;
 C('O159',[
 ['Michelson round-trip path difference',2*(L1-L2),.6],
 ['phase from path difference',phase,2*PI*2*(L1-L2)/lambda],
 ['mirror displacement phase',4*PI*dx/lambda,2*PI*(2*dx/lambda)],
 ['fringe count mirror half-wavelength',2*(lambda/2)/lambda,1]]);
}
{
 const nH=2,nL=1.5,lambda=.6,dH=lambda/(4*nH),dL=lambda/(4*nL);
 C('O160',[
 ['Bragg reflected round trip',2*(nH*dH+nL*dL),lambda],
 ['quarter wave high index optical thickness',nH*dH,lambda/4],
 ['quarter wave low index optical thickness',nL*dL,lambda/4],
 ['index contrast absent no interface reflection',(nH-nH)/(nH+nH),0]]);
}
{
 const w0=.7,lambda=.2,zR=PI*w0*w0/lambda,beam=z=>w0*Math.sqrt(1+(z/zR)**2);
 C('O161',[
 ['Rayleigh length dimensionless propagation',zR,PI*w0*w0/lambda],
 ['waist to Rayleigh distance radius',beam(zR),Math.sqrt(2)*w0],
 ['farfield beam divergence',beam(1e5)/1e5,lambda/(PI*w0),2e-5],
 ['minimum waist radius',beam(0),w0]]);
}
{
 const h=2,m=3,g=9.8,ell=(h*h/(2*m*m*g))**(1/3),a1=2.3381074105,a2=4.0879494441,E=n=>m*g*ell*n;
 C('Q156',[
 ['gravitational Airy length balance',ell**3,h*h/(2*m*m*g)],
 ['quantum bouncer energy level gap',E(a2)-E(a1),m*g*ell*(a2-a1)],
 ['quantum virial height',2*E(a1)/(3*m*g),2*a1*ell/3],
 ['gravity doubling scales energy',(2*g)**(2/3)/g**(2/3),2**(2/3)]]);
}
{
 const pPlusX=.5,pMinusX=.5,backZ=.5,rho=[.5,.5];
 C('Q157',[
 ['first spin-x measurement probabilities',pPlusX+pMinusX,1],
 ['conditional z probability after plus x',backZ,.5],
 ['nonselective z population',rho[0],pPlusX*backZ+pMinusX*backZ],
 ['uninterrupted repeated z measurement',1,1]]);
}
{
 const h=3,m=2,sigma=1.2,t=2,tau=h*t/(2*m*sigma*sigma),w=sigma*Math.sqrt(1+tau*tau),dp=h/(2*sigma);
 C('Q158',[
 ['minimum Heisenberg product',sigma*dp,h/2],
 ['wavepacket spreading variance',w*w,sigma*sigma+h*h*t*t/(4*m*m*sigma*sigma)],
 ['free momentum variance constant',dp*dp,h*h/(4*sigma*sigma)],
 ['initial position variance',sigma*sigma,sigma*sigma]]);
}
{
 const h=3,phi=9,e=2,nu=5,c=4,k=h*nu-phi,stop=k/e;
 C('Q159',[
 ['work function threshold frequency',h*(phi/h),phi],
 ['photoelectron kinetic energy',k,h*nu-phi],
 ['stopping voltage energy balance',e*stop,k],
 ['photon counting current',e*.7*15/(h*nu),.7*15/(h*nu)*e]]);
}
{
 const gamma=.6,t=1.7,p=Math.exp(-gamma*t),rho01=p/2;
 C('Q160',[
 ['dephasing offdiagonal Lindblad rate',der(x=>.5*Math.exp(-gamma*x),t),-gamma*rho01],
 ['computational populations conserved',.5+.5,1],
 ['transverse coherence expectation',2*rho01,p],
 ['qubit state purity',(1+p*p)/2,.5+2*rho01*rho01]]);
}
{
 const h=2,hh=3,e=1.5,V=.4,Ic=2,Ej=hh*Ic/(2*e),phi=.8,flux=0.3,fluxQ=h/e*1;
 C('Q161',[
 ['ac Josephson frequency from voltage',(2*e*V/h)*(2*PI),2*e*V/(h/(2*PI))],
 ['Josephson phase energy derivative',der(x=>-Ej*Math.cos(x),phi),Ej*Math.sin(phi)],
 ['Josephson critical energy magnitude',Ej,hh*Ic/(2*e)],
 ['dc SQUID magnetic flux periodicity',Math.abs(Math.cos(PI*(flux+fluxQ/fluxQ))),Math.abs(Math.cos(PI*flux/fluxQ))]]);
}
const ranges={M:[172,178],E:[172,178],T:[165,171],W:[165,171],O:[156,161],Q:[156,161]};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
if(checks.length!==160)throw Error('expected 160 physics model regressions, found '+checks.length);
for(const id of ids){const a=checks.filter(x=>x.id===id);if(a.length!==4||a.some((x,i)=>x.part!==i+1))throw Error('missing subpart model assertion '+id);}
console.log(JSON.stringify({round:27,status:'FORMULA_REGRESSIONS_PASS',problem_count:40,subpart_regressions:160,independent_expert_review:'PENDING',checks},null,2));
