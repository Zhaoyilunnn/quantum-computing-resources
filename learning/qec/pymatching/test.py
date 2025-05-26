import pymatching
import numpy as np

# 1. Define a parity check matrix (H)
# For a simple 3-qubit repetition code (detects single bit-flip errors)
# Q0 --C1-- Q1 --C2-- Q2
# Check C1: Z0*Z1
# Check C2: Z1*Z2
# H = [[1, 1, 0],  # Z0*Z1
#      [0, 1, 1]]  # Z1*Z2
# Columns correspond to qubits (potential error locations)
# Rows correspond to parity checks
H = np.array([[1, 1, 0], [0, 1, 1]])

# 2. Create a Matching object
m = pymatching.Matching(H)

# 3. Simulate an error and generate a syndrome
# Suppose an error occurs on the first qubit (qubit 0)
error_actual = np.array([1, 0, 0])

# The syndrome is H.error_actual^T (mod 2)
syndrome = H @ error_actual % 2

print(f"Parity Check Matrix (H):\n{H}")
print(f"Actual error: {error_actual}")
print(f"Generated syndrome: {syndrome}")

# 4. Decode the syndrome
# This gives the most likely error pattern causing the syndrome
predicted_error = m.decode(syndrome)

print(f"Predicted error: {predicted_error}")

# 5. Verify the result
# The predicted error should ideally match the actual error
# or be a logically equivalent error (differing by a stabilizer)
is_correct = np.array_equal(predicted_error, error_actual)
print(f"Decoding correct? {is_correct}")

# Example with a different error (on the middle qubit)
error_actual_2 = np.array([0, 1, 0])
syndrome_2 = H @ error_actual_2 % 2
print(f"\nActual error 2: {error_actual_2}")
print(f"Generated syndrome 2: {syndrome_2}")
predicted_error_2 = m.decode(syndrome_2)
print(f"Predicted error 2: {predicted_error_2}")
is_correct_2 = np.array_equal(predicted_error_2, error_actual_2)
print(f"Decoding correct for error 2? {is_correct_2}")

# Example with error on the last qubit
error_actual_3 = np.array([0, 0, 1])
syndrome_3 = H @ error_actual_3 % 2
print(f"\nActual error 3: {error_actual_3}")
print(f"Generated syndrome 3: {syndrome_3}")
predicted_error_3 = m.decode(syndrome_3)
print(f"Predicted error 3: {predicted_error_3}")
is_correct_3 = np.array_equal(predicted_error_3, error_actual_3)
print(f"Decoding correct for error 3? {is_correct_3}")

# Example with no error
error_actual_none = np.array([0, 0, 0])
syndrome_none = H @ error_actual_none % 2
print(f"\nActual error (none): {error_actual_none}")
print(f"Generated syndrome (none): {syndrome_none}")
predicted_error_none = m.decode(syndrome_none)
print(f"Predicted error (none): {predicted_error_none}")
is_correct_none = np.array_equal(predicted_error_none, error_actual_none)
print(f"Decoding correct for no error? {is_correct_none}")
