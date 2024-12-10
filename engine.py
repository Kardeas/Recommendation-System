def find_similar_users(user_id, user_df):
    user_cluster = user_df[user_df['user_id'] == user_id]['cluster'].values[0]
    similar_users = user_df[user_df['cluster'] == user_cluster]['user_id'].head(5).tolist()
    return similar_users

def recommend_similar_items(item_id, item_data):
    try:
       item_cluster = item_data[item_data['app_id'] == item_id]['Cluster'].values[0]
       similar_items = item_data[item_data['Cluster'] == item_cluster]['app_id'].head(5).tolist()
       if item_id in similar_items:
          similar_items.remove(item_id)
       return similar_items
    except IndexError:
        return None

def recommend_items(user_id, user_df, item_df):
    users_segment = find_similar_users(user_id, user_df)
    user_games = user_df[user_df['user_id'] == user_id]['app_id'].tolist()
    
    games_segment = []
    same_user_games = []

    for user_id in users_segment:
        similar_user_games = user_df[user_df['user_id'] == user_id]['app_id'].tolist()
        same_user_games.extend(similar_user_games)

    filtrar_games = [item for item in same_user_games if item not in user_games]
    games_segment.extend(filtrar_games)

    best_games = []

    for app_id in user_games:
        similar_games = recommend_similar_items(app_id, item_df)
        if similar_games != None:
           games_segment.extend(similar_games)

    filtrar_games2 = [item for item in best_games if item not in user_games]
    games_segment.extend(filtrar_games2)

    user_games2 = item_df[item_df['app_id'].isin(user_games)]
    games_segment2 = item_df[item_df['app_id'].isin(games_segment)]

    user_games_columnas = user_games2[["rating_coded", "positive_ratio", "tag_1", "tag_2", "tag_3", "tag_4", "tag_5"]]
    games_segment_columnas = games_segment2[["rating_coded", "positive_ratio", "tag_1", "tag_2", "tag_3", "tag_4", "tag_5"]]

    scaler = StandardScaler()
    user_games_matrix = scaler.fit_transform(user_games_columnas)    
    games_segment_matrix = scaler.fit_transform(games_segment_columnas)
        
    similarities = cosine_similarity(games_segment_matrix, user_games_matrix)
    
    similarity_df = pd.DataFrame(data=similarities, index=games_segment2['app_id'], columns=user_games2['app_id'])
    
    recommendations = similarity_df.reset_index().melt(id_vars='app_id', var_name='ID_Pair', value_name='similarity')
    recommendations = recommendations.sort_values(by='similarity', ascending=False)
    recommendations = recommendations.drop_duplicates(subset='app_id', keep='first')

    recommended_games = []
    game_ids = recommendations['app_id']
    for app_id in game_ids:
        recommend_games = games_ready.loc[games_ready['app_id'] == app_id, 'title']
        recommended_games.extend(recommend_games)  
   
    return recommended_games[:5]
