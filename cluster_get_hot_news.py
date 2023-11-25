# _*_coding : UTF-8 _*_
# 代码作者 : lyt
# 开发时间 : 2023/11/21    10:12
# 代码名称 : test.PY
# 开发工具 : PyCharm
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics


input_file = 'vec_news.csv'
output_file = 'hot_news_1.csv'
MA_WIDTH = 100
HOT_THRESHOLD = 1

df = pd.read_csv(input_file, encoding='ISO-8859-1')

vector_temp = df.avg_vector.apply(lambda x: x.strip('[ ]').split())
vector_float = vector_temp.apply(lambda x: [np.float64(elem) for elem in x])
df['avg_vector'] = vector_float.apply(np.array, dtype=object)


def get_clusters(df, n_clusters=10, metric='cosine'):
    X = np.array(df.avg_vector.tolist(), ndmin=2)
    kmeans = KMeans(n_clusters=n_clusters, init='random').fit(X)
    cluster = kmeans.labels_
    silhouette_values = metrics.silhouette_samples(X, kmeans.labels_,
                                                   metric=metric)
    res = pd.DataFrame({'cluster': cluster,
                        'sil_value': silhouette_values},
                       index=df.index)
    return (res)


def get_cluster_order(df, news_min=10):
    cluster = df.cluster
    silhouette_values = df.sil_value
    sil_clusters = pd.DataFrame({'cluster': cluster, 'sil': silhouette_values})

    grouped = sil_clusters.groupby('cluster')
    col_order_sum = grouped.aggregate({'sil': {sum, 'count'}})['sil'].sort_values(by='sum', ascending=False)
    col_order_sum = col_order_sum[col_order_sum['count'] >= news_min]
    scores = list(col_order_sum['sum'])
    col_order_sum = list(col_order_sum.index)

    res = pd.DataFrame({'cluster': col_order_sum,
                        'score': scores})
    return (res)


df_time = df.set_index('time')
df_time.index = pd.to_datetime(df_time.index)


def setup_intervals(start, end, freq='1D', minute_range=60*24*7):
    dt1 = pd.date_range(start, end, freq=freq)
    dt2 = dt1 - pd.Timedelta(minutes=minute_range)
    intervals = pd.DataFrame({'t_from': dt2, 't_to': dt1})
    return intervals


start = '2022-4-1'
end = '2023-11-17'

start_timestamp = pd.to_datetime(start)
end_timestamp = pd.to_datetime(end)
intervals = setup_intervals(start=start_timestamp, end=end_timestamp)


def get_hot_news(df, intervals):
    scores = list()
    news_list = list()
    good_score = list()
    for index, interval in intervals.iterrows():
        t_from = interval.t_from
        t_to = interval.t_to
        df_interval = df[(df.index >= t_from) & (df.index <= t_to)]

        if len(df_interval) > 50:
            # Clustering, choosing most important cluster
            clusters = get_clusters(df_interval)
            cluster_order = get_cluster_order(clusters)
            validate_score = np.mean(cluster_order.score)
            for i in range(len(cluster_order.score)):
                if cluster_order.score[i] > validate_score:
                    scores.append(cluster_order.score[i])
            good_score.append(cluster_order.score[0])
            good_score.append(cluster_order.score[1])

            # Detecting hot cluster
            ma = 0
            std = 0
            if len(scores) > MA_WIDTH:
                ma = np.mean(scores[-MA_WIDTH:])
                std = np.std(scores[-MA_WIDTH:])
            if len(scores) <= MA_WIDTH:
                ma = np.mean(scores)
                std = np.std(scores)
            for j in range(1):
                if good_score[j] > (ma + HOT_THRESHOLD * std):
                    # Record hot news
                    df_interval_res = pd.concat([df_interval, clusters], axis=1)
                    cluster = cluster_order.head(1)
                    # print('Score = {:.1f}'.format(cluster.score[0]))
                    news = df_interval_res[df_interval_res.cluster == cluster.cluster[j]]. \
                        sort_values(by=['sil_value'], ascending=False).head(3)
                    print(news)
                    news_list.append(news)
                if len(news_list) != 0:
                    news_df = pd.concat(news_list)
                    news_df.to_csv(output_file, index=True)


get_hot_news(df_time, intervals)
# print(scores)
