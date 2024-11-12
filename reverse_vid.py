import ffmpeg

file_fwd       = 'downloads/lecexample000_5fps_fwd.mp4'
file_fwd_alpha = 'downloads/lecexample000_5fps_fwd.pha.mp4'

out_file_rev       = 'downloads/lecexample000_5fps_rev.mp4'
out_file_rev_alpha = 'downloads/lecexample000_5fps_rev.pha.mp4'

ffmpeg.input(file_fwd).output(out_file_rev, vf='reverse').run()
ffmpeg.input(file_fwd_alpha).output(out_file_rev_alpha, vf='reverse').run()
