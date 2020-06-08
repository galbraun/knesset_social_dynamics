import pyodata
import requests

# https://github.com/SAP/python-pyodata/issues/83

SERVICE_URL = "http://knesset.gov.il/Odata/ParliamentInfo.svc/"

client = pyodata.Client(SERVICE_URL, requests.Session())

client.entity_sets.KNS_Position.get_entities().count().execute()

request = client.entity_sets.KNS_Position.get_entities()
for pos in request.execute():
    print(pos)
