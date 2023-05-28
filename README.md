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

La primera fase és la d'extracció (scraping). Es parteix d'un arxiu csv amb dades (nom, artista, any) d'un milió de cançons. A partir d'aquesta informació, es realitzen crides a l'api d'Spotify per tal d'extreure els atributs de cadascuna de les cançons. Aquests atributs son els que s'utilitzaràn per realitzar el clústering. Un cop aconseguida aquesta informació, s'emmagatzemen les noves dades a una base de dades utilitzant SQLite.

La segona fase és la fase de recomenació. Es llegeix informació de l'usuari i es crea un model Kmeans. Amb aquest model, som capaços d'agrupar les cançons segons els seus atributs i podem fer recomenació de cançons aparentment similars. Per realitzar aquestes prediccions, tenim diferents opcions; recomenar segons les últimes cançons escoltades o bé recomenar partint d'una playlist pròpia d'Spotify. Cada cançó crea un conjunt de recomenacions segons la distància en la que es troben. Es pren la cançó més pròxima a cada una de les cançons que utilizem, per tant si partim d'una playlist amb 20 elements, tindrem 20 noves recomenacions.



