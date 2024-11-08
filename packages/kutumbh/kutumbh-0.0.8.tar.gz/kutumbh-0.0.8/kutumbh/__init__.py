import pandas as pd # type: ignore
import plotly.express as px  # type: ignore
import numpy as np # type: ignore
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from fcmeans import FCM # type: ignore
import plotly.express as px  # type: ignore
# Define basic mathematical operations
def add_num(num1, num2):
    """Returns the sum of two numbers."""
    return num1 + num2

def sub_num(num1, num2):
    """Returns the difference between two numbers."""
    return num1 - num2

def mul_num(num1, num2):
    """Returns the product of two numbers."""
    return num1 * num2

def div_num(num1, num2):
    """Returns the division of two numbers. Raises an error if the divisor is zero."""
    if num2 == 0:
        raise ValueError("Division by zero is undefined.")
    return num1 / num2

# Define a function to read EPW files
def read_epw(epw_file_path):
    """
    Reads an EPW (EnergyPlus Weather) file and returns a DataFrame.

    Args:
        epw_file_path (str): Path to the EPW file.

    Returns:
        DataFrame: Pandas DataFrame containing the weather data.
    """
    column_names = [
        "Year", "Month", "Day", "Hour", "Minute", "Data Source and Uncertainty Flags",
        "Dry Bulb Temperature [C]", "Dew Point Temperature [C]", "Relative Humidity [%]",
        "Atmospheric Station Pressure [Pa]", "Extraterrestrial Horizontal Radiation [Wh/m2]",
        "Extraterrestrial Direct Normal Radiation [Wh/m2]", "Horizontal Infrared Radiation Intensity [Wh/m2]",
        "Global Horizontal Radiation [Wh/m2]", "Direct Normal Radiation [Wh/m2]",
        "Diffuse Horizontal Radiation [Wh/m2]", "Global Horizontal Illuminance [lux]",
        "Direct Normal Illuminance [lux]", "Diffuse Horizontal Illuminance [lux]",
        "Zenith Luminance [Cd/m2]", "Wind Direction [degrees]", "Wind Speed [m/s]",
        "Total Sky Cover", "Opaque Sky Cover", "Visibility [km]", "Ceiling Height [m]",
        "Present Weather Observation", "Present Weather Codes", "Precipitable Water [mm]",
        "Aerosol Optical Depth", "Snow Depth [cm]", "Days Since Last Snowfall",
        "Albedo", "Liquid Precipitation Depth [mm]", "Liquid Precipitation Quantity [hr]"
    ]

    try:
        # Read the EPW file into a DataFrame
        data = pd.read_csv(epw_file_path, skiprows=8, header=None, names=column_names, skipinitialspace=True)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {epw_file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
    return data


def temperature_density_plot(epw, months):
    # Read the EPW data into a DataFrame
    data = read_epw(epw)
    
    # Filter the data to include only the specified months, if provided
    if months:
        data = data[data['Month'].isin(months)]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create the 2D density plot
    sns.kdeplot(data=data, x="Hour", y="Dry Bulb Temperature [C]", fill=True, ax=ax, cmap="Blues", thresh=0)
    
    # Create marginal histograms
    sns.histplot(data=data, x="Hour", ax=ax, color='blue', alpha=0.5, bins=30, kde=True, stat='density', legend=False)
    # sns.histplot(data=data, y="Dry Bulb Temperature [C]", ax=ax, color='blue', alpha=0.5, bins=30, kde=True, stat='density', legend=False)

    # Set labels and title
    ax.set_xlabel("Hour")
    ax.set_ylabel("Dry Bulb Temperature [C]")
    ax.set_title("Density Heatmap of Dry Bulb Temperature")

    plt.show()

def get_daily_data(data):
    # Initialize lists to store daily statistics
    data['Day'] = (data.index // 24) + 1
    daily_min_temp = []
    daily_max_temp = []
    daily_mean_humidity = []
    daily_mean_radiation = []
    
    # Process each day
    for day in data['Day'].unique():
        daily_data = data[data['Day'] == day]
        
        min_temp = daily_data['Dry Bulb Temperature [C]'].min()
        max_temp = daily_data['Dry Bulb Temperature [C]'].max()
        mean_humidity = daily_data['Relative Humidity [%]'].mean().round(1)
        mean_radiation = daily_data[daily_data['Global Horizontal Radiation [Wh/m2]'] > 50]['Global Horizontal Radiation [Wh/m2]'].mean().round(0)
        
        daily_min_temp.append(min_temp)
        daily_max_temp.append(max_temp)
        daily_mean_humidity.append(mean_humidity)
        daily_mean_radiation.append(mean_radiation)
    
    # Create a DataFrame for the results
    results = pd.DataFrame({
        'Day': data['Day'].unique(),
        'Dry_Bulb_Temp_Min': daily_min_temp,
        'Dry_Bulb_Temp_Max': daily_max_temp,
        'Relative_Humidity_Mean': daily_mean_humidity,
        'Global_Horizontal_Radiation_Mean': daily_mean_radiation
    })
    return results


def get_clustered(results):
    # Extract relevant columns and scale them
    data_values = results[['Dry_Bulb_Temp_Min', 'Dry_Bulb_Temp_Max', 'Relative_Humidity_Mean', 'Global_Horizontal_Radiation_Mean']].values
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_values)
    
    # Define the range of clusters to test
    cluster_range = range(3, 7)
    best_cluster_count = None
    best_labels = None
    
    # Perform fuzzy c-means clustering for each number of clusters
    for n_clusters in cluster_range:
        fcm = FCM(n_clusters=n_clusters, max_iter=1000, m=2, error=0.005)
        fcm.fit(data_scaled)
        
        # Assign each data point to the cluster with the highest membership score
        cluster_labels = np.argmax(fcm.u, axis=1)
        
        # Count the number of days in each cluster
        cluster_counts = np.bincount(cluster_labels)
        
        # Check if all clusters have at least 20 days
        if np.all(cluster_counts >= 20):
            if n_clusters == 4 or n_clusters == 5:
                best_cluster_count = n_clusters
                best_labels = cluster_labels
                break
            if best_cluster_count is None:
                best_cluster_count = n_clusters
                best_labels = cluster_labels
    
    # Add the cluster labels to the results DataFrame
    results['Season'] = best_labels

    # Create a summary table for each cluster, including the count of days
    summary = results.groupby('Season').agg({
        'Dry_Bulb_Temp_Min': 'mean',
        'Dry_Bulb_Temp_Max': 'mean',
        'Relative_Humidity_Mean': 'mean',
        'Global_Horizontal_Radiation_Mean': 'mean',
        'Day': 'count'  # Count the number of days in each cluster
    }).rename(columns={'Day': 'Number_of_Days'})

    # Round the numerical values to 1 decimal place
    summary = summary.round(1)

    # Print the summary table
    return summary
def seasons_summary(epw):
   data= read_epw(epw)
   results=get_daily_data(data)
   r=get_clustered(results)
   return r
def dry_bulb_temp_heatmap(epw):
    data= read_epw(epw)
    fig = px.density_heatmap(data, x="Hour", y="Dry Bulb Temperature [C]", marginal_x="rug", marginal_y="histogram")
    fig.show()


# Function to get hours for a specific time of day
def get_time_of_day(time):
    if time == 'Morning':
        return [6, 7, 8, 9, 10, 11]
    elif time == 'Noon':
        return [12, 13, 14, 15, 16, 17]
    elif time == 'Evening':
        return [18, 19, 20, 21, 22, 23]
    elif time == 'Night':
        return [0, 1, 2, 3, 4, 5]
    else:
        return "Invalid time of day"

# Function to filter data based on time of day and plot
def plot_timely_wind_data(epw, time_of_day):
    data=read_epw(epw)
    hours = get_time_of_day(time_of_day)
    if hours == "Invalid time of day":
        print("Invalid time of day. Please choose from: 'Morning', 'Noon', 'Evening', or 'Night'.")
        return
    
    # Filter data for the specified time of day
    filtered_data = data[data['Hour'].isin(hours)]
    
    # Plot using Plotly Express
    fig = px.scatter_polar(
        filtered_data,
        r="Wind Speed [m/s]",
        theta="Wind Direction [degrees]",
        color="Dry Bulb Temperature [C]",
        opacity=0.2,
        color_continuous_scale=px.colors.sequential.Plasma_r,
        title=f"Polar Scatter Plot for {time_of_day}"
    )
    fig.show()
