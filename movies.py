import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_movies():
    try:
        df = pd.read_csv("IMDb_Top_250_Movies.csv", encoding="ISO-8859-1")
        df['Director'] = df['Director'].fillna('Unknown')
        df['Stars'] = df['Stars'].fillna('Unknown')
        df['Name'] = df['Name'].fillna('Unknown')
        df['Release_Year'] = df['Release_Year'].fillna('Unknown')
        df['soup'] = df['Director'] + ' ' + df['Stars'] + ' ' + df['Name']
        return df
    except Exception as e:
        print(f"Error loading movies: {e}")
        return None

def get_recommendations(title, preference):
    df = load_movies()
    if df is None:
        return {"error": "Дані не знайдено."}

    indices = pd.Series(df.index, index=df['Name'].str.lower()).drop_duplicates()
    idx = indices.get(title.lower())

    if idx is None:
        return {"error": f"Фільм '{title}' не знайдено у базі даних."}

    if preference == "movie":
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['soup'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]
        recommendations = df.iloc[movie_indices][['Name', 'Rating', 'Director', 'Release_Year']]

    elif preference == "year":
        selected_movie_year = df.loc[idx, 'Release_Year']
        if selected_movie_year == 'Unknown':
            return {"error": "Рік випуску невідомий."}
        recommendations = df[df['Release_Year'] == selected_movie_year][['Name', 'Rating', 'Director', 'Release_Year']].head(10)

    elif preference == "director":
        selected_movie_director = df.loc[idx, 'Director']
        recommendations = df[df['Director'] == selected_movie_director][['Name', 'Rating', 'Director', 'Release_Year']].head(10)

    else:
        return {"error": "Некоректний вибір уподобань."}

    if recommendations.empty:
        return {"error": "Рекомендації не знайдено."}

    # Add icons
    icons = [
        '2025_18397876.png', 'balloons_6266664.png', 'fireworks_14301720.png',
        'heart_7450839.png', 'ornament_9047448.png', 'snowman_3737405.png',
        'snowman_7284636.png', 'tent_8612099.png'
    ]
    recommendations['icon'] = [icons[i % len(icons)] for i in range(len(recommendations))]

    return recommendations.to_dict(orient='records')
