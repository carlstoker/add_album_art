#!/usr/bin/env python3
"""
Add album art in a directory to all MP3 and FLAC files contained within that directory.

usage: add_album_art.py PATH
"""
import os
import shutil
import subprocess
import sys
import tempfile


def add_album_art(path):
    """
    Search for cover.jpg in a directory. If found, add it to all MP3 and FLAC audio
    files within that directory.

    Keyword arguments:
        path -- working directory for adding album art
    """
    cover_path = os.path.abspath(os.path.join(path, 'cover.jpg'))

    if os.path.isfile(cover_path):
        files = [f for f in os.listdir(path) if
                 os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1].lower() in ['.mp3', '.flac']]

        for audio_filename in files:
            add_art_to_file(os.path.join(path, audio_filename), cover_path)
    else:
        print('cover.jpg not found in {}!  Skipping.'.format(path))

    return None


def add_art_to_file(audio_filename, cover_path):
    """
    Add album art to an individual file.

    Keyword arguments:
        audio_filename -- Filename of audio file.
        cover_path -- Filename of cover

    """
    print('Adding cover.jpg to {}'.format(os.path.basename(audio_filename)))

    with tempfile.TemporaryDirectory() as temp_directory:
        command = [
            'ffmpeg',
            '-i', audio_filename,
            '-i', cover_path,
            '-c', 'copy',
            '-map', '0:0',
            '-map', '1:0',
            '-id3v2_version', '3',
            '-metadata:s:v', 'title="Album cover"',
            '-metadata:s:v', 'comment="Cover (front)"',
            '-v', "error",
            os.path.join(temp_directory, os.path.basename(audio_filename))
        ]
        subprocess.call(command)
        shutil.move(os.path.join(temp_directory, os.path.basename(audio_filename)), audio_filename)
        return None


if __name__ == "__main__":
    add_album_art(sys.argv[1])
