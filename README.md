
# glman
This is a program for making interacting with OpenGL and shaders easy. 

## At a Glance
This program allows you to:

* Abstract away all the code needed to set up an OpenGL
* Abstract away all the code needed to link shaders into the graphics pipeline
* Provide sliders for variables that are passed into shaders, so you can play around with shader values in real time.

## User Guide
Once you have the application open, interaction is quite simple.
If you are familiar with shaders, you write them as you normally would. The way you plug those shaders into the application is through a **glib** file.

### A simple glib file
Let’s do an example glib file.
I have a vertex shader named `light.vert` and a fragment shader called `light.frag`.

```
vertex   light
fragment light
cube 1 1 1
```

This tells the application to look for a `.vert` and `.frag` file called light.
It will apply those shaders to the cube of size 1x1x1.

### Adding uniform variables
If you want to add in uniform variables, just declare your program before you draw your shape.

```
vertex   light
fragment light
program  Light {
	uShine <0.0 0.1 1.0>
}
cube 1 1 1
```

This makes the uniform variable called `uShine` that can be accessed in the shaders. 
This glib file specifies that `uShine` has a minimum value of 0.0, a maximum value of 0.1, and it will be set to 0.1 by default.

## Developer Guide
To ensure consistency, make a virtual environment for development.

1. Create your environment: `python3 -m venv venv`
2. Activate your environment:
	* Mac/Linux: `source venv/bin/activate`
	* Windows: call `venv\scripts\activate.bat`
3. Install the required frameworks: `pip install fbs PyQt5==5.9.2 PyInstaller==3.3.1 PyOpenGL PyOpenGL_accelerate`

Then to run the program:

```
python -m fbs run
```

The code to modify for the project is located in the `src/main/python/` directory.
There is a readme in that directory as well that contains way more info on how the code works.
If you would like to contribute, head over there.
The rest of the code in this repository is meant to build the application.

