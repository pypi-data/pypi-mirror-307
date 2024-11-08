"""
This module provides a comprehensive set of functions to preprocess and manipulate
data using PySpark. It includes functions for handling categorical variables,
pivoting data frames, creating binary columns for top categories, executing complex
SQL queries for session retrieval, and writing results back to databases. These
functions are designed to be used within a Spark environment, leveraging Spark SQL
and DataFrame operations to process large datasets efficiently.

Key functionalities include:
- Encoding categorical variables.
- Pivoting DataFrame on specific columns.
- Handling special cases like UUIDs and CHIDs.
- Generating binary columns for the top n categories.
- Preprocessing steps that involve multiple transformations.
- Retrieving and sampling balanced or specific sessions from large datasets.
- Calculating ratios and performing conditional SQL queries.
"""

import math

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.window import Window

from pyspark.ml.feature import StringIndexer

from pyspark.sql.functions import col, expr


spark = SparkSession.builder.getOrCreate()


def pipeline_helper(data):
    """
    Apply transformations to a DataFrame to handle categorical variables, 
    create binary columns, and pivot data.

    Parameters:
        data (DataFrame): A PySpark DataFrame to transform.

    Returns:
        DataFrame: A transformed PySpark DataFrame.
    """

    # Handling Categorical Variables using StringIndexer
    categorical_columns = [t[0] for t in data.dtypes if t[1] == "string"]

    for c in categorical_columns:
        indexer = StringIndexer(inputCol=c, outputCol=f"{c}_coded")
        data = indexer.fit(data).transform(data)

    # Handling 'av' column creation
    data = data.withColumn("av", F.when(
        F.col("price").isNotNull(), 1).otherwise(0))

    # # Pivoting on alternatives
    alts = data.select("alt").distinct().rdd.flatMap(lambda x: x).collect()
    pivot_df = None
    for alt in alts:
        # Not dropping 'alt', just renaming columns accordingly
        tmp_df = data.filter(F.col("alt") == alt).select(
            [
                F.col(c).alias(f"{c}_{alt}") if c != "chid" else F.col(c)
                for c in data.columns
            ]
        )

        if pivot_df is None:
            pivot_df = tmp_df
        else:
            pivot_df = pivot_df.join(tmp_df, on="chid", how="outer")

    # Dropping the 'alt' columns
    for alt in alts:
        column_to_drop = f"alt_{alt}"
        if (
            column_to_drop in pivot_df.columns
        ):  # Checking if the column exists before dropping
            pivot_df = pivot_df.drop(column_to_drop)

    # Dropping unwanted columns at once
    columns_to_drop = []

    # Adding the column names to be dropped into a list
    for alt in [a for a in alts if a != 1]:
        columns_to_drop.append(f"chid_coded_{alt}")
        columns_to_drop.append(f"uuid_coded_{alt}")
        columns_to_drop.append(f"uuid_{alt}")

    # Dropping all the specified columns together
    pivot_df = pivot_df.drop(*columns_to_drop)

    # Renaming specific columns and keeping all the other columns
    final_df = (
        pivot_df.withColumnRenamed("uuid_1", "uuid_ref")
        .withColumnRenamed("uuid_coded_1", "uuid")
        .withColumnRenamed("chid", "chid_ref")
        .withColumnRenamed("chid_coded_1", "chid")
    )

    return final_df


def make_top_n_categories(data, c, n):
    """
    Enhance DataFrame by adding binary columns for the top 'n' categories of a specified column.

    Parameters:
        data (DataFrame): DataFrame to modify.
        c (str): Column name to process.
        n (int): Number of top categories to consider.

    Returns:
        DataFrame: DataFrame with added binary columns.
    """

    # Identifying the top n categories
    top_n_categories_df = data.groupBy(
        c).count().orderBy(F.desc("count")).limit(n)

    # Collecting the top n categories into a list
    top_n_categories = [row[0] for row in top_n_categories_df.collect()]

    # Binarizing the top n categories and creating new columns for each
    for category in top_n_categories:
        column_name = f"{c}_{category}"
        data = data.withColumn(
            column_name, F.when(F.col(c) == category, 1).otherwise(0)
        )

    # Creating an additional binary column for other categories not in the top n
    data = data.withColumn(
        f"{c}_Others", F.when(F.col(c).isin(
            top_n_categories), 0).otherwise(1)
    )

    return data


def preprocess_step_top_n(data):
    """
    Preprocess a DataFrame by applying make_top_n_categories and pipeline_helper sequentially.

    Parameters:
        data (DataFrame): DataFrame to preprocess.

    Returns:
        DataFrame: Preprocessed DataFrame.
    """

    offers_df = data.select(
        *(
            "uuid",
            "chid",
            "alt",
            "choice",
            "schedule_departure_DOW",
            "schedule_journey_time",
            "schedule_transfer_time",
            "schedule_distance",
            "schedule_number_of_legs",
            "rq_arr_airport_code",
            "rq_dep_airport_code",
            "number_of_ods",
            "round_trip",
            "trip_duration",
            "saturday_night",
            "price",
            "pax_count",
            "Dep_2pi_cos",
            "Dep_2pi_sin",
            "Dep_4pi_cos",
            "Dep_4pi_sin",
            "Dep_6pi_cos",
            "Dep_6pi_sin",
            "ndo",
            "od",
            "od_order",
        )
    )
    # offers_df = make_top_n_categories(offers_df, "rq_dep_airport_code", 20)
    offers_df = make_top_n_categories(offers_df, "od", 20)
    return pipeline_helper(data=offers_df)


def handle_columns(preprocessed_data_in_spark):
    """
    Select and prepare columns from a preprocessed DataFrame for further processing.

    Parameters:
        preprocessed_data_in_spark (DataFrame): Preprocessed DataFrame.

    Returns:
        list: List of original and newly prepared columns.
    """

    base_cols = {
        col.rsplit("_", 1)[0]
        for col in preprocessed_data_in_spark.columns
        if len(col.rsplit("_", 1)) > 1
        and col.rsplit("_", 1)[1].isdigit()
        and 1 <= int(col.rsplit("_", 1)[1]) <= 10
    }
    cols = [
        preprocessed_data_in_spark[col] for col in preprocessed_data_in_spark.columns
    ]
    new_cols = [F.lit(0).alias(base_col + "_0") for base_col in base_cols]
    return cols + new_cols


def calculate_chosen_alternative(df):
    """
    Assign 'chosenAlternative' based on 'choice_' columns in the DataFrame.

    Parameters:
        df (DataFrame): DataFrame with 'choice_' columns.

    Returns:
        tuple: A modified DataFrame and a list of choice columns.
    """

    # Find all choice columns
    choice_columns = [c for c in df.columns if c.startswith("choice_")]

    # Initialize 'chosenAlternative' to 0
    df = df.withColumn("chosenAlternative", col(choice_columns[0]) * 0)

    # Update 'chosenAlternative' based on the 'choice_' columns
    choice_expr = "CASE "
    for choice_col in choice_columns:
        # Extract the number after 'choice_'
        choice_num = choice_col.split("_")[-1]
        choice_expr += f"WHEN {choice_col} = 1 THEN {choice_num} "
    choice_expr += "ELSE chosenAlternative END"

    df = df.withColumn("chosenAlternative", expr(choice_expr))

    return df, choice_columns


def preprocess_step(table_in, table_out, no_wa=False):
    """
    Execute a comprehensive preprocessing on data from a table, 
    transforming and writing back to another table.

    Parameters:
        table_in (str): Input table name.
        table_out (str): Output table name.

    Returns:
        bool: True if processing completes successfully, otherwise an error is raised.
    """

    data_read_df = spark.read.table(table_in)
    data_read_df = data_read_df.withColumnRenamed(
        'daysinadvance_fulljourney_departure', 'ndo')
    preprocessed_data_in_spark = preprocess_step_top_n(data_read_df)

    all_cols = handle_columns(preprocessed_data_in_spark)
    offers_final = preprocessed_data_in_spark.select(*all_cols)
    offers_final = offers_final.fillna(0)
    offers_final, _ = calculate_chosen_alternative(offers_final)

    offers_final = offers_final.withColumn("av_0", F.lit(1))

    if no_wa:
        offers_final = offers_final.drop(
            *[c for c in offers_final.columns if c.endswith('_0')])

    offers_final.write.mode("overwrite").saveAsTable(table_out)

    return True


def get_sessions(table, limit=5000):
    """
    Retrieves sessions from a specified table with a total 'choice' equal to 1.

    Parameters:
        table (str): The name of the table to query.
        limit (int, optional): Maximum number of sessions to retrieve, default is 5000.

    Returns:
        DataFrame: A DataFrame containing the sessions that match the criteria.
    """

    stmnt = f"""
WITH POS_L AS (
    SELECT
        DISTINCT chid
    FROM
        {table}
    LIMIT
        {limit}
)
SELECT
a.*
FROM
{table} AS a
INNER JOIN POS_L as b 
ON a.chid = b.chid
    """

    return spark.sql(stmnt)


def get_balanced_sessions(table, limit=5000):
    """
    Retrieves a balanced sample of sessions based on 'choice' values from a specified table.

    Parameters:
        table (str): Name of the table.
        limit (int, optional): Maximum number of rows for each 'choice' category, default is 5000.

    Returns:
        DataFrame: A DataFrame containing a balanced sample of sessions.
    """

    stmnt = f"""
WITH SumChoice AS (
  SELECT chid, SUM(choice) as total_choice
  FROM {table}
  GROUP BY chid
)
, FilteredChoice1 AS (
  SELECT DISTINCT chid
  FROM SumChoice
  WHERE total_choice = 1
  ORDER BY RAND()
  LIMIT {limit}
)
, FilteredChoice0 AS (
  SELECT DISTINCT chid
  FROM SumChoice
  WHERE total_choice = 0
  ORDER BY RAND()
  LIMIT {limit}
)

(SELECT d.*
 FROM {table} d
 JOIN FilteredChoice1 f1 ON d.chid = f1.chid)

UNION ALL

(SELECT d.*
 FROM {table} d
 JOIN FilteredChoice0 f0 ON d.chid = f0.chid)
"""
    return spark.sql(stmnt)


def limit_the_choices(data, alternatives):
    """
    Limits the number of alternative choices in the dataset to enhance focus on relevant data.

    Parameters:
        data (DataFrame): Input Spark DataFrame.
        alternatives (int): Maximum number of alternatives to retain per session.

    Returns:
        DataFrame: A DataFrame with limited number of alternatives per session.
    """

    # Filter rows where choice is 0
    data_0 = data.filter(F.col("choice") == 0)

    # Group by "chid" and filter groups with length less than or equal to alternatives
    window = Window.partitionBy("chid")

    data_small = data_0.withColumn("group_size", F.count("*").over(window)).filter(
        F.col("group_size") < alternatives
    )

    # Group by "chid" and filter groups with length greater than alternatives
    data_0_aux = data_0.withColumn("group_size", F.count("*").over(window)).filter(
        F.col("group_size") >= alternatives
    )

    # Limit the nuber of alternatives
    window_spec = Window.partitionBy("chid").orderBy(F.col("alt"))
    # Add a row number column within each group
    data_0_aux = data_0_aux.withColumn(
        "row_number", F.row_number().over(window_spec))
    # Limit the number of rows per group
    limit_per_group = alternatives - 1
    data_sampled = data_0_aux.filter(F.col("row_number") <= limit_per_group).drop(
        "row_number"
    )

    # Filter rows where choice is 1
    data_chosen = data.filter(F.col("choice") == 1)

    data_small = data_small.drop("group_size")
    data_sampled = data_sampled.drop("group_size")
    data_sampled = data_sampled.select(*data_chosen.columns)

    # Union the DataFrames
    data = data_chosen.union(data_small).union(data_sampled)

    # Add the "alt" column based on the row number within each "chid" group
    data = data.withColumn("alt", F.row_number().over(
        window.orderBy(F.col("chid"))))

    # make sure not to include sessions with just 1 option
    data = data.withColumn("group_size", F.count("*").over(window)).filter(
        F.col("group_size") > 1
    )

    data = data.drop("group_size")

    return data


def sample_balanced(table_in, table_out, n, alternatives=10):
    """
    Samples a balanced dataset from an input table and writes it to an output table.

    Parameters:
    - table_in: str
        Name of the input table.
    - table_out: str
        Name of the output table to write the balanced dataset.
    - n: int
        The number of samples to extract.

    Returns:
    - DataFrame
        A Spark DataFrame containing the sampled data.
    """

    offers_final = get_balanced_sessions(table_in, n)
    offers_final = limit_the_choices(
        data=offers_final, alternatives=alternatives)
    offers_final.write.mode("overwrite").saveAsTable(table_out)
    return offers_final


def sample_sessions(table_in, table_out, n, alternatives=10):
    """
    Samples sessions from an input table, limits the number of choices, 
    and writes to an output table.

    Parameters:
        table_in (str): Input table name.
        table_out (str): Output table name.
        n (int): Number of sessions to sample.

    Returns:
        DataFrame: A DataFrame containing the sampled sessions.
    """

    offers_final = get_sessions(table_in, n)
    offers_final = limit_the_choices(
        data=offers_final, alternatives=alternatives)

    offers_final.write.mode("overwrite").saveAsTable(table_out)
    return offers_final


def get_positive_ratio(table_in):
    """
    Calculates the ratio of positive choices in the dataset.

    Parameters:
        table_in (str): Input table name.

    Returns:
        tuple: A tuple containing the positive ratio and total count of distinct 'chid'.
    """

    positive_count = spark.sql(
        f"""
        SELECT COUNT(DISTINCT chid) as cnt 
        FROM {table_in} 
        GROUP BY chid 
        HAVING SUM(choice) = 1
    """
    ).count()
    total_count = spark.table(table_in).select("chid").distinct().count()
    positive_ratio = positive_count / total_count
    return positive_ratio, total_count


def fetch_chids_to_avoid(table_avoid):
    """
    Fetches distinct 'chid' values from a specified table to avoid in further sampling.

    Parameters:
        table_avoid (str): Table name from which to fetch 'chid' values.

    Returns:
        list: List of distinct 'chid' values.
    """

    data_read_df = spark.read.table(table_avoid)
    distinct_chid_df = data_read_df.select("chid").distinct()
    return [row.chid for row in distinct_chid_df.rdd.collect()]


def sample_chids(table_in, n, total_count, positive_count):
    """
    Samples 'chid' values from the input table while avoiding certain specified 'chid's.
    The sampling is done based on certain conditions and calculations.

    Parameters:
    - table_in (str): Name of the input table
    - chid_str_to_avoid (str): String containing 'chid's to be avoided, separated by commas
    - n (int): Desired number of samples
    - total_count (int): Total count of distinct 'chid' in the table
    - positive_count (int): Count of positive instances based on some condition

    Returns:
    - list: A list of sampled 'chid' values
    """

    rows_to_get = math.ceil(n * (total_count / positive_count))
    sampled_chids_df = spark.sql(
        f"""
    WITH FilteredTable AS (
        SELECT chid
        FROM {table_in}
    )
    SELECT DISTINCT chid 
    FROM FilteredTable TABLESAMPLE ({rows_to_get} ROWS)
    """
    )
    return [row.chid for row in sampled_chids_df.rdd.collect()]


def sample_imbalanced(table_in, table_out, n=100, alternatives=10):
    """
    Samples an imbalanced dataset from an input table while considering 
    specified sessions to avoid, and writes the result to an output table.

    Parameters:
        table_in (str): Input table name.
        table_avoid (str): Table name containing sessions to avoid.
        table_out (str): Output table name.
        n (int, optional): Number of samples to extract, default is 100.
        alternatives (int, optional): Maximum number of alternatives to retain per session, 
        default is 10.

    Returns:
        dict: A dictionary containing the resulting DataFrame and a positive ratio.
    """

    positive_count = spark.sql(
        f"""
        SELECT COUNT(DISTINCT chid) as cnt 
        FROM {table_in} 
        GROUP BY chid 
        HAVING SUM(choice) = 1
    """
    ).count()
    total_count = spark.table(table_in).select("chid").distinct().count()
    positive_ratio = positive_count / total_count

    chid_list = sample_chids(
        table_in, n, total_count, positive_count
    )
    chid_str_to_select = ", ".join([f"'{chid}'" for chid in chid_list])

    sampled_df = spark.sql(
        f"""
    SELECT * FROM {table_in}
    WHERE chid IN ({chid_str_to_select})
    """
    )

    offers_final = limit_the_choices(
        data=sampled_df, alternatives=alternatives)
    offers_final.write.mode("overwrite").saveAsTable(table_out)

    return offers_final, positive_ratio


if __name__ == "__main__":
    TEST = "write your unit test"
    print(f"test {TEST}")
