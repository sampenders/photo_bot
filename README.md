# photo_bot 
This is a twitter bot that pulls historic photos of Minneapolis from library archives and posts them with metadata includin the title, date, address, and description to to @MplsPhotoBot. Currently, photos are pulled from the Hennepin County Library Digital Collections, Minnesota Digital Libary Minnesota Streetcar Museum Collection, and the University of Minnesota Library University Archives. 

I started this project because I enjoyed paging through these archives and seeing how Minneapolis used to be. Finding that there are simply too many photos to look through (this bot access about 100,000), and many interesting photos are not labeled well enough to be searchable, I thought that randomly choosing photos to look at could uncover some amazing, old scenes of Minneapolis.

# How it works
Images are organized in a given library's digital collections by collection, and an id number within that collection. For example, the 200th photo within Hennepin County Library's Floyd Kelley collection can be accessed at the following URL:
https://digitalcollections.hclib.org/digital/collection/FloydKelley/id/200

Since the URL for a given photo is defined by this collection name and id number, each record has a URL we can easily access.

full_url = 'https://cdm16022.contentdm.oclc.org/digital/iiif/msn/' + str(photo_id) + '/full/1920,1920/0/default.jpg'
metadata_url = 'https://collection.mndigital.org//catalog/msn:' + str(photo_id) + '.json'
