import importlib.util
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location('renderer', ROOT / 'html_renderer.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

book = pd.DataFrame([{
    'MUNICIPIO': 'Bogotá', 'UPZ/COMUNA': 'Centro', 'SEG26': 'BASE', 'TIE27': 'TMCB',
    'NAME': 'Tienda prueba', 'ESTADO': 'ABIERTA', 'MESOP_NUM': 1,
    'VENTAS OUM_NUM': 100, 'RENTA UM_NUM': 20, 'AREA_NUM': 10, 'COSTO M2_NUM': 5,
}])
fields = {
    'project_name': 'Punto general', 'city': 'Bogotá', 'upz': 'Centro', 'segment': 'Base',
    'specialist': 'ANDRES DUQUE RESTREPO', 'project_rent': 1200000,
    'project_area': 100, 'project_rent_m2': 12000,
    'commercial_permanencia': 'SI', 'commercial_gracia': '60', 'commercial_ipc': '+2',
    'commercial_operacion': 'SI', 'commercial_alcohol': 'NO', 'commercial_prima': 'SI',
    'commercial_anticipo': 'NO', 'commercial_clausulas': 'SI', 'commercial_restricciones': 'NO',
    'generator_type': 'Comercial',
    'generator_cards': [{'name': 'Centro comercial', 'type': 'Comercial', 'value': 50}],
    'generator_housing_cards': [{'name': 'Vivienda prueba', 'type': 'Residencial', 'value': 80}],
    'microsaturation_enabled': 'Sí', 'book_store': 'Tienda espejo ABC',
    'sister_store_link': 'https://example.com/tienda-espejo',
    'traffic_video_link': 'https://example.com/traffic',
}
images = {
    'microsaturation_image_1': b'one', 'microsaturation_image_2': b'two',
    'microsaturation_image_3': b'three', 'pilot_image_1': b'pilot-one', 'pilot_image_2': b'pilot-two',
    'generator_housing_image_1': b'housing-one',
}
html = renderer.render(fields, {'JUN': book}, images)
assert html.count('<section class="slide') == 15
assert 'Slide 7' not in html
assert 'Performance combinado' not in html
assert 'Venta promedio' in html
assert 'PPT: PUNTO POTENCIAL' in html
assert 'PR: PLAN RECTOR' in html
assert 'NF: NUEVOS FORMATOS' in html
assert 'Networks' in html
assert 'Periodo de gracia (Dias)' in html
assert 'Tienda espejo ABC' in html
assert 'https://example.com/tienda-espejo' in html
assert 'Entorno | Generadores Vivienda' in html
assert 'Vivienda prueba' in html
assert 'aG91c2luZy1vbmU=' in html
assert 'Entorno | Generadores Empleo' in html
assert 'Expansión | Mercado y Tráfico' in html
assert 'Video tráfico' in html
assert 'Piloto 2' in html
assert html.count('data:image/png;base64') >= 5
assert '.micro-photo' in html and 'object-fit:contain' in html
assert '.micro-grid.count-1 { grid-template-columns:1fr; grid-auto-rows:5.7in; }' in html
assert '<h1>Microsaturación 1</h1>' in html
assert '<h1>Microsaturación 2</h1>' in html
assert '<h1>Microsaturación 3</h1>' in html
print('OK: composición general, Microsaturación adicional y Piloto validados')
