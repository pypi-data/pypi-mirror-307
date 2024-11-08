from dnv_bladed_results import *
from dnv_bladed_results import UsageExamples
import os

############   Bladed Results API: Get output group metadata   ############

# Demonstrates how to read metadata from output groups.


def run_script():
    r"""
    Example script that runs when this Python module is called as the main function.
    
    For all groups in a run:

    - Prints group metadata to the console.
    - Prints information about dependent and independent variables to the console.
    """
    
    run_directory = os.path.join(UsageExamples.__path__[0], "Runs/demo/powprod5MW")
    run_name = "powprod5MW"
    display_group_metadata(run_directory, run_name)

    # Clear the cache
    ResultsApi.clear_runs()


def display_group_metadata(run_directory, run_name):
    
    try:
        
        ################################
        #  Get a specific run by name  #
        ################################

        run = ResultsApi.get_run(run_directory, run_name)

        ##########################
        #  Get a specific Group  #
        ##########################

        group = run.get_group("support structure accelerations")
        print("\n#####   Group name: " + group.get_name() + "   #####")
        print("Calculation name: " + group.get_calculation_short_name() + " (" + group.get_calculation_descriptive_name() + ")")

        ####################
        #  Get all groups  #
        ####################

        print("Displaying metadata for run '" + run.get_name() + "'")
        all_groups = run.get_groups()
        print("Run has " + str(all_groups.size) + " output groups")

        # Sort by group number
        all_groups = sorted(all_groups, key=lambda o: o.get_number())
        
        # Iterate group collection
        group: Group
        for group in all_groups:
            
            print("\n#####   Group name: " + group.get_name() + "   #####")
            print("\n  Group number: " + str(group.get_number()))
            
            #########################################
            #  Display some basic calculation info  #
            #########################################

            print("  Calculation name: " + group.get_calculation_short_name() + " (" + group.get_calculation_descriptive_name() + ")")
            print("  Group has " + str(group.get_data_point_count()) + " data points per series")
            
            # Full enumeration of calculation types available via CalculationType:
            calc_type = group.get_calculation_type()
            if calc_type == CALCULATION_TYPE_POWER_PRODUCTION_SIMULATION:
                pass
            elif calc_type == CALCULATION_TYPE_PARKED_SIMULATION:
                pass

            ####################################################
            #  Get independent variables and display metadata  #
            ####################################################

            # Print independent variable info (a group always has either 1 or 2 independent variables)
            print("  Group has " + str(group.get_number_of_independent_variables()) + " independent variables:")
            primary_independent_var = group.get_independent_variable(INDEPENDENT_VARIABLE_ID_PRIMARY)
            print("  - Primary independent variable name: " + primary_independent_var.get_name() + ";\tSI unit: " + primary_independent_var.get_siunit())
            if group.get_number_of_independent_variables() == 2:
                secondary_independent_var = group.get_independent_variable(INDEPENDENT_VARIABLE_ID_SECONDARY)
                print("  - Secondary independent variable name: " + secondary_independent_var.get_name() + ";\tSI unit: " + secondary_independent_var.get_siunit())

            ##################################################
            #  Get dependent variables and display metadata  #
            ##################################################

            if group.get_number_of_independent_variables() == 1:
                all_dependent_vars = group.get_variables_1d()
            else:
                all_dependent_vars = group.get_variables_2d()

            # Print dependent variable info
            print("  Group has " + str(group.get_number_of_variables()) + " dependent variables:")
            dependent_var: Variable
            for dependent_var in all_dependent_vars:
                print("  - Dependent variable name: " + dependent_var.get_name() + ";\tSI unit: " + dependent_var.get_siunit())

        print()

    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    run_script()
