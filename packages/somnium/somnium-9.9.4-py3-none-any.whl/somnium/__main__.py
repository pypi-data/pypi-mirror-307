import re
import json
import time
import requests
from html_telegraph_poster import TelegraphPoster

"""
Function
"""
#Post To Telegraph
def PostTelegraph(title: str, html: str):
    post_client = TelegraphPoster(use_api=True)
    auth_name = "Somnium"
    post_client.create_api_token(auth_name)
    post_page = post_client.post(
        title=title,
        author=auth_name,
        author_url=f"https://pypi.org/project/somnium",
        text=html,
    )
    return post_page["url"]

#Custom Styles
def CustomStyles():
    return requests.get('https://raw.githubusercontent.com/Vauth/custom/main/styles.json').json()

#Get Header
def GetHeader():
    r1 = requests.get("https://dream.ai/create")
    jsfile = (re.findall(r"_app-(\w+)", r1.text))[0]
    r2 = requests.get(f"https://dream.ai/_next/static/chunks/pages/_app-{jsfile}.js")
    googlekey = (re.findall(r'"(AI\w+)"', r2.text))[0]
    
    headers = {
        "authority": "identitytoolkit.googleapis.com",
        "accept": "*/*",
        "accept-language": "ru,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://dream.ai",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "x-client-version": "Chrome/JsCore/9.1.2/FirebaseCore-web",
    }

    TOKEN = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signUp", headers=headers, params={"key": googlekey}, json={"returnSecureToken": True}, timeout=10).json()["idToken"]
    
    return {
        "authority": "paint.api.wombo.ai",
        "accept": "*/*",
        "accept-language": "ru,en;q=0.9",
        "authorization": f"bearer {TOKEN}",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://dream.ai",
        "referer": "https://dream.ai/",
        "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "YaBrowser";v="23"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.895 Yowser/2.5 Safari/537.36",
        "x-app-version": "WEB-2.0.0",
    }

"""
Class
"""
#Main class
class Somnium():
    """"Somnium class
    
    Somnium objects are responsible of Generating artworks & getting artstyles.
    
    Available options:
        - Styles(): --> list                 Get all art-styles list.
        - StylesGraph() --> url              Get all art-styles as UI.
        - Generate(prompt, style): --> url   Generate Artwork using prompt.
    Example:
        - Somnium.Generate('Girl', 2000) #Futurepunk V3
    """
    
    #Get All Styles
    @classmethod
    def Styles(cls):
        r = requests.get("https://paint.api.wombo.ai/api/styles")
        alls = {key:value['id'] for key, value in (CustomStyles()).items()}
        alls.update({style["name"]: style["id"] for style in r.json() if not style["is_premium"]})
        return alls

    #Get Styles UI As Telegraph
    @classmethod
    def StylesGraph(cls):
        html = ''
        for i, b in CustomStyles().items():
            html += f'<h2>{i}:</h2> <pre>{b["id"]}</pre><br/><img src="{b["image"]}">⁪⁬⁮⁮⁮⁮'
        for i in requests.get("https://paint.api.wombo.ai/api/styles").json():
            if i['is_premium'] == False:
                html += f'<h2>{i["name"]}:</h2> <pre>{i["id"]}</pre><br/><img src="{i["photo_url"]}">⁪⁬⁮⁮⁮⁮' 
        return PostTelegraph('List Of ArtStyles', html)

    #Generate Art
    @classmethod
    def Generate(cls, text: str, style: int):
        #Headers
        headers = GetHeader()
        
        #Custom Ids
        CustomIds = {value['id']:key for key, value in CustomStyles().items()}
        
        #Custom Ifs
        if int(style) in CustomIds.keys():
            textQ = (CustomStyles()[CustomIds[int(style)]]['prompt']).replace('{PROMPT}', text)
            styleQ = int(CustomStyles()[CustomIds[int(style)]]['style']) #Poster Art (Changable)
        else:
            textQ = text
            styleQ = style
        
        data = {
            "is_premium": False,
            "input_spec": {
                "prompt": textQ,
                "style": styleQ,
                "display_freq": 10
            }
        }
        
        gen_response = requests.post('https://paint.api.wombo.ai/api/v2/tasks', headers=headers, data=json.dumps(data))

        try:
            image_id = gen_response.json()["id"]
            for i in range(10):
                response = requests.get(f'https://paint.api.wombo.ai/api/v2/tasks/{image_id}', headers=headers)
                if response.json()['state'] == "failed":
                    return None
                    break
                time.sleep(3)
                try:
                    img = response.json()["result"]["final"]
                    return img
                    break
                except:
                    continue
        except Exception as e:
            return None
