"""
Prerequisite installation (works on ubuntu 20.04)
$ apt install python3-gst-1.0 gstreamer1.0-plugins-base gir1.2-gst-rtsp-server-1.0

Source for the RTSP server from Enne2 github:
https://raw.githubusercontent.com/Enne2/PyGObject-GstRtspServer/master/rtsp-server.py

With a bit of stackoverflow for the pipeline configuration:
https://stackoverflow.com/questions/59858898/how-to-convert-a-video-on-disk-to-a-rtsp-stream
"""

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GLib, GObject, GstRtspServer

Gst.init(None)

port = "8554"
mount_point = "/test"
source_file = "/path/to/test.mp4"

server = GstRtspServer.RTSPServer.new()
server.set_service(port)
mounts = server.get_mount_points()
factory = GstRtspServer.RTSPMediaFactory.new()

# Test src
# ~ pipeline = "videotestsrc ! videoconvert ! theoraenc ! queue ! rtptheorapay name=pay0"

#MP4 src
src_demux = f"filesrc location={source_file} ! qtdemux name=demux"
h264_transcode = "demux.video_0"
pipeline = f"{src_demux} {h264_transcode} ! queue ! rtph264pay name=pay0 config-interval=1 pt=96"

factory.set_launch(pipeline)
mounts.add_factory(mount_point, factory)
server.attach()

#  Start serving
print (f"stream ready at rtsp://127.0.0.1:{port}{mount_point}");

loop = GLib.MainLoop()
loop.run()
