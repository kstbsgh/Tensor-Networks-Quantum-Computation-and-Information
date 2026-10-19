from qiskit import QuantumCircuit, transpile
from scipy.optimize import minimize
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.circuit import ParameterVector
from qiskit.primitives import StatevectorEstimator
from qiskit_aer.primitives import EstimatorV2 as AerEstimatorV2

import numpy as np

def expectation(params, ansatz, operator, shots = None):
    '''
    Ansatz is a parameterised QuanutmCircuit instance.
    Operator is a SprasePauliOp instance.

    if shots is provided, then a shot based estimator will be used(AerEstimatorV2) otherwise the StatevectorEstimator will be used.
    '''
    assert len(params) == len(ansatz.parameters), f"{len(params)} params are provided for a circuit with {anstaz.parameters} parameters"
    assert isinstance(ansatz, QuantumCircuit), 'ansatz needs to be a QuantumCircuit instance.'
    assert isinstance(operator, SparsePauliOp), 'operator needs to be a SparsePauliOp instance.'
    # remove the last three lines if you want the code to be more performant.

    if shots is not None:
        estimator = AerEstimatorV2()
        estimator.options.default_shots = shots

    else:
        estimator = StatevectorEstimator()

    pub = (ansatz, operator, list([params]))
    job = estimator.run([pub])
    result = job.result()

    expect_value = float(result[0].data.evs[0])
    return result, expect_value
    #should i return the exepct_value or the result?

def minimisation(cost, init_params, *cost_args, max_iter =1000, method = "COBYLA", tol = 1e-4):
    result = minimize(cost, init_params, args = cost_args, method = method, tol = tol, options = {'maxiter' : max_iter})
    return result

op = SparsePauliOp.from_list([['YZ',1]])

theta = ParameterVector('theta', 1)
qc = QuantumCircuit(2)
qc.ry(theta[0],0)
qc.cx(0,1)

