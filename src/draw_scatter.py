import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import NearestNeighbors

# Read CSV files
result_total_df = pd.read_csv('D:/project/validate_LDtoSD/Result_total_original_new.csv')
result_true_df = pd.read_csv('D:/project/validate_LDtoSD/Result_true_edit_original.csv')
output_path = 'D:/project/validate_LDtoSD/predicted_VS_actual_original.png'

# Extract predict and actual values
predicted = result_total_df['length'].values
actual = result_true_df['Length'].values

# Calculate R-squared and MSE
r_squared = r2_score(predicted, actual)
mse = mean_squared_error(predicted, actual)

# Draw a scatter plot
plt.figure(figsize=(10, 6))

# Plot data points from result_total_df
plt.scatter(predicted, actual, label='Result Predict Data Points', marker='o', color='blue')

# Plot data points from result_true_df (paired)
plt.scatter(actual, actual, label='Result True Data Points', marker='x', color='red')

# Plot the baseline
max_value = max(predicted.max(), actual.max())
plt.plot([0, max_value], [0, max_value], 'r--', label='Baseline')

# Add R-squared and MSE to the plot
plt.text(0.05, 0.95, f'R-squared: {r_squared:.3f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
plt.text(0.05, 0.90, f'MSE: {mse:.3f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

# Add a title and tags
plt.title('Predicted vs Actual Hypocotyl Length')
plt.xlabel('Predicted Hypocotyl Length')
plt.ylabel('Actual Hypocotyl Length')
plt.legend(loc='lower right')
plt.grid(True)
plt.savefig(output_path)
plt.show()
