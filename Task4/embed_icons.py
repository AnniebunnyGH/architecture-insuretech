import xml.etree.ElementTree as ET
import urllib.parse

# Load Task4 diagram
file_path = 'Task4/InsureTech_C4_container-diagram.drawio'
tree = ET.parse(file_path)
root = tree.getroot()

def make_svg_uri(inner_svg):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48"><rect width="48" height="48" rx="4" fill="#2875E2" stroke="#ffffff" stroke-width="2"/>{inner_svg}</svg>'
    return 'data:image/svg+xml,' + urllib.parse.quote(svg)

svg_timeout = make_svg_uri('<circle cx="24" cy="24" r="13" fill="none" stroke="#ffffff" stroke-width="3"/><polyline points="24,16 24,24 29,24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>')
svg_retry = make_svg_uri('<path d="M24,12 A12,12 0 1,0 36,24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/><polygon points="36,15 43,24 33,24" fill="#ffffff"/>')
svg_cb = make_svg_uri('<path d="M24,10 L36,15 C36,26 24,35 24,37 C24,35 12,26 12,15 Z" fill="none" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/><path d="M19,23 L23,27 L29,19" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
svg_rate = make_svg_uri('<path d="M13,31 A13,13 0 1,1 35,31" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/><line x1="24" y1="24" x2="30" y2="17" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/><circle cx="24" cy="24" r="3" fill="#ffffff"/>')

style_base = "aspect=fixed;sketch=0;html=1;dashed=0;whitespace=wrap;verticalLabelPosition=bottom;verticalAlign=top;shape=image;fillColor=#2875E2;strokeColor=#ffffff;"

mapping = {
    'pat_rate_limit_web_ico': svg_rate,
    'pat_rate_limit_sk_ico': svg_rate,
    'pat_timeout_sk_ico': svg_timeout,
    'pat_retry_sk_ico': svg_retry,
    'pat_cb_sk_ico': svg_cb
}

for cell in root.findall('.//mxCell'):
    cid = cell.attrib.get('id')
    if cid in mapping:
        img_uri = mapping[cid]
        cell.attrib['style'] = f"{style_base}image={img_uri};"
        print(f"Updated icon for {cid}")

tree.write(file_path, encoding='utf-8', xml_declaration=True)
print("Successfully embedded SVG icons in Task4/InsureTech_C4_container-diagram.drawio")
