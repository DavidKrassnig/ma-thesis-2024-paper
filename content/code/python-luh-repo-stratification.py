import os
import pandas as pd
import re

def read_csv_file(file_path):
    """
    Reads a CSV file into a Pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the CSV data.
    """
    return pd.read_csv(file_path, index_col=0)

def preprocess_data(df):
    """
    Deletes entries based on the specified criteria and normalizes values in the "dc.date.issued[]" column.

    Args:
        df (pandas.DataFrame): Input DataFrame.

    Returns:
        pandas.DataFrame: DataFrame with entries deleted based on criteria and "dc.date.issued[]" column normalized.
    """
    # Normalize values in "dc.date.issued[]" column to YYYY format
    df['dc.date.issued[]'] = pd.to_datetime(df['dc.date.issued[]'], errors='coerce').dt.year.astype('Int64')

    # Delete entries where "tib.date.embargoEnd[]" or "tib.description.embargoEnd[]" contains dates later than 2023-12-31
    df = df[~((pd.to_datetime(df['tib.date.embargoEnd[]'], errors='coerce') > pd.Timestamp('2023-12-31')) |
              (pd.to_datetime(df['tib.description.embargoEnd[]'], errors='coerce') > pd.Timestamp('2023-12-31')))]
    return df

def filter_dataframes(df, collection_strings):
    """
    Filters DataFrame into separate DataFrames based on collection strings.

    Args:
        df (pandas.DataFrame): Input DataFrame.
        collection_strings (list): List of strings to filter on.

    Returns:
        dict: Dictionary containing filtered DataFrames with collection strings as keys.
    """
    filtered_dfs = {}
    for collection_str in collection_strings:
        regex_str = re.escape(collection_str) + r"(?:\|\||$)"  # Regex pattern to match "123456789/X" followed by "||" or end of string
        filtered_dfs[collection_str] = df[df['collection'].str.contains(regex_str, regex=True)]
    return filtered_dfs

def filter_by_date_range(df):
    """
    Filters DataFrame into three separate DataFrames based on the value of "dc.date.issued[]".

    Args:
        df (pandas.DataFrame): Input DataFrame.

    Returns:
        dict: Dictionary containing filtered DataFrames grouped by date range.
    """
    date_range_dfs = {}
    date_range_dfs['2020-2023'] = df[df['dc.date.issued[]'].between(2020, 2023, inclusive='both')]
    date_range_dfs['2016-2019'] = df[df['dc.date.issued[]'].between(2016, 2019, inclusive='both')]
    date_range_dfs['2012-2015'] = df[df['dc.date.issued[]'].between(2012, 2015, inclusive='both')]
    return date_range_dfs

def write_dataframes_to_csv(dataframes, output_dir="./", prefix=None):
    """
    Writes each DataFrame to a separate CSV file.

    Args:
        dataframes (dict): Dictionary containing DataFrames to write.
        output_dir (str): Directory to save CSV files (default: current directory).
        prefix (str, optional): Prefix to prepend to file names (default: None).
    """
    for key, df in dataframes.items():
        if prefix is None:
            file_name = f"{key}.csv"
        else:
            file_name = f"{prefix}_{key}.csv"
        file_name = re.sub(r'[^\w.-]+', '_', file_name)
        file_path = os.path.join(output_dir, file_name)
        df.to_csv(file_path)
        print(f"DataFrame '{key}' saved to {file_path}")


def main():
    # Read the CSV file into a DataFrame
    file_path = "repo_luh_metadata_20240321T104153.csv"
    df = read_csv_file(file_path)

    # Preprocess data: Normalize values in "dc.date.issued[]" column and delete entries based on specified criteria
    df = preprocess_data(df)

    # Define collection strings for filtering
    collection_strings = [f"123456789/{i}" for i in range(2, 11)]

    # Filter DataFrame into separate DataFrames
    filtered_dfs = filter_dataframes(df, collection_strings)

    # Write filtered DataFrames to separate CSV files
    write_dataframes_to_csv(filtered_dfs,output_dir="./filtered_by_faculty/")

    # Filter each resulting DataFrame by date range and write to CSV
    for key, df in filtered_dfs.items():
        date_range_dfs = filter_by_date_range(df)
        write_dataframes_to_csv(date_range_dfs, output_dir="./filtered_by_faculty_and_year/", prefix=f"{key}")

if __name__ == "__main__":
    main()
