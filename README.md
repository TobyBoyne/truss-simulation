# truss-simulation
Calculates the forces acting on a given truss. Using content from Part IA Engineering, finds forces acting on each member of a statically determinate framework, and displays internal forces.

## Usage
Run `main.py`. To load a template structure, pass one of the examples from `examples.py` into the `EventHandler` object.  
To add a joint, click anywhere on the canvas. To add a member, click on one joint and drag to any other joint. To change the support type of a joint (pin joint, roller, static), right click on the joint.  
To apply a point force, select `FORCE` and drag from one of the joints.  
To delete any part, select `DELETE` and click on the part.

## Example  
Each of the thin black lines represent a force acting towards the joint.  
Below is the simulation of `square_and_triangle` found in `examples.py`.
![Square and Triangle](https://github.com/TobyBoyne/truss-simulation/blob/master/images/square_and_triangle.png)
