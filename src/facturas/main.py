import os
import s3fs
from llama_cloud_services import LlamaExtract, SourceText
# from doctr.models import ocr_predictor


def store_json(json, userid):
    """
    Guarda el resultado en una collección de mongodb
    """
    raise NotImplementedError


def parse_invoice(file, file_name:str):
    """
    Dada una factura extrae el contenido.
    """
    # Instanciamos el agente creado en Llama Cloud
    llama_extract = LlamaExtract()
    agent = llama_extract.get_agent(name=os.environ["LLAMA_CLOUD_AGENTs"])

    source_text = SourceText(file=file, filename=file_name)
    result = agent.extract(source_text)

    return result


def check_folder(userid: str):
    """
    Verifica la carpeta de usuario o la crea
    """
    # Create or check folder in minio
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.environ["MINIO_ENDPOINT"]},
        key=os.environ["MINIO_KEY"],
        secret=os.environ["MINIO_SECRET"],
        use_ssl=False,  # Set to True if MinIO is set up with SSL
    )
    fs.mkdir(f"invoices/{userid}")


def save_invoice_for_user(file, userid: str) -> str:
    """
    Guarda la factura del usuario
    """
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.environ["MINIO_ENDPOINT"]},
        key=os.environ["MINIO_KEY"],
        secret=os.environ["MINIO_SECRET"],
        use_ssl=False,  # Set to True if MinIO is set up with SSL
    )

    filepath = os.path.join(f"invoices/{userid}", file.name)
    with fs.open(filepath, "wb") as f:
        f.write(file.getvalue())

    return filepath
