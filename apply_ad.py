# import os
# from pathlib import Path

# import re 

# def sorted_nicely( l ): 
#     convert = lambda text: int(text) if text.isdigit() else text 
#     alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
#     return sorted(l, key = alphanum_key)

# fileSequence = 1
# folderSequence = 1
# current_working_dir = os.getcwd()

# for folder in os.listdir(current_working_dir):
# 	if folder != "rename.py" and folder != "System Volume Information" :
# 		f_unsorted = os.listdir(current_working_dir + "/" + str(folderSequence))
# 		for x in sorted_nicely(f_unsorted):
# 			print('ffmpeg -ss 0 -i "' + x + '" -t 6 output.mp3')
# 			# do editing...
# 			#1. clipping...
# 			os.system('ffmpeg -ss 0 -i "' + x + '" -t 6 output.mp3')
# 			fileSequence +=1
# 		# fnames = sorted(list(Path(os.listdir(current_working_dir + "\\" + str(folderSequence))).iterdir()), key=lambda path: int(path.stem))
# 		# os.listdir(current_working_dir + "\\" + str(folderSequence)).sort()
# 		# for filename in os.listdir(current_working_dir + "\\" + str(folderSequence)):
# 		# 	os.rename(current_working_dir + "\\" + str(folderSequence) +"\\"+ filename, str(fileSequence) + '.mp3')
# 		folderSequence +=1


# import os
# from pathlib import Path

# current_working_dir = os.getcwd()

# for folder in os.listdir(current_working_dir):
# 	if os.path.isdir(current_working_dir + "/" + folder) and folder != "Books" and folder != "Book":
# 		for mp3_audio in os.listdir(current_working_dir + "/" + folder):
# 			if(mp3_audio.endswith('.mp3')):
# 				print(mp3_audio)
# 				#clip audio....
# 				os.system('ffmpeg -i "' + current_working_dir + '/' + folder + '/' + mp3_audio + '" -ss 120 "' + mp3_audio + '"')

# 				#delete original file from place....
# 				os.remove(current_working_dir + '/' + folder + '/' + mp3_audio)

# 				#join ad with output file...
# 				os.system('ffmpeg -i ad.mp3 -i "' + mp3_audio + '" -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 -b:a 32k "' + current_working_dir + '/' + folder + '/' + mp3_audio + '"')
				
# 				#delete output file...
# 				os.remove(mp3_audio)


import json
import os
from pathlib import Path

current_working_dir = os.getcwd()

for folder in os.listdir(current_working_dir):
  if os.path.isdir(current_working_dir + "/" + folder) and folder != "Books" and folder != "Book":
    for mp3_audio in os.listdir(current_working_dir + "/" + folder):
      if mp3_audio.endswith('.mp3'):
        # Cut first 120 seconds
        os.system('ffmpeg -i "' + current_working_dir + '/' + folder + '/' + mp3_audio + '" -ss 0 -t 120 "front_' + mp3_audio + '"')

        # Append ad.mp3 to "front_ + mp3_audio"
        os.system('ffmpeg -i "front_' + mp3_audio + '" -i ad.mp3 -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" -b:a 64k "appended_' + mp3_audio + '"')

        # Get remaining portion of the original file (using ffseek)
        original_file_duration = os.popen('ffprobe -v quiet -show_format -print_format json -i "' + current_working_dir + '/' + folder + '/' + mp3_audio + '"').read()
        duration_dict = json.loads(original_file_duration)
        duration_in_seconds = float(duration_dict['format']['duration'])
        duration = int(duration_in_seconds)
        remaining_duration = duration - 120

        # Cut remaining portion using ffseek
        os.system('ffmpeg -i "' + current_working_dir + '/' + folder + '/' + mp3_audio + '" -ss 120 -t ' + str(remaining_duration) + ' "remaining_' + mp3_audio + '"')

        # Join "appended_ + mp3_audio" with "remaining_ + mp3_audio"
        os.system('ffmpeg -i "appended_' + mp3_audio + '" -i "remaining_' + mp3_audio + '" -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" -b:a 64k "' + current_working_dir + '/' + folder + '/' + mp3_audio + '"')

        # Cleanup temporary files
        os.remove("front_" + mp3_audio)
        os.remove("appended_" + mp3_audio)
        os.remove("remaining_" + mp3_audio)
        