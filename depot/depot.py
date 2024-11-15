import db
import const


class Depot:
    def depotList(self):
        result = {}
        data = []

        try:
            conn = db.DbConnection.dbconnLunox(self="")
            with conn.cursor() as c:

                sql = "select distinct DEPOT_ID,DEPOT_USER_NAME,DEPOT_ERP_REF from DEPOT " \
                      "where DEPOT_STATUS =: DEPOT_STATUS order by DEPOT_USER_NAME"

                c.execute(sql, ["ACTIVE"])

                for row in c:
                    data.append({"ID": row[0],
                                 "NAME": row[1],
                                 "ERPREF": row[2]})

            result['ERROR'] = False
            result['MSG'] = 'success'
            result['DATA'] = data

        except Exception as error:
            result['ERROR'] = True
            result['MSG'] = str(error)

        return result

    def depotDetails(self):

        result = {}
        data = {}

        try:
            conn = db.DbConnection.dbconnLunox(self="")
            with conn.cursor() as c:

                sql = "select distinct * from DEPOT " \
                      "where DEPOT_ID = :DEPOT_ID"

                c.execute(sql, [self['id']])
                records = c.fetchone()

                if records is not None:
                    data['ID'] = records[0]
                    data['CREATEDATE'] = str(records[1])
                    data['STATUS'] = records[2]
                    data['STATUSDATE'] = str(records[3])
                    data['USERNAME'] = records[4]
                    data['ERPREF'] = records[5]
                    data['ADDRESS'] = records[6]
                    data['REMARKS'] = records[7]
                    data['TYPE'] = records[8]

            result['ERROR'] = False
            result['MSG'] = 'success'
            result['DATA'] = data

        except Exception as error:
            result['ERROR'] = True
            result['MSG'] = str(error)

        return result

    def depotItemlist(self):
        result = {}
        data = []

        try:
            conn = db.DbConnection.dbconnLunox(self="")
            with conn.cursor() as c:

                sql = "select distinct aa.*,bb.* from DEPOT_ITEMS aa, ITEMS bb " \
                      "where aa.DI_ITEM_CODE= bb.ITEM_CODE and  aa.DI_DEPOT_ID = :DI_DEPOT_ID"


                c.execute(sql, [self['id']])

                for row in c:
                    data.append({"ID": row[0],
                                 "ITEMCODE": row[1],
                                 "ITEMDESC": row[11],
                                 "ITEMUNIT": row[12],
                                 "LOTNO": row[2],
                                 "DRUMNO": row[3],
                                 "TOTQTY": row[4],
                                 "RESERVEDQTY": row[5],
                                 "LASTUPDATE": row[6]}
                                )

            result['ERROR'] = False
            result['MSG'] = 'success'
            result['DATA'] = data

        except Exception as error:
            result['ERROR'] = True
            result['MSG'] = str(error)

        return result
