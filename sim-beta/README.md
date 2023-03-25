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

### Install cmake
```
$ curl -L https://github.com/Kitware/CMake/releases/download/v3.24.3/cmake-3.24.3-linux-x86_64.tar.gz --output cmake-3.24.3-linux-x86_64.tar.gz
$ tar -zxf cmake-3.24.3-linux-x86_64.tar.gz
$ cd cmake-3.24.3-linux-x86_64
# Then add bin to $PATH or copy cmake to path
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

### Install conan
```
pip install conan=1.52.0
```

### Build & Test

```
$ mkdir build
$ cd build
$ conan install ..
$ cmake ..
$ make -j 8
$ make test
$ # Alternatively, cd ../test && ../build/bin/simtest
```
