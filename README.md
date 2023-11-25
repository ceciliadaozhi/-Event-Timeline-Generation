# Event-Timeline-Generation

About the implementation code and related resources of event timeline generation

## 1. Get news data
Get news data from https://www.bbc.com/, including title, release time, URL and other information, and store it in the bbc_news.csv file.
1. Get_newsurls.py  
Get the URL of the news from the BBC website and store it in the bbc_newsurls.csv file.  
2. Get_details.py  
Get the title, release time, URL and other information of the news from the URL, and store it in the bbc_news.csv file.  

## 2. Data preprocessing  
First, convert the obtained data to utf-8 format, and then clean the data to remove special characters, spaces, and duplicate news.    
Then perform word segmentation, remove stop words, lemmatization, etc.  
At the same time, pay attention to the part-of-speech filtering, only keep nouns, verbs, adjectives, and adverbs.  

## 3. Get keywords and clustering
There are two ways to get related news:  
one is to use TF-IDF to get keywords, and then get the news with the highest similarity to the keywords;  
the other is to use K-means to cluster the news.  
### 3.1 Get keywords
Use TF-IDF to get keywords, and then use the keywords to get the corresponding news.
1. worldcup.py
From all news, get the news about the World Cup and football news.
2. worldcup-top15.py
Get the top 15 news about the World Cup and football news.
3. word-cloud-data.py
Get keywords from the dataset and generate word cloud csv files.

### 3.2 Clustering
Use K-means to cluster the news, and then get the news with the highest similarity in each cluster as the representative news of the cluster.
1. create_vec.py
Create a vector for each news, and then use K-means to cluster.
2. cluster_get_hot_news.py
Get the news with the highest similarity in each cluster.
3. similarity.py
Calculate the similarity between two news.

## 4. Get event timeline
After getting the representative news of each cluster, use the release time of the news as the time point of the event, and then use the similarity between the news to determine whether the news is related to the event.

## 5. Visualization
Use the React framework to visualize the event timeline.
Detailed implementation process please refer to:https://github.com/ceciliadaozhi/word-time
![image](https://github.com/ceciliadaozhi/Event-Timeline-Generation/assets/65725744/28bf3a8b-9813-48fe-84ad-81f193d71071)
