import xml.etree.ElementTree as ET
import os

# Base on Task3 diagram
src_path = 'Task3/InsureTech_C4_container-diagram.drawio'
dest_path = 'Task4/InsureTech_C4_container-diagram.drawio'

tree = ET.parse(src_path)
root = tree.getroot()
model_root = root.find('.//root')

# 1. Expand the system boundary slightly to fit osago-aggregator and its DB cleanly
# Boundary id: uZ0quFO-MIEIE11IO5jD-1
for obj in model_root.findall('object'):
    if obj.attrib.get('id') == 'uZ0quFO-MIEIE11IO5jD-1':
        cell = obj.find('mxCell')
        geom = cell.find('mxGeometry')
        geom.attrib['width'] = '1180'
        geom.attrib['height'] = '1060'

# 2. Update core-app description to reflect OSAGO API and SSE push
for obj in model_root.findall('object'):
    if obj.attrib.get('id') == 'uZ0quFO-MIEIE11IO5jD-3':
        desc = "Монолитное приложение:\n• витрина продуктов и ОСАГО\n• REST прием заявок ОСАГО и стриминг предложений клиентам через SSE\n• шина событий Kafka (Transactional Outbox)"
        obj.attrib['c4Description'] = desc
        obj.attrib['label'] = '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>'

# 3. Add container: osago-aggregator
# Position: x=1080, y=520, width=240, height=120
osago_agg_id = "osago_aggregator_container"
osago_agg_obj = ET.Element("object", {
    "placeholders": "1",
    "c4Name": "osago-aggregator",
    "c4Type": "Container",
    "c4Technology": "Kotlin, Spring Boot",
    "c4Description": "Агрегатор ОСАГО:\n• параллельная отправка заявок в 10 СК\n• опрос решений (Timeout 60s, Retry, Circuit Breaker)\n• стриминг готовых предложений в Kafka",
    "label": '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>',
    "id": osago_agg_id
})
osago_agg_cell = ET.SubElement(osago_agg_obj, "mxCell", {
    "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=11;labelBackgroundColor=none;fillColor=#23A2D9;fontColor=#ffffff;align=center;arcSize=10;strokeColor=#0E7DAD;metaEdit=1;resizable=0;points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];",
    "vertex": "1",
    "parent": "1"
})
ET.SubElement(osago_agg_cell, "mxGeometry", {
    "x": "1080",
    "y": "520",
    "width": "240",
    "height": "120",
    "as": "geometry"
})
model_root.append(osago_agg_obj)

# 4. Add database: osago-aggregator-db
# Position: x=1380, y=520, width=210, height=120
osago_db_id = "osago_aggregator_db_container"
osago_db_obj = ET.Element("object", {
    "placeholders": "1",
    "c4Type": "osago-aggregator-db",
    "c4Container": "Container",
    "c4Technology": "PostgreSQL / Redis",
    "c4Description": "Хранилище статусов заявок ОСАГО:\n• сопоставление ID заявок InsureTech и СК\n• отслеживание статусов опроса и дедупликация\n• координация между репликами сервиса",
    "label": '<font style="font-size: 16px"><b>%c4Type%</b></font><div>[%c4Container%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>',
    "id": osago_db_id
})
osago_db_cell = ET.SubElement(osago_db_obj, "mxCell", {
    "style": "shape=cylinder3;size=6.17;whiteSpace=wrap;html=1;boundedLbl=1;rounded=0;labelBackgroundColor=none;fillColor=#23A2D9;fontSize=12;fontColor=#ffffff;align=center;strokeColor=#0E7DAD;metaEdit=1;points=[[0.5,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.5,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];resizable=0;",
    "vertex": "1",
    "parent": "1"
})
ET.SubElement(osago_db_cell, "mxGeometry", {
    "x": "1380",
    "y": "520",
    "width": "210",
    "height": "120",
    "as": "geometry"
})
model_root.append(osago_db_obj)

# Helper function to create relationships
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
        "width": "240",
        "relative": "1",
        "as": "geometry"
    })
    if points:
        pts_elem = ET.SubElement(geom, "Array", {"as": "points"})
        for pt in points:
            ET.SubElement(pts_elem, "mxPoint", {"x": str(pt[0]), "y": str(pt[1])})
    model_root.append(obj)

# 5. Add Relationships:
# Rel A: Web -> core-app via Server-Sent Events (SSE) for streaming proposals
add_rel(
    "rel_web_to_core_sse",
    "uZ0quFO-MIEIE11IO5jD-4", # web
    "uZ0quFO-MIEIE11IO5jD-3", # core-app
    "SSE / HTTP/2",
    "Получение предложений ОСАГО в реальном времени\n(по мере поступления от СК)",
    stroke_color="#E65100",
    stroke_width="2",
    points=[(680, 320), (680, 430)]
)

# Rel B: osago-aggregator -> osago-aggregator-db (TCP/JDBC)
add_rel(
    "rel_osago_agg_to_db",
    osago_agg_id,
    osago_db_id,
    "TCP / JDBC",
    "Сохранение состояний и ID заявок СК",
    stroke_color="#828282",
    stroke_width="1"
)

# Rel C: core-app -> Kafka (publish osago applications)
add_rel(
    "rel_core_to_kafka_osago",
    "uZ0quFO-MIEIE11IO5jD-3",
    "kafka_broker_container",
    "Transactional Outbox",
    "Публикация заявки на ОСАГО\n(топик osago.applications)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(560, 550), (560, 710), (810, 710)]
)

# Rel D: Kafka -> osago-aggregator (consume osago applications)
add_rel(
    "rel_kafka_to_osago_agg",
    "kafka_broker_container",
    osago_agg_id,
    "Kafka Consumer",
    "Вычитка новых заявок на расчет\n(топик osago.applications)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(930, 685), (930, 580), (1080, 580)]
)

# Rel E: osago-aggregator -> Kafka (publish individual proposals)
add_rel(
    "rel_osago_agg_to_kafka",
    osago_agg_id,
    "kafka_broker_container",
    "Kafka Producer",
    "Мгновенная публикация предложений СК\n(топик osago.proposals)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(1130, 640), (1130, 740), (1050, 740)]
)

# Rel F: Kafka -> core-app (consume proposals to stream to web)
add_rel(
    "rel_kafka_to_core_proposals",
    "kafka_broker_container",
    "uZ0quFO-MIEIE11IO5jD-3",
    "Kafka Consumer",
    "Прием готовых предложений СК для SSE-трансляции\n(топик osago.proposals)",
    stroke_color="#107C41",
    stroke_width="1.5",
    points=[(850, 685), (850, 470), (730, 470)]
)

# Rel G: osago-aggregator -> 10 СК (REST API: create application & poll proposal)
add_rel(
    "rel_osago_agg_to_sk",
    osago_agg_id,
    "uZ0quFO-MIEIE11IO5jD-11",
    "REST",
    "1. POST /applications (создать заявку)\n2. GET /proposals (опрос статуса, макс 60с)",
    stroke_color="#D32F2F",
    stroke_width="2",
    points=[(1320, 580), (1620, 580)]
)

# 6. Helper to add resilience pattern icons from the provided library
# Shape: mxgraph.kubernetes.icon2 with prIcon
def add_resilience_badge(icon_id, pr_icon, title, x, y, width=38, height=36):
    # Icon cell
    icon_cell = ET.Element("mxCell", {
        "id": f"{icon_id}_ico",
        "value": "",
        "style": f"aspect=fixed;sketch=0;html=1;dashed=0;whitespace=wrap;verticalLabelPosition=bottom;verticalAlign=top;fillColor=#2875E2;strokeColor=#ffffff;points=[[0.005,0.63,0],[0.1,0.2,0],[0.9,0.2,0],[0.5,0,0],[0.995,0.63,0],[0.72,0.99,0],[0.5,1,0],[0.28,0.99,0]];shape=mxgraph.kubernetes.icon2;prIcon={pr_icon}",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(icon_cell, "mxGeometry", {
        "x": str(x),
        "y": str(y),
        "width": str(width),
        "height": str(height),
        "as": "geometry"
    })
    model_root.append(icon_cell)
    
    # Text label cell
    text_cell = ET.Element("mxCell", {
        "id": f"{icon_id}_txt",
        "value": title,
        "style": "text;html=1;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=1;fontSize=9;fontStyle=1;fontColor=#ffffff;fillColor=#1A5276;strokeColor=#154360;spacingLeft=4;",
        "vertex": "1",
        "parent": "1"
    })
    ET.SubElement(text_cell, "mxGeometry", {
        "x": str(x + width + 4),
        "y": str(y + 6),
        "width": str(len(title) * 7 + 10),
        "height": "24",
        "as": "geometry"
    })
    model_root.append(text_cell)

# 7. Add Resilience Pattern badges on the diagram:
# A. Rate Limiter on Web -> core-app entrance (protect against spike of 2500+ users)
add_resilience_badge("pat_rate_limit_web", "job", "Rate Limiter (2500 RPS)", 500, 350)

# B. Timeout (60s) on osago-aggregator -> СК
add_resilience_badge("pat_timeout_sk", "quota", "Timeout (60s)", 1370, 605)

# C. Retry on osago-aggregator polling loop
add_resilience_badge("pat_retry_sk", "deploy", "Retry (Exp. Backoff)", 1370, 645)

# D. Circuit Breaker on osago-aggregator -> СК (isolate failed companies)
add_resilience_badge("pat_cb_sk", "c_role", "Circuit Breaker", 1370, 685)

# E. Rate Limiter on outbound requests to individual insurance companies
add_resilience_badge("pat_rate_limit_sk", "job", "Rate Limiter (per СК)", 1370, 725)

# Save the Task4 diagram
os.makedirs('Task4', exist_ok=True)
tree.write(dest_path, encoding='utf-8', xml_declaration=True)
print(f"Successfully generated {dest_path}")
