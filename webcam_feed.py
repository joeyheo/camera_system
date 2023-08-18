import v4l2
import fcntl
import mmap
import numpy as np
import os
import struct

def get_frame(fd, width, height):
    req = v4l2.v4l2_requestbuffers()
    req.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
    req.memory = v4l2.V4L2_MEMORY_MMAP
    req.count = 1

    fcntl.ioctl(fd, v4l2.VIDIOC_REQBUFS, req)

    buf = v4l2.v4l2_buffer()
    buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
    buf.memory = v4l2.V4L2_MEMORY_MMAP
    buf.index = 0

    fcntl.ioctl(fd, v4l2.VIDIOC_QUERYBUF, buf)

    mmapped_data = mmap.mmap(
        fd, buf.length, mmap.MAP_SHARED, mmap.PROT_READ, offset=buf.m.offset
    )

    fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)
    fcntl.ioctl(fd, v4l2.VIDIOC_STREAMON, v4l2.v4l2_buf_type(v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE))

    while True:
        fcntl.ioctl(fd, v4l2.VIDIOC_DQBUF, buf)
        raw_frame = np.frombuffer(mmapped_data, dtype=np.uint8, count=width * height).reshape((height, width))
        yield raw_frame

        fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)

def main():
    width, height = 640, 480
    webcam_path = '/dev/video0'  # Adjust this path based on your system

    # Open the webcam device
    fd = os.open(webcam_path, os.O_RDWR)

    frame_generator = get_frame(fd, width, height)

    for frame in frame_generator:
        # You can do whatever you want with each frame here
        # For this example, let's print the frame size
        frame_size = struct.calcsize('B') * len(frame)
        print(f'Frame size: {frame_size} bytes')

    os.close(fd)

if __name__ == '__main__':
    main()
