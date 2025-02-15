create table rating as select * from read_csv('../../you_do_1/data/rating_*.txt', columns = {'MovieId': 'int', 'UserId': 'int', 'Date': 'date', 'Rate':'int'} ) ;

-- This causes error because of fields containing ,
-- create table movie_title as select * from read_csv('../../you_do_1/data/movie_titles.csv', columns = {'MovieId':'int','PublishedYear':'int', 'Title':'varchar'}, header=false, delim=',', auto_detect=false)