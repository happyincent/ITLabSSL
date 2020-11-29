# ITLabSSL

Design and Implementation of a Street Light Management System: Configuration and Deployment

> [`ppt`](./20190715.pdf) [`doi:10.6844/NCKU201901461`](http://etds.lib.ncku.edu.tw/etdservice/view_metadata?etdun=U0026-0808201911421100)

- Functions

  - Real-time lighting control
    - Manual configuration
    - Scheduling timetable
  - Real-time information
    - Light status, environmental data from sensors
    - Video streaming from IP camera
  - Historical information Query API
    - Open Data

- Cloud

  - Docker Compose, Dockerfile (Apline Linux)
  - Crontab, Logrotate, Supervisord (process control)
  - Containers
    - Nginx (http2, auth_request)
    - Nginx-RTMP (FFmpeg, RTMP control, HLS with AES)
    - Python Django (Gunicorn - HTTP, Daphne - WebSocket)
    - MongoDB (account, device, history)
    - Redis (session, token)
    - Certbot (Let’s Encrypt)
    - SSHD (SSH tunnel, monitor scripts)

- Edge - Nvidia TX2 / Raspberry Pi (Docker) + IP camera + Arduino

  - Docker Swarm (deploy containers to numerous workers)
  - Docker buildx (build cross-platform images with Dockerfiles)
  - Containers
    - Autossh (SSH tunnel)
    - FFmpeg (RTSP to RTMP with token)
    - Edge (WebSocket with token, USB-serial to Arduino)

- Browser
  - Bootstrap, WebSocket, hls.js, AJAX

---

[Merge repos](https://gist.github.com/x-yuri/6161d90d1af8ebac6e560bcef548c1c3) with [git-filter-repo](https://github.com/newren/git-filter-repo)
