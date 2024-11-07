# exit-notifier
`Exit Notifier` 是一个命令行工具，允许您在脚本执行完毕后，自动发送通知（如电子邮件）。这对于需要长时间运行的脚本或需要在无人值守的情况下监控脚本执行情况的场景非常有用。



## Install

```bash
python -m pip install exit-notifier
```

## Config

### config mail
```bash
exit_notifier config mail
```
### show config
```bash
exit_notifier show
```

### reset config
```bash
exit_notifier reset
```

## Use

```bash
exit_notifier run -c mail -p /path/to/your_script.py --args [脚本参数]
```

### example usage:
```bash
exit_notifier run -c mail -p test_scripts/test_args_in.py --args -n 1 -s ss -l 1 2 5 --flag
exit_notifier run -c mail -p test_scripts/test_script.py 
```

## Notice

你的配置将被以明文记录到配置文件：`~/.exit_notifier/notice.yaml`中，注意警惕隐私泄露