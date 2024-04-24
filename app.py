import praw 
from nltk.corpus import stopwords 
import nltk 
nltk.download('punkt') 
nltk.download('stopwords')
nltk.download('wordnet')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 
import re 
from time import sleep
from flask import Flask, request, render_template, jsonify
import wikipedia


# Reddit API Credentials (Keep these secret!)
client_id = "--" 
client_secret = "--" 
user_agent = "--" 

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

def clean_text(text):
    # Lowercase text
    text = text.lower()
    # Remove special characters, URLs, and punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # Remove stop words (IMP!)
    stop_words = set(stopwords.words("english"))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

def analyze_reddit_sentiment(celebrity):
    subreddit_name = "all"  # Replace with your desired subreddit

    def collect_reddit_posts(subreddit, celebrity, limit=10, delay=1):
        submissions = []
        for submission in subreddit.search(query=celebrity, limit=limit):
            try:
                submission.comments.replace_more(limit=3) 
                for comment in submission.comments.list():
                    submissions.append(clean_text(comment.body))
                sleep(delay) 
            except praw.exceptions.APIException as e:
                print(f"API Error: {e}")
                break 
        return submissions

    def analyze_sentiment(text):
        vader = SentimentIntensityAnalyzer()
        scores = vader.polarity_scores(text)
        return scores['compound']

    subreddit = reddit.subreddit(subreddit_name)
    posts = collect_reddit_posts(subreddit, celebrity)
    sentiment_scores = [analyze_sentiment(text) for text in posts]
    average_score = sum(sentiment_scores) / len(sentiment_scores)
    return average_score

# Flask App
app = Flask(__name__)

def get_wikipedia_image(celebrity):
    
        wikipedia_page=wikipedia.page(celebrity)
        images=wikipedia_page.images

        for image_url in images:
            if image_url.endswith((".jpg",".jpeg",".png")):
                return image_url
        return images[0]
    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment_endpoint():
    celebrity = request.form['name'] 
    average_score = analyze_reddit_sentiment(celebrity)  

    if average_score > 0.05:
        sentiment = "Positive"
    elif average_score < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral" 

    # return render_template('result.html', sentiment=sentiment) 
    try:
        wikipedia_summary = wikipedia.summary(celebrity, sentences=3)  # Get brief summary
        wikipedia_image_url = wikipedia.page(celebrity).images[0]  # Get first image
    except wikipedia.exceptions.DisambiguationError as e:
        wikipedia_summary = f"Multiple people found. Please refine your search. Options: {e.options}"
        wikipedia_image_url = None
    except:
        wikipedia_summary = "Wikipedia information not found."
        wikipedia_image_url = None

    return render_template('result.html', sentiment=sentiment, 
                                          summary=wikipedia_summary,
                                          image_url=wikipedia_image_url) 

if __name__ == '__main__':
    app.run(debug=True)
