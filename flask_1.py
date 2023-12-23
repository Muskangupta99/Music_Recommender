from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app= Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/', methods=['POST'])
def getvalue():
    song = request.form['song']
    rating = request.form['rating']
    print(song,rating)
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    def get_title_from_index(sr_no):
        return df[df.sr_no == sr_no]["Track_Name"]

    def get_index_from_title(Track_Name):
        return df.loc[df.Track_Name == Track_Name]["sr_no"].values[0]

    df = pd.read_csv("D:\\kiit\\top50.csv", encoding='latin-1')

    features = ['Track_Name', 'Artist_Name', 'Genre', 'Popularity']

    for feature in features:
        df[feature] = df[feature].fillna('')

    df["combined_features"] = df['Track_Name'].map(str) + df['Artist_Name'].map(str)
    print("Combined Features:", df["combined_features"].head())
    cv = CountVectorizer()

    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)
    movie_user_likes = song
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
    print("THIS IS THE LIST--->", sorted_similar_movies)
    my_objects = []

    i = 1
    i2 = 0
    a = [0] * 20
    for i in sorted_similar_movies:
        print(get_title_from_index(i[0]))
        sr = str(get_title_from_index(i[0])).split(',')
        sr = str(get_title_from_index(i[0])).isalpha()
        sr = str(get_title_from_index(i[0])).split('\n')
        # sr=str.replace(sr, " ", "",1)
        my_objects.append(sr[0])
        # my_objects.append(get_title_from_index(i[0]))
        i2 = i2 + 1
        if (i2 == 10):
            break
    print("HERE IS a", my_objects)

    dff = pd.DataFrame(columns=["Track_Name"])
    dff["Track_Name"] = my_objects
    dff.drop(dff[dff.Track_Name == "Series([], Name: Track_Name, dtype: object)"].index, inplace=True, axis=0)
    dff['Track_Name'] = dff['Track_Name'].str.replace('\d+', '')
    dff.set_index("Track_Name", inplace=True)
    dff.index.names = ['Tracks']
    dff=dff.to_html()

     

    col_names=["userid","sr_no","rating","timestamp"]
    songs = pd.read_csv(r"D:\kiit\top50.csv", encoding='latin-1')
    ratings=pd.read_csv(r"D:\kiit\Minor Project\ratings2.csv", encoding='latin-1')
    ratings = pd.merge(songs,ratings)

    ratings.head()
    userRatings = ratings.pivot_table(index=['userId'],columns=['Track_Name'],values='rating')
    userRatings.head()
    userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)

    userRatings.head()
    corrMatrix = userRatings.corr(method='pearson')
    corrMatrix.head(20)
    def get_similar(Track_Name,rating):
        similar_ratings = corrMatrix[Track_Name]*(rating-2.5)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings
    pop_lover = [("China",4)]
    similar_songs = pd.DataFrame()
    for Track_Name,rating in pop_lover:
        similar_songs = similar_songs.append(get_similar(Track_Name,rating),ignore_index = True)

    songr=similar_songs.sum().sort_values(ascending=False)
    songr.columns = ['Track_Name','Ratings']
    songr.head(10)
    songr=pd.DataFrame(songr)

    songr.head(10)
    songr=songr.drop([0], axis = 1)
    songr=songr.head(9)
    songr['Tracks']=songr.index
    songr.set_index("Tracks", inplace=True)
    songr=songr.to_html()
    return render_template('pass.html', song=song, rating=rating,a=dff,b=songr)
