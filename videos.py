import pipeline as ppl
from moviepy.editor import VideoFileClip
from IPython.display import HTML

def process_image(image):
    img = ppl.pipeline(image)
    return img

white_output = 'test_videos_output/solidWhiteRight.mp4'
clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
white_clip = clip1.fl_image(process_image)
white_clip.write_videofile(white_output, audio=False)

yellow_output = 'test_videos_output/solidYellowLeft.mp4'
clip2 = VideoFileClip("test_videos/solidYellowLeft.mp4")
yellow_clip = clip2.fl_image(process_image)
yellow_clip.write_videofile(yellow_output, audio=False)

challenge_output = 'test_videos_output/challenge.mp4'
clip3 = VideoFileClip("test_videos/challenge.mp4")
challenge_clip = clip3.fl_image(process_image)
challenge_clip.write_videofile(challenge_output, audio=False)
