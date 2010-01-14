import sys
sys.path.append('tornado')
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.template
import re
import os
import traceback
import setgame

loader = tornado.template.Loader(os.path.join(os.path.join(os.path.realpath(__file__) + '/../'), 'templates'))

class NewPlayerHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player')
        super(NewPlayerHandler, self).__init__(*args, **kwargs)

    def get(self):
        self.write(loader.load('index.html').generate(player=self.player))

class TableHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player')
        super(TableHandler, self).__init__(*args, **kwargs)

    def get(self):
        self.write(loader.load('table.html').generate(player=self.player))

class PlayerMessage(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player')
        super(PlayerMessage, self).__init__(*args, **kwargs)

    def open(self):
        self.receive_message(self.on_message)

    def on_message(self, message):
        cards = []
        try:
            for card_id in message.split(' '):
                cards.append(setgame.Deck.id_to_card[card_id])
            self.player.found_set(cards)
            self.write_message('Got one!')
        except setgame.GameException, e:
            self.write_message(str(e))
        except Exception, e:
            self.write_message('Error: ' + str(e))
        self.receive_message(self.on_message)

settings = {'static_path': os.path.join(os.path.realpath(__file__ + '/../'), 'static')}

game = setgame.Game()
player = setgame.Player(game=game, name="Player")

application = tornado.web.Application(**settings)
application.add_handlers('.*$', [(r'/', NewPlayerHandler, {'player': player}),
                                 (r'/table', TableHandler, {'player': player}),
                                 (r'/get', PlayerMessage, {'player': player})])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9998)
    tornado.ioloop.IOLoop.instance().start()
