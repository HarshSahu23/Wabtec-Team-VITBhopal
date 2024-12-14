import argparse
import shlex
import os
import sys
from tabulate import tabulate
from PIL import Image
from backend.data_handler import DataHandler
from backend.plotter import Plotter


def render_image_to_ascii(image_path, width=40):
    """
    Render the given image as ASCII art.
    """
    try:
        img = Image.open(image_path)
        img = img.convert("L")
        aspect_ratio = img.height / img.width
        height = int(aspect_ratio * width * 0.55)
        img = img.resize((width, height))
        chars = ["#", "*", " "]
        interval = 256 // len(chars)

        ascii_art = "".join([chars[min(pixel // interval, len(chars) - 1)] for pixel in img.getdata()])
        ascii_art = "\n".join([ascii_art[i:i+width] for i in range(0, len(ascii_art), width)])
        return ascii_art
    except Exception as e:
        return f"Error rendering image: {e}"


def display_intro(image_path):
    """
    Display the introductory screen with ASCII art and help information.
    """
    ascii_art = render_image_to_ascii(image_path)
    help_text = """
Welcome to the Wabtec Interactive CLI Tool!
-------------------------------------
Available Commands:
  1. import <folder_path>    Import folder containing CSV files.
  2. summary                 Display summary of the data.
  3. bar <tags>              Plot bar chart for specific tags.
  4. pie <tags>              Plot pie chart for specific tags.
  5. c_bar                   Plot bar chart for all tags.
  6. c_pie                   Plot pie chart for all tags.
  7. exit                    Exit the tool.

Type 'exit' to quit.
Type '--help' for detailed usage information.
"""

    lines_ascii = ascii_art.split("\n")
    lines_help = help_text.strip().split("\n")
    max_lines = max(len(lines_ascii), len(lines_help))

    print("=" * 80)
    for i in range(max_lines):
        left = lines_ascii[i] if i < len(lines_ascii) else ""
        right = lines_help[i] if i < len(lines_help) else ""
        print(f"{left:<40} {right}")
    print("=" * 80)


def import_folder(folder_path=None):
    if not (os.path.exists(folder_path) and
            os.path.isdir(folder_path) and
            os.access(folder_path, os.R_OK)):
        raise ValueError(
            f"Invalid folder path: '{folder_path}'. Ensure it exists, is a directory, and is accessible.")
    print(f"Importing new folder...")
    print(f"Folder path: {folder_path}")
    dh = DataHandler(folder_path)
    return dh


def plot_bar(tags=None, dh: DataHandler = None):
    try:
        filtered_df = dh.ecl_freq_summary[dh.ecl_freq_summary['Description'].isin(
            tags)]
        if filtered_df.empty:
            print(f"No matching tags found for: {tags}")
        else:
            print("Drawing bar chart with given error names...")
            Plotter.plot_bar_chart(
                x=filtered_df['Description'],
                y=filtered_df['Frequency'],
                xlabel="Description",
                ylabel="Frequency"
            )
    except IndexError:
        print("Please specify tags for the bar chart (e.g., bar_chart tag1 tag2).")


def plot_pie(tags=None, dh: DataHandler = None):
    try:
        filtered_df = dh.ecl_freq_summary[dh.ecl_freq_summary['Description'].isin(
            tags)]
        if filtered_df.empty:
            print(f"No matching tags found for: {tags}")
        else:
            print("Drawing pie chart with given error names...")
            Plotter.plot_pie_chart(
                labels=filtered_df['Description'],
                data=filtered_df['Frequency']
            )
    except IndexError:
        print("Please specify tags for the pie chart (e.g., pie_chart tag1 tag2).")


def plot_complete_bar(dh: DataHandler):
    print("Drawing complete bar chart...")
    Plotter.plot_bar_chart(
        x=dh.ecl_freq_summary['Description'],
        y=dh.ecl_freq_summary['Frequency'],
        xlabel="Description",
        ylabel="Frequency"
    )


def plot_complete_pie(dh: DataHandler):
    print("Drawing complete pie chart...")
    Plotter.plot_pie_chart(
        labels=dh.ecl_freq_summary['Description'],
        data=dh.ecl_freq_summary['Frequency']
    )


def validate_data_handler(dh: DataHandler = None):
    if dh == None:
        raise ValueError(
            "The provided data handler object is None. Try importing first.")


def show_summary(dh: DataHandler):
    print("="*20 + "Summary Table" + "="*20)
    print(tabulate(dh.ecl_freq_summary, headers='keys', tablefmt='grid'))


def create_parser():
    parser = argparse.ArgumentParser(
        description="CLI tool for performing actions with options and parameters"
    )
    subparsers = parser.add_subparsers(dest="action", required=True, help="Available actions")
    subparsers.add_parser("import", help="Import folder containing CSV files.").add_argument("folder_path", type=str, help="Path to folder.")
    subparsers.add_parser("exit", help="Exit the command line tool.")
    subparsers.add_parser("bar", help="Plot bar chart of given tags.").add_argument("tags", nargs="+", help="Tags for the error description.")
    subparsers.add_parser("pie", help="Plot pie chart of given tags.").add_argument("tags", nargs="+", help="Tags for the error description.")
    subparsers.add_parser("c_bar", help="Plot bar chart of all tags.")
    subparsers.add_parser("c_pie", help="Plot pie chart of all tags.")
    subparsers.add_parser("summary", help="Get the frequency summary description.")
    return parser


def main():
    image_path = "./logo-white.png"  # Path to your ASCII art image
    display_intro(image_path)
    parser = create_parser()

    dh = None
    while True:
        try:
            print("Type 'exit' to quit.")
            print("Type '--help' or '-h' for detailed usage information.")
            command = input("\n>>> ").strip()
            if command.lower() in {"exit", "quit"}:
                print("Exiting CLI. Goodbye!")
                break

            args = parser.parse_args(shlex.split(command))

            if args.action == "import":
                dh = import_folder(args.folder_path)
                validate_data_handler(dh)
                show_summary(dh)
            elif args.action == "bar":
                validate_data_handler(dh)
                plot_bar(args.tags, dh)
            elif args.action == "pie":
                validate_data_handler(dh)
                plot_pie(args.tags, dh)
            elif args.action == "c_bar":
                validate_data_handler(dh)
                plot_complete_bar(dh)
            elif args.action == "c_pie":
                validate_data_handler(dh)
                plot_complete_pie(dh)
            elif args.action == "summary":
                validate_data_handler(dh)
                show_summary(dh)
            else:
                print("Unknown action. Type '--help' for usage information.\n")

        except SystemExit:
            print("Invalid command. Type '--help' for usage information.\n")
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == "__main__":
    main()
