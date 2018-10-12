
# glman

## Development
To ensure consistency, make a virtual environment for development.

1. Create your environment: `python3 -m venv venv`
2. Activate your environment:
	* Mac/Linux: `source venv/bin/activate`
	* Windows: `call venv\scripts\activate.bat`
3. Install the required frameworks: `pip install fbs PyQt5==5.9.2 PyInstaller==3.3.1`

Then to run the program:

```
python -m fbs run
```

The code to modify for the project is located in the `src/main/python/` directory.
The rest of the code is the build process