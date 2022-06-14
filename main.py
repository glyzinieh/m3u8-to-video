import m3u8
from moviepy.editor import *
from tqdm import tqdm


def main(file: str,base_uri: str=str()) -> VideoClip:
	playlist = m3u8.load(file)
	playlist.base_uri = base_uri
	segments = playlist.segments
	bar = tqdm(total=len(segments))
	bar.set_description('Download')
	clips = list()
	for segment in segments:
		segment: m3u8.Segment
		uri = segment.absolute_uri
		clips.append(VideoFileClip(uri))
		bar.update(1)
	bar.close()
	final_clip = concatenate_videoclips(clips)
	return final_clip

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('in_file',help='m3u8ファイル名')
	parser.add_argument('out_file',help='出力ファイル名')
	parser.add_argument('-b','--base_uri')
	args = parser.parse_args()

	clip = main(args.in_file,args.base_uri)
	clip.write_videofile(
		args.out_file,
    	remove_temp=True
	)
