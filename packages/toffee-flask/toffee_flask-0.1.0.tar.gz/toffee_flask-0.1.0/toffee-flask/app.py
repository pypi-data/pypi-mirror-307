from flask import Flask, request, make_response
import requests

app = Flask('TOFFEE by @PiratesTv')

cookie = "Edge-Cache-Cookie=URLPrefix=aHR0cHM6Ly9ibGRjbXByb2QtY2RuLnRvZmZlZWxpdmUuY29tLw:Expires=1691275195:KeyName=prod_linear:Signature=hL5AkJXog8pISnCVRioHqgwey4S4e7tHf9NXtLlOCPEk-u56FfzpHl9SNxxGagi6JqB2mTrqwbkQRx54PZq6BA"

headers={}

base_url = "https://bldcmprod-cdn.toffeelive.com"


@app.route("/")
def credit():
	
	
	return "Made With Toffee by @PiratesTv"


@app.route("/api/<string:channel_id>.m3u8")
def handle_api(channel_id):
    if channel_id.find("&")>=0:
        channel_id=channel_id.split("&")[0]
    print(channel_id)
    cat="sss"

 # Retrieve the m3u8 content
    link="https://raw.githubusercontent.com/Jeshan-akand/Toffee-Channels-Link-Headers/main/toffee_channel_data.json"
    request=requests.get(link).json()

    channels_data=request["channels"]
    for channel in channels_data:
        link=channel["link"]
        if link.find(channel_id)==-1:pass
        else:
            
            global headers
            headers=channel["headers"]
            cat=channel["category_name"]
            
            break


    if cat=="LIVE":
        
        l=link.replace("index.m3u8","master_1000.m3u8")
        m3u8_url=l
        global base_url
        base_url="https://mprod-cdn.toffeelive.com"
        
        
    		 
        lines=requests.get(l,headers=headers).text
    else:
        print("cat",cat)
        l=link.replace(channel_id+"/playlist.m3u8","slang/"+channel_id+"_576/"+channel_id+"_576.m3u8?bitrate=1000000&channel="+channel_id+"_576&gp_id=")
        lines=requests.get(l,headers=headers).text
    
       
        
      

    
    ara=lines.splitlines()
    a=ara

    if cat=="LIVE":
         for i,line in enumerate(a):
              
              if ".ts" in line:
                   a[i]=link.rsplit('/', 1)[0]+"/"+line

         m3u8_content = "\n".join(a)
         return m3u8_content


                   
              
         



    ts_urls = []
    
    for line in ara:
        
      
            
        if ".ts" in line:
            if cat=="LIVE":
                   
                            

                        

                    ts_urls.append(link.rsplit('/', 1)[0]+"/"+line)
				

            else:
                
                ts_urls.append(f"/ts?id={line}&base={base_url}")                
        else:
            
            ts_urls.append(line)
    m3u8_content = "\n".join(ts_urls)
    
    specified_text_prefix = "/file"
    specified_text_suffix = ".key"
    replacement_text = f"/key?id=/file.key" # Replace with your specified text
    start_index = m3u8_content.find(specified_text_prefix)
    end_index = m3u8_content.find(specified_text_suffix, start_index)
    specified_text = m3u8_content[start_index: end_index + len(specified_text_suffix)]
    result = m3u8_content.replace(specified_text, replacement_text)
    response = make_response(result)
    response.headers.get("content-type")
    return response





@app.route("/ts")
def handle_ts():

     
    # Handler for serving individual TS segments
    ts_id = request.args.get("id")
    base = request.args.get("base")
    



    if not ts_id :
        return "Please provide both 'id' and 'base' parameters in the URL query"

    # Construct the URL for the TS segment
    ts_url = base+ts_id
    print(ts_url)
    print("headers")
    print(headers)



    # Fetch the TS segment content
    response = requests.get(ts_url, headers=headers)
    myresponse = make_response(response.content)
    myresponse.headers.get("content-type") # Using this to get the content type directly from the headers
    return myresponse



@app.route("/key")
def handle_key():
	key_id = request.args.get("id")
	if not key_id:
		return "Please provide both 'id'parameters in the URL query"
	key_url = base_url + key_id
	print(key_url)

	response = requests.get(key_url, headers=headers)

	myresponse = make_response(response.content)
	myresponse.headers.get("content-type")
	return myresponse
@app.route("/set-cookie")
def set_cookie():
	new_cookie = request.args.get("cookie")
	if new_cookie:
		global cookie
		cookie = new_cookie	
		headers["cookie"] = new_cookie
		print(headers)
		return f"Cookie value set to: {new_cookie}"
	else:
 		return "Please provide a 'cookie' parameter in the URL query"

