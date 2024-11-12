from fastapi import HTTPException, UploadFile


class ImageMagic:
    def process_uploaded_file(
            image_file: UploadFile,
            file_name: str,
            upload_directory: str
    ) -> str:
        file_extension = image_file.filename.split(
            ".")[-1] in ("jpg", "jpeg", "png")
        if not file_extension:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only jpg, jpeg, and png are allowed.")

        original_path = f"{upload_directory}/{file_name}.{image_file.filename.split('.')[-1]}"

        with open(original_path, "wb") as file:
            file.write(image_file.file.read())

        return str(original_path)
