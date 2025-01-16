import os
import signal
import socket
import threading
import time
from functools import wraps


def wait_for_tcp(host, port, retries=100, retry_delay=2):
    """等待直到ip及端口能连接"""
    retry_count = 0
    while retry_count <= retries:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            # print("Port is open")
            break
        else:
            # print("Port is not open, retrying...")
            time.sleep(retry_delay)


def is_tcp_listen(port, ip="127.0.0.1"):
    """
    通过“连接” 的方式，确定端口是否listening
    """
    _ip, _port = ip, port

    if isinstance(port, str) and port.find(":") > 0:
        # 参数形如：127.0.0.1:80
        _ip = port.split(":")[0]
        _port = port.split(":")[1]

    _port = int(_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((_ip, _port))
        s.shutdown(2)

        # print("port %s opened" % _port)
        return True
    except Exception as e:
        print(e)
        # print("port %s closed" % _port)
        return False


def get_tcp_open_port(port=0):
    """
    检查端口是否已经绑定
    端口写成0就可以,python会查找一个可用的tcp口绑定
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", port))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
    except Exception as e:
        print(e)
        return None


def check_and_creat_dir(filepath):
    """
    判断文件是否存在，文件路径不存在则创建文件夹
    注意：对于如此简单，又常用的功能，python应该本身有很优雅的函数实现，只是自己没找到而已。
    :param file_url: 文件路径，包含文件名
    :return:
    """
    file_gang_list = filepath.split("/")
    if len(file_gang_list) > 1:
        [fname, fename] = os.path.split(filepath)
        print(fname, fename)
        if not os.path.exists(fname):
            os.makedirs(fname)
        else:
            return
    else:
        return


def getIfaceByIp(ipaddv4):
    """查找绑定了此IP地址的网卡名称"""
    import netifaces

    ifaces = [x for x in netifaces.interfaces() if x != "lo"]
    iface_ips = [
        (x, netifaces.ifaddresses(x)[netifaces.AF_INET][0]["addr"]) for x in ifaces
    ]
    filtered = [x for x in iface_ips if x[1] == ipaddv4]
    if filtered:
        return filtered[0][0]
    return None


def getNetmaskbyIface(ifname):
    """根据网卡名获取子网"""
    import netifaces

    iface = netifaces.ifaddresses(ifname)
    return iface[netifaces.AF_INET][0]["netmask"]


def io_pip_thread(ioin, ioout):
    """
    启动新线程, 从in 流读取,并写入到out流
    """

    def t():
        read_bytes = ioin.read()
        while read_bytes:
            ioout.write(read_bytes)
            ioout.flush()
            read_bytes = ioin.read()

    threading.Thread(
        target=t,
    ).start()


def retry_wrapper(retry_times, exception=Exception, error_handler=None, interval=0.1):
    """
    重试器，包装函数对指定异常进行重试
    函数重试装饰器
    :param retry_times: 重试次数
    :param exception: 需要重试的异常
    :param error_handler: 出错时的回调函数
    :param interval: 重试间隔时间
    :return:
    """

    def out_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    count += 1
                    if error_handler:
                        result = error_handler(func.__name__, count, e, *args, **kwargs)
                        if result:
                            count -= 1
                    if count >= retry_times:
                        raise
                    time.sleep(interval)

        return wrapper

    return out_wrapper


def timeout(timeout_time, default):
    """
    超时器，装饰函数并指定其超时时间
    Decorate a method so it is required to execute in a given time period,
    or return a default value.
    :param timeout_time:
    :param default:
    :return:
    """

    class DecoratorTimeout(Exception):
        pass

    def timeout_function(f):
        def f2(*args):
            def timeout_handler(signum, frame):
                raise DecoratorTimeout

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            # triger alarm in timeout_time seconds
            signal.alarm(timeout_time)
            try:
                retval = f(*args)
            except DecoratorTimeout:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler)
            signal.alarm(0)
            return retval

        return f2

    return timeout_function


def call_later(callback, call_args=tuple(), immediately=True, interval=1):
    """
    应用场景：
    被装饰的方法需要大量调用，随后需要调用保存方法，但是因为被装饰的方法访问量很高，而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后，再调用保存方法。规定间隔内，无论调用多少次被装饰方法，保存方法只会
    调用一次，除非immediately=True
    :param callback: 随后需要调用的方法名
    :param call_args: 随后需要调用的方法所需要的参数
    :param immediately: 是否立即调用
    :param interval: 调用间隔
    :return:
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return func(*args, **kwargs)
            finally:
                if immediately:
                    getattr(self, callback)(*call_args)
                else:
                    now = time.time()
                    if now - self.__dict__.get("last_call_time", 0) > interval:
                        getattr(self, callback)(*call_args)
                        self.__dict__["last_call_time"] = now

        return wrapper

    return decorate


def get_ip():
    """
    获取局域网ip
    :return:
    """
    import psutil

    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and item[1] != "127.0.0.1":
                netcard_info.append((k, item[1]))

    if netcard_info:
        return netcard_info[0][1]
