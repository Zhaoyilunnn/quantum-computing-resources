# qcs
Research repo for Quantum Circuit Simulation

- sim-beta: C++ simulator 
- test\_data: logs for high-level testing and some test data
- tools: some tools

# sim-beta

## Build

System requirement
```
OS: Ubuntu 20.04
gcc: 9.4
cmake: 3.24.1
gflags: 2.2.2
conan: 1.52.0
```

### Install gflags
Follow the [guide](https://github.com/gflags/gflags/blob/master/INSTALL.md)

```
$ tar xzf gflags-$version-source.tar.gz
$ cd gflags-$version
$ mkdir build && cd build
$ ccmake ..

  - Press 'c' to configure the build system and 'e' to ignore warnings.
  - Set CMAKE_INSTALL_PREFIX and other CMake variables and options.
  - Continue pressing 'c' until the option 'g' is available.
  - Then press 'g' to generate the configuration files for GNU Make.

$ make
$ make test    (optional)
$ make install (optional)
```
