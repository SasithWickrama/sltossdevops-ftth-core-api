import hashlib
import random

import zeep
from ldap3 import Server, Connection, ALL
import db
import const
from log import getLogger

logger = getLogger('authentication', 'logs/authentication')


def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))


def randOtp(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    return ''.join((random.choice(sample_string)) for x in range(length))


class Authenticate:

    def userAuth(self, remoteip):
        result = {}
        data = {}
        module = ""

        ref = specific_string(10)

        logger.info(ref + " " + remoteip + " " + self['conname'] + " " + self['uname'])

        if self['conname'] == 'SLT':
            ldap_user_name = self['uname'].strip() + '@intranet.slt.com.lk'
            ldap_user_pwd = self['passwd'].strip()

            ldap_server = f"ldap://intranet.slt.com.lk:389"

            server = Server(ldap_server, get_info=ALL)
            conn = Connection(server, user=ldap_user_name, password=ldap_user_pwd)

            if conn.bind():
                try:
                    conn = db.DbConnection.dbconnLunox(self="")
                    with conn.cursor() as c:
                        sql = "SELECT u.USERID,u.USERNAME,u.USERLOGINNAME,USERLASTLOG,ur.UROLE_NAME,u.USERTYPE, " \
                              "LISTAGG(um.MODULE_ID, '#') WITHIN GROUP (ORDER BY um.MODULE_ID) MODULE_ID" \
                              " FROM users u,user_roles ur, user_roles_module um " \
                              "where u.UROLE_ID = ur.UROLE_ID " \
                              "and u.UROLE_ID = um.UROLE_ID and u.USERLOGINNAME= :USERLOGINNAME " \
                              "GROUP BY u.USERID,u.USERNAME,u.USERLOGINNAME,USERLASTLOG,ur.UROLE_NAME,u.USERTYPE"

                        c.execute(sql, [self['uname']])
                        records = c.fetchone()

                        if records is not None:

                            data['USERID'] = records[0]
                            data['USERNAME'] = records[1]
                            data['USERLOGINNAME'] = records[2]
                            data['USERLASTLOG'] = str(records[3])
                            data['USERROLE'] = records[4]
                            data['USERMODULE'] = records[6]
                            data['USERWG'] = records[5]

                            result['ERROR'] = False
                            result['MSG'] = 'success'
                            result['DATA'] = data

                        else:
                            result['ERROR'] = True
                            result['MSG'] = 'You are not authorized to access this application'

                    with conn.cursor() as c:
                        sql = "update users set USERLASTLOG=sysdate where USERLOGINNAME= :USERLOGINNAME "
                        c.execute(sql, [self['uname']])
                        conn.commit()


                except Exception as error:
                    result['ERROR'] = True
                    result['MSG'] = str(error)


            else:
                result['ERROR'] = True
                result['MSG'] = conn.last_error

        else:
            try:
                conn = db.DbConnection.dbconnLunox(self="")
                with conn.cursor() as c:
                    sql = "SELECT u.USERID,u.USERNAME,u.USERLOGINNAME,USERLASTLOG,ur.UROLE_NAME,u.USERTYPE," \
                          "LISTAGG(um.MODULE_ID, '#') WITHIN GROUP (ORDER BY um.MODULE_ID) MODULE_ID" \
                          " FROM users u,user_roles ur, user_roles_module um " \
                          "where u.UROLE_ID = ur.UROLE_ID " \
                          "and u.UROLE_ID = um.UROLE_ID " \
                          "and u.USERLOGINNAME= :USERLOGINNAME  " \
                          "and u.USERPWDHASH = :USERPWDHASH and u.USERTYPE = :USERTYPE " \
                          "GROUP BY u.USERID,u.USERNAME,u.USERLOGINNAME,USERLASTLOG,ur.UROLE_NAME,u.USERTYPE"

                    otphash = hashlib.md5(self['passwd'].encode())
                    #print(self['passwd'])
                    #print(str(otphash.hexdigest()))
                    c.execute(sql, [self['uname'], str(otphash.hexdigest()), self['conname']])
                    records = c.fetchone()

                    if records is not None:

                        data['USERID'] = records[0]
                        data['USERNAME'] = records[1]
                        data['USERLOGINNAME'] = records[2]
                        data['USERLASTLOG'] = str(records[3])
                        data['USERROLE'] = records[4]
                        data['USERMODULE'] = records[6]
                        data['USERWG'] = records[5]

                        result['ERROR'] = False
                        result['MSG'] = 'success'
                        result['DATA'] = data

                        with conn.cursor() as c2:
                            sql2 = "update users set USERLASTLOG=sysdate,USERPWDHASH=:USERPWDHASH  where USERLOGINNAME= :USERLOGINNAME "
                            c2.execute(sql2, ['', self['uname']])
                            conn.commit()

                    else:
                        result['ERROR'] = True
                        result['MSG'] = 'OTP value already used or You are not authorized to access this application'

            except Exception as error:
                result['ERROR'] = True
                result['MSG'] = str(error)
        logger.info(ref + " " + remoteip + " " + str(result))
        return result

    def userOtp(self,remoteip):
        result = {}
        data = {}
        ref = specific_string(10)

        logger.info(ref + " " + remoteip + " " + self['username'])

        try:
            conn = db.DbConnection.dbconnLunox(self="")
            with conn.cursor() as c:

                sql = "select USERLOGINNAME,USERMOBILE from USERS where USERLOGINNAME =:USERLOGINNAME"
                c.execute(sql, [self['username']])
                records = c.fetchone()

                if records is not None:

                    otp = randOtp(8)
                    #print(otp)
                    otphash = hashlib.md5(otp.encode())
                    #print(otphash.hexdigest())

                    msg = "Your One-Time OTP is " + str(otp) + " for ."

                    client = zeep.Client(wsdl=const.wsdl)
                    data['smsref'] = client.service.smsdirectx(records[1], msg, 'OSS', const.smsuser,
                                                               const.smspwd)

                    try:
                        sql = "update USERS set USERPWDHASH=:USERPWDHASH where  USERMOBILE =:USERMOBILE"
                        with conn.cursor() as cursor:
                            cursor.execute(sql, [str(otphash.hexdigest()), records[1]])
                            conn.commit()

                    except Exception as error:
                        result['ERROR'] = True
                        result['MSG'] = str(error)

                    result['ERROR'] = False
                    result['MSG'] = 'success'

                else:
                    result['ERROR'] = True
                    result['MSG'] = 'User Name not Registered'

        except Exception as error:
            result['ERROR'] = True
            result['MSG'] = str(error)

        logger.info(ref + " " + remoteip + " " + str(result))
        return result
