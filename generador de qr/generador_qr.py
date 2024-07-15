import qrcode
import streamlit as st

filename = "qr_realizados/qr_code.png"

def generate_qr_code(url, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

st.set_page_config(page_title="QR Code Generator", page_icon="💻", layout="centered")
st.title("Generador de codigos QR")
st.image("imagenes/qr_uses.jpg", use_column_width=True)

url = st.text_input("Ingrese la URL que desea convertir a QR")

if st.button("Generar codigo QR"):
    if url:
        generate_qr_code(url, filename)
        st.image(filename, use_column_width=True)
        with open(filename, "rb") as f:
            image_data = f.read()
        st.download_button(label="Download QR", data=image_data, file_name="qr_generado.png")
    else:
        st.warning("Por favor, ingresa una URL válida.")
