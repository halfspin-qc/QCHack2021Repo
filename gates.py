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



# This is the basic circuit to start with
n = 2
base_circ = QuantumCircuit(n,n)
for j in range(n):
    base_circ.h(j)
    base_circ.measure(j,j)

base_circ.draw()


### Add the Gate letter to the circuit
def H_Gate():
    circ_new.h(0)

def X_Gate():
    circ_new.x(0)

def Y_Gate():
    circ_new.y(0)

def Z_Gate():
    circ_new.z(0)

def default():
    return "Invalid Gate!"

switch_case = {
  1: H_Gate,
  2: X_Gate,
  3: Y_Gate,
  4: Z_Gate
}

def switch(x):
    return switch_case.get(x, default)()

circ_new = QuantumCircuit(2,2)
switch(1)   ## hardocding here, but the argument needs to be filled from the button the user chooses to add
circ_new.draw()

####
measure_all = QuantumCircuit(2,2)
measure_all.measure([0,1],[0,1])
measure_all.draw()
final_qc = base_circ+circ_new+measure_all
#final_qc.draw()



shots = 1000
counts = execute(final_qc,Aer.get_backend('qasm_simulator'),shots=shots).result().get_counts()

#### 
probs00 = counts.get('00') /shots
probs01 = counts.get('01') /shots
probs10 = counts.get('10') /shots
probs11 = counts.get('11') /shots

plot_histogram(counts)
