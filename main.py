from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.conversation import Statement
import threading
import warnings
import sys
import time

# Disable all warning messages
warnings.filterwarnings("ignore")

chatbot = ChatBot(
    'mychatbot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Sorry, I do not understand.',
            'maximum_similarity_threshold': 0.8,
            'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance'
        },
        {
            'import_path': 'wolfram_alpha_adapter.WolframAlphaAdapter'
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'wikipedia_adapter.WikipediaAdapter'
        },
        {
            'import_path': 'gpt2_adapter.GPT2Adapter'
        }
    ]
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
trainer.train("my_corpus.yml")

conversation_history = []

def print_thinking_message(event):
    message = 'Bot is thinking...'
    for char in message:
        if event.is_set():
            break
        sys.stdout.write(char)
        sys.stdout.flush()

def clear_thinking_message():
    sys.stdout.write('\r')
    sys.stdout.write(' ' * len('Bot is thinking...'))
    sys.stdout.write('\r')
    sys.stdout.flush()

def print_response(response):
    for char in response:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)
    # Add this line
    sys.stdout.write('\n')

while True:
    request = input('You: ')
    if request.lower() == 'quit':
        break
    event = threading.Event()
    t1 = threading.Thread(target=print_thinking_message, args=(event,))
    t1.start()
    response = chatbot.get_response(request)
    event.set()
    t1.join()
    clear_thinking_message()
    conversation_history.append((request, response.text))
    print_response(response.text)