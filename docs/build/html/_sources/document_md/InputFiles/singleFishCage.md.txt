# Guide for input file  --- cageDict 

![alt text](../figures/Figure19.png)

Currently, cageDict is the only one input file for the program and it contains all the necessary information for numerical simulations.     
    
CageDict is a python dictionary style input file. The name of this dictionary can be varied as you wish.     
Just follow the syntax of a dictionary and record all the necessary parameters for simulations.      

There are some assumptions when we generate mesh for simulations:

* Although the flow direction can be change in the **Environment**, we assume the X+ is the flow direction when we generate the mesh.



Here is the explanation of the parameters in the dictionary.    
  
  
## Environment 

The information about the environmental conditions.  
1. **current**: a python list. Unit: [m/s]. 
    
    -  One velocity,  ```[[u,v,w]]```.  Input the three components of the current velocity that you are indented to use.     
    -  Multiple velocities,  ```[[u1,v1,w1],[u2,v2,w2],[u3,v3,w3]...[un,vn,wn]]``` . Input the current velocities as a list of velocity. The program will run each velocity within the given timeLength sequentially.    
  
2. **waterDepth**:  a floating point number. Unit: [m]. The depth of water. 
  
3. **waves**:  a python list or "False".

    - If there is no wave, please use ```False``` to disable it. 
    - If wave are applied to the environment, Please use ```[wave height, wavelength]``` to define a deep water airy wave. Unit: [m] 
 
4. **fluidDensity**: a floating point number. Unit: [kg/m^3]. The density of fluid, sea water: 1025, fresh water: 1000.

## MeshLib

**MeshLib** is used to tell the mesh generator which library will be used to generate mesh.
The value is used in the net panel(s) is ```cylindrical_NB_cage```.

## CageShape
Define the shape of cage.

1. **shape**: a string chosen from belows. Unit: [-].
    - ```cylindrical-NoBottom```: a cylindrical fish cage without bottom net. 
    - ```cylindrical-WithBottom```: a cylindrical fish cage with bottom net. The bottom can be a flat plane or a cone shape. If it is a cone shape, the **cageCenterTipDepth** should be larger thant **cageHeight**.
    - ```squared-NoBottom```:  a squared fish cage without bottom net.  
    - ```squared-WithBottom```: a squared fish cage with bottom net.  
    
2. **elementOverCir**: a integer number. Unit: [-]. The element that along the circumference of fish cage. 

3. **elementOverHeight**: a integer number. Unit: [-]. The element that along the height of fish cage. 

4. **cageDiameter**: a floating point number. Unit: [m]. The diameter of the fish cage.

5. **cageHeight**: a floating point number. Unit: [m]. The height of the fish cage

6. **cageCenterTipDepth**:a floating point number. Unit: [m]. The depth of cone shape.

## Net
Define the netting of cage. 

1. **HydroModel**: a string to indicate the hydrodynamic model. A detailed explanation can be found later.   
    - Screen model: ```Screen-S1```, ```Screen-S2```, ```Screen-S3```...  
    - Morison model: ```Morison-M1```, ```Morison-M3```, ```Morison-M3```...

2. **nettingType**: a string to indicate the netting type. 
    - ```square```: square netting that are commonly used in aquaculture cage
    - ```rhombus```: rhombus netting that are commonly used in fishing gear, e.g., trawl net, purse seine.

3. **Sn**: a floating point number. Unit: [-]. The solidity ratio of netting. 

4. **twineDiameter**: a floating point number. Unit [m]. The diameter of twine in the physical netting.

5. **meshLength**: a floating point number. Unit [m]. The half mesh length of the physical netting. 

6. **netYoungmodule**: a floating point number. Unit [Pa]. The Young's modulus of netting.

7. **netRho**: a floating point number. Unit: [kg/m^3]. The density of the netting.

## FloatingCollar

Define the floating collar of cage. 

1. **floaterCenter**:a python list. Unit: [m].
    -  One cage,  ```[x,y,z] ```.  Input the position of the floater center.                                                  
    -  Multiple cages,  ```[[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]...[xn,yn,zn]]``` . If there are multiple cages, input the position of each floater center and make it a python list. 

2. **collarNumber**: a integer number. Unit: [-]. The number of floater collar. 

3. **topRingRadius**: a floating point number. Unit [m]. The pipe diameter of the floating pipe.

4. **SDR**: a floating point number. Unit [-]. The ratio of pipe diameter to wall thickness.

5. **floaterRingRho**: a floating point number. Unit [kg/m^3-]. The effective density of floater collar. 

6. **floaterRingYoungModule**: a floating point number. Unit [Pa]. The Young's modulus of floater collar.

## Weight
Define the weight system of cage. 
1. **weightType**: a string to indicate the weight type. 
    - ```sinkers```: conventional type, numbers of sinkers are hung at the bottom of fish cage
    - ```allfixed```: all the nodes are fixed. Thus, the fish cage have no deformation. 
    - ```sinkerTube```: Using sinker tube to keep cultivation volume. 
    - ```sinkerTube+centerweight```: sinker tube + center weight to keep the cultivation volume.

2. **bottomRingRadius**: a floating point number. Unit [m]. The pipe diameter of the sinker tube.

3. **bottomRingDepth**: a floating point number. Unit [m]. The initial depth of bottom ring.
 
4. **SDR**: a floating point number. Unit [-]. The ratio of pipe diameter to wall thickness.
 
5. **bottomRingRho**: a floating point number. Unit [kg/m^3-]. The effective density of floater collar. 
      
6. **bottomRingYoungModule**: a floating point number. Unit [Pa]. The Young's modulus of floater collar.
                 
7. **numOfSinkers**: a integer number. Unit: [-]. The number of sinker.

8. **sinkerWeight**: a floating point number. Unit [N]. The submerged wight of each sinker.

9. **tipWeight**: a floating point number. Unit [N]. The submerged wight at the cone tip. 

## Mooring
Define the mooring system of cage. 

1. **mooringType**:a string to indicate the mooring type.
    - ```None```: No mooring system. The floating collar is fixed on the sea surface.
    - ```hastag```: The mooring system is looked like '#' structure. 
    - ```Xshape```: The mooring system is looked like 'X' structure.

2. **frameLength**': a floating point number. Unit [m]. The length of the fame line, distance between two buoys.

3. **bouncyForce**':a floating point number. Unit [N]. The Maximum bouncy force that the buoy can provide.

4. **bouncyLine**:a floating point number. Unit [m]. The length of the buoy line, distance between the buoy and plate.

5. **mooringLine**: a floating point number. Unit [m]. The length of the mooring line, distance between the mooring point and plate.

## Solver
Define the solver of simulation
 
1. **version**: a string to indicate the version of code_Aster. You can use the following type:
```stable```, ```testing```.
  
2. **coupling**: a string to indicate the whether or not using coupling.
    - ```False```: No coupling. Calculated only with Code_Aster
    - ```FSI```:  Fully couple with OpenFoam. 
    - ```simiFSI```: Semi coupled, only transfer the value from code_aster to OpenFOAM

3. **method**: a string to indicate the method to solve the equation. 
```HHT```: hht-alpha method. 

4. **alpha**:a floating point number for alpha in hht-alpha method.
```24.3``` is the default number for netting. 

5. **timeStep**: a floating point number. Unit [s]. The time step for simulations, usually between 0.2-0.01.

6. **timeLength**: a floating point number. Unit [s]. The length of time for the simulation with each current velocity. Usually, 10 s is enough to reach equilibrium. 

7. **MaximumIteration**: a integer number. Unit: [-]. The number of iteration at each time step, the default value is ```1000```.

8. **Residuals**: a floating point number. Unit [-]. The threshold for the maximum of residual.








