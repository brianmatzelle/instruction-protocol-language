FROM ubuntu:22.04
ENV DISPLAY=host.docker.internal:0

# Install Xfce and VNC server
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    dbus-x11 \
    x11-xserver-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up VNC
RUN mkdir -p ~/.vnc && \
    echo "password" | vncpasswd -f > ~/.vnc/passwd && \
    chmod 600 ~/.vnc/passwd

# Create startup script for VNC with xfce
RUN echo '#!/bin/bash\nstartxfce4 &' > ~/.vnc/xstartup && \
    chmod +x ~/.vnc/xstartup

# Expose VNC port
EXPOSE 5901

# Start VNC server by default
CMD ["bash", "-c", "vncserver :1 -geometry 1280x800 -depth 24 && tail -F /root/.vnc/*.log"]
