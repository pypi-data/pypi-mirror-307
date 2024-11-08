from dnv_bladed_results import *
from dnv_bladed_results import UsageExamples
import os

############   Bladed Results API: Exception handling   ############

# Demonstrates exception handling when getting runs, variables, and metadata
# Exception message should describe the problem in a concise form, including run/variable name and file path(s) as appropriate
# Exception messages come directly from the native C++ Calculation Results library


def run_script():
    r"""
    Example script that runs when this Python module is called as the main function.
    
    - Issues invalid requests to get runs, variables, groups, data, and stats.
    - Catches exception and writes exception message to the console.
    """
    
    exception_handling()

    # Clear the cache
    ResultsApi.clear_runs()


def exception_handling():

    #############
    #  Get run  #
    #############
    
    print("\n*** Demonstrating exception handling when getting runs ***")
    valid_run_directory = os.path.join(UsageExamples.__path__[0], "Runs/demo/powprod5MW")

    # Get a specific run using invalid directory
    try:
        run = ResultsApi.get_run("./non_existent_directory", "powprod5MW")
    except RuntimeError as e:
        print("\n", e)

    # Get a specific run using invalid name
    try:
        run = ResultsApi.get_run(valid_run_directory, "non-existent")
    except RuntimeError as e:
        print("\n", e)

    # Get runs using invalid directory
    try:
        run = ResultsApi.get_runs("./non_existent_directory")
    except RuntimeError as e:
        print("\n", e)

    # Get runs using invalid regex
    try:
        run = ResultsApi.get_runs_matching_name_regex(valid_run_directory, "[")
    except RuntimeError as e:
        print("\n", e)

    # Get a specific valid run
    run = ResultsApi.get_run(valid_run_directory, "powprod5MW")

    ##################
    #  Get variable  #
    ##################

    print("\n*** Demonstrating exception handling when getting variables ***")

    # Get a variable using invalid name
    try:
        var_1d = run.get_variable_1d("non-existent variable")
    except RuntimeError as e:
        print("\n", e)

    # Get a variable with incorrect dimensions
    try:
        var_1d = run.get_variable_1d("Tower Mx")
    except RuntimeError as e:
        print("\n", e)

    # Get variable using valid name
    var_2d: Variable2D_Float32
    var_2d = run.get_variable_2d("Tower Mx")

    ##############################
    #  Get independent variable  #
    ##############################

    print("\n*** Demonstrating exception handling when getting independent variables ***")
    ind_var: IndependentVariable

    # Get independent variable using invalid name
    try:
        ind_var = var_2d.get_independent_variable("invalid independent variable name")
    except RuntimeError as e:
        print("\n", e)

    # Get independent variable using identifier
    ind_var = var_2d.get_independent_variable(INDEPENDENT_VARIABLE_ID_SECONDARY)
    
    # Get the independent variable values
    secondary_independent_variable_values = ind_var.get_values_as_string()

    ##############
    #  Get data  #
    ##############

    print("\n*** Demonstrating exception handling when getting data ***")

    # Get data using invalid secondary independent variable value
    try:
        variable_data = var_2d.get_data_at_value("invalid secondary independent variable value")
    except RuntimeError as e:
        print("\n", e)

    # Get data using valid value
    variable_data = var_2d.get_data_at_value(secondary_independent_variable_values[0])

    ####################
    #  Get statistics  #
    ####################

    print("\n*** Demonstrating exception handling when getting statistics ***")

    # Get mean value using invalid independent variable value
    try:
        mean = var_2d.get_mean_at_value("invalid secondary independent variable value")
    except RuntimeError as e:
        print("\n", e)

    # Get mean value using valid independent variable value 
    mean = var_2d.get_mean_at_value(secondary_independent_variable_values[0])

    # Get contemporaneous maximum value using invalid variable value name
    try:
        mean = var_2d.get_maximum_contemporaneous_at_value("invalid variable name", secondary_independent_variable_values[0])
    except RuntimeError as e:
        print("\n", e)

    # Get contemporaneous maximum value using invalid independent variable value
    try:
        mean = var_2d.get_maximum_contemporaneous_at_value("Tower My", "invalid secondary independent variable value")
    except RuntimeError as e:
        print("\n", e)

    # Get contemporaneous maximum value using valid independent variable value 
    contemporaneous_mean = var_2d.get_maximum_contemporaneous_at_value("Tower My", secondary_independent_variable_values[0])

    ###############
    #  Get group  #
    ###############

    print("\n*** Demonstrating exception handling when getting group ***")

    # Get group using invalid name
    try:
        group = run.get_group("invalid group name")
    except RuntimeError as e:
        print("\n", e)

    # Get group using valid name
    group = run.get_group("blade 1 loads: principal axes")
    print("\n")


if __name__ == "__main__":
    run_script()
