# reddit_mood_bot_python
This is a working framework for a reddit bot that will analyze the overall mood of the thread. Analyses is performed via IBM tone-analyzer API. 

The overall goal of this reddit bot is to determine the moods of a thread. In particular, this bot examines: Emotional Tone, Language Tone, and Social Tone. It responds with the names of the tones for each tone category, as well as the score for that tone. 

The bot searches for two commands:

1) HOW HAPPY? - When found this will return the overall mood of the thread

Beep Boop. I am a bot! I have analyzed this thread and here's what I've found:

Overall emotional tone(s) with their score: Anger : 0.191071 Joy : 0.14016 Fear : 0.206538 Sadness : 0.241032 Disgust : 0.231747

Overall language tone(s) with their score: Anger : 0.586539 Fear : 0.373801 Disgust : 0.0

Overall social tone(s) with their score: Anger : 0.381211 Joy : 0.091186 Fear : 0.511307 Sadness : 0.528247 Disgust : 0.107561

2) WHATS MY MOOD? - When found this will return the overall mood of the user over their past 1000 comments (or number of comments specified). 

The files have been altered to allow any user to use this script and create their own bot. 

for more information on IBM tone-analyzer check out the link below

https://www.ibm.com/watson/services/tone-analyzer/
