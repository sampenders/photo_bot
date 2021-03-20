echo "select * from photos where dont_post=1 order by posted_date;" | sqlite3 photoDB.db
