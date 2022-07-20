from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

def get_moves_default():
    return list()

def get_time_tracker_default():
    return list()

class ChessGameLog(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    whiteAgentName = models.CharField(max_length=1000)
    blackAgentName = models.CharField(max_length=1000)
    timeControl = models.CharField(max_length=100, default='N/A')
    # moves = models.CharField(max_length=10000)
    moves = ArrayField(models.CharField(max_length=100), default=get_moves_default)
    # timeTracker = models.CharField(max_length=10000, default='N/A')
    timeTracker = ArrayField(models.CharField(max_length=100), default=get_time_tracker_default)
    result = models.CharField(max_length=100, default='ongoing')
    numberOfMoves = models.PositiveIntegerField(default=0)
    whiteMaterialLeftCurrent = models.PositiveIntegerField(default=39)
    blackMaterialLeftCurrent = models.PositiveIntegerField(default=39)
    materialDifferenceCurrent = models.IntegerField(default=0)
    whiteTimeLeftCurrent = models.CharField(max_length=100, default='N/A')
    blackTimeLeftCurrent = models.CharField(max_length=100, default='N/A')
    timeDifferenceCurrent = models.CharField(max_length=100, default='N/A')
    whiteMoveLast = models.CharField(max_length=100)
    blackMoveLast = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        if not (self.whiteAgentName or self.blackAgentName or self.timeControl or self.moves
                or self.timeTracker or self.result or self.numberOfMoves or self.whiteMaterialLeft
                or self.blackMaterialLeft or self.materialDifference or self.whiteTimeLeftCurrent
                or self.blackTimeLeftCurrent or self.timeDifferenceCurrent or self.whiteMoveLast or self.blackMoveLast):
            return u'One or more of the fields is missing'
        else:
            return u'Id: %d, White Agent Name: %s, Black Agent Name: %s, Time Control: %s, Moves: %s, ' \
                   u'Time Tracker: %s, Result: %s, Number of Moves: %d, White Material Left Current: %d, ' \
                   u'Black Material Left: %d, Material Difference Current: %d, White Time Left Current: %s, ' \
                   u'Black Time Left Current: %s, Time Difference Current: %s, White Move Last: %s, Black Move Last: %s' % (self.id,
                                                                                               self.whiteAgentName,
                                                                                               self.blackAgentName,
                                                                                               self.timeControl,
                                                                                               self.moves,
                                                                                               self.timeTracker,
                                                                                               self.result,
                                                                                               self.numberOfMoves,
                                                                                               self.whiteMaterialLeftCurrent,
                                                                                               self.blackMaterialLeftCurrent,
                                                                                               self.materialDifferenceCurrent,
                                                                                               self.whiteTimeLeftCurrent,
                                                                                               self.blackTimeLeftCurrent,
                                                                                               self.timeDifferenceCurrent,
                                                                                               self.whiteMoveLast,
                                                                                               self.blackMoveLast)
