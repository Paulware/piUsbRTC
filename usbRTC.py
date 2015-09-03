import serial
import time
import datetime

class RTC ():
   def __init__ (self, comport): 
      self.portName = comport
   
      
   def findUsbDevice (self, response):
      ls = os.popen ( 'ls /dev/ttyUSB*').read()  
      lines = ls.split ( '\n')
      port = ''
      for line in lines:
         if port != '':
            break
         if line.strip() != '':
            portName = line.strip()
            try: 
               comPort = serial.Serial (portName, 57600, timeout = 0.01)
               startTime = time.time()
               while time.time() < startTime + 3:
                  line = comPort.readline () 
                  if line.strip() != '':
                     if line.strip() == expectedResponse:
                        print 'Found expected response on port: ' + port 
                        port = portName
                     break
               comPort.close()
            except Exception as inst:
               print 'Err: ' + str(inst)             
            if port == '':
               print 'Could not find device with response: ' + response
            else:               
               print 'Found device at port: ' + port 
            
      return port 
      
   # d is in format: 'MMM DD YYYY'
   # t is in format: 'HH:MM:SS'   
   def setRTCTime ( self, port, d, t):
      rtc = serial.Serial (port, 57600, timeout = 0.01)
      # read the response 
      startTime = time.time()
      while time.time() < startTime + 3:
         line = rtc.readline()
      rtc.write ( d + ' ' + t + '\r' )
      time.sleep (1)
      rtc.close()
      
   # str should be in the format: 'YYYY-MM-DD HH:MM:SS'      
   def setPiDate (self, str):   
      os.system ( 'date -s \'' + str + '\'' )
      print 'Executed: date -s \'' + str + '\''     
      
   def readRTCTime (self):
      rtc = serial.Serial (self.portName, 57600, timeout = 0.01)
      # read the response 
      startTime = time.time()
      while time.time() < startTime + 3:
         line = rtc.readline()
      rtc.write ( '?')
      startTime = time.time()
      currentTime = ''
      while time.time() < startTime + 3:
         line = rtc.readline()
         if line.strip() != '':
            currentTime = line.strip()
            break
      rtc.close()      
      t = None
      if currentTime == '':
         print 'Could not determine current time'
      else:   
         print 'Current Time: ' + currentTime         
         t = datetime.datetime.strptime ( currentTime, "%Y-%m-%d %H:%M:%S")
         
      return t
         
if __name__ == '__main__':
   port = findUsbDevice ('RTCR'):
   rtc = RTC(port)
   currentTime = str(rtc.readRTCTime())
   print 'Got a current time of: ' + currentTime

   # For pi, set its date/time based on rtc
   # rtc.setPiDate (line)