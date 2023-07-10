import requests, json



url = "http://192.168.1.50:18086/api/v2/query?org=wolke"

payload = "import \"date\" \nmonth = date.truncate(t: now(), unit: 1mo)\nfrom(bucket: \"WeatherPi\")\n  |> range(start: month)\n  |> filter(fn: (r) => r[\"_measurement\"] == \"rain\")\n  |> filter(fn: (r) => r[\"_field\"] == \"volume\")\n  |> aggregateWindow(every: 1mo, fn: sum, createEmpty: false)\n  |> yield(name: \"sum\")"
headers = {
  'Authorization': 'Token eydsJXziy1z2b1blt-7uqBHxW-s44mQxG10YyzNvJTMfsBLbvLMnKtTCbsKJjxZWcJkhq0uxIvuKpOCbPqcTEQ==',
  'Accept': 'application/csv',
  'Content-Type': 'application/vnd.flux'
}

response = requests.post(url, headers=headers, data=payload, proxies={})

if "volume,rain,gauge" in response.text:
    print(response.text)

    lines = response.text.split('\n')

    for line in lines:
        if "volume,rain,gauge" in line:
            rainvolume = round(float(line.split(',')[6]),1)
            print(rainvolume)
