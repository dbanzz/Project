import os
from skimage import io

def convert_tif_to_png(src_folder):
    """
    Convert all .tif images in each subfolder of the src_folder to .png format.

    Parameters:
    src_folder (str): The source folder containing subfolders with .tif images.

    Returns:
    None
    """
    for subdir in os.listdir(src_folder):
        subdir_path = os.path.join(src_folder, subdir)
        if os.path.isdir(subdir_path):
            for filename in os.listdir(subdir_path):
                if filename.lower().endswith('.tif'):
                    img_path = os.path.join(subdir_path, filename)
                    img = io.imread(img_path)
                    new_filename = os.path.splitext(filename)[0] + '.png'
                    new_img_path = os.path.join(subdir_path, new_filename)
                    io.imsave(new_img_path, img)
                    print(f"Converted {img_path} to {new_img_path}")

src_folder = r'D:\project\validate1'
convert_tif_to_png(src_folder)
