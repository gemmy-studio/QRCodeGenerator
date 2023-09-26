from qrcodegen import *
import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="QR Code 생성기", page_icon="favicon.ico", layout="centered", initial_sidebar_state="auto", menu_items=None)

button = """
<script data-name="BMC-Widget" data-cfasync="false" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="woojae" data-description="Support me on Buy me a coffee!" data-message="방문해주셔서 감사합니다 :)" data-color="#40DCA5" data-position="Right" data-x_margin="18" data-y_margin="18"></script>
"""

html(button, height=600, width=400)

st.markdown(
    """
    <style>
        iframe[width="400"] {
            position: fixed;
            bottom: 60px;
            right: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def to_svg_str(qr: QrCode, border: int) -> str:
	"""Returns a string of SVG code for an image depicting the given QR Code, with the given number
	of border modules. The string always uses Unix newlines (\n), regardless of the platform."""
	if border < 0:
		raise ValueError("Border must be non-negative")
	parts: List[str] = []
	for y in range(qr.get_size()):
		for x in range(qr.get_size()):
			if qr.get_module(x, y):
				parts.append(f"M{x+border},{y+border}h1v1h-1z")
	return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 {qr.get_size()+border*2} {qr.get_size()+border*2}" stroke="none">
	<rect width="100%" height="100%" fill="#FFFFFF"/>
	<path d="{" ".join(parts)}" fill="#000000"/>
</svg>
"""

st.title('QR Code 생성기')
url = st.text_input('URL 또는 문자를 입력해주세요. (예: https://www.google.com/)')

if st.button('생성하기'):
    with st.spinner('QR Code 생성중'):
        # Simple operation
        qr_data = QrCode.encode_text(url, QrCode.Ecc.MEDIUM)
        svg_data = to_svg_str(qr_data, 4)  # See qrcodegen-demo

        # 불필요한 개행과 공백 제거
        svg_data_cleaned = svg_data.strip()

        st.image(svg_data_cleaned, caption='QR Code', width=300)

        st.download_button(
            label="SVG 다운받기",
            data=svg_data_cleaned,
            file_name="qrcode.svg",
            mime="image/svg"
        )