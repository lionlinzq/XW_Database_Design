import requests
import json
import re

import utils
from PG import PgInfo
from utils import get_config, get_PG_connect

gHeaders = {}
config = get_config()
ideUrl = config.ideUrl


def setHeaders(headers={}):
    global gHeaders
    gHeaders = headers


def doLogin(params={}):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN",
        "access-control-allow-headers": "Origin, X-Requested-With, Content-Type, Accept, Access-Token",
        "access-control-allow-methods": "*",
        "access-control-allow-origin": "*",
        "content-type": "application/json;charset=UTF-8",
        "ctcode": "7",
        "idetoken": "eyJhbGciOiJIUzI1NiJ9.eyJMb2dpblVzZXIiOnsiYXBwSWQiOiIxIiwidGVuYW50Q29kZSI6IjEwMDAwNjEiLCJwcm9kdWN0Q29kZSI6IjEwMDAwMDAwMDAwMDAwMDAwMCIsInByb2R1Y3RWZXJzaW9uQ29kZSI6IjEwMDAwMDAwMDAwMDAwMDA2MSIsImNsaWVudFR5cGVDb2RlIjpudWxsLCJ1c2VyQ29kZSI6IjE0NzYzNzQwMDY4NTU3NjYwMTYiLCJhY2NvdW50Q29kZSI6bnVsbCwidXNlcm5hbWUiOiLmnY7kv4rmtpsiLCJ0b2tlbklkIjoiOGY0MWQwNjgtOGJiNy00ZmMzLTg1YjUtMTM2ODYxOWY5MWI0IiwiYXBwQ29kZXMiOm51bGwsImFwcENvZGUiOm51bGx9fQ.eN6RHNRN49lgqBpenDh8Wae7-vd6KH524kn4K0pO2qA",
        "metamodeltype": "1",
        "pdcode": "100000000000000000",
        "pscode": "829609747450691584",
        "pvcode": "100000000000000061",
        "req_id": "23",
        "tecode": "1000061",
        "tenantname": "%E6%99%BA%E6%85%A7100V6.1-base%E4%BA%A7%E5%93%81%E7%A7%9F%E6%88%B7",
        "usercode": "1476374006855766016",
        "userinfoname": "%E6%9D%8E%E4%BF%8A%E6%B6%9B",
        "username": "lijuntao",
        "x-requested-with": "XMLHttpRequest"
    }
    setHeaders(headers=headers)


def doPost(url, headers, rawData):
    resp = requests.post(url, json=rawData, headers=headers)
    respDict = json.loads(resp.text)
    respData = respDict['resp_data']
    return respData


def pageModelLogicList(rawData):
    url = ideUrl + "/bizserv/bizmodel/pageModelLogicList"
    print(url)
    headers = gHeaders
    return doPost(url, headers, rawData)


def getModelLogic(rawData):
    url = ideUrl + "/bizserv/bizmodel/getModelLogic"
    headers = gHeaders
    return doPost(url, headers, rawData)


def getTables():
    pg = utils.get_PG_connect("tenant_1000061")
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
    # with open("/Users/lin/PycharmProjects/XW/tables/数据表倒序.txt", "r", encoding='UTF-8') as f:
    #     content = f.read()
    # tables = content.split("\n")
    # regex = "|".join(tables)
    # tables = [regex]
    tables = "|".join(tableList)
    print(tables)
    return tables


def main():
    doLogin()
    tables = getTables()
    print(tables)
    rowData = {"rows": 5000, "page": 1, "modelcode": "rootNode", "keys": "", "directorytypecode": "rootNode",
               "keywords": "", "centercode": "", "actioncategory": "", "actiontype": "", "updateopname": "",
               "updatetimestart": "", "updatetimeend": ""}
    respData = pageModelLogicList(rowData)
    funs = respData["data"]
    match_result = {}
    matchtableSet = set()
    for i in range(len(funs)):
        fun = funs[i]
        rowData2 = {"modellogiccode": fun["modellogiccode"]}
        modelLogic = getModelLogic(rowData2)
        try:
            flycode = modelLogic["operations"][0]["templateparams"]["flycode"]
        except:
            print("发生异常：modelLogic=", modelLogic)
            continue
        # for j in range(len(tables)):
        #     table = tables[j]
        it = re.finditer(tables, flycode, re.M | re.I)
        for match in it:
            matchTable = match.group()
            if matchTable not in matchtableSet:
                match_data = []
                matchtableSet.add(matchTable)
                match_data.append('''{},{},{},{},{}'''.format(matchTable, modelLogic['modellogiccode'],
                                                              modelLogic['modellogicname'],
                                                              str(fun['updatetime'])[0:10],
                                                              fun['updateaccountname']))
                match_result[matchTable] = match_data
        print(i)

    # print(type(match_result))
    file = open("/Users/lin/PycharmProjects/pythonProject/xuanwu/data/match_result.txt", mode='w+', encoding="utf-8")
    file.write(str(match_result))


if __name__ == '__main__':
    main()
    # getTables()
    # fr = open("/Users/lin/PycharmProjects/pythonProject/data/match_result.txt", encoding="utf-8", mode='r+')
    # dic = eval(fr.read())  # 读取的str转换为字典
    # print(dic)
    # print(json.dumps(dic, indent=1, ensure_ascii=False))
    # json = ast.literal_eval(fr.read())
    # print(type(json))
    # print(json.dumps(json,indent = 1,ensure_ascii=False))
