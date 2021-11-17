import network
import ntptime,time
from machine import Timer, Pin, SoftSPI
import machine
import max7219_8digit


WLAN_SSID = ""
WLAN_PASS = ""

time.sleep(1) 
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
		wlan.active(True)
		wlan.connect(WLAN_SSID, WLAN_PASS)
		time.sleep(1) 
		while not wlan.isconnected():
		    machine.idle()

# ntptest = ntptime.settime()
#  while ntptest == None:

time.sleep(1) 
try:
    # update system time from NTP server
    ntptime.settime()
    print("NTP server query successful.")
    print("System time updated:", utime.localtime())
    update_time = utime.ticks_ms()
except:
    print("NTP server query failed.")

time.sleep(1) 

spi =SoftSPI(baudrate=1000000,polarity=1,phase=0,sck=Pin(18),mosi=Pin(23),miso=Pin(19))
ss = Pin(5, Pin.OUT)
display = max7219_8digit.Display(spi, ss)

def tick(timer):
		ttime = (time.time() - time.mktime(time.localtime()[:3]+ (0,0,0,0,0)) ) * 7
		(lh, lm) = time.localtime(ttime+10800)[3:5]
		(rh, rm) = time.localtime(ttime+54000)[3:5]
		display.tarkov_to_buffer("{0:02d}{1:02d}{2:02d}{3:02d}".format(lh,lm,rh,rm))
		display.display()

tim1 = Timer(1)
tim1.init(period=2000, mode=Timer.PERIODIC, callback=tick)
time.sleep(10)