import os
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

# Calculate the center and size of a bounding box
def calculate_center_and_size(bbox):
    x_center = (bbox[0] + bbox[2]) / 2
    y_center = (bbox[1] + bbox[3]) / 2
    width = abs(bbox[2] - bbox[0])
    height = abs(bbox[3] - bbox[1])
    return (x_center, y_center), (width, height)

# Determine if two bounding boxes are close in terms of center distance and size
def is_close_with_size(center1, size1, center2, size2, center_threshold=100, size_threshold=70):
    center_distance = sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
    size_difference = sqrt((size1[0] - size2[0]) ** 2 + (size1[1] - size2[1]) ** 2)
    return center_distance <= center_threshold and size_difference <= size_threshold

# Calculate statistics for bounding boxes (correct detections, total plants, false detections)
def calculate_bbox_stats(correct_bboxes_path, total_bboxes_path):
    correct_bboxes = np.load(correct_bboxes_path, allow_pickle=True)
    total_bboxes = np.load(total_bboxes_path, allow_pickle=True)

    correct_count = len(correct_bboxes)
    false_count = 0

    total_bboxes_reversed = np.flip(total_bboxes, axis=1)
    center_threshold = 120
    size_threshold = 70

    total_plant = 0
    for bbox1 in total_bboxes_reversed:
        center1, size1 = calculate_center_and_size(bbox1)
        for bbox2 in correct_bboxes:
            center2, size2 = calculate_center_and_size(bbox2)
            if is_close_with_size(center1, size1, center2, size2, center_threshold, size_threshold):
                total_plant += 1
                break

    false_count = len(total_bboxes) - total_plant

    return correct_count, total_plant, false_count

# Plot the ROC curve based on correct rates and false counts
def plot_roc_curve(correct_rates, false_counts, min_object_sizes, output_path):
    plt.figure()
    for i in range(len(correct_rates)):
        plt.scatter(false_counts[i], correct_rates[i], marker='o', label=f'min_object_size_{min_object_sizes[i]}')
        plt.annotate(f'{min_object_sizes[i]}', (false_counts[i], correct_rates[i]))
    plt.plot([6,30], [0.37, 0.82], linestyle='--', label='Baseline')
    plt.xlabel('Average False Boxes')
    plt.ylabel('Correctly Marked Plants / Total Plants')
    plt.title('ROC Curve')
    #plt.legend(loc='best')
    plt.grid(True)
    plt.savefig(output_path)
    plt.show()

# Main function to calculate and plot the ROC curve
def main(correct_bboxes_dir, total_bboxes_base_dir, output_path):
    correct_rates = []
    false_counts = []
    min_object_sizes = []

    for min_object_size in range(2, 21):
        total_bboxes_dir = os.path.join(total_bboxes_base_dir, f"min_object_size_{min_object_size}")

        if not os.path.exists(total_bboxes_dir):
            continue

        correct_count_sum = 0
        total_plant_sum = 0
        false_count_sum = 0
        file_count = 0

        for file_name in os.listdir(correct_bboxes_dir):
            if file_name.endswith("_bboxes.npy"):
                correct_bboxes_path = os.path.join(correct_bboxes_dir, file_name)
                total_bboxes_path = os.path.join(total_bboxes_dir, file_name)

                if os.path.exists(total_bboxes_path):
                    correct_count, total_plant, false_count = calculate_bbox_stats(correct_bboxes_path, total_bboxes_path)
                    correct_count_sum += correct_count
                    total_plant_sum += total_plant
                    false_count_sum += false_count
                    file_count += 1

        if file_count > 0:
            avg_correct_rate = total_plant_sum / correct_count_sum
            avg_false_count = false_count_sum / file_count
            correct_rates.append(avg_correct_rate)
            false_counts.append(avg_false_count)
            min_object_sizes.append(min_object_size)

    plot_roc_curve(correct_rates, false_counts, min_object_sizes, output_path)

if __name__ == "__main__":
    correct_bboxes_dir = "D:/project/validate_new/masks"
    total_bboxes_base_dir = "D:/project/validate_new/images/image_edit"
    output_path = "D:/project/validate_new/roc_curve_custom.png"

    main(correct_bboxes_dir, total_bboxes_base_dir, output_path)
