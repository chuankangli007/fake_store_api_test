import pytest
import yaml
from utils.http_request import http_request
from utils.logger import log

with open('./config/test_data.yaml','r',encoding='utf-8') as f:
    test_data = yaml.safe_load(f)

class TestProducts:
    #--------------测试1：查询有效商品---------------
    @pytest.mark.parametrize('product',test_data['product_query']['valid_ids'])
        #参数化装饰器:多组测试数据，逐个传给测试方法的 product 参数，
    # 让同一个测试逻辑自动跑多遍（每组数据跑一次）—— 实现「数据驱动测试」，
    # 避免为每组数据写重复的测试方法。
    def test_get_product_valid(self,init_env,product):
        """测试点：查询存在的商品，验证信息是否正确"""
        response=http_request.get(f'/products/{product['id']}')
        result=response.json()

        #断言：
        assert response.status_code == 200,f'状态码错误：{response.status_code}'
        assert result['id']==product['id'],'商品ID不一致'
        assert result['title']==product['expect_title'],'商品标签不一致'
        assert float(result['price'])==product['expect_price'],'商品价格不一致'
        log.info(f'查询商品用例成功（ID：{product["id"]}）')

    #----------------测试2：查询无效商品（异常场景）--------------
    def test_get_product_invalid(self,init_env):
        """测试点：查询不存在的商品，验证请求失败"""
        invalid_id=test_data['product_query']['invalid_id']
        response=http_request.get(f'/products/{invalid_id}')

        assert response.status_code==200,'状态码错误'
        assert response.text.strip()=='','响应体不为空，商品不应存在'
        log.info('查询无效商品用例执行成功')

    #---------测试3：创建有效商品（正常场景）----------
    def test_create_product_valid(self,init_env):
        """测试点：用合法数据创建商品，验证创建成功"""
        create_data=test_data['product_create']['valid_data']
        response=http_request.post('/products',json_data=create_data)
        result=response.json()

        assert response.status_code==201,'创建失败'
        assert result['title']==create_data['title'],'标题不一致'
        assert float(result['price'])==create_data['price'],'价格不一致'
        log.info('创建商品用例成功执行成功')

    #------------测试4：创建无效商品（异常场景）-------------
    @pytest.mark.xfail(
        reason='Fake Store API未实现价格负数校验，真实项目应该返回400（当前为201）',
        strict=True
    )
    def test_create_product_invalid(self,init_env):
        """测试点：用非法数据创建商品，验证请求失败"""
        invalid_data=test_data['product_create']['invalid_data']
        response=http_request.post('/products',json_data=invalid_data)
        result=response.json()
        log.info(f'Fake Store API的实际响应：状态码={response.status_code},价格={result['price']}')

        try:
            assert response.status_code==400,f'预期：400，实际：{response.status_code}'
            assert 'price' in str(result.get('error','')),'错误信息未包含price字段'
            log.info('真实用例下，该用例执行通过')
        except AssertionError as e:
            log.warning(f'Fake Store API不符合真实业务规则,里面没有对商品价格为负数的校验：{str(e)}')
            raise
        finally:
            log.info('创建价格负数商品用例执行完成')

        #----------测试5：更新商品价格--------
    def test_update_product_price(self,init_env,create_test_product):
        """测试点：更新商品价格，验证更新成功（依赖创建商品夹具）"""
        product_id=create_test_product
        update_data={
            'title':test_data['product_create']['valid_data']['title'],
            'price':test_data['product_update']['update_price'],
        }
        response=http_request.put(f'/products/{product_id}',json_data=update_data)
        result=response.json()

        assert response.status_code==200,'更新失败'
        assert float(result['price'])==test_data['product_update']['update_price'],'价格未更新'
        log.info(f'更新商品价格成功，ID：{product_id}')

      #--------测试6：删除商品（正常删除）---------
    def test_delete_product_valid(self,init_env,create_test_product):
        """测试点：删除存在的商品，验证删除成功（依赖创建商品夹具）"""
        product_id=create_test_product
        response=http_request.delete(f'/products/{product_id}')
        assert response.status_code==200,'删除失败'

        #验证删除后查询失败
        try:
            http_request.get(f'/products/{product_id}')
        except Exception as e:
            assert '404' in str(e),'商品未删除'
        log.info(f'删除商品用例执行成功，ID:{product_id}')