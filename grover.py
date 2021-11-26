import matplotlib.pyplot as plt
import numpy as np
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.visualization import plot_histogram

def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    for qubit in range(nqubits):
        qc.h(qubit)
    for qubit in range(nqubits):
        qc.x(qubit)
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)
    qc.h(nqubits-1)
    for qubit in range(nqubits):
        qc.x(qubit)
    for qubit in range(nqubits):
        qc.h(qubit)
    U_s = qc.to_gate()
    U_s.name = "Us"
    return U_s

def oracle(n, target):
    qc = QuantumCircuit(n)
    U = [[0]*2**n for _ in range(2**n)]
    for i in range(2**n):
        U[i][i] = 1
    U[target][target] = -1
    qc.unitary(U, list(range(n)))
    U_w = qc.to_gate()
    U_w.name = "Uw"
    return U_w

n = 5
qc = QuantumCircuit(n)

for i in range(n):
    qc.h(i)

qc.append(oracle(n, 7), list(range(n)))
qc.append(diffuser(n), list(range(n)))
qc.measure_all()

aer_sim = Aer.get_backend('aer_simulator')
transpiled_grover_circuit = transpile(qc, aer_sim)
results = aer_sim.run(transpiled_grover_circuit).result()
counts = results.get_counts()
print (counts)
x = []
for k in counts:
    x += [int(k, 2)]*counts[k]
print (plot_histogram(counts))
plt.show()