import gzip
import os
import sys
import sqlite3

title_basics_filename = 'title.basics.tsv.gz'
title_ratings_filename = 'title.ratings.tsv.gz'

if os.path.exists('imdb.db'):
    print(':: imdb.db already exists.')
    recreate_db = input('Recreate database (y/n): ')
    if recreate_db != 'y':
        print(':: Aborting...')
        sys.exit(2)
    else:
        os.remove('imdb.db')

if (
    not os.path.exists(title_basics_filename)
    or not os.path.exists(title_ratings_filename)
):
    print(':: IMDB datasets not found.')
    print(
        f':: Please download {title_basics_filename}'
        f' and {title_ratings_filename} from https://datasets.imdbws.com'
    )
    sys.exit(1)


with sqlite3.connect('imdb.db') as conn:
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE title_basics (
            tconst text,
            titleType text,
            primaryTitle text,
            originalTitle text,
            isAdult integer,
            startYear integer,
            endYear integer,
            runtimeMinutes integer,
            genres text
        );
    ''')

    cur.execute('''
        CREATE TABLE title_ratings (
            tconst text,
            averageRating real,
            numVotes real
        );
    ''')

    conn.commit()
    print(':: Created DB imdb.db')
    print(
        f':: Importing data from {title_basics_filename} and'
        f' {title_ratings_filename}...'
    )

    print('\n:: Inserting into title_basics table...')
    with gzip.open(title_basics_filename, 'rb') as gz_title_basics:
        # skip header
        next(gz_title_basics)
        for line in gz_title_basics:
            items = line.decode().split('\t')
            items = [item.strip() for item in items]
            for x in range(len(items)):
                if '\\N' in items[x]:
                    items[x] = ''
            cur.execute('''
                INSERT INTO title_basics
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', items)
    conn.commit()

    print(':: Inserting into title_ratings table...\n')
    with gzip.open(title_ratings_filename, 'rb') as gz_title_ratings:
        # skip header
        next(gz_title_ratings)
        for line in gz_title_ratings:
            items = line.decode().split('\t')
            items = [item.strip() for item in items]
            for x in range(len(items)):
                if '\\N' in items[x]:
                    items[x] = ''
            cur.execute('''
                INSERT INTO title_ratings
                VALUES (?, ?, ?);
            ''', items)
    conn.commit()

    print(':: Data successfully imported to imdb.db database!')
