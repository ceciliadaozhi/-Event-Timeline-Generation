# 根据月份生成词云，统计每个月份的新闻标题中出现频率最高的词汇
import numpy as np
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# import nltk
# nltk.download('stopwords')

# 加载英文的停用词列表
stop_words = set(stopwords.words('english'))
stop_words.add('say') # 添加自定义停用词

# 词性还原saw和see
def get_wordnet_pos(treebank_tag):
    """ 将NLTK的词性标签转换为WordNet的词性标签 """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # 默认作为名词处理

# 数据预处理
def preprocess_text(text):
    # 移除特殊字符并转换为小写
    text_clean = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    # 英文分词，基于空格
    words = text_clean.split()
    words = [word for word in words if word not in stop_words]
    # 词性标注
    tagged_words = nltk.pos_tag(words)
    # 词形还原
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in tagged_words]
    return ' '.join(lemmatized_words)

# 加载数据
file_path = 'bbc_news_modified.csv'  
news_data = pd.read_csv(file_path)

# 将时间字段从字符串转换为日期时间格式
news_data['time'] = pd.to_datetime(news_data['time'])

# 创建特定日期的时间序列（每个月的7号）
start_date = '2022-3-07'
end_date = '2023-11-07'
date_ranges = pd.date_range(start=start_date, end=end_date, freq='MS') + pd.DateOffset(days=6)
date_ranges = np.insert(date_ranges, 0, pd.Timestamp(start_date))  # 插入起始日期

# 使用pd.cut函数划分数据
news_data['time_period'] = pd.cut(news_data['time'], bins=date_ranges, right=False)

# 按时间分组
grouped = news_data.groupby('time_period')
# print(grouped.size())

# 准备空的DataFrame来保存结果
columns = ['word', 'count', 'month']
monthly_word_frequencies = pd.DataFrame(columns=columns)

# 对每个月份的数据生成词云
for name, group in grouped:
    # 应用文本预处理
    group['clean_title'] = group['title'].apply(preprocess_text)

    # 统计词频
    all_tokens = ' '.join(group['clean_title']).split()
    word_counts = Counter(all_tokens)

    # 获取词频最高的3个词
    top_3_words = word_counts.most_common(3)

    # 提取时间信息
    month = name.left.strftime('%Y-%m')

    # 为每个词创建一行
    for word, count in word_counts.items():
        row_data = [word, count, month]
        monthly_word_frequencies = monthly_word_frequencies.append(pd.Series(row_data, index=columns), ignore_index=True)

# 保存所有时间段的词频数据到一个CSV文件
monthly_word_frequencies.to_csv('all_word_counts.csv', index=False)

    # 生成词云
    # wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

    # 使用matplotlib展示词云
    # plt.figure(figsize=(15, 7))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.title(f"Word Cloud for {name}")
    # plt.axis('off')  # 关闭坐标轴
    # plt.show()

    # 保存词云
    # wordcloud.to_file(f'wordcloud_{name}.png')