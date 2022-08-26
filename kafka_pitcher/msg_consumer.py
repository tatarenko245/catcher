"""
Будемо використовувати kafka-python для синхронного пітона.
Вона написана на пітоні. Вміє працювати зі старими версіями кафки (0.8)

Задача взяти вільного конcюмера та підключитися ним до топіку.
Автокоміт може перегрузить систему.
"""

import json
import os
import sqlite3
from datetime import datetime

from kafka import KafkaConsumer

from some_functions import get_project_root

topic = os.getenv("TOPIC_ID")
group = os.getenv("GROUP_ID")
host = os.getenv("HOST")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

consumer = KafkaConsumer(
    topic,
    group_id=group,
    bootstrap_servers=[host],
    security_protocol='SASL_PLAINTEXT',
    sasl_mechanism='PLAIN',
    sasl_plain_username=username,
    sasl_plain_password=password,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    heartbeat_interval_ms=500,
    request_timeout_ms=1000000000000,
    enable_auto_commit=True
)

root = get_project_root()

connection = sqlite3.connect(f"{root}/kafka_catcher/db.sqlite3")
cursor = connection.cursor()

for msg in consumer:
    date = str((datetime.today()).replace(microsecond=0))
    message = msg.value
    print("\nMESSAGE")
    print(message)

    if "X-OPERATION-ID" in message and "ocid" in message['data']:

        cursor.execute(f"""INSERT INTO goodwin_catcher_message (date_of_creation, ocid, x_operation_id, message)
                        VALUES (?,?,?,?);""", (date, message['data']['ocid'], message['X-OPERATION-ID'],
                                               json.dumps(message)))
        connection.commit()
cursor.close()
