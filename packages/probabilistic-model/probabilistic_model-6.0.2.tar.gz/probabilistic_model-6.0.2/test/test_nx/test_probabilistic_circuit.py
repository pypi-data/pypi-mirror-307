import json
import os.path
import unittest

from matplotlib import pyplot as plt
from random_events.interval import closed, SimpleInterval
from random_events.variable import Continuous

from probabilistic_model.distributions.uniform import UniformDistribution
from probabilistic_model.probabilistic_circuit.nx.distributions import UnivariateContinuousLeaf
from probabilistic_model.probabilistic_circuit.nx.probabilistic_circuit import *
import plotly.graph_objects as go


class SymbolEnum(SetElement):
    EMPTY_SET = -1
    A = 0
    B = 1
    C = 2

class SmallCircuitTestCast(unittest.TestCase):
    """
    Integration test for all classes in probabilistic circuits.
    """

    x = Continuous("x")
    y = Continuous("y")

    model: ProbabilisticCircuit

    def setUp(self):
        sum1, sum2, sum3 = SumUnit(), SumUnit(), SumUnit()
        sum4, sum5 = SumUnit(), SumUnit()
        prod1, prod2 = ProductUnit(), ProductUnit()

        sum1.add_subcircuit(prod1, 0.5)
        sum1.add_subcircuit(prod2, 0.5)
        prod1.add_subcircuit(sum2)
        prod1.add_subcircuit(sum4)
        prod2.add_subcircuit(sum3)
        prod2.add_subcircuit(sum5)

        d_x1 = UnivariateContinuousLeaf(UniformDistribution(self.x, SimpleInterval(0, 1)))
        d_x2 = UnivariateContinuousLeaf(UniformDistribution(self.x, SimpleInterval(2, 3)))
        d_y1 = UnivariateContinuousLeaf(UniformDistribution(self.y, SimpleInterval(0, 1)))
        d_y2 = UnivariateContinuousLeaf(UniformDistribution(self.y, SimpleInterval(3, 4)))

        sum2.add_subcircuit(d_x1, 0.8)
        sum2.add_subcircuit(d_x2, 0.2)
        sum3.add_subcircuit(d_x1, 0.7)
        sum3.add_subcircuit(d_x2, 0.3)

        sum4.add_subcircuit(d_y1, 0.5)
        sum4.add_subcircuit(d_y2, 0.5)
        sum5.add_subcircuit(d_y1, 0.1)
        sum5.add_subcircuit(d_y2, 0.9)

        self.model = sum1.probabilistic_circuit

    def test_sampling(self):
        samples = self.model.sample(100)
        unique = np.unique(samples, axis=0)
        self.assertGreater(len(unique), 95)

    def test_conditioning(self):
        event = SimpleEvent({self.x: closed(0, 0.25) | closed(0.5, 0.75)}).as_composite_set()
        conditional, prob = self.model.conditional(event)
        self.assertAlmostEqual(prob, 0.375)
        conditional.plot_structure()
        # plt.show()

    def test_plot(self):
        self.model.plot_structure()
        # plt.show()
        fig = go.Figure(self.model.plot(600, surface=True))
        # fig.show()

from probabilistic_model.learning.jpt.variables import *

class PyCRAMErrorTestCase(unittest.TestCase):

    path = os.path.join(os.path.expanduser("~"), "Documents", "model.json")
    with open(path, "r") as file:
        model: ProbabilisticCircuit = ProbabilisticCircuit.from_json(json.load(file))

    def test_error(self):
        arm, grasp, rx, ry = self.model.variables
        self.model.marginal([rx, ry])
        print(self.model.variables)


if __name__ == '__main__':
    unittest.main()
