import matplotlib.pyplot as plt
import numpy as np
from qiskit import IBMQ, Aer, assemble, transpile
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.visualization import plot_histogram
from simon_reduced import simon_reduced

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

def multicmp(qc, a, b, cmpr, output, n):
    for i in range(n):
        XOR(qc, a[i], b[i], cmpr[i])
        qc.x(cmpr[i])

    qc.mct(cmpr, output)

    for i in range(n):
        qc.x(cmpr[i])
        XOR(qc, a[i], b[i], cmpr[i])

def simon_oracle(qc, k0, k1):
    simon_reduced(qc, l, r, k0, k1, state_size)
    for i in range(state_size):
        XOR(qc, l[i], c0[i], cmpr[i])
        qc.x(cmpr[i])
        XOR(qc, r[i], c1[i], cmpr[state_size+i])
        qc.x(cmpr[state_size+i])
    
    qc.mcx(cmpr, out)

    for i in range(state_size):
        qc.x(cmpr[i])
        XOR(qc, l[i], c0[i], cmpr[i])
        qc.x(cmpr[state_size+i])
        XOR(qc, r[i], c1[i], cmpr[state_size+i])

    for i in range(state_size):
        qc.cx(k1[i],l[i])
        qc.cx(r[(i-2)%state_size],l[i])
        qc.ccx(r[(i-1)%state_size],r[(i-8)%state_size],l[i])
    
    for i in range(state_size):
        qc.cx(k0[i],r[i])
        qc.cx(l[(i-2)%state_size],r[i])
        qc.ccx(l[(i-1)%state_size],l[(i-8)%state_size],r[i])

state_size = 3
l = QuantumRegister(state_size, name='l')
r = QuantumRegister(state_size, name='r')
k0 = QuantumRegister(state_size, name='k0')
k1 = QuantumRegister(state_size, name='k1')
c0 = QuantumRegister(state_size, name='c0')
c1 = QuantumRegister(state_size, name='c1')
cmpr = QuantumRegister(2*state_size, name='cmpr')
cct = ClassicalRegister(2*state_size, name='lc')
out = QuantumRegister(1, name='out')

kl = '0101'
kr = '0010'

c = '10101110'

qc = QuantumCircuit(l, r, k0, k1, c0, c1, cmpr, out, cct)
qc.initialize([1, -1]/np.sqrt(2), out)
for i in range(state_size):
    if int(c[i]):
        qc.x(c0[i])
    
    if int(c[state_size+i]):
        qc.x(c1[i])

simon_oracle(qc, k0, k1)
qc.append(diffuser(2*state_size), [*k0, *k1])
simon_oracle(qc, k0, k1)
qc.append(diffuser(2*state_size), [*k0, *k1])
simon_oracle(qc, k0, k1)
qc.append(diffuser(2*state_size), [*k0, *k1])

qc.measure(k0, cct[:state_size])
qc.measure(k1, cct[state_size:])
# for i in range(state_size):
#     if int(kl[i]):
#         qc.x(k0[i])
    
#     if int(kr[i]):
#         qc.x(k1[i])

# simon_reduced(qc, l, r, k0, k1, state_size)
# qc.measure(l, cct[:4])
# qc.measure(r, cct[4:])


# state_size = 16

# l = QuantumRegister(state_size, name='l')
# r = QuantumRegister(state_size, name='r')
# k0 = QuantumRegister(state_size, name='k0')
# k1 = QuantumRegister(state_size, name='k1')
# k2 = QuantumRegister(state_size, name='k2')
# k3 = QuantumRegister(state_size, name='k3')
# out = QuantumRegister(1, name='out')
# ct = QuantumRegister(2*state_size, name='ct')
# check = QuantumRegister(state_size, name='check')
# k0t = ClassicalRegister(state_size, name='k0t')
# k1t = ClassicalRegister(state_size, name='k1t')
# k2t = ClassicalRegister(state_size, name='k2t')
# k3t = ClassicalRegister(state_size, name='k3t')

# kctl = '0101101011101000'
# kctr = '0010100011101100'
# qc = QuantumCircuit(l, r, k0, k1, k2, k3, ct, out)
# qc.initialize([1, -1]/np.sqrt(2), out)
# qc.h([*k0, *k1, *k2, *k3])

# for i in range(16):
#     if kctl[i] == '1':
#         qc.x(ct[i])
    
#     if kctr[i] == '1':
#         qc.x(ct[16+i])

# simon_oracle(qc, k0, k1, k2, k3, ct)
# qc.append(diffuser(4*state_size), [*k0, *k1, *k2, *k3])

# simon_oracle(qc, k0, k1, k2, k3, ct)
# qc.append(diffuser(4*state_size), [*k0, *k1, *k2, *k3])

# simon_oracle(qc, k0, k1, k2, k3, ct)
# qc.append(diffuser(4*state_size), [*k0, *k1, *k2, *k3])

# simon_oracle(qc, k0, k1, k2, k3, ct)
# qc.append(diffuser(4*state_size), [*k0, *k1, *k2, *k3])

# simon_oracle(qc, k0, k1, k2, k3, ct)
# qc.append(diffuser(4*state_size), [*k0, *k1, *k2, *k3])

# qc.measure(k0, k1, k2)

aer_sim = Aer.get_backend('aer_simulator')
transpiled_simon_circuit = transpile(qc, aer_sim)
results = aer_sim.run(transpiled_simon_circuit).result()
counts = results.get_counts()
plot_histogram(counts)
plt.show()