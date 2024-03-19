import motor


class TikTokMongoDb:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            'mongodb://192.168.196.85:27018,192.168.196.86:27018,192.168.196.87:27018/?replicaSet=tiktok')
        self.db = self.client['tiktok']
        self.following_lists = self.db['following_lists']
        self.following_relations = self.db['following_relations']
        self.tiktok_users = self.db['tiktok_users']
        self.tiktok_follow_list_candidates = self.db['tiktok_users_follow_no_lists_view']
        self.tiktok_follow_view = self.db['tiktok_users_follow_view']


TikTokDb = TikTokMongoDb()
