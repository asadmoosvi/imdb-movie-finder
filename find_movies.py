#!/usr/bin/env python

# Small command line program to filter movies from IMDB
import argparse
import sys
import sqlite3

def main(argv: list = None) -> int:
    db_name = 'imdb.db'
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        # order by
        args = parse_args()
        print(args)

        if args.order_by == 'name':
            order_by = 'primaryTitle'
        elif args.order_by == 'year':
            order_by = 'startYear'
        elif args.order_by == 'rating':
            order_by = 'averageRating'
        else:
            order_by = 'numVotes'

        print(f'order_by = {order_by}')
        if not args.reverse:
            sort_direction = 'ASC'
        else:
            sort_direction = 'DESC'

        print(f'Sort direction: {sort_direction}')
        print('\nSearching for movies based on the criteria provided...\n')
        cur.execute(f'''
            SELECT * from title_basics
            INNER JOIN title_ratings USING (tconst)
            ORDER BY {order_by} {sort_direction}
        ''')

        result = cur.fetchone()

        headings = [
            'Type', 'Name', 'Adult', 'Year',
            'Genres', 'Rating', 'Ratings'
        ]

        print(
            f'{headings[0]:<8}'
            f'{headings[1]:<60}'
            f'{headings[2]:<10}'
            f'{headings[3]:<10}'
            f'{headings[4]:<30}'
            f'{headings[5]:<10}'
            f'{headings[6]:<15}'
        )
        print('-' * 140)
        total_results_found = 0
        while result:
            title_type = result[1].lower()
            if title_type.startswith('tv'):
                title_type = 'tv'
            primary_title = result[2].lower()
            is_adult = result[4]
            if is_adult == 'f':
                is_adult = False
            elif is_adult == 't':
                is_adult = True
            year = result[5]
            genres = result[8].lower().split(',')
            rating = result[9]
            num_ratings = result[10]

            valid_title_type = title_type in args.type or len(args.type) == 0
            valid_primary_title = primary_title.startswith(args.name)
            valid_is_adult = is_adult == args.adult
            valid_year = not year or year >= args.year
            valid_genre = len(args.genres) == 0
            for genre in genres:
                if genre in args.genres:
                    valid_genre = True
                    break
            valid_rating = rating >= args.rating
            valid_num_ratings = num_ratings > args.num_ratings

            if (valid_title_type and valid_primary_title
                    and valid_is_adult and valid_year
                    and valid_genre and valid_rating
                    and valid_num_ratings):
                print(
                    f'{title_type:<8}'
                    f'{primary_title:<60}'
                    f'{is_adult:<10}'
                    f'{year:<10}'
                    f"{', '.join(genres):<30}"
                    f'{rating:<10}'
                    f'{int(num_ratings):<15,}'
                )
                total_results_found += 1
                if args.limit:
                    if total_results_found == args.limit:
                        break
            result = cur.fetchone()
        print(f'\nTotal results found: {total_results_found}')
    return 0

def parse_args(argv: list = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Find movies by filtering based on different criteria '
                    'from IMDB database.'
    )
    parser.add_argument(
        '-t', '--type', help='title type',
        nargs='+', choices=['tv', 'movie', 'short'],
        default=[]
    )
    parser.add_argument(
        '-n', '--name', help='starting name of movie/tvshow',
        action='store', type=str.lower,
        default=''
    )
    parser.add_argument(
        '-a', '--adult', help='select adult movies',
        action='store_true'
    )
    parser.add_argument(
        '-y', '--year', help='minimum start year',
        type=int,
        default=0
    )
    parser.add_argument(
        '-g', '--genres', help='list of genres required',
        nargs='+', type=str.lower, metavar='GENRE',
        default=[]
    )
    parser.add_argument(
        '-r', '--rating', help='minimium rating required',
        type=float, default=0.0
    )
    parser.add_argument(
        '-nr', '--num-ratings', help='minimum number of ratings',
        type=int, default=0
    )
    parser.add_argument(
        '-ob', '--order-by', help='order results in ascending order based on:'
                                 ' name, year, rating, or number of ratings',
        choices=['name', 'year', 'rating', 'num-ratings'], default='num-ratings'
    )
    parser.add_argument(
        '--reverse', help='sort by descending order',
        action='store_true'
    )
    parser.add_argument(
        '-l', '--limit', help='limit search results to the amount specified by COUNT',
        metavar='COUNT', type=int
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    sys.exit(main())
