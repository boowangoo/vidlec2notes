import cv2
import numpy as np

from cv2.typing import MatLike

def process(cap_vidO, cap_vidA, out_fileO, out_fileA):
    # Check if videos opened successfully
    if not cap_vidO.isOpened() or not cap_vidA.isOpened():
        print("Error: Could not open one or both videos.")
        exit()

    frame_count = int(cap_vidO.get(cv2.CAP_PROP_FRAME_COUNT))
    curr_frame = 0
    
    frame_width = int(cap_vidO.get(3))
    frame_height = int(cap_vidO.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'x264' might work as well
    out_writerO = cv2.VideoWriter(out_fileO, fourcc, 5, (frame_width, frame_height))
    out_writerA = cv2.VideoWriter(out_fileA + '.new.mp4', fourcc, 5, (frame_width, frame_height))
    
    # Variables to hold previous frames
    prev_frame_vidO = None
    prev_frame_vidA = None
    prev_new_frame_vid = None

    # Loop through each frame
    while True:
        if (curr_frame % 100 == 0):
            print(f"Frame {curr_frame} of {frame_count}")
        retO, frame_vidO = cap_vidO.read()  # Read frame from VidO
        retA, frame_vidA = cap_vidA.read()  # Read frame from VidA


        curr_frame += 1

        # print(f"Frame {curr_frame} of {frame_count}")

        # Break the loop if there are no frames left
        if not retO or not retA:
            break

        frame_vidA = cv2.cvtColor(frame_vidA, cv2.COLOR_BGR2GRAY)
        # print("01:" + str(frame_vidA.shape))

        # Initialize prev_frame_vidO with the first frame
        if prev_frame_vidO is None:
            prev_frame_vidO = frame_vidO
            prev_frame_vidA = frame_vidA
            prev_new_frame_vid = np.zeros_like(frame_vidA)
            continue

        absA = cv2.convertScaleAbs(frame_vidA)
        diff = cv2.absdiff(frame_vidA, prev_frame_vidA)

        # print("02:" + str(diff.shape))

        fgr = absA > 0 # Identify where the foreground is
        lighter = (diff > 0)  # Identify where changes are lighter

        # print("03:" + str(lighter.shape))
        # print("04:" + str(frame_vid_hist[-1].shape))

        # Replace sections where the frame has become lighter, or is light (ie the foreground)
        frame_vidO[lighter|fgr] = prev_frame_vidO[lighter|fgr]

        new_frame_vid = prev_new_frame_vid
        new_frame_vid[lighter|fgr] += 10
        new_frame_vid[lighter|fgr] = np.clip(new_frame_vid[lighter|fgr], 0, 255)
        new_frame_vid[~(lighter|fgr)] = 0

        # frame_vid_hist[lighter|fgr] += 1
        # frame_vid_hist[~(lighter|fgr)] = 0

        # # Update previous frame
        prev_frame_vidO = frame_vidO
        prev_frame_vidA = frame_vidA

        out_writerO.write(frame_vidO)
        out_writerA.write(cv2.cvtColor(new_frame_vid, cv2.COLOR_GRAY2BGR))

        # Display the result (optional)
        # cv2.imshow('Result', frame_vidO)
        # if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to quit
        #     break
        # print("save")
        # np.save(out_fileO + '.hist.npy', frame_vid_hist)
    cap_vidO.release()
    cap_vidA.release()

# # Initialize video capture for both videos
print("Processing fwd:")
cap_vidFwdO = cv2.VideoCapture('downloads/lecexample000_5fps_fwd.mp4')
cap_vidFwdA = cv2.VideoCapture('downloads/lecexample000_5fps_fwd.pha.mp4')
out_fwd_fileO = 'downloads/lecexample000_nofgr_5fps_fwd.mp4'
out_fwd_fileA = 'downloads/lecexample000_nofgr_5fps_fwd.pha.mp4'
# process(cap_vidFwdO, cap_vidFwdA, out_fileO=out_fwd_fileO, out_fileA=out_fwd_fileA)

print("Processing rev:")
cap_vidRevO = cv2.VideoCapture('downloads/lecexample000_5fps_rev.mp4')
cap_vidRevA = cv2.VideoCapture('downloads/lecexample000_5fps_rev.pha.mp4')
out_rev_fileO = 'downloads/lecexample000_nofgr_5fps_rev.mp4'
out_rev_fileA = 'downloads/lecexample000_nofgr_5fps_rev.pha.mp4'
# process(cap_vidRevO, cap_vidRevA, out_fileO=out_rev_fileO, out_fileA=out_rev_fileA)


cap_vidFwd = cv2.VideoCapture(out_fwd_fileO)
cap_vidFwdNew = cv2.VideoCapture(out_fwd_fileA + '.new.mp4')
# cap_vidFwdA = cv2.VideoCapture(out_fwd_fileA)
cap_vidRev = cv2.VideoCapture(out_rev_fileO)
cap_vidRevNew = cv2.VideoCapture(out_rev_fileA + '.new.mp4')
# cap_vidRevA = cv2.VideoCapture(out_rev_fileA)

frame_width = int(cap_vidFwd.get(3))
frame_height = int(cap_vidFwd.get(4))
resized_dim = (frame_width // 3, frame_height // 3)
double_dim = (2 *(frame_width // 3), 2 * (frame_height // 3))

curr_frame_fwd = 0
curr_frame_rev = int(cap_vidRev.get(cv2.CAP_PROP_FRAME_COUNT))-1

while True:
    cap_vidRev.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_rev)
    cap_vidRevNew.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_rev)

    retFwd, frame_vidFwd = cap_vidFwd.read()  # Read frame from VidFwd
    retRev, frame_vidRev = cap_vidRev.read()  # Read frame from VidRev
    # retFwdA, frame_vidFwdA = cap_vidFwdA.read()  # Read frame from VidFwdA
    # retRevA, frame_vidRevA = cap_vidRevA.read()  # Read frame from VidRevA

    # retFwdNew, frame_vidFwdNew = cap_vidFwdNew.read()  # Read frame from VidFwdNew
    # retRevNew, frame_vidRevNew = cap_vidRevNew.read()  # Read frame from VidRevNew

    # Break the loop if there are no frames left
    if not retFwd or not retRev:
        break
    # if not retFwdNew or not retRevNew:
    #     break

    # frame_vidFwdNew = cv2.cvtColor(frame_vidFwdNew, cv2.COLOR_BGR2GRAY)
    # frame_vidRevNew = cv2.cvtColor(frame_vidRevNew, cv2.COLOR_BGR2GRAY)

    # replace_rev = frame_vidFwdNew >= frame_vidRevNew
    # new_frame = frame_vidRev.copy()
    # new_frame[replace_rev] = frame_vidFwd[replace_rev]

    grayFwd = cv2.cvtColor(frame_vidFwd, cv2.COLOR_BGR2GRAY)
    grayRev = cv2.cvtColor(frame_vidRev, cv2.COLOR_BGR2GRAY)

    edgesFwd = cv2.Canny(grayFwd, 100, 200)
    edgesRev = cv2.Canny(grayRev, 100, 200)

    sum_edgesFwd = np.sum(edgesFwd)
    sum_edgesRev = np.sum(edgesRev)

    # _, threshFwd = cv2.threshold(grayFwd, 0, 255, cv2.THRESH_BINARY)
    # _, threshRev = cv2.threshold(grayRev, 0, 255, cv2.THRESH_BINARY)

    # contoursFwd, _ = cv2.findContours(threshFwd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contoursRev, _ = cv2.findContours(threshRev, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # areaFwd = sum([cv2.contourArea(c) for c in contoursFwd])
    # areaRev = sum([cv2.contourArea(c) for c in contoursRev])

    # best_frame = frame_vidFwd if sum_edgesFwd > sum_edgesRev and areaFwd > areaRev else frame_vidRev
    best_frame = frame_vidFwd if sum_edgesFwd > sum_edgesRev else frame_vidRev

    framesO = cv2.hconcat([cv2.resize(frame_vidFwd, resized_dim), cv2.resize(frame_vidRev, resized_dim)])

    cv2.imshow('Fwd - Rev', cv2.vconcat([framesO, cv2.resize(best_frame, double_dim)]))
    # cv2.imshow('Fwd - Rev', framesO)
    if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to quit
        break

    curr_frame_rev -= 1
    curr_frame_fwd += 1

cap_vidFwd.release()
cap_vidFwdA.release()
cap_vidRev.release()
cap_vidRevA.release()

# Release the video capture objects and close all windows
cv2.destroyAllWindows()
