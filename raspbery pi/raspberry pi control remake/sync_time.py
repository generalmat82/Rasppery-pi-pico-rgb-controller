# mainly taken from https://github.com/LutzEmbeddedTec/Pico_w_RTC/blob/main/RTC_WIFI.py
import network, machine, utime, usocket, ustruct
from time import sleep


# wintertime / Summerzeit
GMT_OFFSET = 0 * 1 # 3600 = 1 h (wintertime)
#GMT_OFFSET = 3600 * 2 # 3600 = 1 h (summertime)

# NTP-Host
NTP_HOST = 'time.nrc.ca'

# Funktion: get time from NTP Server
def getTimeNTP(rtc:machine.RTC):
    print("getting time from NTP server")
    NTP_DELTA = 2208988800
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    print("getting addr info")
    addr = usocket.getaddrinfo(NTP_HOST, 123)[0][-1]
    print("addr:"+str(addr))
    print("sending query?")
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    try:
        s.settimeout(2)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    ntp_time = ustruct.unpack("!I", msg[40:44])[0]
    return utime.gmtime(ntp_time - NTP_DELTA + GMT_OFFSET)

def sync_time(rtc:machine.RTC):
    #! (year, month, day, weekday, hours, minutes, seconds, subseconds)
    print("unsynced time:"+str(rtc.datetime()))
    print('Syncing time...')
    tm = getTimeNTP(rtc)
    rtc.datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    print("synced time:"+str(rtc.datetime()))


WEEKDAYS = {"shortForm" : ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), "longForm" : ("Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday")}
MONTHS = {"shortForm" : ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), "longForm" : ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")}
def strftime(template:str, time:tuple, timezone:str):
    """clone of time.strftime()
        curently only works with: a,d,b,Y,I,M,S,Z
    Args:
        template (str): string template
        time (tuple): time tuple
    """
    weekday = WEEKDAYS["shortForm"][time[3]]
    month = MONTHS["shortForm"][time[1]]
    formattedTime = template.format(a=weekday,d=time[2] ,b=month, Y=time[0], I=time[4], M=time[5],S=time[6], Z=timezone)
    return formattedTime

# mainly taken from https://github.com/LutzEmbeddedTec/Pico_w_RTC/blob/main/RTC_WIFI.py
import network, machine, utime, usocket, ustruct
from time import sleep


# wintertime / Summerzeit
GMT_OFFSET = 0 * 1 # 3600 = 1 h (wintertime)
#GMT_OFFSET = 3600 * 2 # 3600 = 1 h (summertime)

# NTP-Host
NTP_HOST = 'time.nrc.ca'

# Funktion: get time from NTP Server
def getTimeNTP(rtc:machine.RTC):
    print("getting time from NTP server")
    NTP_DELTA = 2208988800
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    print("getting addr info")
    addr = usocket.getaddrinfo(NTP_HOST, 123)[0][-1]
    print("addr:"+str(addr))
    print("sending query?")
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
    try:
        s.settimeout(2)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    ntp_time = ustruct.unpack("!I", msg[40:44])[0]
    return utime.gmtime(ntp_time - NTP_DELTA + GMT_OFFSET)

def sync_time(rtc:machine.RTC):
    #! (year, month, day, weekday, hours, minutes, seconds, subseconds)
    print("unsynced time:"+str(rtc.datetime()))
    print('Syncing time...')
    tm = getTimeNTP(rtc)
    rtc.datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    print("synced time:"+str(rtc.datetime()))


WEEKDAYS = {"shortForm" : ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), "longForm" : ("Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday")}
MONTHS = {"shortForm" : ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), "longForm" : ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")}
def strftime(template:str, time:tuple, timezone:str):
    """clone of time.strftime()
        curently only works with: a,d,b,Y,I,M,S,Z
    Args:
        template (str): string template
        time (tuple): time tuple
    """
    weekday = WEEKDAYS["shortForm"][time[3]]
    month = MONTHS["shortForm"][time[1]]
    formattedTime = template.format(a=weekday,d=time[2] ,b=month, Y=time[0], I=time[4], M=time[5],S=time[6], Z=timezone)
    return formattedTime

