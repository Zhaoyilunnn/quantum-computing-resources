import qiskit_aer.noise as noise


def ideal():
    return None


def depolarizing_model():
    """
    Example: depolarizing model
    Ref: https://qiskit.org/documentation/apidoc/aer_noise.html
    """
    # Error probabilities
    prob_1 = 0.001  # 1-qubit gate
    prob_2 = 0.01   # 2-qubit gate
    
    # Depolarizing quantum errors
    error_1 = noise.depolarizing_error(prob_1, 1)
    error_2 = noise.depolarizing_error(prob_2, 2)
    
    # Add errors to noise model
    noise_model = noise.NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_1, ['u1', 'u2', 'u3'])
    noise_model.add_all_qubit_quantum_error(error_2, ['cx'])
    
    return noise_model


class NoiseModelProvider:

    _NOISE_MODELS = {
        'ideal': ideal,
        'depolarizing': depolarizing_model
    } 

    def get_noise_model(self, noise_model_name):
        return self._NOISE_MODELS[noise_model_name]()


Noise = NoiseModelProvider()
