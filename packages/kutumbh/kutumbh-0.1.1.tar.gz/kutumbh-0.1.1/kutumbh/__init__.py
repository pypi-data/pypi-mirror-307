import pandas as pd # type: ignore
import plotly.express as px  # type: ignore
import numpy as np # type: ignore
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from fcmeans import FCM # type: ignore
import plotly.express as px  # type: ignore
from scipy import stats # type: ignore
from datetime import datetime
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
def radiations_on_walls(lat, long, epw, wall_azimuth):
    # Read the EPW file using the kutumbh package
    data = read_epw(epw)
    
    # Set observer's latitude and longitude
    lstm = 15 * 5.5  # Local Standard Time Meridian for India
    
    # Convert columns to datetime
    data['Date/Time'] = pd.to_datetime(data[['Year', 'Month', 'Day']])
    
    # Calculate the day of the year
    data['day'] = data['Date/Time'].apply(lambda x: x.timetuple().tm_yday)
    
    # Calculate Equation of Time (EoT)
    B = 360 / 365 * (data['day'] - 81)
    eot = 9.87 * np.sin(2 * np.radians(B)) - 7.53 * np.cos(np.radians(B)) - 1.5 * np.sin(np.radians(B))
    
    # Calculate Time Correction (TC)
    tc = 4 * (long - lstm) + eot
    
    # Convert to Local Time (LST)
    data['Local Time'] = data['Date/Time'] + pd.to_timedelta(tc, unit='m')
    
    # Calculate Hour Angle (HRA)
    data['hra'] = 15 * (data['Local Time'].dt.hour + data['Local Time'].dt.minute / 60 - 12)
    
    # Calculate solar declination
    day_angle = 360 * (284 + data['day']) / 365
    data['declination'] = 23.45 * np.sin(np.radians(day_angle))
    
    # Calculate Solar Altitude Angle
    LAT_rad = np.radians(lat)
    delta_rad = np.radians(data['declination'])
    H_rad = np.radians(data['hra'])
    data['Solar Altitude Angle'] = np.degrees(np.arcsin(np.sin(LAT_rad) * np.sin(delta_rad) + np.cos(LAT_rad) * np.cos(delta_rad) * np.cos(H_rad)))
    
    # Calculate solar zenith angle
    data['solar_zenith'] = 90 - data['Solar Altitude Angle']
    
    # Calculate solar azimuth angle
    data['solar_azimuth'] = np.where(
        data['Local Time'].dt.hour < 12,
        np.degrees(np.arccos((np.sin(delta_rad) * np.cos(LAT_rad) - np.cos(delta_rad) * np.sin(LAT_rad) * np.cos(H_rad)))),
        360 - np.degrees(np.arccos((np.sin(delta_rad) * np.cos(LAT_rad) - np.cos(delta_rad) * np.sin(LAT_rad) * np.cos(H_rad))))
    )
    
    # Replace wall azimuth for different orientations
    # Adjust the Wall Azimuth directly based on the given azimuth
    if wall_azimuth == 0:
        wall_azimuth = 180
    elif wall_azimuth == 180:
        wall_azimuth = 0
    elif wall_azimuth == 90:
        wall_azimuth = 270
    elif wall_azimuth == 270:
        wall_azimuth = 90
    
    data['Wall Azimuth'] = wall_azimuth
    
    # Calculate AOI (Angle of Incidence)
    data['AOI'] = np.degrees(np.arccos(np.sin(np.radians(data['solar_zenith'])) * np.cos(np.radians(data['solar_azimuth'] - data['Wall Azimuth']))))
    
    # Calculate ground and diffuse radiation components
    Y = np.maximum(0.45, 0.55 + 0.437 * np.cos(np.radians(data['AOI'])) + 0.313 * np.cos(np.radians(data['AOI']))**2)
    data['DNR on wall'] = data['Direct Normal Radiation [Wh/m2]'] * np.cos(np.radians(data['AOI']))
    data['Diffuse_on_wall'] = data['Diffuse Horizontal Radiation [Wh/m2]'] * Y
    # data['E_ground'] = (data['Direct Normal Radiation [Wh/m2]'] * np.sin(np.radians(data['Solar Altitude Angle'])) +
    #                     data['Diffuse Horizontal Radiation [Wh/m2]']) * 0.2 * (1 + np.cos(np.radians(data['Solar Altitude Angle']))) / 2
    
    # Calculate total radiation on the wall
    data['Total Radiation'] = abs( data['DNR on wall'])
    
    # Plotting the total radiation on the wall throughout the day




# Assuming 'data' has multiple days (use a pivot table if necessary)
    pivot_data = data.pivot_table(index='Hour', columns='day', values='Total Radiation')
    
    plt.figure(figsize=(14, 6))
    sns.heatmap(pivot_data, cmap='YlOrRd', cbar_kws={'label': 'Radiation (Wh/m²)'}, annot=False)
    plt.title(f'Hourly Radiation on Wall Across Days (Wall Azimuth: {wall_azimuth}°)', fontsize=16)
    plt.xlabel('Day of Year', fontsize=14)
    plt.ylabel('Hour of Day', fontsize=14)
    plt.tight_layout()
    plt.show()
def temp_combined_with_humidity(epw,months):
    data= read_epw(epw)
    # Calculate average humidity for each hour
    average_humidity = data.groupby('Hour')['Relative Humidity [%]'].mean().round(10).reset_index()
    
    # Merge average humidity with the original data
    data_with_avg_humidity = pd.merge(data, average_humidity, on='Hour', suffixes=('', '_avg'))
    
    # Create a categorical column for average humidity
    humidity_bins = [0, 30, 60, 100]  # Define bins for humidity
    humidity_labels = ['Low', 'Medium', 'High']  # Define labels for the bins
    data_with_avg_humidity['Humidity Category'] = pd.cut(data_with_avg_humidity['Relative Humidity [%]_avg'],
                                                         bins=humidity_bins, 
                                                         labels=humidity_labels, 
                                                         right=False)
    
    # Filter data for specific months if needed (e.g., March, April, May)
    filtered_data = data_with_avg_humidity[data_with_avg_humidity['Month'].isin(months)]
    
    # Set the style
    sns.set(style="whitegrid")
    
    # Create a boxplot
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=filtered_data, 
                x="Hour", 
                y="Dry Bulb Temperature [C]", 
                hue="Humidity Category")  # Use the humidity category for coloring
    
    # Set the title and labels
    plt.title("Dry Bulb Temperature by Hour and humidity")
    plt.xlabel("Hour")
    plt.ylabel("Dry Bulb Temperature [C]")
    
    # Show the plot
    plt.show()
def plot_monthly_illuminance_box_and_mean_sky_cover(epw):
    """
    Creates a box plot of illuminance for each month and overlays the mean sky cover.

    Parameters:
    epw (str): Path to the EPW file.
    """
    # Read the EPW file
    df = read_epw(epw)

    # Convert date and time columns to a datetime index
    df['Datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute']])
    df.set_index('Datetime', inplace=True)

    # Add month column for grouping
    df['Month'] = df.index.month

    # Calculate mean sky cover for each month
    monthly_sky_cover_mean = df.groupby('Month')['Total Sky Cover'].mean()
   
    # Set up the figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Create the box plot for illuminance by month with a warm color palette
    sns.boxplot(x='Month', y='Global Horizontal Illuminance [lux]', data=df, ax=ax1, palette="YlOrRd")
    ax1.set_ylabel('Global Horizontal Illuminance [lux]', color='darkorange')
    ax1.set_xlabel('Month')
    ax1.set_title('Monthly Illuminance Box Plot and Mean Sky Cover')

    # Plot the mean sky cover as a line plot with sky-inspired colors
    ax2 = ax1.twinx()
    ax2.plot(monthly_sky_cover_mean.index, monthly_sky_cover_mean.values, color='deepskyblue', marker='o', linestyle='-', linewidth=2, label='Mean Sky Cover')
    ax2.set_ylabel('Mean Total Sky Cover', color='deepskyblue')
    ax2.set_ylim(0, 10)  # Assuming sky cover ranges from 0 to 10

    # Add legend and show plot
    ax2.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


