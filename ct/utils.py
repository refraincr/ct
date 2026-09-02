from PIL import Image,ImageOps
import io
from ct.extensions import r2_client,BUCKET_NAME,PUBLIC_DOMAIN

def image_process_and_upload(raw_bytes,content_type,filename):
    img = Image.open(io.BytesIO(raw_bytes))
    process_img = ImageOps.fit(img,(80,80),method=Image.Resampling.LANCZOS)

    # 读进内存
    image_format = content_type.rsplit('/',1)[-1] or 'jpeg'
    buf = io.BytesIO()
    process_img.save(buf,format=image_format, quality=90)
    buf.seek(0)

    process_filename = '/80x80/'.join(filename.split('/',1))
    r2_client.upload_fileobj(
        buf,
        BUCKET_NAME,
        process_filename,
        ExtraArgs={
            'ContentType': content_type or 'image/jpeg'
        }
    )
    return f'{PUBLIC_DOMAIN}/{process_filename}'

