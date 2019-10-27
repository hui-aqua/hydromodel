# Mesh creator
This folder contains different numerical models, which are named according to its shape.
The script can be run by the following command in terminal:

```
/opt/salome2019/appli_V2019_univ/salome -t fishcagewithbottom.py
```
The code and generate three files, one is mesh file end with .med; 
One is line connection file witch can be used to calculate the hydrodynamic forces based on Morison models;
The last on is the surface connection file, which can be used to calculate the hydrodynamic forces according to Screen models.

Any questions about this code, please email: hui.cheng@uis.no

- fishcagewithbottom.py:
 
The fish cage is a cylindrical shape
 
The fish cage has a bottom, and the bottom can be flat or cone shape
 (according to the "cagebottomcenter" at line 37)
 
trawlnet.py:

Generate the mesh file for trawl net, The node and line connection are read from external files.
