# Apps for aquaculture and fishing usage

This folder contains different applications that can make simulations easier. 
The app's name indicates it functionality. 
An alternative way to use this function is to create a link in your working folder, 
then using python to execute it. An example of running the app is shown as below:
```
python3 creatmesh.py
```

Through creatmesh.py, the code can generate two files, one is mesh file end with .med, the other is meshinformation.txt 
which contains the information for further simulations. 

Any questions about this code, please email: hui.cheng@uis.no

The available numerical models are:

- Cylindrical fish cage with bottom net

    The fish cage is a cylindrical shape. And it has a bottom which can be either flat or cone shape(according to the "cagebottomcenter" )
 
 - Cylindrical fish cage without bottom net

    The fish cage is a cylindrical shape. And it do not take the bottom into numerical simulation to 
    generate some corresponding results with experiments.

-----
 Ongoing model:
- trawl net

    Generate the mesh file for trawl net, The node and line connection are read from external files.
    And there is a rule for the line connection file.

- Cylindrical fish cage with mooring system
- Squared fish cage with(out) bottom with(out) mooring system