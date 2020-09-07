# User Guide for Hydrodynamic Model

Author: Hui Cheng

----

The Guide is built using [Phinx](https://www.sphinx-doc.org/en/master/index.html#)

If you do not have sphinx, please install first. It is very easy, just type
```shell
pip3 install -U Sphinx
```
## How to build the User Guide

1. Install Markdown support, i.e.: 
    
``` shell
pip3 install --upgrade recommonmark
```

2. Creat a folder for building, e.g.:
```
mkdir build
```
3.Build the User Guide
```
sphinx-build -b html source/ build/
```
where source is the folder for the source file, build is the flder that will contain the User Guide.

