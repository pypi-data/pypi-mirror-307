import os
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from concurrent.futures import ThreadPoolExecutor

class CSVHandler:
    def __init__(self,  encoding='ISO-8859-1', max_workers=4, chunk_size=150000, logger=None):
        self.encoding =  encoding
        self.chunk_size = chunk_size
        self.max_workers = max_workers  # Maximum number of threads
        self.logger=logger

    def read_csv_file(self, csv_file, usecols=[]):
        """
        Read a CSV file and return its contents as a pandas DataFrame.

        This method uses the ISO-8859-1 encoding, which is suitable for most
        Western European languages and can handle some special characters.

        Args:
            csv_file (str): The path to the CSV file to be read.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from the CSV file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            pd.errors.EmptyDataError: If the file is empty.
            pd.errors.ParserError: If the file is not a valid CSV.
        """
        try:
            if not usecols:
                return pd.read_csv(csv_file, encoding=self.encoding)
            else:
                return pd.read_csv(csv_file, usecols=usecols, encoding=self.encoding)
        except pd.errors.EmptyDataError:
            print(f"The CSV file is empty or has no columns. {csv_file}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_parquet_file(self, file_path, columns=[]):
        """
        Reads a Parquet file and returns a DataFrame.

        Parameters:
        file_path (str): The path to the Parquet file.

        Returns:
        pd.DataFrame: A DataFrame containing the data from the Parquet file.
        """
        try:
            #df = pd.read_parquet(file_path, columns=columns, engine='pyarrow')
            parquet_df = pq.read_table(file_path, columns=columns).to_pandas()
            return parquet_df
        except Exception as e:
            print(f"Error reading the Parquet file: {e}")
            raise ValueError(f"Could not read file {file_path}")


    def read_parquet_file(self, file_path, columns=[]):
        """
        Reads a Parquet file and returns a DataFrame.

        Parameters:
        file_path (str): The path to the Parquet file.

        Returns:
        pd.DataFrame: A DataFrame containing the data from the Parquet file.
        """
        try:
            #df = pd.read_parquet(file_path, columns=columns, engine='pyarrow')
            parquet_df = pq.read_table(file_path, columns=columns).to_pandas()
            return parquet_df
        except Exception as e:
            print(f"Error reading the Parquet file: {e}")
            raise ValueError(f"Could not read file {file_path}")
            
    def write_parquet_file(self, df, output_file, encoding_col=[]):
        if encoding_col:        
            # Apply encoding to specified string columns
            for col in encoding_col:
                df[col] = df[col].astype(str).str.encode(self.encoding).str.decode(self.encoding)
        
        # Create a ParquetWriter outside the loop for appending
        with pq.ParquetWriter(output_file, pa.Table.from_pandas(df.iloc[0:1]).schema, compression='snappy') as writer:
            # Write the DataFrame to a Parquet file in chunks
            for i in range(0, len(df), self.chunk_size):
                chunk = df.iloc[i:i + self.chunk_size]
                table = pa.Table.from_pandas(chunk)
                writer.write_table(table)
        print("Successfully written : ", os.path.basename(output_file))