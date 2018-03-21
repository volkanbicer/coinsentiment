FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m nltk.downloader vader_lexicon
ENTRYPOINT ["python"]
CMD ["app.py"]
