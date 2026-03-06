from storages.backends.s3boto3 import S3Boto3Storage

class SafeS3Boto3Storage(S3Boto3Storage):
    def _save(self, name, content):
        try:
            # Перематываем файл в начало перед загрузкой
            if hasattr(content, "seek"):
                content.seek(0)
        except Exception as e:
            # Логируем, но не ломаем загрузку
            import logging
            logging.warning(f"Seek(0) failed before S3 upload: {e}")

        return super()._save(name, content)