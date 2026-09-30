import xml.etree.ElementTree as ET
import html

# Load clean original XML
tree = ET.parse('Task3/original_clean.drawio')
root = tree.getroot()

# Find diagram root <root> element
model_root = root.find('.//root')

# 1. Update core-db description
for obj in model_root.findall('object'):
    obj_id = obj.attrib.get('id')
    
    if obj_id == 'uZ0quFO-MIEIE11IO5jD-2':  # core-db
        desc = "БД для тарифов, заявок клиентов, оформленных страховок и таблицы outbox_events для надежной публикации событий"
        obj.attrib['c4Description'] = desc
        label = '<font style="font-size: 16px"><b>%c4Type%</b></font><div>[%c4Container%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>'
        obj.attrib['label'] = label
        
    elif obj_id == 'uZ0quFO-MIEIE11IO5jD-3':  # core-app
        desc = "Монолитное приложение:\n• витрина продуктов и локальная реплика тарифов\n• оформление страховок (паттерн Transactional Outbox)\n• подписка на обновления тарифов из шины событий"
        obj.attrib['c4Description'] = desc
        label = '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>'
        obj.attrib['label'] = label

    elif obj_id == 'uZ0quFO-MIEIE11IO5jD-16':  # ins-product-aggregator
        desc = "Интеграция со страховыми компаниями (10 СК): получение тарифов, проверка доступности и публикация событий в Apache Kafka"
        obj.attrib['c4Description'] = desc
        label = '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>'
        obj.attrib['label'] = label

    elif obj_id == 'uZ0quFO-MIEIE11IO5jD-19':  # ins-comp-settlement
        desc = "Сервис взаиморасчётов со страховыми компаниями: асинхронный учет оформленных страховок из Kafka, ежемесячный реестр в СК"
        obj.attrib['c4Description'] = desc
        label = '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>'
        obj.attrib['label'] = label

    elif obj_id in ['uZ0quFO-MIEIE11IO5jD-11', 'uZ0quFO-MIEIE11IO5jD-12', 'uZ0quFO-MIEIE11IO5jD-13']:  # СК
        desc = "10 систем страховых компаний (5 текущих + 5 новых): API для тарифов, андеррайтинга и взаиморасчетов"
        obj.attrib['c4Description'] = desc
        label = '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%]</div><br><div><font style="font-size: 11px"><font color="#cccccc">%c4Description%</font></font></div>'
        obj.attrib['label'] = label

    elif obj_id == 'ckVUTfoMV_SZnMC_Z-Nl-2':  # client-info-db (fix c4Type in template)
        obj.attrib['c4Type'] = 'client-info-db'

# 2. Remove obsolete synchronous REST relationships:
# uZ0quFO-MIEIE11IO5jD-18 (core-app -> ins-product-aggregator)
# uZ0quFO-MIEIE11IO5jD-33 (ins-comp-settlement -> ins-product-aggregator)
# uZ0quFO-MIEIE11IO5jD-34 (ins-comp-settlement -> core-app)
to_remove = ['uZ0quFO-MIEIE11IO5jD-18', 'uZ0quFO-MIEIE11IO5jD-33', 'uZ0quFO-MIEIE11IO5jD-34']
for obj in list(model_root.findall('object')):
    if obj.attrib.get('id') in to_remove:
        model_root.remove(obj)

# 3. Add Apache Kafka container
# Position: x=780, y=530, width=240, height=130
kafka_id = "kafka_broker_container"
kafka_obj = ET.Element("object", {
    "placeholders": "1",
    "c4Name": "Apache Kafka",
    "c4Type": "Container",
    "c4Technology": "Apache Kafka / Event-Streaming",
    "c4Description": "Шина событий (Event Streaming Platform):\n• Топик insurance.products-tariffs\n• Топик insurance.policies\nГарантия At-least-once доставки",
    "label": '<font style="font-size: 16px"><b>%c4Name%</b></font><div>[%c4Type%: %c4Technology%]</div><br><div><font style="font-size: 11px"><font color="#E6E6E6">%c4Description%</font></font></div>',
    "id": kafka_id
})
kafka_cell = ET.SubElement(kafka_obj, "mxCell", {
    "style": "rounded=1;whiteSpace=wrap;html=1;fontSize=11;labelBackgroundColor=none;fillColor=#107C41;fontColor=#ffffff;align=center;arcSize=10;strokeColor=#0B5A2F;metaEdit=1;resizable=0;points=[[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];",
    "vertex": "1",
    "parent": "1"
})
ET.SubElement(kafka_cell, "mxGeometry", {
    "x": "780",
    "y": "530",
    "width": "240",
    "height": "130",
    "as": "geometry"
})
model_root.append(kafka_obj)

# 4. Helper function to create relationship
def add_rel(rel_id, source_id, target_id, tech, desc, points=None):
    obj = ET.Element("object", {
        "placeholders": "1",
        "c4Type": "Relationship",
        "c4Technology": tech,
        "c4Description": desc,
        "label": '<div style="text-align: left"><div style="text-align: center"><b>%c4Description%</b></div><div style="text-align: center">[%c4Technology%]</div></div>',
        "id": rel_id
    })
    cell = ET.SubElement(obj, "mxCell", {
        "style": "endArrow=blockThin;html=1;fontSize=10;fontColor=#404040;strokeWidth=1.5;endFill=1;strokeColor=#107C41;elbow=vertical;metaEdit=1;endSize=14;startSize=14;jumpStyle=arc;jumpSize=16;rounded=0;edgeStyle=orthogonalEdgeStyle;",
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

# Add new Event-Streaming relationships:
# Rel 1: ins-product-aggregator -> Kafka (Publish products-tariffs events)
add_rel(
    "rel_aggregator_to_kafka",
    "uZ0quFO-MIEIE11IO5jD-16",
    kafka_id,
    "Kafka Producer",
    "Публикация событий обновления\nпродуктов и тарифов",
    points=[(1180, 560), (1030, 560)]
)

# Rel 2: Kafka -> core-app (Subscribe products-tariffs events for local replica)
add_rel(
    "rel_kafka_to_core_app",
    kafka_id,
    "uZ0quFO-MIEIE11IO5jD-3",
    "Kafka Consumer",
    "Подписка на события продуктов\nи тарифов (репликация в core-db)",
    points=[(770, 570), (740, 570), (740, 500)]
)

# Rel 3: core-app -> Kafka (Transactional Outbox / CDC for issued policies)
add_rel(
    "rel_core_outbox_to_kafka",
    "uZ0quFO-MIEIE11IO5jD-3",
    kafka_id,
    "Transactional Outbox / CDC",
    "Гарантированная публикация событий\nоформленных страховок (policies)",
    points=[(610, 560), (610, 610), (770, 610)]
)

# Rel 4: Kafka -> ins-comp-settlement (Subscribe policies and tariffs)
add_rel(
    "rel_kafka_to_settlement",
    kafka_id,
    "uZ0quFO-MIEIE11IO5jD-19",
    "Kafka Consumer",
    "Подписка на события оформленных\nстраховок и тарифов",
    points=[(900, 670), (900, 730), (1050, 730)]
)

# Save updated drawio diagram
tree.write('Task3/InsureTech_C4_container-diagram.drawio', encoding='utf-8', xml_declaration=True)
print("Successfully generated Task3/InsureTech_C4_container-diagram.drawio")
