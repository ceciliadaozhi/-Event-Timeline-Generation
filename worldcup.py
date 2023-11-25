import pandas as pd

# Step 1: Load the CSV file
file_path = 'bbc_news_worldcup.csv'  
news_data = pd.read_csv(file_path)

# Step 2: Initial filtering for news related to the World Cup
world_cup_news = news_data[news_data['title'].str.contains("World Cup", case=False, na=False)]

# Step 3: Further filtering for news specifically related to Football World Cup
football_keywords = ["football", "soccer", "FIFA"]
football_world_cup_news = world_cup_news[
    world_cup_news['title'].str.contains('|'.join(football_keywords), case=False, na=False)
]

# Step 4: Save the filtered news to a CSV file
football_world_cup_news.to_csv('football_world_cup_news.csv', index=False)
