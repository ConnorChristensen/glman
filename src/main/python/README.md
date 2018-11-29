# GLman Code Documentation

Since this program is supposed to be a tool for learning, I wanted to make sure that it is well documented so anyone can play around with the source code.
This will be used to address general concepts, as well as particularly tricky bits of code.

## References

* [DrxMario/PyOpenGL-Tutorial](https://github.com/DrxMario/PyOpenGL-Tutorial) provided the `createProgram`, `findFileOrThrow` and `loadShader` functions

## General Layout

This code has two major classes in it:

* `Window`: The is the one that controls everything in the application
* `MakeGLWidget`: This is the one that controls the GL window within the application

There is also a shapes library that holds a collection of functions that will draw a shape in openGL.
The `inspect` library is used to examine which functions exist in the shapes library and make sure that it only calls the shapes that are defined.

## Tricky Bits of Code

### Slider Connection Lambda Function
Here is the code:

```python
slider.valueChanged.connect( lambda newValue, programName=programName, variableName=variableName: self.glWidget.setUniformVariable(programName, variableName, newValue) )
```

Each slider has a connection function to make sure that something in the program can be changed whenever the slider is set to a new value.
The `connect` function requires a function as it's parameter, and it will pass a single integer into the parameters of the function it calls.
In the context that this line is being written, it is happening in three nested for loops. 
This is a critical reason why this lambda function looks so strange.

The context of the for loops in the program are as follows:

For each program we have, loop through all the key value pairs, and if the key says that it is holding all the variables, then loop through those variables.

So this lambda function takes in three values:

* The `newValue` that the slider has been set to
* The `programName` which is the name of the program that this variable belongs to
* The `variableName` which is the name of the variable that we are updating

The last two variables are given default values, which serves the purpose of binding those variables to the value that they hold at that iteration in the loop.
Without this binding, the value for every lambda function that is created is going to be the last value that the loop runs through.

