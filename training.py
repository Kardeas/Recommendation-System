#user data
df_users_pca = data_filtered

# Drop the ID columns for scaling and PCA
users_pca_features = df_users_pca.drop(columns=['review_id', 'user_id', 'app_id'])

# Standardize the feature data
scaler = StandardScaler()
scaled_users_pca = scaler.fit_transform(users_pca_features)

# Apply PCA
pca = PCA(n_components=2)  # Reduce to 2 principal components for example
users_pca = pca.fit_transform(scaled_users_pca)

# Create DataFrames for PCA results
users_pca_df = pd.DataFrame(users_pca, columns=["Componente 1", "Componente 2"])

# Train K-means clustering on the PCA-reduced training data
kmeans_users_pca = KMeans(n_clusters=3, random_state=0)  # Example: 3 clusters
kmeans_users_pca.fit(users_pca_df)

# Assign cluster labels to the PCA DataFrames
users_pca_df['cluster'] = kmeans_users_pca.labels_

users_pca_final_df = pd.concat([df_users_pca[['review_id', 'user_id', 'app_id']].reset_index(drop=True), users_pca_df], axis=1)

print("\nFinal Training DataFrame with PCA and Clusters:")
print(users_pca_final_df)

#game data
train_games, temp_data = train_test_split(segmentacion_games, test_size=0.4, random_state=42)
test_games, val_games = train_test_split(temp_data, test_size=0.5, random_state=42)

train_columnas = train_games[["recommended", "rating_coded", "positive_ratio", "tag_1", "tag_2", "tag_3", "tag_4", "tag_5", "hours"]]
test_columnas = test_games[["recommended", "rating_coded", "positive_ratio", "tag_1", "tag_2", "tag_3", "tag_4", "tag_5", "hours"]]
val_columnas = val_games[["recommended", "rating_coded", "positive_ratio", "tag_1", "tag_2", "tag_3", "tag_4", "tag_5", "hours"]]

scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_columnas)
test_scaled = scaler.transform(test_columnas)
val_scaled = scaler.transform(val_columnas)

kmeans = KMeans(n_clusters=6, random_state=42)
train_games['Cluster'] = kmeans.fit_predict(train_scaled)

test_games['Cluster'] = kmeans.predict(test_scaled)
val_games['Cluster'] = kmeans.predict(val_scaled)
