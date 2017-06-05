import sys
import time
import datetime
import urllib.parse
from enum import Enum
appgwUrl = "https://ottapp-appgw-storage-a.environment.operator.tv3cloud.com/"
acceptedArgsKeys = ['--environment', '-env', '--channelMap', '-cm', '--help', '-help']
envOperatorDict = {"int":"mr", "dev":"mr", "funk":"mr", "pprod":"mr"}
channelMaps = []
slot = "s1"

def parseCmdArgs():
  sys.argv.pop(0) #remove the first argument from the list - it is usually the filename of the program being executed
  args = sys.argv
  
  if len(args) == 0:
    print("you need to provide at least channel map id to check against. Default environment is dev.")
    return 1
  if len(args)%2 != 0:
    print("args need to be passed in pairs")
    
  for argsPairIndex in range (0,int(len(args)/2)):
    argKey = args[argsPairIndex * 2]
    argValue = args[argsPairIndex * 2 + 1]
    
    if argKey not in acceptedArgsKeys:
      print("Invalid argument descriptor: ", argKey)
      return 1
      
    if argKey == acceptedArgsKeys[0] or argKey == acceptedArgsKeys[1]:
      #environment
      env = argValue
      if argValue not in envOperatorDict.keys():
        print("Specified environment is not recognized: " + env)
        return 1
      global appgwUrl
      appgwUrl = appgwUrl.replace("environment", str(env))
      appgwUrl = appgwUrl.replace("operator", envOperatorDict.get(env))
      print("appgw url set to: ", appgwUrl)
    elif argKey == acceptedArgsKeys[2] or argKey == acceptedArgsKeys[3]:
		  #channelMap
      global channelMaps
      channelMaps = argValue.split(",")
      print("channelmaps set to: ", channelMaps)
    elif argKey == acceptedArgsKeys[4] or argKey == acceptedArgsKeys[5]:
      #help
      return 1
  
  if len(channelMaps) <= 0:
    print("Channel map id needs to be specified.")
    return 1
	
#Functions to retrieve schedules
def getChannelMapHubCatchupSchedules(appgwUrl, timestamp, channelMapId, popularityOrder = False):
  cacheUrl = buildChannelMapHubCatchupCacheUrl(appgwUrl, timestamp, channelMapId, popularityOrder)
  print("The channel map hub catchup cache url generated is : \n", cacheUrl)

def buildChannelMapHubCatchupCacheUrl(appgwUrl, timestamp, channelMapId, popularityOrder = False):
  utcDateStr = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
  blobContainerName = slot.lower() + "-catchup-data-" + utcDateStr
  strOrderBy = "Popularity-" if popularityOrder else ""
  cacheFileName = "channelmap-hub-" + strOrderBy + channelMapId + ".gz"
  #format of the url: http://{appgwUrl}/catalogcache/{bloblContainerName}/channelmap-hub-[Popularity-]{channelMapId}.gz
  cacheUrl = appgwUrl + "catalogcache/" + blobContainerName + "/" + cacheFileName
  return cacheUrl

def getPerStationCatchupSchedules(appgwUrl, requestedTimestamp, countPerStation, stations, top, popularityOrder = False):
  cacheUrl = buildPerStationCatchupCacheUrl(appgwUrl, requestedTimestamp, countPerStation, stations, top, popularityOrder = False)
  print("The getPerStationCatchupSchedules url generated is : \n", cacheUrl)
  
def buildPerStationCatchupCacheUrl(appgwUrl, requestedTimestamp, countPerStation, stations, top, popularityOrder = False):
  params = {}
  
  dateStr = datetime.datetime.utcfromtimestamp(requestedTimestamp).strftime('%Y-%m-%dT%H:%M:%S.000Z')
  params['requestedTime'] = dateStr
  params['pivots'] = "Language|en"
  params['countPerStation'] = countPerStation
  params['$orderBy'] = "Popularity" if popularityOrder else ""
  params['$stations'] = stations
  params['$top'] = top
  params['$lang'] = "en-US"
  strUrlEncodedParams = urllib.parse.urlencode(params)
  
  return appgwUrl + slot.upper() + "/discovery/v3/feeds/catchup/pivot-items?" + strUrlEncodedParams
  
def getStationCatchupSchedules(requestedTime, stations, skip, top, popularityOrder = False):
  pass
#End of Functions to retrieve schedules



#MAIN PROGRAM	
#
#
#
#
#
#
#
#
if parseCmdArgs() == 1:
  quit()

nowTimeStamp = time.time()
getChannelMapHubCatchupSchedules(appgwUrl, nowTimeStamp, channelMaps[0])
getPerStationCatchupSchedules(appgwUrl, nowTimeStamp, 10, "2222", 10)