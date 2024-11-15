import random
import re

import requests

import db

def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))

class Erp:
    def getDetails(self):
        result = {}
        data = []

        refid = specific_string(10)

        endpoint = 'http://erp.slt.com.lk:80/webservices/rest/con_stock_check_v2/stock_check_cp/'

        headers = {
            'Authorization': 'Basic Q09OX1BPUlQ6JGx0QEp1biE0XzIy', #username password get as token from postmen
            'Content-Type': 'application/xml'
        }

        try:
            data = """<?xml version = '1.0' encoding = 'UTF-8'?>
                    <NS1:STOCK_CHECK_CP_Input xmlns:NS1="http://xmlns.oracle.com/apps/inv/rest/epic_stock_check/stock_check">
                    <NS1:InputParameters>
                    <NS1:IN_CONTRACTOR_X>"""+self['contractor']+"""</NS1:IN_CONTRACTOR_X>
                    </NS1:InputParameters>
                    </NS1:STOCK_CHECK_CP_Input>"""

            response = requests.request("POST", endpoint,headers=headers,
                                        data=data)

            R = re.findall("<OUT_ONHAND_QTY_TBL_ITEM>(.*?)</OUT_ONHAND_QTY_TBL_ITEM>", str(response.content))

            conn = db.DbConnection.dbconnLunox(self="")

            for val in R:
                R1 = re.findall("<ORG_X>(.*?)</ORG_X>", str(val))
                R2 = re.findall("<SUBINVENTORY_X>(.*?)</SUBINVENTORY_X>", str(val))
                R3 = re.findall("<LOCATOR_X>(.*?)</LOCATOR_X>", str(val))
                R4 = re.findall("<CONTRACTOR_X>(.*?)</CONTRACTOR_X>", str(val))
                R5 = re.findall("<LOT_NUMBER_X>(.*?)</LOT_NUMBER_X>", str(val))
                R6 = re.findall("<DRUM_NO_X>(.*?)</DRUM_NO_X>", str(val))
                R7 = re.findall("<GRN_DATE_X>(.*?)</GRN_DATE_X>", str(val))
                R8 = re.findall("<DATE_TRANSFERED_TO_LOCATOR_X>(.*?)</DATE_TRANSFERED_TO_LOCATOR_X>", str(val))
                R9 = re.findall("<ITEM_CODE_X>(.*?)</ITEM_CODE_X>", str(val))
                R10 = re.findall("<ITEM_DESCRIPTION_X>(.*?)</ITEM_DESCRIPTION_X>", str(val))
                R11 = re.findall("<QUANTITY_X>(.*?)</QUANTITY_X>", str(val))
                R12 = re.findall("<TOTAL_COST_X>(.*?)</TOTAL_COST_X>", str(val))
                R13 = re.findall("<UOM_X>(.*?)</UOM_X>", str(val))
                R14 = re.findall("<PROJECT_NUMBER_X>(.*?)</PROJECT_NUMBER_X>", str(val))
                R15 = re.findall("<CONTRACTOR_CODE_X>(.*?)</CONTRACTOR_CODE_X>", str(val))

                if not len(R1):
                    org= ''
                else:
                    org =R1[0]

                if not len(R2):
                    sub= ''
                else:
                    sub =R2[0]

                if not len(R3):
                    loct= ''
                else:
                    loct =R3[0]

                if not len(R4):
                    con= ''
                else:
                    con =R4[0]

                if not len(R5):
                    lot= ''
                else:
                    lot =R5[0]

                if not len(R6):
                    drum= ''
                else:
                    drum =R6[0]

                if not len(R7):
                    grn= ''
                else:
                    grn =R7[0]

                if not len(R8):
                    trans= ''
                else:
                    trans =R8[0]

                if not len(R9):
                    item= ''
                else:
                    item =R9[0]

                if not len(R10):
                    des= ''
                else:
                    des =R10[0]

                if not len(R11):
                    qty= ''
                else:
                    qty =R11[0]

                if not len(R12):
                    cost= ''
                else:
                    cost =R12[0]

                if not len(R13):
                    uom= ''
                else:
                    uom =R13[0]

                if not len(R14):
                    proj= ''
                else:
                    proj =R14[0]

                if not len(R15):
                    code= ''
                else:
                    code =R15[0]

                sqldepot = "INSERT INTO DEPOT_ITEMS(DI_DEPOT_ID,DI_ITEM_CODE,DI_LOT_NO,DI_DRUM_NO,DI_TOT_QTY,DI_STATUS_DATE," \
                           "DI_ORG,DI_SUBINVENTORY,DI_LOCATOR,DI_DATE_TRANSFERED,DI_TOTAL_COST,DI_PROJECT_NUMBER) " \
                           "VALUES ( :R1,:R2,:R3,:R4,:R5,sysdate,:R6,:R7,:R8,:R9,:R10,:R11)"
                with conn.cursor() as cursor:
                    cursor.execute(sqldepot,[self['id'],item,lot,drum,qty,org,sub,loct,trans,cost,proj])
                    conn.commit()
                    #print(cursor.rowcount)

                sqlerp = "INSERT INTO ERP_DATA VALUES ( :R1,:R2,:R3,:R4,:R5,:R6,:R7,:R8,:R9,:R10,:R11,:R12,:R13,:R14,:R15,:refid,sysdate)"
                with conn.cursor() as cursor:
                    cursor.execute(sqlerp,[org,sub,loct,con,lot,drum,grn,trans,item,des,qty,cost,uom,proj,code,refid])
                    conn.commit()

                sqlerp = "INSERT INTO ERP_DATA VALUES ( :R1,:R2,:R3,:R4,:R5,:R6,:R7,:R8,:R9,:R10,:R11,:R12,:R13,:R14,:R15,:refid,sysdate)"
                with conn.cursor() as cursor:
                    cursor.execute(sqlerp,[org,sub,loct,con,lot,drum,grn,trans,item,des,qty,cost,uom,proj,code,refid])
                    conn.commit()

                try:
                    sqlitem = "INSERT INTO ITEMS (ITEM_CODE,ITEM_DISCRIPTION,ITEM_MESSUREMENT) VALUES ( :R1,:R2,:R3)"
                    with conn.cursor() as cursor:
                        cursor.execute(sqlitem,[item,des,uom])
                        conn.commit()
                        #print(cursor.rowcount)
                except Exception as error:
                        res =  error


            result['ERROR'] = False
            result['MSG'] = 'success'


        except Exception as error:
            result['ERROR'] = True
            result['MSG'] = str(error)
        return result