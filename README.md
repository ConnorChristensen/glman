
# GLman

This is a program for making interacting with OpenGL and shaders easy. 

## At a Glance
This program allows you to:

* Abstract away all the code needed to set up an OpenGL
* Abstract away all the code needed to link shaders into the graphics pipeline
* Provide sliders for variables that are passed into shaders, so you can play around with shader values in real time.


## Running the Source Code
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
The rest of the code is the build process.

