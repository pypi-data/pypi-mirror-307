"""
This module provides utilities for preprocessing data, inspecting utilities, setting up data 
and variables for model building, and configuring models for discrete choice analysis 
using Biogeme. It integrates functionalities from Pandas, PySpark, Numpy, and Biogeme 
to facilitate the creation, manipulation, and analysis of choice models.

The functions include data feature engineering, utility inspection, data preparation for modeling, 
model retrieval and setup based on MLflow runs, and dynamic creation of Biogeme model variables 
and expressions. These utilities are designed to work with transportation datasets and 
choice modeling scenarios but can be adapted for other use cases.
"""


import os
import numpy as np
import biogeme.database as db
import biogeme.results as res
from pyspark.sql.window import Window
from pyspark.sql import functions as F
from biogeme.expressions import Beta, exp, Numeric


def format_expression(expr):
    """
    Formats a Biogeme expression by splitting it into multiple lines for better readability.

    Parameters:
    - expr: The Biogeme expression to format.

    Returns:
    - A string with the formatted expression, where each term is separated onto a new line.
    """
    parts = str(expr).split(" + ")
    return "\n".join(parts)


def inspect_the_utilities(v):
    """
    Prints the utilities and their associated expressions in a readable format.

    Parameters:
    - v: A dictionary where keys are alternatives and values are Biogeme expressions
    representing the utility of each alternative.
    """
    for key, value in v.items():
        print(f"Key {key}:\n{format_expression(value)}\n")


def feature_eng(data, no_alternatives, wa=True):
    """
    Performs feature engineering on the input dataset by creating new columns based on
    existing ones.

    Parameters:
    - data: A PySpark DataFrame containing the original dataset.

    Returns:
    - A PySpark DataFrame with additional columns resulting from feature engineering.
    """
    lower_bound = 0 if wa else 1
    for i in range(lower_bound, no_alternatives + 1):
        data = data.withColumn(
            f"number_of_stops_{i}",
            F.greatest(F.col(f"schedule_number_of_legs_{i}") - 1, F.lit(0)),
        )

        data = data.withColumn(
            f"journey_time_per_leg_{i}",
            F.when(F.col(f"schedule_number_of_legs_{i}") == 0, F.lit(0)).otherwise(
                (
                    F.col(f"schedule_journey_time_{i}")
                    / F.col(f"schedule_number_of_legs_{i}")
                )
                - 1
            ),
        )

        data = data.withColumn(
            f"flight_time_{i}",
            F.col(f"schedule_journey_time_{i}") - F.col(f"schedule_transfer_time_{i}"),
        )

    return data


def columns_factory(data, no_alternatives, wa=True):
    """
    Prepares the dataset for modeling by applying feature engineering and selecting
    relevant columns.

    Parameters:
    - data: A PySpark DataFrame containing the original dataset.
    - no_alternatives: The number of alternatives in the choice model.

    Returns:
    - A tuple containing the transformed PySpark DataFrame and a list of filtered origin variables.
    """

    if wa:
        lower_bound = 0
    else:
        lower_bound = 1

    data = feature_eng(data, no_alternatives=no_alternatives, wa=wa)
    orgs = [
        "_".join(o.split("_")[:-1])
        for o in data.columns
        if o.startswith("rq_dep_airport_code")
    ]
    orgs_filtered = list(
        {
            o
            for o in orgs
            if o
            not in (
                "rq_dep_airport_code",
                "rq_dep_airport_code_coded",
                "rq_dep_airport_code_Others",
            )
            and not o.endswith("rq_dep_airport_code")
        }
    )
    features = [
        "av",
        "choice",
        "price",
        "Dep_2pi_cos",
        "Dep_2pi_sin",
        "Dep_4pi_cos",
        "Dep_4pi_sin",
        "Dep_6pi_cos",
        "Dep_6pi_sin",
        "schedule_number_of_legs",
        "schedule_journey_time",
        "number_of_ods",
        "saturday_night",
        "round_trip",
        "trip_duration",
        "schedule_transfer_time",
        "schedule_distance",
        "pax_count",
        "schedule_departure_DOW_coded",
        "ndo",
        "number_of_stops",
        "journey_time_per_leg",
        "flight_time",
    ]
    features.extend(orgs_filtered)
    cols_f = [
        f"{f}_{i}" for i in range(lower_bound, no_alternatives + 1) for f in features
    ]
    cols = ["chosenAlternative", "chid", "uuid"] + cols_f
    return data.select(*cols), orgs_filtered


def feature_eng_long(data, no_alternatives, wa):
    # Define the logic to add an alternative based on the condition
    if wa:
        # Use a window to identify rows with alt = 1 within each chid group
        windowSpec = Window.partitionBy("chid")

        # Create a DataFrame that identifies where alt = 1
        alt_one_df = data.filter(F.col("alt") == 1)

        # Create new rows where alt is set to 0, copying other columns
        new_rows = alt_one_df.withColumn("alt", F.lit(0))

        # Combine the original data with the new rows
        result_df = data.unionByName(new_rows)

        return result_df
    else:
        return data


def columns_factory_long(data, no_alternatives, wa=True):
    """
    Prepares the dataset for modeling by applying feature engineering and selecting
    relevant columns.

    Parameters:
    - data: A PySpark DataFrame containing the original dataset.
    - no_alternatives: The number of alternatives in the choice model.

    Returns:
    - A tuple containing the transformed PySpark DataFrame and a list of filtered origin variables.
    """

    data = feature_eng_long(data=data, no_alternatives=no_alternatives, wa=wa)
    data = data.withColumn(
        "number_of_stops", F.greatest(F.col("schedule_number_of_legs") - 1, F.lit(0))
    )
    data = data.withColumn(
        "journey_time_per_leg",
        F.when(F.col("schedule_number_of_legs") == 0, F.lit(0)).otherwise(
            (F.col("schedule_journey_time") / F.col("schedule_number_of_legs")) - 1
        ),
    )

    data = data.withColumn(
        "flight_time",
        F.col("schedule_journey_time") - F.col("schedule_transfer_time"),
    )

    return data


def prepare_data(data, desired_rows=100000, no_alternatives=10, as_requested=False):
    """
    Samples and prepares data for modeling, adjusting the row count to a desired number.

    Parameters:
    - data (DataFrame): A PySpark DataFrame to be prepared.
    - desired_rows (int, optional): The target number of rows for the sample. Defaults to 100000.
    - no_alternatives (int, optional): The number of alternatives in the choice model.
    Defaults to 10.
    - as_requested (bool, optional): Flag to indicate whether to sample
    as requested without adjustments. Defaults to False.

    Returns:
    - tuple: A tuple containing a Pandas DataFrame of the sampled data and
    a list of filtered origin variables.
    """

    data, orgs_filtered = columns_factory(data, no_alternatives=no_alternatives)

    if as_requested:
        sampled_data = data
    else:
        if desired_rows == 1:
            sampled_data = data.limit(1)
        else:
            total_rows = data.count()
            fraction = desired_rows / float(total_rows)
            sampled_data = data.sample(withReplacement=False, fraction=fraction)
            if sampled_data.count() > desired_rows:
                sampled_data = sampled_data.limit(desired_rows)
    return sampled_data.toPandas(), orgs_filtered


def get_the_model(
    run_name, local_dir, data, rows, no_alternatives=10, as_requested=False
):
    """
    Retrieves a model from MLflow, prepares the data, and sets up the
    Biogeme database for modeling.

    Parameters:
    - run_name (str): The name of the MLflow run.
    - local_dir (str): The local directory to save artifacts.
    - data (DataFrame): The dataset to use for modeling.
    - rows (int): The number of rows to sample for modeling.
    - no_alternatives (int, optional): The number of alternatives in the choice model.
    Defaults to 10.
    - as_requested (bool, optional): Flag to sample data as requested without adjustments.
    Defaults to False.

    Returns:
    - tuple: A tuple containing the final dataset in a Pandas DataFrame,
    the Biogeme database object, beta values from the model, and a l
    ist of filtered origin variables.
    """
    # Model
    if not os.path.exists(local_dir):
        os.mkdir(local_dir)
    # Betas
    results = res.bioResults(pickleFile=f"{run_name}.pickle")
    beta_values = results.getBetaValues()
    # Get the data
    final_dataset, orgs_filtered = prepare_data(
        data,
        desired_rows=rows,
        no_alternatives=no_alternatives,
        as_requested=as_requested,
    )
    # Biogeme database
    database = db.Database(f"dataset/{run_name}", final_dataset)
    return final_dataset, database, beta_values, orgs_filtered


def setup_data_and_variables(
    run_name, local_dir, data, rows, no_alternatives=10, as_requested=False
):
    """
    Set up the data and variables for the model.

    Parameters:
    - run_name (str): The name of the run.
    - local_dir (str): The local directory path.
    - data (str): The data source.
    - rows (int): The number of rows.
    - no_alternatives (int, optional): The number of alternatives. Defaults to 10.
    - as_requested (bool, optional): Whether the data is requested or not. Defaults to False.

    Returns:
    - dataset_in_pandas (pandas.DataFrame): The dataset in pandas DataFrame format.
    - biogeme_database (str): The biogeme database.
    - betas (str): The betas.
    - orgs_filtered (str): The filtered organizations.
    """

    dataset_in_pandas, biogeme_database, betas, orgs_filtered = get_the_model(
        run_name=run_name,
        local_dir=local_dir,
        data=data,
        rows=rows,
        no_alternatives=no_alternatives,
        as_requested=as_requested,
    )

    return dataset_in_pandas, biogeme_database, betas, orgs_filtered


def setup_parameters_and_availability(
    globals_dict,
    orgs_filtered,
    betas=None,
    fix_betas=False,
    no_alternatives=10,
    asc_nobuy=None,
    wa=True,
):
    """
    Set up parameters and availability for flight scenario optimization.

    Args:
        globals_dict (dict): A dictionary containing global variables.
        orgs_filtered (list): A list of filtered OD.
        betas (dict, optional): A dictionary of beta values. Defaults to None.
        fix_betas (bool, optional): Whether to fix the beta values. Defaults to False.
        no_alternatives (int, optional): The number of alternatives. Defaults to 10.
        asc_nobuy (float, optional): The ASC_NOBUY value. Defaults to None.
        wa (bool, optional): Whether to use a lower bound of 0 for availability. Defaults to True.

    Returns:
        tuple: A tuple containing the updated globals_dict and availability dictionary.
    """

    # All parameters
    linear = [
        "price",
        "Dep_2pi_cos",
        "Dep_2pi_sin",
        "Dep_4pi_cos",
        "Dep_4pi_sin",
        "Dep_6pi_cos",
        "Dep_6pi_sin",
        "schedule_number_of_legs",
        "schedule_journey_time",
        "trip_duration",
        "schedule_transfer_time",
        "schedule_distance",
        "number_of_stops",
        "journey_time_per_leg",
        "schedule_transfer_time",
        "flight_time",
        "ndo",
        "pax_count",
    ]
    interactions = [
        "price",
        "ndo",
        "number_of_ods",
        "saturday_night",
        "round_trip",
        "pax_count",
        "schedule_departure_DOW_coded",
        "schedule_number_of_legs",
        "schedule_journey_time",
        "number_of_stops",
        "journey_time_per_leg",
        "schedule_transfer_time",
        "trip_duration",
        "flight_time",
        "Dep_2pi_cos",
        "Dep_2pi_sin",
        "Dep_4pi_cos",
        "Dep_4pi_sin",
        "Dep_6pi_cos",
        "Dep_6pi_sin",
        "pax_count",
    ]
    interactions.extend(orgs_filtered)

    if fix_betas:
        if wa:
            # Calibrate it
            betas["ASC_NOBUY"] = asc_nobuy

            globals_dict["ASC_NOBUY"] = Beta("ASC_NOBUY", asc_nobuy, None, None, 0)
            globals_dict["ASC_CHOSEN"] = Beta("ASC_CHOSEN", 0, None, None, 1)

        for col in linear:
            if f"B_{col}" in betas.keys():
                v = betas[f"B_{col}"]
                globals_dict[f"B_{col}"] = Beta(f"B_{col}", v, None, None, 1)
            else:
                globals_dict[f"B_{col}"] = Beta(f"B_{col}", 0, None, None, 1)
        # Add the interaction terms

        for j, feature1 in enumerate(interactions):
            # Start from j + 1
            for _, feature2 in enumerate(interactions[j + 1 :]):
                if feature1 == "price" and feature2 in interactions:
                    beta_key = f"B_I_{feature1}_{feature2}"
                    if beta_key in betas.keys():
                        v = betas[beta_key]
                    else:
                        v = 0  # Default value
                    globals_dict[beta_key] = Beta(
                        beta_key, v, None, None, 1
                    )  # Add the interaction term

    else:
        if wa:
            globals_dict["ASC_NOBUY"] = Beta("ASC_NOBUY", asc_nobuy, None, None, 0)
            globals_dict["ASC_CHOSEN"] = Beta("ASC_CHOSEN", 0, None, None, 1)

        for col in linear:
            globals_dict[f"B_{col}"] = Beta(f"B_{col}", 0, None, None, 0)

        for j, feature1 in enumerate(interactions):
            for _, feature2 in enumerate(interactions[j + 1 :]):
                if feature1 == "price" and feature2 in interactions:
                    globals_dict[f"B_I_{feature1}_{feature2}"] = Beta(
                        f"B_I_{feature1}_{feature2}", 0, None, None, 0
                    )
    # Availability

    if wa:
        av = {i: globals_dict[f"av_{i}"] for i in range(0, no_alternatives + 1)}
    else:
        av = {i: globals_dict[f"av_{i}"] for i in range(1, no_alternatives + 1)}

    return globals_dict, av


def define_the_model(
    globals_dict, linear_terms, interaction_terms, no_alternatives, wa=True
):
    """
    Defines the model based on the given parameters.

    Args:
        fix_betas (bool): Indicates whether the betas should be fixed.
        globals_dict (dict): A dictionary containing global variables.
        linear_terms (list): A list of linear terms.
        interaction_terms (list): A list of interaction terms.
        no_alternatives (int): The number of alternatives.
        wa (bool, optional): Indicates whether the model should use the weighted average.
        Defaults to True.

    Returns:
        dict: A dictionary containing the defined model.

    """
    v = {}

    if wa:
        v = {0: globals_dict["ASC_NOBUY"]}
        for i in range(1, no_alternatives + 1):
            expression = globals_dict["ASC_CHOSEN"]
            # Add the main terms
            for feature in linear_terms:
                coefficient = globals_dict[f"B_{feature}"]
                variable = globals_dict[f"{feature}_{i}"]
                expression += coefficient * variable
            # Add the interaction terms
            for j, feature1 in enumerate(interaction_terms):
                for _, feature2 in enumerate(interaction_terms[j + 1 :]):
                    if feature1 == "price" and feature2 in interaction_terms:
                        interaction_coefficient = globals_dict[
                            f"B_I_{feature1}_{feature2}"
                        ]
                        variable1 = globals_dict[f"{feature1}_{i}"]
                        expression += interaction_coefficient * variable1 * variable
            # Assign the constructed expression to the dictionary
            v[i] = expression
    else:
        for i in range(1, no_alternatives + 1):
            # Add the main terms
            # just init expression
            feature = linear_terms[0]
            coefficient = globals_dict[f"B_{feature}"]
            variable = globals_dict[f"{feature}_{i}"]
            expression = coefficient * variable
            # continue
            for feature in linear_terms[1:]:
                coefficient = globals_dict[f"B_{feature}"]
                variable = globals_dict[f"{feature}_{i}"]
                expression += coefficient * variable
            # Add the interaction terms
            for j, feature1 in enumerate(interaction_terms):
                for _, feature2 in enumerate(interaction_terms[j + 1 :]):
                    if feature1 == "price" and feature2 in interaction_terms:
                        interaction_coefficient = globals_dict[
                            f"B_I_{feature1}_{feature2}"
                        ]
                        variable1 = globals_dict[f"{feature1}_{i}"]
                        expression += interaction_coefficient * variable1 * variable
            # Assign the constructed expression to the dictionary
            v[i] = expression

    return v


def setup_model(
    globals_dict,
    orgs_filtered,
    betas,
    fix_betas,
    no_alternatives,
    linear_terms,
    interaction_terms,
    asc_nobuy,
):
    """
    Configures and calibrates the choice model by defining utility functions and availability
    for each alternative.

    Parameters:
    - globals_dict: A dictionary to store global variables dynamically created during model setup.
    - orgs_filtered: A list of origin variables filtered from the dataset.
    - betas: A dictionary of beta values for model parameters.
    - fix_betas: A boolean indicating whether to fix the beta values to those provided
    or estimate them.
    - no_alternatives: The number of alternatives in the choice model.
    - linear_terms: A list of variables to be included as linear terms in the utility functions.
    - interaction_terms: A list of variables to be considered for interaction terms
    in the utility functions.
    - asc_nobuy: The alternative-specific constant for the "no buy" option.

    Returns:
    - A tuple containing a dictionary of availability indicators for each alternative and
    a dictionary of utility functions for each alternative.
    """

    globals_dict, av = setup_parameters_and_availability(
        globals_dict=globals_dict,
        orgs_filtered=orgs_filtered,
        betas=betas,
        fix_betas=fix_betas,
        no_alternatives=no_alternatives,
        asc_nobuy=asc_nobuy,
    )

    v = define_the_model(
        fix_betas=fix_betas,
        globals_dict=globals_dict,
        linear_terms=linear_terms,
        interaction_terms=interaction_terms,
        no_alternatives=no_alternatives,
    )

    # Set the costs (need to get form data)
    cost = np.full(no_alternatives + 1, 0.0)

    beta_price_with_interactions = {}

    for r in range(no_alternatives + 1):
        beta_price_with_interactions[r] = globals_dict["B_price"]

        for j, feature1 in enumerate(interaction_terms):
            for k, feature2 in enumerate(interaction_terms[j + 1 :]):
                if feature1 == "price" and feature2 in interaction_terms:
                    interaction_coefficient = globals_dict[f"B_I_{feature1}_{feature2}"]
                    variable2 = globals_dict[f"{feature2}_{r}"]
                    beta_price_with_interactions[r] += (
                        interaction_coefficient * variable2 * av[r]
                    )

    option_quality = {}
    for r in range(no_alternatives + 1):
        option_quality[r] = 0.0
        for feature in linear_terms:
            if feature != "price":
                coefficient = globals_dict[f"B_{feature}"]
                variable = globals_dict[f"{feature}_{r}"]
                option_quality[r] += coefficient * variable * av[r]

    c1 = {}
    for r in range(no_alternatives + 1):
        c1[r] = 0.0
        saux = 0.0
        for i in range(no_alternatives + 1):
            if i != r:
                price = globals_dict[f"price_{i}"]
                saux += (price - cost[i]) * exp(v[i])
        c1[r] += (
            (saux)
            / (exp(option_quality[r] - beta_price_with_interactions[r] * cost[r]))
        ) * av[r]

    c2 = {}
    for r in range(no_alternatives + 1):
        c2[r] = 0.0
        saux = 0.0
        for k in range(1, no_alternatives + 1):
            if k != r:
                saux += exp(v[k]) * av[r]
        c2[r] += (
            (exp(v[0]) + saux)
            / (exp(option_quality[r] - beta_price_with_interactions[r] * cost[r]))
        ) * av[r]

    w = {}
    for r in range(no_alternatives + 1):
        w[r] = (
            exp(-(beta_price_with_interactions[r] * c1[r]) / c2[r] - 1.0) / c2[r]
        ) * av[r]

    return av, v, beta_price_with_interactions, option_quality, c1, c2, w


def setup_model_v2(
    globals_dict,
    orgs_filtered,
    betas,
    fix_betas,
    no_alternatives,
    linear_terms,
    interaction_terms,
    asc_nobuy,
):
    """
    Configures and calibrates the choice model by defining utility functions
    and availability for each alternative.

    Parameters:
    - globals_dict: A dictionary to store global variables dynamically created during model setup.
    - orgs_filtered: A list of origin variables filtered from the dataset.
    - betas: A dictionary of beta values for model parameters.
    - fix_betas: A boolean indicating whether to fix the beta values to those provided
    or estimate them.
    - no_alternatives: The number of alternatives in the choice model.
    - linear_terms: A list of variables to be included as linear terms in the utility functions.
    - interaction_terms: A list of variables to be considered for interaction
    terms in the utility functions.
    - asc_nobuy: The alternative-specific constant for the "no buy" option.

    Returns:
    - A tuple containing a dictionary of availability indicators for each alternative
    and a dictionary of utility functions for each alternative.
    """

    globals_dict, av = setup_parameters_and_availability(
        globals_dict=globals_dict,
        orgs_filtered=orgs_filtered,
        betas=betas,
        fix_betas=fix_betas,
        no_alternatives=no_alternatives,
        asc_nobuy=asc_nobuy,
    )

    v = define_the_model(
        fix_betas=fix_betas,
        globals_dict=globals_dict,
        linear_terms=linear_terms,
        interaction_terms=interaction_terms,
        no_alternatives=no_alternatives,
    )

    # Set the costs (need to get form data)
    cost = np.full(no_alternatives + 1, 0.0)

    b = globals_dict["B_price"]

    option_quality = {}
    for r in range(no_alternatives + 1):
        option_quality[r] = 0.0
        for feature in linear_terms:
            if feature != "price":
                coefficient = globals_dict[f"B_{feature}"]
                variable = globals_dict[f"{feature}_{r}"]
                option_quality[r] += coefficient * variable

    a = {}
    for k in range(1, no_alternatives + 1):
        a[k] = 0.0
        for feature in linear_terms:
            if feature != "price":
                coefficient = globals_dict[f"B_{feature}"]
                variable = globals_dict[f"{feature}_{k}"]
                a[k] += coefficient * variable

    w = 0.0
    for k in range(1, no_alternatives + 1):
        w += exp(a[k] - b * cost[k] - 1.0)

    w = 0.0
    c1 = 0.0
    a = {}
    # Set the costs (need to get form data)
    c = np.full(no_alternatives + 1, 0.0)

    # Loop to create each entry in the dictionary
    for k in range(no_alternatives + 1):
        # Starting expression
        expression = globals_dict["ASC_CHOSEN"] if k > 0 else globals_dict["ASC_NOBUY"]
        expression3 = globals_dict["ASC_CHOSEN"]

        # Add the main terms
        for feature in linear_terms:
            coefficient = globals_dict[f"B_{feature}"]
            variable = globals_dict[f"{feature}_{k}"]
            expression += coefficient * variable
            if feature != "price":
                expression3 += coefficient * variable

        # Assign the constructed expression to the dictionary
        v[k] = expression
        w = exp(expression3 - b * c[k] - 1)
        c1 = exp(expression3 - b * c[k])
        a[k] = exp(expression3 - b[k] * c[k])

    return av, v, w, c1, a


def calculate_terms(
    globals_dict,
    v,
    av,
    betas,
    no_alternatives,
    linear_terms,
    interaction_terms,
    asc_nobuy,
    cost,
):
    """
    Configures and calibrates the choice model by defining utility functions and availability
    for each alternative.

    Parameters:
    - globals_dict: A dictionary to store global variables dynamically created during model setup.
    - orgs_filtered: A list of origin variables filtered from the dataset.
    - betas: A dictionary of beta values for model parameters.
    - fix_betas: A boolean indicating whether to fix the beta values to those provided
    or estimate them.
    - no_alternatives: The number of alternatives in the choice model.
    - linear_terms: A list of variables to be included as linear terms in the utility functions.
    - interaction_terms: A list of variables to be considered for interaction terms
    in the utility functions.
    - asc_nobuy: The alternative-specific constant for the "no buy" option.

    Returns:
    - A tuple containing a dictionary of availability indicators for each alternative and
    a dictionary of utility functions for each alternative.
    """

    beta_price_with_interactions = {}

    for r in range(no_alternatives + 1):
        beta_price_with_interactions[r] = globals_dict["B_price"]

        for j, feature1 in enumerate(interaction_terms):
            for k, feature2 in enumerate(interaction_terms[j + 1 :]):
                if feature1 == "price" and feature2 in interaction_terms:
                    interaction_coefficient = globals_dict[f"B_I_{feature1}_{feature2}"]
                    variable2 = globals_dict[f"{feature2}_{r}"]
                    beta_price_with_interactions[r] += (
                        interaction_coefficient * variable2 * av[r]
                    )

    option_quality = {}
    for r in range(no_alternatives + 1):
        option_quality[r] = 0.0
        for feature in linear_terms:
            if feature != "price":
                coefficient = globals_dict[f"B_{feature}"]
                variable = globals_dict[f"{feature}_{r}"]
                option_quality[r] += coefficient * variable * av[r]

    c1 = {}
    for r in range(no_alternatives + 1):
        c1[r] = 0.0
        saux = 0.0
        for i in range(no_alternatives + 1):
            if i != r:
                price = globals_dict[f"price_{i}"]
                saux += (price - cost[i]) * exp(v[i])
        c1[r] += (
            (saux)
            / (exp(option_quality[r] - beta_price_with_interactions[r] * cost[r]))
        ) * av[r]

    c2 = {}
    for r in range(no_alternatives + 1):
        c2[r] = 0.0
        saux = 0.0
        for k in range(1, no_alternatives + 1):
            if k != r:
                saux += exp(v[k]) * av[r]
        c2[r] += (
            (exp(v[0]) + saux)
            / (exp(option_quality[r] - beta_price_with_interactions[r] * cost[r]))
        ) * av[r]

    w = {}
    for r in range(no_alternatives + 1):
        w[r] = (
            exp(-(beta_price_with_interactions[r] * c1[r]) / c2[r] - 1.0) / c2[r]
        ) * av[r]

    return beta_price_with_interactions, option_quality, c1, c2, w