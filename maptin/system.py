from .data.users import User
from .utills.http import success, fail
from flask import request


class System:

    def main(self, req: request, action:str):

        if req.method == 'GET':
            if action == 'getUsers':
                return self.getUserInfo()
            return fail('actions not found')

        if req.method == 'PUT':
            if action == 'updateUserPassword':
                return self.userResetPassword(request.headers.get('userId'))
            return fail(f'action {action} not found')


    def getUserInfo(self):
        users = User().getAll()

        for u in users:
            u['joined'] = u['joined'].strftime("%d/%m/%Y")

        return success({'users': users})

    def userResetPassword(self, usrId: int):
        newPw = User().updatePassword(usrId)
        return success({'password': newPw})

