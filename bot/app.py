import os
import re
import asyncio

import telepot
from telepot.async.delegate import per_message, create_open


class MeBot(telepot.async.helper.UserHandler):

    def __init__(self, seed_tuple, timeout):
        super(MeBot, self).__init__(seed_tuple, timeout, flavors=['inline_query', 'chosen_inline_result'])
        self._answerer = telepot.async.helper.Answerer(self.bot)

    def on_inline_query(self, msg):
        def compute_answer():
            article = {'type': 'article', 'id': 'me', 'title': 'My mood', 'parse_mode': 'markdown',
                       'thumb_url': 'http://s32.postimg.org/784wo23b9/avatar.png'}

            query_string = re.compile(r'([\[\*_`])').sub(r'\\\1', msg['query']).strip()

            if len(query_string) < 1:
                article.update({
                    'description': '{0}'.format(msg['from']['username']),
                    'message_text': '*{0}*'.format(msg['from']['username'])
                })
            else:
                article.update({
                    'description': '{0} {1}'.format(msg['from']['username'], query_string),
                    'message_text': '*{0}*``` {1}```'.format(msg['from']['username'], query_string)
                })

            return [article]

        self._answerer.answer(msg, compute_answer)

    # override default on_chosen_inline_result
    def on_chosen_inline_result(self, msg):
        pass

    # override default logger error in on_close, otherwise logs become messy
    def on_close(self, exception):
        pass

    # fix a bug with UserHandler expecting on_chat_message to be implemented
    def on_chat_message(self, msg):
        pass


ACCESS_TOKEN = os.getenv('TELEGRAM_API_KEY')

bot = telepot.async.DelegatorBot(ACCESS_TOKEN, [
    (per_message(), create_open(MeBot, timeout=0)),
])
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop())

print('Started!')

loop.run_forever()
