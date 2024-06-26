""""
To generate Random sequences using the Simulators instead the actual Quantum Device to 
avoid the errors and noice may occur during the process.

This code specifically written to execute on IBM Quantum Lab Platform.

Check this link: https://github.com/Qiskit/qiskit-ibm-provider

"""""


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute, IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit_ibm_provider import IBMProvider

provider = IBMProvider("966bbf0869e7e72d9d794695d32a38f8e9f0d76553533d1c650d58cfcf1ae079eb9077a59d1accaa76e038db084ccee20555d81b384f0f6568")
# print(provider.backends())                              # Check the available backends
backend = provider.get_backend('ibmq_qasm_simulator')             # select the backend device or simulator

q = QuantumRegister(16, 'q')                            # set Quantum Register with up-to 63 qubits
c = ClassicalRegister(16, 'c')                          # set Classical Register with up-to 63 qubits

circuit = QuantumCircuit(q, c)                          # Create Quantum Circuit using the Quantum and Classical Registers

circuit.h(q)                                            # Apply hadamard gate on all qubits

circuit.measure(q, c)                                   # Measures each qubit and save the result in Classical bits

binary_sequence_1 = ""                                  # empty string to save the binary sequence
binary_sequence_2 = ""

# for i in range(5):
job = execute(circuit, backend, shots=30)          # execute the Q-circuit on the simulator or Q-device which returns an object

print(f'Executing Job...\n {job_monitor(job)}\n')  # Check the Status in real time

result = job.result()                              # returns a dictionary from an object

counts = result.get_counts()                       # number of times - unique binary sequences
for i in range(5):
    binary_sequence_1 += list(counts.keys())[0]        # select the unique binary sequence by its index here it's [0]
    binary_sequence_2 += list(counts.keys())[1]        # select the unique binary sequence by its index here it's [0]

binary_sequence_1 = binary_sequence_1[:256]            # Consider only required sequence length
binary_sequence_2 = binary_sequence_2[:256]

# print the binary sequence
print('seq_1 ', binary_sequence_1, '\nseq_2 ', binary_sequence_2, '\n')
print("Similarity between sequences:", binary_sequence_1 == binary_sequence_2, '\n')
print('1', len(binary_sequence_1), '\n2', len(binary_sequence_2))
