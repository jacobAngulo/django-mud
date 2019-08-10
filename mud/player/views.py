from rest_framework import viewsets
from mud.player.serializers import PlayerSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from threading import Timer
from .models import Player
import requests
import json


class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = PlayerSerializer

    @action(detail=False, methods=['GET'])
    def players(self, request, pk=None):
        queryset = Player.objects.all()
        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def create_player(self, request, pk=None):
        token = request.data['token']

        response = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/status',
            headers={
                'Authorization': f'Token {token}'},
        )

        if response:

            data = response.json()
            # name = data['name']
            # gold = data['gold']
            # strength = data['strength']
            # encumbrance = data['encumbrance']

            new_player = Player(
                name=data['name'],
                token=token,
                gold=data['gold'],
                encumbrance=data['encumbrance'],
                visited='{}',
                path='[]'
            )

            new_player.save()

            return Response({'message': 'new player created'})
        else:
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
