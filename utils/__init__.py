#coding=utf-8


import uuid

def generate_uuid4():
    return str(uuid.uuid4()).replace('-', '') 


