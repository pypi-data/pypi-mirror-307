"""
This Python module provides functions for predicting outcomes using discrete choice models
via the Biogeme framework. It includes functions to perform predictions on both full datasets
and sampled subsets, incorporating functionalities for data preprocessing, model simulation,
and ranking of probability outcomes.

Functions:
    predict_d(data, betas): Predicts discrete choice probabilities and rankings for each choice level.
    predict_on_data(data_in_pandas, run_name, description, n=500, random_state=1963): Predicts discrete choice probabilities on a sampled subset of data, ranks choice levels, and calculates normalized probabilities excluding the "walk-away" option.

Dependencies:
    numpy, pandas, biogeme (biogeme.database, biogeme.biogeme, biogeme.models, biogeme.version, biogeme.expressions, biogeme.results), and a custom 'helpers' module.

Example usage:
    import pandas as pd
    data_frame = pd.read_csv('your_data.csv')
    betas = {'beta1': 0.5, 'beta2': -1.2}
    predictions = predict_d(data_frame, betas)
"""

import numpy as np  
import pandas as pd
from collections import namedtuple
from pyspark.sql.types import FloatType, StructField, StructType
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql import functions as F
import pyspark

from scipy.special import lambertw

import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.version as ver
from biogeme.expressions import Variable, Beta
import biogeme.results as res

def simulate_helper(V, av, no_alternatives=10, lower_limit=0):
    """
    Simulates choice probabilities for each alternative using a logit model,
    given utilities and availability.

    Parameters:
        V (dict): The systematic utilities for each alternative.
        av (dict): The availability indicators for each alternative.
        no_alternatives (int): The total number of alternatives.
        lower_limit (int): The lower bound to start simulating from (inclusive).

    Returns:
        dict: A dictionary with alternatives as keys and their simulated
        choice probabilities as values.
    """
    probabilities = {
        f"prob_fare_level_{i}": models.logit(V, av, i)
        for i in range(lower_limit, no_alternatives + 1)
    }
    return probabilities




def optimize_for_price(betas, data):
    # Range of indices
    indices = range(11)  # 0 to 10

    # Process each index
    for index in indices:
        # Initialize the column for summing up the products
        sum_col = F.lit(0)

        # Iterate over betas and apply logic
        for key, value in betas.items():
            if key != "B_price" and not key.startswith("ASC_"):
                # Extract base column name
                base_col_name = key.split("B_")[-1]

                # Construct the full column name with index
                full_col_name = f"{base_col_name}_{index}"

                # Check if the column exists in the DataFrame
                if full_col_name in data.columns:
                    # Compute product and add to sum_col
                    # Only include if av_index is 1
                    sum_col += F.when(
                        F.col(f"av_{index}") == 1, F.col(full_col_name) * F.lit(value)
                    ).otherwise(0)

        # Add the computed sum as a new column a_index
        data = data.withColumn(f"a_{index}", sum_col)

        b = betas["B_price"]


def predict_d(V, av, data, betas):
    """
    Predict discrete choice model probabilities using the specified betas.

    This function simulates the choice probabilities for different fare levels in the dataset,
    ranks the probabilities, and appends the results to the original dataframe.

    Parameters:
        data (pandas.DataFrame): The input data on which to perform predictions.
        betas (dict): A dictionary of beta coefficients used for simulation.

    Returns:
        pandas.DataFrame: The original dataframe augmented with simulated probabilities and their rankings.
    """

    df = data.copy()

    database = db.Database("dataset/offers", df)
    simulate = simulate_helper(V, av)
    biogeme = bio.BIOGEME(database, simulate)

    simulatedValues = biogeme.simulate(betas)
    simulatedValues["prob_sum"] = simulatedValues.sum(axis=1)

    df = pd.concat([df, simulatedValues], axis=1).reset_index(drop=True)
    ranked_cols = [
        "prob_fare_level_0",
        "prob_fare_level_1",
        "prob_fare_level_2",
        "prob_fare_level_3",
        "prob_fare_level_4",
        "prob_fare_level_5",
        "prob_fare_level_6",
        "prob_fare_level_7",
        "prob_fare_level_8",
        "prob_fare_level_9",
        "prob_fare_level_10",
    ]
    df[[col + "_rank" for col in ranked_cols]] = df[ranked_cols].rank(
        axis=1, method="dense", ascending=False
    )
    return df


def predict_d_v2(
    asc_nobuy_cal,
    V,
    av,
    database,
    dataset,
    betas,
):
    """
    Simulate and rank discrete choice model probabilities on a sampled subset of the data.

    The function samples a subset of data, performs simulation to predict choice probabilities,
    and then ranks the probabilities for each fare level. Additionally, it computes the normalized
    probabilities excluding the "walk-away" option.

    Parameters:
        V: utilities
        av: availability
        data_in_pandas (pandas.DataFrame): The complete dataset from which a sample will be taken.
        run_name (str): The name for the simulation run, used for identifying output files.
        description (str): A brief description of the simulation run.
        n (int): The number of samples to draw from the dataset (default is 500).
        random_state (int): A seed for the random number generator to ensure reproducibility (default is 1963).

    Returns:
        pandas.DataFrame: A sampled and augmented dataframe with simulated probabilities, rankings, and normalized probabilities.
    """

    simulate = simulate_helper(V, av)
    biogeme = bio.BIOGEME(database, simulate)

    betas["ASC_NOBUY"] = asc_nobuy_cal

    simulatedValues = biogeme.simulate(betas)
    simulatedValues["prob_sum"] = simulatedValues.sum(axis=1)

    data_result = pd.concat([dataset, simulatedValues], axis=1).reset_index(drop=True)

    ranked_cols = [
        "prob_fare_level_0",
        "prob_fare_level_1",
        "prob_fare_level_2",
        "prob_fare_level_3",
        "prob_fare_level_4",
        "prob_fare_level_5",
        "prob_fare_level_6",
        "prob_fare_level_7",
        "prob_fare_level_8",
        "prob_fare_level_9",
        "prob_fare_level_10",
    ]
    data_result[[col + "_rank" for col in ranked_cols]] = data_result[ranked_cols].rank(
        axis=1, method="dense", ascending=False
    )

    return data_result


def predict_on_data(
    V, av, data_in_pandas, run_name, description, n=500, random_state=1963
):
    """
    Simulate and rank discrete choice model probabilities on a sampled subset of the data.

    The function samples a subset of data, performs simulation to predict choice probabilities,
    and then ranks the probabilities for each fare level. Additionally, it computes the normalized
    probabilities excluding the "walk-away" option.

    Parameters:
        V: utilities
        av: availability
        data_in_pandas (pandas.DataFrame): The complete dataset from which a sample will be taken.
        run_name (str): The name for the simulation run, used for identifying output files.
        description (str): A brief description of the simulation run.
        n (int): The number of samples to draw from the dataset (default is 500).
        random_state (int): A seed for the random number generator to ensure reproducibility (default is 1963).

    Returns:
        pandas.DataFrame: A sampled and augmented dataframe with simulated probabilities, rankings, and normalized probabilities.
    """

    data_sampled = data_in_pandas.sample(n=n, random_state=random_state)
    database = db.Database("dataset/offers", data_sampled)

    simulate = simulate_helper(V, av)

    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = f"{run_name}-{description}"

    betas = biogeme.freeBetaNames

    results = res.bioResults(pickleFile=f"{run_name}.pickle")
    betaValues = results.getBetaValues()
    simulatedValues = biogeme.simulate(betaValues)
    simulatedValues["prob_sum"] = simulatedValues.sum(axis=1)

    data_sampled = pd.concat([data_sampled, simulatedValues], axis=1).reset_index(
        drop=True
    )

    ranked_cols = [
        "prob_fare_level_0",
        "prob_fare_level_1",
        "prob_fare_level_2",
        "prob_fare_level_3",
        "prob_fare_level_4",
        "prob_fare_level_5",
        "prob_fare_level_6",
        "prob_fare_level_7",
        "prob_fare_level_8",
        "prob_fare_level_9",
        "prob_fare_level_10",
    ]
    data_sampled[[col + "_rank" for col in ranked_cols]] = data_sampled[
        ranked_cols
    ].rank(axis=1, method="dense", ascending=False)

    # Add the probabilities without walk-away normalized
    for level in range(1, 11):
        data_sampled[f"prob_no_wa_{level}"] = data_sampled[
            f"prob_fare_level_{level}"
        ] / (1.0 - data_sampled["prob_fare_level_0"])

    ranked_cols = [
        "prob_no_wa_1",
        "prob_no_wa_2",
        "prob_no_wa_3",
        "prob_no_wa_4",
        "prob_no_wa_5",
        "prob_no_wa_6",
        "prob_no_wa_7",
        "prob_no_wa_8",
        "prob_no_wa_9",
        "prob_no_wa_10",
    ]
    data_sampled[[col + "_rank" for col in ranked_cols]] = data_sampled[
        ranked_cols
    ].rank(axis=1, method="dense", ascending=False)

    return data_sampled


PredictFlags = namedtuple(
    "Predict_flags",
    [
        "V",
        "av",
        "data_in_pandas",
        "run_name",
        "description",
        "no_alternatives",
        "wa",
        "asc_nobuy",
    ],
)


def predict_on_data_v2(**kwargs):
    """
    Simulate and rank discrete choice model probabilities on a sampled subset of the data.

    The function samples a subset of data, performs simulation to predict choice probabilities,
    and then ranks the probabilities for each fare level. Additionally, it computes the normalized
    probabilities excluding the "walk-away" option.

    Parameters:
        V: utilities
        av: availability
        data_in_pandas (pandas.DataFrame): The complete dataset from which a sample will be taken.
        run_name (str): The name for the simulation run, used for identifying output files.
        description (str): A brief description of the simulation run.
        n (int): The number of samples to draw from the dataset (default is 500).
        random_state (int): A seed for the random number generator to ensure
        reproducibility (default is 1963).

    Returns:
        pandas.DataFrame: A sampled and augmented dataframe with simulated probabilities,
        rankings, and normalized probabilities.
    """

    (
        utilities,
        av,
        data_in_pandas,
        run_name,
        description,
        no_alternatives,
        wa,
        asc_nobuy,
    ) = PredictFlags(**kwargs)

    database = db.Database("dataset/offers", data_in_pandas)

    lower_limit = 0 if wa else 1

    simulate = simulate_helper(utilities, av, no_alternatives, lower_limit)

    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = f"{run_name}-{description}"

    results = res.bioResults(pickleFile=f"{run_name}.pickle")
    beta_values = results.getBetaValues()

    if asc_nobuy != 0:
        beta_values["ASC_NOBUY"] = asc_nobuy

    simulated_values = biogeme.simulate(beta_values)
    simulated_values["prob_sum"] = simulated_values.sum(axis=1)

    final_df = pd.concat([data_in_pandas, simulated_values], axis=1).reset_index(
        drop=True
    )

    ranked_cols = [f"prob_fare_level_{i}" for i in range(1, no_alternatives + 1)]

    final_df[[col + "_rank" for col in ranked_cols]] = final_df[ranked_cols].rank(
        axis=1, method="dense", ascending=False
    )

    return final_df


# ******************************
# *     Pandas UDF version     *
# ******************************
PredictFlags_UDF = namedtuple(
    "Predict_flags",
    [
        "V",
        "av",
        "data_in_pandas",
        "run_name",
        "description",
        "no_alternatives",
        "wa",
        "beta_values",
        "asc_nobuy",
    ],
)

# Define a Pandas UDF for applying the model simulation
def udf_factory(
    utilities,
    availability,
    run_name,
    description,
    no_alternatives,
    wa,
    beta_values,
    asc_nobuy,
):
    def predict_on_data_udf(pdf):
        # Create a database from the incoming pdf
        database = db.Database("dataset/offers", pdf)
        lower_limit = 0 if wa else 1

        # Simulate based on the provided utility definitions
        simulate = simulate_helper(
            utilities, availability, no_alternatives, lower_limit
        )

        biogeme = bio.BIOGEME(database, simulate)
        biogeme.modelName = f"{run_name}-{description}"

        # Update ASC_NOBUY in the beta_values dictionary
        local_beta_values = (
            beta_values.copy()
        )  # Make a copy if shared across invocations
        local_beta_values["ASC_NOBUY"] = asc_nobuy

        simulated_values = biogeme.simulate(local_beta_values)

        # simulated_values["prob_sum"] = simulated_values.sum(axis=1)

        # # Merge results back to the original data
        # final_df = pd.concat([pdf, simulated_values], axis=1).reset_index(drop=True)

        # # Generate ranked columns based on probabilities
        # ranked_cols = [f"prob_fare_level_{I}" for I in range(1, no_alternatives + 1)]
        # final_df[[col + "_rank" for col in ranked_cols]] = final_df[ranked_cols].rank(
        #     axis=1, method="dense", ascending=False
        # )

        # final_df.columns = list(final_df.columns)

        return pdf

        # return spark.createDataFrame(final_df)

    return predict_on_data_udf


def predict_on_data_v3(
    asc_nobuy_cal,
    V,
    av,
    data_in_pandas,
    run_name,
    description,
    n=500,
    random_state=1963,
):
    """
    Simulate and rank discrete choice model probabilities on a sampled subset of the data.

    The function samples a subset of data, performs simulation to predict choice probabilities,
    and then ranks the probabilities for each fare level. Additionally, it computes the normalized
    probabilities excluding the "walk-away" option.

    Parameters:
        V: utilities
        av: availability
        data_in_pandas (pandas.DataFrame): The complete dataset from which a sample will be taken.
        run_name (str): The name for the simulation run, used for identifying output files.
        description (str): A brief description of the simulation run.
        n (int): The number of samples to draw from the dataset (default is 500).
        random_state (int): A seed for the random number generator to ensure reproducibility (default is 1963).

    Returns:
        pandas.DataFrame: A sampled and augmented dataframe with simulated probabilities, rankings, and normalized probabilities.
    """

    data_sampled = data_in_pandas.sample(n=n, random_state=random_state)
    database = db.Database("dataset/offers", data_sampled)

    simulate = simulate_helper(V, av)

    biogeme = bio.BIOGEME(database, simulate)
    biogeme.modelName = f"{run_name}-{description}"

    betas = biogeme.freeBetaNames

    results = res.bioResults(pickleFile=f"{run_name}.pickle")
    betaValues = results.getBetaValues()

    betaValues["ASC_NOBUY"] = asc_nobuy_cal

    simulatedValues = biogeme.simulate(betaValues)
    simulatedValues["prob_sum"] = simulatedValues.sum(axis=1)

    data_sampled = pd.concat([data_sampled, simulatedValues], axis=1).reset_index(
        drop=True
    )

    ranked_cols = [
        "prob_fare_level_0",
        "prob_fare_level_1",
        "prob_fare_level_2",
        "prob_fare_level_3",
        "prob_fare_level_4",
        "prob_fare_level_5",
        "prob_fare_level_6",
        "prob_fare_level_7",
        "prob_fare_level_8",
        "prob_fare_level_9",
        "prob_fare_level_10",
    ]
    data_sampled[[col + "_rank" for col in ranked_cols]] = data_sampled[
        ranked_cols
    ].rank(axis=1, method="dense", ascending=False)

    return data_sampled


# **********************************
# *      Parallel version.         *
# **********************************


def worker_helper(
    utilities,
    availability,
    run_name,
    description,
    no_alternatives,
    wa,
    beta_values,
    asc_nobuy,
):
    def worker(rows):
        # Convert the iterator of rows to a pandas DataFrame
        pandas_df = pd.DataFrame([row.asDict() for row in rows])

        # Perform the simulation on the pandas DataFrame
        database = db.Database("dataset/offers", pandas_df)

        lower_limit = 0 if wa else 1

        # Simulate based on the provided utility definitions
        simulate = simulate_helper(
            utilities, availability, no_alternatives, lower_limit
        )

        biogeme = bio.BIOGEME(database, simulate)
        biogeme.modelName = f"{run_name}-{description}"

        # Update ASC_NOBUY in the beta_values dictionary
        local_beta_values = (
            beta_values.copy()
        )  # Make a copy if shared across invocations
        if wa:
            local_beta_values["ASC_NOBUY"] = asc_nobuy

        simulated_values = biogeme.simulate(local_beta_values)

        simulated_values["prob_sum"] = simulated_values.sum(axis=1)

        # Generate ranked columns based on probabilities
        ranked_cols = [f"prob_fare_level_{I}" for I in range(1, no_alternatives + 1)]
        simulated_values[[col + "_rank" for col in ranked_cols]] = simulated_values[
            ranked_cols
        ].rank(axis=1, method="dense", ascending=False)

        # Yield the simulated values as a dictionary
        for _, row in simulated_values.iterrows():
            yield row.to_dict()

    return worker


def predict_on_data_v4(
    spark,
    data_in_pandas,
    utilities,
    availability,
    run_name,
    description,
    no_alternatives,
    wa,
    beta_values,
    asc_nobuy,
):

    spark_df = spark.createDataFrame(data_in_pandas)
    # Use mapPartitions to apply the worker function to each partition
    simulated_values = spark_df.rdd.mapPartitions(
        worker_helper(
            utilities,
            availability,
            run_name,
            description,
            no_alternatives,
            wa,
            beta_values,
            asc_nobuy,
        )
    )
    simulated_values = pd.DataFrame(simulated_values.collect())
    # Merge results back to the original data
    final_df = pd.concat([data_in_pandas, simulated_values], axis=1).reset_index(
        drop=True
    )

    return final_df
