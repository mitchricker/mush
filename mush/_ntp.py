import machine
import mush
net=mush._load_internal("_net")
NTP_EPOCH=2208988800
DEFAULT_SERVER="pool.ntp.org"
def time(server,timeout=2000):
    s=net["udp_connect"](server,123,timeout)
    try:
        packet=bytearray(48)
        packet[0]=0x1b
        s.send(packet)
        response=s.recv(48)
        if len(response)<48:
            raise OSError("invalid NTP response")
        seconds=(
            (response[40]<<24)|
            (response[41]<<16)|
            (response[42]<<8)|
            response[43]
        )
        return seconds-NTP_EPOCH
    finally:
        net["safe_close"](s)
def _datetime(timestamp):
    days=timestamp//86400
    seconds=timestamp%86400
    year=1970
    while True:
        leap=year%4==0 and (
            year%100!=0 or year%400==0
        )
        count=366 if leap else 365
        if days<count:
            break
        days-=count
        year+=1
    leap=year%4==0 and (
        year%100!=0 or year%400==0
    )
    months=(
        31,
        29 if leap else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    )
    month=1
    for count in months:
        if days<count:
            break
        days-=count
        month+=1
    return (
        year,
        month,
        days+1,
        seconds//3600,
        (seconds%3600)//60,
        seconds%60,
    )
def set_clock(timestamp):
    year,month,day,hour,minute,second=_datetime(timestamp)
    machine.RTC().datetime((
        year,
        month,
        day,
        0,
        hour,
        minute,
        second,
        0,
    ))
def sync(server):
    timestamp=time(server)
    set_clock(timestamp)
    return timestamp
