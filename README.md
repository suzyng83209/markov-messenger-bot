# EngHack 2017: GooseBoy

## Inspiration
At first, we wanted to create a bot because we were awful at replying to people. As the hackathon progressed, we realized the amazing potentials of a chat bot. 

## What it does
This project allows users to automatically reply so they can spend more time focusing on their busy lives. 

## How we built it
We used the Messenger API to scrape user conversations with people, which was parsed and cleaned using NLTK and pyenchant to create a user-based corpus. Based on the message received, the bot identifies keywords and uses Markov chains and POS tags to reply. A server written in JS hosted on Heroku listens for messages and acts as the communication point for the bot to send messages. GooseBoy also uses sentiment analysis to react to messages appropriately (angery react best react). 

## Challenges we ran into
It was difficult to find a good tradeoff since a larger corpus led to better grammar and more "English-sounding" sentences, but it took longer to identify keywords and send a message.

## Accomplishments that we're proud of
There's no hard coding in this project, and each conversation with a different person uses a different corpus, allowing the bot to have different "personalities" depending on who you talk to. 

## What we learned
Eating 8 of those coffee gummy cubes is a bad idea, regardless of how tired you are. 

## What's next for Goose Boy
Goose Boy will better use keywords to understand conversation context and will use better algorithms to create sentences faster. 

## Built With
We used: python, JavaScript, nltk, markov chains, machine learning, heroku, react native, and the Facebook API
