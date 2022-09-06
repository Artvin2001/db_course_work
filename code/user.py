class User():
    def __init__(self, id, login, password, permission):
        self.id = id
        self.login = login
        self.password = password
        self.permission = permission

    def update_user(self, login, password, permission):
        self.login = login
        self.password = password
        self.permission = permission

    def set_login(self, login):
        self.login = login

    def set_password(self, password):
        self.password = password

    def set_permission(self, perm):
        self.permission = perm