# ny_jointsFollowingCurve
## Autodesk Maya tool to create joints/controllers on a NURBS curve

![Maya Tool_ Joints Following Curve-low](https://user-images.githubusercontent.com/41262770/115991394-d594a000-a5d0-11eb-87a8-2d73c79f2ba4.gif)

https://vimeo.com/348662006

**FEATURES**: Can create any number of joints/controllers. Scalable. Optional offset locators.

**INSTALL**: Paste the "ny_jointsFollowingCurve.py" file to your "\maya\20**\scripts" folder.

**HOW TO USE**: Run this Python code: `import ny_jointsFollowingCurve;reload (ny_jointsFollowingCurve)`

Give your setup a unique name, then enter the number of joint you want(minimum 2).  
If you want controllers for each CV on the curve, select for Each CV.  
If you want controllers with a defined number, use the Ctrl Number button and put in a number.  
If you choose neither of them or leave Ctrl Number at 0, it won't create any controllers.  
