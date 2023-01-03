import json

sensorID = 'abc'
val = 9.6
ts = '2022-09-29T8'
payload = {"value": f"{val}", "createdAt": f"{ts}"}
data = f'{sensorID}, {json.dumps(payload)}'

print(payload)
print(data)