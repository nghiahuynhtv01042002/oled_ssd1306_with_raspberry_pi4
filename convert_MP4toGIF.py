from moviepy.editor import VideoFileClip

# Tải video MP4
video = VideoFileClip("gifDisplay.mp4")

# Thay đổi kích thước video
video_resized = video.resize(newsize=(480,1068))

# Chuyển đổi video đã thay đổi kích thước thành GIF
video_resized.write_gif("gifDisplay.gif")
