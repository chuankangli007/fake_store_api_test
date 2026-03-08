import pytest
import yaml
from utils.http_request import http_request
from utils.logger import log

with open('./config/test_data.yaml', 'r', encoding='utf-8') as f:
    test_data=yaml.safe_load(f)

class TestUsers:
    #------测试1：合法注册（正常场景）-------
    def test_register_user_valid(self,init_env):
     """测试点：用合法数据注册，验证注册成功"""
     register_data=test_data['user']['register_valid']
     response=http_request.post('/users',json_data=register_data)
     result=response.json()

     assert response.status_code==201,'注册失败'
     assert 'id' in result,'未返回用户ID'
     log.info(f'用户注册成功，ID：{result["id"]}')

     #--------测试2：非法注册（异常场景）--------
    @pytest.mark.xfail(
        reason='Fake Store API 未实现邮箱格式校验，非法邮箱注册仍返回201；真实项目应返回400',
        strict=True
    )
    def test_register_user_invalid(self,init_env):
        """测试点：邮箱格式错误，验证注册失败"""
        invalid_data=test_data['user']['register_invalid']
        log.info('以错误的邮箱格式进行创建')
        response=http_request.post('/users',json_data=invalid_data)
        result=response.json()

        try:
            assert response.status_code==400,f'预期：400，实际：{response.status_code}'
            assert 'email' in str(result.get('error','')),'错误提示未关联email字段'
            log.info('真实用例下，该用例执行成功')
        except AssertionError as e:
            log.warning(f'Fake Store API不符合真实业务规则,里面没有对邮箱格式不对的校验：{str(e)}')
            raise
        finally:
            log.info('创建邮箱格式错误的用例执行完成')
    #------------------测试3：合法登录（正常场景）-----------
    #因为Fake Store API没有记忆注册账号信息的功能，所以需要用官方给的账号登录
    def test_login_user_valid(self,init_env):
        """测试点：用官方给的账号，验证返回token"""
        login_data=test_data['user']['login_valid']
        response=http_request.post('/auth/login',json_data=login_data)
        result=response.json()

        assert response.status_code==201,'登录失败'
        assert 'token' in result,'未返回token'
        assert result['token']!='','token为空'
        log.info(f'用户登录成功，token：{result["token"][:20]}...')

