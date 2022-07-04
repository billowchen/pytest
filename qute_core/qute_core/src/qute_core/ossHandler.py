import oss2
from qute_core.logHandler import LogHandler
from qute_core.configparserHandler import ConfigparserHandler


class Oss2Handler(object):

    def __init__(self, config_file, key):
        self.config = ConfigparserHandler(config_file)
        self.key = self.config.get_data(key, 'key')
        self.secret = self.config.get_data(key, 'secret')
        self.endpoint = self.config.get_data(key, 'endpoint')
        self.token = self.config.get_data(key, 'token')
        self.logging = LogHandler().log()

        if self.token:
            self.auth = oss2.StsAuth(self.key, self.secret, self.token)
        else:
            self.auth = oss2.Auth(self.key, self.secret)

    def show_bucket(self):
        sevice = oss2.Service(self.auth, self.endpoint)
        bucket_name = [info.name for info in oss2.BucketIterator(sevice)]
        return bucket_name

    def get_bucketInfo(self, bucket_name):
        bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)
        bucket_info = bucket.get_bucket_info()
        return bucket_info

    def get_bucketStatus(self, bucket_name):
        bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)
        bucket_status = bucket.get_bucket_stat()
        return bucket_status

    def create_bucket(self, bucket_name, private=False):
        if not self.token:
            bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)
            if private:
                bucket.create_bucket(permission=oss2.models.BUCKET_ACL_PRIVATE)

            if bucket_name in self.show_bucket():
                self.logging.info('{}创建成功'.format(bucket_name))
            else:
                self.logging.info('{}创建失败'.format(bucket_name))
        else:
            self.logging.info('{}权限不够,不能创建'.format(self.key))

    def upload(self, bucket_name, file_name):
        bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)
        with open(oss2.to_unicode(file_name), 'rb') as f:
            bucket.put_object(file_name, f)
        if bucket.get_object_meta(file_name):
            self.logging.info('{}上传成功'.format(file_name))
        else:
            self.logging.error('{}上传失败'.format(file_name))

    def download(self, bucket_name, cloud_name):
        bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)
        bucket.get_object_to_file(cloud_name, cloud_name)

    def delete(self, bucket_name, cloud_name):
        bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)
        bucket.delete_object(cloud_name)
