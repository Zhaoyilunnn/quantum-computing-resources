# Getting Started

## Learning Quantum Basis

There're lots of tutorials for quantum computing, we recommend to start from the book "[Quantum computation and quantum information, 10th anniversary](https://github.com/Zhaoyilunnn/qcs/blob/main/doc/tutorials/Quantum%20computation%20and%20quantum%20information.pdf)". To get familiar with some basic concepts, reading Sec. 1.2-1.3 and Sec. 2.1-2.2 is more than enough. Trying to solve the exercise problems of this book is extremely helpful, you can refer to this [forked repository](https://github.com/Zhaoyilunnn/SolutionQCQINielsenChuang) for solutions of Sec. 2 and Sec. 9, and we encourage you to add solutions for other sections and we can contribute to the original repository.

Besides this book, there are some tutorials of different software frameworks. We recommend [qiskit tutorials](https://qiskit.org/documentation/tutorials.html) and Baidu [qulearn](https://qulearn.baidu.com/). It is also recommended to get familiar with qiskit framework.

You can also go through this [awesome list](https://github.com/desireevl/awesome-quantum-computing) of quantum computing.

### Know about NISQ
We're now in the [Noisy Intermediate Scale Quantum](http://arxiv.org/abs/1801.00862) era. It is recommended to go through [this paper](http://arxiv.org/abs/1801.00862) to understand the fundamental concepts and limitations of NISQ quantum computers. Moreover, it is helpful to learn about NISQ algorithms. Many well-know algorithms like [Shor's algorithm](https://doi.org/10.1137/S0036144598347011) and [Grover's algorithm](https://link.aps.org/doi/10.1103/PhysRevLett.79.325) require fault-tolerant quantum computers, which may take decades to realize. NISQ algorithms are developed for NISQ devices and potentially have practical applications in the near future.
There're some great review papers of NISQ algorithms.
1. [Noisy intermediate-scale quantum (NISQ) algorithms](http://arxiv.org/abs/2101.08448) 
2. [Variational quantum algorithms](https://www.nature.com/articles/s42254-021-00348-9)

### Check Your Knowledge
Generally we recommend to *learn through research*. However it is necessary to get familiar with some basic concepts.
If you could answer following questions without referring to textbooks, you should be ready to move forward to read papers in the field of quantum computer system.
1. What is the state of an $N$-qubit system?
2. What is pure state and mixed state?
3. Could you write down the matrix form of following quantum operations: $X$, $Y$, $Z$, $X$, $H$, $CNOT$?
4. How could a single qubit be represented in a bloch sphere?
5. Could you write down the state of a quantum system after measurement?
6. What are projective measurements and POVM measurements?
7. What is an *observable*?

## Reading Papers
The "[Quantum Computer Systems -- Research for Noisy Intermediate-Scale Quantum Computers](https://github.com/Zhaoyilunnn/qcs/blob/main/doc/tutorials/Quantum%20Computer%20Systems.pdf)" by [Yongshan Ding](https://www.yongshanding.com/) and [Fred Chong](http://people.cs.uchicago.edu/~ftchong/) is a great book to glance through and learn about the topics that system-architecture community cares.

Currently we primarily focus on three aspects of quantum computer system.
 - Design automation of quantum circuits.
 - Quantum computer system software.
 - Quantum circuit simulation.

Our target conferences include top conferences in computer architecture and design automation listed in [CS rankings](https://csrankings.org/), i.e., [ISCA](https://csconferences.org/#ISCA), [MICRO](https://csconferences.org/#MICRO), [HPCA](https://csconferences.org/#HPCA), [ASPLOS](https://csconferences.org/#ASPLOS), [DAC](https://dblp.org/db/conf/dac/index.html), [ICCAD](https://dblp.org/db/conf/iccad/index.html).

### How to find papers
[DBLP](https://dblp.org/) and [Google Scholar](https://scholar.google.com/) are recommended to search papers. We also build a [script](https://github.com/Zhaoyilunnn/utils/tree/main/research) to find papers from DBLP.

### How to read papers
Bare in mind the following questions when reading papers.
 - What problem this paper is trying to solve?
 - Why this is a problem?
 - How they solve it?
 - Why they are better than other state-of-the-art approaches?

# Miscellaneous

## Notes
There are some of my personal notes of learning quantum basis and reading papers. You could find some representative papers in different directions.
 - [Quantum Basis](https://gist.github.com/Zhaoyilunnn/788c9eac3d8af18b3e3258e982505d40)
 - [Quantum Computer Architecture](https://gist.github.com/Zhaoyilunnn/4f050154941fb87b33d47c2d09aa23ae)
	 - [Qudit](https://gist.github.com/Zhaoyilunnn/4f050154941fb87b33d47c2d09aa23ae#multi-level)
  	 - [Control Architecture](https://gist.github.com/Zhaoyilunnn/4f050154941fb87b33d47c2d09aa23ae#control-processor)
 - [Quantum Error](https://gist.github.com/Zhaoyilunnn/1eb8a512f0c087b47a233c0720004994)
	 - [Error Mitigation](https://gist.github.com/Zhaoyilunnn/1eb8a512f0c087b47a233c0720004994#error-mitigation)
	 - [Error Correction](https://gist.github.com/Zhaoyilunnn/1eb8a512f0c087b47a233c0720004994#error-correction)
 - [Quantum Compiler](https://gist.github.com/Zhaoyilunnn/c3a031815ac43c5894b3b8cdf643775a)
 - [Quantum Programming Language](https://gist.github.com/Zhaoyilunnn/ddd4eeaeb475cd2b075fda176e4692c6)
 - [Quantum System Software](https://gist.github.com/Zhaoyilunnn/c43d40f895f57ce136b9b3701e7a5668)
 - [Quantum Circuit Simulation](https://gist.github.com/Zhaoyilunnn/07f5e6913dfa00fefbd4a8bff638f0bf)
	 - [Tensor Network](https://gist.github.com/Zhaoyilunnn/07f5e6913dfa00fefbd4a8bff638f0bf#tensor-network)

## Reference

If you find some interesting papers, please add an bibtex entry (use [this tool](https://www.doi2bib.org/) or google scholar to get bibtex entry) in [references.bib](https://github.com/Zhaoyilunnn/qcs/blob/master/doc/references.bib). (You can use this [tool](https://github.com/FlamingTempura/bibtex-tidy) ([website](https://flamingtempura.github.io/bibtex-tidy/)) to remove redundancy). We can reuse this file when writting papers.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEzMzk4MTczMzEsLTExNTk0NjE3MzUsMT
AzNzM4MzQxOF19
-->