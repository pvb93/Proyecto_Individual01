import streamlit as st
import pandas as pd
import ast

st.title('Consultas de películas')

# Import datasets
df = pd.read_csv('data/movies_etl.csv')
df_ml = pd.read_csv('data/movies_ml.csv')

#Set datatypes df

df['budget'] = pd.to_numeric(df['budget'])
df['release_date'] = pd.to_datetime(df['release_date'])
df['production_countries_name'] = df['production_countries_name'].apply(lambda x: ast.literal_eval(x))
df['production_companies_name'] = df['production_companies_name'].apply(lambda x: ast.literal_eval(x))

#Set datatypes df_ml
df_ml['release_year'] = pd.to_numeric(df_ml['release_year'])
df_ml['vote_count'] = pd.to_numeric(df_ml['vote_count'])
df_ml['vote_average'] = pd.to_numeric(df_ml['vote_average'])

st.markdown('***')
st.markdown('## Cantidad de peliculas que se estrenaron en el mes seleccionado')

#Function use in pelicula_mes
def obtener_n_mes(mes_name):
    '''
    Given the month's name returns it's associated number
    '''
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
    
    return meses.get(mes_name.lower(), 'Mes no válido')

#First endpoint
def peliculas_mes(mes):
    '''
    The input is the month's name. The function returns the number of movies that were released that month historically.
    '''
    #Transform string to number
    mes_n = obtener_n_mes(mes)
    if mes_n == 'Mes no válido':
        return 'Mes no válido'
    else:
    #Filter by the given month and then counts
        respuesta = df[df['release_date'].dt.month == mes_n]['title'].count()
        return {'mes':mes, 'cantidad':respuesta}
    
meses = st.text_input('Escriba el mes deseado')

end01 = peliculas_mes(meses)

if st.button('Consultar Mes'):
    if end01 != 'Mes no válido':
        st.write('Se estrenaron',end01['cantidad'],'películas históricamente en',end01['mes'])
    else:
        st.write(end01)

st.markdown('***')
st.markdown('## Cantidad de peliculas que se estrenaron en el día de la semana seleccionado')

#Function use in peliculas_dia
def obtener_n_dia(week):
    '''
    Given the day of the week's name returns it's associated number
    '''
    week_day = {
        'lunes': 0,
        'martes': 1,
        'miercoles': 2,
        'miércoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sabado': 5,
        'sábado': 5,
        'domingo': 6,
       }
    
    return week_day.get(week.lower(), 'Día no válido')
    
#Second endpoint
def peliculas_dia(dia):
    '''
    The input is the day of the week. The function returns the number of movies that were released that day historically.
    '''
     #Transform string to number
    dia_n = obtener_n_dia(dia)
    if dia_n == 'Día no válido':
        return 'Día no válido'
    else:
    #Filter by the given day and then counts
        respuesta = df[df['release_date'].dt.dayofweek == dia_n]['title'].count()
        return {'dia':dia, 'cantidad':respuesta}
    
dias = st.radio('Seleccione día de la semana',('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'))

end02 = peliculas_dia(dias)

st.write('Se estrenaron',end02['cantidad'],'películas históricamente')

st.markdown('***')
st.markdown('## Cantidad de peliculas, ganancia total y promedio de la franquicia seleccionada')

#Third endpoint
def franquicia(franquicia):
    '''
    The input is the franchise, returning the number of movies, total and average profit
    '''
    #Collection names
    collection_name = df['collection'].unique()
    #Verified if franquicia is a valid input
    if franquicia in collection_name:
        franquicia = franquicia
    elif (franquicia + ' Collection') in collection_name:
        franquicia = (franquicia + ' Collection')
    else:
        return 'Colección no encontrada'
    #Calculate output
    n_pelis = df[df['collection'] == franquicia]['title'].count()
    ganancia_total = df[df['collection'] == franquicia]['revenue'].sum()
    ganancia_promd = df[df['collection'] == franquicia]['revenue'].mean()
    return {'franquicia':franquicia, 'cantidad':n_pelis, 'ganancia_total':round(ganancia_total,0), 'ganancia_promedio':round(ganancia_promd,0)}

unique_collections = df['collection'].dropna().sort_values().unique().tolist()

collect = st.selectbox('Seleccione franquicia', unique_collections)

end03 = franquicia(collect)

st.write(end03['franquicia'], 'tiene',end03['cantidad'],'películas, con una gancia total de',end03['ganancia_total'],'y una gancia promedio de',end03['ganancia_promedio'])

st.markdown('***')
st.markdown('## Cantidad de peliculas producidas en el país seleccionado')

# create an empty set to hold unique countries
unique_country_0 = set()
# iterate over each row in the column with lists
for row in df['production_countries_name']:
    # update the set with the unique countries in the row
    unique_country_0.update(set(row))
# convert the set back to a list and set names to lowercase
unique_country = [country.lower() for country in list(unique_country_0)]

#Fourth endpoint
def peliculas_pais(pais):
    '''
    The input is the country, it returns the number of films produced in it
    '''
    pais_low = pais.lower()
    #Validate input
    if pais_low in unique_country:
        # create a boolean mask that is True for rows where pais appears in 'production_countries_name'
        mask = df['production_countries_name'].apply(lambda x: pais_low in [p.lower() for p in x])
        # use the boolean mask to filter the dataframe
        n_films = df[mask]['title'].count()
        return {'pais':pais, 'cantidad':n_films}
    else:
        return 'País no válido'

select_country = sorted([country for country in list(unique_country_0)])

pais_elegido = st.selectbox('Seleccione país', select_country)

end04 = peliculas_pais(pais_elegido)

st.write('En',end04['pais'], 'se han producido',end04['cantidad'],'películas')

st.markdown('***')
st.markdown('## Cantidad de peliculas producidas por la productora seleccionada y su ganancia total')

# create an empty set to hold unique companies
unique_company_0 = set()
# iterate over each row in the column with lists
for row in df['production_companies_name']:
    # update the set with the unique companies in the row
    unique_company_0.update(set(row))
# convert the set back to a list and set names to lowercase
unique_company = [company.lower() for company in list(unique_company_0)]

#Fifth endpoint
def productoras(productora):
    '''
    The input is the production company, returning the total profit and the number of movies they produced.
    '''
    productora_low = productora.lower()
    #Validate input
    if productora_low in unique_company:
        # create a boolean mask that is True for rows where productora appears in 'production_companies_name'
        mask = df['production_companies_name'].apply(lambda x: productora_low in [p.lower() for p in x])
        # use the boolean mask to filter the dataframe
        n_films = df[mask]['title'].count()
        total_revenue = df[mask]['revenue'].sum()
        return {'productora':productora, 'ganancia_total':total_revenue, 'cantidad':n_films}
    else:
        return 'Productora no válida'

select_company = sorted([company for company in list(unique_company_0)])

productora_elegido = st.selectbox('Seleccione productora', select_company)

end05 = productoras(productora_elegido)

st.write(end05['productora'], 'ha producido',end05['cantidad'],'películas, con una ganancia total de',end05['ganancia_total'])

st.markdown('***')
st.markdown('##  Inversión, ganancia, retorno y año de lanzamiento de la película seleccionada')

#Sixth endpoint
def retorno(pelicula):
    '''
    The input is the movie's title, it returns the investment, the profit, the return and the year in which it was released
    '''
    try:
        peli_low = pelicula.lower()
        #Find the index of the given title in the dataframe
        indx = df[df['title'].apply(lambda x: x.lower()) == peli_low].index
        inversion = list(df.loc[indx,'budget'].values)
        ganancia = list(df.loc[indx,'revenue'].values)
        retorno = list(df.loc[indx,'return'].values)
        anio = list(df.loc[indx,'release_year'].values)
        return {'pelicula':pelicula, 'inversion':inversion, 'ganancia':ganancia,'retorno':retorno, 'anio':anio}
    except:
        return 'Película no válida'
    
unique_movies = df['title'].dropna().sort_values().unique().tolist()

movie = st.selectbox('Seleccione película', unique_movies)

end06 = retorno(movie)

if type(end06['inversion']) != list:
    st.write('En',end06['pelicula'], 'se invirtió',end06['inversion'],'se tuvo una ganancia de',end06['ganancia'],'y un retorno de',end06['retorno'])
    st.write('La película se estrenó en el año',end06['anio'])
else:
    for i in range(len(end06['inversion'])):
        st.write('En',end06['pelicula'], 'se invirtió',end06['inversion'][i],'se tuvo una ganancia de',end06['ganancia'][i],'y un retorno de',end06['retorno'][i])
        st.write('La película se estrenó en el año',end06['anio'][i])

st.markdown('***')
st.markdown('##  Recomendación de películas basada en película seleccionada y dividida por períodos')

# ML endpoint

#Divide the data in 3 due to computational issues

#movies90 = df_ml[(df_ml['release_year'] < 1990)].reset_index()# Movies before 1990
movies91 = df_ml[(df_ml['release_year'] > 1998) & (df_ml['release_year'] < 2000)].reset_index()# Movies between 1990 and 2010
#movies20 = df_ml[(df_ml['release_year'] > 2000)].reset_index() # Movies after 2000

#Calculate cosine similarity
def vector_df(movies):
    '''
    The input is a dataframe. The output is the cosine similarity matrix between movies and
    a Series with the titles as index and indexes as values.
    '''
    #Vectorize column
    from sklearn.feature_extraction.text import CountVectorizer
    count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    count_matrix = count.fit_transform(movies['soup'])
    #Calculate cosine similarity
    from sklearn.metrics.pairwise import cosine_similarity
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    #Create a Series with index equal to title and values, equal to index
    indices = pd.Series(movies.index, index=movies['title'])
    return cosine_sim, indices

#Calculate weighted average votes
def weighted_rating(x, m, C):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

#Recomendation system
def recomendacion(titulo, movies, cosine_sim, indices):
    #Find movies's index
    idx = indices[titulo]
    #Verify if idx is an int, with repeating titles, recommend based on the last movie
    try:
        int(idx)
    except:
        idx = indices[titulo][-1]
    #Similiraty score of given movie with other movies
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:12]
    movie_indices = [i[0] for i in sim_scores]
    
    #Filter movies by ratings and vote counts
    movie_rmd = movies.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'release_year']]
    movie_rmd['years'] = abs(movie_rmd['release_year'] - movies.loc[idx,'release_year'])
    C_rm = movies['vote_average'].mean()
    m_rm = movies['vote_count'].quantile(0.60)
    qualified = movie_rmd[(movie_rmd['vote_count'] >= m_rm) & (movie_rmd['vote_count'].notnull()) & (movie_rmd['vote_average'].notnull()) & (movie_rmd['years'] <= 8)]
    qualified['wr'] = qualified.apply(weighted_rating, m = m_rm, C = C_rm,axis=1)
    qualified = qualified.sort_values(by = ['wr','years'],ascending=[False,True]).head(5)
    return {'lista recomendada': list(qualified['title'])}

#Get list of titles for each subdataset
#lista_movies90 = movies90['title'].dropna().sort_values().unique().tolist()
lista_movies91 = movies91['title'].dropna().sort_values().unique().tolist()
#lista_movies20 = movies20['title'].dropna().sort_values().unique().tolist()

#Apply vectorize and cosine similarity to each dataset
#cosine_sim90, indices90 = vector_df(movies91)
cosine_sim91, indices91 = vector_df(movies91)
#cosine_sim20, indices20 = vector_df(movies20)

#Movie selection & recomendation, movies before 1990

#titulo_elegido90 = st.selectbox('Películas estrenadas antes de 1990', lista_movies90)

#ml_90 = recomendacion(titulo_elegido90, movies90, cosine_sim90, indices90)

#st.write("Se recomiendan las siguientes películas")
#for item in ml_90['lista recomendada']:
#    st.write("- " + item)

#Movie selection & recomendation, between 1990 and 2010

titulo_elegido91 = st.selectbox('Películas estrenadas entre 1990 y 2010', lista_movies91)

ml_91 = recomendacion(titulo_elegido91, movies91, cosine_sim91, indices91)

st.write("Se recomiendan las siguientes películas")
for item in ml_91['lista recomendada']:
    st.write("- " + item)

#Movie selection & recomendation, after 2000

#titulo_elegido20 = st.selectbox('Películas estrenadas después del 2000', lista_movies20)

#ml_20 = recomendacion(titulo_elegido20, movies20, cosine_sim20, indices20)

#st.write("Se recomiendan las siguientes películas")
#for item in ml_20['lista recomendada']:
#    st.write("- " + item)
