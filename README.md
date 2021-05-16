# Create Movies Collections

## User Register
Register User name and Password and provide Json access Token that have access time of 1 day.

## Access public api
Access public api for retrieving moives raw data, this is done by get request with BasiAuth credentials, 

## Models [Tabels]

### 1. Collections

|id |Title |Description |UUID |User_id|
|---|---|---|---|---|

### 2. Movies
|id |Title |Description |UUID| 
|---|---|---|----|

### 3. Genres
|id |Genre |
|---|---|

### Two Bridge tables

#### 1. CollectionMovies Table 
|id |Collection_id |Movie_id|
|---|---|---|

#### 2. MoviesGenre Table
|id |Movie_id |Genre_id |
|---|---|---|


## OPERATIONS
**1. Create Collections** <br>

**2. Read individual collection** <br>
**3. Read all the collection of a user** <br>
**4. Update movies in a given collection** <br>
**5. Delete collecton** <br>
