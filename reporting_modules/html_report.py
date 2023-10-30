# Define the function for firewall detection
# MIT License
#
# Copyright (c) 2023 Tim Kelly
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import pandas as pd
from datetime import datetime

# Function to write DataFrame to an HTML file
def write_to_html(dataframe, filename):
    try:
        # Add description at the top of the HTML file
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        description = f"<p>Scan results courtesy of <a href='https://github.com/austimkelly/rekon' target='_blank'>rekon</a> on {current_datetime}.</p>"

        # Write the description to the HTML file
        with open(filename, "w") as file:
            file.write(f"<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'><style>table {{ min-width: 350px; width: 100%; }}</style></head><body>{description}")

        if "screen_shot_name" in dataframe.columns:
            # Create a copy of the dataframe to avoid modifying the original dataframe
            df_copy = dataframe.copy()

            # Iterate through rows
            for index, row in df_copy.iterrows():
                screenshot_name = row["screen_shot_name"]

                # If the value is "DNT" or doesn't end with ".png", do nothing
                if screenshot_name == "DNT" or not screenshot_name.endswith(".png"):
                    continue

                # Wrap the text in a relative HTML link
                relative_path = f"./{screenshot_name}"
                df_copy.at[index, "screen_shot_name"] = f'<a href="{relative_path}" target="_blank">{screenshot_name}</a>'

                # Display the image from the text in the column (resized to 100% width)
                image_tag = f'<img src="{relative_path}" alt="{screenshot_name}" style="width: 100%;">'
                df_copy.at[index, "screen_shot_name"] += f'<br>{image_tag}'

                # Move the screenshot to the folder
                # os.rename(screenshot_name, f"./{screenshot_name}")

            # Append the modified dataframe to HTML
            with open(filename, "a") as file:
                df_copy.to_html(file, index=False, escape=False)
        else:
            # Write the dataframe to HTML
            with open(filename, "a") as file:
                dataframe.to_html(file, index=False, escape=False)

        # Close the HTML file
        with open(filename, "a") as file:
            file.write("</body></html>")

        print(f"DataFrame has been successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")

# Example usage:
# write_to_html(your_dataframe, "output.html")
