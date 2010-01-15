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

games = []

class NewGameHandler(tornado.web.RequestHandler):
    def get(self):
        game = setgame.Game()
        game.url = '/' + str(id(game))
        games.append(game)
        application.add_handlers(r'.*$', [(r'/' + str(id(game)), NewPlayerHandler, {'game': game})])
        self.redirect('/' + str(id(game)))

class NewPlayerHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.game = kwargs.pop('game')
        super(NewPlayerHandler, self).__init__(*args, **kwargs)

    def get(self):
        player = setgame.Player(game=self.game)
        application.add_handlers(r'.*$', [(r'/' + str(id(self.game)) + '/' + str(id(player)) + '/get', PlayerMessage, {'player': player})])
        application.add_handlers(r'.*$', [(r'/' + str(id(self.game)) + '/' + str(id(player)) + '/table', TableHandler, {'player': player})])
        application.add_handlers(r'.*$', [(r'/' + str(id(self.game)) + '/' + str(id(player)), PlayerHandler, {'player': player})])
        self.redirect('/' + str(id(self.game)) + '/' + str(id(player)))

class PlayerHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player')
        super(PlayerHandler, self).__init__(*args, **kwargs)

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
        self.player.socket = self
        super(PlayerMessage, self).__init__(*args, **kwargs)

    def open(self):
        for player in self.player.game.players:
            if player == self.player:
                continue
            try:
                player.socket.write_message('Another player joined')
            except:
                pass
        self.receive_message(self.on_message)

    def on_message(self, message):
        cards = []
        try:
            for card_id in message.split(' '):
                cards.append(setgame.Deck.id_to_card[card_id])
            self.player.found_set(cards)
            results = ['Score']
            for number, player in enumerate(self.player.game.players):
                results.append('Player %s: %s' % (number + 1, player.sets))
            for player in self.player.game.players:
                try:
                    player.socket.write_message('<br/>'.join(results))
                except:
                    pass
        except setgame.GameException, e:
            self.write_message('Error: ' + str(e))
        except Exception, e:
            self.write_message('Error: ' + str(e))
            print traceback.print_exc()
        self.receive_message(self.on_message)

settings = {'static_path': os.path.join(os.path.realpath(__file__ + '/../'), 'static')}

application = tornado.web.Application(**settings)
application.add_handlers('.*$', [(r'/', NewGameHandler)])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9998)
    tornado.ioloop.IOLoop.instance().start()
