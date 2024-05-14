import os
import imageio
from django.shortcuts import render
from moviepy.editor import VideoFileClip
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def index(request):
    # Set the speed factor for slow-motion playback
    speed_factor = 0.5  # Example: Play at half speed

    # Path to the video file
    video_path = "static/sample.mp4"  # Replace with the actual path to your video

    # Load the video clip
    clip = VideoFileClip(video_path)

    # Get the size of the video file in bytes
    filesize = os.path.getsize(video_path)

    print(filesize)

    # Reduce the bitrate by 50%
    reduced_bitrate = filesize * 0.5

    # Apply the slow-motion effect
    slowed_clip = clip.speedx(factor=speed_factor)

    # Define the output path for the slowed video
    output_path = f"static/slow_motion_{speed_factor}x.mp4"

    # Write the slowed video to the output file with compression
    slowed_clip.write_videofile(output_path, codec='libx264', fps=clip.fps, bitrate=f'{int(reduced_bitrate)}')

    # Pass the output path to the template
    context = {'output_path': output_path}

    # Render the template with the output video path
    return render(request, 'videoplayerapp/index.html', context)


@csrf_exempt
def capture_frame(request):
    if request.method == 'GET':
        # Get the time from the request
        time_str = request.GET.get('time')
        if time_str is not None:
            try:
                time = float(time_str)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid time format'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Time parameter is missing'}, status=400)

        # Rest of your code to process the time parameter
        video_path = "static/slow_motion_0.5x.mp4"
        output_dir = "static/frames"
        os.makedirs(output_dir, exist_ok=True)
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(time)
        frame_path = os.path.join(output_dir, f"frame_{time}.jpg")
        imageio.imwrite(frame_path, frame)  # Save the frame as an image file

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
