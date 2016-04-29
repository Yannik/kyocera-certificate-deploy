This automates deployment of ssl certificates (e.g. from letsencrypt) to kyocera printers.

Confirmed working printer models:
  - Kyocera FS1370DN

Example usage:

    ./kyocera-certificate-deploy.py "https://printer.internal.example.org" "/path/to/key_and_cert.pem" "password"
