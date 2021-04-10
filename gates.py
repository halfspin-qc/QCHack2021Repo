import numpy as np
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from ibm_quantum_widgets import *
# Loading your IBM Q account(s)
provider = IBMQ.load_account()
%matplotlib inline

    # initialization
import matplotlib.pyplot as plt
import numpy as np
import pygame as pg
# importing Qiskit
from qiskit import IBMQ, BasicAer
# from qiskit.providers.ibmq import least_busy
from qiskit.providers.ibmq import *
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.visualization import plot_histogram


n = 2
qc_output = QuantumCircuit(n,n)
for j in range(n):
    qc_output.h(j)
    qc_output.measure(j,j)

qc_output.draw()


###

n = 2
qc_output = QuantumCircuit(n,n)
for j in range(n):
    qc_output.h(j)
    qc_output.measure(j,j)

qc_output.draw()

####
shots = 1000
counts = execute(qc_output,Aer.get_backend('qasm_simulator'),shots=shots).result().get_counts()

#### 
counts = result.get_counts()
probs00 = counts.get('00') /counts
probs01 = counts.get('01') /counts
probs10 = counts.get('10') /counts
probs11 = counts.get('11') /counts
