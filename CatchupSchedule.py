import datetime


class CatchupSchedule:
  playInfoDateFormat = "%Y-%m-%dT%H:%M:00Z"

  def __init__(self, stationId, startUtc, endUtc, programId, name):
    self._stationId = stationId
    self._startUtc = startUtc
    self._endUtc = endUtc
    self._programId = programId
    self._name = name
    
  def getPlayInfoUri(self):
    scheduledStartTime = "ScheduledStartTime=" + self.getPlayInfoDateString(self._startUtc)
    stationId = "stationid=" + self._stationId
    uri = "/dvrproxy/catchup/playinfo?" + scheduledStartTime + "&" + stationId
    return uri
    
  def getPlayInfoDateString(self, date):
    if date.microsecond is not 0:
      print("Date of the schedule for  " + self._programId + " has microseconds value not equal to 0 - this will result in wrong playinfo URL!!")
    return datetime.datetime.strftime(date, CatchupSchedule.playInfoDateFormat)
    
  def toString(self):
    return "CatchupSchedule {programId: " + self._programId + "}"