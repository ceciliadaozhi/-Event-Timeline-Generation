import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Step 1: Read the CSV file
file_path = 'football_world_cup_news.csv' 
news_data = pd.read_csv(file_path)

# Convert the 'time' column from string to datetime format
news_data['time'] = pd.to_datetime(news_data['time'])

# Function to extract top N important news based on TF-IDF scores
def extract_top_news(news_df, top_n=15):
    # Using TF-IDF to find important words in the titles
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(news_df['title'])
    
    # Summing up the TF-IDF scores for each document
    document_scores = np.sum(tfidf_matrix.toarray(), axis=1)
    
    # Getting the indices of the top N documents
    top_indices = np.argsort(document_scores)[::-1][:top_n]

    # Selecting the top N news
    top_news = news_df.iloc[top_indices]
    return top_news.sort_values(by='time')

# Applying the function to extract the top 15 news items
top_15_news = extract_top_news(news_data)

# Displaying the selected news
print(top_15_news[['time', 'title' , 'url']])

# Saving the selected news to a CSV file, events_2.csv
top_15_news.to_csv('events_2.csv', index=False)