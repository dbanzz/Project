import torch

from argparse import ArgumentParser

from unet.utils import *
from unet.unet import UNet

parser = ArgumentParser()
parser.add_argument("--images_path", type=str, required=True)
parser.add_argument("--model", type=str, required=True)
parser.add_argument("--result_folder", type=str, required=True)
parser.add_argument("--device", type=str, default='cuda')
parser.add_argument("--min_object_size_range", type=tuple, default=(2,20))
parser.add_argument("--max_object_size", type=float, default=np.inf)
parser.add_argument("--dpi", type=float, default=False)
parser.add_argument("--dpm", type=float, default=False)
parser.add_argument("--visualize", type=bool, default=False)
args = parser.parse_args()

# determining dpm
dpm = args.dpm if not args.dpi else dpi_to_dpm(args.dpi)

print("Loading dataset...")
predict_dataset = ReadTestDataset(args.images_path)
device = torch.device(args.device)
print("Dataset loaded")

print("Loading model...")
unet = UNet(3, 3)
unet.load_state_dict(torch.load(args.model, map_location=device))
model = ModelWrapper(unet, args.result_folder, cuda_device=device)
print("Model loaded")
min_object_size_range = range(args.min_object_size_range[0], args.min_object_size_range[1] + 1)

for min_object_size in min_object_size_range:
        result_folder = os.path.join(args.result_folder, f"min_object_size_{min_object_size}")
        os.makedirs(result_folder, exist_ok=True)
        print(f"Measuring images with min_object_size={min_object_size}...")
        model.measure_large_images(predict_dataset, export_path=result_folder,
                                   visualize_bboxes=args.visualize, filter=[min_object_size, args.max_object_size],
                                   dpm=dpm, verbose=True, tile_res=(256, 256))
