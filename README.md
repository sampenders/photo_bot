# Motivation 
This is a twitter bot that pulls historic photos of Minneapolis from library archives and posts them with metadata includin the title, date, address, and description to to [@MplsPhotoBot](https://twitter.com/MplsPhotoBot). Currently, photos are pulled from the Hennepin County Library Digital Collections, Minnesota Digital Libary Minnesota Streetcar Museum Collection, and the University of Minnesota Library University Archives. 

I started this project because I enjoyed paging through these archives and seeing how Minneapolis used to be. Finding that there are simply too many photos to look through (this bot access about 100,000), and many interesting photos are not labeled well enough to be searchable, I thought that randomly choosing photos to look at could uncover some amazing, old scenes of Minneapolis.

# How it works
`send_tweet.py` randomly selects historic photos of Minneapolis from a sqlite database, downloads the photo and its metadata with `wget`, and posts it to twitter using the `tweepy` package.

Images are organized in a given library's digital collections by collection, and an id number within that collection. For example, the 200th photo within Hennepin County Library's Floyd Kelley collection can be accessed at the following URL:
https://digitalcollections.hclib.org/digital/collection/FloydKelley/id/200

Since the URL for a given photo is defined by this collection name and id number, each record has a URL we can easily access to retrieve metadata. Similarly, each photo has a unique url defined by its collection and ID number where it can be downloaded:
https://digitalcollections.hclib.org/digital/download/collection/FloydKelley/id/200/size/full

For each collection, I determined the maximum ID number.
