import random
import requests
import boto3
import os
from dotenv import load_dotenv


def send_email():
    load_dotenv()
    client = boto3.client(
        "sns",
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_ID"),
        region_name="us-east-1"
    )

    response = client.create_topic(Name="Pokemon")
    topic_arn = response["TopicArn"]

    # Publish to topic
    client.publish(TopicArn=topic_arn,
                   Message="Your Pokémon of the hour is " + getMon(),
                   Subject="Pokémon Of The Hour")


def subscribe(email):
    load_dotenv()
    client = boto3.client(
        "sns",
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_ID"),
        region_name="us-east-1"
    )

    response = client.create_topic(Name="Pokemon")
    topic_arn = response["TopicArn"]

    # Check to see if email is already subscribed
    subscriptions = client.list_subscriptions_by_topic(TopicArn=topic_arn).get('Subscriptions')
    found = False
    for sub in subscriptions:
        if sub.get('Endpoint') == email:
            found = True

    # Add subscriber to list
    if not found:
        response = client.subscribe(TopicArn=topic_arn, Protocol="Email", Endpoint=email)


def getMon():
    rng = random.randint(1, 925)  # There are 924 Pokémon
    url = "https://pokeapi.co/api/v2/pokemon/" + str(rng)
    # The URL for the API is found at pokeapi.co, instructions for using it are on their website
    request = requests.get(url)  # .get() will return all the contents that the URL will output from the given request
    name = request.json()["forms"][0]["name"].title()
    # This is just a lot of map navigation, but basically it pulls the generated Pokémon's name from the returned
    # JSON file
    return name