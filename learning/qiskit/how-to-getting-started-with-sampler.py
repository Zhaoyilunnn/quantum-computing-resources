"""
qiskit                   0.39.0
qiskit-aer               0.11.0
qiskit-ibmq-provider     0.19.2
qiskit-terra             0.22.0
"""

#!/usr/bin/env python
# coding: utf-8

# # Get started with the Sampler primitive

# In this tutorial we will show you how to set up the Qiskit Runtime `Sampler` primitive, explore the different options you can use to configure it, and invoke the primitive efficiently inside a session.

# ## Primitives

# [Primitives](https://qiskit.org/ecosystem/ibm-runtime/primitives.html) are core functions that make it easier to build modular algorithms and applications.
#
# The initial release of Qiskit Runtime includes two primitives:
#
# **Sampler:** Generates quasi-probability distribution from input circuits.
#
# **Estimator:** Calculates expectation values from input circuits and observables.

# In this tutorial we will focus on the `Sampler` primitive. There is a separate tutorial on [Getting started with the Estimator primitive](how-to-getting-started-with-estimator.ipynb).

# ## Using the Sampler primitive

# Similar to the `Backend` base class, there is an `Sampler` base class defined in Qiskit Terra that standardizes the way users interact with all `Sampler` implementations.
# This allows users to easily change their choice of simulator or device for performing expectation value calculations, even if the underlying implementation is different.
#
# In this section we will be using the default implementation in Qiskit Terra, which uses a local state vector simulator.

# ### 1. Create a circuit

# You will need at least one quantum circuit to prepare our system in a precise quantum state for study. Our examples all have circuits in them, but you can use Qiskit to create your own. To learn how to create circuits by using Qiskit, see the [Circuit basics tutorial](https://qiskit.org/documentation/tutorials/circuits/01_circuit_basics.html).

# In[1]:


from qiskit.circuit.random import random_circuit

circuit = random_circuit(2, 2, seed=0, measure=True).decompose(reps=1)


# ### 2. Initialize a Sampler class

# <!-- vale off -->
# The next step is to create an instance of an `Sampler` class, which can be any of the subclasses that comply with the base specification. For simplicity, we will use Qiskit Terra's `qiskit.primitives.Sampler` class, based on the [Statevector construct](https://qiskit.org/documentation/stubs/qiskit.quantum_info.Statevector.html?highlight=statevector#qiskit.quantum_info.Statevector) (that is, algebraic simulation).
# <!-- vale on -->

# In[2]:


from qiskit.primitives import Sampler

sampler = Sampler()


# ### 3. Invoke the Sampler and get results

# To estimate the quasi-probability distribution of the circuit output, invoke the `run()` method of the `Sampler` instance you just created and pass in the circuit as an input parameter. This method call is asynchronous, and you will get a `Job` object back. You can use this object to query for information like `job_id()` and `status()`.

# In[3]:


job = sampler.run(circuit)
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")


# The `result()` method of the job will return the `SamplerResult`, which includes both the quasi-probability distribution and job metadata.

# In[4]:


result = job.result()
print(f">>> {result}")
print(f"  > Quasi-probability distribution: {result.quasi_dists[0]}")


# You can keep invoking the `run()` method again with the different inputs:

# In[5]:


circuit = random_circuit(2, 2, seed=1, measure=True).decompose(reps=1)

job = sampler.run(circuit)
result = job.result()

print(f">>> Quasi-probability distribution: {result.quasi_dists[0]}")


# You can also provide compound inputs to the `run()` method:

# In[6]:


circuits = (
    random_circuit(2, 2, seed=0, measure=True).decompose(reps=1),
    random_circuit(2, 2, seed=1, measure=True).decompose(reps=1),
)

job = sampler.run(circuits)
result = job.result()

print(f">>> Quasi-probability distribution: {result.quasi_dists}")


# Or use parameterized circuits:

# In[7]:


from qiskit.circuit.library import RealAmplitudes

circuit = RealAmplitudes(num_qubits=2, reps=2).decompose(reps=1)
circuit.measure_all()
parameter_values = [0, 1, 2, 3, 4, 5]

job = sampler.run(circuit, parameter_values)
result = job.result()

print(f">>> Parameter values: {parameter_values}")
print(f">>> Quasi-probability distribution: {result.quasi_dists[0]}")


# ## Using Qiskit Runtime Sampler

# In this section we will go over how to use Qiskit Runtime's implementation of the `Sampler` primitive.

# ### 1. Initialize the account

# Since Qiskit Runtime `Sampler` is a managed service, you will first need to initialize your account. You can then select the simulator or real backend you want to use to calculate the expectation value.
#
# Follow the steps in the [getting started guide](https://qiskit.org/documentation/partners/qiskit_ibm_runtime/getting_started.html) if you don't already have an account set up.

# In[8]:
