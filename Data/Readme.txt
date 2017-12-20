This directory includes two fake news dataset that contain both the news contents and social context information. The fake news ground truth are collected from two platforms: BuzzFeed and PolitiFact. For example, for PolitiFact, the data scheme is explained as follows:

 - News.txt: the news_id list, index by the row num. For example, 'PolitiFact_Real_1' is in the 1st row, so it's corresponding to index 1.
 - User.txt: the user_name list, index by the row num. For example, 'f4b46be21c2f553811cc8a73c4f0ff05' is in the 1st row, so so it's corresponding to index 1.
 - FakeNewsContent/@news_id_Webpage.json: the detail fake news content meta data, with news source, headline, image, body_text, publish_data, etc. The file name is the news id.
 - RealNewsContent/@news_id_Webpage.json: the detail real news content meta data, with news source, headline, image, body_text, publish_data, etc. The file name is the news id.
 - PolitiFactNewsUser.txt: the news-user relationship. For example, '240	1' means news 240 is posted/spreaded by user 1.
 - PolitiFactUserUser.txt: the user-user relationship. For example, '1589	1' means user 1589 is following user 1;


