
# 🚀 aiodoc: Async ByteIO Retrieval from Any Source 🪣

Welcome to **aiodoc**! 🎉 This library allows you to retrieve `BytesIO` objects from various sources asynchronously. Whether you're dealing with cloud storage, HTTP endpoints, FTP servers, or local files, `aiodoc` has got you covered! 🌐

## 🎯 Key Features

- **Async all the way** 🌟: Perform all file operations asynchronously to keep your application responsive.
- **Retrieve from any source** 🔌: Supports AWS S3, MinIO, Google Cloud Storage, HTTP, FTP, Redis, Memcached, and even local file systems.
- **Unified API** 🤹: A simple, easy-to-use interface for interacting with any storage system.

## 💼 Supported Providers

- 🐘 **AWS S3** via `aiobotocore` 🚀
- 🦒 **MinIO** using `minio-py` 🛠️
- ☁️ **Google Cloud Storage** with `google-cloud-storage` 🎩
- 🌐 **HTTP** with `httpx` 🌍
- 📂 **Local file system** with `aiofile` 🗂️
- 🧠 **Memcached** using `aiomemcached` 🧳
- 🔥 **Redis** via `aioredis` 🔥
- 🔗 **FTP** with `aioftp` 📡

## 🎒 How to Install

1. Clone the repo:
    ```bash
    git clone https://github.com/your-repo/aiodoc.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Done! 🎉 Now you're ready to use `aiodoc` for all your asynchronous file needs.

## 🛠️ Usage

### 🎩 Create Your Provider

You can set up and use different providers based on your needs.

#### 🐘 AWS S3 Example
```python
from aiobotocore.session import AioSession
from aiodoc import S3Provider

# Initialize S3 provider
session = AioSession()
s3_provider = S3Provider(session)

# Retrieve a file as a BytesIO object
file_bytes = await s3_provider.download("my-bucket", "my-file.txt")
```

#### ☁️ Google Cloud Storage Example
```python
from google.cloud import storage
from aiodoc import GCPProvider

# Initialize GCP provider
client = storage.Client()
gcp_provider = GCPProvider(client)

# Retrieve a file as a BytesIO object
file_bytes = await gcp_provider.download("my-bucket", "my-file.txt")
```

#### 📂 Local File System Example
```python
from aiodoc import FileProvider

# Initialize File provider
file_provider = FileProvider()

# Retrieve a file as a BytesIO object
file_bytes = await file_provider.download("bucket", "/path/to/file.txt")
```

#### 🔥 Redis Example
```python
from aioredis import Redis
from aiodoc import RedisProvider

# Initialize Redis provider
redis_client = await Redis.create()
redis_provider = RedisProvider(redis_client)

# Retrieve a file as a BytesIO object
file_bytes = await redis_provider.download("bucket", "file-key")
```

### 🛠️ Available Operations

- **Upload** 🆙: Upload a `BytesIO` object to any provider.
- **Download** ⬇️: Retrieve a `BytesIO` object from any provider.
- **List Files** 📜: List files (where supported).
- **Delete File** ❌: Delete a file (where supported).

## 🤝 Contributing

Feel free to submit issues or pull requests if you'd like to contribute!

## 📝 License

This project is licensed under the MIT License.
