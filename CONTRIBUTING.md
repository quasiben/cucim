# Contribute to cuCIM

If you are interested in contributing to cuCIM, your contributions will fall
into three categories:
1. You want to report a bug, feature request, or documentation issue
    - File an [issue](https://github.com/rapidsai/cucim/issues/new/choose)
    describing what you encountered or what you want to see changed.
    - The RAPIDS team will evaluate the issues and triage them, scheduling
    them for a release. If you believe the issue needs priority attention
    comment on the issue to notify the team.
2. You want to propose a new Feature and implement it
    - Post about your intended feature, and we shall discuss the design and
    implementation.
    - Once we agree that the plan looks good, go ahead and implement it, using
    the [code contributions](#code-contributions) guide below.
3. You want to implement a feature or bug-fix for an outstanding issue
    - Follow the [code contributions](#code-contributions) guide below.
    - If you need more context on a particular issue, please ask and we shall
    provide.

## Code contributions

### Your first issue

1. Read the project's [README.md](https://github.com/rapidsai/cucim/blob/main/README.md)
    to learn how to setup the development environment
2. Find an issue to work on. The best way is to look for the [good first issue](https://github.com/rapidsai/cucim/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
    or [help wanted](https://github.com/rapidsai/cucim/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) labels
3. Comment on the issue saying you are going to work on it
4. Code! Make sure to update unit tests!
5. When done, [create your pull request](https://github.com/rapidsai/cucim/compare)
6. Verify that CI passes all [status checks](https://help.github.com/articles/about-status-checks/). Fix if needed
7. Wait for other developers to review your code and update code as needed
8. Once reviewed and approved, a RAPIDS developer will merge your pull request

Remember, if you are unsure about anything, don't hesitate to comment on issues
and ask for clarifications!

### Seasoned developers

Once you have gotten your feet wet and are more comfortable with the code, you
can look at the prioritized issues of our next release in our [project boards](https://github.com/rapidsai/cucim/projects).

> **Pro Tip:** Always look at the release board with the highest number for
issues to work on. This is where RAPIDS developers also focus their efforts.

Look at the unassigned issues, and find an issue you are comfortable with
contributing to. Start with _Step 3_ from above, commenting on the issue to let
others know you are working on it. If you have any questions related to the
implementation of the issue, ask them in the issue instead of the PR.


## Setting Up Your Build Environment

The following instructions are for developers and contributors to cuCIM OSS development. These instructions are tested on Linux Ubuntu 16.04 & 18.04. Use these instructions to build cuCIM from source and contribute to its development.  Other operating systems may be compatible, but are not currently tested.

### Code Formatting

#### Python

cuCIM uses [Black](https://black.readthedocs.io/en/stable/),
[isort](https://readthedocs.org/projects/isort/), and
[flake8](http://flake8.pycqa.org/en/latest/) to ensure a consistent code format
throughout the project. `Black`, `isort`, and `flake8` can be installed with
`conda` or `pip`:

```bash
conda install black isort flake8
```

```bash
pip install black isort flake8
```

These tools are used to auto-format the Python code in the repository. Additionally, there is a CI check in place to enforce
that committed code follows our standards. You can use the tools to
automatically format your python code by running:

```bash
isort --atomic python/**/*.py
black python
```

### Get libcucim Dependencies

Compiler requirements:

* `gcc`     version 9.0+
* `nvcc`    version 11.0+
* `cmake`   version 3.18.0+

CUDA/GPU requirements:

* CUDA 11.0+
* NVIDIA driver 450.36+
* Pascal architecture or better

You can obtain CUDA from [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads).


# Script to build cuCIM from source

### Build from Source

- Clone the repository
```bash
CUCIM_HOME=$(pwd)/cucim
git clone https://github.com/rapidsai/cucim.git $CUCIM_HOME
cd $CUCIM_HOME
```

- Create the conda development environment `cucim`:
```bash
conda env create -f ./conda/environments/env.yml
# activate the environment
conda activate cucim
```

- Build and install `libcucim` and `cucim` (python bindings):
```bash
export CC=$CONDA_PREFIX/bin/x86_64-conda_cos6-linux-gnu-gcc
export CXX=$CONDA_PREFIX/bin/x86_64-conda_cos6-linux-gnu-g++
./run build_local all release $CONDA_PREFIX
```

- Build command will create the following files:
  - ./install/lib/libcucim*
  - ./python/install/lib/_cucim.cpython-38-x86_64-linux-gnu.so
  - ./cpp/plugins/cucim.kit.cuslide/install/lib/cucim.kit.cuslide@*.so

- Install libcucim/cuslide/cucim(python):
```bash
# libcucim
cp -P -r install/bin/* $CONDA_PREFIX/bin/
cp -P -r install/lib/* $CONDA_PREFIX/lib/
cp -P -r install/lib/* $CONDA_PREFIX/lib/
cp -P -r install/include/* $CONDA_PREFIX/include/

# cuslide plugin
cp -P -r cpp/plugins/cucim.kit.cuslide/install/bin/* $CONDA_PREFIX/bin
cp -P -r cpp/plugins/cucim.kit.cuslide/install/lib/* $CONDA_PREFIX/lib/

# cucim (python)
cp -P python/install/lib/* python/cucim/src/cucim/clara/
cd python/cucim/
python -m pip install .
```
