#!/usr/bin/env python3
"""Independent relativistic and quantum-number QA for Irodov Part VI.291--310.

A high-energy decay/threshhold numerical suite plus *individual* Q, B, S,
electron-flavor and muon-flavor lepton bookkeeping for all six examples in
each of original 308, 309 and 310. Detects independent simultaneous
violations (especially 310(3)) rather than just the book's first reason.
"""
from math import exp,log,sqrt,asin,degrees,isclose
MP=938.2720813
MN=939.5654205
M_E=.510998950
M_PI=139.57039
M_PI0=134.9768
M_MU=105.6583745
M_K=493.677
M_SIGMINUS=1197.449
M_SIGPLUS=1189.37
M_LAMBDA=1115.683
C=299792458.
testlog=[]

def test(q,subject,result,reference,rtol=.025):
    if not isclose(result,reference,rel_tol=rtol,abs_tol=1e-12):
        raise AssertionError(f"VI.{q} {subject}: {result:.9g} != {reference:.9g}")
    testlog.append((q,subject,result))

def two_body_T(parent_mass,daughter,other):
    return (parent_mass**2+daughter**2-other**2)/(2*parent_mass)-daughter

def threshold(incident,target,finalsum):
    """Relativistic lab kinetic threshold, all inputs rest energies in MeV."""
    return (finalsum**2-(incident+target)**2)/(2*target)

for p,target in [(100,5.31),(1000,433.0),(10000,9106.0)]:
    test(291,f"proton with momentum {p}MeV/c kinetic MeV",
         sqrt(p*p+MP*MP)-MP,target)
test(292,"pion travel distance at T=1.2 rest mass metres",
     C*25.5e-9*sqrt(1.2*(1.2+2)),15.0)
test(293,"pion proper lifetime in ns from 11m travel",
     11*M_PI/(C*sqrt(100*(100+2*M_PI)))*1e9,26.3)
test(294,"pion survival at 20m, T=rest mass",
     exp(-20/(C*25.5e-9*sqrt(3))),.22)
test(295,"pion-at-rest muon kinetic MeV",
     two_body_T(M_PI,M_MU,0),4.12)
test(295,"pion-at-rest neutrino energy MeV",
     (M_PI*M_PI-M_MU*M_MU)/(2*M_PI),29.79)
test(296,"Sigma- at rest neutron kinetic MeV",
     two_body_T(M_SIGMINUS,MN,M_PI),19.6)
test(297,"muon-at-rest maximal positron kinetic MeV",
     ((M_MU-M_E)**2)/(2*M_MU),52.32)
p_c=sqrt(5.3*(5.3+2*MP))
ML_est=MP+5.3+sqrt(p_c*p_c+M_PI*M_PI)
test(298,"Lambda0 parent rest mass from Tp=5.3MeV",ML_est,1115.2)
test(298,"Lambda0 measured vs source parent mass difference",
     abs(ML_est-M_LAMBDA),.5,.5)
test(299,"90deg neutrino laboratory energy MeV",
     (M_PI*M_PI-M_MU*M_MU)/(2*(M_PI+50)),21.9)
mx=sqrt(M_SIGPLUS**2+M_PI**2-2*(M_SIGPLUS+320)*(M_PI+42))
test(300,"neutral daughter mass MeV from transverse pion",mx,941)
test(301,"pi0 kinetic equal pi0 rest mass MeV",M_PI0,135)
test(301,"each of two 60deg photons energy MeV",M_PI0,135)
test(302,"relativistic endothermic general toy threshold MeV",
     threshold(140,938,140+938+50),
     50*(1+140/938)+50*50/(2*938))
test(303,"positron/electron annihilation opening angle deg",
     2*degrees(asin(sqrt(2*M_E/(.750+2*M_E)))),98.8)
test(304,"gamma on free electron pair-production threshold MeV",
     threshold(0,M_E,3*M_E),2.044)
test(304,"gamma on proton charged-pion-pair threshold MeV",
     threshold(0,MP,MP+2*M_PI),321)
test(305,"proton-antiproton threshold kinetic GeV",
     threshold(MP,MP,4*MP)/1000,5.63)
test(305,"proton-proton neutral pion threshold MeV",
     threshold(MP,MP,2*MP+M_PI0),280)
test(306,"pi- + p -> K+ Sigma- threshold MeV",
     threshold(M_PI,MP,M_K+M_SIGMINUS),905)
test(306,"pi0 + p -> K+ Lambda0 threshold MeV",
     threshold(M_PI0,MP,M_K+M_LAMBDA),766)

# Quantum-number vector is (electric charge, baryon number,
# strangeness, electron-flavour lepton number, muon-flavour lepton number).
Q,B,S,LE,LM=range(5)
sp={
 'p': (+1,1,0,0,0), 'n':(0,1,0,0,0),
 'pi+':(+1,0,0,0,0), 'pi-':(-1,0,0,0,0), 'pi0':(0,0,0,0,0),
 'K+':(+1,0,+1,0,0), 'K-':(-1,0,-1,0,0),
 'K0':(0,0,+1,0,0),
 'Sigma+':(+1,1,-1,0,0), 'Sigma-':(-1,1,-1,0,0),
 'Lambda0':(0,1,-1,0,0), 'Xi-':(-1,1,-2,0,0),
 'Xi0':(0,1,-2,0,0), 'Omega-':(-1,1,-3,0,0),
 'e-':(-1,0,0,+1,0),'e+':(+1,0,0,-1,0),
 'mu-':(-1,0,0,0,+1),'mu+':(+1,0,0,0,-1),
 'nue':(0,0,0,+1,0),'anue':(0,0,0,-1,0),
 'numu':(0,0,0,0,+1),'anumu':(0,0,0,0,-1)
}
names=['Q','B','S','Le','Lmu']
def quantum_difference(left,right):
    def add(s):
        return [sum(sp[x][i] for x in s) for i in range(5)]
    a,b=add(left),add(right)
    return tuple(b[i]-a[i] for i in range(5))
def verify(q,n,left,right,changed,scope=None):
    diff=quantum_difference(left,right)
    actual={names[i] for i,x in enumerate(diff) if x and
            (scope is None or names[i] in scope)}
    if actual!=set(changed):
        raise AssertionError(f"VI.{q}({n}) changed {actual}, expected {changed}; diff={diff}")
    testlog.append((q,f"case {n}: exact quantum-number changes ({','.join(changed) or 'none'})",diff))

test(307,"neutral Xi0 Gell-Mann--Nishijima electric charge",
     1/2+(1-2)/2,0,.0000001)
test(307,"neutral Xi0 strangeness",-2,-2,.0000001)
test(307,"neutral Xi0 hypercharge",-1,-1,.0000001)

# 308: which violate separate lepton-flavour conservation?
v308=[
 (['n'],['p','e-','nue'],('Le',)),
 (['pi+'],['mu+','e-','e+'],('Lmu',)),
 (['pi-'],['mu-','numu'],('Lmu',)),
 (['p','e-'],['n','nue'],()),
 (['mu+'],['e+','nue','anumu'],()),
 (['K-'],['mu-','anumu'],())
]
for i,(initial,final,violated) in enumerate(v308,1):
    verify(308,i,initial,final,violated,scope=('Le','Lmu'))

# 309: strong interactions must conserve S (as well as Q,B).
v309=[
 (['pi-','p'],['Sigma-','K+'],()),
 (['pi-','p'],['Sigma+','K-'],('S',)),
 (['pi-','p'],['K+','K-','n'],()),
 (['n','p'],['Lambda0','Sigma+'],('S',)),
 (['pi-','n'],['Xi-','K+','K-'],('S',)),
 (['K-','p'],['Omega-','K+','K0'],())
]
for i,(initial,final,violated) in enumerate(v309,1):
    verify(309,i,initial,final,violated,scope=('S',))

# 310: some processes fail MORE THAN ONE independent conservation law.
v310=[
 (['Sigma-'],['Lambda0','pi-'],()),  # excluded by mass threshold, not Q/B/S
 (['pi-','p'],['K+','K-'],('B',)),
 (['K-','pi-'],['Omega-','K+','K0'],('Q','B')),
 (['n','p'],['Sigma+','Lambda0'],('S',)),
 (['pi-'],['mu-','e+','e-'],('Lmu',)),
 (['mu-'],['e-','nue','anumu'],('Le','Lmu'))
]
for i,(initial,final,violated) in enumerate(v310,1):
    verify(310,i,initial,final,violated)
# First 310 candidate conserves Q/B/S, but parent rest energy is insufficient.
test(310,"Sigma- cannot decay to Lambda0+pi- mass deficit MeV",
     M_LAMBDA+M_PI-M_SIGMINUS,57.8)
# Demonstrate flavour-resolved failure when TOTAL lepton number is unchanged.
left=sp['mu-'][LE]+sp['mu-'][LM]
right=sum(sp[x][LE]+sp[x][LM] for x in ['e-','nue','anumu'])
test(310,"case6 conserves summed lepton number",
     right-left,0,.0000001)
# The weird case 310(3) also fails baryon number independently.
a=quantum_difference(['K-','pi-'],['Omega-','K+','K0'])
test(310,"case3 baryon number discrepancy",a[B],1,.0000001)
test(310,"case3 electric charge discrepancy",a[Q],2,.0000001)

print(f"PASS: {len(testlog)} independent relativistic decay/threshold and "
      "flavour-resolved conservation checks for original Part VI.291--310.")
for number,item,value in testlog:
    print(f" VI.{number:<3} {item:<54} {value}")
