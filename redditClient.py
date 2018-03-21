import requests
import json
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import sys
import utils
import statistics as s
import praw
import appConfig as cfg


class RedditClient:
    base_url = 'https://www.reddit.com/r'
    reddi_url = 'https://www.reddit.com'
    sia = SIA()
    reddit = praw.Reddit(client_id=cfg.reddit['client_id'],
                         client_secret=cfg.reddit['client_secret'],
                         password=cfg.reddit['password'],
                         user_agent=cfg.reddit['user_agent'],
                         username=cfg.reddit['username'])


    def __init__(self):
        pass

    def get_data(self, topic = 'bitcoin', data_count = 5):
        return self.get_headlines(topic, data_count)

    def get_headlines(self, topic, data_count = 10):
        hdr = {'User-Agent': 'linux:r/'+topic+'.single.result:v1.0' + '(by /u/vlknbcr)'}
        url = self.base_url+topic+'/.json'
        req = requests.get(url, headers = hdr)
        json_data = json.loads(req.text)
        data_all = json_data['data']['children']
        num_of_posts = 0
        while len(data_all) <= data_count:
            time.sleep(2)
            last = data_all[-1]['data']['name']
            url = self.base_url+topic+'/.json?after=' + str(last)
            req = requests.get(url, headers=hdr)
            data = json.loads(req.text)
            data_all += data['data']['children']
            if num_of_posts == len(data_all):
                break
            else:
                num_of_posts = len(data_all)
        return self.create_data(data_all)

    def create_data(self, topics):
        pos_list = []
        neg_list = []
        notr_list = []
        for topic in topics:
            title = topic['data']['title']
            comments = self.get_comments(topic)
            comments_polarity_score = self.calculate_comment_score(comments[:10])
            polarity_score = self.calculate_polarity(title)
            score = s.mean([polarity_score, comments_polarity_score])

            d = {'title': title,
                 'link': self.reddi_url + topic['data']['permalink'],
                 'time': topic['data']['created_utc']}

            if score <= -0.2:
                neg_list.append(d)
            elif score >= 0.2:
                pos_list.append(d)
            else:
                notr_list.append(d)

        pos_list.sort(key=lambda x:x['time'])
        neg_list.sort(key=lambda x:x['time'])
        notr_list.sort(key=lambda x:x['time'])
        return {'pos': pos_list,
                'neg': neg_list,
                'notr': notr_list,
                'total_count': len(pos_list) + len(neg_list) + len(notr_list)}

    def get_comments(self, topic):
        subreddit = topic['data']['subreddit']
        hdr = {'User-Agent': 'linux:r/'+subreddit+'.single.result:v1.0' + '(by /u/vlknbcr)'}
        url = self.base_url + subreddit +'/comments/'+ topic['data']['id'] + '.json'
        req = requests.get(url, headers = hdr)
        json_data = json.loads(req.text)
        comments = json_data[1]['data']['children']
        return comments

    def calculate_polarity(self, text):
        res = self.sia.polarity_scores(text)
        return res['compound']

    def calculate_comment_score(self, comments):
        if len(comments) == 0: return 0.0
        try:
            normalized_reddit_scores = utils.unity_based_normalization(dict([(str(c.id), c.score) for c in comments]))
            scores = []
            for comment in comments:
                polarity = self.calculate_polarity(comment.body)
                score = normalized_reddit_scores[str(comment.id)] * polarity
                scores.append(score)
            total_score = s.mean(scores)
            return total_score
        except Exception as e:
            print('Exception occured when calculating comment score!', e)
            return 0

    def get(self, topic = 'bitcoin', data_count = 20):
        # print(topic)
        pos_list = []
        neg_list = []
        notr_list = []
        for submission in self.reddit.subreddit(topic).hot(limit=data_count):
            # print(submission.title, submission.score, submission.id, submission.url)
            top_level_comments = list(submission.comments)
            comments_polarity_score = self.calculate_comment_score(top_level_comments)
            polarity_score = self.calculate_polarity(submission.title)
            score = s.mean([polarity_score, comments_polarity_score])

            d = {'title': submission.title,
                 'link': submission.url,
                 'time': submission.created_utc,
                 'score': score}

            if score < -0.1:
                neg_list.append(d)
            elif score > 0.1:
                pos_list.append(d)
            else:
                notr_list.append(d)

        pos_list.sort(key=lambda x:x['time'])
        neg_list.sort(key=lambda x:x['time'])
        notr_list.sort(key=lambda x:x['time'])
        return {'pos': pos_list,
                'neg': neg_list,
                'notr': notr_list,
                'total_count': len(pos_list) + len(neg_list) + len(notr_list)}
