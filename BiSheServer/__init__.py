import pymysql
import mimetypes

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)
pymysql.install_as_MySQLdb()