from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import wikipediaapi

class WikipediaAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.wiki = wikipediaapi.Wikipedia('simple')

    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        page = self.wiki.page(statement.text)
        if page.exists():
            response_text = page.summary
            confidence = 1
        else:
            response_text = "Sorry, I couldn't find anything on Wikipedia about that."
            confidence = 0
        response_statement = Statement(text=response_text)
        response_statement.confidence = confidence
        return response_statement