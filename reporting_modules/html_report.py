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


# Function to write DataFrame to an HTML file
def write_to_html(dataframe, filename):
    try:
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

                # Display the image from the text in the column (resized to 250x250 pixels)
                image_tag = f'<img src="{relative_path}" alt="{screenshot_name}" style="max-width: 250px; max-height: 250px;">'
                df_copy.at[index, "screen_shot_name"] += f'<br>{image_tag}'

                # Move the screenshot to the folder
                #os.rename(screenshot_name, f"./{screenshot_name}")

            # Write the modified dataframe to HTML
            df_copy.to_html(filename, index=False, escape=False)
        else:
            dataframe.to_html(filename, index=False)

        print(f"DataFrame has been successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to {filename}: {e}")