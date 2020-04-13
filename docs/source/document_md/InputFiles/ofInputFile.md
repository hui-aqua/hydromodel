## netDict for OpenFOAM

An Example:
```
NetInfo1
{
    Sn                             0.20;
    PorousMediaThickness           0.045; 
    halfMeshSize                   29e-3; 
    twineDiameter	           2.8e-3; 
    fluidDensity                   1000.0;
    velocityUpdateInterval         0; 
    velocityProbeCorrection        (1 0 0);		
    ropeEnhance                    0;
}
```
The name of the variable in the net information (NetInfo1) is quite straight forwards.

- **Sn** is the solidity of net panel, which is usually between 0-1.

- **PorousMediaThickness** is the thickness of porous media. 

- **halfMeshSize** is the minimum knot-to-knot distance.

- **twineDiameter** is the diameter of the net twine.

- **fluidDensity** is the density of the fluid.

- **velocityUpdateInterval** is the velocity update time step, when the value is 0, the velocity will update at each time step.

- **velocityProbeCorrection** is the correction vector for velocity probe. during the FSI, the velocity on each net element is corrected by moving the reference probe a certain distance along the input vector. 

- **ropeEnhance** is used to show the velocity field of netting with stitching rope.
    - 0: no enhance, might be a hole; 
    - 1: the thickness of twine is the same with thickness of net; 
    - 2: enhanced, the thickness of twine is twice the thickness of net.