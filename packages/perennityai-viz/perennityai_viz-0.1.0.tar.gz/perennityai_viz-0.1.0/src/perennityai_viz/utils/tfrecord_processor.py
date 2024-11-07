
import os
import sys
import glob
import numpy as np
import tensorflow as tf

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from .feature_header import get_header

ALL_FEATURE_COLUMNS = get_header().split('\t')


class TFRecordProcessor:
    """
    A class for processing and managing TFRecord files for storing and reading landmark data 
    with optional conversion from CSV format.

    Attributes:
        input_file (str or list): Path to a single TFRecord file or list of file paths.
        input_path (str): Directory path containing TFRecord or CSV files.

    Methods:
        __init__(self, input_file='', input_path='', logger=None):
            Initializes the TFRecordReader with specified parameters and file paths.
        
    Raises:
        ValueError: If the TFRecord path does not exist, no TFRecord files are found, or if an invalid file format is provided.
    """

    def __init__(self, input_file='', input_path='', logger=None):
        """
        Initializes the TFRecordReader with necessary parameters for handling TFRecord data.

        Args:
            input_file (str, optional): Path to a single TFRecord file. Defaults to an empty string.
            input_path (str, optional): Path to a directory containing TFRecord or CSV files. Defaults to an empty string.
            logger (optional): Logger instance for logging. Defaults to None.

        Raises:
            ValueError: If the specified TFRecord path does not exist or no TFRecord files are found.
            ValueError: If an invalid file format is provided in `data_input_format`.
        """
        self.input_file = input_file
        self.file_pattern = None
        self.input_path = input_path
        self.logger = logger

        # Handling single TFRecord file or converting CSV path to TFRecord paths
        if os.path.isfile(input_file):
            self.input_file = [input_file]
            self.input_path = os.path.dirname(input_file)

        # Set up TFRecord path and file pattern
        if self.input_path:
            if os.path.exists(self.input_path):
                self.file_pattern = f'{self.input_path}/*.tfrecord'

                # Use glob to match files and verify
                self.input_file = glob.glob(self.file_pattern)
                if not self.input_file:
                    self.logger.debug(f"No TFRecord files found in {self.input_path}")

        # Define feature descriptions for TFRecord parsing
        self.feature_description = {COL: tf.io.VarLenFeature(dtype=tf.float32) for COL in ALL_FEATURE_COLUMNS}
        self.feature_description["phrase"] = tf.io.FixedLenFeature([], dtype=tf.string)

    def set_shape(self, num_features, channels):
        """
        Updates the shape configuration for features and channels.

        Args:
            num_features (int): The number of features per sample.
            channels (int): The number of channels per feature (e.g., x, y, z coordinates).

        Sets:
            self.num_features (int): Updates the number of features.
            self.channels (int): Updates the number of channels.
            self.total_num_features (int): Calculates and sets the total number of features,
                                           which is `num_features * channels`.
        """
        self.num_features = num_features
        self.channels = channels
        self.total_num_features = num_features * channels

    def set_input_file(self, input_file):
        """
        Sets the TFRecord file path and updates the file pattern.

        Args:
            input_file (str): Path to a single TFRecord file.

        Sets:
            self.input_file (str): Updates the path to the TFRecord file.
            self.file_pattern (list): Sets `file_pattern` to a list containing the `input_file`.
        """
        self.input_file = input_file
        self.file_pattern = [self.input_file]

    def set_tfrecord_path(self, tfrecord_path):
        """
        Sets the TFRecord directory path and updates the file pattern.

        Args:
            tfrecord_path (str): Path to the directory containing TFRecord files.

        Sets:
            self.input_path (str): Updates the path to the directory containing TFRecord files.
            self.file_pattern (str): Sets the `file_pattern` to match all TFRecord files 
                                      in the specified directory.
        """
        self.input_path = tfrecord_path
        self.file_pattern = f'{tfrecord_path}/*.tfrecord'
        # Use glob to match files and verify
        self.input_file = glob.glob(self.file_pattern)


    def decode_fn(self, record_bytes):
        """
        Decodes a single example from a serialized TFRecord file, parsing it into
        structured data for further processing.

        Parameters:
        ----------
        record_bytes : tf.Tensor
            A tensor containing serialized bytes from a TFRecord file.

        Returns:
        -------
        tuple
            A tuple with two elements:
            - landmarks : tf.Tensor
                A tensor containing the decoded landmark data, transposed to maintain
                the original shape for easy visualization or further processing.
            - phrase : tf.Tensor
                A tensor containing the decoded phrase label associated with the landmark data.
        
        Process:
        -------
        1. Parses the serialized `record_bytes` using the provided `feature_description`.
        2. Extracts and decodes the `phrase` feature.
        3. Converts the sparse tensors for each landmark in `ALL_FEATURE_COLUMNS` to dense tensors.
        4. Transposes the landmark tensor for proper shape alignment.
        
        Notes:
        ------
        - This method assumes `ALL_FEATURE_COLUMNS` and `self.feature_description` have been 
        predefined to align with the TFRecord schema.
        - Useful in data pipelines where landmark and phrase information are required for 
        visualization or model input.
        """
        features = tf.io.parse_single_example(record_bytes, self.feature_description)
        phrase = features["phrase"]
        landmarks = ([tf.sparse.to_dense(features[COL]) for COL in ALL_FEATURE_COLUMNS])
        # Transpose to maintain the original shape of landmarks data.
        landmarks = tf.transpose(landmarks)
        return landmarks, phrase


    def get_files(self):
        return self.input_file

    def get_dataset(self, input_file):
        """
        Loads and decodes a TFRecord dataset from the specified file.

        Parameters:
        ----------
        input_file : str
            The file path to the TFRecord file containing serialized dataset examples.

        Returns:
        -------
        tf.data.Dataset
            A `tf.data.Dataset` object where each entry is a tuple of:
            - landmarks : tf.Tensor
                The decoded landmark data, transposed to maintain the original shape.
            - phrase : tf.Tensor
                The phrase label associated with each set of landmark data.

        Process:
        -------
        1. Loads the raw dataset from the provided TFRecord file using `tf.data.TFRecordDataset`.
        2. Applies `self.decode_fn` to parse and decode each serialized example, using
        `num_parallel_calls=tf.data.AUTOTUNE` for efficient multi-threaded processing.
        3. Returns the decoded dataset ready for further processing or training.

        Notes:
        ------
        - This method assumes that `self.decode_fn` and `self.feature_description` are 
        appropriately defined to match the TFRecord schema.
        - Designed to handle large datasets efficiently by leveraging TensorFlow's 
        `tf.data` API for seamless data loading and decoding.
        """
        raw_dataset = tf.data.TFRecordDataset(input_file)

        # Decode using self.decode_fn for each example
        dataset = raw_dataset.map(self.decode_fn, num_parallel_calls=tf.data.AUTOTUNE)
        
        return dataset


    def write_dataset_to_tfrecord(self, train_ds, tfrecord_path):
        """
        Saves the dataset to the specified path using the updated tf.data.Dataset.save method.
    
        Args:
            train_ds (tf.data.Dataset): The dataset to be saved.
            tfrecord_path (str): The path where the dataset should be saved.
        """
        # Save the dataset using the new tf.data.Dataset.save method
        train_ds.save(tfrecord_path)
        self.logger.debug(f"Dataset saved to {tfrecord_path}")
    
    def read_tfrecord_to_dataset(self, tfrecord_path):
        """
        Loads the dataset from the specified path using the updated tf.data.Dataset.load method.
    
        Args:
            tfrecord_path (str): The path where the dataset is saved.
    
        Returns:
            tf.data.Dataset: The loaded dataset.
        """
        # Load the dataset using the new tf.data.Dataset.load method
        dataset = tf.data.Dataset.load(tfrecord_path)
    
        # Iterate over the dataset to print shapes
        for landmark, target, label in dataset.take(1):  # Take one batch to show shapes
            self.logger.debug(f"Landmark shape: {landmark.shape}, Target shape: {target.shape}, Label shape: {label.shape}")
            pass
    
        return dataset
    
    def write_df_to_tfrecord(self, tf_file, frames_df):
        # Make a copy of the DataFrame
        seq_df = frames_df.copy()
        phrase = frames_df.at[0, 'phrase']

        # Filter out unwanted columns that start with specific prefixes
        seq_df = seq_df.filter(regex='^(?!sequence_id)')
        seq_df = seq_df.filter(regex='^(?!phrase)')
        seq_df = seq_df.filter(regex='^(?!context)')

        missing_columns = [col for col in ALL_FEATURE_COLUMNS if col not in frames_df.columns]
        if missing_columns:
            raise ValueError(f"Missing columns : {missing_columns}")

        # Reorder columns based on a predefined order in `ALL_FEATURE_COLUMNS`
        seq_df = seq_df[ALL_FEATURE_COLUMNS]

        # Ensure the target TFRecord file path exists
        if not os.path.exists(tf_file):
            # Write processed data to TFRecord
            with tf.io.TFRecordWriter(tf_file) as file_writer:
                # Loop through each row of the DataFrame and write as TFRecord
                for idx, (seq_id, phrase) in enumerate(zip(frames_df.sequence_id, frames_df.phrase)):
                    print(f"Processing sequence {idx}, phrase: {phrase}")  # Check if loop runs
                    try:
                        frames_np = seq_df.to_numpy()
                        features = {ALL_FEATURE_COLUMNS[i]: tf.train.Feature(
                            float_list=tf.train.FloatList(value=frames_np[:, i])) for i in range(len(ALL_FEATURE_COLUMNS))}
                        features["phrase"] = tf.train.Feature(bytes_list=tf.train.BytesList(value=[bytes(phrase, 'utf-8')]))
                        
                        record_bytes = tf.train.Example(features=tf.train.Features(feature=features)).SerializeToString()
                        file_writer.write(record_bytes)
                        print("Record written.")
                    except Exception as e:
                        print("Error in serialization:", e)

