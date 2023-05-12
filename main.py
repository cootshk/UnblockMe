import flask as f#Flask, make_response, request
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests
import json
#--------------------------------------#
# "webstie" breaking things counter: 5 #
#--------------------------------------#

stats = {}
try:
    with open("stats.json", "r") as file:
        stats = json.load(file)
except:
    pass
app = f.Flask(__name__)
def get(website: str, headers:dict | None={}) -> str | bytes:
    ##get css file coming soon 
    output = requests.get(website, headers=headers)
    for filetype in [
        "html", 
        "htm",
        "css",
        "js",
        "json"
    ]:
        if website.removesuffix("/").endswith(filetype):
            return output.text
    return output.content if "." in website.removesuffix("/").split("/")[-1] else output.text #output as text if the website is a path, otherwise binary
    #return output.text if not website.removesuffix("/").endswith(".png") 
def post(website: str, headers:dict={}, data: dict={}) -> str | None:
    return requests.post(website,headers=headers,data=data).text
def format(output: str | bytes ,website: str) -> str:
    if not isinstance(output, str):
        return str(output)
    #redirect links to this site
    output = output.replace("'/",f"'/{website.split('/')[0]}/").replace('"/',f'"/{website.split("/")[0]}/').replace("https://","/").replace("http://","/") #if output.startswith("/") else output
    #print scripts
    soup = bs(output, "html.parser")
    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            script_url = urljoin(website, script.attrs.get("src"))
            #output = output.replace(url, script_url)
            print(script_url)
    return output

def isafile(website: str) -> bool:
    website = website.removesuffix("/")
    for type in [
        "js",
        "png",
        "jpeg",
        "jpg",
        "css",
        "webp",
        "html",
        "json",
        "svg"
    ]:
        if website.endswith(type):
            return True
    return False

#-----Homepage------
@app.route('/')
def index() -> f.Response:
    res = f.make_response()
    res.set_data(open("index.html").read())
    res.set_cookie('lastsite',"")
    return res
@app.route("/styles.css")
def indexstyles() -> str:
    return open("styles.css").read()
@app.route("/favicon.ico")
def icon() -> str:
    return open("favicon.ico","b").read()
@app.route("/apple-touch-icon-precomposed.png")
def androidsucks() -> str:
    return open("apple-touch-icon-precomposed.png","b").read()
@app.route("/button.js")
def buttonscript() -> str:
    return open("button.js").read()
@app.route("/stop")
def stop():
    print("Stopping!")
    import sys
    sys.exit(0)
    print("Stopped!")
    exit(0)

#-----Unblocker------
@app.route('/<path:website>', methods=['GET'])
def anyget(website: str):
    print("getting ",website)
    website = website.removeprefix("/")
    if not "." in website.split("/")[0] and (f.request.cookies.get('lastsite') == None or f.request.cookies.get('lastsite') == ""):
        res = f.make_response()
        print("unable to locate cookie 'lastsite': ",{f.request.cookies.get('lastsite')})
        res.status_code = 404
        return res
    if website == "":# or website == "/":
        return index() #no idea why this triggers
    elif website == "styles.css":# or website == "/styles.css":
        return indexstyles() #still no idea why this triggers
    if (#not "/" in website.removeprefix("/").removesuffix("/") or
        "." in website.split("/")[0].replace(".","",1)
       #) and (isafile(website)
        and not "www." in website.split("/")[0]
        and not "." in website.split("/")[0].replace(".","",2)):
        website = f"{f.request.cookies.get('lastsite')}/{website}"
        print(f"invalid path, correcting to {website}")
    if len(website.split("/")[0].split(".")) < 2:
        website = f"{f.request.cookies.get('lastsite')}/{website}"
        print(f"getting cookie for site {website}: added {f.request.cookies.get('lastsite')}")
        #if f.request.cookies.get("redirected") != None and f.request.cookies.get("redirected") != "False":
        #res = f.make_response()
        #res.set_cookie("redirected", "True")# Use string bc cant use bool
        #res.set_data(f.redirect(website))
        #res.status_code = 308
        print("redirecting to ",website)
        return f.redirect(website,308)
    if len(website.split("/")[0].split(".")) < 3:
        #output = get(f"https://www.{website}",headers=f.request.headers)
        print("adding www.")
        #res = f.make_response()
        #res.status_code = 308
        #res.set_data(f.redirect(f"www.{website}"))
        return f.redirect(f"{f.request.host_url.removesuffix('/')}/www.{website}",308)
    else:
        output = get(f"https://{website}")
    res = f.make_response()
    res.set_cookie("lastsite", website.split("/")[0])
    #res.set_cookie("redirected", "False")
    res.set_data(format(output,website))
    res.status_code = 200
    try:
        stats[str(website)] += 1
    except:
        stats[str(website)] = 1
    with open("stats.json", "w") as file:
        json.dump(stats,file)
    #    return res 
    #print("getting "+website)
    return res
@app.route('/<path:website>', methods=['POST'])
def anypost(website):
    website = website.removeprefix("/").removesuffix("/")
    if website == "":# or website == "/":
        return index() #no idea why this triggers
    #elif website == "styles.css":# or website == "/styles.css":
    #    return indexstyles() #still no idea why this triggers
    if  (#not "/" in website.removeprefix("/").removesuffix("/") or
        "." in f"{website}/".split("/")[0].replace(".","",1)
        ) and (isafile(website)
        and not "www." in website):
        website = f"{f.request.cookies.get('lastsite')}/{website}"
        print(f"invalid path, correcting to {website}")
    if len(f"{website}/".split("/")[0].split(".")) < 2:
        website = f"{f.request.cookies.get('lastsite')}/{website}"
        print(f"getting cookie for site {website}: added {f.request.cookies.get('lastsite')}")
        #if f.request.cookies.get("redirected") != None and f.request.cookies.get("redirected") != "False":
        print("redirecting to ",website)
        #print(f"getting cookie for site {website}: added {f.request.cookies.get('lastsite')}")
        return f.redirect(f"www.{website}",308)
    if len(website.split("/")[0].split(".")) < 3:
        output = post(f"https://www.{website}",headers=f.request.headers,data=f.request.form)
        print("adding www.")
    else:
        print("posting to ",website)
        output = post(f"https://{website}",headers=f.request.headers,data=f.request.form)
    res = f.make_response()
    res.set_cookie("lastsite", f"{website}/".split("/")[0] if f"{website}/".split("/")[0] != None else (f.request.cookies.get("lastsite") if f.request.cookies.get("lastsite") != None else "")) # type: ignore
    #res.set_cookie("redirected", "False")
    res.set_data(format(str(output),website))
    res.status_code = 200
    #    return res 
    #print("getting "+website)
    return res
@app.errorhandler(500)
def internalservererror(e):
    website = f.request.url
    print("Cookie list: ", f.request.cookies)
    print("Cookie: ",f.request.cookies.get('lastsite'))
    print(f"fixing {website.removeprefix(f.request.host_url)}\nInto {f.request.cookies.get('lastsite')}/{website.removeprefix(f.request.host_url)}")
    website = f"/{str(f.request.cookies.get('lastsite'))}/{website.removeprefix(f.request.host_url)}/"
    print(f"Final Redirect: ({f.request.host_url})/{website}")
    if f.request.form == None or f.request.form == {}: #or f.request.form == ImmutableMultiDict({}):
        print("getting webite")
        output = anyget(website)
    else:
        print(f.request.form)
        print(f.request.content_type)
        print("posting to website")
        output = anypost(website)
    print(output)
    return output
    #print(f.request.host_url)
@app.errorhandler(404)
def notfound404(e):
    return open("404.html").read()

print("Starting web server!")
app.run(host='0.0.0.0', port=81)

