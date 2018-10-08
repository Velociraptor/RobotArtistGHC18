# RobotArtistGHC18
Information and starter code for the Program a Robot Artist workshop presented at the 2018 Grace Hopper Celebration by Evelyn Parenteau and Hannah Sarver. We built custom Arduino-based drawing robots for use in this workshop, but hope to include enough information here for anyone to replicate the workshop. Please feel free to reach out to us at hbsarver@gmail.com with questions or comments!

# Starter Code
The GHCRobotArtistStarter folder and included .ino file contain some starter functions (ie drive_forward, turnLeft) that can be used to build up code to draw shapes. To get started, simply load the .ino in the Arduino IDE and upload to your robot via serial cable. These are suggestions and can be modified, and we hope the documentation is sufficient to tell what they're each doing. Modify the "drawPicture" function to draw your desired design -- we recommend starting with something seemingly simple like drawing a square to get a sense of the challenges working with a real-world robot.

# Example Code
We have provided some code that we experimented with to draw a couple of different example shapes, in the ExampleDrawings directory.
![Sample Robot Drawing Images](https://github.com/Velociraptor/RobotArtistGHC18/blob/master/Images/ExampleDrawingsOutput.png)

# Robot Features
![Robot Architecture Features](https://github.com/Velociraptor/RobotArtistGHC18/blob/master/Images/RobotArchitecture.png)
![Robot Control Features](https://github.com/Velociraptor/RobotArtistGHC18/blob/master/Images/RobotControlFeatures.png)

# Assembly Instructions
See the [PDF file here](AssembblyInstructions.pdf) (warning: 40 MB)

# Bill of Materials
We've included the list of materials we used for building our workshop robots. Of course this is just one option of a kit of parts, but this set allowed us to have all the capabilities we were looking for and were available in the quantities we needed.

# Chassis Design & Script
Our robot chassis design is pretty cool! It's a code-generated .svg file that can be read by laser-cutter software to cut a robot chassis (or many) out of acrylic or other plastic. Check out the [readme](chassis/README.md)
