#!/usr/bin/env python3
"""Twenty deeper cross-method physics tests for ALREADY transcribed high-risk candidate solutions.
These prove only specified model identities, NOT original scans, figures, expert acceptance, or publication rights.
"""
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def close(a,b,rel=0.002,absolute=1e-15):
    if not math.isclose(a,b,rel_tol=rel,abs_tol=absolute):
        raise AssertionError(f"{a!r} != {b!r}")

def collision_1_3():
    u1,u2,delay,decel=90/3.6,65/3.6,.7,7.5
    separation=80-(u1+u2)*delay
    t=((u1+u2)-math.sqrt((u1+u2)**2-4*decel*separation))/(2*decel)
    close((u1+u2)*t-decel*t*t,separation,rel=1e-9)
    assert 0<t<min(u1,u2)/decel
    close(u1-decel*t,12.93197289)

def degenerate_bead_2_25():
    g,R,m=9.8,.75,1.2
    def potential(theta):
        return m*g*R*(1-math.cos(theta))-.5*m*(g/R)*R**2*math.sin(theta)**2
    theta=.06
    ratio=potential(theta)/(m*g*R*theta**4)
    close(ratio,1/8,rel=.005)
    assert potential(theta)>0 and potential(-theta)>0

def rocket_height_3_14():
    mass,flow,exhaust,g,tb=2.72e6,1.29e3,5.50e4,9.8,155.
    def v(t):
        return exhaust*math.log(mass/(mass-flow*t))-g*t
    remaining=mass-flow*tb
    analytic=exhaust*(tb-remaining/flow*math.log(mass/remaining))-.5*g*tb**2
    N=2048
    step=tb/N
    trapezoid=step*(.5*v(0)+sum(v(k*step) for k in range(1,N))+.5*v(tb))
    close(analytic,trapezoid,rel=1e-5)
    close(analytic,203590,rel=.02)
    assert mass-flow*tb>0

def bungee_energy_4_10():
    mass,g,unstretched,k=72.,9.8,20.,60.
    x=(mass*g+math.sqrt((mass*g)**2+2*k*mass*g*unstretched))/k
    close(.5*k*x*x,mass*g*(unstretched+x),rel=1e-12)
    close(x,36.4318,rel=.002)
    assert unstretched+x<60.

def lorentz_synchrony_8_5():
    c=2.99792458e8
    v=.60*c
    spacing=10
    times=[-v*(n*spacing)/c**2 for n in (-2,-1,0,1,2)]
    close(times[0],-times[-1])
    assert times[0]>times[1]>times[2]>times[3]>times[4]

def waterdrop_charge_14_13():
    k,e,NA,earth=8.9875517923e9,1.602176634e-19,6.02214076e23,6.37e6
    def voltage(drop_grams):
        return k*(10*(drop_grams/18)*NA*e)/earth
    close(voltage(.05),3.78e6,rel=.01)
    close(voltage(1.)/voltage(.05),20.,rel=1e-10)
    assert voltage(1.)>7e7

def membrane_polarity_15_6():
    epsilon=.52e-3/(8.8541878128e-12*6.)
    potential=epsilon*5.2e-9
    close(potential,.0509,rel=.01)
    assert -potential<0 and potential>0

def kirchhoff_three_branch_16_11():
    resistors=[2.,.5,5.]
    emf=[0.,3.,6.]
    V=-sum(e/r for e,r in zip(emf,resistors))/sum(1/r for r in resistors)
    I=[(V+e)/r for e,r in zip(emf,resistors)]
    close(sum(I),0.,absolute=1e-12)
    close(I[0],-4/3,rel=1e-10)
    close(I[1],2/3,rel=1e-10)
    close(I[2],2/3,rel=1e-10)

def proton_relativistic_energy_18_7():
    c,e,mp=2.99792458e8,1.602176634e-19,1.6726219e-27
    momentum=e*20*3.5
    rest=mp*c*c
    Etot=math.sqrt((momentum*c)**2+rest**2)
    kinetic=Etot-rest
    close(Etot/e/1e9,21.01,rel=.01)
    close(kinetic/e/1e9,20.07,rel=.01)
    assert kinetic>0 and kinetic<Etot

def coercivity_edges_19_11():
    H=2.
    onset=2*math.pi*.00025*H
    whole=2*math.pi*.00040*H
    close(onset,.00314,rel=.01)
    close(whole,.00503,rel=.01)
    assert onset<whole

def current_magnetic_energy_20_26():
    mu0=4*math.pi*1e-7
    current=100.
    D1,D2=.1,.2
    delta_L=mu0/math.pi*math.log(D2/D1)
    delta_field=.5*current**2*delta_L
    mechanical=mu0*current**2/(2*math.pi)*math.log(D2/D1)
    supply=current**2*delta_L
    close(mechanical,delta_field,rel=1e-12)
    close(supply,mechanical+delta_field,rel=1e-12)

def gascell_path_22_23():
    fringes,wavelength,cell=98,589.3e-9,.20
    single=1+fringes*wavelength/cell
    double=1+fringes*wavelength/(2*cell)
    close(single,1.000289,rel=5e-7)
    close((single-1)/(double-1),2.,rel=1e-8)

def array_order_23_17():
    wavelength=2.99792458e8/232e6
    N,d=192.,6.
    first_zero=math.asin(wavelength/(N*d))
    first_grating=math.asin(wavelength/d)
    close(first_zero,1.122e-3,rel=.02)
    close(math.degrees(first_grating),12.5,rel=.02)
    assert first_grating>100*first_zero

def crossed_polarizer_24_11():
    theta=math.radians(60)
    I1=.5
    I3=I1*.5*math.sin(2*theta)**2
    close(I3,3/16,rel=1e-12)
    assert I3<I1

def refractive_eye_radius_25_11():
    n1,n2,image_distance,object_distance=1.,1.4,2.6,25.
    radius=(n2-n1)/(n1/object_distance+n2/image_distance)
    close(n1/object_distance+n2/image_distance,(n2-n1)/radius)
    close(radius,.691,rel=.01)
    assert abs(radius-.361)>.2

def telescope_effective_focal_25_21():
    primary_focal=20.
    secondary_pos=14.
    s2=-(primary_focal-secondary_pos)
    s2prime=secondary_pos+4.
    f2=1/(1/s2+1/s2prime)
    amplification=-s2prime/s2
    feff=primary_focal*amplification
    close(f2,-9.,rel=1e-12)
    close(feff/.20,300.,rel=1e-12)
    assert feff != 14+14+4

def compton_upper_bound_26_16():
    initial=4000.
    rest=511000.
    final=initial/(1+2*initial/rest)
    recoil=initial-final
    close(recoil,61.7,rel=.01)
    assert 0<recoil<initial

def moving_compton_mass_shell_26_18():
    rest=511.
    E_in=50.
    electron_in=rest+20.
    p_in=-math.sqrt(20*(20+2*rest))
    system_E=E_in+electron_in
    system_p=E_in+p_in
    scattered=(system_E**2-system_p**2-rest**2)/(2*(system_E+system_p))
    electron_out=system_E-scattered
    electron_momentum=system_p+scattered
    close(electron_out**2-electron_momentum**2,rest**2,rel=1e-12)
    close(scattered,69.39,rel=.01)

def neutron_flux_conservation_30_17():
    neutron_flux=2e12
    exposed_area=4.0
    claimed_thin_capture=1.74e14
    max_rate=neutron_flux*exposed_area
    assert claimed_thin_capture/max_rate>20.
    assert claimed_thin_capture>max_rate

def neutron_absorption_30_18():
    number_density=8.64*6.02214076e23/112.4
    section=4000*1e-24
    depth=-math.log(.05)/(number_density*section)
    thin_depth=.95/(number_density*section)
    close(1-math.exp(-number_density*section*depth),.95,rel=1e-12)
    close(depth,.0162,rel=.01)
    close(1-math.exp(-number_density*section*thin_depth),.613,rel=.002)
    assert depth>3*thin_depth

CASES=[
 ("1.3","习题",collision_1_3),
 ("2.25","习题",degenerate_bead_2_25),
 ("3.14","习题",rocket_height_3_14),
 ("4.10","习题",bungee_energy_4_10),
 ("8.5","思考题",lorentz_synchrony_8_5),
 ("14.13","习题",waterdrop_charge_14_13),
 ("15.6","习题",membrane_polarity_15_6),
 ("16.11","习题",kirchhoff_three_branch_16_11),
 ("18.7","习题",proton_relativistic_energy_18_7),
 ("19.11","习题",coercivity_edges_19_11),
 ("20.26","习题",current_magnetic_energy_20_26),
 ("22.23","习题",gascell_path_22_23),
 ("23.17","习题",array_order_23_17),
 ("24.11","习题",crossed_polarizer_24_11),
 ("25.11","习题",refractive_eye_radius_25_11),
 ("25.21","习题",telescope_effective_focal_25_21),
 ("26.16","习题",compton_upper_bound_26_16),
 ("26.18","习题",moving_compton_mass_shell_26_18),
 ("30.17","习题",neutron_flux_conservation_30_17),
 ("30.18","习题",neutron_absorption_30_18),
]
def main():
    assert len(CASES)==20 and len(set(key for key,*_ in CASES))==20
    for key,kind,check in CASES:
        chapter=int(key.split(".")[0])
        prefix=(ROOT/f"supplement_selected_thought/{chapter:02d}" if kind=="思考题" else ROOT/f"chapters/{chapter:02d}")
        marker=rf"\paragraph{{{kind} {key}}}"
        for suffix in ("questions","solutions"):
            if marker not in (prefix/f"{suffix}.tex").read_text(encoding="utf-8"):
                raise AssertionError(f"Missing existing source candidate {kind} {key} {suffix}")
        check()
        print(f"PASS high-risk cross-method {kind} {key}")
    print("PASS 20 high-risk candidate cross-method scenarios; original figures/expert check remain pending.")
if __name__=="__main__": main()
