import praw
import config #config file contains all the reddit login information
import json
from pprint import pprint
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    username = 'USERNAME',
    password = 'PASSWORD',
    version='2016-05-19'
)



# this is somply the login process for Reddit usin the PRAW library
def login_reddit():
    login = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                 client_secret = config.client_secret,
                 user_agent = "MESSAGE ABOUT YOUR USER")
    login.config.store_json_result = True

    return login


login = login_reddit()


def run_my_bot(login):
    #URL can be any url you select
    #below will simply take in the comments of the particular thread and save them into a file
    submission = login.submission(url='https://www.reddit.com/r/explainlikeimfive/comments/80kjhf/eli5_how_come_when_im_underwater_water_doesnt/')
    with open('responses.txt', 'w') as outfile:
        for comment in submission.comments:
            outfile.write(comment.body.encode('ascii', 'ignore'))

    outfile.close()

    #below will utilize IBM tone_analyzer and save it into a JSON file

    f = open("responses.txt", 'r')
    with open('final.json','w') as outfile:
        outfile.write(json.dumps(
            tone_analyzer.tone(f.read(), content_type="text/plain")
            , indent=2))

    outfile.close()
    f.close()


    result = analyze_thread()

    #print to terminal the results
    print result

    #reply to the thread with the post-analyses results
    submission.reply(result)



def analyze_thread():
    myFile = open('final.txt')
    data = json.load(myFile) #load the JSON file

    emotion_list = {}

    language_list = {}

    social_list = {}


    #each of these loops below obtains the Tone as well as the score for that tone. It saves them into a dictionary
    for i in range(len(data['document_tone']['tone_categories'][0]['tones'])):
        emotion_list[data['document_tone']['tone_categories'][0]['tones'][i]['tone_name']] = data['document_tone']['tone_categories'][0]['tones'][i]['score']


    for i in range(len(data['document_tone']['tone_categories'][1]['tones'])):
        language_list[data['document_tone']['tone_categories'][0]['tones'][i]['tone_name']] = data['document_tone']['tone_categories'][1]['tones'][i]['score']

    for i in range(len(data['document_tone']['tone_categories'][2]['tones'])):
        social_list[data['document_tone']['tone_categories'][0]['tones'][i]['tone_name']] = data['document_tone']['tone_categories'][2]['tones'][i]['score']


    #obtain the results i.e. the comment that we will post on reddit

    result = "Beep Boop. I am a bot! I have analyzed this thread and here's what I've found: \n"

    emotion_rslt = "\nOverall emotional tone(s) with their score: \n"
    emtn = ''
    for key in emotion_list:
        emtn += key + " : " + str(emotion_list[key]) + '\n'

    result += emotion_rslt + emtn

    language_rslt = "\nOverall language tone(s) with their score: \n"
    lng = ''
    for key in language_list:
        lng += key + " : " + str(language_list[key]) + '\n'

    result += language_rslt + lng

    social_rslt = "\nOverall social tone(s) with their score: \n"
    scl = ''
    for key in social_list:
        scl += key + " : " + str(social_list[key]) + '\n'

    result += social_rslt + scl

    return result



run_my_bot(login)
