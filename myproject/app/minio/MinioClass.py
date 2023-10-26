from minio import Minio
from minio.error import S3Error
from io import BytesIO
from base64 import b64encode, b64decode
import os


from minio import Minio

               # опциональный параметр, отвечающий за вкл/выкл защищенное TLS соединение



class MinioClass:
    def __init__(self):
        try:
            self.client = Minio(endpoint="127.0.0.1:9000",
                                access_key='minioadmin',
                                secret_key='minioadmin',
                                secure=False)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def addUser(self, buck_name: str):
        try:
            self.client.make_bucket(buck_name)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def removeUser(self, buck_name: str):
        try:
            self.client.remove_bucket(buck_name)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def addImage(self, buck_name: str, image_base64: str,object_name:str):
        try:
            image_data = b64decode(image_base64)
            image_stream = BytesIO(image_data)
            self.client.put_object(bucket_name=buck_name,
                                   object_name=object_name,
                                   data=image_stream,
                                   length=len(image_data))
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def getImage(self, buck_name: str, object_name :str):
        try:
            result = self.client.get_object(bucket_name=buck_name,
                                            object_name=(object_name))
            #print (b64encode(BytesIO(result.data).read()).decode())
            return b64encode(BytesIO(result.data).read()).decode()
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def removeImage(self, buck_name: str, object_name:str):
        try:
            self.client.remove_object(bucket_name=buck_name,
                                      object_name=object_name)
        except S3Error as e:
            print("minio error occurred: ", e)
        except Exception as e:
            print("unexpected error: ", e)

    def check_bucket_exists(self, bucket_name):
        info_bucket = self.client.bucket_exists(bucket_name)
        if (info_bucket):
            print(f'[{info_bucket}] Бакет "{bucket_name}" существует')
        else:
            print(f'[{info_bucket}] Бакет "{bucket_name}" не существует')