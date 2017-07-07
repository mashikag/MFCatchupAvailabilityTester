import json
import CatchupSchedule
import datetime

class HubCache:
  hubCacheDateFormat = "%Y-%m-%dT%H:%M:%fZ"
  
  def __init__(self, strData):
    self.cache = json.loads(strData)
    self._splitHubCacheToIntervals()
    print("Retrived " + str(len(self._cacheIntervals)) + " cache intervals.")
    if not self._updateCurrentCacheInterval():
      print("Failed to find current cache interval in the hub cache.")
    
  def toString(self):
    objStr = "HubCache Instance\n"
    if self._currentCacheInterval:
      objStr += "startTime: " + datetime.datetime.strftime(self._currentCacheInterval.getStartTime(), HubCache.hubCacheDateFormat)
      objStr += "endTime: " + datetime.datetime.strftime(self._currentCacheInterval.getEndTime(), HubCache.hubCacheDateFormat)
      objStr += "numOfCatchupSchedules: " + str(len(self._currentCacheInterval.getSchedules()))
    else:
      objStr += "NOT GOOD - no currentCacheInterval!"
    print(objStr)
    
  def _splitHubCacheToIntervals(self):
    self._cacheIntervals = []
    for cacheInterval in self.cache:
      self._cacheIntervals.append(HubCacheInterval(cacheInterval))
      
  def _updateCurrentCacheInterval(self):
    self._currentCacheInterval = None
    utcNow = datetime.datetime.utcnow()
    for cacheInterval in self._cacheIntervals:
      if utcNow >= cacheInterval.getStartTime() and utcNow < cacheInterval.getEndTime():
        self._currentCacheInterval = cacheInterval
        break
    return self._currentCacheInterval
    
  def getCurrentCacheInterval(self):
    self._updateCurrentCacheInterval()
    return self._currentCacheInterval
    
###############################################################################################################################################################
class HubCacheInterval:
  def __init__(self, intervalData):
    self._startTime = datetime.datetime.strptime(intervalData['StartTime'], HubCache.hubCacheDateFormat)
    self._endTime = datetime.datetime.strptime(intervalData['EndTime'], HubCache.hubCacheDateFormat)
    self._initSchedulesArray(intervalData['Schedules'])
    
  def _initSchedulesArray(self, schedulesData):
    self._schedules = []
    for schedule in schedulesData:
      stationId = schedule['StationId']
      startUtc = datetime.datetime.strptime(schedule['StartUtc'], HubCache.hubCacheDateFormat)
      endUtc = datetime.datetime.strptime(schedule['EndUtc'], HubCache.hubCacheDateFormat)
      programId = schedule['ProgramId']
      name = schedule['Name']
      self._schedules.append(CatchupSchedule.CatchupSchedule(stationId, startUtc, endUtc, programId, name))
    
  def getStartTime(self):
    return self._startTime
    
  def getEndTime(self):
    return self._endTime
    
  def getSchedules(self):
    return self._schedules
    
  def toString(self):
    objStr = "HubCacheInterval Instance\n"
    objStr += "startTime: " + datetime.datetime.strftime(self._startTime, HubCache.hubCacheDateFormat) + "\n"
    objStr += "endTime: " + datetime.datetime.strftime(self._endTime, HubCache.hubCacheDateFormat) + "\n"