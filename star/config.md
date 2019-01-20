# Config

## gstreamer
```
gst-launch-1.0 rtspsrc location=rtsp://root:itlabcsyang92633@10.27.164.152/live3.sdp ! decodebin ! x264enc bitrate=256 tune=zerolatency ! h264parse ! flvmux name=mux streamable=true ! queue ! rtmpsink location='rtmp://140.116.215.203:1935/itlab/demo live=1'
```

## rpi
```
ffmpeg -rtsp_transport tcp -i rtsp://10.27.164.151:5000/unicast \
-flags +low_delay  -tune zerolatency  -preset:v ultrafast  -probesize 32  -c:v libx264 \
-x264opts "keyint=1:min-keyint=1:no-scenecut" \
-force_key_frames "expr:gte(t,n_forced*1)" \
-r 15 -f flv -an rtmp://localhost:1935/itlab/rpi -nostdin

ffmpeg -err_detect ignore_err \
    -use_wallclock_as_timestamps 1 -flags global_header \
    -r 15 -rtsp_transport tcp \
    -i rtsp://10.27.164.151:5000/unicast \
    -flags +low_delay -tune zerolatency -preset:v ultrafast -probesize 32 \
    -x264opts "keyint=1:min-keyint=1:no-scenecut" \
    -force_key_frames "expr:gte(t,n_forced*1)" \
    -fflags +genpts -vcodec copy -an -bsf:v h264_mp4toannexb \
    -f flv -y rtmp://localhost:1935/itlab/rpi -nostdin

ffmpeg -f mjpeg -i http://10.27.164.151:5000/video_feed \
-flags +low_delay  -tune zerolatency  -preset:v ultrafast  -probesize 32  -c:v libx264 \
-x264opts "keyint=1:min-keyint=1:no-scenecut" \
-force_key_frames "expr:gte(t,n_forced*1)" \
-r 15 -f flv -an rtmp://localhost:1935/itlab/rpi -nostdin
```

## IP Camera
```
ffmpeg -err_detect ignore_err \
    -use_wallclock_as_timestamps 1 -flags global_header \
    -r 15 -rtsp_transport tcp \
    -i rtsp://root:itlabcsyang92633@10.27.164.152/live3.sdp \
    -flags +low_delay -tune zerolatency \
    -vcodec copy -an \
    -f flv -y rtmp://localhost:1935/itlab/demo -nostdin

ffmpeg -err_detect ignore_err \
    -use_wallclock_as_timestamps 1 -flags global_header \
    -r 15 -rtsp_transport tcp \
    -i rtsp://root:itlabcsyang92633@10.27.164.152/live3.sdp \
    -flags +low_delay -tune zerolatency -preset:v ultrafast -probesize 32 \
    -x264opts "keyint=1:min-keyint=1:no-scenecut" \
    -force_key_frames "expr:gte(t,n_forced*1)" \
    -fflags +genpts -vcodec copy -an -bsf:v h264_mp4toannexb \
    -f flv -y rtmp://localhost:1935/itlab/demo -nostdin
```

## SSH Tunnel
```
# reverse tunnel
ssh -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3" -N -R localhost:1935:localhost:1935 -p 22018 nvidia@ddl.itlab.ee.ncku.edu.tw -i /home/itlab/.ssh/id_rsa

ssh -N \
    -R localhost:1935:$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nginx-star):1935 \
    -o "ServerAliveInterval 60" \
    -o "ServerAliveCountMax 3" \
    -p 22018 nvidia@ddl.itlab.ee.ncku.edu.tw \
    -i /home/itlab/.ssh/id_rsa

# tunnel
ssh -N \
-o "ServerAliveInterval 60" \
-o "ServerAliveCountMax 3" \
-L localhost:1935:localhost:1935 \
-p 22018 itlab@ssl.itlab.ee.ncku.edu.tw \
-i /home/nvidia/.ssh/id_rsa
```