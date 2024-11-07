import argparse
import os
import smtplib
import subprocess
import threading
from abc import ABC, abstractmethod
from collections import deque
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

import yaml

CONFIG_DIR = os.path.expanduser('~/.exit_notifier')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'notice.yaml')


class Notice(ABC):
    @abstractmethod
    def send(self, title: str, content): ...


class MailNotice(Notice):
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password, from_addr, to_addrs):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_addr = from_addr
        self.to_addrs = to_addrs if isinstance(to_addrs, list) else [to_addrs]
        self.ready_status = False
        self.configure()

    def configure(self):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=5)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.quit()
            self.ready_status = True
        except Exception as e:
            print(f"邮件配置失败: {e}")
            self.ready_status = False

    def send(self, title: str, content):
        if not self.ready_status:
            print("邮件配置未就绪。")
            return False
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = title
            msg['From'] = self.from_addr
            msg['To'] = ", ".join(self.to_addrs)
            msg['Date'] = formatdate(localtime=True)
            msg['Message-ID'] = make_msgid()

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.from_addr, self.to_addrs, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False


class Trigger(ABC):
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run)
        self._lock = threading.Lock()
        self._running = False

    def start(self):
        with self._lock:
            if not self._running:
                self._running = True
                self._thread.start()

    def stop(self):
        with self._lock:
            self._stop_event.set()
            self._running = False
        if threading.current_thread() != self._thread:
            self._thread.join()

    def join(self):
        if threading.current_thread() != self._thread:
            self._thread.join()

    @abstractmethod
    def _run(self): ...


class ExecTrigger(Trigger):
    def __init__(self, command, action_func, log_lines=10):
        super().__init__()
        self.command = command
        self.action_func = action_func
        self.log_lines = log_lines
        self.logs = deque(maxlen=log_lines)

    def _run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            for line in process.stdout:
                print(line, end='')
                self.logs.append(line)

            process.wait()
            return_code = process.returncode
            self.action_func(self.get_last_logs(), return_code)
        except Exception as e:
            print(f"execute error: {e}")
        finally:
            self.stop()

    def get_last_logs(self):
        return ''.join(self.logs)


def config_mail():
    print("请按提示输入邮件通知的 SMTP 配置：")
    smtp_server = input("SMTP服务器地址：")
    smtp_port = input("SMTP服务器端口（默认587）：") or "587"
    smtp_user = input("SMTP用户名：")
    smtp_password = input("SMTP密码：")
    from_addr = input("发件人邮箱地址：")
    to_addrs = input("收件人邮箱地址（多个地址用逗号分隔）：")
    config = {
        'type': 'mail',
        'smtp_server': smtp_server,
        'smtp_port': int(smtp_port),
        'smtp_user': smtp_user,
        'smtp_password': smtp_password,
        'from_addr': from_addr,
        'to_addrs': [addr.strip() for addr in to_addrs.split(',')]
    }
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)
    print("邮件通知配置已保存。")


def show_config():
    if not os.path.exists(CONFIG_FILE):
        print("没有找到通知配置。")
        return
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    if config['type'] == 'mail':
        print("邮件通知配置：")
        print(f"SMTP服务器地址：{config['smtp_server']}")
        print(f"SMTP服务器端口：{config['smtp_port']}")
        print(f"SMTP用户名：{config['smtp_user']}")
        print(f"发件人邮箱地址：{config['from_addr']}")
        print(f"收件人邮箱地址：{', '.join(config['to_addrs'])}")
    else:
        print("未知的通知配置类型。")


def reset_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print("通知配置已删除。")
    else:
        print("没有找到通知配置。")


def run_script(notice_type, script_path, script_args):
    if not os.path.exists(CONFIG_FILE):
        print("没有找到通知配置，请先配置通知。")
        return
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    if config['type'] != notice_type:
        print(f"通知类型不匹配，请配置 {notice_type} 类型的通知。")
        return
    if notice_type == 'mail':
        mail_notice = MailNotice(
            smtp_server=config['smtp_server'],
            smtp_port=config['smtp_port'],
            smtp_user=config['smtp_user'],
            smtp_password=config['smtp_password'],
            from_addr=config['from_addr'],
            to_addrs=config['to_addrs']
        )
        if not mail_notice.ready_status:
            print("邮件通知配置无效，请检查配置。")
            return

        def action(logs, return_code):
            subject = f"脚本 {os.path.basename(script_path)} 执行完毕"
            content = f"退出代码：{return_code}\n最后的日志：\n{logs}"
            mail_notice.send(subject, content)
        command = ['python', script_path] + script_args
        trigger = ExecTrigger(command, action_func=action, log_lines=10)
        trigger.start()
        trigger.join()
    else:
        print("未知的通知类型。")


def main():
    parser = argparse.ArgumentParser(description='Exit Notifier CLI 工具')
    subparsers = parser.add_subparsers(dest='command')
    parser_config = subparsers.add_parser('config', help='配置通知')
    parser_run = subparsers.add_parser('run', help='运行脚本并使用通知')
    parser_run.add_argument('-c', '--config', required=True, help='通知类型')
    parser_run.add_argument('-p', '--path', required=True, help='脚本路径')
    parser_run.add_argument('--args', nargs=argparse.REMAINDER, help='脚本参数', default=[])
    args = parser.parse_args()
    if args.command == 'config':
        if args.subcommand == 'mail':
            config_mail()
        elif args.subcommand == 'reset':
            reset_config()
        else:
            parser_config.print_help()
    elif args.command == 'show':
        show_config()
    elif args.command == 'run':
        run_script(args.config, args.path, args.args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
