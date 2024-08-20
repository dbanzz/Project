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

# Determine if two bounding boxes are close in terms of center distance and size difference
def is_close_with_size(center1, size1, center2, size2, center_threshold=140, size_threshold=70):
    center_distance = sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)  
    size_difference = sqrt((size1[0] - size2[0]) ** 2 + (size1[1] - size2[1]) ** 2)  
    return center_distance <= center_threshold and size_difference <= size_threshold  

# Calculate statistics for correct and total bounding boxes
def calculate_bbox_stats(correct_bboxes_path, total_bboxes_path, center_threshold=140, size_threshold=70):
    correct_bboxes = np.load(correct_bboxes_path, allow_pickle=True)  
    total_bboxes = np.load(total_bboxes_path, allow_pickle=True)  

    correct_count = len(correct_bboxes)  
    false_count = 0  

    total_bboxes_reversed = np.flip(total_bboxes, axis=1)  

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

# Plot the ROC curve
def plot_roc_curve(all_results, output_path):
    plt.figure()
    colors = ['blue', 'green', 'red', 'purple']  
    shapes = ['o', 's', 'D', '^']  
    labels_added = []  
    for result, shape, color in zip(all_results, shapes, colors):
        correct_rates, false_counts, min_object_sizes, label = result
        for i in range(len(correct_rates)):
            adjusted_false_count = false_counts[i]
            if label not in labels_added:
                plt.scatter(adjusted_false_count, correct_rates[i], marker=shape, label=label, color=color)
                labels_added.append(label)  
            else:
                plt.scatter(adjusted_false_count, correct_rates[i], marker=shape, color=color)
            plt.annotate(f'{min_object_sizes[i]}', (adjusted_false_count, correct_rates[i]))
    plt.xlabel('Average False Boxes')
    plt.ylabel('Correctly Marked Plants / Total Plants')
    plt.title('ROC Curve Day 5')
    plt.legend(loc='best')  
    plt.grid(True)  
    plt.savefig(output_path)  
    plt.show()  

# Collect results for different minimum object sizes
def collect_results(correct_bboxes_dir, total_bboxes_base_dir, label):
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

    return correct_rates, false_counts, min_object_sizes, label  


def main(output_path):
    correct_bboxes_dirs = [
        "D:/project/validate_sameday/CLD/masks",
        "D:/project/validate_sameday/CSD/masks",
        "D:/project/validate_sameday/LDtoSD/masks",
        "D:/project/validate_sameday/SDtoLD/masks"
    ]
    total_bboxes_base_dirs = [
        "D:/project/validate_sameday/CLD/image_edit",
        "D:/project/validate_sameday/CSD/image_edit",
        "D:/project/validate_sameday/LDtoSD/image_edit",
        "D:/project/validate_sameday/SDtoLD/image_edit"
    ]
    labels = ["CLD", "CSD", "LDtoSD", "SDtoLD"]

    all_results = []

    for correct_bboxes_dir, total_bboxes_base_dir, label in zip(correct_bboxes_dirs, total_bboxes_base_dirs, labels):
        result = collect_results(correct_bboxes_dir, total_bboxes_base_dir, label)
        all_results.append(result)

    plot_roc_curve(all_results, output_path)

if __name__ == "__main__":
    output_path = "D:/project/validate_new/roc_curve_all_categories.png"
    main(output_path)
