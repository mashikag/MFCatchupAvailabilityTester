import datetime
import urllib.parse

#Functions to retrieve schedules
def getChannelMapHubCatchupSchedules(appgwUrl, slot, timestamp, channelMapId, popularityOrder = False):
  cacheUrl = _buildChannelMapHubCatchupCacheUrl(appgwUrl, slot, timestamp, channelMapId, popularityOrder)
  print("The channel map hub catchup cache url generated is : \n", cacheUrl)

def _buildChannelMapHubCatchupCacheUrl(appgwUrl, slot, timestamp, channelMapId, popularityOrder = False):
  utcDateStr = datetime.datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
  blobContainerName = str(slot).lower() + "-catchup-data-" + utcDateStr
  strOrderBy = "Popularity-" if popularityOrder else ""
  cacheFileName = "channelmap-hub-" + strOrderBy + channelMapId + ".gz"
  #format of the url: http://{appgwUrl}/catalogcache/{bloblContainerName}/channelmap-hub-[Popularity-]{channelMapId}.gz
  cacheUrl = appgwUrl.replace("{type}", "client") + "catalogcache/" + blobContainerName + "/" + cacheFileName
  return cacheUrl

def getPerStationCatchupSchedules(appgwUrl, slot, requestedTimestamp, countPerStation, stations, top, popularityOrder = False):
  cacheUrl = _buildPerStationCatchupCacheUrl(appgwUrl, slot, requestedTimestamp, countPerStation, stations, top, popularityOrder)
  print("The PerStationCatchupSchedules url generated is : \n", cacheUrl)
  
def _buildPerStationCatchupCacheUrl(appgwUrl, slot, requestedTimestamp, countPerStation, stations, top, popularityOrder = False):
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
  
def getStationCatchupSchedules(appgwUrl, slot, requestedTime, stationId, skip, top, popularityOrder = False):
  cacheUrl = _buildStationCatchupCacheUrl(appgwUrl, slot, requestedTime, stationId, skip, top, popularityOrder)
  print("The StationCatchupSchedules url generated is : \n", cacheUrl)
  
def _buildStationCatchupCacheUrl(appgwUrl, slot, requestedTimestamp, stationId, skip, top, popularityOrder = False):
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
  return appgwUrl.replace("{type}", "client") + slot.upper() + "/discovery/v3/libraries/catchup/items?" + strUrlEncodedParams
#End of Functions to retrieve schedules