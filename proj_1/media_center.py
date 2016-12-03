#!/usr/bin/python

# To include Non-ASCII characters in code
#coding=utf-8

import media
import fresh_tomatoes

your_name = media.Movie('你的名字', 
'Two high school kids who\'ve never met - city boy Taki and country girl Mitsuha - \
are united through their dreams.', 
'https://upload.wikimedia.org/wikipedia/zh/thumb/d/d6/Kiminona.jpg/340px-Kiminona.jpg', 
'https://youtu.be/ANWzJ19yEuY')

the_english_patient = media.Movie('The Egnlish Patient', 
'At the close of WWII, a young nurse tends to a badly-burned plane crash victim. \
His past is shown in flashbacks, revealing an involvement in a fateful love affair.', 
'https://upload.wikimedia.org/wikipedia/en/b/bd/The_English_Patient_Poster.jpg', 
'https://www.youtube.com/watch?v=Xk_LRcOFT0c')

jason_bourne_2016 = media.Movie('Jason Bourne (2016)', 
'The CIA\'s most dangerous former operative is drawn out of hiding to uncover \
more explosive truths about his past.', 
'https://upload.wikimedia.org/wikipedia/en/8/8b/Jason_Bourne_soundtrack_cover.jpg', 
'https://www.youtube.com/watch?v=v71ce1Dqqns')

the_good_the_bad_and_the_ugly = media.Movie('The good, the Bad and the Ugly', 
'A bounty hunting scam joins two men in an uneasy alliance against a third \
in a race to find a fortune in gold buried in a remote cemetery.', 
'https://upload.wikimedia.org/wikipedia/zh/3/3a/The_Good，the_bad_and_the_ugly.jpg', 
'https://www.youtube.com/watch?v=13EUXqIwDkQ')

doctor_strange = media.Movie('Doctor Strange', 
'A former neurosurgeon embarks on a journey of healing only to be drawn into \
the world of the mystic arts.', 
'https://upload.wikimedia.org/wikipedia/en/c/c7/Doctor_Strange_poster.jpg', 
'https://www.youtube.com/watch?v=HSzx-zryEgM')

# Array includes the movies above
movies = [your_name, the_english_patient, jason_bourne_2016, the_good_the_bad_and_the_ugly, doctor_strange]
# Show movies
fresh_tomatoes.open_movies_page(movies)