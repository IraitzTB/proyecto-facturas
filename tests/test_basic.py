from facturas import parse_invoice

def test_manual_save_json_in_user_folder():
    """
    Validamos si extrae bien lso datos de PDF
    """
    # TODO: Cambiar para que funcione con las credenciales de LLAMA_CLOUD

    #result = parse_invoice(doc, "muestras/factura3.pdf")

    # See Iraitz
    assert True #result.data["merchant"]["name"] == "Iraitz Montalbán"
