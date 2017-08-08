#Recording code
#Brian Levitt
#7/24/17

#!/bin/bash
now=$(date +%m-%d-%Y_%H-%M-%S)
#now="video1" ##Test

sudo raspivid -o /mnt/TrippwireVideos/$now.h264 -t 30000 -w 1280 -h 720 -fps 8 -n
cd ../
cd /mnt/TrippwireVideos/
sudo MP4Box -add $now.h264:fps=32 $now.mp4
echo "TESTME"
sudo rm $now.h264
echo "RARA"
exit
echo "AFTER EXIT"
