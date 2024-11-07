import json
import pandas as pd
from datetime import datetime, timedelta, timezone
import numpy as np
from scipy import stats
from influxdb_client import InfluxDBClient

# import itsdb
from .logger import Logger as logger

TSDB_CLIENT = None
BUCKET = None

def tsdb_init(host, port, token, org, bucket):

    global TSDB_CLIENT, BUCKET

    TSDB_CLIENT = InfluxDBClient(
        url = f"http://{host}:{port}",
        token = token,
        org = org,
        debug = False,
        timeout = 10000
    )

    BUCKET = bucket

def tsdb_disconnect():
    global TSDB_CLIENT
    if TSDB_CLIENT:
        TSDB_CLIENT.close()
        TSDB_CLIENT = None

'''
def get_sensor_list(group_code: str, id: str) -> list:
    result = []

    group_codes = ("P", "G", "S", "D")
    if group_code not in group_codes:
        return result

    if group_code == "P":
        group = "p.projectid"
    elif group_code == "G":
        group = "g.groupid"
    elif group_code == "S":
        group = "st.stid"
    elif group_code == "D":
        group = "d.deviceid"
    else:
        return result

    stmt = f"SELECT s.deviceid, CAST(IFNULL(s.channel,1) AS CHAR) AS channel \
        , d.devicetype AS device_type, tddt.data_type \
        , IF(tdc.modelname IS NOT NULL,'Y','N') AS is3axis \
        FROM tb_sensor s \
        JOIN tb_device d ON d.deviceid = s.deviceid \
        JOIN tb_structure st ON st.stid = d.stid \
        JOIN tb_group g ON g.groupid = st.groupid \
        JOIN tb_project p ON p.projectid = g.projectid \
        LEFT JOIN tb_device_data_type tddt ON d.devicetype = tddt.device_type \
        LEFT JOIN tb_device_catalog tdc ON tdc.idx = d.modelidx AND tdc.modelname IN ('SSC-320HR(2.0g)','SSC-320HR(5.0g)','SSC-320(3.0g)') \
        WHERE {group} = '{id}' \
        AND d.manageyn = 'Y' AND s.manageyn = 'Y' \
        ORDER BY p.projectid, g.groupid, st.stid, d.deviceid, s.channel;"
    query_result = itsdb.do_select(stmt)
    result = query_result
    return result
'''

def convert_to_utc(date: str):
    kst = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").astimezone(
        timezone(timedelta(hours=9))
    )
    utc = kst.astimezone(timezone(timedelta(hours=0)))
    return datetime.strftime(utc, "%Y-%m-%dT%H:%M:%S.000Z")

def query_data(id, ch, range_start, range_end, d_type, sample_count=1):

    if d_type == '1'or d_type == '3':
        add_query = f'|> filter(fn:(r) => r._field == "anal1" or r._field == "anal2")'
        data_type = 'anal'
    else:
        add_query = f'|> filter(fn:(r) => r._field == "sv" or r._field == "humidity" or r._field == "temperature")'
        data_type = 'sv'

    utc_start_time = convert_to_utc(range_start)
    utc_end_time = convert_to_utc(range_end)

    query_api = TSDB_CLIENT.query_api()

    if data_type == 'anal':
        stmt = f'from(bucket:"{BUCKET}")\
        |> range(start: {utc_start_time}, stop: {utc_end_time})\
        |> filter(fn:(r) => r._measurement == "sensor_data")\
        |> filter(fn:(r) => r.id == "{id}" and r.channel == "{ch}")\
        {add_query}\
        |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")\
        |> sample(n: {sample_count}, column: "_time")\
        |> keep(columns: ["_time","anal1","anal2"])'

    else:
        stmt = f'from(bucket:"{BUCKET}")\
        |> range(start: {utc_start_time}, stop: {utc_end_time})\
        |> filter(fn:(r) => r._measurement == "sensor_data")\
        |> filter(fn:(r) => r.id == "{id}" and r.channel == "{ch}")\
        {add_query}\
        |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")\
        |> sample(n: {sample_count}, column: "_time")\
        |> keep(columns: ["_time","sv","temperature","humidity"])'
    
    records = query_api.query(stmt)

    result = json.loads(records.to_json(indent=0))
    dataframe = pd.DataFrame(result)
    print(dataframe)

    '''
    dataframe['_time'] = pd.to_datetime(dataframe['_time'])
    dataframe['_time'] = dataframe['_time'].dt.tz_convert('Asia/Seoul')
    dataframe['_time'] = dataframe['_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    dataframe = dataframe.rename(columns={'_time': 'time'})
    dataframe['time'] = pd.to_datetime(dataframe['time'])
    '''

    dataframe['_time'] = pd.to_datetime(dataframe['_time'], errors='coerce', utc=True)
    dataframe['_time'] = dataframe['_time'].dt.tz_convert('Asia/Seoul')

    dataframe['_time'] = dataframe['_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    dataframe = dataframe.rename(columns={'_time': 'time'})
    dataframe['time'] = pd.to_datetime(dataframe['time'], format='%Y-%m-%d %H:%M:%S')

    
    dataframe = dataframe.drop(['result', 'table'], axis=1)

    print(dataframe)
   
    return dataframe

def query_data_adv(id, ch, range_start, range_end, data_interval):

    utc_start_time = convert_to_utc(range_start)
    utc_end_time = convert_to_utc(range_end)

    query_api = TSDB_CLIENT.query_api()

    stmt = f'from(bucket:"{BUCKET}")\
    |> range(start: {utc_start_time}, stop: {utc_end_time})\
    |> filter(fn:(r) => r._measurement == "sensor_data")\
    |> filter(fn:(r) => r.id == "{id}" and r.channel == "{ch}")\
    |> filter(fn:(r) => r._field != "channel")\
    |> aggregateWindow(every: {data_interval}, fn: mean, createEmpty: false)\
    |> keep(columns: ["_time","_value"])'
    
    records = query_api.query(stmt)
    result = json.loads(records.to_json(indent=0))

    dataframe = pd.DataFrame(result)

    dataframe['_time'] = pd.to_datetime(dataframe['_time'])
    dataframe['_time'] = dataframe['_time'].dt.tz_convert('Asia/Seoul')
    dataframe['_time'] = dataframe['_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    dataframe = dataframe.rename(columns={'_time': 'time', '_value': 'sv'})
    dataframe['time'] = pd.to_datetime(dataframe['time'])

    dataframe = dataframe.drop(['result', 'table'], axis=1)

    print(dataframe)
        
    return dataframe

def get_sensor_data_gw_influx(itsip, start_date_str, end_date_str, deviceid, channel, data_interval):

    date_obj_start = datetime.strptime(start_date_str, "%Y%m%d")
    formatted_start_date = date_obj_start.strftime("%Y-%m-%d %H:%M:%S")

    date_obj_end = datetime.strptime(end_date_str, "%Y%m%d")
    formatted_end_date = date_obj_end.strftime("%Y-%m-%d %H:%M:%S")

    data_interval = data_interval.lower()

    df = query_data_adv(deviceid, channel, formatted_start_date, formatted_end_date, data_interval)

    return df