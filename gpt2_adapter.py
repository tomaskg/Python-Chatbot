from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from transformers import pipeline
import re
import warnings

# Disable all warning messages
warnings.filterwarnings("ignore")

class GPT2Adapter(LogicAdapter):
    def __init__(self, chatbot,
                 model='gpt2',
                 max_length=500,
                 pad_token_id=50256,
                 context_file='bot_context.txt',
                 num_sentences=3,
                 temperature=0.9,
                 top_k=50,
                 top_p=0.9,
                 **kwargs):
        super().__init__(chatbot, **kwargs)
        self.generator = pipeline('text-generation', model=model,
                                  max_length=max_length,
                                  pad_token_id=pad_token_id)
        with open(context_file, 'r') as f:
            self.context = f.read()
        self.num_sentences = num_sentences
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p

    def can_process(self, statement):
        return True

    def process(self, statement,
                additional_response_selection_parameters=None):
        prompt = self.context + '\nUser: ' + statement.text + '\nBot: '
        response_text = self.generator(prompt,
                                       temperature=self.temperature,
                                       top_k=self.top_k,
                                       top_p=self.top_p)[0]['generated_text']
        truncated_response_text = self.truncate_text(response_text)
        confidence = 1
        response_statement = Statement(text=truncated_response_text)
        response_statement.confidence = confidence
        return response_statement

    def truncate_text(self, text):
        text_after_bot = text.split('Bot: ')[-1]
        text_before_next_user_or_bot = re.split(r'User: |Bot:', text_after_bot)[0]
        sentences = re.split(r'(?<=[.!?])\s', text_before_next_user_or_bot)
        truncated_text = ' '.join(sentences[:self.num_sentences])
        return truncated_text