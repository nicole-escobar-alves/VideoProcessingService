Feature: Video Processing

  Scenario: Sanitize a video
    Given a mock video "tests/mock_video.avi" with 5 frames
    When I sanitize the video and save as "tests/output_video.mp4"
    Then the file "tests/output_video.mp4" should exist

  Scenario: Extract frames and save zip file
    Given a mock video "tests/mock_video.avi" with 5 frames
    When I extract frames to "tests" with video id "video123"
    Then a zip file "tests/video123_frames.zip" should exist
