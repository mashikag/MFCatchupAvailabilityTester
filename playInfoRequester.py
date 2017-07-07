import urllib.request
import threading 
import time
import CachesRetriever
import CachesStore

class PlayInfoRequester:

  def __init__(self, reachClientUrl, appgwUrl, slot, channelMaps):
    self._appgwUrl = appgwUrl
    self._reachClientUrl = reachClientUrl
    self._slot = slot
    self._channelMaps = channelMaps
    self._stop = False
    self.requesterThread = threading.Thread(target=self._requester)
    
  def start(self):
    self.requesterThread.start()
    
  def stop(self):
    self._stop = True
    
  def _requester(self):
    nowTimeStamp = time.time()
    hubCacheRetriever = CachesRetriever.HubCacheRetriever(self._appgwUrl, self._slot)
    cacheStrData = hubCacheRetriever.getCache(nowTimeStamp, self._channelMaps[0])
    hubCache = CachesStore.HubCache(cacheStrData)
    print(hubCache.toString())
    
    while not self._stop: 
      print("Requester running")
      currentCacheInterval = hubCache.getCurrentCacheInterval()
      for catchupSchedule in currentCacheInterval.getSchedules():
        self.requestPlayInfo(catchupSchedule.getPlayInfoUri())
      time.sleep(20)
      
    print("Exiting the requester...")
      
  def requestPlayInfo(self, relativePlayInfoUri):
    clientAppgwUrl = self._appgwUrl.replace("{type}", "client")
    playInfoUrl = clientAppgwUrl + self._slot.upper() + relativePlayInfoUri
    try:
      playinfo = urllib.request.urlopen(playInfoUrl)
      print(playinfo)
    except urllib.error.HTTPError:
      print ("HTTPError when trying to obtain playinfo: " + playInfoUrl)