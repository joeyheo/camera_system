# Misung Webcam Watermarking with OpenCV

This program captures a live video feed from the default webcam, applies a watermark to each frame, and then displays the watermarked video in real-time.

## Prerequisites

- Python 3
- OpenCV for Python (`opencv-python` package)

## Setup

1. Ensure you have Python 3 and OpenCV installed.

   You can install OpenCV using pip:

   ```bash
   pip install opencv-python
   ```

2. Clone/download the script to your machine.

3. Obtain a PNG watermark image. If your watermark image has a transparent background, the script will handle it correctly.

4. Update the placeholder path `"/path/to/your/watermark.png"` in the `main()` function with the actual path to your watermark image.

## Usage

Run the script with:

```bash
python webcam_feed.py
```

This will open a window displaying the live video feed from the default webcam with the watermark applied. To exit the live feed and close the window, press the `q` key.

## How It Works

- **add_watermark(frame, watermark_image_path)**: This function takes a video frame and the path to a watermark image as its arguments. It then processes the watermark (if it has transparency), places it on the bottom-right corner of the frame, and blends the two images together.

- **main()**: This is the main driver function. It initializes the webcam, captures each frame, applies the watermark, and then displays the watermarked frame. It runs in a continuous loop until the user presses the `q` key.

## Notes

- The position and transparency level of the watermark are hardcoded in the `add_watermark` function. You can adjust them as needed.
- If the webcam isn't available or there's an issue accessing it, the script will print "Could not open webcam!" and exit.
