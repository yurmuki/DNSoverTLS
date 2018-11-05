FROM python:2.7-alpine

ENV PYTHONUNBUFFERED=0

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /dnsovertls
COPY dns-over-tls.py /dnsovertls
COPY privatekey.pem /dnsovertls
COPY certificate.pem /dnsovertls

EXPOSE 53

CMD ["python", "dns-over-tls.py"]
