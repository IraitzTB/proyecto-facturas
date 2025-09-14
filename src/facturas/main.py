import os
import s3fs
import json
from doctr.models import ocr_predictor

def store_json(json, userid):
    """
    Guarda el resultado en una collección de mongodb
    """
    raise NotImplementedError

def parse_invoice(file):
    """
    Dada una factura extrae el contenido.
    """
    model = ocr_predictor("db_resnet50", "crnn_vgg16_bn", pretrained=True)
    result = model(file)
    json_output = result.export()
    return result, json_output

def check_folder(userid: str):
    """
    Verifica la carpeta de usuario o la crea
    """
    # Create or check folder in minio
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': os.environ["MINIO_ENDPOINT"]},
        key=os.environ["MINIO_KEY"],
        secret=os.environ["MINIO_SECRET"],
        use_ssl=False  # Set to True if MinIO is set up with SSL
    )
    fs.mkdir(f'invoices/{userid}')

def save_invoice_for_user(file, userid: str) -> str:
    """
    Guarda la factura del usuario
    """
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': os.environ["MINIO_ENDPOINT"]},
        key=os.environ["MINIO_KEY"],
        secret=os.environ["MINIO_SECRET"],
        use_ssl=False  # Set to True if MinIO is set up with SSL
    )

    filepath = os.path.join(f'invoices/{userid}', file.name)
    with fs.open(filepath, "wb") as f:
        f.write(file.getvalue())

    return filepath
