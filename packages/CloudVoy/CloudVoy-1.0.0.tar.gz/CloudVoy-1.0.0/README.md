# CloudVoy

CloudVoy is a Python library designed to automate the process of uploading YouTube videos to Instagram Reels. It fetches videos from a specified YouTube playlist, downloads them, uploads to AWS S3, and then publishes them as Instagram Reels using the Instagram Graph API. The library also tracks the upload status using AWS DynamoDB.

## Features

- **Fetch YouTube Playlist Videos**: Retrieve videos from a specified YouTube playlist.
- **Download Videos**: Download YouTube videos using `yt_dlp`.
- **Upload to AWS S3**: Store videos temporarily in AWS S3.
- **Publish to Instagram Reels**: Upload videos as Instagram Reels via the Instagram Graph API.
- **Track Upload Status**: Monitor upload status using AWS DynamoDB to prevent duplicate uploads.

## Installation

You can install CloudVoy via `pip`:

```bash
pip install CloudVoy
