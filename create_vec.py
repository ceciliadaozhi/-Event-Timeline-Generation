import numpy as np
import pandas as pd
from collections import Counter

from nltk.corpus import stopwords
import re
import gensim

# 加载英文的停用词列表
stop_words = set(stopwords.words('english'))
input_file_path = 'bbc_news.csv'
output_file_path = 'vec_news.csv'
google_file = 'GoogleNews-vectors-negative300.bin'
df = pd.read_csv(input_file_path, encoding='ISO-8859-1')
print(df)

# 数据预处理
def text_to_words(text):
    # 移除特殊字符并转换为小写
    text_clean = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    # 英文分词，基于空格
    words = text_clean.split()
    words = [word for word in words if word not in stop_words]
    return words


df['clean_title'] = df.apply(lambda x: text_to_words(x.title), axis=1)
clean_title = df.clean_title.tolist()

model = gensim.models.KeyedVectors.load_word2vec_format(google_file, binary=True)
vectors = list()
avg_vectors = list()
for sentence in clean_title:
    vectors.append([model[word] for word in sentence
                    if word in model])

avg_vectors = []
for sentence_vectors in vectors:
    if len(sentence_vectors) > 0:
        avg_vector = np.mean(sentence_vectors, axis=0)
    else:
        # 处理空切片的情况
        avg_vector = None  # 或其他默认向量
    avg_vectors.append(avg_vector)

df['avg_vector'] = avg_vectors
df.dropna(subset=['avg_vector'], inplace=True)
df.to_csv(output_file_path, index=False)


