import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from time import sleep
import praw.exceptions
import re
from nltk.corpus import stopwords  

# Replace with your Reddit app credentials
client_id = "--"
client_secret = "--"
user_agent = "--"

# Initialize Reddit client
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# cleaning of  text 
def clean_text(text):
    # Lowercase text
    text = text.lower()
    # Remove special characters, URLs, and punctuation
    text = re.sub(r"[^\w\s]", "", text)
    # Remove stop words (IMP!)
    stop_words = set(stopwords.words("english"))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text


def analyze_sentiment(text):
    vader = SentimentIntensityAnalyzer()
    scores = vader.polarity_scores(text)
    # Return compound score for overall sentiment
    return scores['compound']


# Function to search and collect top comments 
# includes rate limiting)
def collect_reddit_posts(subreddit, celebrity, limit=10, delay=1):
    submissions = []
    for submission in subreddit.search(query=celebrity, limit=limit):
        try:
            # Access top 3 comments (replace 3 with desired number)
            submission.comments.replace_more(limit=3)
            for comment in submission.comments.list():
                submissions.append(clean_text(comment.body))
            sleep(delay)  # Implement delay to avoid exceeding rate limits
        except praw.exceptions.APIException as e:
            print(f"API Error: {e}")
            break  # Exit loop on API error
    return submissions


# name the celebrity or  public figure you want to study here
#you can also input any topic
celebrity = "Manchester City"
subreddit = reddit.subreddit("all")  # Change to specific subreddits if desired, type all if wanting to search whole reddit

# Collecting comments with rate limiting
posts = collect_reddit_posts(subreddit, celebrity)

# Sentiment analysis and score aggregation
sentiment_scores = [analyze_sentiment(text) for text in posts]
average_score = sum(sentiment_scores) / len(sentiment_scores)

#adjust the numbers as needed
if average_score > 0.05:
    print(f"Overall Sentiment for {celebrity} on Reddit: Positive")
elif average_score < -0.05:
    print(f"Overall Sentiment for {celebrity} on Reddit: Negative")
else:
    print(f"Overall Sentiment for {celebrity} on Reddit: Neutral")

