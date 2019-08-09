from rest_framework import viewsets
from mud.player.serializers import PlayerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from threading import Timer
import requests
import json

# token = 'a59389e4f3a4ed93a20b676b768c7f8e01c00d4b'


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = PlayerSerializer

    @action(detail=False, methods=['POST'])
    def create_player(self, request, pk=None):
        pass

    @action(detail=False, methods=['POST'])
    def mine(self, request, pk=None):
        token = request.data['token']
        def loop():

            print('here')

            current_response = requests.get(
                'https://lambda-treasure-hunt.herokuapp.com/api/adv/init',
                headers={
                    'Authorization': f'Token {token}'},
            )

            if current_response:
                print(current_response, current_response.json()
                      ['cooldown'], len(token))
                Timer(current_response.json()['cooldown'],
                      loop).start()
            else:
                print(current_response)
                pass

            # loop

            # if player is at a mining spot and has a name
            # -> mine

            # else if the player has a name but isn't at a mining spot
            # -> find a mining spot

            # else if a player has no name but has enough gold to buy one and is at name changer
            # -> change name

            # else if player has no name but has enough gold to buy a name but isn't at
            # the name changer
            # -> find the name changer

            # else if player has no name and not enough gold to buy the name
            # -> if the player is encumbered and at the store
            # -> -> sell treasure
            # -> else if player is not encumbered
            # -> -> find and pick up treasure
            pass

        initial_response = requests.get(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/init',
            headers={
                'Authorization': f'Token {token}'},
        )

        if initial_response:

            Timer(initial_response.json()[
                  'cooldown'], loop).start()
            return Response({'message': 'traversal has commenced'})

            # return Response({'success': initial_response.json()['room_id']})

        else:
            return Response({'error': f'{initial_response}'})
