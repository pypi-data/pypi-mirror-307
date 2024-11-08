"""
A module for performing ranking and normalization operations on predictive data.

This module provides functions to calculate and append normalized count metrics
to a pandas DataFrame, based on ranking conditions related to fare level probabilities.
These functions are particularly useful for analyzing and comparing the predicted
probabilities of different fare levels within transportation or revenue management systems.

Functions:
- top_n: Calculate a normalized count for each fare level based on a threshold rank.
- top_n_no_wa: Calculate a normalized count for fare levels excluding 'walk-away' (level 0) based on a threshold rank.
"""

import numpy as np
import pandas as pd

def top_n(data_predict, n, no_alternatives=10, no_records=0):
    """
    Append a column to the DataFrame that represents the normalized count of 
    each fare level being the chosen alternative and having a probability rank 
    within the top `n` ranks.

    The normalization is performed over all rows in the DataFrame.

    Parameters:
    - data_predict (pd.DataFrame): The input DataFrame with fare level probabilities and ranks.
    - n (int): The threshold rank value for counting the top ranks.

    Returns:
    pd.DataFrame: The DataFrame with an appended column named 'top_{n}' reflecting
                  the normalized count for each fare level.

    Raises:
    - ValueError: If `data_predict` is not a pandas DataFrame, `n` is not an integer,
                  the DataFrame is empty, `n` is negative, or the required columns
                  are not present in the DataFrame.
    """

    # Basic input validations
    if not isinstance(data_predict, pd.DataFrame) or not isinstance(n, int):
        raise ValueError("Input parameters are not of the expected type.")


    required_cols = ["chosenAlternative"] + \
        [f"prob_fare_level_{i}_rank" for i in range(1, no_alternatives + 1)]
    if not all(col in data_predict.columns for col in required_cols):
        raise ValueError(
            "Required columns are not present in the input DataFrame.")

    # Ensure the DataFrame is non-empty and `n` is non-negative
    if data_predict.shape[0] == 0:
        raise ValueError("Input DataFrame should not be empty.")
    if n < 0:
        raise ValueError("Parameter n should be a non-negative integer.")

    # Initialize the new column
    data_predict[f"top_{n}"] = 0

    # Calculating and normalizing the count
    for level in range(1, no_alternatives + 1):  # Assuming there are 11 levels (0 through 10)
        condition = (data_predict["chosenAlternative"] == level) & (
            data_predict[f"prob_fare_level_{level}_rank"] <= n)
        count = data_predict.loc[condition].shape[0]
        data_predict[f"top_{n}"] += count

    # Normalizing the new column by the total count of non-walk-away alternatives
    data_predict[f"top_{n}"] /= no_records

    return data_predict


def top_n_no_wa(data_predict, n):
    """
    Append a column to the DataFrame that represents the normalized count of 
    each fare level, excluding the 'walk-away' option (level 0), being the 
    chosen alternative and having a probability rank within the top `n` ranks.

    The normalization is performed only over rows where the chosen alternative 
    is not the 'walk-away' option.

    Parameters:
    - data_predict (pd.DataFrame): The input DataFrame with fare level probabilities and ranks.
    - n (int): The threshold rank value for counting the top ranks, excluding 'walk-away'.

    Returns:
    pd.DataFrame: The DataFrame with an appended column named 'top_{n}_no_wa' reflecting
                  the normalized count for each fare level, excluding 'walk-away'.

    Raises:
    - ValueError: If `data_predict` is not a pandas DataFrame, `n` is not an integer,
                  the DataFrame is empty, `n` is negative, or the required columns
                  are not present in the DataFrame.
    """

    # Basic input validations
    if not isinstance(data_predict, pd.DataFrame) or not isinstance(n, int):
        raise ValueError("Input parameters are not of the expected type.")

    # Ensure required columns are present in the DataFrame
    required_cols = ["chosenAlternative"] + \
        [f"prob_no_wa_{i}_rank" for i in range(1, 11)]
    if not all(col in data_predict.columns for col in required_cols):
        raise ValueError(
            "Required columns are not present in the input DataFrame.")

    # Ensure the DataFrame is non-empty and `n` is non-negative
    if data_predict.shape[0] == 0:
        raise ValueError("Input DataFrame should not be empty.")
    if n < 0:
        raise ValueError("Parameter n should be a non-negative integer.")

    # Initialize the new column
    data_predict[f"top_{n}_no_wa"] = 0

    # Calculating and normalizing the count
    for level in range(1, 11):  # Assuming there are 11 levels (0 through 10)
        condition = (data_predict["chosenAlternative"] == level) & (
            data_predict[f"prob_no_wa_{level}_rank"] <= n)
        count = data_predict.loc[condition].shape[0]
        data_predict[f"top_{n}_no_wa"] += count

    # Normalizing the new column
    count_rows = len(data_predict[data_predict.chosenAlternative > 0])
    data_predict[f"top_{n}_no_wa"] /= count_rows

    return data_predict






















