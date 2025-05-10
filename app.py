from flask import Flask, render_template, jsonify
from influxdb_client import InfluxDBClient, QueryApi
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# 连接 InfluxDB
client = InfluxDBClient(
    url="http://localhost:8086",
    token="iXKclTXCS-sTHoP2QgUt--UtVbJHog9bs5zjYgD16uNozmD36cDvuwUH_tWQ_F9CAfhh6QmiryV31hSPtuD_3g==",
    org="csd"
)
bucket = "csd"
query_api = client.query_api()

@app.route('/')
def index():
    # 查询最近10分钟的实时人流数据
    query = f'''
    from(bucket: "csd")
      |> range(start: -1m)
      |> filter(fn: (r) => r._measurement == "exhibition_traffic")
    '''
    tables = query_api.query(query)
    
    data = []
    for table in tables:
        for record in table.records:
            data.append({
                "exhibition_id": record["exhibition_id"],
                "location": record["location"],
                "current_people": record.get_value(),
                "time": record.get_time()
            })
    
    return render_template('index.html', data=data)

@app.route('/api/traffic_data')
def get_traffic_data():
    # 查询最近1分钟的实时人流数据
    query = f'''
    from(bucket: "csd")
      |> range(start: -1m)
      |> filter(fn: (r) => r._measurement == "exhibition_traffic")
    '''
    tables = query_api.query(query)
    
    data = []
    for table in tables:
        for record in table.records:
            data.append({
                "exhibition_id": record["exhibition_id"],
                "location": record["location"],
                "current_people": record.get_value(),
                "time": record.get_time().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
