from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def oracle(circuit, target):
    """
    Oracle function to mark the target state by flipping its phase.
    For a 2-qubit system, target is a string like '11'.
    """
    if target == '00':
        circuit.x(0)
        circuit.x(1)
        circuit.cz(0, 1)
        circuit.x(0)
        circuit.x(1)
    elif target == '01':
        circuit.x(1)
        circuit.cz(1, 0)
        circuit.x(1)
    elif target == '10':
        circuit.x(0)
        circuit.cz(0, 1)
        circuit.x(0)
    elif target == '11':
        circuit.cz(0, 1)

def diffusion(circuit):
    """
    Diffusion operator for amplitude amplification.
    Implements the inversion about the mean.
    """
    circuit.h(0)
    circuit.h(1)
    circuit.x(0)
    circuit.x(1)
    circuit.cz(0, 1)
    circuit.x(0)
    circuit.x(1)
    circuit.h(0)
    circuit.h(1)

# Target state to search for
target = '10'

# Simulate for 0 to 4 iterations to show probability increase and oscillation
for iterations in range(5):
    qc = QuantumCircuit(2, 2)

    # Initialize to uniform superposition
    qc.h(0)
    qc.h(1)

    # Apply Grover iterations
    for _ in range(iterations):
        oracle(qc, target)
        diffusion(qc)

    # Measure
    qc.measure_all()

    # Simulate
    backend = AerSimulator()
    job = backend.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)

    print(f"Iterations: {iterations}")
    print("Counts:", counts)

    # Plot histogram
    plot_histogram(counts)
    plt.title(f"Grover's Algorithm - {iterations} Iterations (Target: {target})")
    plt.savefig(f'grover_{iterations}_iterations.png')
    plt.show()

# Display the circuit for 1 iteration
qc_example = QuantumCircuit(2, 2)
qc_example.h(0)
qc_example.h(1)
oracle(qc_example, target)
diffusion(qc_example)
qc_example.measure_all()
print("\nCircuit diagram for 1 iteration:")
print(qc_example.draw())
