from urllib import response
import streamlit as st
import pickle
import pandas as pd
import requests 

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4715b9e5ea265522c04207c91d6f0a75&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original/"+data['poster_path']




movies_dict=pickle.load(open('movie_dict.pkl','rb'))
moviees=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster


def recommend2(*movie):
    movie_indices=[]
    for i in movie:
        movie_indices.append(moviees[moviees['title']==i].index[0])
    
    sum=0
    
    for j in movie_indices:
        sum+=similarity[j]
    distances=sum/len(movie)
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    recommended_movies=[]
    recommended_movies_poster=[]
    
    
    for i in movie_list:
        movie_id=moviees.iloc[i[0]].movie_id
        recommended_movies.append(moviees.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

st.title('Movie Recommender System')
selected_movie_name=st.multiselect("Enter the movie below:(Multiple Movies can also be selected)",moviees['title'].values)
if st.button('Recommend'):
    names,posters=recommend2(*selected_movie_name)

        

    col1,col2,col3,col4,col5,col6,col7,col8,col9,col10=st.columns(10)
    cols=[col1,col2,col3,col4,col5,col6,col7,col8,col9,col10]

    for i in range(1,11):
        with cols[i-1]:
            st.text(names[i-1])
            st.image(posters[i-1])