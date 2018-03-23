# Coinsentiment

Does sentiment analysis based on subreddit and the comments belongs to topic.
View live [here](https://coinsentiment.herokuapp.com/)

## Installing

* Create virtual environment
```
virtualenv -p python3 p3env
```
* Activate environment
```
source p3env/bin/activate
```
* Install dependencies
```
pip install -r requirements.txt
```
* Install nltk [`vader_lexicon`](https://github.com/cjhutto/vaderSentiment) data
```
  python
  import nltk
  nltk.download('vader_lexicon')
```
* Reddit requires [OAuth2](https://github.com/reddit-archive/reddit/wiki/OAuth2) authentication. Create your client and then change configuration in appConfig.py
  * `client_id`
  * `client_secret`
  * `password`
  * `user_agent`
  * `username`

## Running
Simply run application
```bash
python app.py
```

If you want the run application in docker container

```Bash
./run.sh
```

## Built With
* [Flask](https://github.com/pallets/flask)
* [Flask Cache](https://github.com/thadeusb/flask-cache)
* [Nltk](https://github.com/nltk/nltk)
* [Praw](https://github.com/praw-dev/praw)
