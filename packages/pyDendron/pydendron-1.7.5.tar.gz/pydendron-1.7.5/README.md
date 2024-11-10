pyDendron

## Dendrochronology: Wikipedia

``Dendrochronology (or tree-ring dating) is the scientific method of dating tree rings (also called growth rings) to the exact year they were formed in a tree. As well as dating them, this can give data for dendroclimatology, the study of climate and atmospheric conditions during different periods in history from the wood of old trees. Dendrochronology derives from the Ancient Greek dendron (δένδρον), meaning "tree", khronos (χρόνος), meaning "time", and -logia (-λογία), "the study of".''

## pyDendron

*pyDendron* is an open-source Python package dedicated to dendrochronology. It provides a web-based graphical user interface (GUI) for managing, plotting, and dating data. *pyDendron* is developed by members of the GROUping Research On Tree-rings Database (GROOT), one of the three workshops within the BioArcheoDat CNRS interdisciplinary research network.

Development is in its early stages.

## Requirements 

- [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) or [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/). Miniconda is recommended.

- Download miniconda and install it. Default options are OK. 
Choose the version that corresponds to our OS: [Miniconda installer links](https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/)

### Option: mdb-tools for Sylphe database import

- install mdb-tools programs

- On Linux (debian example)
```bash
apt-get install mdb-tools
```

- On macOS
```bash
brew install mdb-tools
```

- On Windows
    - Download zip on https://github.com/lsgunth/mdbtools-win,
    - copy file in `miniconda3/scripts` directory (simple but dirty method) or add the location directory in your `$PATH`.

## Installation

- On Linux and macOS, open a terminal. On Windows, open Anaconda Prompt (available from the Windows menu).
<!--
- pyDendron can be installed on Linux, Windows, or macOS with ``pip``:

```bash
pip install pyDendron
```
-->
The installation is done with ``conda``, but add conda-forge channel before installing pyDendron:

```bash
conda config --add channels conda-forge
```
Command to install pyDendron
```bash
conda install symeignier::pyDendron
```

## Run application
- On Linux and macOS, open a terminal. On Windows, open Anaconda Prompt (available from the Windows menu).
- Launch *pyDendron*: 
```bash
pyDendron
```
- On Windows, you can create a shortcut to `miniconda3/scripts/pyDendron.exe` the Windows menus or Taskbar.

### Update pyDendron 
<!--
with pip:
```bash
pip install --upgrade pyDendron
```

with conda:
-->
```bash
conda update pyDendron
```
