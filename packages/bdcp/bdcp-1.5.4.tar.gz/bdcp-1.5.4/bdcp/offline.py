#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import sys
import pymysql
import pandas as pd
import paramiko
import re
import os
import platform
import configparser

class Offline:

    def __init__(self, host='', passwd='', match_id=''):
        self.host = host
        self.passwd = passwd
        self.match_id = match_id

    def setvar(self, host_str):
        """
        hostname, host, public_ip, passwd
        """
        command = "echo {} >> /usr/etx.txt".format(host_str)
        # 执行远程命令
        out, err = self.exec(command=command)

    def setbasic(self, is_single=True):
        """
        登录主机后的基本操作
        """
        # 执行远程命令
        if not is_single:
            # print("{}-cluster".format(resource_name))
            download_command = "curl -o /etc/profile.d/my.sh -O -L https://gitee.com/yiluohan1234/vagrant_bigdata_cluster/raw/master/resources/bdcompetition/cluster.sh"
            out, err = self.exec(command=download_command)
            out, err = self.exec(command="source /etc/profile")
            out, err = self.exec(command="setvar")
            # 设置ip
            out, err = self.exec(command='source /etc/profile && setip')
        else:
            # print("{}-single".format(resource_name))
            download_command = "curl -o /etc/profile.d/my.sh -O -L https://gitee.com/yiluohan1234/vagrant_bigdata_cluster/raw/master/resources/bdcompetition/single.sh && source /etc/profile"
            out, err = self.exec(command=download_command)

        print("setbasic success!")

    def setenvbasic(self, is_single=True):
        """
        登录主机后的基本操作
        """
        # 远程执行setvar
        import bdcp
        package_path = os.path.dirname(bdcp.__file__)
        if platform.system() == 'Windows':
            cluster_file = package_path + '\sh\cluster.sh'
            single_file = package_path + '\sh\single.sh'
        else:
            cluster_file = package_path + '/sh/cluster.sh'
            single_file = package_path + '/sh/single.sh'

        if not is_single:
            # print("{}-cluster".format(resource_name))
            self.upload(cluster_file, '/etc/profile.d/my.sh')
            out, err = self.exec(command="source /etc/profile")
            out, err = self.exec(command="setvar")
            # 设置ip
            out, err = self.exec(command='source /etc/profile && setip')
        else:
            # print("{}-single".format(resource_name))
            self.upload(single_file, '/etc/profile.d/my.sh')
            out, err = self.exec(command="source /etc/profile")

        print("setbasic success!")

    def exec(self, command):
        """
        远程执行命令
        """
        hostname = self.host
        port = '22'
        username = 'root'
        password = self.passwd
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=port, username=username, password=password)

            stdin, stdout, stderr = ssh.exec_command(command)
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            ssh.close()
        return out, err

    def check(self, verbose=True, inplace=True):
        """
        获取远程的日志文件内容
        """
        import bdcp
        package_path = os.path.dirname(bdcp.__file__)
        if platform.system() == 'Windows':
            demo_file = package_path + '\sql\demo.h5'
        else:
            demo_file = package_path + '/sql/demo.h5'
        hostname = self.host
        port = 22
        username = 'root'
        password = self.passwd
        out, err = self.exec(command="echo $(ps -ef | grep aliyun-assist | grep aliyun-service | grep -v grep | awk '{print $8}'|xargs dirname)/log/aliyun_assist_main.log")
        file = out.replace('\n', '')

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(hostname, port, username, password)
            sftp_client = client.open_sftp()
            remote_file = sftp_client.open(file, "r")
            file_content = remote_file.readlines()
            lines = [line for line in file_content if "/luban/api/v1/task/finish" in line]
            ret_list = []
            for line in lines:
                line_str = line.replace("\\", "")
                json_match = re.search(r'{\s*"status":\s*(-?\d+),\s*"message":\s*".*?"\s*}', line_str)
                if json_match:
                    status_json = json_match.group(0)
                    status_data = json.loads(status_json)
                    ret_list.append(status_data)
            # 去除无用信息并过滤空字典
            filtered_list = [{k: v for k, v in ret_data.items() if k not in ["status", "message"]} for ret_data in ret_list]


            if not os.path.exists('./md/{}'.format(self.match_id)):
                # 目录不存在，创建目录
                os.makedirs('./md/{}'.format(self.match_id))

            # 将数据进行转换
            if verbose and len(filtered_list) > 0:
                for ret_data in filtered_list:
                    if 'command' in ret_data:
                        command = ret_data["command"]
                        if command.strip().startswith("cat"):
                            file_name = ret_data["command"].split()[1].strip()
                            greps = [word.split()[-1] for word in command.split("|")[1:] if word.strip().startswith("grep")]
                            grep_string = ",".join(greps) if len(greps) > 0 else ''
                            keyword = ',' + ret_data['keyword'] if 'keyword' in ret_data else ''
                            str_string = ',' + ret_data['strs'] if 'strs' in ret_data else ''
                            file_path = '/'.join(file_name.split('/')[:-1])
                            ret_data['exec'] = "[ ! -d {} ] && mkdir -p {}; echo '{}{}{}' >> {}".format(file_path, file_path, grep_string, keyword, str_string, file_name)

                        if command.strip().startswith("head"):
                            file_name = ret_data["command"].split()[3].strip()
                            greps = [word.split()[-1] for word in command.split("|")[1:] if word.strip().startswith("grep")]
                            grep_string = ",".join(greps) if len(greps) > 0 else ''
                            keyword = ',' + ret_data['keyword'] if 'keyword' in ret_data else ''
                            str_string = ',' + ret_data['strs'] if 'strs' in ret_data else ''
                            file_path = '/'.join(file_name.split('/')[:-1])
                            ret_data['exec'] = "[ ! -d {} ] && mkdir -p {}; echo '{}{}{}' >> {}".format(file_path, file_path, grep_string, keyword, str_string, file_name)

                        if command.strip().startswith("grep"):
                            file_name = ret_data["command"].split()[2].strip()
                            command_key = ret_data["command"].split()[1].strip()
                            greps = [word.split()[-1] for word in command.split("|")[1:] if word.strip().startswith("grep")]
                            grep_string = ',' + ",".join(greps) if len(greps) > 0 else ''
                            keyword = ',' + ret_data['keyword'] if 'keyword' in ret_data else ''
                            str_string = ',' + ret_data['strs'] if 'strs' in ret_data else ''
                            file_path = '/'.join(file_name.split('/')[:-1])
                            ret_data['exec'] = "[ ! -d {} ] && mkdir -p {}; echo '{}{}{}{}' >> {}".format(file_path, file_path, command_key, grep_string, keyword, str_string, file_name)

                        if command.strip().startswith("file"):
                            if ret_data['keyword'] == 'Hierarchical Data Format':
                                file_name = command.split()[1]
                                download_command = "curl -o {} -O -L https://gitee.com/yiluohan1234/vagrant_bigdata_cluster/raw/master/resources/bdcompetition/demo.h5".format(file_name)
                                # out, err = self.exec(command=download_command)
                                self.upload(demo_file, file_name)
                            else:
                                path_name = ret_data["command"].split()[1].strip()
                                keyword = ret_data['keyword'] if 'keyword' in ret_data else ''
                                str_string = ',' + ret_data['strs'] if 'strs' in ret_data else ''
                                ret_data['exec'] = "echo '{}{}' >> {}".format(keyword, str_string, path_name)

                        if command.strip().startswith("ls"):
                            dir_path = ret_data["command"].split()[1].strip()
                            keyword = ret_data['keyword'] if 'keyword' in ret_data else ''
                            str_string = '-' + ret_data['strs'] if 'strs' in ret_data else ''
                            file_name = dir_path + '/demo.' + keyword +  str_string
                            ret_data['exec'] = "touch {} ".format(file_name)
                    else:
                        if 'file' in ret_data:
                            str_string = ret_data['strs'] if 'strs' in ret_data else ''
                            ret_data['exec'] = "echo '{}' >> {}".format(str_string, ret_data['file'])
                        elif 'directory' in ret_data:
                            dir_path = ret_data['directory']
                            ret_data['exec'] = "mkdir -p {}".format(dir_path)

            # 节省时间，仅执行最新的命令
            # if inplace and len(filtered_list) > 0 and 'exec' in filtered_list[-1]:
            #     self.exec(resource_name=resource_name, command=filtered_list[-1]['exec'])
            if inplace:
                file_path = './md/{}/exec.txt'.format(self.match_id)
                lines_set = {line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines()} if os.path.exists(file_path) else set()

                for ret in filtered_list[-3:]:
                    if 'exec' in ret and ret['exec'] not in lines_set:
                        self.exec(command=ret['exec'])
                        with open(file_path, 'a+', encoding='utf-8') as file:
                            file.write(ret['exec'] + "\n")

            # 去重
            distinct_list = []
            for ret in filtered_list:
                if ret not in distinct_list:
                    distinct_list.append(ret)

            # 打印倒数3个JSON数据
            if len(filtered_list) > 0:
                for data in filtered_list[-3:]:
                    print(data)

            # 保存
            with open('./md/{}/{}.json'.format(self.match_id, self.host), 'w', encoding='utf-8') as f:
                json.dump(distinct_list, f, ensure_ascii=False, indent=4)

        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            remote_file.close()
            client.close()

    def hostname(self, host, hostname):
        ip = host
        if platform.system() == 'Windows':
            host_file = "C:/Windows/System32/drivers/etc/HOSTS"
        else:
            host_file = "/etc/hosts"

        with open(host_file, "r") as file:
            current_hosts_content = file.readlines()

        new_hosts_content = [line for line in current_hosts_content if not line.strip().endswith(hostname)]

        new_hosts_content.append("{} {}\n".format(ip, hostname))

        with open(host_file, "w") as file:
            file.writelines(new_hosts_content)

    def upload(self, local_file_path, remote_file_path):
        """
        获取远程的日志文件内容
        """
        hostname = self.host
        port = 22
        username = 'root'
        password = self.passwd
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port, username, password)
            sftp = client.open_sftp()
            # 上传本地文件到远程服务器
            # 报错Failure：sftp.put("/tmp/xx.py", "/tmp/xx.py")
            sftp.put(local_file_path, remote_file_path)
        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            sftp.close()
            client.close()

    def download(self, remote_file):
        """
        获取远程的日志文件内容
        """
        local_dir = './download/{}/'.format(self.match_id)
        if not os.path.exists(local_dir):
            # 目录不存在，创建目录
            os.makedirs(local_dir)

        file_name = remote_file.split('/')[-1]
        local_file = local_dir + file_name
        hostname = self.host
        port = 22
        username = 'root'
        password = self.passwd
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port, username, password)
            sftp = client.open_sftp()
            # 上传本地文件到远程服务器
            # 报错Failure：sftp.put("/tmp/xx.py", "/tmp/xx.py")
            sftp.get(remote_file, local_file)
        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            sftp.close()
            client.close()

    def getsql(self, sql_name):
        """
        获取sql文件
        """
        download_sql = "curl -o /root/{}.sql -O -L https://gitee.com/yiluohan1234/vagrant_bigdata_cluster/raw/master/resources/bdcompetition/sql/{}.sql && source /etc/profile".format(sql_name, sql_name)
        out, err = self.exec(command=download_sql)
        print("upload sql success！")

    def getenvsql(self, sql_name):
        """
        获取sql文件
        """
        import bdcp
        package_path = os.path.dirname(bdcp.__file__)
        if platform.system() == 'Windows':
            local_file = package_path + '\sql\{}.sql'.format(sql_name)
        else:
            local_file = package_path + '/sql/{}.sql'.format(sql_name)
        remote_file = '/root/{}.sql'.format(sql_name)
        self.upload(local_file, remote_file)
        print("upload sql success！")

    def get_command(self, title):
        if platform.system() == 'Windows':
            username = os.environ.get('USERNAME')
            config_path = 'C:/Users/{}/.config.ini'.format(username)
        else:
            config_path = '/root/.config.ini'
        # 读取INI配置文件
        config = configparser.ConfigParser()
        config.read(config_path)

        # 获取配置
        host = config.get('MySQL', 'host')
        user = config.get('MySQL', 'user')
        passwd = config.get('MySQL', 'passwd')
        port = int(config.get('MySQL', 'port'))
        db_name = config.get('MySQL', 'db_name')
        ret = []
        try:
            db=pymysql.connect(host=host,user=user,passwd=passwd, port=port, db=db_name,charset='utf8')
            cursor = db.cursor()
            sql = "select * from bd_command where title like '%{}%'".format(title)
            cursor.execute(sql)
            data_list = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()
        for data in data_list:
            #print(data)
            ret.append({'type':data[1], 'title':data[2], 'command': data[3]})
        if len(ret) == 0:
            print("no data")
            return
        return ret

    def get_abcd(self, title):
        if platform.system() == 'Windows':
            username = os.environ.get('USERNAME')
            config_path = 'C:/Users/{}/.config.ini'.format(username)
        else:
            config_path = '/root/.config.ini'
        # 读取INI配置文件
        config = configparser.ConfigParser()
        config.read(config_path)

        # 获取配置
        host = config.get('MySQL', 'host')
        user = config.get('MySQL', 'user')
        passwd = config.get('MySQL', 'passwd')
        port = int(config.get('MySQL', 'port'))
        db_name = config.get('MySQL', 'db_name')
        ret = []
        try:
            db=pymysql.connect(host=host,user=user,passwd=passwd, port=port, db=db_name,charset='utf8')
            cursor = db.cursor()
            sql = "select * from bd_practice where title like '%{}%'".format(title)
            cursor.execute(sql)
            data_list = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()
        for data in data_list:
            #print(data)
            ret.append({'type':data[2], 'answer':data[7], 'title':data[1], 'A':data[3], 'B':data[4], 'C':data[5], 'D':data[6]})
        if len(ret) == 0:
            print("no data")
            return
        return ret

    def init_mysql_config(self, host='localhost', passwd='123456'):
        """
        初始化mysql配置文件,124.70.110.14
        """
        if platform.system() == 'Windows':
            username = os.environ.get('USERNAME')
            config_path = 'C:/Users/{}/.config.ini'.format(username)
        else:
            config_path = '/root/.config.ini'
        with open(config_path, 'w', encoding='utf8') as f:
            f.write("[MySQL]\n")
            f.write("host={}\n".format(host))
            f.write("user=root\n")
            f.write("passwd={}\n".format(passwd))
            f.write("port=3306\n")
            f.write("db_name=hongya\n")

    def clear(self):
        """
        删除my.sh
        """
        # 执行远程命令
        out, err = self.exec(command='rm -rf /etc/profile.d/my.sh')
