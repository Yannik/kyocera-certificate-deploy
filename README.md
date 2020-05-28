This automates deployment of ssl certificates (e.g. from letsencrypt) to kyocera printers.

Confirmed working printer models:
  - Kyocera FS1370DN
  - Kyocera FS-C5250DN

Usage:

```
usage: kyocera-certificate-deploy.py [-h] [--headless] [--insecure]
                                     [--no-screenshots] [--debug]
                                     host password certfile

positional arguments:
  host              printer hostname
  password          printer admin password
  certfile          certfile should contain both cert and key

optional arguments:
  -h, --help        show this help message and exit
  --headless        run headless
  --insecure        ignore invalid ssl cert on phone (useful for first setup)
  --no-screenshots  disable saving screenshots for each step
  --debug           debug output
```
