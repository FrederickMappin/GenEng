import pandas as pd
import matplotlib.pyplot as plt
import math
import missingno as msno
from scipy.stats import skew


def calculate_statistics(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path, index_col=0)

    # Initialize a list to store the statistics for each column
    stats_list = []

    # Iterate through each column in the DataFrame
    for column in df.columns:
        col_data = df[column].dropna().astype(float)  # Drop NaN values and convert to float
        mean = col_data.mean()
        median = col_data.median()
        mode = col_data.mode().iloc[0] if not col_data.mode().empty else np.nan
        std_dev = col_data.std()
        min_val = col_data.min()
        max_val = col_data.max()
        skewness = skew(col_data)


        # Append the statistics to the list
        stats_list.append([mean, median, mode, std_dev, min_val, max_val, skewness])

    # Create a DataFrame from the statistics list
    stats_df = pd.DataFrame(stats_list, columns=['Mean', 'Median', 'Mode', 'Standard Deviation', 'Min', 'Max', 'Skewness'], index=df.columns)

    return stats_df







def plot_histograms(file_path, columns_to_plot):
    # Read the CSV file
    df = pd.read_csv(file_path, index_col=0)

    # Filter the DataFrame to include only the specified columns
    df = df[columns_to_plot]

    # Determine the number of columns to plot
    num_cols = df.shape[1]
    cols = 4  # Number of columns for subplots
    rows = math.ceil(num_cols / cols)  # Calculate the number of rows needed

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Iterate through each column in the DataFrame
    for i, column in enumerate(df.columns):
        numeric_data = df[column].dropna().astype(float)
        axes[i].hist(numeric_data, bins=10)
        axes[i].set_title(f'Histogram for {column}')
        axes[i].set_xlabel('Value')
        axes[i].set_ylabel('Frequency')

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def plot_boxplots(file_path, columns_to_plot):
    # Read the CSV file
    df = pd.read_csv(file_path, index_col=0)

    # Filter the DataFrame to include only the specified columns
    df = df[columns_to_plot]

    # Determine the number of columns to plot
    num_cols = df.shape[1]
    cols = 4  # Number of columns for subplots
    rows = math.ceil(num_cols / cols)  # Calculate the number of rows needed

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Iterate through each column in the DataFrame
    for i, column in enumerate(df.columns):
        numeric_data = df[column].dropna().astype(float)
        axes[i].boxplot(numeric_data, vert=False)
        axes[i].set_title(f'Box Plot for {column}')
        axes[i].set_xlabel('Value')

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

def plot_barplots(file_path, columns_to_plot):
    # Read the CSV file
    df = pd.read_csv(file_path, index_col=0)

    # Filter the DataFrame to include only the specified columns
    df = df[columns_to_plot]

    # Determine the number of columns to plot
    num_cols = df.shape[1]
    cols = 4  # Number of columns for subplots
    rows = math.ceil(num_cols / cols)  # Calculate the number of rows needed

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Iterate through each column in the DataFrame
    for i, column in enumerate(df.columns):
        numeric_data = df[column].dropna().astype(float)
        axes[i].bar(range(len(numeric_data)), numeric_data)
        axes[i].set_title(f'Bar Plot for {column}')
        axes[i].set_xlabel('Index')
        axes[i].set_ylabel('Value')

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()



def plot_missing_map(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path, index_col=0)

    # Create the missing value map with black for present values and gray for missing values
    msno.matrix(df, figsize=(15, 5), color=(0.5, 0.5, 0.5), sparkline=False)
    plt.gca().patch.set_facecolor('gray')  # Set the background color to gray
    plt.show()




# Example usage
file_path = "Book1.csv"
df = pd.read_csv(file_path, index_col=0)  # Read the CSV file to get the columns
columns_to_plot = df.columns[0:9]  # Example: selecting columns from index 1 to 8

plot_histograms(file_path, columns_to_plot)
plot_boxplots(file_path, columns_to_plot)
plot_barplots(file_path, columns_to_plot)
plot_missing_map(file_path)
stats_df = calculate_statistics(file_path)
print(stats_df)
