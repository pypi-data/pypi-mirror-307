import numpy as np
from .Qutrit import Qutrit

class QuantumGate:
    def __init__(self, matrix):
        self.matrix = matrix
        self.size = matrix.shape[0]  # Store the size of the gate

    def to_matrix(self):
        """Return the matrix representation of the gate."""
        return self.matrix

    @staticmethod
    def identity_qutrit():
        """3x3 identity gate for qutrit."""
        return QuantumGate(np.eye(3, dtype=complex))

    @staticmethod
    def cycle_gate():
        """Qutrit 'X' gate that cycles |0⟩ -> |1⟩, |1⟩ -> |2⟩, |2⟩ -> |0⟩."""
        return QuantumGate(np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex))

    @staticmethod
    def phase_gate(theta):
        """Phase gate for qutrit."""
        return QuantumGate(np.array([
            [1, 0, 0],
            [0, np.exp(1j * theta), 0],
            [0, 0, 1]
        ], dtype=complex))

class CNOTGate(QuantumGate):
    def __init__(self):
        # Define a 9x9 matrix for a CNOT gate on qutrits
        matrix = np.eye(9, dtype=complex)  # Identity for cases where control is in |0⟩ or |2⟩
        # Define the flip when control qutrit is in |1⟩ state
        matrix[4, 4] = 0
        matrix[4, 5] = 1
        matrix[5, 5] = 0
        matrix[5, 4] = 1
        super().__init__(matrix)

    def apply_to(self, control_qutrit: Qutrit, target_qutrit: Qutrit):
        """Applies the CNOT gate to the given control and target qutrits."""
        combined_state = np.kron(control_qutrit.state, target_qutrit.state)
        new_state = np.dot(self.matrix, combined_state)

        # Split the combined state back to individual qutrit states
        control_qutrit.state = new_state[:3]
        target_qutrit.state = new_state[3:6]

class ControlledGate(QuantumGate):
    def __init__(self, control_qutrit: Qutrit, target_qutrit: Qutrit, base_gate: QuantumGate):
        super().__init__(base_gate.to_matrix())  # Initialize with the base gate matrix
        self.control_qutrit = control_qutrit
        self.target_qutrit = target_qutrit
        self.base_gate = base_gate

    def apply_to(self):
        """Applies the base gate to the target qutrit if the control qutrit is in the |1⟩ state."""
        if np.abs(self.control_qutrit.state[1]) > 0.5:  # Threshold for "in state |1⟩"
            self.target_qutrit.apply_gate(self.base_gate)


