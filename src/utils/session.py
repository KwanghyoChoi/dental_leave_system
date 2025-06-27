class Session:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.current_user = None
        return cls._instance
    
    def login(self, user_data):
        self.current_user = user_data
    
    def logout(self):
        self.current_user = None
    
    def is_logged_in(self):
        return self.current_user is not None
    
    def is_admin(self):
        return self.current_user and self.current_user.get('is_admin', False)
    
    def get_user_id(self):
        return self.current_user['id'] if self.current_user else None
    
    def get_user_name(self):
        return self.current_user['name'] if self.current_user else None