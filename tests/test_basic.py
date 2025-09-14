from doctr.io import DocumentFile
from facturas import parse_invoice


def test_manual_save_json_in_user_folder():
    """
    Validamos si extrae bien lso datos de PDF
    """
    with open("muestras/factura3.pdf","rb") as f:
        contenido = f.read()
        doc = DocumentFile.from_pdf(contenido)

    _, json = parse_invoice(doc)

    # Contiene pages
    assert list(json.keys()) == ["pages"]

    # Pages es una lista
    assert isinstance(json["pages"], list)

    # See Iraitz
    assert json["pages"][0]["blocks"][0]["lines"][1]["words"][0]["value"] == "Iraitz"
