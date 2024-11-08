"""
This module provides functionality for validating and computing the total beta price
for a given set of alternatives using their associated beta values and interaction terms.
The calculations are based on the inputs provided from a specified database and utilize
PySpark for handling and processing the data.

The module includes:
- Spark session initialization for distributed data processing.
- A function to validate and compute the total beta price for each alternative.

The function processes the data using numpy for mathematical operations and PySpark
to construct and return a DataFrame that contains the final computed prices.

Functions:
    validate_total_beta_price(globals_dict, betas, database, interaction_terms, no_alternatives)

Example usage:
    # Define input parameters
    globals_dict = {
        'some_global_variable': some_value,
        ...
    }
    betas = {
        'B_price': 1.0,
        'B_I_price_feature1': 0.5,
        ...
    }
    database = 'your_database_name'
    interaction_terms = ['feature1', 'feature2']
    no_alternatives = 3

    # Compute total beta price
    total_beta_price_df = validate_total_beta_price(
        globals_dict, betas, database, interaction_terms, no_alternatives
    )

Dependencies:
    - numpy: For numerical operations.
    - pyspark: For creating and manipulating DataFrames.
"""

import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, StructField, FloatType

# Initialize Spark session
spark = SparkSession.builder.appName("validation").getOrCreate()


def validate_total_beta_price(globals_dict, betas, database, interaction_terms, no_alternatives):
    """
    Validates the total beta price for each alternative based on the given parameters.

    Args:
        globals_dict (dict): A dictionary containing global variables.
        betas (dict): A dictionary containing beta values for price and interaction terms.
        database (str): The name of the database from which values are fetched.
        interaction_terms (list): A list of interaction terms used in the beta price calculation.
        no_alternatives (int): The number of alternatives to compute prices for.

    Returns:
        DataFrame: A PySpark DataFrame containing the final total beta price for each alternative,
                   with columns for the offer and the computed price.
    """
    final_total_beta_price = {}

    for r in range(1, no_alternatives + 1):
        bprice = float(betas["B_price"])
        final_total_beta_price[r] = bprice
        for i in interaction_terms:
            if i != "price":
                coef = betas[f"B_I_price_{i}"]
                val = globals_dict[f"{i}_{r}"].getValue_c(
                    database=database, betas=betas, prepareIds=True
                )
                min_val = np.min(val)
                max_val = np.max(val)

                final_total_beta_price[r] += coef * float(max_val)

                if bprice > 0:
                    if coef < 0:
                        final_total_beta_price[r] += coef * float(min_val)
                elif bprice < 0:
                    if coef > 0:
                        final_total_beta_price[r] += coef * float(max_val)

    # Define the schema for the resulting DataFrame
    schema = StructType([
        StructField("Offer", StringType(), True),
        StructField("Final Total Beta Price", FloatType(), True),
    ])

    data = [(f"offer_{i}", float(final_total_beta_price[i]))
            for i in final_total_beta_price]

    # Create and return the DataFrame using the specified schema
    total_beta_price_df = spark.createDataFrame(data, schema=schema)

    return total_beta_price_df
