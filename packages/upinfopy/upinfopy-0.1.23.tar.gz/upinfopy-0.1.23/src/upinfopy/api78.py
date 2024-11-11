import json
import requests
import sys
import os


class Api78:
    def __init__(self, base_url):
        self.base_url = base_url

    async def send_back(self, endpoint, params,backtype="json"):
        url = f"{self.base_url}/{endpoint}"
        back = None
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查响应状态码
            res= response.json()  # 返回JSON格式的数据
            if(res["res"]!=0):
                print(f"{url} 请求失败 : {res['errmsg']}")
                return    
                  
            if(backtype=="json"):
                try:
                    back = json.loads(res["back"])
                except json.JSONDecodeError as json_err:
                    #return {"error": f"JSON decode error: {json_err}"}
                    back=res["back"]
           
            else:
                back=res["back"]
            return back
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"error": f"An error occurred: {err}"}

    def send_request(self, endpoint, params):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查响应状态码
            return response.json()  # 返回JSON格式的数据
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"error": f"An error occurred: {err}"}
        
    def send(self, endpoint, params):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查响应状态码
            return response.text  # 返回str格式的数据
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"error": f"An error occurred: {err}"}

# 示例使用
if __name__ == "__main__":
    # 将包目录添加到模块搜索路径中
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from upinfo import UpInfo
    up= UpInfo()
    up.sid="GUEST888-8888-8888-8888-GUEST88GUEST"
    up.uname="guest"
    UpInfo.setMaster(up)

    up.set_par("gameid", 42)
    sendtext=up.to_url_encode()
    
    client = Api78("http://test.778878.net")
    params = sendtext
    result = client.send_request("apitest/testmenu/testtb/get", params)
    print(result)
        