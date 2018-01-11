This directory includes two fake news dataset that contain both the news contents and social context information. The fake news ground truth are collected from two platforms: BuzzFeed and PolitiFact. For example, for PolitiFact, the data scheme is explained as follows:

 - News.txt: the news_id list, index by the row num. For example, 'PolitiFact_Real_1' is in the 1st row, so it's corresponding to index 1.
 - User.txt: the user_name list, index by the row num. For example, 'f4b46be21c2f553811cc8a73c4f0ff05' is in the 1st row, so so it's corresponding to index 1.
 - FakeNewsContent/@news_id_Webpage.json: the detail fake news content meta data, with news source, headline, image, body_text, publish_data, etc. The file name is the news id.
 - RealNewsContent/@news_id_Webpage.json: the detail real news content meta data, with news source, headline, image, body_text, publish_data, etc. The file name is the news id.
 - PolitiFactNewsUser.txt: the news-user relationship. For example, '240	1	1' means news 240 is posted/spreaded by user 1 for 1 time.
 - PolitiFactUserUser.txt: the user-user relationship. For example, '1589	1' means user 1589 is following user 1;

----------------------------------------------------------------------------------------------------------------
References
----------------------------------------------------------------------------------------------------------------

@article{shu2017fake,
  title={Fake News Detection on Social Media: A Data Mining Perspective},
  author={Shu, Kai and Sliva, Amy and Wang, Suhang and Tang, Jiliang and Liu, Huan},
  journal={ACM SIGKDD Explorations Newsletter},
  volume={19},
  number={1},
  pages={22--36},
  year={2017},
  publisher={ACM}
}
@article{shu2017exploiting,
  title={Exploiting Tri-Relationship for Fake News Detection},
  author={Shu, Kai and Wang, Suhang and Liu, Huan},
  journal={arXiv preprint arXiv:1712.07709},
  year={2017}
}
