import requests
import yaml
from utils.logger import log

#HTTP请求封装类
class HttpRequest:
    def __init__(self):
        #读取env.yaml里的配置环境
        with open('./config/env.yaml','r',encoding='utf8') as f:
            self.env=yaml.safe_load(f)#安全地读取环境配置的文件
            self.base_url=self.env['base_url']
            self.timeout=self.env['timeout']
            self.headers=self.env['headers']

    def get(self,url_path:str,params=None): #params是请求参数，比如http地址后面带的id，可有可无
        """get请求，用来查询数据"""
        full_url=self.base_url+url_path
        try:
            log.info(f'发送GET请求：{full_url}，参数：{params}')
            response=requests.get(
                url=full_url,
                headers=self.headers,
                timeout=self.timeout,
                params=params,
            )
            try:
                data=response.json()
                log.info(f'GET响应：状态码={response.status_code},数据={data}')
            except ValueError:
                log.info(f'GET响应：状态码={response.status_code}，数据=空，说明访问一个不存在的ID')
            return response
        except Exception as e:
            log.error(f'GET请求失败：{str(e)}')
            raise #使隐藏的问题暴露，在测试的终端是暴露异常
    def post(self,url_path:str,json_data=None):#这里json_data是指以json形式的数据，可选
        """POST请求：用来创建数据（注册用户，创建购物车）"""
        full_url=self.base_url+url_path
        try:
            log.info(f'发送POST请求：{full_url}，数据：{json_data}')
            response=requests.post(
                url=full_url,
                json=json_data,
                headers=self.headers,
                timeout=self.timeout,
            )
            log.info(f'POST响应：状态码={response.status_code}，数据={response.json()}')
            return response
        except Exception as e:
            log.error(f'POST请求失败：{str(e)}')
            raise
    def put(self,url_path:str,json_data=None):
        """PUT请求：用于更新数据（修改商品价格）"""
        full_url=self.base_url+url_path
        try:
            log.info(f'发送PUT请求：{full_url}，数据：{json_data}')
            response=requests.put(
                url=full_url,
                json=json_data,
                headers=self.headers,
                timeout=self.timeout,
            )
            log.info(f'PUT响应：状态码={response.status_code}，数据={response.json()}')
            return response
        except Exception as e:
            log.error(f'PUT请求失败：{str(e)}')
            raise
    def delete(self,url_path:str):
        """DELETE请求，用来删除数据（删除商品）"""
        full_url=self.base_url+url_path
        try:
            log.info(f'发送DELETE请求：{full_url}')
            response=requests.delete(
                url=full_url,
                headers=self.headers,
                timeout=self.timeout,
            )
            #判断响应体是否为空，空则不解析json
            response_data=None
            if response.text.strip():
                try:
                    response_data=response.json()
                    log.info(f'DELETE响应：状态码={response.status_code},数据={response_data}')
                except ValueError as E:
                    log.warning(f'DELETE非空但json解析失败：{str(E)},原始数据：{response.text}')
                    response_data=response.text
            else:
                log.info(f'DELETE响应：状态码={response.status_code},数据=空')
            #给response对象新增一个属性，方便外部获取：response.parsed_data=response_data
            setattr(response,'parsed_data',response_data)
            return response
        except Exception as e:
            log.error(f'DELETE请求失败：{str(e)}')
            raise

#把这个类实例化，方便，这样之后就不用一个一个实例化，直接调用
http_request=HttpRequest()







