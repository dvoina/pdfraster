FROM alpine:latest
RUN apk update --no-cache && apk add --no-cache  poppler poppler-utils python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache && pip install flask && mkdir -p /opt/rasterizer 
COPY rasterizer /opt/rasterizer
WORKDIR /tmp
EXPOSE 5000
ENTRYPOINT [ "python", "/opt/rasterizer/app.py", "--host", "0.0.0.0"]



