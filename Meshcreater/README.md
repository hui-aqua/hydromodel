# Mesh creator
This folder contains different numerical models, which are named according to its shape.
The script can be run by the following command in terminal:

```
python3 creatmesh.py
```
The code and generate three files, one is mesh file end with .med; 
One is line connection file witch can be used to calculate the hydrodynamic forces based on Morison models;
The last on is the surface connection file, which can be used to calculate the hydrodynamic forces according to Screen models.

Any questions about this code, please email: hui.cheng@uis.no

The available numerical models are:

- cylindrical fish cage with bottom 
The fish cage is a cylindrical shape. And it has a bottom which can be either flat or cone shape
 (according to the "cagebottomcenter" at line 37)
 
trawlnet.py:

Generate the mesh file for trawl net, The node and line connection are read from external files.
