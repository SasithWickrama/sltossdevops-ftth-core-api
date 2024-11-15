import cx_Oracle



class DbConnection:

    def dbconnLunox(self):
        try:
            hostname = 'prxd1-scan.intranet.slt.com.lk'
            port = '1521'
            service = 'HADWH'
            user = 'LUNOX'
            password = 'slt#LUNox'

            dsn_tns = cx_Oracle.makedsn(hostname, port, service_name=service)
            conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
            return conn
        except Exception as e:
            print("Exception : %s" % e)
            return e

    def dbconnUat(self):
        try:
            hostname = '172.25.16.243'
            port = '1521'
            service = 'clty'
            user = 'OSSRPT'
            password = 'ossrpt123'

            dsn_tns = cx_Oracle.makedsn(hostname, port, service_name=service)
            conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
            return conn
        except Exception as e:
            print("Exception : %s" % e)
            return e

    def dbconnErp(self):
        try:
            hostname = '172.25.18.150'
            port = '1576'
            service = 'EBSDRG'
            user = 'OSS_USER'
            password = 'Oss678'

            dsn_tns = cx_Oracle.makedsn(hostname, port, service_name=service)
            conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
            return conn
        except Exception as e:
            print("Exception : %s" % e)
            return e