# Force model
This folder is to build the hydrodynamic force model in the FE solver. 
In this folder, there are few script for different applications

- hydro4c_mother.py:
 
 This file contains the original hydrodynamic force models for pure current conditions. 
 Some of the code can be reused in other python files. Note: you should not use this model to calculate 
 the hydrodynamic force on nets.
 
 - hydro4c1.py
 
 Build the hydrodynamic models using class method. It can be used for fish cage under pure current conditions. 
 Or it can also do simulations for trawl net.
 
 - hydro4c2.py

Build the hydrodynamic models using function method. This is an old version of hydrodynamic code, it can be used for debugging the errors. 

- hydro4wc.py

For combined waves and current conditions, for trawl net and fish cages.