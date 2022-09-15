# Description    
[@MplsPhotoBot](https://twitter.com/MplsPhotoBot) is a twitter bot that posts historic photos of Minneapolis with metadata (title, data, address, and caption). The photos are sourced from various public photo archives, totaling about 100,000 records. The account has 6,400 followers as of September 2022. This project was featured in [Racket](https://racketmn.com/you-gotta-follow-mplsphotobot/) and frequently appears in the [Southwest Voices newsletter](https://www.southwestvoices.news/posts/minneapolis-boys-hockey-team-in-historical-playoffs-tap-your-trees-for-syrup-park-board-meets-tonight).

I started this project because I enjoyed paging through these archives and seeing how Minneapolis used to be. Finding that there are simply too many photos to page through manually, I decided to let the computer do the work and hopefully present some gems in its random search.

This bot is driven by a Python script which utilizes the Twitter API. I built a sqlite database to store all available records to post and keep track of which have already been posted.
