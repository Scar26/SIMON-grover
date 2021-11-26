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
    
def XOR(qc, a, b, output):
    qc.cx(a, output)
    qc.cx(b, output)


def oracle():
    ins = QuantumRegister(4, name='input')
    outs = QuantumRegister(4, name='outs')
    out = QuantumRegister(1, name='out')
    qc = QuantumCircuit(ins, outs, out)
    clauses = [[0, 1], [0, 2], [1, 3], [2, 3]]

    for i in range(4):
        u, v = clauses[i]
        XOR(qc, ins[u], ins[v], outs[i])

    qc.mct(outs, out)

    for i in range(4):
        u, v = clauses[i]
        XOR(qc, ins[u], ins[v], outs[i])
    
    U_w = qc.to_gate()
    U_w.name = "Uw"
    return U_w

ins = QuantumRegister(4, name='input')
outs = QuantumRegister(4, name='outs')
out = QuantumRegister(1, name='out')
cbits = ClassicalRegister(4, name='cbits')
qc = QuantumCircuit(ins, outs, out, cbits)
qc.initialize([1, -1]/np.sqrt(2), out)


for i in range(4):
    qc.h(ins[i])

qc.append(oracle(), list(range(9)))
qc.append(diffuser(4), ins)
qc.append(oracle(), list(range(9)))
qc.append(diffuser(4), ins)
qc.measure(ins, cbits)

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