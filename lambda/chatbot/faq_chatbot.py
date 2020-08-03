from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot import ChatBot
import logging

logging.getLogger().setLevel(logging.DEBUG)

BOT_NAME = 'Firebug'
KEY_ADD = '/add'
# TODO KEY_REPLACE = '/replace'


def ensure_nltk_download_succeeded():
    # If failed to complete nltk.download because of "certificate verify failed"
    # https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
    import nltk
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('stopwords')


class BaseChatbot():
    def __init__(self, name):
        self._name = name
        self.chatbot = ChatBot(
            name,
            database_uri='sqlite:///db.sqlite3',    # TODO
            logic_adapters=[
                'chatterbot.logic.BestMatch',
                #'chatterbot.logic.MathematicalEvaluation',
            ],
        )
        self.training()

    def add_conversations(self, converations):
        """Add converations (list of list) to training dataset"""
        trainer = ListTrainer(self.chatbot)
        for conversation in converations:
            trainer.train(conversation)

    def process_new_faq(self, content):
        """Process message with KEY_ADD"""
        lines = list(map(str.strip, content.split(KEY_ADD)[1:]))
        logging.debug(lines)
        self.add_conversations([lines])

    def running_on_terminal(self):
        """Running on terminal"""
        print('Type something to begin...')
        while True:
            try:
                user_input = input()

                if '/new' in user_input:
                    self.process_new_faq(user_input)
                    print('Learnt something new!')
                else:
                    print(self.chatbot.get_response(user_input))

            # Press ctrl-c or ctrl-d on the keyboard to exit
            except (KeyboardInterrupt, EOFError, SystemExit):
                break
    
    def training(self):
        """Initial training"""

        # Train the chatbot based on the english corpus
        ChatterBotCorpusTrainer(self.chatbot).train('chatterbot.corpus.english')

        who_am_i =[[question, f"I'm {self._name}."] for question in [
            'What is your name?',
            'Who are you?',
            'Do you have a name?',
        ]]
        self.add_conversations(who_am_i)


def main():
    ensure_nltk_download_succeeded()

    BaseChatbot(BOT_NAME).running_on_terminal()


if __name__ == '__main__':
     main()
