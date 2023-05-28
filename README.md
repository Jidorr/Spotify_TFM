# TFM - Creació d’un model de recomenació musical utilitzant dades d’Spotify 

<img src="data\img\spotify.png" width="400"/>

## Arxius
 * **src/api_scraping/get_song_data.py**: arxiu utilitzat per la creació de la base de dades
 * **src/api_scraping/get_user_data.py**: arxiu utilitzat per obtenir informació de les cançons de l'usuari
 * **src/api_scraping/cred.py**: conté les credencials per identificar-se a l'api d'Spotify
 * **src/api_scraping/user_functions.py**: funcions utilitzades per aconseguir dades de l'usuari

 * **src/modeling/modeling.py**: creació del model
 * **src/modeling/predictions.py**: arxiu utilitzat per fer les prediccions (arxiu principal)
 * **src/modeling/data_analysis.ipynb**: anàlisi prèvi de les dades 

## Data
 * **data/files/song_data.csv**: arxiu original de 1M Song Dataset
 <img src="data\img\data.PNG" width="400"/>
 
 * **data/model/**: conté el model generat
 * **data/img/** : imatges

## Diagrama de flow
<img src="data\img\flow_diagram.PNG"/>

El procés consta de dues fases clau que treballen conjuntament per proporcionar recomanacions de música personalitzades i rellevants. A continuació, es descriurà cada fase en detall:

#### Fase 1: Extracció de dades

La primera fase del procés és l'extracció de dades, també coneguda com a scraping. Inicialment, es disposa d'un arxiu CSV que conté informació sobre un milió de cançons, incloent-hi el nom de la cançó, l'artista i l'any de publicació.

Utilitzant aquest arxiu com a punt de partida, es realitzen crides a l'API d'Spotify per obtenir informació detallada sobre cada cançó. A través d'aquestes crides, s'extreuen els atributs musicals i característiques específiques de cada cançó, com ara el tempo, la tonalitat, l'energia, l'acústica, el ritme i molts altres. Aquests atributs són essencials per realitzar el següent pas del procés, que és el clústering.

Una vegada que s'ha obtingut amb èxit tota aquesta informació per a cada cançó, les dades s'emmagatzemen en una base de dades utilitzant el sistema de gestió de bases de dades SQLite. Aquesta base de dades ens permetrà accedir i utilitzar posteriorment les dades per generar recomanacions de música personalitzades.

#### Fase 2: Recomanació de cançons

La segona fase és la fase de recomanació, on s'utilitza la informació de l'usuari per generar recomanacions de música. En aquesta fase, es recull informació rellevant de l'usuari, com ara les seves preferències musicals, les últimes cançons escoltades o una playlist personalitzada de Spotify.

Amb aquesta informació de l'usuari, es crea un model K-means, un algorisme de clústering que agrupa les cançons segons els seus atributs musicals. Aquest model de clústering ens permet agrupar les cançons en categories similars basades en els atributs musicals compartits.

A partir d'aquest model K-means, podem realitzar recomanacions de cançons que semblen similars a les preferències de l'usuari. Tenim diverses opcions per realitzar aquestes prediccions: podem recomanar cançons basades en les últimes cançons escoltades per l'usuari, o bé utilitzar una playlist pròpia de Spotify com a punt de partida per a les recomanacions.

Per cada cançó, s'obté un conjunt de recomanacions basades en la seva proximitat a altres cançons dins del mateix clúster. Per exemple, si partim d'una playlist amb 20 elements, s'utilitzen aquests elements com a punts de partida per buscar les cançons més properes en termes de similitud musical. Això ens proporciona 20 noves recomanacions de cançons que tenen característiques similars i s'ajusten als gustos musicals de l'usuari.

En resum, aquest procés consta de dues fases essencials: l'extracció de dades, on s'obté informació detallada de les cançons a través de l'API d'Spotify i s'emmagatzema en una base de dades, i la fase de recomanació, on s'utilitza la informació de l'usuari i un model de clústering per generar recomanacions de música personalitzades. Aquest sistema permet descobrir noves cançons que s'ajustin als gustos musicals de l'usuari basant-se en les similituds musicals entre les cançons.



