import openpyxl
from ExcelOp import ExcelOp
import json

from PG import PgInfo

# 工作表绝对地址
workExcelPath = "/Users/lin/PycharmProjects/pythonProject/xuanwu/data/智慧100 数据字典整理110.xlsx"
# 提取出来的表与IDE接口及作者映射文件绝对地址
tableIdeAuthorPath = "/Users/lin/PycharmProjects/pythonProject/xuanwu/data/match_result.txt"
# 报表信息excel
reportAuthorExcelPath = "/Users/lin/PycharmProjects/pythonProject/xuanwu/data/报表任务及调度.xlsx"
# IDE实体及创建人映射文件绝对地址
tableAuthorPath = '/Users/lin/PycharmProjects/pythonProject/xuanwu/data/table_author.txt'


def pretty(d):
    return json.dumps(d, indent=4, ensure_ascii=False)


def get_data_from_excel():
    excel_op = ExcelOp(file=workExcelPath)
    result = excel_op.get_value()
    basic_data = {}
    for i in range(len(result)):
        if i == 0:
            continue
        else:
            basic_data[result[i][0]] = result[i]
    return basic_data


# 根据列表生成Excel
def list_build_excel(sheetName, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheetName
    result = make_excel_for_build_word()
    for each in result:
        ws.append(result[each])
    wb.save(path)


# 从报表整理文件中获取表与负责人对应关系
def get_report_author():
    excel_op = ExcelOp(file=reportAuthorExcelPath)
    # targeTable = excel_op.get_col_value(9)
    # scheduling_name = excel_op.get_col_value(1)
    # authorName = excel_op.get_col_value(7)
    table_author = {}
    # for i in range(len(targeTable)):
    #     tables = targeTable[i]
    #     if tables is not None:
    #         tables = tables.replace('\n', ',')
    #         tables = tables.replace('"', '')
    #         tables = tables.replace('public', '')
    #         tables = tables.replace('.', '')
    #         tables = tables.replace(' ', '')
    #         tables = tables.split(',')
    #         for table in tables:
    #             temp = [table, scheduling_name, authorName[i]]
    #             table_author[table] = temp

    all_data = excel_op.get_all_rows_value()
    for i in range(len(all_data)):
        rowList = all_data[i]
        for j in range(len(rowList)):
            remark = str(rowList[0]).strip()
            tableName = str(rowList[8]).strip()
            table_author[tableName] = remark
    table_author = str(table_author)
    table_author = table_author.replace("'", "\"")
    table_author = table_author.replace("\"public\".\"\"", "")
    print(table_author)
    return table_author


# 更新新的表数据进已有的exel
def get_and_update_excel():
    # 获取工作excel
    print("1.读取旧整理文档Excel")
    workExcel = get_data_from_excel()
    excel_tables = set(workExcel.keys())
    pg = PgInfo(database='tenant_1000061')
    # 查询表名及表行数
    print("2.查询数据库public模式下所有用户表的表名、表注释及表数据行数")
    # reltuples
    sql = '''SELECT
    relname,
	cast (
		obj_description (relfilenode, 'pg_class') as varchar
	) as comment,
	reltuples
FROM
    pg_class
    CLS LEFT JOIN pg_namespace N ON ( N.oid = CLS.relnamespace )
WHERE
    nspname NOT IN ( 'pg_catalog', 'information_schema' )
    AND relkind = 'r'
ORDER BY
    relname DESC'''
    countDict = pg.ExecQuery_And_Get_Return(sql)
    print("3.更新表基础信息(表名、表注释、数据行数)")
    table_basicInfo = {}
    for row in countDict:
        # 为了与原有的excel表格行一致，手动填充五个空白单元格
        count_annotation = [row[0], row[1], row[2], '', '', '', '', '']
        table_basicInfo[row[0]] = count_annotation
    datasource_tables = set(table_basicInfo.keys())
    # 获取交集
    inner_tables = datasource_tables & excel_tables
    # 获取差集
    extra_tables = datasource_tables - excel_tables

    # 更新旧表基础信息
    print("--------->3.1更新旧表基础信息")
    for table in inner_tables:
        old_detail = workExcel[table]
        # 如果原文档表注释为空则更新表注释
        if old_detail[1] is None or old_detail[1] == '':
            old_detail[1] = table_basicInfo[table][1]
        # 更新表行数(预估)
        old_detail[2] = table_basicInfo[table][2]

    excel_have_datasource_unHave = excel_tables - datasource_tables
    for table in excel_have_datasource_unHave:
        workExcel[table] = [table, '删除', '删除', '删除', '删除', '删除', '删除', '删除']

    # 只提取增量更新的表可以把这个注释打开
    # workExcel = {}
    # 插入新表信息
    print("--------->3.2插入新表基础信息")
    for table in extra_tables:
        workExcel[table] = table_basicInfo[table]
    return workExcel


# 对已有excel补充作者及IDE接口数据
def make_excel_for_build_word():
    # 读取IDE提取的表名+接口+更新人
    tableIdeAuthor = open(tableIdeAuthorPath, encoding="utf-8", mode='r+')
    match_result = eval(tableIdeAuthor.read())  # 读取的str转换为字典

    # 读取IDE实体+创建人文件
    tableAuthor = open(tableAuthorPath, encoding="utf-8", mode='r+')
    table_author_dict = eval(tableAuthor.read())  # 读取的str转换为字典

    # 获取工作excel
    workExcel = get_and_update_excel()

    # 1.从IDE接口中提取信息到excel
    print("4.读取IDE中提取的接口信息更新到excel(表名+接口+最后使用时间+使用人)")
    for rowData in match_result:
        if rowData in workExcel.keys():
            for items in match_result[rowData]:
                tableRow = workExcel[rowData]
                items = items.split(',')
                # 添加IDE领域接口信息
                tableRow.append(items[1])
                tableRow.append(items[2])
                tableRow.append(items[3])
                tableRow.append(items[4])
                if tableRow[3] is None or tableRow[3] == '':
                    tableRow[3] = items[4]
                    # print(tableRow)

    # 2.从报表整理中提取信息到excel
    print("5.读取报表整理信息更新到excel(表名+注释+负责人)")
    reportAuthor = get_report_author()
    for rowData in reportAuthor:
        if rowData in workExcel.keys():
            reportRow = reportAuthor[rowData]
            tableRow = workExcel[rowData]
            tableRow[3] = reportRow[1]
    # print(workExcel)

    # 3.从IDE实体+创建人文件中提取信息到excel
    print("6.读取IDE实体+创建人文件信息更新到excel(表名+注释+负责人)")
    for rowData in table_author_dict:
        if rowData in workExcel.keys():
            # 表名
            if workExcel[rowData][1] is None or workExcel[rowData][1] == '':
                workExcel[rowData][1] = table_author_dict[rowData][1]
            # 负责人
            if workExcel[rowData][3] is None or workExcel[rowData][3] == '':
                # print(table_author_dict[rowData])
                workExcel[rowData][3] = table_author_dict[rowData][0]
    return workExcel


if __name__ == '__main__':
    list_build_excel('数据字典整理', '/Users/lin/PycharmProjects/pythonProject/xuanwu/data/数据库111.xlsx')
    # get_report_author()
    # get_and_update_excel()
