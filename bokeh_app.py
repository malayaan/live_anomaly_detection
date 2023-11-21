import os
import json
from bokeh.plotting import figure, show, output_file
from bokeh.models.formatters import DatetimeTickFormatter
import pandas as pd
from datetime import datetime

# Directory containing the JSON files
directory_path = 'data2'  # Replace with your directory path

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame(columns=['timestamp', 'value'])

# Iterate over each file in the directory
for file_name in os.listdir(directory_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(directory_path, file_name)
        
        # Load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Filter and process data
        variable_to_plot = 'VL10.Compteur_Horaire_secondes'
        filtered_data = [entry for entry in data if entry['pointId'] == variable_to_plot]
        timestamps = [datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00')) for entry in filtered_data]
        values = [entry['data']['value'] for entry in filtered_data]
        
        # Create a temporary DataFrame and append to all_data
        temp_df = pd.DataFrame({'timestamp': timestamps, 'value': values})
        all_data = pd.concat([all_data, temp_df])

# Sort the combined DataFrame
all_data.sort_values('timestamp', inplace=True)

# Verify data
print(all_data.head())  # Check the first few rows

# Bokeh plot setup
output_file("combined_visualisation.html")  # Output to HTML file
p = figure(title="VL10.Compteur_Horaire_secondes Over Time - Combined Data", x_axis_type="datetime", height=350, width=800)
p.line(all_data['timestamp'], all_data['value'], line_width=2, color='green', alpha=0.7)

# Datetime format
p.xaxis.formatter = DatetimeTickFormatter(
    hours="%H:%M",
    days="%Y-%m-%d %H:%M",
    months="%Y-%m-%d %H:%M",
    years="%Y-%m-%d %H:%M"
)

# Axis labels
p.xaxis.axis_label = "Timestamp"
p.yaxis.axis_label = "Value"

# Display plot
show(p)
