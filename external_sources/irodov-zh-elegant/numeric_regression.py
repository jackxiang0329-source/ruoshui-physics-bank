#!/usr/bin/env python3
"""Independently recompute selected high-risk Irodov Part-VI answers.

Regression anchors are derived from the original user-provided scan and
standard formulae; they are independent of the prose TeX files. Running this
suite is NOT an independent peer review of the entire 1878-problem book.
"""
import math

N_A = 6.02214076e23
U = 1.66053906660e-27
C = 299792458.0
E = 1.602176634e-19
H_BAR = 1.054571817e-34
LN2 = math.log(2.0)
MEV = 1e6 * E
results = []


def check(problem, label, actual, expected, tolerance=0.025):
    if not math.isfinite(actual):
        raise AssertionError(f"{problem} {label}: non-finite result")
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=0.0):
        raise AssertionError(f"{problem} {label}: computed {actual:.8g}, expected {expected:.8g}")
    results.append((problem, label, actual))


# 6.167 first rotor angular speed, equal-atom rigid rotor
ms = 32.06 * U
d = 189e-12
check("6.167", "rotor rad/s", math.sqrt(2) * H_BAR / (ms*d*d/2), 1.57e11)
# 6.190 zero point vibrational energy per gram
check("6.190", "J/g", 9*8.314462618*330/(8*63.546), 48.6)
# 6.197 degenerate electron gas mean energy/EF
check("6.197", "mean EF ratio", 3/5, 0.6, .00001)
# 6.207 intrinsic band gap from conductance ratio
check("6.207", "Eg eV", (2*1.380649e-23*300*400/(400-300)*math.log(5))/E, 0.333)
# 6.220 verify published mean lifetime is 1.02 DAYS, not one year
co_lambda = -math.log(.96)/3600
check("6.220", "decay constant 1/s", co_lambda, 1.134e-5)
check("6.220", "mean lifetime day", (1/co_lambda)/86400, 1.02)
# 6.222 radiocarbon dating
check("6.222", "wood age years", 5570/LN2*math.log(5/3), 4106)
# 6.225 Na24 blood tracing: 16 per minute, not per second
check("6.225", "tracer volume cm3", (2000/(16/60))*2**(-5/15), 5953)
# 6.261 U235 energy and coal equivalence (book answer coal typo)
fission_1kg = (1000/235*N_A)*(200*MEV)
check("6.261", "joules per kg", fission_1kg, 8.21e13)
check("6.261", "coal kg", fission_1kg/30e6, 2.74e6)
# 6.262 deuterium fusion into one gram of helium
fusion_1gram = (N_A/4) * (23.85*MEV)
check("6.262", "fusion J", fusion_1gram, 5.75e11)
check("6.262", "coal kg", fusion_1gram/30e6, 1.92e4)
# 6.276 4.4 MeV alpha on Li7 produces 10B at center-of-mass speed
T_alpha = 4.4*MEV
recoil_speed = math.sqrt(2*4*U*T_alpha)/(11*U)
check("6.276", "recoil m/s", recoil_speed, 5.3e6)
# 6.278 photon threshold above deuteron binding
check("6.278", "excess percent", (2.2/(2*2*931.494))*100, 0.059)
# 6.281 cadmium thermal neutron absorption cross-section
sigma_cd = math.log(360)/(8.65/112.4*N_A*0.05)/1e-24
check("6.281", "cross section barns", sigma_cd, 2540)
# 6.282 heavy water exponential attenuation
attenuation = math.exp((1.11/20.0*N_A)*(2*7.0+4.2)*1e-24*5)
check("6.282", "attenuation factor", attenuation, 20.9)
# 6.283 competing Fe absorption/scattering
thickness = (7.87/55.85*N_A)*13.5e-24*0.5
fraction_scattered = (11/13.5)*(1-math.exp(-thickness))
check("6.283", "scattering loss", fraction_scattered, 0.35)
# 6.284 proton induced Be7 production
lam_be = LN2/(53*86400)
reaction_yield = 1.35e8*E/(10e-6*(2*3600)*lam_be)
check("6.284", "reaction yield", reaction_yield, 2.0e-3)
# 6.285 1% Au197 depletion and short-time Au198 saturation
J = 1.0e10
cross = 98e-24
t_au = -math.log(0.99)/(J*cross)/(365.25*86400)
check("6.285", "gold depletion years", t_au, 325)
N0 = 0.01/197*N_A
N_saturated = J*cross*N0/(LN2/(2.7*86400))
check("6.285", "Au198 saturation nuclei", N_saturated, 1.0e13)
# 6.287 reconstruct flux from delayed decay activity
lam = LN2/(2.7*86400)
J_au = 1.9e7*math.exp(lam*12*3600)/(96e-24*(0.2/197*N_A)*(1-math.exp(-lam*6*3600)))
check("6.287", "gold foil neutron flux", J_au, 6.0e9)
# 6.288 initial particles are generation ONE
check("6.288", "generation 100", 1000*1.05**99, 1.25e5)
# 6.290 physical original page has 1.0 MIN, 1.10 seconds, k=1.010
check("6.290", "reactor gain after one minute", 1.010**(60/1.10), 1.72)
check("6.290", "reactor period s", 1.10/math.log(1.010), 110.5)
# 6.291 proton kinetic energy with relativistic rest energy 938.272 MeV
mp = 938.2720813
check("6.291", "T at 0.10 GeV/c in MeV", math.sqrt(100**2+mp**2)-mp, 5.31)
# 6.292 pion mean flight distance
check("6.292", "pion flight metres", C*25.5e-9*math.sqrt(1.2*(1.2+2)), 15.0)
# 6.293 pion proper lifetime
mpi = 139.57
check("6.293", "pion lifetime ns", 11*mpi/(C*math.sqrt(100*(100+2*mpi)))*1e9, 26.3)
# 6.294 pion survival probability
check("6.294", "survival fraction", math.exp(-20/(math.sqrt(3)*C*25.5e-9)), 0.22)
# 6.295 rest pion two-body decay energy sharing
mmu = 105.658
check("6.295", "muon kinetic MeV", (mpi-mmu)**2/(2*mpi), 4.12)
check("6.295", "neutrino MeV", (mpi**2-mmu**2)/(2*mpi), 29.79)
# 6.298 parent lambda hyperon from observed proton kinetic energy
pc = math.sqrt(5.3*(5.3+2*mp))
check("6.298", "parent rest MeV", mp+5.3+math.sqrt(pc**2+mpi**2), 1115.2)
# 6.303 gamma pair from annihilation on fixed electron
check("6.303", "gamma divergence degrees",
      2*math.degrees(math.asin(math.sqrt(2*511/(750+2*511)))), 98.8)
# 6.304 threshold for gamma+e pair production, and gamma+p pion pair
check("6.304", "pair threshold MeV", 4*0.510999, 2.044)
check("6.304", "pion pair threshold MeV", 2*mpi*(1+mpi/mp), 321)
# 6.305 anti-proton production threshold MUST be GeV, not MeV
check("6.305", "antiproton threshold GeV", 6*mp/1000, 5.63)
# 6.306 pion proton production of K+ Sigma- and K+ Lambda0
mK = 493.677
check("6.306", "K Sigma threshold MeV",
      ((mK+1197.449)**2-(mpi+mp)**2)/(2*mp), 905)
check("6.306", "K Lambda threshold MeV",
      ((mK+1115.683)**2-(134.977+mp)**2)/(2*mp), 766)

print(f"PASS: {len(results)} independent numerical regression checks"
      " across 25+ critical Irodov VI original questions.")
for ident, name, value in results:
    print(f"  {ident:>5}  {name:<42} {value:.7g}")
