# python converter.py -v C0010.MP4 -fps 1
import os
import argparse
import cv2
import math
import pycolmap
from tqdm import tqdm
#import distortion
from . import distortion
import time
import shutil
from pathlib import Path
from .train import training
from .arguments import ModelParams, ArgumentParser, OptimizationParams, PipelineParams


def measure_elapsed_time():
    start_time = time.time()

    def get_elapsed_time():
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        remaining_seconds = int(elapsed_time % 60)

        return f"Elapsed time: {hours} hrs {minutes} mins {remaining_seconds:.2f} secs"

    return get_elapsed_time


class VideoToPLYConverter:
    def __init__(self, method='pycolmap'):
        self.method = method

    # def convert_video_to_ply(self, video_path, fps, skip_ba):

    def convert_video_to_ply(self, video_path, fps):
        # Get the directory and filename without extension
        # directory = os.path.dirname(video_path)
        directory = os.getcwd()  # main dir
        filename = os.path.splitext(os.path.basename(video_path))[0]

        # Define the output file folder
        ply_path = Path(directory) / filename
        ply_path.mkdir(parents=True, exist_ok=True)  # filename

        if self.method == 'pycolmap':
            self._convert_using_pycolmap(video_path, ply_path, fps)
        # elif self.method ==
        else:
            raise ValueError("Invalid method.")

    def _extract_frames(self, image_dir, video_path, target_fps=None):
        # pre-define the maxmium frames extracted from the video
        max_frames = 500

        video = cv2.VideoCapture(video_path)

        if not video.isOpened():
            print("Error: Could not open video.")
            return

        original_fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / original_fps
        # print(f"The video has an original fps of {original_fps} and total frames of {total_frames}")

        fps_to_use = target_fps if target_fps else round(max_frames / video_duration, 2)

        skip_frames = math.ceil(original_fps / fps_to_use)
        expected_frames = math.ceil(total_frames / skip_frames)

        # print(f"Extracting at a rate of {fps_to_use} and total frames of {expected_frames}")

        frame_count = 0
        saved_frame_idx = 0
        with tqdm(total=expected_frames, desc="Extracting frames", unit="frame") as pbar:
            while video.isOpened():
                ret, frame = video.read()
                if not ret:  # No more frames or error
                    break

                if frame_count % skip_frames == 0:
                    frame_filename = f"{image_dir}/{saved_frame_idx:04d}.jpg"
                    cv2.imwrite(frame_filename, frame)
                    saved_frame_idx += 1
                    pbar.update(1)

                frame_count += 1

        video.release()
        print(f"Extracted {saved_frame_idx} frames")

    def _convert_using_pycolmap(self, video_path, ply_path, fps):
        # Create necessary directories
        work_dir = os.path.join(ply_path, "data")  # filename/data
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)

        image_dir = os.path.join(work_dir, "images")  # filename/data/images

        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)
        os.makedirs(image_dir)

        # extract frames from input and save as images
        self._extract_frames(image_dir, video_path, fps)

        distorted_path = os.path.join(work_dir, "distorted")  # filename/data/distorted
        database_path = os.path.join(distorted_path, "database.db")  # filename/data/distorted/database.db
        sparse_path = os.path.join(distorted_path, "sparse")  # filename/data/distorted/sparse
        os.makedirs(distorted_path + "/sparse", exist_ok=True)

        if os.path.exists(database_path):
            os.remove(database_path)

        '''
        extract_features()
        The following argument types are supported:
            database_path: str, 
            image_path: str, 
            image_list: List[str] = [], 
            camera_mode: pycolmap.CameraMode = <CameraMode.AUTO: 0>, 
            camera_model: str = 'SIMPLE_RADIAL', 'PINHOLE'
            reader_options: pycolmap.ImageReaderOptions = <pycolmap.ImageReaderOptions object at 0x7f84459de730>, 
            sift_options: pycolmap.SiftExtractionOptions = <pycolmap.SiftExtractionOptions object at 0x7f84459de6b0>, 
            device: pycolmap.Device = <Device.auto: -1>) -> None
        '''
        pycolmap.extract_features(
            database_path,
            image_dir,
            camera_model='PINHOLE',
            sift_options={"max_num_features": 512, "gpu_index": '0'}
        )
        print("--------------------------- Extract features DONE ---------------------------")

        '''
        match_exhaustive()
        The following argument types are supported:
            database_path: str, 
            sift_options: pycolmap.SiftMatchingOptions = <pycolmap.SiftMatchingOptions object at 0x7ff0929d80f0>, 
            matching_options: pycolmap.ExhaustiveMatchingOptions = <pycolmap.ExhaustiveMatchingOptions 
        '''
        pycolmap.match_exhaustive(
            database_path,
            sift_options={"gpu_index": '0'}
        )
        print("--------------------------- Match features DONE ---------------------------")

        # incremental mapping
        maps = distortion.perform_bundle_adjustment(
            database_path,
            image_dir,
            distorted_path + '/sparse'
        )
        maps[0].write(work_dir)
        print("--------------------------- Incremental Mapping DONE ---------------------------")

        # Undistortion does not needed when camera model is SIMPLE_PINHOLE or PINHOLE
        # pycolmap.undistort_images(work_dir, sparse_path+'/0', image_dir)
        # print("--------------------------- Image Undistortion DONE ---------------------------")

        # If undistort_images() is called, manage the files into the right directory for training
        # self._manage_files(work_dir)
        # print("--------------------------- Manage files DONE ---------------------------")

        # resize images
        # for img_name in tqdm(os.listdir(image_dir), desc="Resizing images", unit="image"):
        #     img_path = os.path.join(image_dir, img_name)
        #     try:
        #         with Image.open(img_path) as img:
        #             img = img.resize((980, 545), Image.LANCZOS)
        #             img.save(img_path)  # Overwrite the larger image
        #     except Exception as e:
        #         print(f"Error processing {img_name}: {str(e)}")

        # print("--------------------------- Image resizing DONE ---------------------------")

        self._run_training(ply_path)
        print("--------------------------- Training process DONE ---------------------------")

    def _run_training(self, ply_path):
        print("--------------------------- Starting Training Process ---------------------------")

        # Define training parameters
        parser2 = ArgumentParser(description="Training script parameters")
        dataset = ModelParams(parser2)
        op = OptimizationParams(parser2)
        pp = PipelineParams(parser2)
        parser2.add_argument('--ip', type=str, default="127.0.0.1")
        parser2.add_argument('--port', type=int, default=6009)
        parser2.add_argument('--debug_from', type=int, default=-1)
        parser2.add_argument('--detect_anomaly', action='store_true', default=False)
        # parser2.add_argument("--testing_iterations", nargs="+", type=int, default=[30_000])
        # parser2.add_argument("--save_iterations", nargs="+", type=int, default=[1_000])
        parser2.add_argument("--save_iterations", nargs="+", type=int, default=[30_000, 70_000])
        parser2.add_argument("--quiet", action="store_true")
        parser2.add_argument("--checkpoint_iterations", nargs="+", type=int, default=[])
        parser2.add_argument("--start_checkpoint", type=str, default=None)
        parser2.add_argument("--saved_ply_path", type=str, default=ply_path)
        args2 = parser2.parse_args([])

        training(dataset.extract(args2),
                 op.extract(args2),
                 pp.extract(args2),
                 args2.save_iterations,
                 args2.checkpoint_iterations,
                 args2.start_checkpoint,
                 args2.debug_from,
                 args2.saved_ply_path)

        # # Assuming the training process generates a .ply file, return its path
        # result_path = os.path.join(dataset, "trained_model", "point_cloud.ply")

        # return result_path


# def main():
#     parser = argparse.ArgumentParser(description='Convert video to PLY file')
#     parser.add_argument('-v', '--video_path', type=str, help='Path to the input video file', required=True)
#     parser.add_argument('-fps', '--frame_rate', help="Extraction frame rate from the video", required=False, type=float)
#     # parser.add_argument('-ba', '--skip_ba', help="Skip incremental mapping and global bundle adjusement process",
#     #                     required=False, default=0, type=int)
#
#     args = parser.parse_args()
#
#     timer = measure_elapsed_time()
#
#     converter = VideoToPLYConverter(method='pycolmap')
#     try:
#         # output_ply = converter.convert_video_to_ply(args.video_path, args.frame_rate, args.skip_ba)
#         output_ply = converter.convert_video_to_ply(args.video_path, args.frame_rate)
#         # print(f"Conversion successful. PLY file created at: {output_ply}")
#     except Exception as e:
#         print(f"Error: {str(e)}")
#
#     print(timer())
#
#
# if __name__ == "__main__":
#     main()

