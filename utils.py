import yaml
from munch import Munch
from PG import PgInfo

# 配置文件路径
configPath = "./config.yaml"


# 常用的方法
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


if __name__ == '__main__':
    get_PG_connect()
