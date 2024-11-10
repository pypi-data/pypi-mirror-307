def db_sync_json_demo():
    return """
    {
      "task_name": "mysql用户信息同步",
      "nodes": "drn->dwn",
      "datasource": {
        "db1": {
          # 由于底层使用sqlachemy,链接串写法按照其官网来
          # 格式: dialect[+driver]://user:password@host/dbname[?key=value..];sqlite,mysql+pymysql, oracle+cx_oracle
          # 目前只试验了,sqlite, mysql, oracle
          "url": "mysql+pymysql://root:123456@localhost:4002/test1"
        },
        "db2": {
          "url": "mysql+pymysql://root:123456@localhost:4000/test2"
        }
      },
      # drn内置的数据读取节点,dwn内置的描述数据写节点
      "drn": {
        # db引用必须以_db结尾,这里描述是说引用上述datasource中的db1
        "from_db": "db1",
        "from_table":"users1",
        "incr_key": "updated_at",
        "incr_key_value": "1900-01-01",
        "page_size": 100000,
        # sql_template可选的，不配置默认按照from_table增量同步
        "sql_template":"select * from users1  limit {page_offset},{page_size} "
      },
      "dwn": {
        # db引用必须以_db结尾,这里描述是说引用上述datasource中的db2
        "to_db": "db2",
        "to_table":"users"
      }
    }    
    """


def command(args):
    print(db_sync_json_demo())
