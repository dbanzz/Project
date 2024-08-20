import matplotlib.pyplot as plt

# Prepare the data
metrics = ['Data Augmentation', 'Learning rate', 'Batch size']
mse_values = [3696.685, 1873.043, 504.504]
r_squared_values = [-0.304, -0.723, -1.074]

# Control group values for MSE and R-squared
control_mse_value = 4032.704
control_r_squared_value = -0.2726
control_group_label = 'Control Group: Data Augmentation, LR: 1e-4, Batch size: 4'

# Create figure and set the size
fig, ax = plt.subplots(2, 1, figsize=(8, 12))

# First bar chart: MSE
ax[0].bar(metrics, mse_values, color='skyblue')
ax[0].axhline(y=control_mse_value, color='gray', linestyle='--', label=control_group_label)
ax[0].set_title('Mean Squared Error by Hyperparameter')
ax[0].set_ylabel('MSE Value')
ax[0].legend(loc = 'best')

# Second bar chart: R-squared
ax[1].bar(metrics, r_squared_values, color='salmon')
ax[1].axhline(y=control_r_squared_value, color='gray', linestyle='--', label=control_group_label)
ax[1].set_title('R-Squared by Hyperparameter')
ax[1].set_ylabel('R-Squared Value')
ax[1].legend(loc = 'lower left')

# Layout adjustment
plt.tight_layout()

# Save the figure to local storage (ensure the directory exists or adjust to a valid one)
plt.savefig('D:/project/validate_new/Hyperparameter_Performance_Charts.png')

# Show the charts
plt.show()
