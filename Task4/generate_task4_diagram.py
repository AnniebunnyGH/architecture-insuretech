import xml.etree.ElementTree as ET
import os

src_path = 'Task3/InsureTech_C4_container-diagram.drawio'
dest_path = 'Task4/InsureTech_C4_container-diagram.drawio'

tree = ET.parse(src_path)
root = tree.getroot()
model_root = root.find('.//root')

# Clean existing objects we will reposition or recreate
# Let's inspect objects in model_root
objects = {obj.attrib.get('id'): obj for obj in model_root.findall('object')}

# 1. System Boundary: InsureTech Prod
# Expand to cover all well-spaced elements: x=420, y=120, width=1360, height=1120
boundary = objects.get('uZ0quFO-MIEIE11IO5jD-1')
if boundary is not None:
    cell = boundary.find('mxCell')
    geo = cell.find('mxGeometry')
    geo.attrib['x'] = '420'
    geo.attrib['y'] = '120'
    geo.attrib['width'] = '1360'
    geo.attrib['height'] = '1120'

# 2. Web Container: InsureTech Web
# Position: x=480, y=160, width=250, height=150
web_obj = objects.get('uZ0quFO-MIEIE11IO5jD-4')
if web_obj is not None:
    geo = web_obj.find('mxCell/mxGeometry')
    geo.attrib['x'] = '480'
    geo.attrib['y'] = '160'
    geo.attrib['width'] = '250'
    geo.attrib['height'] = '150'

# 3. core-app
# Position: x=480, y=430, width=250, height=130
core_app = objects.get('uZ0quFO-MIEIE11IO5jD-3')
if core_app is not None:
    core_app.attrib['c4Description'] = "Монолитное приложение:\n• витрина продуктов и расчет ОСАГО\n• REST прием заявок, стриминг котировок через SSE\n• надежная публикация в Kafka (Transactional Outbox)"
    core_app.attrib['label'] = '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>'
    geo = core_app.find('mxCell/mxGeometry')
    geo.attrib['x'] = '480'
    geo.attrib['y'] = '430'
    geo.attrib['width'] = '250'
    geo.attrib['height'] = '130'

# 4. core-db
# Position: x=480, y=700, width=250, height=120
core_db = objects.get('uZ0quFO-MIEIE11IO5jD-2')
if core_db is not None:
    geo = core_db.find('mxCell/mxGeometry')
    geo.attrib['x'] = '480'
    geo.attrib['y'] = '700'
    geo.attrib['width'] = '250'
    geo.attrib['height'] = '120'

# 5. client-info
# Position: x=880, y=160, width=240, height=120
client_info = objects.get('ckVUTfoMV_SZnMC_Z-Nl-1')
if client_info is not None:
    geo = client_info.find('mxCell/mxGeometry')
    geo.attrib['x'] = '880'
    geo.attrib['y'] = '160'
    geo.attrib['width'] = '240'
    geo.attrib['height'] = '120'

# 6. client-info-db
# Position: x=1240, y=160, width=240, height=120
client_db = objects.get('ckVUTfoMV_SZnMC_Z-Nl-2')
if client_db is not None:
    geo = client_db.find('mxCell/mxGeometry')
    geo.attrib['x'] = '1240'
    geo.attrib['y'] = '160'
    geo.attrib['width'] = '240'
    geo.attrib['height'] = '120'

# 7. ins-product-aggregator
# Position: x=880, y=430, width=250, height=130
prod_agg = objects.get('uZ0quFO-MIEIE11IO5jD-16')
if prod_agg is not None:
    geo = prod_agg.find('mxCell/mxGeometry')
    geo.attrib['x'] = '880'
    geo.attrib['y'] = '430'
    geo.attrib['width'] = '250'
    geo.attrib['height'] = '130'

# 8. osago-aggregator (New)
# Position: x=1360, y=430, width=260, height=140
osago_agg_id = "osago_aggregator_container"
osago_agg = objects.get(osago_agg_id)
if osago_agg is None:
    osago_agg = ET.Element("object", {
        "placeholders": "1",
        "c4Name": "osago-aggregator",
        "c4Type": "Container",
        "c4Technology": "Kotlin, Spring Boot",
        "c4Description": "Агрегатор ОСАГО:\n• параллельная отправка заявок в 10 СК\n• опрос решений (Timeout 60s, Retry, CB)\n• мгновенная публикация предложений в Kafka",
        "label": '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>',
        "id": osago_agg_id
    })
    cell = ET.SubElement(osago_agg, "mxCell", {
        "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=11;labelBackgroundColor=none;fillColor=#23A2D9;fontColor=#ffffff;align=center;arcSize=10;strokeColor=#0E7DAD;metaEdit=1;resizable=0;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(cell, "mxGeometry", {
        "x": "1360", "y": "430", "width": "260", "height": "140", "as": "geometry"
    })
    model_root.append(osago_agg)
else:
    geo = osago_agg.find('mxCell/mxGeometry')
    geo.attrib['x'] = '1360'
    geo.attrib['y'] = '430'
    geo.attrib['width'] = '260'
    geo.attrib['height'] = '140'

# 9. osago-aggregator-db (New)
# Position: x=1370, y=640, width=240, height=120
osago_db_id = "osago_aggregator_db_container"
osago_db = objects.get(osago_db_id)
if osago_db is None:
    osago_db = ET.Element("object", {
        "placeholders": "1",
        "c4Type": "osago-aggregator-db",
        "c4Container": "Container",
        "c4Technology": "PostgreSQL / Redis",
        "c4Description": "Хранилище заявок ОСАГО:\n• сопоставление ID заявок InsureTech и СК\n• отслеживание статусов опроса и дедупликация\n• координация между репликами сервиса",
        "label": '<font style="font-size: 16px"><b>%c4Type%</b></font><div>[%c4Container%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>',
        "id": osago_db_id
    })
    cell = ET.SubElement(osago_db, "mxCell", {
        "style": "shape=cylinder3;size=6.17;whiteSpace=wrap;html=1;boundedLbl=1;rounded=0;labelBackgroundColor=none;fillColor=#23A2D9;fontSize=12;fontColor=#ffffff;align=center;strokeColor=#0E7DAD;metaEdit=1;resizable=0;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(cell, "mxGeometry", {
        "x": "1370", "y": "640", "width": "240", "height": "120", "as": "geometry"
    })
    model_root.append(osago_db)
else:
    geo = osago_db.find('mxCell/mxGeometry')
    geo.attrib['x'] = '1370'
    geo.attrib['y'] = '640'
    geo.attrib['width'] = '240'
    geo.attrib['height'] = '120'

# 10. Apache Kafka
# Position: x=860, y=700, width=290, height=140
kafka = objects.get('kafka_broker_container')
if kafka is not None:
    geo = kafka.find('mxCell/mxGeometry')
    geo.attrib['x'] = '860'
    geo.attrib['y'] = '700'
    geo.attrib['width'] = '290'
    geo.attrib['height'] = '140'

# 11. ins-comp-settlement
# Position: x=1370, y=840, width=240, height=120
settlement = objects.get('uZ0quFO-MIEIE11IO5jD-19')
if settlement is not None:
    geo = settlement.find('mxCell/mxGeometry')
    geo.attrib['x'] = '1370'
    geo.attrib['y'] = '840'
    geo.attrib['width'] = '240'
    geo.attrib['height'] = '120'

# 12. ins-comp-settlement-db
# Position: x=1370, y=1030, width=240, height=120
settle_db = objects.get('uZ0quFO-MIEIE11IO5jD-28')
if settle_db is not None:
    geo = settle_db.find('mxCell/mxGeometry')
    geo.attrib['x'] = '1370'
    geo.attrib['y'] = '1030'
    geo.attrib['width'] = '240'
    geo.attrib['height'] = '120'

# 13. External: 10 Страховых компаний
# Move to x=1920, y=430, width=250, height=140 to give 300px clean space for arrows & badges
for sk_id in ['uZ0quFO-MIEIE11IO5jD-11', 'uZ0quFO-MIEIE11IO5jD-12', 'uZ0quFO-MIEIE11IO5jD-13']:
    sk_obj = objects.get(sk_id)
    if sk_obj is not None:
        geo = sk_obj.find('mxCell/mxGeometry')
        offset = 10 if sk_id == 'uZ0quFO-MIEIE11IO5jD-12' else (20 if sk_id == 'uZ0quFO-MIEIE11IO5jD-13' else 0)
        geo.attrib['x'] = str(1920 + offset)
        geo.attrib['y'] = str(430 + offset)
        geo.attrib['width'] = '250'
        geo.attrib['height'] = '140'

# 14. External: Клиент
client_person = objects.get('uZ0quFO-MIEIE11IO5jD-23')
if client_person is not None:
    geo = client_person.find('mxCell/mxGeometry')
    geo.attrib['x'] = '505'
    geo.attrib['y'] = '-80'

# 15. External: Системы партнеров
for p_id in ['uZ0quFO-MIEIE11IO5jD-7', 'uZ0quFO-MIEIE11IO5jD-8', 'uZ0quFO-MIEIE11IO5jD-9']:
    p_obj = objects.get(p_id)
    if p_obj is not None:
        geo = p_obj.find('mxCell/mxGeometry')
        offset = 10 if p_id == 'uZ0quFO-MIEIE11IO5jD-8' else (20 if p_id == 'uZ0quFO-MIEIE11IO5jD-9' else 0)
        geo.attrib['x'] = str(40 + offset)
        geo.attrib['y'] = str(500 + offset)

# 16. External: Платежный сервис
payment_obj = objects.get('uZ0quFO-MIEIE11IO5jD-36')
if payment_obj is not None:
    geo = payment_obj.find('mxCell/mxGeometry')
    geo.attrib['x'] = '40'
    geo.attrib['y'] = '300'

# Helper to remove and clean up existing edges/badges that will be updated
def remove_element(el_id):
    for el in list(model_root):
        if el.attrib.get('id') == el_id:
            model_root.remove(el)

# Remove old task4 elements if exist to rebuild cleanly
old_ids = [
    "rel_web_to_core_sse", "rel_osago_agg_to_db", "rel_core_to_kafka_osago",
    "rel_kafka_to_osago_agg", "rel_osago_agg_to_kafka", "rel_kafka_to_core_proposals",
    "rel_osago_agg_to_sk", "pat_rate_limit_web_ico", "pat_rate_limit_web_txt",
    "pat_timeout_sk_ico", "pat_timeout_sk_txt", "pat_retry_sk_ico", "pat_retry_sk_txt",
    "pat_cb_sk_ico", "pat_cb_sk_txt", "pat_rate_limit_sk_ico", "pat_rate_limit_sk_txt",
    "opt_note_callout", "opt_note_edge"
]
for oid in old_ids:
    remove_element(oid)

# Helper to add clean relationship
def add_rel(rel_id, source_id, target_id, tech, desc, stroke_color="#828282", stroke_width="1", points=None):
    obj = ET.Element("object", {
        "placeholders": "1",
        "c4Type": "Relationship",
        "c4Technology": tech,
        "c4Description": desc,
        "label": f'<div style="text-align: left"><div style="text-align: center"><b>%c4Description%</b></div><div style="text-align: center">[%c4Technology%]</div></div>',
        "id": rel_id
    })
    cell = ET.SubElement(obj, "mxCell", {
        "style": f"endArrow=blockThin;html=1;fontSize=10;fontColor=#404040;strokeWidth={stroke_width};endFill=1;strokeColor={stroke_color};elbow=vertical;metaEdit=1;endSize=14;startSize=14;jumpStyle=arc;jumpSize=16;rounded=0;edgeStyle=orthogonalEdgeStyle;",
        "edge": "1",
        "parent": "1",
        "source": source_id,
        "target": target_id
    })
    geom = ET.SubElement(cell, "mxGeometry", {
        "width": "240", "relative": "1", "as": "geometry"
    })
    if points:
        pts_elem = ET.SubElement(geom, "Array", {"as": "points"})
        for pt in points:
            ET.SubElement(pts_elem, "mxPoint", {"x": str(pt[0]), "y": str(pt[1])})
    model_root.append(obj)

# Update existing relationships points to match clean spacing
# Rel: web -> core-app REST (uZ0quFO-MIEIE11IO5jD-5)
rel_web_core_rest = objects.get('uZ0quFO-MIEIE11IO5jD-5')
if rel_web_core_rest is not None:
    geo = rel_web_core_rest.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    # direct points on left side: x=540
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "540", "y": "320"})
    ET.SubElement(arr, "mxPoint", {"x": "540", "y": "430"})

# Rel: core-app -> core-db (uZ0quFO-MIEIE11IO5jD-6)
rel_core_db = objects.get('uZ0quFO-MIEIE11IO5jD-6')
if rel_core_db is not None:
    geo = rel_core_db.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)

# Rel: client-info -> client-info-db (ckVUTfoMV_SZnMC_Z-Nl-3)
rel_cinfo_db = objects.get('ckVUTfoMV_SZnMC_Z-Nl-3')
if rel_cinfo_db is not None:
    geo = rel_cinfo_db.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)

# Rel: web -> client-info (ckVUTfoMV_SZnMC_Z-Nl-5)
rel_web_cinfo = objects.get('ckVUTfoMV_SZnMC_Z-Nl-5')
if rel_web_cinfo is not None:
    geo = rel_web_cinfo.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "730", "y": "220"})
    ET.SubElement(arr, "mxPoint", {"x": "880", "y": "220"})

# Rel: core-app -> client-info (ckVUTfoMV_SZnMC_Z-Nl-4)
rel_core_cinfo = objects.get('ckVUTfoMV_SZnMC_Z-Nl-4')
if rel_core_cinfo is not None:
    geo = rel_core_cinfo.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "800", "y": "460"})
    ET.SubElement(arr, "mxPoint", {"x": "800", "y": "260"})
    ET.SubElement(arr, "mxPoint", {"x": "880", "y": "260"})

# Rel: ins-product-aggregator -> 10 СК (uZ0quFO-MIEIE11IO5jD-17)
rel_prod_sk = objects.get('uZ0quFO-MIEIE11IO5jD-17')
if rel_prod_sk is not None:
    geo = rel_prod_sk.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "1130", "y": "390"})
    ET.SubElement(arr, "mxPoint", {"x": "1920", "y": "390"})

# Rel: ins-comp-settlement -> 10 СК (uZ0quFO-MIEIE11IO5jD-32)
rel_settle_sk = objects.get('uZ0quFO-MIEIE11IO5jD-32')
if rel_settle_sk is not None:
    geo = rel_settle_sk.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "1610", "y": "900"})
    ET.SubElement(arr, "mxPoint", {"x": "1800", "y": "900"})
    ET.SubElement(arr, "mxPoint", {"x": "1800", "y": "550"})
    ET.SubElement(arr, "mxPoint", {"x": "1920", "y": "550"})

# Rel: Kafka -> ins-comp-settlement (rel_kafka_to_settlement)
rel_k_settle = objects.get('rel_kafka_to_settlement')
if rel_k_settle is not None:
    geo = rel_k_settle.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "1150", "y": "800"})
    ET.SubElement(arr, "mxPoint", {"x": "1260", "y": "800"})
    ET.SubElement(arr, "mxPoint", {"x": "1260", "y": "880"})
    ET.SubElement(arr, "mxPoint", {"x": "1370", "y": "880"})

# Rel: ins-product-aggregator -> Kafka (rel_aggregator_to_kafka)
rel_prod_k = objects.get('rel_aggregator_to_kafka')
if rel_prod_k is not None:
    geo = rel_prod_k.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "950", "y": "560"})
    ET.SubElement(arr, "mxPoint", {"x": "950", "y": "700"})

# Rel: Kafka -> core-app (rel_kafka_to_core_app)
rel_k_core = objects.get('rel_kafka_to_core_app')
if rel_k_core is not None:
    geo = rel_k_core.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "860", "y": "730"})
    ET.SubElement(arr, "mxPoint", {"x": "790", "y": "730"})
    ET.SubElement(arr, "mxPoint", {"x": "790", "y": "520"})
    ET.SubElement(arr, "mxPoint", {"x": "730", "y": "520"})

# Rel: core-app -> Kafka (rel_core_outbox_to_kafka)
rel_core_k = objects.get('rel_core_outbox_to_kafka')
if rel_core_k is not None:
    geo = rel_core_k.find('mxCell/mxGeometry')
    arr = geo.find('Array')
    if arr is not None:
        geo.remove(arr)
    arr = ET.SubElement(geo, "Array", {"as": "points"})
    ET.SubElement(arr, "mxPoint", {"x": "730", "y": "550"})
    ET.SubElement(arr, "mxPoint", {"x": "810", "y": "550"})
    ET.SubElement(arr, "mxPoint", {"x": "810", "y": "780"})
    ET.SubElement(arr, "mxPoint", {"x": "860", "y": "780"})


# --- ADD NEW TASK 4 CONNECTIONS ---

# 1. Web -> core-app (SSE / HTTP/2 for real-time proposals)
add_rel(
    "rel_web_to_core_sse",
    "uZ0quFO-MIEIE11IO5jD-4", # web
    "uZ0quFO-MIEIE11IO5jD-3", # core-app
    "SSE / HTTP/2",
    "Потоковая передача предложений ОСАГО\n(по мере поступления от СК)",
    stroke_color="#E65100",
    stroke_width="2",
    points=[(670, 310), (670, 430)]
)

# 2. osago-aggregator -> osago-aggregator-db (TCP / JDBC)
add_rel(
    "rel_osago_agg_to_db",
    osago_agg_id,
    osago_db_id,
    "TCP / JDBC",
    "Сохранение состояний, ID заявок СК\nи координация реплик",
    stroke_color="#828282",
    stroke_width="1"
)

# 3. osago-aggregator -> 10 СК (REST: create app & poll)
add_rel(
    "rel_osago_agg_to_sk",
    osago_agg_id,
    "uZ0quFO-MIEIE11IO5jD-11",
    "REST",
    "1. POST /applications (создать заявку)\n2. GET /proposals (опрос статуса, дедлайн 60с)",
    stroke_color="#D32F2F",
    stroke_width="2",
    points=[(1620, 500), (1920, 500)]
)

# 4. core-app -> Kafka (publish osago applications)
add_rel(
    "rel_core_to_kafka_osago",
    "uZ0quFO-MIEIE11IO5jD-3",
    "kafka_broker_container",
    "Transactional Outbox",
    "Публикация заявки на расчет ОСАГО\n(топик osago.applications)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(730, 480), (840, 480), (840, 710), (860, 710)]
)

# 5. Kafka -> osago-aggregator (consume osago applications)
add_rel(
    "rel_kafka_to_osago_agg",
    "kafka_broker_container",
    osago_agg_id,
    "Kafka Consumer",
    "Вычитка заявок на расчет\n(топик osago.applications)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(1150, 720), (1280, 720), (1280, 540), (1360, 540)]
)

# 6. osago-aggregator -> Kafka (publish proposals immediately)
add_rel(
    "rel_osago_agg_to_kafka",
    osago_agg_id,
    "kafka_broker_container",
    "Kafka Producer",
    "Мгновенная публикация котировок СК\n(топик osago.proposals)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(1360, 470), (1220, 470), (1220, 760), (1150, 760)]
)

# 7. Kafka -> core-app (consume proposals for SSE stream)
add_rel(
    "rel_kafka_to_core_proposals",
    "kafka_broker_container",
    "uZ0quFO-MIEIE11IO5jD-3",
    "Kafka Consumer",
    "Прием готовых предложений СК для SSE\n(топик osago.proposals)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(860, 810), (760, 810), (760, 540), (730, 540)]
)

# --- ADD RESILIENCE BADGES IN CLEAN, DEDICATED SPACES ---

def add_resilience_badge(icon_id, pr_icon, title, x, y, width=36, height=34):
    icon_cell = ET.Element("mxCell", {
        "id": f"{icon_id}_ico",
        "value": "",
        "style": f"aspect=fixed;sketch=0;html=1;dashed=0;whitespace=wrap;verticalLabelPosition=bottom;verticalAlign=top;fillColor=#2875E2;strokeColor=#ffffff;shape=mxgraph.kubernetes.icon2;prIcon={pr_icon}",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(icon_cell, "mxGeometry", {
        "x": str(x), "y": str(y), "width": str(width), "height": str(height), "as": "geometry"
    })
    model_root.append(icon_cell)
    
    text_cell = ET.Element("mxCell", {
        "id": f"{icon_id}_txt",
        "value": title,
        "style": "text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;fontSize=9;fontStyle=1;fontColor=#ffffff;fillColor=#1A5276;strokeColor=#154360;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(text_cell, "mxGeometry", {
        "x": str(x - 15), "y": str(y + height + 2), "width": str(width + 30), "height": "20", "as": "geometry"
    })
    model_root.append(text_cell)

# Badge 1: Rate Limiter on Web -> core-app entrance (x=440, y=340, left of arrows)
add_resilience_badge("pat_rate_limit_web", "job", "Rate Limiter\n(per User / IP)", 440, 335)

# Badges 2-5: In the spacious corridor between osago-aggregator (x=1620) and 10 СК (x=1920)
# Column at x=1710, y=340..580
add_resilience_badge("pat_timeout_sk", "quota", "Timeout\n(60s)", 1670, 390)
add_resilience_badge("pat_retry_sk", "deploy", "Retry\n(Backoff)", 1750, 390)
add_resilience_badge("pat_cb_sk", "c_role", "Circuit\nBreaker", 1830, 390)
add_resilience_badge("pat_rate_limit_sk", "job", "Rate Limiter\n(per СК)", 1750, 560)

# --- ARCHITECTURAL OPTIMIZATION NOTE (PUSH GATEWAY / SSE PROXY) ---
note_cell = ET.Element("mxCell", {
    "id": "opt_note_callout",
    "value": "<b>💡 Архитектурная оптимизация (TO-BE Evolution):</b><br>Для разгрузки <i>core-app</i> от удержания 2 500+ долгоживущих SSE-соединений целесообразно вынести прослойку <b>Push Gateway / API Gateway</b>.<br>Веб-клиент держит SSE со шлюзом, а шлюз вычитывает топик <i>osago.proposals</i> напрямую из Kafka и пушит в браузер.",
    "style": "shape=note;whiteSpace=wrap;html=1;size=14;verticalAlign=top;align=left;spacing=8;fillColor=#FFF9C4;strokeColor=#FBC02D;fontColor=#333333;fontSize=10;dashed=1;",
    "vertex": "1",
    "parent": "1"
})
ET.SubElement(note_cell, "mxGeometry", {
    "x": "40", "y": "140", "width": "340", "height": "115", "as": "geometry"
})
model_root.append(note_cell)

# Dashed pointer from note to the SSE arrow area
note_edge = ET.Element("mxCell", {
    "id": "opt_note_edge",
    "style": "endArrow=open;dashed=1;html=1;strokeColor=#FBC02D;strokeWidth=1.5;elbow=vertical;rounded=0;edgeStyle=orthogonalEdgeStyle;",
    "edge": "1",
    "parent": "1",
    "source": "opt_note_callout"
})
note_geo = ET.SubElement(note_edge, "mxGeometry", {
    "relative": "1", "as": "geometry"
})
note_arr = ET.SubElement(note_geo, "Array", {"as": "points"})
ET.SubElement(note_arr, "mxPoint", {"x": "380", "y": "200"})
ET.SubElement(note_arr, "mxPoint", {"x": "670", "y": "200"})
ET.SubElement(note_arr, "mxPoint", {"x": "670", "y": "360"})
model_root.append(note_edge)

os.makedirs('Task4', exist_ok=True)
tree.write(dest_path, encoding='utf-8', xml_declaration=True)
print(f"Successfully generated cleaned and spaced {dest_path}")

