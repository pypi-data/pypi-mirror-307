import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType

from .metrics import top_n
from .helpers import actual_revenue_helper, expected_revenue_helper
from .predictions import predict_on_data_v4
from .predictions import udf_factory
from .predictions import predict_on_data_v2

def diagnostic_1(spark,
    data_in_pandas,
    utilities,
    availability,
    run_name,
    no_alternatives,
    wa,
    asc_nobuy,
    beta_values,
    description,
) -> float:
    predictions = predict_on_data_v4(
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
    )
    # Transpose prob columns
    prob_cols = (
        [f"prob_fare_level_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"prob_fare_level_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_proba = predictions[prob_cols]
    y_prob_chosen = df_proba.stack().reset_index(drop=True).to_frame()

    # Transpose choice columns
    choice_cols = (
        [f"choice_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"choice_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_choice = predictions[choice_cols]
    y_true = df_choice.stack().reset_index(drop=True).to_frame()

    return {
        "buy_pred" : df_choice.sum(),
        "bought": y_true.sum()
    }

def eval_how_close(
    spark,
    data_in_pandas,
    utilities,
    availability,
    run_name,
    no_alternatives,
    wa,
    asc_nobuy,
    beta_values,
    description,
) -> float:
    predictions = predict_on_data_v4(
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
    )
    no_records = (
        data_in_pandas.loc[data_in_pandas["chosenAlternative"] > 0].shape[0]
        if wa
        else data_in_pandas.shape[0]
    )

    for n in range(1, 6):
        predictions = top_n(predictions, n, no_alternatives, no_records)

    top_1 = predictions["top_1"][0]
    top_2 = predictions["top_2"][0]
    top_3 = predictions["top_3"][0]
    top_4 = predictions["top_4"][0]
    top_5 = predictions["top_5"][0]

    # Transpose prob columns
    prob_cols = (
        [f"prob_fare_level_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"prob_fare_level_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_proba = predictions[prob_cols]
    y_prob_chosen = df_proba.stack().reset_index(drop=True).to_frame()

    # Transpose choice columns
    choice_cols = (
        [f"choice_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"choice_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_choice = predictions[choice_cols]
    y_true = df_choice.stack().reset_index(drop=True).to_frame()

    brier_score = brier_score_loss(y_true, y_prob_chosen)
    predictions["brier_score"] = brier_score

    actual_revenue = actual_revenue_helper(
        data_predict=predictions, no_alternatives=no_alternatives
    )
    expected_revenue = expected_revenue_helper(
        data_predict=predictions,
        no_alternatives=no_alternatives,
        lower_limit=0 if wa else 1,
    )
    relative_error = abs((expected_revenue - actual_revenue) / actual_revenue)
    predictions["relative_error"] = relative_error

    return float(relative_error)


def eval_how_close_with_diag_1(
    spark,
    data_in_pandas,
    utilities,
    availability,
    run_name,
    no_alternatives,
    wa,
    asc_nobuy,
    beta_values,
    description,
) -> float:
    predictions = predict_on_data_v4(
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
    )
    no_records = (
        data_in_pandas.loc[data_in_pandas["chosenAlternative"] > 0].shape[0]
        if wa
        else data_in_pandas.shape[0]
    )

    for n in range(1, 6):
        predictions = top_n(predictions, n, no_alternatives, no_records)

    top_1 = predictions["top_1"][0]
    top_2 = predictions["top_2"][0]
    top_3 = predictions["top_3"][0]
    top_4 = predictions["top_4"][0]
    top_5 = predictions["top_5"][0]

    # Transpose prob columns
    prob_cols = (
        [f"prob_fare_level_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"prob_fare_level_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_proba = predictions[prob_cols]
    y_prob_chosen = df_proba.stack().reset_index(drop=True).to_frame()

    # Transpose choice columns
    choice_cols = (
        [f"choice_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"choice_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_choice = predictions[choice_cols]
    y_true = df_choice.stack().reset_index(drop=True).to_frame()

    brier_score = brier_score_loss(y_true, y_prob_chosen)
    predictions["brier_score"] = brier_score

    actual_revenue = actual_revenue_helper(
        data_predict=predictions, no_alternatives=no_alternatives
    )
    expected_revenue = expected_revenue_helper(
        data_predict=predictions,
        no_alternatives=no_alternatives,
        lower_limit=0 if wa else 1,
    )
    relative_error = abs((expected_revenue - actual_revenue) / actual_revenue)
    predictions["relative_error"] = relative_error

    buy_pred = sum(1.0-df_proba.prob_fare_level_0)
    bought = y_true.sum().values[0]

    rel_diag_1 = abs((buy_pred - bought)/bought)
    return abs(relative_error + rel_diag_1)



def print_stats_3(
    spark,
    data_in_pandas,
    utilities,
    availability,
    run_name,
    no_alternatives,
    wa,
    asc_nobuy,
    beta_values,
    description,
):
    predictions = predict_on_data_v4(
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
    )

    no_records = (
        data_in_pandas.loc[data_in_pandas["chosenAlternative"] > 0].shape[0]
        if wa
        else data_in_pandas.shape[0]
    )

    for n in range(1, 6):
        predictions = top_n(predictions, n, no_alternatives, no_records)

    top_1 = predictions["top_1"][0]
    top_2 = predictions["top_2"][0]
    top_3 = predictions["top_3"][0]
    top_4 = predictions["top_4"][0]
    top_5 = predictions["top_5"][0]

    # Transpose prob columns
    prob_cols = (
        [f"prob_fare_level_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"prob_fare_level_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_proba = predictions[prob_cols]
    y_prob_chosen = df_proba.stack().reset_index(drop=True).to_frame()

    # Transpose choice columns
    choice_cols = (
        [f"choice_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"choice_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_choice = predictions[choice_cols]
    y_true = df_choice.stack().reset_index(drop=True).to_frame()

    brier_score = brier_score_loss(y_true, y_prob_chosen)
    predictions["brier_score"] = brier_score

    actual_revenue = actual_revenue_helper(
        data_predict=predictions, no_alternatives=no_alternatives
    )
    expected_revenue = expected_revenue_helper(
        data_predict=predictions,
        no_alternatives=no_alternatives,
        lower_limit=0 if wa else 1,
    )
    relative_error = (expected_revenue - actual_revenue) / actual_revenue
    predictions["relative_error"] = relative_error

    return {
        "how_close": float(relative_error),
        "brier_score": float(brier_score),
        "accuracy": float(top_1),
        "top_2": float(top_2),
        "top_3": float(top_3),
        "top_4": float(top_4),
        "top_5": float(top_5)
    }, predictions


def print_stats_4(
    spark,
    data_in_pandas,
    utilities,
    availability,
    run_name,
    no_alternatives,
    wa,
    asc_nobuy,
    beta_values,
    description,
):
    predictions = predict_on_data_v4(
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
    )

    no_records = (
        data_in_pandas.loc[data_in_pandas["chosenAlternative"] > 0].shape[0]
        if wa
        else data_in_pandas.shape[0]
    )

    for n in range(1, 6):
        predictions = top_n(predictions, n, no_alternatives, no_records)

    top_1 = predictions["top_1"][0]
    top_2 = predictions["top_2"][0]
    top_3 = predictions["top_3"][0]
    top_4 = predictions["top_4"][0]
    top_5 = predictions["top_5"][0]

    # Transpose prob columns
    prob_cols = (
        [f"prob_fare_level_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"prob_fare_level_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_proba = predictions[prob_cols]
    y_prob_chosen = df_proba.stack().reset_index(drop=True).to_frame()

    # Transpose choice columns
    choice_cols = (
        [f"choice_{i}" for i in range(no_alternatives + 1)]
        if wa
        else [f"choice_{i}" for i in range(1, no_alternatives + 1)]
    )
    df_choice = predictions[choice_cols]
    y_true = df_choice.stack().reset_index(drop=True).to_frame()

    brier_score = brier_score_loss(y_true, y_prob_chosen)
    predictions["brier_score"] = brier_score

    actual_revenue = actual_revenue_helper(
        data_predict=predictions, no_alternatives=no_alternatives
    )
    expected_revenue = expected_revenue_helper(
        data_predict=predictions,
        no_alternatives=no_alternatives,
        lower_limit=0 if wa else 1,
    )
    relative_error = (expected_revenue - actual_revenue) / actual_revenue
    predictions["relative_error"] = relative_error

    return {
        "how_close": float(relative_error),
        "brier_score": float(brier_score),
        "accuracy": float(top_1),
        "top_2": float(top_2),
        "top_3": float(top_3),
        "top_4": float(top_4),
        "top_5": float(top_5),
        "buy_pred" : sum(1.0-df_proba.prob_fare_level_0),
        "bought": y_true.sum().values[0]
    }, predictions



def generate_schema(existing_schema, no_alternatives):
    fields = existing_schema.fields

    fields.extend(
        [
            StructField("prob_sum", DoubleType(), True),
        ]
    )
    for i in range(1, no_alternatives + 1):
        fields.extend(
            [
                StructField(f"prob_fare_level_{i}", DoubleType(), True),
                StructField(f"prob_fare_level_{i}_rank", DoubleType(), True),
            ]
        )

    schema = StructType(fields)

    return schema


def print_stats_2(
    spark,
    data,
    utilities,
    availability,
    run_name,
    no_alternatives,
    wa,
    asc_nobuy,
    beta_values,
    description,
):
    # Convert the Pandas DataFrame to a Spark DataFrame
    spark_df = spark.createDataFrame(data)

    schema = generate_schema(spark_df.schema, no_alternatives)

    # Generate UDF with provided parameters
    custom_udf = udf_factory(
        utilities,
        availability,
        run_name,
        description,
        no_alternatives,
        wa,
        beta_values,
        asc_nobuy,
    )

    predictions = spark_df.groupby("chid").applyInPandas(custom_udf, schema=schema)

    # Convert Spark DataFrame back to Pandas DataFrame for further processing
    predictions = predictions.toPandas()

    for n in range(1, 6):
        predictions = top_n(
            data_predict=predictions, n=n, no_alternatives=no_alternatives
        )

    top_1 = predictions["top_1"][0]
    top_2 = predictions["top_2"][0]
    top_3 = predictions["top_3"][0]
    top_4 = predictions["top_4"][0]
    top_5 = predictions["top_5"][0]

    # Transpose prob columns
    prob_cols = (
        [f"prob_fare_level_{i}" for i in range(11)]
        if wa
        else [f"prob_fare_level_{i}" for i in range(1, 11)]
    )
    df_proba = predictions[prob_cols]
    y_prob_chosen = df_proba.stack().reset_index(drop=True).to_frame()

    # Transpose choice columns
    choice_cols = (
        [f"choice_{i}" for i in range(11)]
        if wa
        else [f"choice_{i}" for i in range(1, 11)]
    )
    df_choice = predictions[choice_cols]
    y_true = df_choice.stack().reset_index(drop=True).to_frame()

    brier_score = brier_score_loss(y_true, y_prob_chosen)
    predictions["brier_score"] = brier_score

    actual_revenue = actual_revenue_helper(
        data_predict=predictions, no_alternatives=no_alternatives
    )
    expected_revenue = expected_revenue_helper(
        data_predict=predictions,
        no_alternatives=no_alternatives,
        lower_limit=0 if wa else 1,
    )
    relative_error = (expected_revenue - actual_revenue) / actual_revenue
    predictions["relative_error"] = relative_error

    return {
        "how_close": float(relative_error),
        "brier_score": float(brier_score),
        "accuracy": float(top_1),
        "top_2": float(top_2),
        "top_3": float(top_3),
        "top_4": float(top_4),
        "top_5": float(top_5),
    }


def print_stats(
    data, utilities, availability, run_name, no_alternatives, wa, asc_nobuy, description
):
    predictions = predict_on_data_v2(
        V=utilities,
        av=availability,
        data_in_pandas=data,
        run_name=run_name,
        description=description,
        no_alternatives=no_alternatives,
        wa=wa,
        asc_nobuy=asc_nobuy,
    )

    lower_limit = 0 if wa else 1

    predictions = top_n(data_predict=predictions, n=1, no_alternatives=no_alternatives)
    predictions = top_n(data_predict=predictions, n=2, no_alternatives=no_alternatives)
    predictions = top_n(data_predict=predictions, n=3, no_alternatives=no_alternatives)
    predictions = top_n(data_predict=predictions, n=4, no_alternatives=no_alternatives)
    predictions = top_n(data_predict=predictions, n=5, no_alternatives=no_alternatives)

    top_1 = predictions["top_1"][0]
    top_2 = predictions["top_2"][0]
    top_3 = predictions["top_3"][0]
    top_4 = predictions["top_4"][0]
    top_5 = predictions["top_5"][0]

    # Transpose prob columns
    prob_cols = (
        [
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
        if wa
        else [
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
    )
    df_proba = predictions[prob_cols]
    y_prob_chosen = df_proba.stack().reset_index(drop=True).to_frame()

    # Transpose choice columns
    choice_cols = (
        [
            "choice_0",
            "choice_1",
            "choice_2",
            "choice_3",
            "choice_4",
            "choice_5",
            "choice_6",
            "choice_7",
            "choice_8",
            "choice_9",
            "choice_10",
        ]
        if wa
        else [
            "choice_1",
            "choice_2",
            "choice_3",
            "choice_4",
            "choice_5",
            "choice_6",
            "choice_7",
            "choice_8",
            "choice_9",
            "choice_10",
        ]
    )
    df_choice = predictions[choice_cols]
    y_true = df_choice.stack().reset_index(drop=True).to_frame()
    brier_score = brier_score_loss(y_true, y_prob_chosen)
    predictions["brier_score"] = brier_score
    actual_revenue = actual_revenue_helper(
        data_predict=predictions, no_alternatives=no_alternatives
    )
    expected_revenue = expected_revenue_helper(
        data_predict=predictions,
        no_alternatives=no_alternatives,
        lower_limit=lower_limit,
    )
    relative_error = (expected_revenue - actual_revenue) / actual_revenue
    predictions["relative_error"] = relative_error

    return {
        "how_close": float(relative_error),
        "brier_score": float(brier_score),
        "accuracy": float(top_1),
        "top_2": float(top_2),
        "top_3": float(top_3),
        "top_4": float(top_4),
        "top_5": float(top_5),
    }


def how_close_baseline(df, prob_buy) -> float:
    price_columns = [col for col in df.columns if col.startswith("price_")]
    mean_prices = df[price_columns].mean(axis=1)
    adjusted_prices = mean_prices * prob_buy
    total_adjusted_price = adjusted_prices.sum()
    return total_adjusted_price


def wa_global(predictions) -> float:
    return predictions.prob_fare_level_0.mean()