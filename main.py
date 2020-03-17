import requests
import tweepy
import json
import time
from pprint import pprint
import random
from keys import *

def get_poke(mention):
    pokedex = random.randint(0 , 807)
    pokedex = str(pokedex)
    url = "https://pokeapi.co/api/v2/pokemon/" + pokedex
    response = requests.get(url)
    data = response.json()
    name = data['name']
    name = name.capitalize()
    type = data['types'][0]['type']['name']
    type = type.capitalize()
    api.update_status('@' + mention.user.screen_name+ ("\nPokemon: " + name + "\n") +  ("Pokedex #: " + str(data['id']) + "\n") +   ("Type: " + type), mention.id)



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


file = 'last_seen_id.txt'

def retrieve_last_seen_id(file):
    f_read = open(file, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file):
    f_write = open(file, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply():
    print("test")
    last_seen_id = retrieve_last_seen_id(file)

    mentions = api.mentions_timeline(last_seen_id , tweet_mode = 'extended' )

    for mention in reversed(mentions):
        print(str(mention.id) +" - "+ mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id,file)
        if  '#poke' in mention.full_text.lower():
            print("found poke")

            get_poke(mention)

while True:
    reply()
    time.sleep(15)
