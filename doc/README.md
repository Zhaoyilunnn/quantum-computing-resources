# Getting Started

## Learning Quantum Basis

There're lots of tutorials for quantum computing, we recommend to start from the book "[Quantum computation and quantum information, 10th anniversary](https://github.com/Zhaoyilunnn/qcs/blob/main/doc/tutorials/Quantum%20computation%20and%20quantum%20information.pdf)". To get familiar with some basic concepts, reading Sec. 1.2-1.3 and Sec. 2.1-2.2 is more than enough. Trying to solve the exercise problems of this book is extremely helpful, you can refer to this [forked repository](https://github.com/Zhaoyilunnn/SolutionQCQINielsenChuang) for solutions of Sec. 2 and Sec. 9, and we encourage you to add solutions for other sections and we can contribute to the original repository.

### Tutorials from various software frameworks

- IBM: [qiskit tutorials](https://qiskit.org/documentation/tutorials.html) (Qiskit is currently the most popular framework).
- Microsoft: [Azure Quantum](https://learn.microsoft.com/en-us/azure/quantum/)
- Baidu: [qulearn](https://qulearn.baidu.com/).
- Google: Qsim
- Huawei: mind-quantum
- ...

### Additional Resources

- [Awesome list of quantum computing](https://github.com/desireevl/awesome-quantum-computing).
- [5 Year Update to the Next Steps in Quantum Computing Report, 2023](https://github.com/Zhaoyilunnn/qcs/blob/main/doc/reports/5-Year-Update-to-the-Next-Steps-in-Quantum-Computing.pdf)

### Know about NISQ

We're now in the [Noisy Intermediate Scale Quantum](http://arxiv.org/abs/1801.00862) era. It is recommended to go through [this paper](http://arxiv.org/abs/1801.00862) to understand the fundamental concepts and limitations of NISQ quantum computers. Moreover, it is helpful to learn about NISQ algorithms. Many well-know algorithms like [Shor's algorithm](https://doi.org/10.1137/S0036144598347011) and [Grover's algorithm](https://link.aps.org/doi/10.1103/PhysRevLett.79.325) require fault-tolerant quantum computers, which may take decades to realize. NISQ algorithms are developed for NISQ devices and potentially have practical applications in the near future.
There're some great review papers of NISQ algorithms.

1. [Noisy intermediate-scale quantum (NISQ) algorithms](http://arxiv.org/abs/2101.08448)
2. [Variational quantum algorithms](https://www.nature.com/articles/s42254-021-00348-9)

### Check Your Knowledge

Generally we recommend to _learn through research_. However it is necessary to get familiar with some basic concepts.
If you could answer following questions without referring to textbooks, you should be ready to move forward to read papers in the field of quantum computer system.

1. What is the state of an $N$-qubit system?
2. What is pure state and mixed state?
3. Could you write down the matrix form of following quantum operations: $X$, $Y$, $Z$, $X$, $H$, $CNOT$?
4. How could a single qubit be represented in a bloch sphere?
5. Could you write down the state of a quantum system after measurement?
6. What are projective measurements and POVM measurements?
7. What is an _observable_?

## Reading Papers

The "[Quantum Computer Systems -- Research for Noisy Intermediate-Scale Quantum Computers](https://github.com/Zhaoyilunnn/qcs/blob/main/doc/tutorials/Quantum%20Computer%20Systems.pdf)" by [Yongshan Ding](https://www.yongshanding.com/) and [Fred Chong](http://people.cs.uchicago.edu/~ftchong/) is a great book to glance through and learn about the topics that system-architecture community cares.

Currently we primarily focus on three aspects of quantum computer system.

- Design automation of quantum circuits.
- Quantum computer system software.
- Quantum circuit simulation.

Our target conferences include (_but definitely not limited to_) top conferences in computer architecture and design automation listed in [CS rankings](https://csrankings.org/), i.e., [ISCA](https://csconferences.org/#ISCA), [MICRO](https://csconferences.org/#MICRO), [HPCA](https://csconferences.org/#HPCA), [ASPLOS](https://csconferences.org/#ASPLOS), [DAC](https://dblp.org/db/conf/dac/index.html), [ICCAD](https://dblp.org/db/conf/iccad/index.html).

### How to find papers

[DBLP](https://dblp.org/) and [Google Scholar](https://scholar.google.com/) are recommended to search papers. We also build a [script](https://github.com/Zhaoyilunnn/utils/tree/main/research) to find papers from DBLP.

Additionally, domain-specific journals including [ACM TQC](https://dl.acm.org/journal/tqc), [IEEE TQE](https://tqe.ieee.org/) and conferences like [QCE](https://qce.quantum.ieee.org/) also contain many valuable works.

Tips

- [Search for articles from a specific journal in Google Scholar](https://academia.stackexchange.com/questions/102122/how-to-search-for-articles-from-a-specific-journal-in-google-scholar-when-the-jo): `"key word" site:<site-address>`.

### How to read papers

Bare in mind the following questions when reading papers.

- What problem this paper is trying to solve?
- Why this is a problem?
- How they solve it?
- Why they are better than other state-of-the-art approaches?

My paper notes convention

- red: Challenges to solve / drawbacks of SOTA.
- green: Insights / Novelty / Philosophy.
- blue: Other key info.
