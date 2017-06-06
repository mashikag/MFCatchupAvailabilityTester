import datetime
import urllib.parse
import urllib.request

#Functions to retrieve schedules
class HubCacheRetriever: 
  def __init__(self, appgwUrl, slot):
    self.appgwUrl = appgwUrl
    self.slot = slot
    
  def getCache(self, timestamp, channelMapId, popularityOrder = False):
    cacheUrl = self._buildCacheUrl(timestamp, channelMapId, popularityOrder)
    print("The channel map hub catchup cache url generated is : \n", cacheUrl)
    cache = None
    self.lastRequestedUrl = cacheUrl
    try:
      cache = urllib.request.urlopen(cacheUrl).read()
    except urllib.error.HTTPError:
      print("HTTPError when trying to obtain Hub Cache. URL:" + cacheUrl)
    return cache
    
  def _buildCacheUrl(self, timestamp, channelMapId, popularityOrder = False):
    utcDateStr = datetime.datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
    blobContainerName = str(self.slot).lower() + "-catchup-data-" + utcDateStr
    strOrderBy = "Popularity-" if popularityOrder else ""
    cacheFileName = "channelmap-hub-" + strOrderBy + channelMapId + ".gz"
    #format of the url: http://{appgwUrl}/catalogcache/{bloblContainerName}/channelmap-hub-[Popularity-]{channelMapId}.gz
    cacheUrl = self.appgwUrl.replace("{type}", "storage") + "catalogcache/" + blobContainerName + "/" + cacheFileName
    return cacheUrl

    
class PerStationCacheRetriever:
  def __init__(self, appgwUrl, slot):
    self.appgwUrl = appgwUrl
    self.slot = slot
    
  def getCache(self, requestedTimestamp, countPerStation, stations, top, popularityOrder = False):
    cacheUrl = _buildPerStationCatchupCacheUrl(requestedTimestamp, countPerStation, stations, top, popularityOrder)
    print("The PerStationCatchupSchedules url generated is : \n", cacheUrl)
    cache = None
    self.lastRequestedUrl = cacheUrl
    try:
      cache = urllib.request.urlopen(cacheUrl).read()
    except urllib.error.HTTPError:
      print("HTTPError when trying to obtain PerStation Cache. URL:" + cacheUrl)
    return cache
  
  def _buildCacheUrl(self, requestedTimestamp, countPerStation, stations, top, popularityOrder = False):
    params = {}
    dateStr = datetime.datetime.utcfromtimestamp(requestedTimestamp).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    params['requestedTime'] = dateStr
    params['pivots'] = "Language|en"
    params['countPerStation'] = countPerStation
    params['$orderBy'] = "Popularity" if popularityOrder else ""
    params['$stations'] = ",".join(map(str, stations))
    params['$top'] = top
    params['$lang'] = "en-US"
    strUrlEncodedParams = urllib.parse.urlencode(params)
    return appgwUrl.replace("{type}", "client") + slot.upper() + "/discovery/v3/feeds/catchup/pivot-items?" + strUrlEncodedParams


class StationCacheRetriever:
  def __init__(self, appgwUrl, slot):
    self.appgwUrl = appgwUrl
    self.slot = slot
    
  def getCache(self, requestedTime, stationId, skip, top, popularityOrder = False):
    cacheUrl = _buildStationCatchupCacheUrl(requestedTime, stationId, skip, top, popularityOrder)
    print("The StationCatchupSchedules url generated is : \n", cacheUrl)
    cache = None
    self.lastRequestedUrl = cacheUrl
    try:
      cache = urllib.request.urlopen(cacheUrl).read()
    except urllib.error.HTTPError:
      print("HTTPError when trying to obtain Station Cache. URL:" + cacheUrl)
    return cache
  
  def _buildCacheUrl(self, requestedTimestamp, stationId, skip, top, popularityOrder = False):
    params = {}
    dateStr = datetime.datetime.utcfromtimestamp(requestedTimestamp).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    params['requestedTime'] = dateStr
    params['pivots'] = "Language|en"
    params['$skip'] = skip
    params['$orderBy'] = "Popularity" if popularityOrder else ""
    params['$stations'] = stationId
    params['$top'] = top
    params['$lang'] = "en-US"
    strUrlEncodedParams = urllib.parse.urlencode(params)
    return self.appgwUrl.replace("{type}", "client") + self.slot.upper() + "/discovery/v3/libraries/catchup/items?" + strUrlEncodedParams
#End of Functions to retrieve schedules