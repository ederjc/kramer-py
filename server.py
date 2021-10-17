#!/usr/bin/env python3
# -*- coding: utf8 -*-

import paho.mqtt.client as mqtt
import kramer
from time import sleep
import internal

# Set up logging
import logging
logging.basicConfig(level=logging.WARNING, filename="server.log", format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

logger.info("Starting Kramer controller server...")

kramer = kramer.Kramer_switch(internal.KRAMER_DEVICE_IP, internal.KRAMER_DEVICE_PORT, internal.KRAMER_DEVICE_ID)

def mqtt_on_connect(client, userdata, flags, rc):
    logger.info( "Connected to broker with result code " + str(rc) )
    mqttc.subscribe(internal.KRAMER_CONTROL_TOPIC + "/#", 2)

def mqtt_on_message(client, userdata, message):
    logger.info( "Received MQTT message.\nTopic: " + str(message.topic) + "\nPayload: " + str(message.payload))
    parse_mqtt_message(message.topic, message.payload)

def parse_mqtt_message( mqtt_topic, message ):
    mqtt_topic = str(mqtt_topic)
    if internal.KRAMER_CONTROL_TOPIC in mqtt_topic:
        logger.debug("Parsing message as input switch command.")
        out_port = mqtt_topic.split('/')[-1]
        in_port = message.decode('utf-8')
        logger.debug("Switch output " + str(out_port) + " to input " + str(in_port))
        kramer.setVideoSwitchState(in_port, out_port)
        return 1
    else:
        logger.error("Could not find suitable way to parse message in topic " + mqtt_topic)
        return False

mqttc = mqtt.Client()

mqttc.on_connect = mqtt_on_connect
mqttc.on_message = mqtt_on_message

mqttc.connect(internal.MQTT_BROKER_IP)
mqttc.loop_start()

while True:
    sleep(1)
