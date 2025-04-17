import os
import sys
import cv2
import numpy as np
from behave import given, when, then

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.processor import sanitize_video, extract_frames_to_zip

@given('a mock video "{video_path}" with {num_frames:d} frames')
def step_impl(context, video_path, num_frames):
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path, fourcc, 10.0, (640, 480))

    for _ in range(num_frames):
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        out.write(frame)

    out.release()
    context.video_path = video_path

@when('I sanitize the video and save as "{output_path}"')
def step_impl(context, output_path):
    sanitize_video(context.video_path, output_path)
    context.sanitized_video_path = output_path

@then('the file "{expected_path}" should exist')
def step_impl(context, expected_path):
    assert os.path.exists(expected_path), f"File {expected_path} was not created."

@when('I extract frames to "{root_path}" with video id "{video_id}"')
def step_impl(context, root_path, video_id):
    zip_path = extract_frames_to_zip(video_id, root_path, context.video_path)
    context.zip_path = zip_path

@then('a zip file "{expected_zip_path}" should exist')
def step_impl(context, expected_zip_path):
    assert os.path.exists(expected_zip_path), f"Zip file {expected_zip_path} was not created."
