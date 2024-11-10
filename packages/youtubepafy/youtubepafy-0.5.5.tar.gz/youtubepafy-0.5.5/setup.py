# setup.py
import os
from setuptools import setup

# Read the version from version.py
version = {}
with open(os.path.join(os.path.dirname(__file__), 'youtubepafy', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='youtubepafy',
    packages=['youtubepafy'],
    # Remove the scripts line if not needed
    # scripts=['scripts/ytdl'],
    version=version['__version__'],
    description="Retrieve YouTube content and metadata",
    keywords=["youtubepafy", "API", "YouTube", "youtube", "download", "video", "Het Saraiya", "hetsaraiya"],
    author="Het Saraiya",
    author_email="hetsaraiya06@gmail.com",
    url="https://github.com/hetsaraiya/youtubepafy",
    download_url="https://github.com/hetsaraiya/youtubepafy/tags",
    install_requires=[
        'yt_dlp',
    ],
    extras_require={
        'youtube-dl-backend': ["youtube-dl"],
    },
    package_data={"": ["LICENSE", "README.rst", "CHANGELOG", "AUTHORS"]},
    include_package_data=True,
    license='LGPLv3',
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS 9",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows XP",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP"
    ],
    long_description=open("README.rst").read(),
    long_description_content_type='text/x-rst'
)