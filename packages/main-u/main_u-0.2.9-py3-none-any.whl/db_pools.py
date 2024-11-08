import pymysql
from dbutils.pooled_db import PooledDB
from sshtunnel import SSHTunnelForwarder

class DatabaseConnectionPool:
    def __init__(self):
        self.pools = {}

    def add_connection_pool(self, name, host, port, user, password, database, maxconnections=5, ssh_host=None, ssh_port=None, ssh_user=None, ssh_password=None):
        if ssh_host and ssh_port and ssh_user and ssh_password:
            self.pools[name] = self._create_ssh_pooled_db(host, port, user, password, database, ssh_host, ssh_port, ssh_user, ssh_password, maxconnections)
        else:
            self.pools[name] = PooledDB(
                creator=pymysql,
                host=host,
                port=int(port),
                user=user,
                password=password,
                database=database,
                maxconnections=maxconnections,
                blocking=True
            )

    def _create_ssh_pooled_db(self, db_host, db_port, db_user, db_password, db_database, ssh_host, ssh_port, ssh_user, ssh_password, maxconnections=5):
        def create_ssh_tunnel():
            tunnel = SSHTunnelForwarder(
                (ssh_host, int(ssh_port)),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_host, int(db_port))
            )
            tunnel.start()
            return tunnel

        def get_pooled_db(tunnel):
            return PooledDB(
                creator=pymysql,
                host='127.0.0.1',
                port=tunnel.local_bind_port,
                user=db_user,
                password=db_password,
                database=db_database,
                maxconnections=maxconnections,
                blocking=True
            )

        tunnel = create_ssh_tunnel()
        return get_pooled_db(tunnel)

    def query(self, pool_name, sql):
        if pool_name not in self.pools:
            raise ValueError(f"No connection pool named '{pool_name}' exists.")
        conn = self.pools[pool_name].connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results