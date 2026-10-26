"""Targeted safeguards for physical assumptions and four revised derivations.

This is a limited equation check, not human six-round physics review.
"""
from pathlib import Path
import sympy as s
import unittest

ROOT=Path(__file__).resolve().parent.parent


class AssumptionAndDerivationTests(unittest.TestCase):
    def source(self,pid,part):
        return (ROOT/'bank'/pid/(part+'.tex')).read_text(encoding='utf-8')

    def test_thermal_connectors_are_not_unmodelled_reservoirs(self):
        for pid in ('T001','T006'):
            question=self.source(pid,'question')
            self.assertIn('热容',question)
            self.assertIn('可忽略',question)

    def test_ambiguous_dimensionless_optical_data_is_restricted(self):
        q=self.source('O003','question')
        self.assertIn('空气',q)
        self.assertIn('折射率',q)

    def test_coaxial_capacitor_asks_for_energy_per_length(self):
        q=self.source('E005','question')
        self.assertIn('单位长度',q)
        self.assertIn('$U/L$',q)

    def test_atwood_force_torque_independent_rederivation(self):
        m1,m2,g,R,I=s.symbols('m1 m2 g R I',positive=True)
        a=(m2-m1)*g/(m1+m2+I/R**2)
        t1=m1*(g+a)
        t2=m2*(g-a)
        self.assertEqual(s.simplify((t2-t1)*R-I*a/R),0)

    def test_coaxial_field_energy_matches_capacitance(self):
        lam,eps,a,b,r=s.symbols('lam eps a b r',positive=True)
        er=lam/(2*s.pi*eps*r)
        integral=s.integrate(s.Rational(1,2)*eps*er**2*2*s.pi*r,(r,a,b))
        result=lam**2*s.log(b/a)/(4*s.pi*eps)
        self.assertEqual(s.simplify(integral-result),0)

    def test_equal_heat_capacity_entropy_and_minimum(self):
        t1,t2,n,cv=s.symbols('t1 t2 n cv',positive=True)
        tf=(t1+t2)/2
        self.assertEqual(s.simplify(n*cv*(tf-t1)+n*cv*(tf-t2)),0)
        self.assertEqual(
            s.simplify(s.log(tf/t1)+s.log(tf/t2)-s.log((t1+t2)**2/(4*t1*t2))),0)
        self.assertEqual(s.expand((t1+t2)**2-4*t1*t2),s.expand((t1-t2)**2))

    def test_infinite_well_transition_frequency(self):
        m,L,hbar=s.symbols('m L hbar',positive=True)
        delta=(4-1)*s.pi**2*hbar**2/(2*m*L**2)
        freq=delta/(2*s.pi*hbar)
        self.assertEqual(s.simplify(freq-3*s.pi*hbar/(4*m*L**2)),0)


if __name__=='__main__':
    unittest.main()
