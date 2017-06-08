import json
import zlib

class HubCache:
  #Take the cache in as HTTP request object
  def __init__(self, cache):
    decompressedData = zlib.decompress(cache.read(), 16+zlib.MAX_WBITS)
    strData = data.decode('utf-8')
    self.cache = json.loads(strData)
    
  def getSchedulesBatch():
    
    