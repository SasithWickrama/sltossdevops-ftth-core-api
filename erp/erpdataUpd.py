import random
import re

import requests

import db

def specific_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    # define the condition for random string
    return ''.join((random.choice(sample_string)) for x in range(length))

class ErpUpd:
    def updateErp(self):

        try:
            result = {}

            connerp = db.DbConnection.dbconnErp(self="")
            conn = db.DbConnection.dbconnUat(self="")

            for item in self:

                pronum = item['projectNo']
                tsknum = item['taskNo']
                con = item['contractor']
                jobref = item['jobId']
                subproref = item['subJobId']
                lineno = item['lineNo']
                itemcode = item['itemCode']
                lotnum = item['lotNo']
                qty = item['usedQty']
                status = item['status']
                outmoveorder = item['outMoveOrder']
                outmsg = item['outMsg']
                depid = item['depotId']
                drumno = item['drumNo']
                totqty = item['totQty']
                usedqty = item['usedQty']
                actualqty = item['actualQty']
                reservedqty = item['reservedQty']
                unreservedqty = item['unreservedQty']
                accumulatedqty = item['accumulatedQty']
                updby = item['updateBy']

                sqlupderp = "INSERT INTO Apps.XXSLT_INVN40_CNP_STG (PROJECTNUM, TASKNUM, CONTRACTOR, JOBREF, SUBPROREF, LINENO, ITEMCODE, LOTNUM, QUANTITY, STATUS, OUTMOVEORDER, OUTMSG) VALUES ( :R1,:R2,:R3,:R4,:R5,:R6,:R7,:R8,:R9,:R10,:R11,:R12)"
                with connerp.cursor() as cursor:
                    cursor.execute(sqlupderp,[pronum,tsknum, con, jobref, subproref, lineno, itemcode, lotnum, qty, status, outmoveorder, outmsg])
                    connerp.commit()

                sqlupd = "INSERT INTO DEPOT_ITEMS_LOG (DIL_ID, DIL_JOB_ID, DIL_DEPOT_ID, DIL_ITEM_CODE, DIL_LOT_NO, DIL_DRUM_NO, DIL_TOT_QTY, DIL_USED_QTY, DIL_ACTUAL_QTY, DIL_RESERVED_QTY, DIL_UNRESERVED_QTY, DIL_ACCUMULATED_QTY, DIL_PROJECT_ID, DIL_UPDATE_DATE, DIL_UPDATE_BY) VALUES ( DEPOT_ITEMS_LOG_SEQ.nextval,:R2,:R3,:R4,:R5,:R6,:R7,:R8,:R9,:R10,:R11,:R12,:R13,sysdate,:R15)"
                with conn.cursor() as cursor:
                    cursor.execute(sqlupd,[jobref,depid,itemcode,lotnum,drumno,totqty,usedqty,actualqty,reservedqty,unreservedqty,accumulatedqty,pronum,updby])
                    conn.commit()

            result['ERROR'] = False
            result['MSG'] = 'success'

        except Exception as error:
            result['ERROR'] = True
            result['MSG'] = str(error)

        return result