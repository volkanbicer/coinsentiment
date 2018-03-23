FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('vader_lexicon', download_dir='/app/nltk_data')" ]
ENTRYPOINT ["python"]
CMD ["app.py"]
