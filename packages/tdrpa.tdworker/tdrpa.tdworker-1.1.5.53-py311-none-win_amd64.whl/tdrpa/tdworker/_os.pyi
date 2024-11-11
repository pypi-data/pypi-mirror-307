class App:
    @staticmethod
    def Kill(processName: str | int):
        """
        强制停止应用程序的运行（结束进程）

        App.Kill('chrome.exe')

        :param processName:[必选参数]应用程序进程名或进程PID
        :return:None
        """

    @staticmethod
    def GetStatus(processName: str | int, status: int = 0):
        """
        获取应用运行状态
        App.GetStatus('chrome.exe', status=0)

        :param processName:[必选参数]应用程序进程名或进程PID
        :param status:[可选参数]筛选进程状态。0:所有状态 1:运行 2:暂停 3:未响应 4:未知。默认0
        :return:进程存在返回True，不存在返回False
        """

    @staticmethod
    def Run(exePath, waitType: int = 0, showType: int = 1):
        """
        启动应用程序
        App.Run('''C:\\Windows\\system32\\mspaint.exe''')

        :param exePath:[必选参数]应用程序文件路径
        :param waitType:[可选参数]0是等待、1是等待应用程序准备好、2是等待应用程序执行到退出。默认0
        :param showType:[可选参数]程序启动后的显示样式（不一定生效）：0是隐藏、1是默认、3是最大化、6是最小化
        :return:返回应用程序的 PID
        """
