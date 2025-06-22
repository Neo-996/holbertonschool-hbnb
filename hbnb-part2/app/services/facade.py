def list_users(self):
    return self.user_repo.list_all()

def update_user(self, user_id, data):
    user = self.user_repo.get(user_id)
    if not user:
        return None
    user.update(data)
    return user
