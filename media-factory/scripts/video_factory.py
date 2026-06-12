import sys
import subprocess
import os
import argparse

def create_video(audio_path, image_path, output_path, mode="cinema", fps=30):
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return

    # Check for ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is not installed or not in PATH.")
        return

    # Define filter based on mode
    filter_complex = ""
    if mode == "blur":
        # Square to 16:9 with blurred background
        filter_complex = (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=20:10[bg];"
            "[0:v]scale=-1:1000[fg];" 
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        )
    elif mode == "cinema":
        # Fill screen (crop to fit 1920x1080)
        filter_complex = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
    elif mode == "fit":
        # Fit inside 1920x1080 with black bars
        filter_complex = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"

    cmd = [
        "ffmpeg",
        "-y", 
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path
    ]
    
    if filter_complex:
        cmd.extend(["-filter_complex" if mode == "blur" else "-vf", filter_complex])
        
    cmd.extend([
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac", 
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest", 
        "-r", str(fps),
        output_path
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully created video ({mode} mode): {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating video: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a video from a static image and an audio file.")
    parser.add_argument("audio", help="Path to the input audio file")
    parser.add_argument("image", help="Path to the input image file")
    parser.add_argument("output", help="Path to the output video file")
    parser.add_argument("--mode", choices=["cinema", "blur", "fit"], default="cinema", help="Video rendering mode (cinema=fill, blur=bg-effect, fit=black-bars)")
    
    args = parser.parse_args()
    
    create_video(args.audio, args.image, args.output, mode=args.mode)
