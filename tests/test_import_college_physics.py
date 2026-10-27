import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import import_college_physics as cp
class CollegeTests(unittest.TestCase):
 def test_balanced_exercise(self):
  sample='''---
title: "Newton and Gravity"
---
<div data-type="exercise" data-element-type="problems-exercises">
<div data-type="problem" markdown="1">
A block with a mass of five kilograms is pushed by a constant force of twenty newtons. Compute its acceleration.
</div><div data-type="solution" markdown="1">4 m/s²</div>
</div>
'''
  rows=cp.parse(sample)
  self.assertEqual(len(rows),1)
  self.assertEqual(rows[0]["section"],"Newton and Gravity")
  self.assertNotIn("4 m/s²",rows[0]["content"])
 def test_figure_exclusion(self):
  sample='''---
title: "Motion"
---
<div data-type="exercise" data-element-type="conceptual-questions">
<div data-type="problem" markdown="1">Refer to [[link]](#graph), and calculate the instantaneous acceleration from the indicated graph.</div></div>
'''
  self.assertEqual(cp.parse(sample),[])
 def test_topics(self):
  self.assertEqual(cp.group("Magnetic Field"),"电磁学")
  self.assertEqual(cp.group("Thermodynamics"),"热学")
  self.assertEqual(cp.group("Displacement"),"力学")
  self.assertEqual(cp.group("Addition of Velocities"),"力学")
  self.assertEqual(cp.group("Problem-Solving Strategies"),"物理基础")
  self.assertEqual(cp.group("Falling Objects"),"力学")
  self.assertEqual(cp.group("Impulse"),"力学")
  self.assertEqual(cp.group("Physics: An Introduction"),"物理基础")
  self.assertEqual(cp.group("Vector Addition and Subtraction: Analytical Methods"),"力学")
  self.assertEqual(cp.group("Satellites and Kepler’s Laws"),"力学")
  self.assertEqual(cp.group("Archimedes’ Principle"),"力学")
  self.assertEqual(cp.group("Bernoulli’s Equation"),"力学")
  self.assertEqual(cp.group("Viscosity and Laminar Flow"),"力学")
  self.assertEqual(cp.group("The Simple Pendulum"),"振动与波动")
  self.assertEqual(cp.group("Hearing"),"振动与波动")
  self.assertEqual(cp.group("Conductors and Insulators"),"电磁学")
  self.assertEqual(cp.group("Aberrations"),"光学")
