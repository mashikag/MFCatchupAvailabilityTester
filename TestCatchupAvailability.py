import sys
import playInfoRequester

appgwUrl = "https://ottapp-appgw-{type}-a.{environment}.{operator}.tv3cloud.com/"
reachClientUrl = "https://reachclient.{environment}.{operator}.tv3cloud.com/"
acceptedArgsKeys = ['--environment', '-env', '--channelMap', '-cm', '--slot', '-s', '--help', '-help']
envOperatorDict = {"int":"mr", "dev":"mr", "funk":"mr", "pprod":"mr"}
channelMaps = []
slot = "s1"
env = "dev"

stations = [1703911,1705992,1704240,1703535,1704647,2580743,2580745,2580740,2485189,2485054]

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
      global env
      env = argValue
      if argValue not in envOperatorDict.keys():
        print("Specified environment is not recognized: " + env)
        return 1
    elif argKey == acceptedArgsKeys[2] or argKey == acceptedArgsKeys[3]:
		  #channelMap
      global channelMaps
      channelMaps = argValue.split(",")
      print("channelmaps set to: ", channelMaps)
    elif argKey == acceptedArgsKeys[4] or argKey == acceptedArgsKeys[5]:
      #slot
      global slot
      slot = argValue
      print("slot set to: ", slot)
    elif argKey == acceptedArgsKeys[6] or argKey == acceptedArgsKeys[7]:
      #help
      return 1
	
def prepareAppgwUrl():
  global appgwUrl
  appgwUrl = appgwUrl.replace("{environment}", str(env))
  appgwUrl = appgwUrl.replace("{operator}", envOperatorDict.get(env))
  print("appgw url set to: ", appgwUrl)

def prepareReachClientUrl():
  global reachClientUrl
  reachClientUrl = reachClientUrl.replace("{environment}", str(env))
  reachClientUrl = reachClientUrl.replace("{operator}", envOperatorDict.get(env))
  print("reachClient url set to: ", reachClientUrl)

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
  sys.exit(1)

if len(channelMaps) <= 0:
  print("Channel map id needs to be specified.")
  sys.exit(1)
  
prepareAppgwUrl()
prepareReachClientUrl()

requester = playInfoRequester.PlayInfoRequester(reachClientUrl, appgwUrl, slot, channelMaps)
requester.start() 
input("Press any key to kill the program...")
requester.stop()
sys.exit(0)