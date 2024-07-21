from minio import Minio
from minio.error import S3Error

# 创建 MinIO 客户端
client = Minio(
    "play.min.io",  # 替换为你的 MinIO 服务器地址
    access_key="YOUR-ACCESSKEYID",  # 替换为你的 Access Key
    secret_key="YOUR-SECRETACCESSKEY",  # 替换为你的 Secret Key
    secure=True  # 如果使用 HTTP，则设置为 False
)

# 创建一个 Bucket
bucket_name = "my-bucket"
try:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' created successfully.")
except S3Error as err:
    print(f"Error creating bucket: {err}")

# 上传文件到 Bucket
file_path = "path/to/your/file.txt"
object_name = "file.txt"
try:
    client.fput_object(bucket_name, object_name, file_path)
    print(f"File '{file_path}' uploaded successfully as '{object_name}'.")
except S3Error as err:
    print(f"Error uploading file: {err}")

# 下载文件从 Bucket
output_path = "path/to/save/file.txt"
try:
    client.fget_object(bucket_name, object_name, output_path)
    print(f"File '{object_name}' downloaded successfully to '{output_path}'.")
except S3Error as err:
    print(f"Error downloading file: {err}")

# 列出 Bucket 中的对象
try:
    objects = client.list_objects(bucket_name)
    print("Objects in bucket:")
    for obj in objects:
        print(obj.object_name)
except S3Error as err:
    print(f"Error listing objects: {err}")

# 删除文件从 Bucket
try:
    client.remove_object(bucket_name, object_name)
    print(f"File '{object_name}' deleted successfully.")
except S3Error as err:
    print(f"Error deleting file: {err}")

# 删除 Bucket
try:
    client.remove_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' deleted successfully.")
except S3Error as err:
    print(f"Error deleting bucket: {err}")
