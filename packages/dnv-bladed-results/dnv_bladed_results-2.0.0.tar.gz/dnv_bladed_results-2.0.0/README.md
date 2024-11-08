# Bladed Results API 2.0

The Bladed Results API is an easy, fast, and robust way to access Bladed results using Python.

It provides features for:

- Discovering Bladed runs
- Finding variables in a set of runs
- Getting data from variables
- Reporting run and variable metadata
- Exploring and writing output groups.

The API is able to read results from any Bladed version.

The API depends on the [`numpy`](https://numpy.org) package.

> Currently only Windows is supported.

> Bladed Results API 2.0 replaces Results API 1.x which is being discontinued.

## Pre-requisites

- Requires a _32- or 64-bit Windows_ installation of:
  - Python 3.9
  - or Python 3.10
  - or Python 3.11
  - or Python 3.12

> 64-bit Python is recommended.

- The Results API has been tested on Windows 10.

### Quick Start

```shell
pip install dnv-bladed-results
```

```python
from dnv_bladed_results import *

run = ResultsApi.get_run(run_dir, run_name)
var_1d = run.get_variable_1d(variable_name)
print(var_1d.get_data())
```

### Code completion

We recommend enabling code completion in the IDE for the best user experience.  Code completion displays a popup listing the available functions as the user types.  Together with inline documentation, code completion makes it easy to explore and understand the API.

![Code completion](https://raw.githubusercontent.com/pmdnv/dnv-bladed-results/869a59758ff98d60c6f69bb4b123a9805221c558/images/code-completion.PNG)

For guidance on enabling and customising code completion, please refer to the following resources:

[`IntelliSense in Visual Studio Code`](https://code.visualstudio.com/docs/editor/intellisense)

[`Code completion in PyCharm`](https://www.jetbrains.com/help/pycharm/auto-completing-code.html)

> If using Visual Studio Code, a type hint is needed for code completion to work with API classes inside a loop.  This issue does not affect PyCharm.
> ```python
> # Note the following type hint declared on the run loop variable
> run: Run
> for run in runs:
>    # Do something with run - easy now code completion works!
> ```

> If using PyCharm, we recommend enabling the options "Show suggestions as you type" and "Show the documentation popup in...", available in Settings > Editor > General > Code Completion.

## Usage Examples

Usage examples demonstrating core functionality are distributed with the package.  A brief description of each example follows.

The `UsageExamples` installation folder and list of available examples may be enquired as follows:

```python
import os
from dnv_bladed_results import UsageExamples
print(UsageExamples.__path__[0])
os.listdir(UsageExamples.__path__[0])
```

The examples below show how each script may be launched from within a Python environment.

### Basic Operations

Load a Bladed run, request groups and variables, and get data for tower members and blade stations:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_BasicOperations
ResultsApi_BasicOperations.run_script()
```

### Variable Data

Load a Bladed run, request 1D and 2D variables* from both the run and from a specific output group, and obtain data from the returned variables:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ReadBasic
ResultsApi_VariableData_ReadBasic.run_script()
```

Obtain data from a 2D variable* for specific independent variable values, and specify the precision of the data to read:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ReadExtended
ResultsApi_VariableData_ReadExtended.run_script()
```

  > *1D and 2D variables are dependent variables with one and two independent variables respectively.

### Runs

Use filters and regular expressions to find a subset of runs in a directory tree:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_FindRuns
ResultsApi_FindRuns.run_script()
```

Find and process runs asynchronously using a Python generator:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_FindRunsUsingGenerator
ResultsApi_FindRunsUsingGenerator.run_script()
```

### Metadata

Get metadata for runs, groups, and variables:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_RunMetadata
ResultsApi_RunMetadata.run_script()
```

```python
from dnv_bladed_results.UsageExamples import ResultsApi_GroupMetadata
ResultsApi_GroupMetadata.run_script()
```

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableMetadata
ResultsApi_VariableMetadata.run_script()
```

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableStats
ResultsApi_VariableStats.run_script()
```

### Output

Export 1D and 2D Bladed output groups, as well as an entire run, using the HDF5 file format:

  > Requires the `h5py` library, available via pip: `pip install h5py`.  The example has been tested with h5py 3.11.0.

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ExportHDF5
ResultsApi_VariableData_ExportHDF5.run_script()
```

Export Bladed output groups using the Matlab file format:

  > Requires the `scipy` library, available via pip: `pip install scipy`.  The example has been tested with scipy 1.13.1.

```python
from dnv_bladed_results.UsageExamples import ResultsApi_VariableData_ExportMatlab
ResultsApi_VariableData_ExportMatlab.run_script()
```

Write 1D and 2D output groups using the Bladed file format:

```python
from dnv_bladed_results.UsageExamples import ResultsApi_WriteGroup
ResultsApi_WriteGroup.run_script()
```

### Charting

Create 2D and 3D plots of blade loads:

  > Requires the `matplotlib` library, available via pip: `pip install matplotlib`.  The examples have been tested with matplotlib 3.9.1.

```python
from dnv_bladed_results.UsageExamples import ResultsApi_Charting2D
ResultsApi_Charting2D.run_script()
```

```python
from dnv_bladed_results.UsageExamples import ResultsApi_Charting3D
ResultsApi_Charting3D.run_script()
```

### Post-Processing

Post-process two-dimensional variable data into bespoke data structures and into a Pandas DataFrame.
Plot the data choosing specific points of the DataFrame.

  > Requires the `matplotlib` library, available via pip: `pip install matplotlib`.  The example has been tested with matplotlib 3.9.1.
  
  > Requires the `pandas` library, available via pip: `pip install pandas`.  The example has been tested with pandas 2.2.3.

```python
from dnv_bladed_results.UsageExamples import ResultsApi_PostProcessing
ResultsApi_PostProcessing.run_script()
```

## Results Viewer example

The following images demonstrate how Bladed data shown in Results Viewer may be accessed using the Results API 2.0.

Results Viewer is a standalone package providing enhanced results viewing functionality. Bladed and the Results Viewer application are both available from the [`Downloads`](https://mysoftware.dnv.com/knowledge-centre/bladed/help-library/getting-started/installation#downloading-installers) page.

One-dimensional variables:

![ResultsViewer 1D](https://raw.githubusercontent.com/pmdnv/dnv-bladed-results/97a4982168df83f0f9260b7d0a27e7877df33f92/images/ResultsViewer_ResultsAPI_1D.png)

Two-dimensional variables:

![ResultsViewer 2D](https://raw.githubusercontent.com/pmdnv/dnv-bladed-results/97a4982168df83f0f9260b7d0a27e7877df33f92/images/ResultsViewer_ResultsAPI_2D.png)

## Data types

The API comprises a generated Python wrapper dispatching to a C++ DLL.  The DLL performs the work of fetching and storing data, validation, and memory management.

### NumPy support

All arrays returned or accepted by API functions are of type NumPy `ndarray`. These functions wrap the underlying data without copying*.

For every function returning a NumPy array, the API provides counterpart functions returning C-style native array denoted with the suffix `_native_array`. These functions slightly improve performance by avoiding the (generally small) cost of wrapping a native array as NumPy.

> For most purposes, the functions returning NumPy array should be preferred as they offer several useful functions and improved memory safety.

  *Functions returning a two-dimensional NumPy array, for example the 2D variable function `get_data_for_all_independent_variable_values`, perform a deep copy of the underlying data. In performance-sensitive code, the counterpart function returning native array should be preferred.

### One- and two-dimensional variable return types

The API has separate functions for getting 1D and 2D variables* primarily due to differences in the shape of the data and hence differences in the functions required to operate on the data.

  > *1D and 2D variables are dependent variables with one and two independent variables respectively. 

## Glossary

### Run

The output from running a Bladed calculation. Typically, this comprises several output _groups_, with each group containing variables that relate to a specific part of the model.

### Variable

In the context of the Results API, the term _variable_ is synonymous with _dependent variable_.

### Dependent variable

A variable calculated as the result of changing one or more independent variables. Dependent variables are listed next to the `VARIAB` key of an output group header file.

 Dependent variables may be one-dimensional (1D) or two-dimensional (2D).

- The value of a one-dimensional variable is determined by one independent variable, known as the _primary_ independent variable.

  Example: in a time series turbine simulation, 1D variable `Rotor speed` depends on primary independent variable `Time`. The data for `Rotor speed` is a one-dimensional array indexed on time.

- The value of a two-dimensional variable is determined by two independent variables, known as _primary_ and _secondary_ independent variables.

  Example: In a time series turbine simulation with a multi-member tower, 2D variable `Tower Mx` depends on primary independent variable `Time`, and secondary independent variable `Location`. The data for `Tower Mx` is a two-dimensional array indexed on member location and time.

### Independent variable

A variable whose value does not depend on other variables in the calculation. Independent variables are denoted by the `AXISLAB` key of an output group header file.

In a time series calculation, a _primary_ independent variable typically represents time. A _secondary_ independent variable typically represents an measurement point, such as a blade station.

### Header file

A file containing metadata describing an output group. A header files extension takes the form `.%n`, where `n` is a number uniquely identifying the group within the run.

### Data file

A file containing an output group’s data (binary or ASCII). A data file extension takes the form `.$n`, where `n` matches the corresponding header file number.

### (Output) group

A collection of variables that relate to a specific part of the model. For example, the variables `Rotor speed` and `Generator speed` belong to the `Drive train variables` group.

A Bladed group is represented by two files: a header file containing metadata, and a data file containing data for all dependent variables in the group.
