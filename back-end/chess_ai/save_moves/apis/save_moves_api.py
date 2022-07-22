from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ChessGameLog


class ChessGameLogSerializer(ModelSerializer):
    class Meta:
        model = ChessGameLog
        fields = ['token', 'turn', 'whiteAgentName', 'blackAgentName', 'timeControl', 'result','numberOfMoves',
                  'whiteMaterialLeftCurrent', 'blackMaterialLeftCurrent', 'materialDifferenceCurrent',
                  'whiteTimeLeftCurrent', 'blackTimeLeftCurrent', 'timeDifferenceCurrent', 'whiteMoveLast',
                  'blackMoveLast']

    def validate(self, user_data):
        if not (user_data['token'] or user_data['turn'] or user_data['whiteAgentName'] or user_data['blackAgentName']
                or user_data['timeControl'] or user_data['result'] or user_data['numberOfMoves']
                or user_data['whiteMaterialLeftCurrent'] or user_data['blackMaterialLeftCurrent']
                or user_data['whiteTimeLeftCurrent'] or user_data['materialDifferenceCurrent']
                or user_data['blackTimeLeftCurrent'] or user_data['timeDifferenceCurrent'] or user_data['whiteMoveLast']
                or user_data['blackMoveLast']):
            print('One or more of the fields is missing.')
            return ValidationError
        return user_data

    def create(self, user_data):
        new_input = ChessGameLog.objects.create(**user_data)
        new_input.save()
        return new_input

    def update(self, user_data):
        print("made it")
        currentChessGame = ChessGameLog.objects.filter(id=user_data['id'])
        fields = ['token', 'turn', 'whiteAgentName', 'blackAgentName', 'timeControl', 'result',
                  'numberOfMoves', 'whiteMaterialLeftCurrent', 'blackMaterialLeftCurrent', 'materialDifferenceCurrent',
                  'whiteTimeLeftCurrent', 'blackTimeLeftCurrent', 'timeDifferenceCurrent', 'whiteMoveLast',
                  'blackMoveLast']
        for i in fields:
            currentChessGame[i] = user_data[i]
        currentChessGame.save()
        return currentChessGame


class ChessGameLogViewSet(ModelViewSet):
    serializer_class = ChessGameLogSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'options']
    queryset = ChessGameLog.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('token', 'turn', 'whiteAgentName', 'blackAgentName', 'timeControl', 'result', 'numberOfMoves',
                        'whiteMaterialLeftCurrent', 'blackMaterialLeftCurrent', 'materialDifferenceCurrent',
                        'whiteTimeLeftCurrent', 'blackTimeLeftCurrent', 'timeDifferenceCurrent', 'whiteMoveLast',
                        'blackMoveLast')
