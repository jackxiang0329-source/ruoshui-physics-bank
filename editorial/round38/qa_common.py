"""Executable numeric verification helpers. Never imply human approval."""
import math

P=math.pi
S=math.sqrt
E=math.exp
L=math.log
C=math.cos
SI=math.sin
CH=math.cosh
SH=math.sinh
TH=math.tanh
A=abs
tests=[]

def integrate(f,a,b,n=12000):
    if n%2:n+=1
    h=(b-a)/n
    val=f(a)+f(b)
    for i in range(1,n):val+=(4 if i%2 else 2)*f(a+i*h)
    return val*h/3

def der(f,x,h=1e-5):
    return (f(x+h)-f(x-h))/(2*h)

def der2(f,x,h=1e-4):
    return (f(x+h)-2*f(x)+f(x-h))/(h*h)

def root(f,a,b,n=90):
    fa=f(a)
    if fa*f(b)>0:raise ValueError("bracket has no sign change")
    for i in range(n):
        m=(a+b)/2;fm=f(m)
        if fa*fm<=0:b=m
        else:a=m;fa=fm
    return (a+b)/2

def jb(n,x):
    term=(x/2)**n
    for j in range(1,n+1):term/=j
    total=term
    for j in range(1,45):
        term*=-(x*x/4)/(j*(j+n));total+=term
    return total

def check(uid,part,name,actual,expected,tol=1e-5,method="numeric"):
    aa=float(actual)
    bb=float(expected)
    err=abs(aa-bb)
    passing=math.isfinite(aa) and math.isfinite(bb) and err<=tol*max(1,abs(bb))
    tests.append({"id":uid,"part":part,"method":method,"name":name,
                  "actual":aa,"expected":bb,"abs_error":err,
                  "rel_tolerance":tol,"pass":passing})
    return passing

def gate_ids(ids):
    expected={(uid,p) for uid in ids for p in (1,2,3,4)}
    found=[(t["id"],t["part"]) for t in tests]
    errors=[t for t in tests if not t["pass"]]
    if len(found)!=200 or len(set(found))!=200 or set(found)!=expected:
        raise RuntimeError(f"Expected 200 individually addressed checks, found {len(found)} / {len(set(found))} unique")
    if errors:raise RuntimeError(f"{len(errors)} physics-model checks failed; details saved in report: {errors[:3]}")
    return len(found)
