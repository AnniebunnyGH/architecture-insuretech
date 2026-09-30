import json
import re
import xml.etree.ElementTree as ET

# Load services library
with open('libraries/Yandex_Cloud_services_oct_23.xml', 'r', encoding='utf-8') as f:
    text = f.read()
    match = re.search(r'<mxlibrary>(.*?)</mxlibrary>', text)
    services_lib = json.loads(match.group(1))

services = {item.get('title'): item for item in services_lib}

# Create XML Root
root = ET.Element('mxfile', {'host': 'app.diagrams.net', 'version': '24.7.11'})
diag = ET.SubElement(root, 'diagram', {'name': 'InureTech_технологическая архитектура_to-be', 'id': 'inuretech-to-be'})
model = ET.SubElement(diag, 'mxGraphModel', {
    'dx': '1422', 'dy': '850', 'grid': '1', 'gridSize': '10', 'guides': '1',
    'tooltips': '1', 'connect': '1', 'arrows': '1', 'fold': '1', 'page': '1',
    'pageScale': '1', 'pageWidth': '2400', 'pageHeight': '1600', 'math': '0', 'shadow': '0'
})
r = ET.SubElement(model, 'root')
ET.SubElement(r, 'mxCell', {'id': '0'})
ET.SubElement(r, 'mxCell', {'id': '1', 'parent': '0'})

cell_id = 2
def next_id():
    global cell_id
    res = str(cell_id)
    cell_id += 1
    return res

def add_cell(value="", style="", parent="1", vertex="1", x=0, y=0, w=100, h=50):
    cid = next_id()
    if vertex == "1" or vertex == 1:
        if "html=1" not in style:
            style = "html=1;" + style
        if "whiteSpace=wrap" not in style:
            style = "whiteSpace=wrap;" + style
    cell = ET.SubElement(r, 'mxCell', {
        'id': cid,
        'value': value,
        'style': style,
        'parent': parent,
        'vertex': str(vertex)
    })
    ET.SubElement(cell, 'mxGeometry', {
        'x': str(x), 'y': str(y), 'width': str(w), 'height': str(h), 'as': 'geometry'
    })
    return cid

def add_edge(source, target, value="", style="", points=None, exit_xy=None, entry_xy=None):
    cid = next_id()
    base_style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;fontColor=#0F172A;fontSize=11;labelBackgroundColor=#FFFFFF;strokeWidth=2;"
    if style:
        base_style += style
    else:
        base_style += "strokeColor=#2563EB;"
    
    if exit_xy:
        base_style += f"exitX={exit_xy[0]};exitY={exit_xy[1]};"
    if entry_xy:
        base_style += f"entryX={entry_xy[0]};entryY={entry_xy[1]};"

    edge = ET.SubElement(r, 'mxCell', {
        'id': cid,
        'value': value,
        'style': base_style,
        'parent': '1',
        'edge': '1',
        'source': source,
        'target': target
    })
    geom = ET.SubElement(edge, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
    if points:
        pts = ET.SubElement(geom, 'Array', {'as': 'points'})
        for px, py in points:
            ET.SubElement(pts, 'mxPoint', {'x': str(px), 'y': str(py)})
    return cid

# ==================== 1. TOP HEADER BANNER ====================
add_cell(
    value="<div style='font-size:20px; font-weight:bold; color:#FFFFFF;'>InsureTech: Целевая технологическая архитектура (TO-BE)</div>"
          "<div style='font-size:13px; color:#94A3B8; margin-top:3px;'>"
          "Multi-AZ (3 зоны) | SLA: 99.9% | RTO &le; 45 мин. (факт &lt; 1 мин.) | RPO &le; 15 мин. (факт 0 мин.) | Yandex Cloud CDN + L7 ALB"
          "</div>",
    style="rounded=1;fillColor=#0F172A;strokeColor=#1E293B;fontColor=#FFFFFF;align=center;verticalAlign=middle;shadow=1;",
    x=60, y=30, w=2280, h=60
)

# ==================== 2. CLIENT TIER (y: 110 to 170) ====================
users_cell = add_cell(
    value="<div style='font-size:14px; font-weight:bold; color:#1E40AF;'>👥 Пользователи в регионах РФ</div>"
          "<div style='font-size:12px; color:#475569;'>Клиенты из 11 часовых поясов РФ (Калининград ... Владивосток)</div>",
    style="rounded=1;fillColor=#FFFFFF;strokeColor=#2563EB;strokeWidth=2;fontColor=#0F172A;align=center;verticalAlign=middle;shadow=1;",
    x=450, y=110, w=480, h=55
)

partners_cell = add_cell(
    value="<div style='font-size:14px; font-weight:bold; color:#475569;'>🏢 B2B Партнёры и Агенты</div>"
          "<div style='font-size:12px; color:#475569;'>Банки, агрегаторы, ритейл (REST / gRPC API)</div>",
    style="rounded=1;fillColor=#FFFFFF;strokeColor=#475569;strokeWidth=2;fontColor=#0F172A;align=center;verticalAlign=middle;shadow=1;",
    x=1470, y=110, w=480, h=55
)

# ==================== 3. EDGE PERIMETER: CDN, DNS, WAF (y: 190 to 275) ====================
cdn_box = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#0369A1;'>🌐 Yandex Cloud CDN (Edge Caching)</div>"
          "<div style='font-size:11px; color:#334155; line-height:140%; margin-top:3px;'>"
          "• Точки присутствия (PoPs) по всей РФ (СПб, Урал, Сибирь, ДВ, Юг)<br>"
          "• Кэширование статики SPA (JS/CSS, картинки) | <b>TTFB &lt; 50 мс</b>"
          "</div>",
    style="rounded=1;fillColor=#F0F9FF;strokeColor=#0284C7;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=60, y=190, w=680, h=80
)

dns_box = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#334155;'>🛡️ Cloud DNS &amp; DDoS Protection</div>"
          "<div style='font-size:11px; color:#334155; line-height:140%; margin-top:3px;'>"
          "• Anycast GeoDNS маршрутизация<br>"
          "• Защита от L3/L4 DDoS-атак на периметре"
          "</div>",
    style="rounded=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=780, y=190, w=740, h=80
)

waf_box = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#B45309;'>🔒 WAF &amp; Rate Limiting</div>"
          "<div style='font-size:11px; color:#334155; line-height:140%; margin-top:3px;'>"
          "• Защита от L7 веб-атак (OWASP Top 10)<br>"
          "• Rate Limiting &amp; Quotas (изоляция B2B партнёров)"
          "</div>",
    style="rounded=1;fillColor=#FEFCE8;strokeColor=#CA8A04;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=1560, y=190, w=780, h=80
)

# Connect Clients to Perimeter
add_edge(users_cell, cdn_box, value="<b>Статика (SPA)</b>", style="strokeColor=#0284C7;dashed=1;", exit_xy=(0.2, 1), entry_xy=(0.5, 0))
add_edge(users_cell, dns_box, value="<b>Динамика (API)</b>", style="strokeColor=#2563EB;", exit_xy=(0.7, 1), entry_xy=(0.3, 0))
add_edge(partners_cell, waf_box, value="<b>B2B API</b>", style="strokeColor=#CA8A04;", exit_xy=(0.5, 1), entry_xy=(0.5, 0))

# ==================== 4. APPLICATION LOAD BALANCER WIDE BAR (y: 295 to 350) ====================
alb_bar = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#1E40AF;'>⚖️ Yandex Application Load Balancer (ALB) — L7 Multi-AZ</div>"
          "<div style='font-size:11px; color:#334155; margin-top:2px;'>"
          "Anycast IP в 3 зонах | SSL Termination | Балансировка на Ingress | <b>Health Check: <code>GET /healthz</code> (каждые 2с)</b>"
          "</div>",
    style="rounded=1;fillColor=#EFF6FF;strokeColor=#2563EB;strokeWidth=2;fontColor=#0F172A;align=center;verticalAlign=middle;shadow=1;",
    x=60, y=295, w=2280, h=55
)

# Connect Perimeter to ALB
add_edge(dns_box, alb_bar, value="", style="strokeColor=#2563EB;", exit_xy=(0.5, 1), entry_xy=(0.45, 0))
add_edge(waf_box, alb_bar, value="", style="strokeColor=#CA8A04;", exit_xy=(0.5, 1), entry_xy=(0.85, 0))
add_edge(cdn_box, alb_bar, value="Origin (cache miss)", style="strokeColor=#0284C7;dashed=1;", exit_xy=(0.5, 1), entry_xy=(0.15, 0))

# ==================== 5. MULTI-AZ REGION (y: 375 to 1100) ====================
region_box = add_cell(
    value="<div style='font-size:14px; font-weight:bold; color:#334155;'>☁️ Регион Yandex Cloud: ru-central1 (3 зоны доступности: ru-central1-a, ru-central1-b, ru-central1-d)</div>",
    style="rounded=1;fillColor=#F8FAFC;strokeColor=#94A3B8;strokeWidth=1.5;dashed=1;fontColor=#1E293B;verticalAlign=top;align=left;spacingTop=8;spacingLeft=15;",
    x=60, y=375, w=2280, h=720
)

# Regional Master Control Plane Banner
k8s_control_plane = add_cell(
    value="<div style='font-size:12px; font-weight:bold; color:#1E3A8A;'>☸️ Managed Service for Kubernetes: Regional Master (3 AZ, кворум etcd, SLA 99.95%, единый CI/CD)</div>",
    style="rounded=1;fillColor=#DBEAFE;strokeColor=#2563EB;strokeWidth=1.5;fontColor=#1E3A8A;align=center;verticalAlign=middle;",
    x=90, y=410, w=2220, h=38
)

# 3 AZ Configurations
az_configs = [
    {
        'name': 'Зона A (ru-central1-a)',
        'x': 90, 'w': 710,
        'hdr_bg': '#1E40AF',
        'alb_anchor': 0.18,
        'db_title': '🐘 PostgreSQL Master',
        'db_title_color': '#B91C1C',
        'db_fill': '#FEF2F2', 'db_stroke': '#DC2626',
        'db_sub': '<b>Чтение и запись</b> | 50 GB | PgBouncer Pool | Схемы: core, client, settlement'
    },
    {
        'name': 'Зона B (ru-central1-b)',
        'x': 845, 'w': 710,
        'hdr_bg': '#065F46',
        'alb_anchor': 0.50,
        'db_title': '🐘 PostgreSQL Synchronous Standby',
        'db_title_color': '#047857',
        'db_fill': '#ECFDF5', 'db_stroke': '#059669',
        'db_sub': '<b>Синхронная реплика (RPO = 0)</b> | Auto-Failover Patroni (&lt; 30с) | PgBouncer'
    },
    {
        'name': 'Зона D (ru-central1-d)',
        'x': 1600, 'w': 710,
        'hdr_bg': '#1E3A8A',
        'alb_anchor': 0.82,
        'db_title': '🐘 PostgreSQL Asynchronous Standby',
        'db_title_color': '#1D4ED8',
        'db_fill': '#EFF6FF', 'db_stroke': '#2563EB',
        'db_sub': '<b>Read-Only реплика</b> (аналитика settlement) | Кворум 3 узлов | PgBouncer'
    }
]

az_ingress_cells = []
az_db_cells = []

for az in az_configs:
    # AZ Background Box
    add_cell(
        value="",
        style="rounded=1;fillColor=#FFFFFF;strokeColor=#CBD5E1;strokeWidth=1.5;fontColor=#0F172A;shadow=1;",
        x=az['x'], y=465, w=az['w'], h=515
    )

    # AZ Header Ribbon
    add_cell(
        value=f"<div style='font-size:13px; font-weight:bold; color:#FFFFFF;'>{az['name']}</div>",
        style=f"rounded=1;fillColor={az['hdr_bg']};strokeColor=none;fontColor=#FFFFFF;align=center;verticalAlign=middle;",
        x=az['x'], y=465, w=az['w'], h=30
    )

    # Ingress Controller
    ing = add_cell(
        value=f"<div style='font-size:12px; font-weight:bold; color:#1E40AF;'>Ingress Controller</div>"
              "<div style='font-size:10px; color:#64748B;'>Nginx / ALB Ingress | Health Check: <code>GET /healthz</code></div>",
        style="rounded=1;fillColor=#F1F5F9;strokeColor=#2563EB;strokeWidth=1.5;fontColor=#0F172A;align=center;verticalAlign=middle;",
        x=az['x'] + 20, y=505, w=az['w'] - 40, h=38
    )
    az_ingress_cells.append(ing)

    # Node Group Box
    add_cell(
        value="<div style='font-size:11px; font-weight:bold; color:#475569;'>💻 Kubernetes Node Group (Compute VMs) | Autoscaling</div>",
        style="rounded=1;fillColor=#F8FAFC;strokeColor=#94A3B8;strokeWidth=1;fontColor=#0F172A;verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;",
        x=az['x'] + 20, y=555, w=az['w'] - 40, h=230
    )

    # Namespace insuretech container
    ns_box = add_cell(
        value="<div style='font-size:11px; font-weight:bold; color:#DC2626;'>Namespace: insuretech (Active-Active поды)</div>",
        style="rounded=1;fillColor=#FFFFFF;strokeColor=#DC2626;strokeWidth=1.5;dashed=1;fontColor=#991B1B;verticalAlign=top;align=center;spacingTop=4;",
        x=az['x'] + 35, y=580, w=az['w'] - 70, h=195
    )

    # 4 Pods inside namespace (Clear, short labels)
    add_cell(
        value="<div style='font-size:12px; font-weight:bold; color:#991B1B;'>core-app</div>"
              "<div style='font-size:10px; color:#475569;'>HPA: 3–10 | Витрина, тарифы, заявки</div>",
        style="rounded=1;fillColor=#FEF2F2;strokeColor=#DC2626;strokeWidth=1;fontColor=#0F172A;align=center;verticalAlign=middle;",
        x=az['x'] + 50, y=608, w=290, h=65
    )

    add_cell(
        value="<div style='font-size:12px; font-weight:bold; color:#991B1B;'>client-info</div>"
              "<div style='font-size:10px; color:#475569;'>HPA: 2–6 | Профили клиентов, ПДн</div>",
        style="rounded=1;fillColor=#FEF2F2;strokeColor=#DC2626;strokeWidth=1;fontColor=#0F172A;align=center;verticalAlign=middle;",
        x=az['x'] + 365, y=608, w=290, h=65
    )

    add_cell(
        value="<div style='font-size:12px; font-weight:bold; color:#991B1B;'>ins-product-aggregator</div>"
              "<div style='font-size:10px; color:#475569;'>Адаптер к 5 СК | Circuit Breaker</div>",
        style="rounded=1;fillColor=#FEF2F2;strokeColor=#DC2626;strokeWidth=1;fontColor=#0F172A;align=center;verticalAlign=middle;",
        x=az['x'] + 50, y=690, w=290, h=65
    )

    add_cell(
        value="<div style='font-size:12px; font-weight:bold; color:#991B1B;'>ins-comp-settlement</div>"
              "<div style='font-size:10px; color:#475569;'>Взаиморасчеты с СК (реестры полисов)</div>",
        style="rounded=1;fillColor=#FEF2F2;strokeColor=#DC2626;strokeWidth=1;fontColor=#0F172A;align=center;verticalAlign=middle;",
        x=az['x'] + 365, y=690, w=290, h=65
    )

    # Ingress -> Namespace
    add_edge(ing, ns_box, style="strokeColor=#2563EB;strokeWidth=1.5;", exit_xy=(0.5, 1), entry_xy=(0.5, 0))

    # Database Box
    db_vm = add_cell(
        value=f"<div style='font-size:13px; font-weight:bold; color:{az['db_title_color']};'>{az['db_title']}</div>"
              f"<div style='font-size:11px; color:#334155; margin-top:2px;'>{az['db_sub']}</div>",
        style=f"rounded=1;fillColor={az['db_fill']};strokeColor={az['db_stroke']};strokeWidth=1.5;fontColor=#0F172A;align=center;verticalAlign=middle;shadow=1;",
        x=az['x'] + 20, y=805, w=az['w'] - 40, h=70
    )
    az_db_cells.append(db_vm)

    # Namespace -> Database (Clean straight vertical line)
    add_edge(ns_box, db_vm, value="<b>TCP / JDBC (PgBouncer)</b>", style="strokeColor=#475569;strokeWidth=1.5;", exit_xy=(0.5, 1), entry_xy=(0.5, 0))

# Connect ALB to Ingress Controllers (Straight vertical)
for i, az in enumerate(az_configs):
    add_edge(
        alb_bar, az_ingress_cells[i],
        value="<b>/healthz &amp; Трафик</b>",
        style="strokeColor=#2563EB;strokeWidth=2;",
        exit_xy=(az['alb_anchor'], 1),
        entry_xy=(0.5, 0)
    )

# Connect Database Replications
# Master -> Sync Standby (Straight horizontal)
add_edge(
    az_db_cells[0], az_db_cells[1],
    value="<b>Sync (RPO = 0)</b>",
    style="strokeColor=#059669;strokeWidth=2.5;",
    exit_xy=(1, 0.5),
    entry_xy=(0, 0.5)
)

# Master -> Async Standby (Routed cleanly below)
add_edge(
    az_db_cells[0], az_db_cells[2],
    value="<b>Async Streaming (Read-Only)</b>",
    style="strokeColor=#2563EB;strokeWidth=1.5;dashed=1;",
    exit_xy=(0.5, 1),
    entry_xy=(0.5, 1),
    points=[(445, 930), (1955, 930)]
)

# ==================== 6. BACKUP TIER (y: 1010 to 1070) ====================
s3_box = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#166534;'>🗄️ Yandex Object Storage (S3) — Резервное копирование и Disaster Recovery</div>"
          "<div style='font-size:11px; color:#334155; margin-top:2px;'>"
          "• <b>Continuous WAL Archiving (WAL-G):</b> PITR восстановление на любую секунду (<b>RPO &le; 15 мин.</b>, факт &lt; 5 мин.)<br>"
          "• <b>Daily Base Backups:</b> ежедневные снапшоты (хранение 30 дней) | Восстановление базы 50 GB за 5–10 мин. (<b>RTO &le; 45 мин.</b>)"
          "</div>",
    style="rounded=1;fillColor=#F0FDF4;strokeColor=#16A34A;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=90, y=1010, w=2220, h=65
)

# Arrow from DB Master to S3
add_edge(
    az_db_cells[0], s3_box,
    value="<b>WAL-G &amp; Бэкапы</b>",
    style="strokeColor=#16A34A;strokeWidth=2;",
    exit_xy=(0.15, 1),
    entry_xy=(0.12, 0)
)

# ==================== 7. CONCISE ARCHITECTURAL DECISIONS (y: 1115 to 1345) ====================
callout_y = 1115
callout_h = 240
w_callout = 436
spacing = 25

c1 = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#1E40AF;'>1. Масштабирование</div>"
          "<div style='font-size:11px; color:#64748B;'>Horizontal vs Vertical</div>"
          "<hr style='border:0.5px solid #E2E8F0; margin:4px 0;'>"
          "<div style='font-size:11px; color:#1E293B; line-height:140%;'>"
          "• <b>Stateless-слой:</b> горизонтальное (Scale-Out) через K8s HPA по CPU/RAM/RPS.<br>"
          "• <b>Stateful-слой (50 GB):</b> вертикальное (Scale-Up) узлов БД + реплика на чтение.<br>"
          "• <b>Multi-AZ:</b> 3 зоны для выполнения норматива доступности <b>SLA 99.9%</b>."
          "</div>",
    style="rounded=1;fillColor=#FFFFFF;strokeColor=#2563EB;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=60, y=callout_y, w=w_callout, h=callout_h
)

c2 = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#1E40AF;'>2. K8s: Растянутый кластер</div>"
          "<div style='font-size:11px; color:#64748B;'>Конфигурация развёртывания</div>"
          "<hr style='border:0.5px solid #E2E8F0; margin:4px 0;'>"
          "<div style='font-size:11px; color:#1E293B; line-height:140%;'>"
          "• <b>Региональный Master:</b> 3 AZ, кворум etcd (SLA 99.95%), единый CI/CD.<br>"
          "• <b>topologySpreadConstraints:</b> автобалансировка подов по 3 зонам.<br>"
          "• <b>Отказ от независимых кластеров:</b> исключает риски сложного Service Mesh."
          "</div>",
    style="rounded=1;fillColor=#FFFFFF;strokeColor=#2563EB;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=60 + (w_callout + spacing), y=callout_y, w=w_callout, h=callout_h
)

c3 = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#0369A1;'>3. Балансировка и CDN</div>"
          "<div style='font-size:11px; color:#64748B;'>Регионы РФ и Health Checks</div>"
          "<hr style='border:0.5px solid #E2E8F0; margin:4px 0;'>"
          "<div style='font-size:11px; color:#1E293B; line-height:140%;'>"
          "• <b>Yandex Cloud CDN:</b> кэш статики по городам РФ &rarr; <b>TTFB &lt; 50 мс</b>.<br>"
          "• <b>L7 ALB Multi-AZ:</b> распределение динамического API-трафика.<br>"
          "• <b>Health Check:</b> опрос <code>GET /healthz</code> каждые 2с (отвод при 2 сбоях)."
          "</div>",
    style="rounded=1;fillColor=#FFFFFF;strokeColor=#0284C7;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=60 + 2 * (w_callout + spacing), y=callout_y, w=w_callout, h=callout_h
)

c4 = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#B91C1C;'>4. Отказ от шардирования</div>"
          "<div style='font-size:11px; color:#64748B;'>Обоснование для 50 GB</div>"
          "<hr style='border:0.5px solid #E2E8F0; margin:4px 0;'>"
          "<div style='font-size:11px; color:#1E293B; line-height:140%;'>"
          "• <b>Объём 50 GB:</b> легко обслуживается одним сервером PostgreSQL.<br>"
          "• <b>Без оверхеда:</b> нет 2PC, сохранены Foreign Keys и аналитика.<br>"
          "• <b>Отказоустойчивость:</b> Master + Synchronous Standby (<b>RPO = 0</b>)."
          "</div>",
    style="rounded=1;fillColor=#FFFFFF;strokeColor=#DC2626;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=60 + 3 * (w_callout + spacing), y=callout_y, w=w_callout, h=callout_h
)

c5 = add_cell(
    value="<div style='font-size:13px; font-weight:bold; color:#15803D;'>5. Фейловер (RTO / RPO)</div>"
          "<div style='font-size:11px; color:#64748B;'>RTO &le; 45 мин. | RPO &le; 15 мин.</div>"
          "<hr style='border:0.5px solid #E2E8F0; margin:4px 0;'>"
          "<div style='font-size:11px; color:#1E293B; line-height:140%;'>"
          "• <b>Сбой зоны (ЦОД):</b> ALB переключает трафик за <b>4–10 сек.</b> (RPO = 0).<br>"
          "• <b>Сбой Master БД:</b> Patroni промоутит Standby за <b>15–30 сек.</b> (RPO = 0).<br>"
          "• <b>Катастрофа:</b> восстановление 50 GB из S3 за <b>5–10 мин.</b> (&le; 45 мин.)."
          "</div>",
    style="rounded=1;fillColor=#FFFFFF;strokeColor=#16A34A;strokeWidth=1.5;fontColor=#0F172A;align=left;verticalAlign=top;spacing=10;shadow=1;",
    x=60 + 4 * (w_callout + spacing), y=callout_y, w=w_callout, h=callout_h
)

# Write output file
tree = ET.ElementTree(root)
out_path = 'Task1/InureTech_технологическая архитектура_to-be.drawio'

ET.indent(tree, space="  ", level=0)
tree.write(out_path, encoding='utf-8', xml_declaration=True)

print("Successfully regenerated with minimal, crisp text:")
print(" -", out_path)
