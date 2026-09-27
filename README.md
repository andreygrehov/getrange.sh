# Range website

A static page: `index.html`, `style.css`, `main.js`. No build step; serve the
directory from anywhere that serves files.

Preview locally:

```bash
python3 -m http.server 8002
open http://127.0.0.1:8002/
```

`python3 check.py` fails if a benchmark number the page quotes goes missing, if
a claimed speedup stops matching the times beside it, or if the design picks up
rounded corners, gradients, uppercase labels or blurred shadows.
