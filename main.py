import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

cuisines = ["イタリアン","日本食","メキシコ料理","インド料理","中国料理","フレンチ","タイ料理","アメリカ料理"]

def generate_restaurant_data(
        n_restaurants=100
) -> pd.DataFrame:
    price_ranges = [1000,2000,3000]

    data = {
        'restaurant_id': range(1, n_restaurants + 1),
        'name': [f'レストラン {i}' for i in range(1, n_restaurants + 1)],
        'cuisine': np.random.choice(cuisines, n_restaurants),
        'price_range': np.random.choice(price_ranges, n_restaurants),
        'rating': np.random.uniform(1, 5, n_restaurants).round(1),
        'distance_km': np.random.uniform(0.5, 20, n_restaurants).round(1),
    }

    for cuisine in cuisines:
        data[f'has_{cuisine.lower()}_speciality'] = np.random.choice([True, False], n_restaurants)
    
    return pd.DataFrame(data)

def ask_question(question):
    ans = input(question + " (y/n): ").strip().lower()
    while ans not in ['y','n']:
        print("y か n で答えてください")
        ans = input(question + " (y/n): ").strip().lower()
    return ans == 'y'

def create_user_profile(
) -> dict:
    profile = {
        'preferred_cuisines': [],
        'price_preference': '',
        'max_distance': 0,
        'min_rating': 0,
    }

    for cuisine in cuisines:
        if ask_question(f"{cuisine}が好きですか？"):
            # ユーザーが好みなら 1 そうでなければ 0 のベクトルを作成
            profile['preferred_cuisines'].append(cuisine)
    
    profile['price_preference'] = int(input("予算はいくらですか？ (1000, 2000, 3000): ").strip())
    profile['max_distance'] = float(input("最大距離は何kmですか？ "))
    profile['min_rating'] = float(input("最低評価は何点ですか？ "))

    return profile

def vectorize_restaurant(
        restaurant,user_profile
) -> np.array:
    vector = []

    if restaurant['cuisine'] in user_profile['preferred_cuisines']:
        vector.append(1)
    else:
        vector.append(0)

    # 予算が高いほど 1 に近づく
    vector.append(restaurant['price_range'] / 3000)

    # 評価が高いほど 1 に近づく
    vector.append(restaurant['rating'] / 5)

    # 距離が近いほど 1 に近づく
    vector.append(1 - (restaurant['distance_km'] / user_profile['max_distance']))

    return np.array(vector)

def recommend_restaurants(
        restaurants: pd.DataFrame, 
        user_profile: dict, 
        n_recommendations=5
) -> pd.DataFrame:
    # レストランの特徴量ベクトルを作成
    restaurant_vectors = np.array([vectorize_restaurant(row,user_profile) for _, row in restaurants.iterrows()])

    # ユーザーの理想的な特徴量ベクトルを作成(全部 1 になる)
    user_vector = np.ones_like(restaurant_vectors[0])

    similarities = cosine_similarity([user_vector], restaurant_vectors)[0]

    mask = (restaurants['rating'] >= user_profile['min_rating']) & (restaurants['distance_km'] <= user_profile['max_distance'])
    filtered_restaurants = restaurants[mask]
    filtered_similarities = similarities[mask]

    if filtered_restaurants.empty:
        return restaurants.sort_values('rating', ascending=False).head(n_recommendations)

    top_indices = filtered_similarities.argsort()[-n_recommendations:][::-1]
    return filtered_restaurants.iloc[top_indices]

if __name__ == '__main__':
    restaurants = generate_restaurant_data(100)
    user_profile = create_user_profile()
    recommendations = recommend_restaurants(restaurants, user_profile)
    print(recommendations[['name','cuisine','price_range','rating','distance_km']])

    



