# Chatting Bot ⚙️ SteamPunk Girl ⚙️

A chatbot in a Telegram that has three possible branches for an answer:

- [x] **_The bot is answering following the rules._**
  - There is a small data set ([`Bot_config`](https://github.com/ElizaLo/Telegram-Bots/blob/master/Chatting%20Bot%20SteamPunk%20Girl/final_bot_config.py)) created by users that contains all possible questions and answers to them. This option uses a generative classifier (namely **Multinomial Naive Bayes classifier**) to generate answers to questions from `BOT_CONFIG`.

- [x] **_The bot is answering using Generative model._**
  - The [data set](https://github.com/Koziev/NLP_Datasets/blob/master/Conversations/Data/dialogues.zip) with dialogues and replica exchanges contains more than 130 MB, collected from fiction and similar sources. We receive a message from the user at the entrance and calculate the Levenstein distance to all qustions and issue a random answer from responses.
  
- [x] **_The bot is answering using failure phrase._**
  - If no answer was found using the two previous options, then one of the automatic failure answers is used.
  
  
## Code Organization

    ├── Chat.ipynb                      <- Creating simple chat
    ├── Chating Bot.ipynb               <- Chatting Bot with three branches of dialogue
    ├── Data preprocessing.ipynb        <- Preprocessing of the data set with dialogues and replica exchanges
    ├── Making Final Config.ipynb       <- Making final config
    ├── final_bot_config.py             <- Final version of BOT_CONFIG
    ├── Сlassifier of Intentions.ipynb  <- Different classifier for intentions

    
    
