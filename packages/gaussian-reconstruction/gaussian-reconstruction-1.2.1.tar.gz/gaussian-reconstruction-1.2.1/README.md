
# Gaussian Reconstruction

**Gaussian Reconstruction** is a Python package for 3D Gaussian splatting reconstruction from video inputs, designed for efficient and high-quality 3D model generation.

## Installation and Setup

Follow these steps to set up the environment and install the package.

### Step 1: Create the Conda Environment

First, create the `gaussian_splatting` environment using the provided `environment.yml` file:

```bash
conda env create -f gsrecon/environment.yml
```

### Step 2: Activate the Environment

Activate the newly created environment:

```bash
conda activate gaussian_splatting
```

### Step 3: Install Gaussian Reconstruction Package

Install the `gaussian-reconstruction` package using `pip`:

```bash
pip install gaussian-reconstruction
```

#### Additional Dependencies

To ensure successful operation, the following dependencies are required (these are included in the package requirements, but you may install them manually if needed):

- OpenCV (cv2): `pip install opencv-python`
- PyColmap: `pip install pycolmap`

## Usage

Once the package is installed, you can start the conversion process.

### Step 4: Import the Library

Import the `VideoToPLYConverter` class from the package:

```python
from gsrecon.converter import VideoToPLYConverter
```

### Step 5: Create a Converter Instance

Create an instance of `VideoToPLYConverter` with the desired method (e.g., `pycolmap`):

```
converter = VideoToPLYConverter(method='pycolmap')
```

### Step 6: Start the Conversion

Use the `convert_video_to_ply` function to start the conversion process. Provide the path to the video file and set the extraction rate (frames per second):

```
video_path = "path/to/your/video.mp4"  # Replace with your video file path
extraction_rate = None  # Set the frame extraction rate; defaults to None (extract all frames unless specified, e.g., 1 for 1 FPS)
converter.convert_video_to_ply(video_path, extraction_rate)
```

## License

This project is licensed under the terms specified in the LICENSE file.

---

This documentation provides a step-by-step guide to installing, setting up, and using the Gaussian Reconstruction package for 3D Gaussian splatting reconstruction.
```
