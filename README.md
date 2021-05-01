# Content-based-recommendation
A content based recommendation program that performs item-item neighborhood collaborative filtering. This repo uses movie rating data to form a movie-user matrix and learn representations to recommend top N movies based on user id.
## Requirements
Requirements can be found in `requirements.txt`
## Datasets
Datasets are from the Movielens dataset
- Rating.csv: Ratings given to movies by users
- Movies_w_imgurl.csv: Movie metadata including genres
- Tags.csv: Tags given to movies by users
## Recommendation Generation
In practice, adjust input.txt to change user ids to generate recommendations for
1. Adjust input.txt. The input format is `user_id` for each line
2. Run `python main.py`
3. Check `output.txt` for results. The output format is `user_id, movie_id, prediction_score` for each line. The result is sorted in descending order
