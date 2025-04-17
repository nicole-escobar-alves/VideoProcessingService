Feature: S3 Upload and Download

  Scenario: Download a video file from S3
    Given a video is uploaded to S3
    When I download the video
    Then the file should exist

  Scenario: Upload a zip file to S3
    Given a zip file
    When I upload the zip to S3 for user with original key
    Then the zip file should be uploaded to S3 with the correct key
