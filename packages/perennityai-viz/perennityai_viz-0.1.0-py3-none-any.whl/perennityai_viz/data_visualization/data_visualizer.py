import os
import cv2
import glob
import json
import pandas as pd
import numpy as np
import mediapipe
import tensorflow as tf

from mediapipe.framework.formats import landmark_pb2
from matplotlib.animation import PillowWriter
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.animation import FuncAnimation
from perennityai_viz.utils import TFRecordProcessor
from perennityai_viz.utils import CSVHandler
from perennityai_viz.utils import Log
from perennityai_viz.utils import get_header

header = get_header().split('\t')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


mp_pose = mediapipe.solutions.pose
mp_hands = mediapipe.solutions.hands
mp_face_mesh = mediapipe.solutions.face_mesh
mp_drawing = mediapipe.solutions.drawing_utils
mp_drawing_styles = mediapipe.solutions.drawing_styles

# Animation setup
rc('animation', html='jshtml')

# Increase the animation embed limit to, for example, 50MB
plt.rcParams['animation.embed_limit'] = 50 * 1024 * 1024  # 50 MB

class DataVisualizer:
    """
    The DataVisualizer class handles and validates dataset files in CSV or TFRecord formats,
    prepares them for visualization, and initializes the appropriate processing pipeline.
    
    Attributes:
        input_file (str): Path to a single input data file (CSV or TFRecord).
        input_dir (str): Path to a directory containing input data files (CSV or TFRecord).
        output_dir (str): Directory path where processed data and animations will be saved.
        data_input_format (str): The format of the input data files, either 'csv' or 'tfrecord'.
        logger (Logger): Optional logger instance for logging information or errors.
        dataset_path (str): Path to the dataset directory if input_dir is specified.
        output_dir (str): Output directory path for animations created during processing.
        tf_dataset_files (list): List of TFRecord files if the dataset format is TFRecord.
        csv_dataset_files (list): List of CSV files if the dataset format is CSV.
        parquet_dataset_files (list): List of Parquet files if the dataset format is Parquet.
        tfrecord_processor (TFCSVRecordProcessor): Instance of TFCSVRecordProcessor for data handling.
        
    Methods:
        __init__(self, input_file='', input_dir='', output_dir='', logger=None,verbose='csv'):
            Initializes the DataVisualizer with paths for input, output, and data format configuration.
        
    Raises:
        ValueError: If required paths (input file, input directory, or output directory) are not provided.
        ValueError: If no valid input files are found in the input directory.
    """
    
    def __init__(self, input_file='', input_dir='', output_dir='', encoding='', verbose='INFO'):
        """
        Initializes the DataVisualizer with the specified input file or directory, output directory,
        and data input format. Validates paths and sets up the output directory structure. If no valid
        files are found, raises a ValueError.

        Args:
            input_file (str): Path to a specific input file (CSV or TFRecord).
            input_dir (str): Path to a directory containing input data files.
            output_dir (str): Directory path where processed data and visualizations will be saved.
            data_input_format (str): Format of input data files ('csv' or 'tfrecord'). Defaults to 'csv'.
            logger (Logger, optional): Logger instance for logging activities. Defaults to None.

        Raises:
            ValueError: If neither input file nor input directory is valid.
            ValueError: If the output directory does not exist.
            ValueError: If no valid files are found in the specified input directory.
        """
        self.input_file = input_file
        self.input_dir = input_dir
        

        self.logger = Log(log_file=os.path.join(output_dir,  f"data_visualizer.log"), verbose=verbose)
        

        # Validate input and output paths
        if not os.path.exists(input_file) and not os.path.exists(input_dir):
            raise ValueError("Please, provide input file or input path!")
        
        if not os.path.exists(output_dir):
            raise ValueError("Please, provide output_dir!")
        # Join after verification
        self.output_dir = os.path.join(output_dir, 'animations')
        # Ensure Path
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize input and output paths based on input format
        if os.path.exists(input_dir):

            # Collect files based on specified data format
            self.tf_dataset_files = glob.glob(f'{self.input_dir}/*.tfrecord')

            self.csv_dataset_files = glob.glob(f'{self.input_dir}/*.csv')

            self.parquet_dataset_files = glob.glob(f'{self.input_dir}/*.parquet')
            
            # Check for valid files
            if len(self.csv_dataset_files) == 0 and len(self.tf_dataset_files) == 0 and len(self.parquet_dataset_files) == 0:
                raise ValueError("The input directory is empty!")
        
        elif '.tfrecord' in input_file and os.path.exists(input_file):
            self.tf_dataset_files = [input_file]
        elif '.csv' in input_file and os.path.exists(input_file):
            self.csv_dataset_files = [input_file]
        elif '.parquet' in input_file and os.path.exists(input_file):
            self.parquet_dataset_files = [input_file]
        else:
            raise ValueError(f"Please provide valid input! input_dir: {self.input_dir},  input_file:{self.input_file}")
        
        self.csv = CSVHandler(encoding=encoding)
        self.tfrecord_processor = TFRecordProcessor(input_file=input_file, input_path=self.input_dir, logger=self.logger)

        self.logger.debug("input_file : ", self.input_file)
        self.logger.debug("input_dir : ", self.input_dir)
        self.logger.debug("output_dir : ", self.output_dir)
        
    @classmethod
    def from_pretrained(cls, config):
        """
        Loads a pretrained configuration for initializing a DataVisualizer instance.

        Args:
            config_path (str): Path to the JSON file containing the configuration.

        Returns:
            DataVisualizer: An instance initialized with pretrained configurations.
        """
        if not os.path.isfile(config) or not isinstance(config, dict):
            raise FileNotFoundError(f"No configuration file found at {config}")

        if not isinstance(config, dict):
            with open(config, "r") as file:
                config = json.load(file)
        
        return cls(
            input_file=config.get('input_file', ''),
            input_dir=config.get('input_dir', ''),
            output_dir=config.get('output_dir', ''),
            data_input_format=config.get('data_input_format', 'csv'),
            encoding=config.get('encoding','ISO-8859-1'),
            verbose=config.get('verbose','INFO')
        )

    def get_hands(self, seq_df):
        """
        Extracts hand landmarks from a DataFrame and generates annotated images for both hands.

        Args:
            seq_df (pandas.DataFrame): A DataFrame containing hand landmark data, with columns for x, y, and z coordinates 
                                    of both the right and left hands.

        Returns:
            tuple: A tuple containing:
                - images (list of list of numpy.ndarray): A list of lists, where each inner list contains two annotated images 
                showing the right and left hand landmarks, respectively.
                - all_hand_landmarks (list of list of landmark_pb2.NormalizedLandmarkList): A list of lists containing 
                hand landmarks for both hands for each frame.

        Raises:
            ValueError: If seq_df does not contain any hand data for either hand.
        """
        images = []
        all_hand_landmarks = []

        if seq_df.empty:
            raise ValueError("The input DataFrame is empty.")

        for seq_idx in range(len(seq_df)):
            # Extract right hand landmarks
            x_hand = seq_df.iloc[seq_idx].filter(regex="x_right_hand.*").values
            y_hand = seq_df.iloc[seq_idx].filter(regex="y_right_hand.*").values
            z_hand = seq_df.iloc[seq_idx].filter(regex="z_right_hand.*").values

            right_hand_image = np.zeros((600, 600, 3))
            right_hand_landmarks = landmark_pb2.NormalizedLandmarkList()
            right_len = 0
            
            for x, y, z in zip(x_hand, y_hand, z_hand):
                right_hand_landmarks.landmark.add(x=x, y=y, z=z)
                right_len += 1
            self.logger.debug('right_hand_landmarks: %d', right_len)

            # Draw right hand landmarks
            mp_drawing.draw_landmarks(
                right_hand_image,
                right_hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())

            # Extract left hand landmarks
            x_hand = seq_df.iloc[seq_idx].filter(regex="x_left_hand.*").values
            y_hand = seq_df.iloc[seq_idx].filter(regex="y_left_hand.*").values
            z_hand = seq_df.iloc[seq_idx].filter(regex="z_left_hand.*").values

            left_hand_image = np.zeros((600, 600, 3))
            left_hand_landmarks = landmark_pb2.NormalizedLandmarkList()
            left_len = 0
            
            for x, y, z in zip(x_hand, y_hand, z_hand):
                left_hand_landmarks.landmark.add(x=x, y=y, z=z)
                left_len += 1
            self.logger.debug('left_hand_landmarks: %d', left_len)

            # Draw left hand landmarks
            mp_drawing.draw_landmarks(
                left_hand_image,
                left_hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style())

            # Append images and landmarks to the results
            images.append([right_hand_image.astype(np.uint8), left_hand_image.astype(np.uint8)])
            all_hand_landmarks.append([right_hand_landmarks, left_hand_landmarks])

        return images, all_hand_landmarks


    def get_face(self, seq_df):
        """
        Extracts face landmarks from a DataFrame and generates annotated images.

        Args:
            seq_df (pandas.DataFrame): A DataFrame containing face landmark data, with columns for x, y, and z coordinates.

        Returns:
            tuple: A tuple containing:
                - images (list of numpy.ndarray): A list of annotated images showing the face landmarks.
                - all_face_landmarks (list of landmark_pb2.NormalizedLandmarkList): A list of face landmarks for each frame.

        Raises:
            ValueError: If seq_df does not contain any face data.
        """
        images = []
        all_face_landmarks = []
        
        if seq_df.empty:
            raise ValueError("The input DataFrame is empty.")
        
        for seq_idx in range(len(seq_df)):
            x_face = seq_df.iloc[seq_idx].filter(regex="x_face.*").values
            y_face = seq_df.iloc[seq_idx].filter(regex="y_face.*").values
            z_face = seq_df.iloc[seq_idx].filter(regex="z_face.*").values

            annotated_image = np.zeros((600, 600, 3))

            face_landmarks = landmark_pb2.NormalizedLandmarkList()
            i = 0
            for x, y, z in zip(x_face, y_face, z_face):
                face_landmarks.landmark.add(x=x, y=y, z=z)
                i += 1
            self.logger.debug('face_landmarks: %d', i)

            # Draw face mesh tessellation
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
            
            # Draw face mesh contours
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

            images.append(annotated_image.astype(np.uint8))
            all_face_landmarks.append(face_landmarks)

        return images, all_face_landmarks

    def get_pose(self, seq_df):
        """
        Extracts pose landmarks from a DataFrame and generates annotated images.

        Args:
            seq_df (pandas.DataFrame): A DataFrame containing pose landmark data, with columns for x, y, and z coordinates.

        Returns:
            tuple: A tuple containing:
                - images (list of numpy.ndarray): A list of annotated images showing the pose landmarks.
                - all_pose_landmarks (list of landmark_pb2.NormalizedLandmarkList): A list of pose landmarks for each frame.

        Raises:
            ValueError: If seq_df does not contain any pose data.
        """
        images = []
        all_pose_landmarks = []
        
        if seq_df.empty:
            raise ValueError("The input DataFrame is empty.")
        
        for seq_idx in range(len(seq_df)):
            x_pose = seq_df.iloc[seq_idx].filter(regex="x_pose.*").values
            y_pose = seq_df.iloc[seq_idx].filter(regex="y_pose.*").values
            z_pose = seq_df.iloc[seq_idx].filter(regex="z_pose.*").values

            annotated_image = np.zeros((600, 600, 3))

            data_points = []
            i = 0
            for x, y, z in zip(x_pose, y_pose, z_pose):
                data_points.append(np.array([x, y, z]))
                i += 1
            self.logger.debug('pose_landmarks: %d', i)

            pose_landmarks = landmark_pb2.NormalizedLandmarkList()
            for row in data_points:
                pose_landmarks.landmark.add(x=row[0], y=row[1], z=row[2])

            mp_drawing.draw_landmarks(
                annotated_image,
                pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            
            images.append(annotated_image.astype(np.uint8))
            all_pose_landmarks.append(pose_landmarks)

        return images, all_pose_landmarks


    def create_animation(self, images, title=''):
        """
        Creates an animation from a sequence of images.

        Args:
            images (list of numpy.ndarray): A list of images (as NumPy arrays) to include in the animation.
            title (str, optional): The title to display on each frame of the animation. Default is an empty string.

        Returns:
            FuncAnimation: An animation object that can be displayed or saved.

        Raises:
            ValueError: If the images list is empty.
        """
        if not images:
            raise ValueError("The images list cannot be empty.")

        bg_color = '#030012'
        fig = plt.figure(figsize=(8, 8)) # Set the figure size with width and height (in inches)
        fig.patch.set_facecolor(bg_color)  # Set figure background color (light gray here)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        ax.set_facecolor(bg_color)         # Set axis background color (light blue here)
        fig.add_axes(ax)
        im = ax.imshow(images[0])
        plt.close(fig)

        # Function to update each frame
        def animate_func(i):
            ax.clear()  # Clear previous image before drawing new one
            ax.imshow(images[i], animated=True)
            ax.set_title(title)  # Set the title for each frame
            return [ax]

        return FuncAnimation(fig, animate_func, frames=len(images), interval=1000/10)


    def resize_image(self, image, size):
        """
        Resizes the given image to the specified dimensions.

        Args:
            image (numpy.ndarray): The input image to resize. Must be in the form of a NumPy array.
            size (tuple): A tuple (width, height) specifying the new size for the image.

        Returns:
            numpy.ndarray: The resized image as a NumPy array.

        Raises:
            ValueError: If the input image is not a valid NumPy array or if size is not a tuple.
        """
        return cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    def combine_images(self, right_hand_images, left_hand_images, face_images, pose_images):
        """
        Combines images of right hand, left hand, face, and body pose into a single image for each set of images.

        Args:
            right_hand_images (list of numpy.ndarray): List of images depicting the right hand landmarks.
            left_hand_images (list of numpy.ndarray): List of images depicting the left hand landmarks.
            face_images (list of numpy.ndarray): List of images depicting face landmarks.
            pose_images (list of numpy.ndarray): List of images depicting body pose landmarks.

        Returns:
            list of numpy.ndarray: A list of combined images, each containing the overlaid right hand, left hand, face, 
                                and pose images, resized to the target dimensions.

        Raises:
            ValueError: If the lengths of the input image lists do not match.
        """
        combined_images = []
        target_size = (1280, 720)  # Ensure all images are resized to this target size

        # Check if all input lists are of the same length
        if not (len(right_hand_images) == len(left_hand_images) == len(face_images) == len(pose_images)):
            raise ValueError("All input image lists must have the same length.")

        for idx, (rh_img, lh_img, face_img, pose_img) in enumerate(zip(right_hand_images, left_hand_images, face_images, pose_images)):
            
            # Resize images to the target size
            rh_img_resized = self.resize_image(rh_img, target_size)
            lh_img_resized = self.resize_image(lh_img, target_size)
            face_img_resized = self.resize_image(face_img, target_size)
            pose_img_resized = self.resize_image(pose_img, target_size)

            # Create a blank image for the combined output
            combined_image = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)

            # Overlay each image onto the blank image
            combined_image = cv2.addWeighted(combined_image, 1.0, rh_img_resized, 1.0, 0)
            combined_image = cv2.addWeighted(combined_image, 1.0, lh_img_resized, 1.0, 0)
            combined_image = cv2.addWeighted(combined_image, 1.0, face_img_resized, 1.0, 0)
            combined_image = cv2.addWeighted(combined_image, 1.0, pose_img_resized, 1.0, 0)

            # Append the combined image to the result list
            combined_images.append(combined_image)

        return combined_images


    def remove_sample_by_index(self, file_index):
        """
        Removes a sample file from the dataset based on its index in the tf_dataset_files list.

        Args:
            file_index (int): The index of the file to be removed from the tf_dataset_files list.

        Raises:
            IndexError: If the file_index is out of range for the tf_dataset_files list.
            FileNotFoundError: If the file specified by file_index does not exist.

        Logs:
            Information about the removal operation using the provided logger.
        """
        file_path = self.tf_dataset_files[file_index]
        os.remove(file_path)
        self.logger.info(f"File {file_path} removed successfully.")


    def read_tfrecord_as_df(self, tfrecord_file):
        """
        Reads a TFRecord file and returns its contents as a DataFrame.

        Args:
            tfrecord_file (str): The path to the TFRecord file to be read.

        Returns:
            tuple: A tuple containing:
                - pandas.DataFrame: A DataFrame containing the decoded landmarks from the TFRecord file.
                - str: The phrase associated with the first entry in the TFRecord file.

        Raises:
            ValueError: If the TFRecord file is invalid or cannot be processed.

        This method utilizes the TFCSVRecordProcessor to extract the dataset from the provided TFRecord file.
        It iterates through the dataset to collect landmarks and phrases, storing them in lists which are
        then converted into a DataFrame.
        """
        # Read the TFRecord file
        self.tfrecord_processor.set_tfrecord_path(tfrecord_file)
        dataset = self.tfrecord_processor.get_dataset(tfrecord_file)

        phrase_list = []
        landmarks_list = []
        
        # Iterate over the decoded dataset and check for missing or empty features
        for landmarks, phrase in dataset:
            phrase_list.append(phrase)
            landmarks_list.append(landmarks)
        
        landmark_tf = tf.concat(landmarks_list, axis=0)
        self.logger.debug("tf to dr landmark shape : ", landmark_tf.shape)

        phrase = phrase_list[0].numpy().decode('utf-8')
        landmarks = pd.DataFrame(landmark_tf.numpy(), columns=header)
        return landmarks, phrase

    def read_tf_sample_file_with_index(self, file_index=0):
        """
        Reads a sample TFRecord file at a specified index and returns its contents.

        Args:
            file_index (int, optional): The index of the TFRecord file to read. 
                Defaults to 0, which reads the first file in the list.

        Returns:
            tuple: A tuple containing:
                - pandas.DataFrame: A DataFrame containing the decoded landmarks from the TFRecord file.
                - str: The phrase associated with the TFRecord entry.

        This method retrieves the TFRecord file path using the provided index,
        logs the action, and then reads the file using the `read_tfrecord_as_df` method.
        """
        sample_file = f'{self.tf_dataset_files[file_index]}'
        self.logger.debug('Reading : ', sample_file)

        return self.read_tfrecord_as_df(sample_file)


    def read_csv_sample_file_with_index(self, file_index=0):
        """
        Reads a sample CSV file at a specified index and returns its contents.

        Args:
            file_index (int, optional): The index of the CSV file to read. 
                Defaults to 0, which reads the first file in the list.

        Returns:
            tuple: A tuple containing:
                - pandas.DataFrame: A DataFrame containing the data from the CSV file.
                - str: The phrase associated with the CSV entry.

        This method retrieves the CSV file path using the provided index,
        logs the action, and then reads the file using the `read_csv` method.
        """
        sample_file = f'{self.csv_dataset_files[file_index]}'
        
        self.logger.debug('Reading : ', sample_file)
        return self.read_csv(sample_file)
    
    def read_parquet_sample_file_with_index(self, file_index=0):
        """
        Reads a sample parquet file at a specified index and returns its contents.

        Args:
            file_index (int, optional): The index of the parquet file to read. 
                Defaults to 0, which reads the first file in the list.

        Returns:
            tuple: A tuple containing:
                - pandas.DataFrame: A DataFrame containing the data from the parquet file.
                - str: The phrase associated with the parquet entry.

        This method retrieves the parquet file path using the provided index,
        logs the action, and then reads the file using the `read_csv` method.
        """
        sample_file = f'{self.parquet_dataset_files[file_index]}'
        
        self.logger.debug('Reading : ', sample_file)
        return self.read_parquet(sample_file)
    
    def read_parquet(self, parquet_file):
        """
        Reads a parquet file and extracts landmark data and an associated phrase.

        Args:
            parquet_file (str): The path to the parquet file to be read.

        Returns:
            tuple: A tuple containing:
                - pandas.DataFrame: A DataFrame with landmark data, excluding specified columns.
                - str: The phrase associated with the first entry in the parquet.

        This method loads the parquet file into a pandas DataFrame, retrieves the phrase from the first row,
        and removes any columns that are not relevant to the landmark data. 
        The resulting DataFrame is cast to float32 for consistency.
        """
        # Read the CSV file into a DataFrame
        seq_df = self.csv.read_parquet_file(parquet_file, columns=['phrase'] + header)
        phrase = seq_df.iloc[0]['phrase']

        self.logger.debug("index ", seq_df.index)
        
        # Delete columns that start with the following
        seq_df = seq_df.filter(regex='^(?!frame)')
        seq_df = seq_df.filter(regex='^(?!phrase)')
        seq_df = seq_df.filter(regex='^(?!context)')

        landmarks = seq_df.astype(np.float32)

        return landmarks, phrase


    def read_csv(self, csv_file):
        """
        Reads a CSV file and extracts landmark data and an associated phrase.

        Args:
            csv_file (str): The path to the CSV file to be read.

        Returns:
            tuple: A tuple containing:
                - pandas.DataFrame: A DataFrame with landmark data, excluding specified columns.
                - str: The phrase associated with the first entry in the CSV.

        This method loads the CSV file into a pandas DataFrame, retrieves the phrase from the first row,
        and removes any columns that are not relevant to the landmark data. 
        The resulting DataFrame is cast to float32 for consistency.
        """
        # Read the CSV file into a DataFrame
        seq_df = self.csv.read_csv_file(csv_file)

        # Use for testing parquest and tfrecord
        # self.csv.write_parquet_file(seq_df, csv_file.replace(".csv", '.parquet'))
        # print(list(seq_df.columns))
        # seq_df['sequence_id'] = 1
        # self.tfrecord_processor.write_df_to_tfrecord(csv_file.replace(".csv", '.tfrecord'), seq_df)
        
        phrase = seq_df.iloc[0]['phrase']
        self.logger.debug("index ", seq_df.index)
        
        # Delete columns that start with the following
        seq_df = seq_df.filter(regex='^(?!frame)')
        seq_df = seq_df.filter(regex='^(?!phrase)')
        seq_df = seq_df.filter(regex='^(?!context)')

        landmarks = seq_df.astype(np.float32)

        return landmarks, phrase


    def visualize_data(self, csv_file=None, tfrecord_file=None, parquet_file=None, tf_file_index=-1, csv_file_index=-1, parquet_file_index=-1, animation_name='', write=False, output_format='.gif'):
        """
        Generates a visual animation of hand, face, and body poses from a specified CSV or TFRecord file. 

        This method allows visualization of sample files in the dataset. It combines frames of 
        right and left hands, face, and body poses into an animation, which can optionally be saved 
        in the output directory.

        Args:
            csv_file (str, optional): Path to a CSV file to visualize. Defaults to None.
            tfrecord_file (str, optional): Path to a TFRecord file to visualize. Defaults to None.
            tf_file_index (int, optional): Index of the TFRecord file to read from the dataset path.
            csv_file_index (int, optional): Index of the CSV file to read from the dataset path.
            parquet_file  (int, optional): Index of the parquet_file file to read from the dataset path.
            parquet_file_index (int, optional): Index of the parquet file to read from the dataset path.
            animation_name (str, optional): Custom name for the animation file. Defaults to ''.
            write (bool, optional): Whether to save the animation to the filesystem. Defaults to False.
            output_format (str, optional): The output format for the animation file (e.g., '.gif'). Defaults to '.gif'.

        Returns:
            matplotlib.animation.Animation: The generated animation showing the hand, face, and body poses.

        Raises:
            ValueError: If no valid input file is provided (csv_file, tfrecord_file, or file index).

        Examples:
            # Example with CSV file by index
            animation = data_visualizer.visualize_data(
                csv_file_index=0,
                animation_name='sample_animation',
                write=True
            )
            
            # Example with a specific TFRecord file
            animation = data_visualizer.visualize_data(
                tfrecord_file='path/to/sample.tfrecord',
                write=False
            )
        """
        input_file = csv_file if csv_file else tfrecord_file
        input_file = input_file if input_file else self.input_file
        self.logger.info("Started processing : ",  input_file)
        
        # Set the animation name if not provided
        if animation_name == '':
            animation_name = 'animation'
        if output_format == '':
            output_format = '.gif'

        # Read the specified data file
        if tf_file_index >= 0:
            seq_df, phrase = self.read_tf_sample_file_with_index(file_index=tf_file_index)
            sample_file = f'{self.tf_dataset_files[tf_file_index]}'
            animation_name = os.path.splitext(os.path.basename(sample_file))[0]
        elif csv_file_index >= 0:
            seq_df, phrase = self.read_csv_sample_file_with_index(file_index=csv_file_index)
            sample_file = f'{self.csv_dataset_files[csv_file_index]}'
            animation_name = os.path.splitext(os.path.basename(sample_file))[0]
        elif parquet_file_index >=0:
            seq_df, phrase = self.read_parquet_sample_file_with_index(file_index=parquet_file_index)
            sample_file = f'{self.parquet_dataset_files[parquet_file_index]}'
            animation_name = os.path.splitext(os.path.basename(sample_file))[0]
        elif tfrecord_file is not None:
            if '.tfrecord' in self.input_file and not tfrecord_file:
                tfrecord_file = self.input_file
            seq_df, phrase = self.read_tfrecord_as_df(tfrecord_file)
            animation_name = os.path.basename(tfrecord_file).replace('.tfrecord', '')
        elif csv_file is not None:
            if '.csv' in self.input_file and not csv_file:
                csv_file = self.input_file
            seq_df, phrase = self.read_csv(csv_file)
            animation_name = os.path.basename(csv_file).replace('.csv', '')
        elif parquet_file is not None:
            if '.parquet' in self.input_file and not parquet_file:
                parquet_file = self.input_file
            seq_df, phrase = self.read_parquet(parquet_file)
            animation_name = os.path.basename(csv_file).replace('.parquet', '')
        else:
            raise ValueError("Either file_index or tfrecord or df must be provided")

        animation_name = animation_name + output_format

        # Generate hand pose images
        hand_images, _ = self.get_hands(seq_df)
        right_hand_images = np.array(hand_images)[:, 0]
        left_hand_images = np.array(hand_images)[:, 1]

        # Generate face and body poses
        face_images, _ = self.get_face(seq_df)
        pose_images, _ = self.get_pose(seq_df)

        # Combine hand, face, and body images into frames
        combined_images = self.combine_images(right_hand_images, left_hand_images, face_images, pose_images)

        # Create and display the animation
        animation = self.create_animation(combined_images, title=f'Gesture: {phrase} ({animation_name})')

        # Save animation if write is True
        if write:
            out_file = f'{self.output_dir}/{animation_name}'
            animation.save(out_file, dpi=80, writer=PillowWriter(fps=3))

            self.logger.info("Finished processing : ", out_file)

        return animation
