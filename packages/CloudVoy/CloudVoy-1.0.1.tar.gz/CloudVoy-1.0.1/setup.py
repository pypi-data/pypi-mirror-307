from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
setup(
    name='CloudVoy',
    version='1.0.1',
    description='A library to upload YouTube videos to Instagram Reels automatically.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'yt-dlp',
        'boto3',
        'requests',
        'python-dotenv'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
