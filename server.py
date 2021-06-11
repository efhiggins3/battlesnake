import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        return {
            "apiversion": "1",
            "author": "efhiggins3",
            "color": "#F4B400",
            "head": "pixel",
            "tail": "pixel",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        data = cherrypy.request.json

        move_values = {
          "up": {"x": 0, "y": 1},
          "down": {"x": 0, "y": -1},
          "left": {"x": -1, "y": 0},
          "right": {"x": 1, "y": 0}
        }
        possible_moves = list(move_values.keys())
        
        # Board configuration
        b_y = data["board"]["height"]-1
        b_x = data["board"]["width"]-1
        my_x = data["you"]["head"]["x"]
        my_y = data["you"]["head"]["y"]

        # Where my snake came from
        sb_x = data["you"]["body"][1]["x"]
        sb_y = data["you"]["body"][1]["y"]

        # Avoid walls
        if my_x == b_x:
          possible_moves.remove("right")
        if my_y == 0:
          possible_moves.remove("down")
        if my_x == 0:
          possible_moves.remove("left")
        if my_y == b_y:
          possible_moves.remove("up")

        # Avoid turning back on myself
        if my_y == sb_y - 1:
          possible_moves.remove("up")
        if my_y == sb_y + 1:
          possible_moves.remove("down")
        if my_x == sb_x - 1:
          possible_moves.remove("right")
        if my_x == sb_x + 1:
          possible_moves.remove("left")

        move = random.choice(possible_moves)
        
        # Avoid running into any piece of the body
        new_x = my_x + move_values[move]["x"]
        new_y = my_y + move_values[move]["y"]

        for seg in data["you"]["body"]:
          if seg["x"] == new_x and seg["y"] == new_y:
            possible_moves.remove(move)
            # Pull a new move
            move = random.choice(possible_moves)

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
