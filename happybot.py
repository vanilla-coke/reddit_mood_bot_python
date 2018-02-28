import praw
import config #config file contains all the reddit login information
import json
from pprint import pprint
from watson_developer_cloud import ToneAnalyzerV3
import time

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



    #able to set the subreddit, as well as the limit (max 1000)
    verified = False
    for comment in login.subreddit('NAME_OF_SUBREDDIT').comments(limit=100):

        #Below, this if statement simply checks to see if the comment contains HOW HAPPY?
        #if it does, the bot will compelte sentiment analyses on the particular thread else see 'ELIF' statement below

        #verified will be used to determine if both IF statements below should run or not
        if "HOW HAPPY?" in comment.body:
            with open('responses.txt', 'w') as outfile:
                submission = login.submission(url=comment.submission.url)
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
            #comment.reply(result)
            verified = True  #see line 107
            print(verified)



        #this statement runs if a user write "WHATS MY MOOD?"
        #the bot will obtain maximum of 1000 of that particular users comments and perform mood analyses
        #Note: if both HOW HAPPY? and WHATS MY MOOD? are present, then the script will only be able to send the former
        #this is due to reddits limit on commenting.

        if "WHATS MY MOOD?" in comment.body:
            c = comment
            with open('responses.txt', 'w') as outfile:
                for comment in login.redditor(str(comment.author)).comments.new(limit=None):

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


            result = analyze_user()

            #print to terminal the results
            print result




            #as in line 69, if verified was true this means we must wait 9 minutes to post i.e. 540 seconds
            # this we will wait 545 (just to be safe) before posting
            #if verified is false, we can just simply post without waiting.
            if(verified):
                time.sleep(545)
                c.reply(result) #reply to the thread with the post-analyses results
            else:
                c.reply(result)




def analyze_thread():
    myFile = open('final.json')
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

#this function is the same as analyze_thread however the respone is worded differently, and only deals with user comments
def analyze_user():
    myFile = open('final.json')
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

    result = "Beep Boop. I am a bot! I have analyzed your accounr and here's what I've found: \n"

    emotion_rslt = "\nYour most common overall emotional tones with scores are: \n"
    emtn = ''
    for key in emotion_list:
        emtn += key + " : " + str(emotion_list[key]) + '\n'

    result += emotion_rslt + emtn

    language_rslt = "\nYour most common overall language tones with scores are: \n"
    lng = ''
    for key in language_list:
        lng += key + " : " + str(language_list[key]) + '\n'

    result += language_rslt + lng

    social_rslt = "\nYour most common overall social tones with scores are: \n"
    scl = ''
    for key in social_list:
        scl += key + " : " + str(social_list[key]) + '\n'

    result += social_rslt + scl

    return result




#initialize bot
run_my_bot(login)
