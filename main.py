import modules as md
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.editor import VideoFileClip, AudioFileClip
from typing import Union
import os

def mkdir(path:str):
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print(f'Directory {path} already exists')

def rmdir(path:str):
	if os.path.exists(path):
		for file in os.listdir(path):
			file_path = os.path.join(path, file)
			if os.path.isfile(file_path):
				os.remove(file_path)
			elif os.path.isdir(file_path):
				rmdir(file_path)
	else:
		print(f'Directory {path} does not exist')

def download_best_quality_video(url):
	def get_video_and_audio(url:str, video_filename:Union[str, None]=None, audio_filename:Union[str, None]=None):
		if video_filename is None or audio_filename is None:
			video_filename = 'video.mp4'
			audio_filename = 'audio.mp4'
		else:
			if not video_filename.endswith('.mp4'):
				video_filename += '.mp4'
			if not audio_filename.endswith('.mp4'):
				audio_filename += '.mp4'
		yt = YouTube(url, on_progress_callback = on_progress)
		video_title = yt.title
		video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
		audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
		# video_filename = 'videos/components/'+ video_filename 
		# audio_filename = 'videos/components/'+ audio_filename 
		# print(video_filename)
		# print(audio_filename)
		video_stream.download(output_path="videos/components", filename=video_filename)
		audio_stream.download(output_path="videos/components",filename=audio_filename)
		video_filename = 'videos/components/'+ video_filename
		audio_filename = 'videos/components/'+ audio_filename
		return video_filename, audio_filename, video_title

	def join_video_stream(video_filename:str, audio_filename:str, output_filename:Union[str, None]):
		if output_filename is None:
			output_filename = 'output.mp4'
		if not output_filename.endswith('.mp4'):
			output_filename += '.mp4'
		video_clip = VideoFileClip(video_filename)
		audio_clip = AudioFileClip(audio_filename)

		final_clip = video_clip.set_audio(audio_clip)
		output_filename = str(output_filename).replace('/', ' ').replace('  ',' ')
		output_filename = output_filename.strip()
		final_clip.write_videofile('videos/'+output_filename, codec='libx264')

	mkdir('videos/components')
	video_filename, audio_filename, video_title = get_video_and_audio(url)
	join_video_stream(video_filename, audio_filename, output_filename=video_title)
	rmdir('videos/components')

if __name__ == '__main__':
	memes = [
		'https://www.youtube.com/watch?v=fe6lg0rqlHE',
		'https://www.youtube.com/watch?v=K9PGxyTsqLM',
		'https://www.youtube.com/watch?v=oS3HBWFciiA',
		'https://www.youtube.com/watch?v=6WR0-eOq5iY',
		'https://www.youtube.com/watch?v=l5txdFZxPag'
	]
	for meme in memes:
		download_best_quality_video(url=meme)
