import boto3
import time
from botocore.exceptions import NoCredentialsError, ClientError

class S3Manager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, s3_path, file_name, region_name="ap-northeast-2", log_level='INFO'):
        """
        S3Manager 객체 초기화

        Parameters:
        - aws_access_key_id: str, AWS 접근 키
        - aws_secret_access_key: str, AWS 비밀 접근 키
        - aws_session_token: str, AWS 세션 토큰 (필요한 경우)
        - bucket_name: str, S3 버킷 이름
        - file_name: str, 파일 이름
        - region_name: str, AWS 리전 (기본값: ap-northeast-2)
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.s3_path = s3_path
        self.file_name = file_name+'.txt'
        parts = s3_path.split('/')

        # 두 번째 부분을 author로, 세 번째 부분을 id로 할당
        self.author = parts[1]
        self.id = parts[2]
        self.file_content = f"[{self.author}] [{self.id}] S3Manager 초기화 시작\n"
        self.log_level = log_level

    def print(self, file_content,log_level = 'INFO'):
        """
        S3에 파일 업로드

        Parameters:
        - file_content: str, 파일 내용

        Returns:
        - file_content str, 파일 내용
        """
        try:
            file_content = f"{time.strftime('%Y.%m.%d - %H:%M:%S')}[{log_level}] {file_content} \n"
            if self.log_level == log_level :
                self.file_content = self.file_content + file_content
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=f"{self.s3_path}{self.file_name}",
                    Body=self.file_content
                )
            print(file_content)
            return file_content
        except NoCredentialsError:
            msg = "AWS Credentials are not available."
            print(msg)
            return msg
        except ClientError as e:
            msg = f"An error occurred: {e}"
            print(msg)
            return msg
