from flask import Flask, request
from flask_restful import Api, Resource

from erp.erpdata import Erp
from erp.erpdataUat import Erpuat
from erp.erpdataUpd import ErpUpd
from login.login import Authenticate
from depot.depot import Depot

app = Flask(__name__)
api = Api(app)


class login(Resource):
    def post(self):
        data = request.get_json()
        return Authenticate.userAuth(data,request.remote_addr)

class otp(Resource):
    def post(self):
        data = request.get_json()
        return Authenticate.userOtp(data,request.remote_addr)

class depotlist(Resource):
    def get(self):
        return Depot.depotList("")

class depot(Resource):
    def get(self):
        data = request.get_json()
        return Depot.depotDetails(data)

class depotitemlist(Resource):
    def get(self):
        data = request.get_json()
        return Depot.depotItemlist(data)

class erpget(Resource):
    def post(self):
        data = request.get_json()
        return Erp.getDetails(data)

class erpgetuat(Resource):
    def post(self):
        data = request.get_json()
        return Erpuat.getDetails(data)

class erpupdate(Resource):
    def get(self):
        data = request.get_json()
        return Depot.depotDetails(data)

class erpupd(Resource):
    def post(self):
        data = request.get_json()
        return ErpUpd.updateErp(data)

#login
api.add_resource(login, '/ftthcore/login/')

#OTP
api.add_resource(otp, '/ftthcore/otp/')

#Depot
api.add_resource(depotlist, '/ftthcore/depotlist/')

api.add_resource(depot, '/ftthcore/depot/')

api.add_resource(depotitemlist, '/ftthcore/depotitemlist/')

#ERP
api.add_resource(erpget, '/ftthcore/erpget/')

api.add_resource(erpgetuat, '/ftthcore/erpgetuat/')

api.add_resource(erpupdate, '/ftthcore/erpupdate/')

#back update erp table with material summary
api.add_resource(erpupd, '/ftthcore/erpupd/')

if __name__ == '__main__':
    app.run(debug=True, port=7650)