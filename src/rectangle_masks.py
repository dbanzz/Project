import os
import numpy as np
from skimage import io, measure
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def get_bounding_boxes(mask, threshold=128):
    labeled_mask = measure.label(mask > threshold)
    bbox_list = []
    for region in measure.regionprops(labeled_mask):
        min_row, min_col, max_row, max_col = region.bbox
        bbox_list.append((min_col, min_row, max_col, max_row))
    return bbox_list

def plot_and_save_bounding_boxes(mask_path, output_image_path, output_data_path):
    # Load mask
    mask = io.imread(mask_path)

    # Get bounding boxes
    bboxes = get_bounding_boxes(mask)

    # Save bounding box data
    np.save(output_data_path, bboxes)

    # Plot and save the mask with bounding boxes
    fig, ax = plt.subplots()
    ax.imshow(mask, cmap='gray')
    for bbox in bboxes:
        min_col, min_row, max_col, max_row = bbox
        rect = Rectangle((min_col, min_row), max_col - min_col, max_row - min_row,
                         linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.axis('off')
    plt.savefig(output_image_path, bbox_inches='tight')
    plt.close(fig)

def process_directory(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith("-hypo.png"):
            base_name = filename[:-9]  # Remove the '-hypo.png' part
            mask_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(output_dir, f"{base_name}_bboxes.png")
            output_data_path = os.path.join(output_dir, f"{base_name}_bboxes.npy")

            print(f"Processing {filename}...")
            plot_and_save_bounding_boxes(mask_path, output_image_path, output_data_path)

# Paths
input_dir = "D:/project/validate_sameday/"
output_dir = "D:/project/validate_sameday/"

# Process all images in the directory
process_directory(input_dir, output_dir)
