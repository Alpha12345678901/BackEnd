# BackEnd
Install Docker and docker-compose (https://docs.docker.com/compose/). On MacOS this can be accomplished by simply installing Docker Desktop (https://docs.docker.com/desktop/install/mac-install/).

Run the following command. This may take a while on the first go since it will build images.

docker-compose up

Backend will be available on http://localhost:8000/

You can test get API (http://127.0.0.1:8000/save_moves/chessgamelog) and post API (http://127.0.0.1:8000/rest_apis/postdata) in Postman.

Here is a sample raw JSON you can submit to the post API in Postman.

{
    "token": "newgame1",
    "turn": "white",
    "whiteAgentName": "player1",
    "blackAgentName": "player2",
    "timeControl": "",
    "result": "",
    "numberOfMoves": 1,
    "whiteMaterialLeftCurrent": 39,
    "blackMaterialLeftCurrent": 39,
    "materialDifferenceCurrent": 0,
    "whiteTimeLeftCurrent": "",
    "blackTimeLeftCurrent": "",
    "timeDifferenceCurrent": "",
    "whiteMoveLast": "e4",
    "blackMoveLast": ""
}

Note that you can set either whiteAgentName or blackAgentName (or both) to minimax and/or reinforcement to call on the minimax and/or reinforcement AIs to play.

Note that minimax and reinforcement AIs are currently not implemented, so random legal chess moves will be returned instead.

After the post API with the above data goes through, you can filter based on various parameters including the token by using the get API.

For example, here is the resulting raw JSON from this get API call where we filter for the token "newgame1" (http://127.0.0.1:8000/save_moves/chessgamelog?token=newgame1).

[
    {
        "token": "newgame1",
        "whiteAgentName": "player1",
        "blackAgentName": "player2",
        "timeControl": "",
        "result": "",
        "numberOfMoves": 1,
        "whiteMaterialLeftCurrent": 39,
        "blackMaterialLeftCurrent": 39,
        "materialDifferenceCurrent": 0,
        "whiteTimeLeftCurrent": "",
        "blackTimeLeftCurrent": "",
        "timeDifferenceCurrent": "",
        "whiteMoveLast": "e4",
        "blackMoveLast": ""
    }
]

Note that each unique token passed in to the post API corresponds to a unique chess game. Pass in an existing token if you want to update an existing game with the next player's move or a new tokenn for a new chess game.
