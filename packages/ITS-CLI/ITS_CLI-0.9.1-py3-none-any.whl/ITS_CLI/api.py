import os
import time
import threading
import pyfiglet
import time
from tabulate import tabulate
import pandas as pd
from prettytable import PrettyTable
from datetime import datetime
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import traceback

from .logger import Logger as log
from . import config
from . import tcp_client
from . import timeseriesdb as tsdb

project_df = pd.DataFrame()
structure_df = pd.DataFrame()
USER = None
PASS = None

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False
    
def date_formatted(start_date, end_date):

    date_obj_start = datetime.strptime(start_date, "%Y%m%d %H%M%S")
    formatted_start_date = date_obj_start.strftime("%Y-%m-%d %H:%M:%S")

    date_obj_end = datetime.strptime(end_date, "%Y%m%d %H%M%S")
    formatted_end_date = date_obj_end.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_start_date, formatted_end_date

def add_failure(df, d_id, ch):
    print(d_id)
    print(type(d_id))
    print(ch)
    print(type(ch))
    new_row = pd.DataFrame({'device_id': [d_id], 'channel': [ch]})
    df = pd.concat([df, new_row], ignore_index=True)
    return df

def print_welcome_message():
    title = pyfiglet.figlet_format("Welcome to ITS", font="slant")
    description = "ITS(IoT Total Solution) is provided by SmartC&S."

    print(title)
    print(description)

def print_table(df):
    table = PrettyTable()
    table.field_names = df.columns.tolist()
    for index, row in df.iterrows():
        table.add_row(row.tolist())
    for column in table.field_names:
        table.max_width[column] = 60
    print(table)

def show_menu():
    menu = """
    Please select an option:
    1) View my project list
    2) View my structure list
    3) Query sensor data
    4) Download sensor data
    5) Exit
    """
    print(menu)

def run_demo_program():
    try:
        global project_df, structure_df, USER, PASS

        result = None
        print_welcome_message()

        config.config_load()

        server_cert = config.certfile

        ITS_CLIENT = tcp_client.TCPClient(config.SERVER_IP, config.SERVER_PORT, config.ITS_NUM, server_cert)

        client_thread = threading.Thread(target=ITS_CLIENT.receive_messages)
        client_thread.daemon = True  # This ensures the thread will exit when the main program exits
        client_thread.start()

        time.sleep(1)

        USER = input("Input your ITS User ID       : ").strip().lower()
        PASS = input("Input your ITS User Password : ").strip().lower()

        result = ITS_CLIENT.set_user_password(USER, PASS)

        print("Login....")

        result = ITS_CLIENT.message('login')

        if result['result'] != 'Success':
            print(f"Login Failed({result['msg']})")
            return
        else:
            print("Login Success")

        while True:
            show_menu()
            result = None
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                print("Viewing my project list...")
                if project_df.empty:

                    result = ITS_CLIENT.message('get_project_list')
                    if result['result'] != 'Success':
                        print(f"Login Failed({result['msg']})")
                        break
                    elif 'data' in result.keys():
                        data = result['data']
                        df = pd.DataFrame(data)
                        df.reset_index(inplace=True)
                        df['regdate'] = pd.to_datetime(df['regdate'], unit='ms', errors='coerce')
                        df['closedate'] = pd.to_datetime(df['closedate'], unit='ms', errors='coerce')

                        print_table(df)
                        project_df = df
                else:
                    print_table(project_df)
                    
            elif choice == '2':
                print("Viewing my structure list...")

                if project_df.empty:

                    result = ITS_CLIENT.message('get_project_list')
                    if result['result'] != 'Success':
                        print(f"Login Failed({result['msg']})")
                        break
                    elif 'data' in result.keys():
                        data = result['data']
                        df = pd.DataFrame(data)
                        df.reset_index(inplace=True)
                        df['regdate'] = pd.to_datetime(df['regdate'], unit='ms', errors='coerce')
                        df['closedate'] = pd.to_datetime(df['closedate'], unit='ms', errors='coerce')

                    project_df = df
                    print_table(df)

                else:
                    print_table(project_df)
                    
                user_input = input("Please enter the index of the project for which you want to check the list of structures (number): ").strip().lower()

                if user_input.isdigit():
                    project_index = int(user_input)
                    project_df['index'] = project_df['index'].astype(int)
                    matching_row = pd.DataFrame()
                    matching_row = project_df[project_df['index'] == project_index]

                    if matching_row.empty:
                        print("There is no matching project.")
                        continue
                    else:
                        result = ITS_CLIENT.message('get_structure_list', projectid= matching_row['projectid'].values[0])
                        if result['result'] != 'Success':
                            print(f"Login Failed({result['msg']})")
                            break
                        elif 'data' in result.keys():
                            data = result['data']
                            df = pd.DataFrame(data)
                            df.reset_index(inplace=True)

                            structure_df = df

                            print_table(df)

                else:
                    print("Wrong input")
                    continue

                
            elif choice == '3':
                print("Querying sensor data...")

                if project_df.empty:

                    result = ITS_CLIENT.message('get_project_list')
                    if result['result'] != 'Success':
                        print(f"Login Failed({result['msg']})")
                        break
                    elif 'data' in result.keys():
                        data = result['data']
                        df = pd.DataFrame(data)
                        df.reset_index(inplace=True)
                        df['regdate'] = pd.to_datetime(df['regdate'], unit='ms', errors='coerce')
                        df['closedate'] = pd.to_datetime(df['closedate'], unit='ms', errors='coerce')

                    project_df = df
                    print_table(df)

                else:
                    print_table(project_df)

                user_input = input("Please select the index of the project for which you want to download the sensor data (index): ").strip().lower()

                if user_input.isdigit():
                    project_index = int(user_input)
                    project_df['index'] = project_df['index'].astype(int)
                    matching_row = pd.DataFrame()
                    matching_row = project_df[project_df['index'] == project_index]

                    if matching_row.empty:
                        print("There is no matching project.")
                        continue
                    else:
                        result = ITS_CLIENT.message('get_structure_list', projectid= matching_row['projectid'].values[0])
                        if result['result'] != 'Success':
                            print(f"Login Failed({result['msg']})")
                            break
                        elif 'data' in result.keys():
                            data = result['data']
                            df = pd.DataFrame(data)
                            df.reset_index(inplace=True)

                            print_table(df)
                            structure_df = df

                        user_input = input("Please enter the index of the structure for which you want to download the sensor data (index): ").strip().lower()

                        if user_input.isdigit():
                            structure_index = int(user_input)
                            structure_df['index'] = structure_df['index'].astype(int)
                            matching_row_st = pd.DataFrame()
                            matching_row_st = structure_df[structure_df['index'] == structure_index]

                            if matching_row_st.empty:
                                print("There is no matching structure.")
                                continue
                            else:
                                while True:
                                    start_date = input("Please enter the back up start date (YYYYMMDD) : ")
                                    end_date = input("Please enter the back up end date (YYYYMMDD) : ")
                                
                                    if not is_valid_date(start_date) or not is_valid_date(end_date):
                                        print("Wrong input. Please enter the date in the format of YYYYMMDD")
                                    else:
                                        break

                                result = ITS_CLIENT.message('download_sensordata', projectid= matching_row['projectid'].values[0], structureid = matching_row_st['stid'].values[0])
                                if result['result'] != 'Success':
                                    print(f"Login Failed({result['msg']})")
                                    break
                                elif 'data' in result.keys():
                                    data = result['data']
                                    host = result['dbinfo']['host']
                                    port = result['dbinfo']['port']
                                    token = result['dbinfo']['token']
                                    org = result['dbinfo']['org']
                                    bucket = result['dbinfo']['bucket']

                                    tsdb.tsdb_init(host, port, token, org, bucket)

                                    df = pd.DataFrame(data)
                                    print(df)

                                    start_date_str = str(start_date) + " 000000"
                                    end_date_str = str(end_date) + " 235959"
                                    formatted_start_date, formatted_end_date = date_formatted(start_date_str, end_date_str)

                                    Success_Count = 0
                                    Fail_Count = 0
                                    df_failures = pd.DataFrame(columns=['device_id', 'channel'])

                                    dir_path = config.DATA_DIR
                                    if dir_path[-1] != '/':
                                        dir_path += '/'
                                    dir_path += matching_row['projectid'].values[0] + '/' + matching_row_st['stid'].values[0] + '/'

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
                                                continue
                                            else:
                                                # Sensor data를 리스트에 저장
                                                sensor_data['device_id'] = d_id
                                                sensor_data['channel'] = ch
                                                sensor_data['d_type'] = d_type

                                                # sensor_data['time'] = pd.to_datetime(sensor_data['time'])

                                                all_sensor_data.append(sensor_data)

                                                

                                                Success_Count += 1
                                        except Exception as e:
                                            log.error(f"Exception occurred: {str(e)}")
                                            Fail_Count += 1
                                            continue

                                    tsdb.tsdb_disconnect()

                                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
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

                                    

                                            # x-axis 날짜 형식을 일자 단위로 설정
                                            # ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # 하루 간격으로 레이블 표시
                                            # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 월-일 형식으로 표시
                                            # fig.autofmt_xdate(rotation=45)  # 날짜 라벨을 45도 회전하여 표시
        
                                            plt.savefig(f'{dir_path}sensor_{sensor_data["device_id"].values[0]}_{sensor_data["channel"].values[0]}.png')
                                            plt.close()
                                        except KeyError as e:
                                            log.error(f"KeyError: {str(e)} - for Device {sensor_data['device_id'].values[0]} Channel {sensor_data['channel'].values[0]}")

            elif choice == '4':
                print("Downloading sensor data...")

                if project_df.empty:

                    result = ITS_CLIENT.message('get_project_list')
                    if result['result'] != 'Success':
                        print(f"Login Failed({result['msg']})")
                        break
                    elif 'data' in result.keys():
                        data = result['data']
                        df = pd.DataFrame(data)
                        df.reset_index(inplace=True)
                        df['regdate'] = pd.to_datetime(df['regdate'], unit='ms', errors='coerce')
                        df['closedate'] = pd.to_datetime(df['closedate'], unit='ms', errors='coerce')

                    project_df = df
                    print_table(df)

                else:
                    print_table(project_df)

                user_input = input("1) Project level \n2) Structure level \nPlease select the unit for downloading sensor data: ").strip().lower()

                if user_input.isdigit():
                    data_level = int(user_input)

                    if data_level == 1:
                        if project_df.empty:
                            result = ITS_CLIENT.message('get_project_list')
                            if result['result'] != 'Success':
                                print(f"Login Failed({result['msg']})")
                                break
                            elif 'data' in result.keys():
                                data = result['data']
                                df = pd.DataFrame(data)
                                df.reset_index(inplace=True)
                                df['regdate'] = pd.to_datetime(df['regdate'], unit='ms', errors='coerce')
                                df['closedate'] = pd.to_datetime(df['closedate'], unit='ms', errors='coerce')
                            project_df = df
                            print(df)
                        else:
                            print_table(project_df)

                        user_input = input("Please select the index of the project for which you want to download the sensor data (index): ").strip().lower()

                        if user_input.isdigit():
                            project_index = int(user_input)
                            project_df['index'] = project_df['index'].astype(int)
                            matching_row = pd.DataFrame()
                            matching_row = project_df[project_df['index'] == project_index]

                            if matching_row.empty:
                                print("There is no matching project.")
                                continue
                            else:

                                while True:
                                    start_date = input("Please enter the back up start date (YYYYMMDD) : ")
                                    end_date = input("Please enter the back up end date (YYYYMMDD) : ")
                                
                                    if not is_valid_date(start_date) or not is_valid_date(end_date):
                                        print("Wrong input. Please enter the date in the format of YYYYMMDD")
                                    else:
                                        break
                                
                                result = ITS_CLIENT.message('download_sensordata', projectid= matching_row['projectid'].values[0])
                                if result['result'] != 'Success':
                                    print(f"Login Failed({result['msg']})")
                                    break
                                elif 'data' in result.keys():
                                    data = result['data']
                                    host = result['dbinfo']['host']
                                    port = result['dbinfo']['port']
                                    token = result['dbinfo']['token']
                                    org = result['dbinfo']['org']
                                    bucket = result['dbinfo']['bucket']

                                    tsdb.tsdb_init(host, port, token, org, bucket)

                                    df = pd.DataFrame(data)
                                    print(df)

                                    start_date_str = str(start_date) + " 000000"
                                    end_date_str = str(end_date) + " 235959"
                                    formatted_start_date, formatted_end_date = date_formatted(start_date_str, end_date_str)

                                    Success_Count = 0
                                    Fail_Count = 0
                                    df_failures = pd.DataFrame(columns=['device_id', 'channel'])

                                    dir_path = config.DATA_DIR
                                    if dir_path[-1] != '/':
                                        dir_path += '/'
                                    dir_path += matching_row['projectid'].values[0] + '/'

                                    if not os.path.isdir(dir_path):
                                        os.makedirs(dir_path)

                                    df.reset_index(drop=True, inplace=True)

                                    for index, row in df.iterrows():
                                        try:
                                            print(f"Querying sensor data : {index + 1} / {df.shape[0]}")
                                            print(f"Success: {Success_Count} / Fail: {Fail_Count}")
                                            d_id, ch, d_type, data_type, is3axis = row

                                            sensor_data = tsdb.query_data(d_id, ch, formatted_start_date, formatted_end_date, d_type, sample_count = 1)
                                            if sensor_data.empty:
                                                print(f"Empty Data: {d_id} {ch}")
                                                df_failures = add_failure(df_failures, str(d_id), str(ch))
                                                Fail_Count += 1
                                                continue
                                            else:
                                                filename = dir_path + str(d_id) + '_' + str(ch) + '.csv'
                                                sensor_data.to_csv(filename, encoding='utf-8-sig', index=False)
                                                Success_Count += 1
                                        except Exception as e:
                                            print(e)
                                            df_failures = add_failure(df_failures, str(d_id), str(ch))
                                            Fail_Count += 1
                                            continue

                                    tsdb.tsdb_disconnect()

                                    failure_filename = dir_path + 'failures.csv'
                                    df_failures.to_csv(failure_filename, encoding='utf-8-sig', index=False)

                                    if 'device_info' in result.keys():
                                        device_info = result['device_info']
                                        print(device_info)
                                        df_device_info = pd.DataFrame(json.loads(device_info))

                                        device_filename = dir_path + 'device_info.csv'
                                        df_device_info.to_csv(device_filename, encoding='utf-8-sig', index=False)


                        else:
                            print("Wrong input")
                            continue

                    elif data_level == 2:

                        print_table(project_df)

                        user_input = input("Enter the index of the project where the structure for which you want to download data exists (index): ").strip().lower()

                        if user_input.isdigit():
                            project_index = int(user_input)
                            
                            project_df['index'] = project_df['index'].astype(int)
                            matching_row = pd.DataFrame()
                            matching_row = project_df[project_df['index'] == project_index]

                            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                            print("project")
                            print(user_input)
                            print(project_index)
                            print(matching_row)
                            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                            if matching_row.empty:
                                print("There is no matching project.")
                                continue
                            else:
                                result = ITS_CLIENT.message('get_structure_list', projectid= matching_row['projectid'].values[0])
                                if result['result'] != 'Success':
                                    print(f"Login Failed({result['msg']})")
                                    break
                                elif 'data' in result.keys():
                                    data = result['data']
                                    df = pd.DataFrame(data)
                                    df.reset_index(inplace=True)

                                    print_table(df)
                                    structure_df = df

                                user_input = input("Please enter the index of the structure for which you want to download the sensor data (index): ").strip().lower()

                                if user_input.isdigit():
                                    structure_index = int(user_input)
                                    structure_df['index'] = structure_df['index'].astype(int)
                                    matching_row_st = pd.DataFrame()
                                    matching_row_st = structure_df[structure_df['index'] == structure_index]

                                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                                    print("structure")
                                    print(user_input)
                                    print(structure_index)
                                    print(matching_row_st)
                                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

                                    if matching_row_st.empty:
                                        print("There is no matching structure.")
                                        continue
                                    else:
                                        while True:
                                            start_date = input("Please enter the back up start date (YYYYMMDD) : ")
                                            end_date = input("Please enter the back up end date (YYYYMMDD) : ")
                                        
                                            if not is_valid_date(start_date) or not is_valid_date(end_date):
                                                print("Wrong input. Please enter the date in the format of YYYYMMDD")
                                            else:
                                                break

                                        result = ITS_CLIENT.message('download_sensordata', projectid= matching_row['projectid'].values[0], structureid = matching_row_st['stid'].values[0])
                                        if result['result'] != 'Success':
                                            print(f"Login Failed({result['msg']})")
                                            break
                                        elif 'data' in result.keys():
                                            data = result['data']
                                            host = result['dbinfo']['host']
                                            port = result['dbinfo']['port']
                                            token = result['dbinfo']['token']
                                            org = result['dbinfo']['org']
                                            bucket = result['dbinfo']['bucket']

                                            tsdb.tsdb_init(host, port, token, org, bucket)

                                            df = pd.DataFrame(data)
                                            print(df)

                                            start_date_str = str(start_date) + " 000000"
                                            end_date_str = str(end_date) + " 235959"
                                            formatted_start_date, formatted_end_date = date_formatted(start_date_str, end_date_str)

                                            Success_Count = 0
                                            Fail_Count = 0
                                            df_failures = pd.DataFrame(columns=['device_id', 'channel'])

                                            dir_path = config.DATA_DIR
                                            if dir_path[-1] != '/':
                                                dir_path += '/'
                                            dir_path += matching_row['projectid'].values[0] + '/' + matching_row_st['stid'].values[0] + '/'

                                            if not os.path.isdir(dir_path):
                                                os.makedirs(dir_path)

                                            df.reset_index(drop=True, inplace=True)

                                            for index, row in df.iterrows():
                                                try:
                                                    print(f"Querying sensor data : {index + 1} / {df.shape[0]}")
                                                    print(f"Success: {Success_Count} / Fail: {Fail_Count}")
                                                    d_id, ch, d_type, data_type, is3axis = row

                                                    sensor_data = tsdb.query_data(d_id, ch, formatted_start_date, formatted_end_date, d_type, sample_count = 1)
                                                    if sensor_data.empty:
                                                        print(f"Empty Data: {d_id} {ch}")
                                                        df_failures = add_failure(df_failures, str(d_id), str(ch))
                                                        Fail_Count += 1
                                                        continue
                                                    else:
                                                        filename = dir_path + str(d_id) + '_' + str(ch) + '.csv'
                                                        sensor_data.to_csv(filename, encoding='utf-8-sig', index=False)
                                                        Success_Count += 1
                                                except Exception as e:
                                                    print(e)
                                                    df_failures = add_failure(df_failures, str(d_id), str(ch))
                                                    Fail_Count += 1
                                                    continue

                                            tsdb.tsdb_disconnect()

                                            failure_filename = dir_path + 'failures.csv'
                                            df_failures.to_csv(failure_filename, encoding='utf-8-sig', index=False)

                                            if 'device_info' in result.keys():
                                                device_info = result['device_info']
                                                print(device_info)
                                                df_device_info = pd.DataFrame(json.loads(device_info))

                                                device_filename = dir_path + 'device_info.csv'
                                                df_device_info.to_csv(device_filename, encoding='utf-8-sig', index=False)


                        else:
                            print("Wrong input")
                            continue

                    else:
                        print("Wrong Number")
                        continue

                else:
                    print("Wrong input")
                    continue

            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
            time.sleep(1)

    except Exception as e:
        log.error(str(e))
        print(traceback.format_exc())


if __name__ == '__main__':

    run_demo_program()

    print("Exiting the program. Goodbye!")
