import os
import socket
import threading
import time
from configparser import ConfigParser
import json
import ssl
import pandas as pd
import matplotlib.pyplot as plt

from . import api
from . import timeseriesdb as tsdb
from .logger import Logger as log
from . import config

class TCPClient:
    def __init__(self, host, port, its, server_cert):
        self.host = host
        self.port = port
        self.its = its
        self.user = None
        self.password = None
        self.client_socket = None
        self.connected = False
        self.result = False  # 로그인 성공 여부 플래그
        self.response = None
        self.msg = None
        self.server_cert = server_cert

    def set_user_password(self, user, password):
        self.user = user
        self.password = password

        return

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(self.server_cert)

        try:
            wrapped_socket = context.wrap_socket(self.client_socket, server_hostname=self.host)
            wrapped_socket.connect((self.host, self.port))
            self.client_socket = wrapped_socket
            self.connected = True
            print(f"Connected to {self.host}:{self.port} with SSL/TLS")
        except socket.error as e:
            print(f"Unable to connect to server: {e}")
            self.connected = False
        '''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to {self.host}:{self.port}")
        except socket.error as e:
            print(f"Unable to connect to server: {e}")
            self.connected = False
        '''
    def receive_messages(self):
        incomplete_data = ""  # 누적된 데이터를 저장할 변수

        while True:
            if not self.connected:
                self.connect()
                if not self.connected:
                    time.sleep(5)
                    continue

            try:
                while self.connected:
                    response = self.client_socket.recv(81920).decode()
                    if not response:
                        break

                    # 누적된 데이터에 새로 받은 데이터를 추가
                    incomplete_data += response

                    while True:
                        try:
                            # 누적된 데이터를 JSON으로 변환
                            response_dict = json.loads(incomplete_data)
                            
                            # JSON 변환에 성공하면 누적된 데이터를 비우고 처리
                            incomplete_data = ""

                            if 'data' in response_dict:
                                response_dict['data'] = json.loads(response_dict['data'])
                            self.message_parser(response_dict)

                        except json.JSONDecodeError:
                            # JSON 변환에 실패하면 더 많은 데이터가 필요하므로 루프를 벗어남
                            break

            except socket.error as e:
                log.error(f"Error receiving data: {e}")
            finally:
                self.connected = False
                self.disconnect()
    '''
    def receive_messages(self):
        while True:
            if not self.connected:
                self.connect()
                if not self.connected:
                    time.sleep(5)
                    continue
            try:
                while self.connected:
                    response = self.client_socket.recv(4096).decode()
                    if not response:
                        break
                    # log.info(f"Received: {response}")
                    try:
                        response_dict = json.loads(response)
                        if 'data' in response_dict:
                            response_dict['data'] = json.loads(response_dict['data'])
                        self.message_parser(response_dict)
                    except json.JSONDecodeError:
                        log.error("Failed to decode JSON response")
            except socket.error as e:
                log.error(f"Error receiving data: {e}")
            finally:
                self.connected = False
                self.disconnect()
    '''
    def send_message(self, message):
        if not self.connected:
            return
        try:
            self.client_socket.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def message(self, command, projectid = None, structureid = None):
        if command.lower() == 'login':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password
            }
        elif command.lower() == 'get_project_list':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password
            }

        elif command.lower() == 'get_structure_list':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "projectid": projectid
            }

        elif command.lower() == 'get_project_structure_list':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password
            }

        elif command.lower() == 'download_sensordata':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "projectid": projectid,
                "structureid": structureid
            }

        else:
            response = {}
            response['result'] = 'Fail'
            response['msg'] = 'not defined command'
            return response

        # elif command.lower() == 'download_sensordata':
        #     message = {
        #         "command": command,
        #         "its": self.its,
        #         "user": self.user,
        #         "password": self.password,
        #         "projectid": projectid,
        #         "structureid": structureid
        #     }

        send_message = json.dumps(message)

        try:
            response = self.send_and_wait_for_response(send_message)
            return response
        except socket.error as e:
            print(f"Error sending data: {e}")
            response = {}
            response['result'] = 'Fail'
            response['msg'] = str(e)
            return
        
    def message_getdata(self, command, start_date, end_date, projectid = None, structureid = None):
        if command.lower() == 'download_sensordata':
            message = {
                "command": command,
                "its": self.its,
                "user": self.user,
                "password": self.password,
                "projectid": projectid,
                "structureid": structureid
            }

        send_message = json.dumps(message)

        try:
            response = self.send_and_wait_for_response(send_message)

            print(response)

            if response['result'] != 'Success':
                print(f"Login Failed({response['msg']})")
                return response
            elif 'data' in response.keys():
                data = response['data']
                host = response['dbinfo']['host']
                port = response['dbinfo']['port']
                token = response['dbinfo']['token']
                org = response['dbinfo']['org']
                bucket = response['dbinfo']['bucket']

                tsdb.tsdb_init(host, port, token, org, bucket)

                df = pd.DataFrame(data)
                print(df)

                start_date_str = str(start_date) + " 000000"
                end_date_str = str(end_date) + " 235959"
                formatted_start_date, formatted_end_date = api.date_formatted(start_date_str, end_date_str)

                Success_Count = 0
                Fail_Count = 0
                df_failures = pd.DataFrame(columns=['device_id', 'channel'])

                dir_path = config.DATA_DIR
                if dir_path[-1] != '/':
                    dir_path += '/'
                if projectid != None and structureid != None:
                    dir_path += projectid + '/' + structureid + '/'
                elif projectid == None and structureid != None:
                    dir_path += structureid + '/'
                elif projectid != None and structureid == None:
                    dir_path += projectid + '/'
                else:
                    response = {}
                    response['result'] = 'Fail'
                    response['msg'] = 'input projectid or structureid'
                    return response

                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path)

                df.reset_index(drop=True, inplace=True)

                all_sensor_data = []

                for index, row in df.iterrows():
                    try:
                        print(f"Querying sensor data : {index + 1} / {df.shape[0]}")
                        print(f"Success: {Success_Count} / Fail: {Fail_Count}")
                        d_id, ch, d_type, data_type, is3axis = row

                        sensor_data = tsdb.query_data(d_id, ch, formatted_start_date, formatted_end_date, d_type, sample_count=1)
                        if sensor_data.empty:
                            print(f"Empty Data: {d_id} {ch}")
                            Fail_Count += 1
                            df_failures = api.add_failure(df_failures, str(d_id), str(ch))
                            continue
                        else:
                            # Sensor data를 리스트에 저장
                            sensor_data['device_id'] = d_id
                            sensor_data['channel'] = ch
                            sensor_data['d_type'] = d_type

                            # sensor_data['time'] = pd.to_datetime(sensor_data['time'])

                            all_sensor_data.append(sensor_data)
                            filename = dir_path + str(d_id) + '_' + str(ch) + '.csv'
                            sensor_data.to_csv(filename, encoding='utf-8-sig', index=False)

                            Success_Count += 1
                    except Exception as e:
                        log.error(f"Exception occurred: {str(e)}")
                        df_failures = api.add_failure(df_failures, str(d_id), str(ch))
                        Fail_Count += 1
                        continue

                failure_filename = dir_path + 'failures.csv'
                df_failures.to_csv(failure_filename, encoding='utf-8-sig', index=False)

                if 'device_info' in response.keys():
                    device_info = response['device_info']
                    print(device_info)
                    df_device_info = pd.DataFrame(json.loads(device_info))

                    device_filename = dir_path + 'device_info.csv'
                    df_device_info.to_csv(device_filename, encoding='utf-8-sig', index=False)

                # 각 센서 데이터를 개별 플롯으로 저장
                for sensor_data in all_sensor_data:
                    fig, ax = plt.subplots(figsize=(15, 10))
                    d_type = sensor_data['d_type'].values[0]
                    try:
                        if d_type == '1' or d_type == '3':
                            ax.plot(sensor_data['time'], sensor_data['anal1'], label=f"Device {sensor_data['device_id'].values[0]} Channel {sensor_data['channel'].values[0]} anal1")
                            ax.plot(sensor_data['time'], sensor_data['anal2'], label=f"Device {sensor_data['device_id'].values[0]} Channel {sensor_data['channel'].values[0]} anal2")
                        else:
                            # plt.plot(sensor_data['time'], sensor_data['humidity'], label=f"Device {sensor_data['device_id'].values[0]} Channel {sensor_data['channel'].values[0]} humidity")
                            ax.plot(sensor_data['time'], sensor_data['sv'], label=f"Device {sensor_data['device_id'].values[0]} Channel {sensor_data['channel'].values[0]} sv")
                            # plt.plot(sensor_data['time'], sensor_data['temperature'], label=f"Device {sensor_data['device_id'].values[0]} Channel {sensor_data['channel'].values[0]} temperature")
                        
                        ax.set_title(f'Sensor Data for Device {sensor_data["device_id"].values[0]} Channel {sensor_data["channel"].values[0]}')
                        ax.set_xlabel('Time')
                        ax.set_ylabel('Value')
                        ax.legend()
                        ax.grid(True)

                        plt.savefig(f'{dir_path}sensor_{sensor_data["device_id"].values[0]}_{sensor_data["channel"].values[0]}.png')
                        plt.close()
                    except KeyError as e:
                        log.error(f"KeyError: {str(e)} - for Device {sensor_data['device_id'].values[0]} Channel {sensor_data['channel'].values[0]}")

            tsdb.tsdb_disconnect()

            return response
        except socket.error as e:
            print(f"Error sending data: {e}")
            response = {}
            response['result'] = 'Fail'
            response['msg'] = str(e)
            tsdb.tsdb_disconnect()
            return

    def login(self):
        # if not self.connected:
        #     print("Server is not connected")
        #     return
        
        message = {
            "command": "login",
            "its": self.its,
            "user": self.user,
            "password": self.password
        }

        send_message = json.dumps(message)

        try:
            response = self.send_and_wait_for_response(send_message)
            return response
        except socket.error as e:
            print(f"Error sending data: {e}")

    def disconnect(self):
        self.client_socket.close()
        self.connected = False
        print("Connection closed.")

    def get_connect_status(self):
        return self.connected

    def get_login_status(self):
        return self.result
    
    def get_error_message(self):
        return self.msg
    
    def message_parser(self, response_dict):

        if response_dict.get("result") == "Success":
            self.result = True
        else:
            self.result = False
            
        self.response = response_dict

    def send_and_wait_for_response(self, message):
        self.response = None  # 이전 응답 초기화
        self.send_message(message)
        # 응답 대기
        while self.response is None:
            time.sleep(0.1)
        return self.response


'''
import socket
import threading
import time
from configparser import ConfigParser
import json

from logger import Logger as log

class TCPClient:
    def __init__(self, host, port, its, user, password):
        self.host = host
        self.port = port
        self.its = its
        self.user = user
        self.password = password
        self.client_socket = None
        self.connected = False

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to {self.host}:{self.port}")
        except socket.error as e:
            print(f"Unable to connect to server: {e}")
            self.connected = False

    def receive_messages(self):
        while True:
            if not self.connected:
                self.connect()
                if not self.connected:
                    time.sleep(5)
                    continue
            try:
                while self.connected:
                    response = self.client_socket.recv(1024).decode()
                    if not response:
                        break
                    log.info(f"Received: {response}")
                    response_dict = json.loads(response)
                    message_parser(response_dict)
            except socket.error as e:
                log.error(f"Error receiving data: {e}")
            finally:
                self.connected = False
                self.disconnect()

    def send_message(self, message):
        if not self.connected:
            return
        try:
            self.client_socket.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def login(self):
        if not self.connected:
            print("Server is not connected")
            return
        
        message = {
            "command" : "login",
            "its" : self.its,
            "user" : self.user,
            "password" : self.password
        }

        send_message = json.dumps(message)

        try:
            self.send_message(send_message)
        except socket.error as e:
            print(f"Error sending data: {e}")

    def disconnect(self):
        self.client_socket.close()
        self.connected = False
        print("Connection closed.")

    def get_connect_status(self):
        return self.connected
    
def message_parser(response_dict):

    print(response_dict)
'''