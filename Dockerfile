FROM python:3-onbuild
RUN pip3 install --upgrade pip

RUN git clone  https://github.com/guleroman/SimpleDecision.git /APII

EXPOSE 7777

ENTRYPOINT ["python3", "app.py"]
