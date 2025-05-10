# 依赖fluxdb（docker启动的）

```shell
docker pull influxdb:latest

cd /Users/shhaofu/Code/cursor-projects/influxdb-p

(translate-env) shhaofu@shhaofudeMacBook-Pro influxdb-p % tree
.
├── CREATE
└── influxdb_data

docker run -d \
  --name influxdb \
  -p 8086:8086 \
  -v influxdb_data:/var/lib/influxdb \
  influxdb:latest

```

# 产生模拟数据（每5秒钟产生3条新数据，模拟设备实时推送数据到db中）
python /Users/shhaofu/Code/cursor-projects/aka_music/backend/app/scripts/fluxdb/generate_data.py

# 启动flask服务
python app.py# p-fluxdb-web
