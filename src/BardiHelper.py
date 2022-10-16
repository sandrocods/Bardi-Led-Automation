#
# Bardi connector using adb
# only works for BARDI Bluetooth Light Bulb 9W RGBWW
#
import time

import uiautomator2 as u2


class BardiConnector:

    def __init__(self, timeout=20.0, connection_type="wifi", address=None):

        if connection_type.lower() == "wifi":
            self.device = u2.connect(addr=address)
        elif connection_type.lower() == "usb":
            self.device = u2.connect()  # connect to device

        self.device.app_stop("com.bardi.smart.home")  # stop app
        self.device.app_start("com.bardi.smart.home")  # start app
        self.timeout = timeout  # timeout for wait
        self.location_color = {
            "green": (0.693, 0.598),
            "pink": (0.144, 0.447),
            "blue": (0.769, 0.396),
            "lime": (0.258, 0.595),
            "cyan": (0.802, 0.545),
        }
        self.brightness = {
            "50": (0.529, 0.727),
            "100": (0.815, 0.672),
            "1": (0.182, 0.671),
            "25": (0.331, 0.715),
            "75": (0.655, 0.717),
        }
        self.theme_data = {}

    def get_bardi_device(self):

        data_device = []
        if self.device(resourceId="com.bardi.smart.home:id/tv_dev_name").wait(timeout=self.timeout):
            for i in self.device(resourceId="com.bardi.smart.home:id/tv_dev_name"):
                data_device.append(i.info["text"])

            return {
                "status": True,
                "data_device": data_device
            }

        else:
            return {
                "status": False,
                "message": "Device not found"
            }

    def connect_bardi_device(self, device_name):
        if self.device(text=device_name).wait(timeout=self.timeout):
            self.device(text=device_name).click()
            device_connection_status = True

            counter = 0
            while device_connection_status:

                if counter > 10:
                    return {
                        "status": False,
                        "message": "Device not connected try again later"
                    }

                if self.device(text="Device Connection Failure").exists(timeout=self.timeout):
                    self.device.press("back")
                    self.device(text=device_name).click()
                    device_connection_status = True
                    counter += 1
                else:
                    self.device.click(0.468, 0.949)
                    device_connection_status = False

            return {
                "status": True,
                "message": "Device connected"
            }

        else:
            return {
                "status": False,
                "message": "Device not found"
            }

    def change_state(self, state):
        if state.lower() == "on":
            self.device.xpath(
                '//*[@resource-id="com.bardi.smart.home:id/ty_fragment_reactroot"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[8]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()

            return {
                "status": True,
                "message": "Device state changed to {}".format(state)
            }
        elif state.lower() == "off":
            self.device.xpath(
                '//*[@resource-id="com.bardi.smart.home:id/ty_fragment_reactroot"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[8]/android.view.ViewGroup[1]/android.view.ViewGroup[3]').click()
            return {
                "status": True,
                "message": "Device state changed to {}".format(state)
            }
        else:
            return {
                "status": False,
                "message": "Device state not changed"
            }

    def change_brightness(self, brightness):
        time.sleep(0.5)
        self.device.click(*self.brightness[brightness])

    def change_color(self, color):

        if color.lower() == "white":
            self.device(text="White").click()
            time.sleep(0.5)
            self.device.click(0.86, 0.472)
        elif color.lower() == "half white":
            self.device(text="White").click()
            time.sleep(0.5)
            self.device.click(0.501, 0.49)
        elif color.lower() == "sepia":
            self.device(text="White").click()
            time.sleep(0.5)
            self.device.click(0.134, 0.473)
        else:
            self.device(text="Color").click()
            time.sleep(0.5)
            self.device.click(*self.location_color[color])

    def get_theme(self):
        theme_datas = []
        self.device.xpath(
            '//*[@resource-id="com.bardi.smart.home:id/ty_fragment_reactroot"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[3]/android.view.View[1]'
        ).click()
        time.sleep(0.5)

        for i in self.device.xpath(
                '//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.TextView').all():
            theme_datas.append(
                {
                    "theme_name": i.info["text"],
                    "theme_location": i.center()
                }
            )
        self.theme_data = theme_datas

    def get_theme_by_music(self):
        theme_datas = []
        self.device.xpath(
            '//*[@resource-id="com.bardi.smart.home:id/ty_fragment_reactroot"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[8]/android.view.ViewGroup[4]/android.view.View[1]').click()
        time.sleep(0.5)

        counter = 0
        for i in self.device.xpath(
                '//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.TextView').all():
            theme_datas.append(
                {
                    "theme_name": i.info["text"],
                    "theme_location": self.device.xpath(
                        '//android.widget.ScrollView/android.view.ViewGroup[1]/android.view.ViewGroup[{counter}]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.widget.ImageView[1]'.format(
                            counter=counter + 1)).center()
                }
            )
        self.theme_data = theme_datas

    def change_theme(self, theme_name, theme_type):
        if theme_type.lower() == "normal":
            self.get_theme()
        elif theme_type.lower() == "music":
            self.get_theme_by_music()

        time.sleep(0.5)
        for i in self.theme_data:
            if i["theme_name"] == theme_name:
                self.device.click(*i["theme_location"])
                return {
                    "status": True,
                    "message": "Theme changed to {}".format(theme_name)
                }
