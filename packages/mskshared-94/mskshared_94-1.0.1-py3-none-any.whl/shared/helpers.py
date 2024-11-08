"""
Biogeme Simulation Module

This module provides functions to work with Biogeme - a Python package designed
for the maximum likelihood estimation of parametric models in general, with a
special emphasis on discrete choice models. It leverages Biogeme to simulate 
probabilities and revenues based on logistic models.

The module consists of helper functions to process data and simulate expected
revenues, actual revenues, and alternative-specific probabilities using logit
models. It assumes a global context where variables and availability indicators
are defined.

Functions:
    is_running_on_databricks(): Checks if the script is running on Databricks.
    extract_file_name_from_url(url): Extracts the file name from a given URL.
    get_last_nonzero_available(row, no_alternatives): Identifies the last non-zero availability
                                                      indicator in a row of a DataFrame.
    simulate_helper(V, av, no_alternatives, lower_limit): Simulates the probability
                                                          of choosing each fare level
                                                          using a logit model.
    actual_revenue_helper(data_predict, no_alternatives, lower_limit): Calculates
                                                                       the actual revenue
                                                                       based on choices
                                                                       and prices.
    expected_revenue_helper(data_predict, no_alternatives, lower_limit): Calculates
                                                                         the expected revenue
                                                                         based on simulated
                                                                         probabilities and
                                                                         prices.
    expected_revenue_helper_no_wa(data_predict): Calculates the expected revenue,
                                                 ignoring a specific scenario
                                                 (without availability).

Note:
    This module requires the global variables `V` (systematic utility) and `av`
    (availability indicators) to be defined before calling `simulate_helper`.
"""

import os
import pandas as pd
import biogeme.models as models


def cal_proba_i(cal_wa, uncal_wa, uncal_proba):
    return (1.0 - cal_wa) * (uncal_proba / (1.0 - uncal_wa))


def convert_to_base_name_dict(column_names):
    base_name_dict = {}
    for name in column_names:
        # Split the name on underscore and take all parts except the last as the base name
        base_name = "_".join(name.split("_")[:-1])
        base_name_dict[name] = base_name
    return base_name_dict


def is_running_on_databricks():
    """
    Determine if the Python script is running in a Databricks notebook environment.

    Returns:
        bool: True if running on Databricks, False otherwise.
    """
    return "DATABRICKS_RUNTIME_VERSION" in os.environ


def extract_file_name_from_url(url: str) -> str:
    """
    Extracts the file name from a given URL, excluding the file extension.

    Parameters:
        url (str): The URL from which the file name is to be extracted.

    Returns:
        str: The extracted file name without the extension.
    """
    path = os.path.normpath(url)
    base_name = os.path.basename(path)
    file_name, _ = os.path.splitext(base_name)
    return file_name


def get_last_nonzero_available(row, no_alternatives=10):
    """
    Identifies the last non-zero availability indicator from a series of columns in a DataFrame row.

    Parameters:
        row (pd.Series): The DataFrame row to check for availability.
        no_alternatives (int): The number of alternative availability indicators to check.

    Returns:
        int: The index of the last non-zero availability indicator, or 0 if all are zero.
    """
    for i in reversed(range(1, no_alternatives + 1)):
        if row[f"av_{i}"] != 0:
            return i
    return 0

def actual_revenue_helper(data_predict, no_alternatives=10):
    """
    Calculates actual revenue from a DataFrame of choices and prices.

    Parameters:
        data_predict (pd.DataFrame): The DataFrame containing choice indicators and
        prices for each alternative.
        no_alternatives (int): The total number of alternatives.
        lower_limit (int): The lower bound to start calculating from (inclusive).

    Returns:
        float: The total actual revenue calculated from the selected choices and
        their corresponding prices.
    """
    revenue = sum(
        data_predict[f"choice_{i}"] * data_predict[f"price_{i}"]
        for i in range(1, no_alternatives + 1)
    )
    return revenue.sum()


def expected_revenue_helper(data_predict, no_alternatives=10, lower_limit=0) -> float:
    """
    Calculates the expected revenue based on simulated probabilities of
    selection and the corresponding prices for each alternative.

    This function multiplies each alternative's probability by its price and sums
    these products to get the total expected revenue.

    Parameters:
        data_predict (pd.DataFrame): A DataFrame containing the columns for probabilities
        ('prob_fare_level_i') and prices ('price_i') for each alternative.
        no_alternatives (int, optional): The total number of alternatives considered.
        Defaults to 10.
        lower_limit (int, optional): The index of the first alternative to consider
        (1-based), allowing for exclusion of alternatives below a certain threshold. Defaults to 0.

    Returns:
        float: The total expected revenue calculated across all considered alternatives.
    """

    # Calculate and return the sum of products of probabilities and their corresponding
    # prices for the specified range of alternatives
    sum_products = sum(
        data_predict[f"prob_fare_level_{i}"] * data_predict[f"price_{i}"]
        for i in range(lower_limit, no_alternatives + 1)
    )
    return sum_products.sum()


def expected_revenue_helper_no_wa(
    data_predict: pd.DataFrame, no_alternatives: int = 10
) -> float:
    """
    Calculates the expected revenue excluding the walk-away scenario, if applicable.
    This is done by considering only the alternatives that represent actual choices
    (excluding the highest-indexed 'walk away' option).

    Parameters:
        data_predict (pd.DataFrame): A DataFrame containing the columns for probabilities
        ('prob_fare_level_i') and prices ('price_i') for each alternative, excluding
        the walk-away alternative.
        no_alternatives (int, optional): The total number of alternatives including the
        walk-away option. The function automatically excludes the walk-away alternative by
        adjusting the range. Defaults to 10.

    Returns:
        float: The total expected revenue calculated across all alternatives excluding the
        walk-away option.
    """

    # Calculate and return the sum of products of probabilities and their corresponding prices,
    # excluding the walk-away option
    sum_products = sum(
        data_predict[f"prob_fare_level_{i}"] * data_predict[f"price_{i}"]
        for i in range(1, no_alternatives + 1)
    )
    return sum_products.sum()