# _*_coding : UTF-8 _*_
# 代码作者 : lyt
# 开发时间 : 2023/11/21    14:35
# 代码名称 : similarity.PY
# 开发工具 : PyCharm
import numpy as np
import pandas as pd
from cv2 import norm

input_file = 'm12.csv'
output_file = 'events_13.csv'
m_file = 'm13.csv'
df = pd.read_csv(input_file)
df.drop_duplicates(subset=['title'], inplace=True)

df.reset_index()

vector_temp = df.avg_vector.apply(lambda x: x.strip('[ ]').split())
vector_float = vector_temp.apply(lambda x: [np.float64(elem) for elem in x])
j = 154

def compute_similarity(df, vector):
    similarity = []
    for i in range(len(df.title)):
        cosine_similarity = np.dot(np.array(vector), np.array(vector_float[i])) / (
                    norm(np.array(vector)) * norm(np.array(vector_float[i])))
        similarity.append(cosine_similarity)
    return similarity


print(df.title[j])


def find_events(df, similarity_list):
    indices_to_delete = []
    for i in range(len(similarity_list)):
        if 0.65 < similarity_list[i]:
            print(df.title[i])
            indices_to_delete.append(i)
    print(indices_to_delete)

    for k in range(len(indices_to_delete)):
        similarity_list = compute_similarity(df, vector_float[indices_to_delete[k]])

    for i in range(len(similarity_list)):
        if 0.6 < similarity_list[i] and (i not in indices_to_delete):
            print(df.title[i])
            indices_to_delete.append(i)
    print(indices_to_delete)

    if len(indices_to_delete) >= 5:
        print('can make eventline')
        extracted_rows = df.iloc[indices_to_delete]
        df_filtered = df.drop(indices_to_delete)
        extracted_rows.to_csv(output_file, index=False)
        df_filtered.to_csv(m_file, index=False)


if __name__ == '__main__':
    similarity_list = compute_similarity(df, vector_float[j])
    find_events(df, similarity_list)
