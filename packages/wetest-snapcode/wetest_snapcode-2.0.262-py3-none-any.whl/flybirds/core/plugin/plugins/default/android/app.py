"""
android app core api implement
"""

import flybirds.core.global_resource as gr
from flybirds_airtest.core.api import (time, stop_app, install, uninstall, start_app, clear_app)
from flybirds.core.exceptions import FlybirdsException

__open__ = ["App"]


class App:
    """Android App Class"""

    name = "android_app"

    def wake_app(self, package_name, wait_time=None):
        """
        Start the target application on device
        """
        try:
            start_app(package_name)
            if not (wait_time is None):
                time.sleep(wait_time)
        except Exception as e:
            err=e.stdout
            package_err=b"No activities found to run, monkey aborted"
            if package_err in err:
                raise FlybirdsException(f"package {package_name} not found")
            raise FlybirdsException(f"start app fail: {e.stdout}")

    def shut_app(self, package_name):
        """
        关闭测试app
        """
        stop_app(package_name)

    def install_app(self, package_path, wait_time=None):
        """
        Install application on device

        :param package_path: the path to file to be installed on target device
        :param wait_time:
        :return: None
        :platforms: Android
        :Example:
            >>> install_app(r"D:\\demo\\test.apk")
        """
        i_result = install(package_path)
        if not (wait_time is None):
            time.sleep(wait_time)
        return i_result

    def uninstall_app(self, package_name, wait_time=None):
        """
        Uninstall application on device

        :param package_name: name of the package, see also `start_app`
        :param wait_time:
        :return: None
        :platforms: Android
        :Example:
            >>> uninstall("com.flyBirds.music")
        """
        uninstall(package_name)
        if not (wait_time is None):
            time.sleep(wait_time)

    def current_app(self):
        """
        Get current app package name
        """
        device = gr.get_value("deviceInstance")
        app = device.get_top_activity_name()
        return app


    def clear_app(self, package):
        """
         Clear data of the target application on device
        """
        clear_app(package)


    def list_apps(self, show_system=False):
        """
        Get current app package name
        """
        device = gr.get_value("deviceInstance")
        if show_system:
            cmd_package_installed = "pm list packages"
        else:
            cmd_package_installed = "pm list packages -3"
        cmd_result = device.shell(cmd_package_installed)
        apps = []
        if cmd_result is not None:
            lines = cmd_result.splitlines()
            for line in lines:
                if line is not None and line:
                    ls = line.split(":")
                    if len(ls) == 2:
                        apps.append(ls[1].strip())
        return apps