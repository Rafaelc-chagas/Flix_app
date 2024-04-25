import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from actors.service import ActorService
from genres.service import GenreService
from movies.service import MovieService
from datetime import datetime


def show_movies():
    movie_service = MovieService()
    movies = movie_service.get_movies()

    if movies:
        st.write('Lista de Filmes:')
        movies_df = pd.json_normalize(movies)
        movies_df = movies_df.drop(columns=['actors', 'genre.id'])
        AgGrid(
            data=movies_df,
            key='movies_grid'
        )
    else:
        st.warning('Nenhum Filme encontrado.')

    st.title('Cadastrar novo Filme')
    title = st.text_input('Nome do Filme')

    genre_service = GenreService()
    genres = genre_service.get_genres()
    genre_names = {genre['name']: genre['id'] for genre in genres}
    selected_genre_name = st.selectbox('Gênero', list(genre_names.keys()))

    realease_date = st.date_input(
        label='Data de lançamento',
        value=datetime.today(),
        min_value=datetime(1900, 1, 1).date(),
        max_value=datetime.today(),
        format='DD/MM/YYYY',
    )

    actor_servie = ActorService()
    actors = actor_servie.get_actors()
    actor_names = {actor['name']: actor['id'] for actor in actors}
    selected_actors_names = st.multiselect('Atores/Atrizes', list(actor_names.keys()))
    selected_actors_ids = [actor_names[name] for name in selected_actors_names]

    resume = st.text_area('Resumo')

    if st.button('Cadastrar'):
        new_movie = movie_service.create_movies(
            title=title,
            genre=genre_names[selected_genre_name],
            release_date=realease_date,
            actors=selected_actors_ids,
            resume=resume,
        )
        if new_movie:
            st.rerun()
        else:
            st.error('Erro ao cadastrar Filme. Verifique os campos.')
