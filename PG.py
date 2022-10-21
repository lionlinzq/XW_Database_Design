import psycopg2
import yaml
from munch import Munch


def get_config():
    # 默认获取当前目录下的config
    configPath = "./config.yaml"
    with open(configPath, 'r', encoding='utf-8') as config_file:
        config = Munch(yaml.safe_load(config_file))
    print(config.database)
    return config


def get_PG_connect(database):
    config = get_config()
    databaseConfig = config.database
    print("databaseConfig:", databaseConfig)
    conn = PgInfo(database, host=databaseConfig.host, user=databaseConfig.user,
                  password=databaseConfig.password)
    return conn


class PgInfo:
    def __init__(self, database, user, password, host):
        self.database = database
        # self.user = "postgres"
        # self.password = "1xkrxt12pevzcol0"
        # self.host = "101.200.205.231"
        self.port = 5432
        self.user = user
        self.password = password
        self.host = host
        # self.port = port
        self.conn = psycopg2.connect(database=self.database, host=self.host, user=self.user, password=self.password,
                                     port=self.port)

    # 常用的方法
    def GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.database:
            raise (NameError, "没有设置数据库信息")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery_And_Get_Return(self, sql):
        """
        执行查询语句
        """
        if sql == 'close':
            self.conn.close()
        try:
            cursor = self.conn.cursor()
            # 执行语句
            cursor.execute(sql)
            resultList = cursor.fetchall()
            que = cursor.query
            # self.conn.commit()
            return resultList
        except psycopg2.Error as e:
            self.conn.rollback()
            print(e)

    def ExecQuery(self, sql):
        """
        执行查询语句
        """
        if sql == 'close':
            self.conn.close()
        try:
            cursor = self.conn.cursor()
            # 执行语句
            print("执行的语句为:", end='')
            print(sql)
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
        except psycopg2.Error as e:
            print(e)


if __name__ == '__main__':
    pg = get_PG_connect(database='tenant_1000061')
    # 查询表名及表行数
    sql = '''SELECT
    relname,
    reltuples
FROM
    pg_class
    CLS LEFT JOIN pg_namespace N ON ( N.oid = CLS.relnamespace )
WHERE
    nspname NOT IN ( 'pg_catalog', 'information_schema' )
    AND relkind = 'r'
ORDER BY
    reltuples DESC'''
    countDict = pg.ExecQuery_And_Get_Return(sql)
    tableCount = {}
    for row in countDict:
        tableCount[row[0]] = str(row[1])[:-2]
    print(tableCount)
