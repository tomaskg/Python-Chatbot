from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import wolframalpha

class WolframAlphaAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.client = wolframalpha.Client('6W2VKY-7429T3XE5W')

    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        res = self.client.query(statement.text)
        if res['@success'] == 'true':
            response_text = next(res.results).text
            confidence = 1
        else:
            response_text = "Sorry, I couldn't find anything on Wolfram Alpha about that."
            confidence = 0
        response_statement = Statement(text=response_text)
        response_statement.confidence = confidence
        return response_statement