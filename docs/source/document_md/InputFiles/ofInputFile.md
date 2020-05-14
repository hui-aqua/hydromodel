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
    velocityCorrector              1;
    velocityProbeCorrection        (1 0 0);		
    ropeEnhance                    0;
}
```
The name of the variable in the net information (NetInfo1) is quite straight forwards.

- **Sn** is the solidity of net panel, which is usually between 0-1.

- **PorousMediaThickness** is the thickness of porous media in OpenFOAM. Usually, the thickness of porous media should be 3-5 times of the mesh length.

- **halfMeshSize** is defined as the minimum knot-to-knot distance. It is called half mesh size in fishing and aquaculture community. 

- **twineDiameter** is the physical diameter of the net twine.

- **fluidDensity** is the density of the fluid.

- **velocityUpdateInterval** is the velocity update time step.

    * ```0```: The velocities on points will update at each time step.
    * ```1```: The velocities on points will update every 1 second.
     
- **velocityCorrector** is a scalar factor to correct the velocity. 

    - ```0```: All the output velocity from OpenFOAMon nodes are zeros. 
    - ```1```: All the output velocity from OpenFOAMon nodes are identical to the velocity in the corresponding cells.
    - ```1.5```: The output velocity is amplified by 1.5 times.

- **velocityProbeCorrection** is the correction vector for velocity probe. during the FSI, the velocity on each net element is corrected by moving the reference probe a certain distance along the input vector.
 
    - ```(0,0,0)``` The probe position will not be corrected, meaning the output velocities is extract from exact position.
    - ```(1,0,0)``` The probe position will move 1 unit length, usually 1 meter, along X+ direction. 
    
- **ropeEnhance** is used to show the velocity field of netting with stitching rope.

    - 0: no enhance, might be a hole; 
    - 1: the thickness of twine is the same with thickness of net; 
    - 2: enhanced, the thickness of twine is twice the thickness of net.