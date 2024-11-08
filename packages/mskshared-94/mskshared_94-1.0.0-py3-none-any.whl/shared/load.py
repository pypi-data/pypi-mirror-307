"""
This module contains functions for loading, processing, and saving flight data using PySpark.

Functions:
- add_time_of_day_coding: Encodes departure time as cyclical features for machine learning models.
- add_indicators: Adds indicator features for flight alternatives.
- save_the_offers: Saves a PySpark DataFrame of offers to a specified table.
- save_the_train_data: Saves a PySpark DataFrame as the training dataset.
- save_the_test_data: Saves a PySpark DataFrame as the testing dataset.
- save_the_validation_data: Saves a PySpark DataFrame as the validation dataset.
- load_wa_data: Loads flight search data from a CSV file.
- split_sessions: Splits a PySpark DataFrame into training and testing sets based on user sessions.
- split_sessions_2: Splits a PySpark DataFrame into training and testing sets, 
ensuring representation of positive cases.
- split_the_data_2: Splits a PySpark DataFrame into training and testing sets with 
positive case stratification.
"""

from math import pi
from collections import namedtuple
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
import pandas as pd

spark = SparkSession.builder.getOrCreate()


_WA_QSI_FILE = "/dbfs/FileStore/data/dpe/feed/qsi_departuretime.csv"
_OFFERSFILE = "dbfs:/FileStore/data/dpe/feed/offers.csv"
_OFFERS_FOR_DP_FILE = "/dbfs/FileStore/data/dpe/out/offers_for_dp.csv"
_FULL_UIDS = "/dbfs/FileStore/data/dpe/feed/match_type_full_jan_2022.csv"


def add_time_of_day_coding(d):
    """
    Adds time of day coding columns to the input DataFrame.

    Args:
        d (DataFrame): Input DataFrame containing the schedule departure time.

    Returns:
        DataFrame: DataFrame with additional time of day coding columns.
    """

    d = d.withColumn(
        "Dep_norm_2pi", 2 * pi *
        F.col("schedule_departure_time_minutes") / 1440.0
    )
    d = d.withColumn(
        "Dep_norm_4pi", 4 * pi *
        F.col("schedule_departure_time_minutes") / 1440.0
    )
    d = d.withColumn(
        "Dep_norm_6pi", 6 * pi *
        F.col("schedule_departure_time_minutes") / 1440.0
    )
    d = d.withColumn("Dep_2pi_cos", F.cos(F.col("Dep_norm_2pi")))
    d = d.withColumn("Dep_2pi_sin", F.sin(F.col("Dep_norm_2pi")))
    d = d.withColumn("Dep_4pi_cos", F.cos(F.col("Dep_norm_4pi")))
    d = d.withColumn("Dep_4pi_sin", F.sin(F.col("Dep_norm_4pi")))
    d = d.withColumn("Dep_6pi_cos", F.cos(F.col("Dep_norm_6pi")))
    d = d.withColumn("Dep_6pi_sin", F.sin(F.col("Dep_norm_6pi")))

    return d


def add_indicators(d):
    """
    Adds indicators to the DataFrame 'd' based on certain conditions.

    Parameters:
    - d: DataFrame
        The input DataFrame to which the indicators will be added.

    Returns:
    - d: DataFrame
        The modified DataFrame with the added indicators.
    """

    # Indicators for the alternatives
    d = d.withColumn(
        "has_one_leg", F.when(F.col("schedule_number_of_legs")
                              == 1.0, 1).otherwise(0)
    )
    d = d.withColumn(
        "has_three_legs",
        F.when(F.col("schedule_number_of_legs") == 3.0, 1).otherwise(0),
    )
    d = d.withColumn(
        "dp_less_than_7_days",
        F.when(F.col("daysinadvance_fulljourney_departure")
               < 7.0, 1).otherwise(0),
    )
    d = d.withColumn(
        "dp_more_than_7_less_than_14_days",
        F.when(
            (F.col("daysinadvance_fulljourney_departure") >= 7.0)
            & (F.col("daysinadvance_fulljourney_departure") < 14.0),
            1,
        ).otherwise(0),
    )
    d = d.withColumn(
        "dp_more_than_14_days",
        F.when(F.col("daysinadvance_fulljourney_departure")
               >= 14.0, 1).otherwise(0),
    )
    d = d.withColumn(
        "traveling_with_child",
        F.when(F.col("rq_childrenratio")
               == 0, 1).otherwise(0),
    )
    d = d.withColumn(
        "booking_weekday",
        F.when(F.col("transaction_DOW").isin(
            ["Saturday", "Sunday"]), "Weekend").otherwise("Weekday"),
    )
    d = d.withColumn(
        "departure_weekday",
        F.when(F.col("schedule_departure_DOW").isin(
            ["Saturday", "Sunday"]), "Weekend").otherwise("Weekday"),
    )

    return d


def save_the_offers(offers_pdf, table="flx_datascience.offers_for_dp"):
    """
    Save the offers PDF as a table in the specified database table.

    Args:
        offers_pdf (DataFrame): The offers PDF to be saved.
        table (str, optional): The name of the database table to save the offers. 
        Defaults to "flx_datascience.offers_for_dp".
    """
    offers_pdf.write.mode("overwrite").saveAsTable(table)


def save_the_train_data(df):
    """
    Saves the train data DataFrame to the 'flx_datascience.train_data_for_dp' table.

    Args:
        df (DataFrame): The DataFrame containing the train data.

    Returns:
        None
    """
    df.write.mode("overwrite").saveAsTable("flx_datascience.train_data_for_dp")


def save_the_test_data(df):
    """Saves a PySpark DataFrame as the testing dataset.

    Args:
        df (pyspark.sql.DataFrame): The DataFrame containing testing data.
    """

    df.write.mode("overwrite").saveAsTable("flx_datascience.test_data_for_dp")


def save_the_validation_data(df):
    """Saves a PySpark DataFrame as the validation dataset.

    Args:
        df (pyspark.sql.DataFrame): The DataFrame containing validation data.
    """

    df.write.mode("overwrite").saveAsTable(
        "flx_datascience.validation_data_for_dp")


def load_wa_data():
    """
    Load the WA data from a CSV file.

    Returns:
        pandas.DataFrame: The loaded WA data.
    """
    return pd.read_csv(_WA_QSI_FILE)


def split_sessions(d, train_ratio=0.9):
    """
    Split the input DataFrame into train and test DataFrames based on the given train ratio.

    Args:
        d (DataFrame): The input DataFrame to be split.
        train_ratio (float, optional): The ratio of data to be used for training. Defaults to 0.9.

    Returns:
        tuple: A tuple containing the train DataFrame and test DataFrame.
    """
    grouped_df = d.groupBy("uuid").agg(F.expr("collect_list(chid) as ids"))
    split_df = grouped_df.withColumn("split", F.rand(seed=1963))

    train_df = split_df.filter(F.col("split") <= train_ratio).drop(
        "split").join(d, on="uuid")
    test_df = split_df.filter(F.col("split") > train_ratio).drop(
        "split").join(d, on="uuid")

    return train_df, test_df


def split_sessions_2(d, train_ratio=0.9):
    """
    Splits the input DataFrame into training and test sets based on the given train ratio.

    Args:
        d (DataFrame): The input DataFrame to be split.
        train_ratio (float, optional): The ratio of data to be used for training. Defaults to 0.9.

    Returns:
        tuple: A tuple containing the training and test DataFrames.
    """

    positive_df = d.filter(F.col("chosenAlternative") > 0)
    negative_df = d.filter(F.col("chosenAlternative") <= 0)

    test_ratio = 1.0 - train_ratio

    pos_train, pos_test = positive_df.randomSplit(
        [train_ratio, test_ratio], seed=1963)
    neg_train, neg_test = negative_df.randomSplit(
        [train_ratio, test_ratio], seed=1963)

    train_df = pos_train.union(neg_train)
    test_df = pos_test.union(neg_test)

    assert train_df.filter(F.col("chosenAlternative") > 0).count(
    ) > 0, "No positive cases in training set!"
    assert test_df.filter(F.col("chosenAlternative") >
                          0).count() > 0, "No positive cases in test set!"

    return train_df, test_df


def split_the_data_2(d, train_ratio=0.8, test_ratio=0.2):
    """
    Splits the input DataFrame into training and test sets based on the given ratios.

    Args:
        d (DataFrame): The input DataFrame to be split.
        train_ratio (float, optional): The ratio of data to be used for training. Defaults to 0.8.
        test_ratio (float, optional): The ratio of data to be used for testing. Defaults to 0.2.

    Returns:
        tuple: A tuple containing the training DataFrame and the test DataFrame.
    """
    positive_df = d.filter(F.col("chosenAlternative") > 0)
    negative_df = d.filter(F.col("chosenAlternative") <= 0)
    pos_train, pos_test = positive_df.randomSplit(
        [train_ratio, test_ratio], seed=1963)
    neg_train, neg_test = negative_df.randomSplit(
        [train_ratio, test_ratio], seed=1963)
    train_df = pos_train.union(neg_train)
    test_df = pos_test.union(neg_test)
    assert train_df.filter(F.col("chosenAlternative") > 0).count(
    ) > 0, "No positive cases in training set!"
    assert test_df.filter(F.col("chosenAlternative") > 0).count(
    ) > 0, "No positive cases in test set!"
    return train_df, test_df


def split_the_data(d, train_ratio=0.7, debug_ratio=0.2):
    """
    Splits the input DataFrame into train, debug, and test datasets based on the specified ratios.

    Args:
        d (DataFrame): The input DataFrame to be split.
        train_ratio (float, optional): The ratio of data to be allocated for the train dataset. 
        Defaults to 0.7.
        debug_ratio (float, optional): The ratio of data to be allocated for the debug dataset. 
        Defaults to 0.2.

    Returns:
        dict: A dictionary containing the split datasets.
            - "data": The original input DataFrame without the "ids" column.
            - "train_data": The train dataset without the "ids" column.
            - "debug_data": The debug dataset without the "ids" column.
            - "test_data": The test dataset without the "ids" column.
    """

    grouped_df = d.groupBy("uuid").agg(F.expr("collect_list(chid) as ids"))
    split_df = grouped_df.withColumn("split", F.rand(seed=1963))
    train_df = (
        split_df.filter(F.col("split") <= train_ratio)
        .drop("split")
        .join(d, on="uuid")
    )
    debug_df = (
        split_df.filter(
            (F.col("split") > train_ratio)
            & (F.col("split") <= train_ratio + debug_ratio)
        )
        .drop("split")
        .join(d, on="uuid")
    )
    test_df = (
        split_df.filter(F.col("split") > train_ratio + debug_ratio)
        .drop("split")
        .join(d, on="uuid")
    )

    return {
        "data": d.drop("ids"),
        "train_data": train_df.drop("ids"),
        "debug_data": debug_df.drop("ids"),
        "test_data": test_df.drop("ids"),
    }


OffersFlags = namedtuple(
    "Offers_flags",
    [
        "day_start",
        "day_end",
        "month",
        "year",
        "include_walk_away",
        "choice_is_booked",
        "is_partial",
        "in_usd",
        "is_cheapest",
        "include_schedule",
        "data",
        "carrier"
    ],
)


def load_offers(**kwargs):
    """
    Load offers based on the provided filters.

    Args:
            **kwargs: Keyword arguments for filtering the offers.

    Returns:
            Tuple: A tuple containing the following:
                    - offers_pdf (DataFrame): The loaded offers data.
                    - cols_to_work_on (list): List of columns to work on.
                    - query (str): The SQL query used to load the offers.
    """

    of = OffersFlags(**kwargs)

    correct_index = "offer_booked_index" if of.choice_is_booked else "offer_priced_index"
    correct_field = "offer_booked" if of.choice_is_booked else "offer_priced"
    date_filter = f"""
        AND transaction_year_part2 = {of.year}
        AND transaction_month_part3 = {of.month}
        AND (
        transaction_DOM_part4 BETWEEN {of.day_start} AND {of.day_end}
        )
    """
    usd_filter = """
        AND currency = 'USD'
        """ if of.in_usd else ""
    partial_filter = """
        AND match_result = 'Partial'
        """ if of.is_partial else ""

    just_positive_and_cheapest_filter = """
        AND max_correct_index = 0
        AND sum_correct_field = 1
    """ if of.is_cheapest and not of.include_walk_away else ""
    wa_and_cheapest_filter = """
        AND (max_correct_index <= 0 OR max_correct_index is null)
        AND sum_correct_field <= 1
    """ if of.include_walk_away else ""
    just_positive_filter = """
        AND max_correct_index >= 0
    """ if not of.include_walk_away and not of.is_cheapest else ""

    single_cols_filter = """
        CAST(SPLIT(price_list, ',') [0] AS FLOAT) AS price,
        CAST(SPLIT(AS_rbd_list, ',') [0] AS STRING) AS rbd,
        CAST(SPLIT(farebasiscode_list, ',') [0] AS STRING) AS farebasiscode,
        CAST(SPLIT(AS_cabintypecode_list, ',') [0] AS STRING) AS cabintypecode,
        CAST(SPLIT(offer_id_list, ',') [0] AS STRING) AS offer_id
        """ if of.is_cheapest else f"""
        CASE 
                WHEN {correct_index} = -1 THEN 0
                ELSE {correct_index}
        END AS adjusted_index,
        CAST(SPLIT(price_list, ',') [adjusted_index] AS FLOAT) AS price,
        CAST(SPLIT(AS_rbd_list, ',') [adjusted_index] AS STRING) AS rbd,
        CAST(SPLIT(farebasiscode_list, ',') [adjusted_index] AS STRING) AS farebasiscode,
        CAST(SPLIT(AS_cabintypecode_list, ',') [adjusted_index] AS STRING) AS cabintypecode,
        CAST(SPLIT(offer_id_list, ',') [adjusted_index] AS STRING) AS offer_id
        """

    query = f"""
WITH ReducedDS AS (
    SELECT
        *,
        CONCAT(uuid, '->', CAST(od_order AS STRING)) AS chid,
        {correct_field} AS choice,
        {single_cols_filter},
        MAX({correct_index}) OVER (PARTITION BY src_grp_part1,
            transaction_year_part2,
            transaction_month_part3,
            transaction_DOM_part4,
            uuid,
            od_order) max_correct_index,
         SUM({correct_field}) OVER (PARTITION BY src_grp_part1,
            transaction_year_part2,
            transaction_month_part3,
            transaction_DOM_part4,
            uuid,
            od_order) sum_correct_field
    FROM
        {of.data}
    WHERE
        src_grp_part1 IN ({of.carrier})
        {date_filter}
        {usd_filter}
        {partial_filter}
)
SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY chid
      ORDER BY
        created
    ) AS alt
FROM ReducedDS
WHERE
    1 = 1
    {just_positive_and_cheapest_filter}
    {wa_and_cheapest_filter}
    {just_positive_filter}
        """

    offers_pdf = spark.sql(query)

    offers_pdf = offers_pdf.withColumn(
        "pax_count", F.size(F.split(F.col("pax_ptc_list"), ","))
    )
    offers_pdf = offers_pdf.withColumn(
        "price", F.col("price") / (F.col("pax_count") * 100.0)
    )

    offers_pdf = add_indicators(offers_pdf)
    offers_pdf = add_time_of_day_coding(offers_pdf)

    if of.include_schedule:
        cols_to_work_on = [
            c
            for c in offers_pdf.columns
            if not c == "jobStartDate"
            and not c == "price_cheapest"
            and not c == "user_created"
            and not c == "created"
        ]
    else:
        cols_to_work_on = [
            c
            for c in offers_pdf.columns
            if not c.startswith("schedule_")
            and not c == "jobStartDate"
            and not c == "price_cheapest"
            and not c == "user_created"
            and not c == "created"
        ]

    return offers_pdf, cols_to_work_on, query


def load_a_file_for_prediction(limit=0, offset=0, chid=None):
    """
    Load a file for prediction.

    Args:
        limit (int, optional): The maximum number of records to load. Defaults to 0.
        offset (int, optional): The starting index of the records to load. Defaults to 0.
        chid (str, optional): The chid value to filter the records. Defaults to None.

    Returns:
        tuple: A tuple containing two dataframes: 
            - df_o: The loaded offers data filtered by chid, limit, and offset.
            - load_wa_data(): The loaded wa data.
    """

    answ, _, _ = load_offers()  # Load the offers data
    df_o = answ

    if chid is not None:
        df_o = df_o[df_o.chid == chid]
        df_o = df_o.reset_index()

    if limit > 0:
        c = df_o.chid.unique()
        upper = offset + limit
        f = c[offset:upper]
        df_o = df_o[df_o.chid.isin(f)]
        df_o = df_o.reset_index()

    return df_o, load_wa_data()


def load_offers_from_file(b_save=False, b_partial=True):
    """
    Load flight offers from a file and perform optional data processing.

    Args:
        b_save (bool, optional): Whether to save the loaded offers to a file. Defaults to False.
        b_partial (bool, optional): Whether to filter out offers that have already been processed. 
        Defaults to True.

    Returns:
        pandas.DataFrame: The loaded flight offers.

    """
    df = spark.read.csv(_OFFERSFILE, header=True, inferSchema=True)
    offers = df.toPandas()

    if b_partial:
        full_uuid = pd.read_csv(_FULL_UIDS)
        offers = offers[~offers.uuid.isin(full_uuid.uuid)]

    if b_save:
        offers.to_csv(_OFFERS_FOR_DP_FILE, index=False)

    # Column renaming
    offers = offers.rename(columns=str.lower)
    offers = offers.rename(
        columns={
            "rq_dep_airport_or_citycode": "rq_dep_airport_code",
            "rq_arr_airport_or_citycode": "rq_arr_airport_code",
        }
    )
    return offers


if __name__ == "__main__":
    # Load the offers data
    data, cols, sql = load_offers()
    offers_final = data[cols]
