import torch

import torch
from model import MattingNetwork


model = MattingNetwork('mobilenetv3').eval().cuda()  # or "resnet50"
model.load_state_dict(torch.load('res/rvm_mobilenetv3.pth'))

from inference import convert_video

input_file = 'lecexample000_5fps_fwd'
input_source = 'downloads/' + input_file + '.mp4'
output_composition = 'downloads/' + input_file + '.com.mp4'
output_alpha = 'downloads/' + input_file + '.pha.mp4'
output_foreground = 'downloads/' + input_file + '.fgr.mp4'

convert_video(
    model,                           # The model, can be on any device (cpu or cuda).
    input_source,        # A video file or an image sequence directory.
    output_type='video',             # Choose "video" or "png_sequence"
    output_composition=output_composition,    # File path if video; directory path if png sequence.
    output_alpha=output_alpha,          # [Optional] Output the raw alpha prediction.
    output_foreground=output_foreground,     # [Optional] Output the raw foreground prediction.
    output_video_mbps=4,             # Output video mbps. Not needed for png sequence.
    downsample_ratio=None,           # A hyperparameter to adjust or use None for auto.
    seq_chunk=12,                    # Process n frames at once for better parallelism.
)
