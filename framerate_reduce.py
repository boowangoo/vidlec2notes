import ffmpeg

in_file = 'res/lecexample000.mp4'

out_file = 'downloads/lecexample000_5fps_fwd.mp4'

ffmpeg.input(in_file).output(out_file, vf='fps=5').run()
