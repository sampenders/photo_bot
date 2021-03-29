from send_tweet import description_parts

d = 'Written on back: "My dear Harry, Rec. your letter with views from Eugene. They were very nice. I sent you what you asked for yesterday. Hope you will get it all right. Mrs. Davies and I are going to town this morning so might not have time to write a letter. Will write one this afternoon. Thanks for the views, am so glad you are well. Love Mother. Mr. Tromer called up yesterday. and wished for your address. Guess he wants to write you. Bye Bye." Addressed to: "Mr. Harry H. Hoover, Portland Y.M.C.A." Postmarked Minneapolis, Minn Jun 17, 1913, 2:00 PM. Stamped Jun 20, 1913.'

a = description_parts(d)
print(a)
