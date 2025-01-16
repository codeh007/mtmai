import logging

logger = logging.getLogger()


# def process_output(process):
#     while True:
#         output = process.stdout.readline().decode()
#         if process.poll() is not None:
#             break
#         if output:
#             print(output, flush=True)


# def exec_cmd2(cmd, output_file="/var/log/clilog.log"):
#     """
#     助手函数, 启动系统进程,并将进程的输出写入到文件中
#     TODO: 应该升级为流模式, 这样就不用关日志是不是文件,可以使用StringIO
#     """

#     def handle_output(process):
#         try:
#             with open(output_file, "ab+") as logfile:
#                 while True:
#                     if process.stdout:
#                         bytes = process.stdout.read()
#                         logfile.write(bytes)
#                         logfile.flush()
#                     if process.stderr:
#                         bytes = process.stderr.read()
#                         logfile.write(bytes)
#                         logfile.flush()

#                     if process.poll() is not None:
#                         break
#         except Exception as e:
#             print(e)

#     process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)  # noqa: S603
#     threading.Thread(target=handle_output, args=(process,)).start()
