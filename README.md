# imdb-movie-finder

This is a simple command line application written in Python that allows you to find movies from a local downloaded IMDB database based on various different criteria like:

- title type (tv, movie)
- name of the tv/movie (searches the for names starting with certain letters)
- minimum year it should have
- genres
- minimum rating
- minimum number of ratings provided by users

I wrote this program because I found it sort of annoying to find movies to watch directly from the IMDB website. I usually tend to apply various criteria like these to find a movie. So I thought why not make a command line application that does that for me?

It uses the data provided directly by IMDB on their website at [IMDB Datasets](https://datasets.imdbws.com).

By default without any arguments, it lists all the movies in the database.

## Help Menu

```
usage: find_movies.py [-h] [-t {tv,movie,short} [{tv,movie,short} ...]] [-n NAME] [-a] [-y YEAR] [-g GENRE [GENRE ...]] [-r RATING] [-nr NUM_RATINGS] [-ob {name,year,rating,num-ratings}] [--reverse]
                      [-l COUNT]

Find movies by filtering based on different criteria from IMDB database.

optional arguments:
  -h, --help            show this help message and exit
  -t {tv,movie,short} [{tv,movie,short} ...], --type {tv,movie,short} [{tv,movie,short} ...]
                        title type
  -n NAME, --name NAME  starting name of movie/tvshow
  -a, --adult           select adult movies
  -y YEAR, --year YEAR  minimum start year
  -g GENRE [GENRE ...], --genres GENRE [GENRE ...]
                        list of genres required
  -r RATING, --rating RATING
                        minimium rating required
  -nr NUM_RATINGS, --num-ratings NUM_RATINGS
                        minimum number of ratings
  -ob {name,year,rating,num-ratings}, --order-by {name,year,rating,num-ratings}
                        order results in ascending order based on: name, year, rating, or number of ratings
  --reverse             sort by descending order
  -l COUNT, --limit COUNT
                        limit search results to the amount specified by COUNT
```



# Examples

Get movies/tvshows starting from the year 2010 with a rating of at least 7.5 and number of ratings of 50,000:

`python find_movies.py --year 2010 --rating 7.5 --num-ratings 50000`



Get only movies with with the genres of comedy or crime that were made after the year of 2015 and order by the rating (ascending by default ,`--reverse` reverses the direction). Only display the top 5 results.

By specifying the genres, this doesn't mean it'll only fetch titles that are comedy and crime only. It just means comedy or crime should be present as the possible genres.

> `python find_movies.py --genres comedy crime --year 2015 --order-by rating --limit 5`
>
> or
>
> `python find_movies.py --genres comedy crime --year 2015 --order-by rating --limit 5 --reverse` for descending order by rating.



# Getting the IMDB Dataset

In order to use this program you need to have imdb.db (the sqlite database populated with the latest data from IMDB). The data files can be downloaded from [IMDB Datasets](https://datasets.imdbws.com).

You would need to download the following files:

- title.basics.tsv.gz
- title.ratings.tsv.gz

After downloading these files you can run `python create_imdb_db.py` to create the `imdb.db` file. This is a simple SQLite database. After the database has been created, you can use the `find_movies.py` program.
