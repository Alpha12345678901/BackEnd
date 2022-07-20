from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ChessGameLog


class ChessGameLogSerializer(ModelSerializer):
    class Meta:
        model = ChessGameLog
        fields = ['whiteAgentName', 'blackAgentName', 'timeControl', 'moves', 'timeTracker', 'result',
                  'numberOfMoves', 'whiteMaterialLeftCurrent', 'blackMaterialLeftCurrent', 'materialDifferenceCurrent',
                  'whiteTimeLeftCurrent', 'blackTimeLeftCurrent', 'timeDifferenceCurrent', 'whiteMoveLast',
                  'blackMoveLast']

    def validate(self, user_data):
        if not (user_data['whiteAgentName'] or user_data['blackAgentName']
                or user_data['timeControl'] or user_data['moves'] or user_data['timeTracker'] or user_data['result']
                or user_data['numberOfMoves'] or user_data['whiteMaterialLeftCurrent']
                or user_data['blackMaterialLeftCurrent'] or user_data['whiteTimeLeftCurrent']
                or user_data['materialDifferenceCurrent'] or user_data['blackTimeLeftCurrent']
                or user_data['timeDifferenceCurrent'] or user_data['whiteMoveLast']
                or user_data['blackMoveLast']):
            print('One or more of the fields is missing.')
            return ValidationError
        return user_data

    def create(self, user_data):
        user_data['moves'] = list()
        user_data['moves'].append(user_data['whiteMoveLast'])

        if user_data['blackMoveLast'] != "":
            user_data['moves'].append(user_data['blackMoveLast'])

        user_data['timeTracker'] = list()
        user_data['timeTracker'].append(user_data['whiteTimeLeftCurrent'])

        if user_data['blackTimeLeftCurrent'] != "":
            user_data['timeTracker'].append(user_data['blackTimeLeftCurrent'])


        user_data['materialDifferenceCurrent'] = user_data['whiteMaterialLeftCurrent'] - \
                                                 user_data['blackTimeLeftCurrent']

        new_input = ChessGameLog.objects.create(**user_data)
        new_input.save()
        return new_input

    def update(self, existing_input, user_data):
        fields = ['whiteAgentName', 'blackAgentName', 'timeControl', 'moves', 'timeTracker', 'result',
                  'numberOfMoves', 'whiteMaterialLeftCurrent', 'blackMaterialLeftCurrent', 'materialDifferenceCurrent',
                  'whiteTimeLeftCurrent', 'blackTimeLeftCurrent', 'timeDifferenceCurrent', 'whiteMoveLast',
                  'blackMoveLast']
        for i in fields:
            '''
            if i == 'moves':
                field_value = user_data['moves']
                if user_data['numberOfMoves'] % 2 == 0:
                    field_value.append(user_data['whiteMoveLast'])
                else:
                    field_value.append(user_data['blackMoveLast'])
            elif i == 'timeTracker':
                field_value = user_data['moves']
                if user_data['numberOfMoves'] % 2 == 0:
                    field_value.append(user_data['whiteMoveLast'])
                else:
                    field_value.append(user_data['blackMoveLast'])
            '''
            if i == 'materialDifferenceCurrent':
                field_value = user_data['whiteMaterialLeftCurrent'] - user_data['blackMaterialLeftCurrent']
            else:
                field_value = user_data.get(i, getattr(existing_input, i))
            setattr(existing_input, i, field_value)
        existing_input.save()
        return existing_input


class ChessGameLogViewSet(ModelViewSet):
    serializer_class = ChessGameLogSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'options']
    queryset = ChessGameLog.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'whiteAgentName', 'blackAgentName', 'timeControl', 'result',
                        'numberOfMoves', 'whiteMaterialLeftCurrent', 'blackMaterialLeftCurrent',
                        'materialDifferenceCurrent', 'whiteTimeLeftCurrent', 'blackTimeLeftCurrent',
                        'timeDifferenceCurrent', 'whiteMoveLast', 'blackMoveLast')
