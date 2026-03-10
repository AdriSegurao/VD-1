import pandas as pd

input_file = r"C:\Users\adria\OneDrive\Documentos\FIB\MDS\2_Cuatri\VD\simpsons_episodes.csv"
output_file = r'C:\Users\adria\OneDrive\Documentos\FIB\MDS\2_Cuatri\VD\simpsons_episodes_clean.csv'

df = pd.read_csv(input_file)

# Keep useful columns for the tasks 
important_cols = ["title", "season", "number_in_season", "number_in_series", "original_air_date", "imdb_rating", "imdb_votes", "us_viewers_in_millions"]
df = df[important_cols].copy()


# Covert types 
print(df.dtypes)

df["original_air_date"] = pd.to_datetime(df["original_air_date"], errors="coerce")
print(df.dtypes)

# Check NA
print(df.isna().sum())
print(df[df.isna().any(axis=1)])

# TODO: Hay que buscar la info a ver si la encontramos, eliminar o imputar es algo que en este caso puede afectar a el futuro análisis
# Rating se puede coger esas 3 y votos
# Pero los views y el numero de votos, no, porque estos datos son de 2016 y se ve muy afectada si los cogemos de 2026. Si decidimos actualizar la columna "us_viewers_in_millions" hay que cogerlo todo
# ver varianza para hacer un calculo de cuanto ha variado los votos en 2016 a ahora 2026 y asi poner un numero adecuado.

# Se puede actualizar todo el dataset

#Nos quedamos con las primeras 27 temporadas de los Simpson completas
df = df[df["season"] != 28]

# Hacmeos interpolacion lineal para imputar NAN por temporada para que no afecte a la tendencia
df["us_viewers_in_millions"] = df.groupby("season")["us_viewers_in_millions"].transform(lambda s: s.interpolate())

# Check duplicates 
print(df[df.duplicated()]) # No hay

#Derived columns
# 1. Separe de date by individual columns
df["air_year"] = df["original_air_date"].dt.year
df["air_month"] = df["original_air_date"].dt.month
df["weekday_num"] = df["original_air_date"].dt.weekday

# 2. Join the columns season and number_in_season
df["season_episode"] = ( "S" + df["season"].astype(int).astype(str).str.zfill(2) + "E" + df["number_in_season"].astype(int).astype(str).str.zfill(2))

# 3. Number of episodes in one season
episodes_per_season = df.groupby("season")["number_in_season"].count()
df["episodes_in_season_dataset"] = df["season"].map(episodes_per_season)

# Sort
df = df.sort_values(["original_air_date", "season", "number_in_season"]).reset_index(drop=True)
print(df)


df.to_csv(output_file, index=False)