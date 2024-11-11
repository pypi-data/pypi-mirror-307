import argparse
import subprocess
import os
from datetime import datetime

def is_recently_modified(file_path, delay_duration):
    """
    Check if a file was modified within the specified delay duration.

    Args:
        file_path (str): Path to the file.
        delay_duration (int): Delay duration in hours.

    Returns:
        bool: True if the file was modified within the delay duration, False otherwise.
    """
    # Get the timestamp of when the file was last modified
    modified_time = os.path.getmtime(file_path)

    # Calculate the cutoff timestamp for the delay duration
    delay_duration_seconds = delay_duration * 60 * 60
    cutoff_time = datetime.now().timestamp() - delay_duration_seconds

    # Check if the modified time is within the delay duration
    return modified_time > cutoff_time

def play_audio_if_needed(audio_file, delay_duration):
    # Generate a unique tracking file name based on the audio file name
    played_file_path = os.path.splitext(audio_file)[0] + "_played.txt"

    # Create the played file if it does not exist
    if not os.path.exists(played_file_path):
        with open(played_file_path, 'w') as f:
            f.write(datetime.now().isoformat())
        subprocess.run(["afplay", audio_file])
        return

    # Check if the played file was modified within the delay duration
    if not is_recently_modified(played_file_path, delay_duration):
        # Update the played file with the current timestamp
        with open(played_file_path, 'w') as f:
            f.write(datetime.now().isoformat())
        print(f"Playing: {audio_file}")

        # Run the subprocess to play the audio
        subprocess.run(["afplay", audio_file])
    else:
        print(f"Audio file '{audio_file}' was played within the last {delay_duration} hours. Skipping playback.")

def parse_arguments():
    """
    Parse command-line arguments using argparse.

    Returns:
        Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Play an MP3 file if it hasn't been played in the specified delay duration."
    )
    parser.add_argument(
        "audio_file",
        type=str,
        help="Path to the MP3 audio file."
    )
    parser.add_argument(
        "-d",
        "--delay-duration",
        type=int,
        default=3,
        help="Delay duration in hours to wait before playing the file again."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Validate the audio file path
    if not os.path.exists(args.audio_file):
        parser.error(f"Audio file '{args.audio_file}' does not exist.")
    if not args.audio_file.lower().endswith(".mp3"):
        parser.error("Only MP3 files are supported.")

    return args

if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

    # Play the audio if needed
    play_audio_if_needed(args.audio_file, args.delay_duration)
