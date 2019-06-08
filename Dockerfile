FROM python:3-onbuild
RUN pip3 install --upgrade pip
RUN pip install -U git+https://github.com/text-machine-lab/sentimental.git
RUN git clone  https://github.com/guleroman/SimpleDecision.git /APII

EXPOSE 7777

ENTRYPOINT ["python3", "app.py"]
