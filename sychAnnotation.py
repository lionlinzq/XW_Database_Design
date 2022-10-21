import requests
import json
from PG import PgInfo

gHeaders = {}
url_prev = "http://101.200.205.231:8001"
header_raw = '''Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN
Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Access-Token
Access-Control-Allow-Methods: *
Access-Control-Allow-Origin: *
Content-Length: 187
Content-Type: application/json;charset=UTF-8
ctcode: 7
Host: 101.200.205.231:8001
idetoken: eyJhbGciOiJIUzI1NiJ9.eyJMb2dpblVzZXIiOnsiYXBwSWQiOiIxIiwidGVuYW50Q29kZSI6IjEwMDAwNjEiLCJwcm9kdWN0Q29kZSI6IjEwMDAwMDAwMDAwMDAwMDAwMCIsInByb2R1Y3RWZXJzaW9uQ29kZSI6IjEwMDAwMDAwMDAwMDAwMDA2MSIsImNsaWVudFR5cGVDb2RlIjpudWxsLCJ1c2VyQ29kZSI6IjE0OTQyMjI5MDU5MDU2NDc2MTYiLCJhY2NvdW50Q29kZSI6bnVsbCwidXNlcm5hbWUiOiLmnpflv5fmnYMiLCJ0b2tlbklkIjoiODUxMTA3NDktMjhmZi00ODQ0LWFmMDctNTI2ZDMyYTYwNjQyIiwiYXBwQ29kZXMiOm51bGwsImFwcENvZGUiOm51bGx9fQ.0-l4U_qGomTdYnRRT5FQi7mIMkWista-MyEs4-OP3Sc
metamodeltype: 1
pdcode: 100000000000000000
Proxy-Connection: keep-alive
pscode: 829609747450691584
pvcode: 100000000000000061
req_id: 23
tecode: 1000061
tenantname: %E6%99%BA%E6%85%A7100V6.1-base%E4%BA%A7%E5%93%81%E7%A7%9F%E6%88%B7
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) AppleWebKit/537.36 (KHTML, like Gecko) aPaaS-IDE-V3/3.4.0 Chrome/87.0.4280.141 Electron/11.4.3 Safari/537.36
usercode: 1494222905905647616
userinfoname: %E6%9E%97%E5%BF%97%E6%9D%83
username: linzhiquan
X-Requested-With: XMLHttpRequest'''


def get_headers(header_raw):
    """
    通过原生请求头获取请求头字典
    :param header_raw: {str} 浏览器请求头
    :return: {dict} headers
    """
    return dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


def get_cookies(cookie_raw):
    """
    通过原生cookie获取cookie字段
    :param cookie_raw: {str} 浏览器原始cookie
    :return: {dict} cookies
    """
    return dict(line.split("=", 1) for line in cookie_raw.split("; "))


def setHeaders(headers={}):
    global gHeaders
    gHeaders = headers


def doLogin(params={}):
    # headers = {
    #     # "accept": "application/json, text/plain, */*",
    #     # "accept-language": "zh-CN",
    #     # "access-control-allow-headers": "Origin, X-Requested-With, Content-Type, Accept, Access-Token",
    #     # "access-control-allow-methods": "*",
    #     # "access-control-allow-origin": "*",
    #     # "content-type": "application/json;charset=UTF-8",
    #     # "ctcode": "7",
    #     # "idetoken": "eyJhbGciOiJIUzI1NiJ9.eyJMb2dpblVzZXIiOnsiYXBwSWQiOiIxIiwidGVuYW50Q29kZSI6IjEwMDAwNjEiLCJwcm9kdWN0Q29kZSI6IjEwMDAwMDAwMDAwMDAwMDAwMCIsInByb2R1Y3RWZXJzaW9uQ29kZSI6IjEwMDAwMDAwMDAwMDAwMDA2MSIsImNsaWVudFR5cGVDb2RlIjpudWxsLCJ1c2VyQ29kZSI6IjE0NzYzNzQwMDY4NTU3NjYwMTYiLCJhY2NvdW50Q29kZSI6bnVsbCwidXNlcm5hbWUiOiLmnY7kv4rmtpsiLCJ0b2tlbklkIjoiOGY0MWQwNjgtOGJiNy00ZmMzLTg1YjUtMTM2ODYxOWY5MWI0IiwiYXBwQ29kZXMiOm51bGwsImFwcENvZGUiOm51bGx9fQ.eN6RHNRN49lgqBpenDh8Wae7-vd6KH524kn4K0pO2qA",
    #     # "metamodeltype": "1",
    #     # "pdcode": "100000000000000000",
    #     # "pscode": "829609747450691584",
    #     # "pvcode": "100000000000000061",
    #     # "req_id": "23",
    #     # "tecode": "1000061",
    #     # "tenantname": "%E6%99%BA%E6%85%A7100V6.1-base%E4%BA%A7%E5%93%81%E7%A7%9F%E6%88%B7",
    #     # "usercode": "1476374006855766016",
    #     # "userinfoname": "%E6%9D%8E%E4%BF%8A%E6%B6%9B",
    #     # "username": "lijuntao",
    #     # "x-requested-with": "XMLHttpRequest"
    # }
    headers = get_headers(header_raw)
    setHeaders(headers=headers)


def doPost(url, headers, rawData):
    resp = requests.post(url, json=rawData, headers=headers)
    respDict = json.loads(resp.text)
    respData = respDict['resp_data']
    return respData


def biz_pageList(rawData):
    url = url_prev + "/bizserv/biz/pageList"
    headers = gHeaders
    return doPost(url, headers, rawData)


def biz_getBizObject(rawData):
    url = url_prev + "/bizserv/biz/getBizObject"
    headers = gHeaders
    return doPost(url, headers, rawData)


def getTables():
    pg = PgInfo(database='tenant_1000061')
    sql = '''SELECT
        	relname
        FROM
        	pg_class C,
        	pg_namespace n
        WHERE
        	C.relnamespace = n.oid
        	AND nspname = 'public'
        	AND relkind = 'r'
        ORDER BY
        	relname DESC'''
    tableDict = pg.ExecQuery_And_Get_Return(sql)
    tableList = []
    for row in tableDict:
        tableList.append(row[0])
    return tableList


def main():
    doLogin()
    excludeTable = {'kx_shopgoods_sku_result', 'ka_kq_channelcustomers', 'kx_kq_product', 'pl_userinfo',
                    'kx_userinfo', 'kx_kq_visit_appeal', 'test_table', 'pl_orgstruct', 'pl_dictionary',
                    'kx_product_view'}
    rowData = {"objectname": "", "directorytypecode": "rootNode", "page": 1, "rows": 2000, "starttime": "",
               "centercode": ""}
    respData = biz_pageList(rowData)
    bizObjects = respData["data"]
    dic = {}
    pg = PgInfo(database='tenant_1000061')
    # sql = '''COMMENT ON TABLE test_table IS '测试111' '''
    # pg.ExecQuery(sql)
    extraList = set()
    x = 0
    for i in range(len(bizObjects)):
        bizObject = bizObjects[i]
        # rowData2 = {"objectcode": bizObject["objectcode"]}
        # bizObjectDetail = biz_getBizObject(rowData2)
        # tableName = str(bizObjects[i]["tablename"]).replace("\'", "\"")
        #
        # objectName = str(bizObjects[i]["objectname"]).replace("\'", "\"")
        # print(objectName)
        # dic[tableName] = objectName
        # properties = bizObjectDetail["properties"]
        # print("\n-----", str(i+1), "：", bizObjectDetail["tablename"], "=", bizObjectDetail["objectname"], "-----\n")
        # print("\n-------{}".format(i + 1))
        # if bizObject["tablename"] not in excludeTable and bizObject["datapattern"] == 1:
        # if bizObject["objectdescr"] is not None and bizObject["objectdescr"] != "":
        #     sql = "COMMENT ON TABLE {0} IS '{1}';".format(bizObject["tablename"], bizObject["objectdescr"])
        # else:
        # sql = "COMMENT ON TABLE {0} IS '{1}';".format(bizObject["tablename"], bizObject["objectname"])
        # print(sql)
        # x = x+1
        # pg.ExecQuery(sql)
        # for j in range(len(properties)):
        #     propertie = properties[j]
        #     # print(str(j+1), "：", properties["columnname"], "=", properties["propertyname"])
        #     print("COMMENT ON COLUMN {0}.{1} IS '{2}';".format(bizObjectDetail["tablename"], propertie["columnname"],
        #                                                        propertie["propertyname"]))
    # pg = PgInfo(database='tenant_1000061')
    # sql = '''COMMENT ON TABLE test_table IS '1asa' '''
    # pg.ExecQuery(sql)
    table_author = {}
    for i in range(len(bizObjects)):
        bizObject = bizObjects[i]
        tableName = bizObject['tablename']
        createAuthor = bizObject['createaccountname']
        tableAnnotation = bizObject['objectname']
        table_author[tableName] = [createAuthor, tableAnnotation]
        # rowData2 = {"objectcode": bizObject["objectcode"]}
        # bizObjectDetail = biz_getBizObject(rowData2)
        # tableName = str(bizObjects[i]["tablename"]).replace("\'", "\"")
        #
        # objectName = str(bizObjects[i]["objectname"]).replace("\'", "\"")
        # print(objectName)
        # dic[tableName] = objectName
        # properties = bizObjectDetail["properties"]
        # print("\n-----", str(i+1), "：", bizObjectDetail["tablename"], "=", bizObjectDetail["objectname"], "-----\n")
        # print("\n-------{}".format(i + 1))
        # if tableName in getTables():
        #     print("COMMENT ON TABLE {0} IS '{1}';".format(bizObjects[i]["tablename"], bizObjects[i]["objectname"]))
        # if tableName == 'kx_order_detail':
        #     for j in range(len(properties)):
        #         propertie = properties[j]
        #         # print(str(j+1), "：", properties["columnname"], "=", properties["propertyname"])
        #         sql = "COMMENT ON COLUMN {0}.{1} IS '{2}';".format(bizObjectDetail["tablename"], propertie["columnname"],
        #                                                            propertie["propertyname"])
        #         pg.ExecQuery(sql)

        # 查看表名称和表备注不一致的表名
        # if bizObject["tablename"] != bizObject["objectmark"]:
        #     extraList.add(bizObject["tablename"])

    print(x)
    file = open("/Users/lin/PycharmProjects/pythonProject/xuanwu/data/table_author.txt", mode='w+', encoding="utf-8")
    file.write(str(table_author))
    print(dic.values())


if __name__ == '__main__':
    main()
