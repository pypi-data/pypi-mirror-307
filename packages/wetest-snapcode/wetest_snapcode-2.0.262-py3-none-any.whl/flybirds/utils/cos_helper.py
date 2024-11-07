# -*- coding: utf-8 -*-
"""
file download
"""
import os
from urllib.parse import urlparse
from qcloud_cos import CosConfig, CosS3Client

COS_FILE_PREFIX = "cos:///"


class CosClient(object):
    def __init__(self):
        self.config = None
        if os.environ.get("COS_SECRET_ID"):
            self.secret_id = os.environ["COS_SECRET_ID"]
            self.secret_key = os.environ["COS_SECRET_KEY"]
            self.bucket = os.environ.get("COS_BUCKET", "/")
            if os.environ.get("COS_SERVER_ADDR"):
                # use local cos server
                server_addr = urlparse(os.environ["COS_SERVER_ADDR"])
                self.config = CosConfig(
                    Scheme=server_addr.scheme,
                    Domain=server_addr.netloc,
                    SecretId=self.secret_id,
                    SecretKey=self.secret_key,
                )
            elif os.environ.get("COS_REGION") is not None:
                # public tencent cos server
                self.region = os.environ["COS_REGION"]
                self.config = CosConfig(
                    Region=self.region,
                    SecretId=self.secret_id,
                    SecretKey=self.secret_key,
                )

        if self.config is not None:
            self.client = CosS3Client(self.config)

    def downloadFromCos(self, url, path):
        """
        cos file download
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket,
                Key=url,
            )
        except Exception as e:
            print(f"download from cos failed {e}")
            return None

        response["Body"].get_stream_to_file(path)

    def uploadToCos(self, path):
        """
        cos file download
        """
        try:
            # 本地路径 简单上传
            response = self.client.put_object_from_local_file(
                Bucket=self.bucket,
                LocalFilePath=path,
                Key=path,
            )
            response.values()
            print(response)
            return response["ETag"]
        except Exception as e:
            print(f"upload to cos failed {e}")
            return None


cos_client = CosClient()
