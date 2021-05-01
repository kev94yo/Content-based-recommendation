import numpy as np
import pandas as pd

# 1. Represent Movies with genre IDF
df = pd.read_csv('data/movies_w_imgurl.csv', index_col = 0)
total_counts = df['movieName'].shape[0]
genre_df = df['genres']
genre_df = genre_df.str.split('|')

genre_dict = {}
for index, row in genre_df.items():
    for genre in row:
        if genre not in genre_dict:
            genre_dict[genre] = 1
        else:
            genre_dict[genre] += 1

for genre in genre_dict.keys():
    genre_dict[genre] = np.log10(total_counts / genre_dict[genre])

movie_df = pd.DataFrame(0, index = df.index, columns = sorted(genre_dict.keys()))
for index in movie_df.index:
    for genre in genre_df.loc[index]:
        movie_df.loc[index, genre] = genre_dict[genre]

# 2. Use tags to enhance movie representations
tag_df = pd.read_csv('data/tags.csv', index_col = 0)
tag_df['tag'] = tag_df['tag'].str.split(',')

movie_tag_dict = {}
for index, row in tag_df.iterrows():
    movieId = row['movieId']
    tags = row['tag']
    for tag in tags:
        tag = tag.strip()
        if tag not in movie_tag_dict:
            movie_tag_dict[tag] = [movieId]
        else:
            if movieId not in movie_tag_dict[tag]:
                movie_tag_dict[tag].append(movieId)

total_count = len(tag_df['movieId'].unique())
for key in movie_tag_dict.keys():
    movie_tag_dict[key] = np.log10(total_count / len(movie_tag_dict[key]))

tag_embedding_df = pd.DataFrame(0, index = movie_df.index, columns = list(movie_tag_dict.keys()))

for index, row in tag_df.iterrows():
    movieId = row['movieId']
    for tag in row['tag']:
        tag = tag.strip()
        tag_embedding_df.loc[movieId, tag] += movie_tag_dict[tag]

genre_array = movie_df.values
tag_array = tag_embedding_df.values

# 3. Get Cosine Similarity
reps = np.concatenate((genre_array, tag_array), axis=1)
dot = reps @ reps.T
magnitude = np.sqrt(np.outer(np.sum(np.square(reps), axis = 1), np.sum(np.square(reps), axis = 1)))
sim_df = pd.DataFrame(dot / magnitude, index = df.index, columns = df.index)

# 4. Rate Items
rating_df = pd.read_csv('data/ratings.csv', index_col = 0).drop(columns = ['timestamp'])

def get_scores(user_id):
    user_df = rating_df.loc[user_id]
    user_sim = []
    user_rating = np.array(user_df['rating'])
    for movie in user_df['movieId']:
        user_sim.append(sim_df.loc[movie])
    user_sim = np.array(user_sim)
    sim_sum = np.sum(user_sim, axis= 0)
    
    return np.matmul(user_sim.T, user_rating) / (1 + sim_sum)

def recommendations(user_id):
    score = get_scores(user_id)
    top_30_ind = np.argpartition(score, -30)[-30:]
    top_list = []
    for i in range(0, len(score[top_30_ind])):
        top_list.append([user_id, score[top_30_ind][i], sim_df.index[top_30_ind][i]])
    top_list = sorted(top_list, key=lambda x: (-x[1], x[2]))
    
    return top_list   