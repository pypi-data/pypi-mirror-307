import sys
import os
import argparse

import webbrowser
import tempfile
from matplotlib.animation import FuncAnimation
from pathlib import Path

# Add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from perennityai_viz.data_visualization import DataVisualizer
from perennityai_viz.utils import Log

def open_animation_in_browser(animation: FuncAnimation):
    """
    Saves the FuncAnimation as an HTML file, adds CSS to center the animation,
    and opens it in a new browser window. Also adds a logo to the HTML.

    Parameters:
        animation (FuncAnimation): The animation to display in the browser.
        logo_path (str): Path to the logo image file.
    """
    # Create a temporary HTML file to store the animation
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_html:
        temp_path = Path(temp_html.name)
        
        # Get the HTML content of the animation
        html_content = animation.to_jshtml()
        logo_path = 'https://perennityai.com/_next/image?url=%2Fimg%2Fperennity.png&w=128&q=75'
        # Add CSS and logo to center the animation
        centered_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PerennityAI MediaPipe Visualization Animation</title>
            <style>
                body {{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #030012;
                    font-family: Arial, sans-serif;
                    position: relative;
                }}
                #logo {{
                    position: absolute;
                    top: 20px;
                    left: 30px;
                    z-index: 10;
                    text-align: center;
                }}
                #logo img {{
                    width: 50px;
                    height: 50px;
                }}
                #logo-text {{
                    font-size: 20px;
                    color: #c3c0d8;
                    margin-top: 10px;
                    font-weight: bold;
                }}
                #animation {{
                    max-width: 100%; /* Sets a maximum width */
                    max-height: 100%; /* Maintains aspect ratio */
                    width: auto;
                }}
            </style>
        </head>
        <body>
            <!-- Logo Section -->
            <div id="logo">
                <img src="{logo_path}" alt="Logo" />
                <div id="logo-text">PerennityAI</div>
            </div>

            <!-- Animation Section -->
            <div id="animation">
                {html_content}
            </div>
        </body>
        </html>
        """
        
        # Write the centered HTML content to the temporary file
        temp_path.write_text(centered_html)
        
        # Open the HTML file in a new browser window
        webbrowser.open_new(temp_path.as_uri())
        
        

def parse_arguments():
    parser = argparse.ArgumentParser(description="Data Visualizer Processor for creating animations from dataset files.")
    
    # Input/Output arguments
    parser.add_argument('--input_file', type=str, default='', help='CSV or TFRecord input file.')
    parser.add_argument('--input_dir', type=str, default='', help='Directory containing multiple dataset files.')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save output animations.')
    
    # Format and file handling
    parser.add_argument('--data_input_format', type=str, choices=['csv', 'tfrecord', 'parquet'], default='csv', 
                        help='Input file format: "csv" or "tfrecord".')
    
    # Visualization options
    parser.add_argument('--csv_file', type=str, default='', 
                    help='CSV file in input to visualize.')
    parser.add_argument('--tfrecord_file', type=str, default='', 
                        help='TFRecord file in input to visualize.')
    parser.add_argument('--parquet_file', type=str, default='', 
                    help='Path to a specific Parquet file for visualization.')
    
    parser.add_argument('--csv_file_index', type=int, default=-1, 
                        help='Index of CSV file in input directory to visualize.')
    parser.add_argument('--tf_file_index', type=int, default=-1, 
                        help='Index of TFRecord file in input directory to visualize.')
    parser.add_argument('--parquet_file_index', type=int, default=-1, 
                        help='Index of Parquet file in input directory to visualize.')
    parser.add_argument('--animation_name', type=str, default='', help='Custom name for the output animation file.')
    parser.add_argument('--output_format', type=str, default='.gif', choices=['.gif', '.mp4'], 
                        help='Format of the output animation, e.g., ".gif" or ".mp4".')
    parser.add_argument('--write',type=bool, default=True, help='Flag to save the animation to the output directory.')
    parser.add_argument('--verbose', type=str, default='INFO', choices=['DEBUG', 'ERROR', 'WARNING'], help='Set logging level for output')
    parser.add_argument('--show', type=bool, default=False, help='Set to show animation in browser')
    parser.add_argument('--encoding', type=str, default='ISO-8859-1', help='Encoding format for CSV files.')
    
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    animation = None

    try:

        # Initialize the DataVisualizerProcessor
        visualizer = DataVisualizer(
            input_file=args.input_file,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            encoding=args.encoding,
            verbose=args.verbose
        )

        # Create the animation based on specified parameters
        if args.data_input_format == 'csv':
            if args.csv_file_index >= 0:
                animation = visualizer.visualize_data(
                    csv_file_index=args.csv_file_index,
                    animation_name=args.animation_name,
                    write=args.write,
                    output_format=args.output_format
                )

            elif args.csv_file or '.csv' in args.input_file:
                animation = visualizer.visualize_data(
                    csv_file=args.csv_file,
                    animation_name=args.animation_name,
                    write=args.write,
                    output_format=args.output_format
                )
            else:
                print("CSV Invalid input!")

        elif args.data_input_format == 'tfrecord':
            if args.tf_file_index >= 0:
                animation = visualizer.visualize_data(
                    tf_file_index=args.tf_file_index,
                    animation_name=args.animation_name,
                    write=args.write,
                    output_format=args.output_format
                )
            elif args.tfrecord_file or '.tfrecord' in args.input_file:
                animation = visualizer.visualize_data(
                    tfrecord_file=args.tfrecord_file,
                    animation_name=args.animation_name,
                    write=args.write,
                    output_format=args.output_format
                )
            else:
                print("TFrecord_file Invalid input!")
        elif args.data_input_format == 'parquet':
            if args.parquet_file_index >= 0:
                animation = visualizer.visualize_data(
                    parquet_file_index=args.parquet_file_index,
                    animation_name=args.animation_name,
                    write=args.write,
                    output_format=args.output_format
                )
            elif args.tfrecord_file or '.parquet' in args.input_file:
                animation = visualizer.visualize_data(
                    parquet_file=args.parquet_file,
                    animation_name=args.animation_name,
                    write=args.write,
                    output_format=args.output_format
                )
            else:
                print("Parquet_file Invalid input!")

        # Display animation in browser
        if animation is not None:
            if args.show:
                # Open the animation in a new browser window
                open_animation_in_browser(animation)
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"Configuration loading failed: {e}")

if __name__ == "__main__":
    main()
