import rumps
import psutil
import time


class IStat(rumps.App):
    def __init__(self):
        super(IStat, self).__init__("IStat")
        self.last_time = time.time()
        self.last_sent, self.last_recv = self.get_bytes()

    def get_speed(self):
        sent, recv = self.get_bytes()
        current_time = time.time()
        upload = (sent - self.last_sent) / (current_time - self.last_time)
        download = (recv - self.last_recv) / (current_time - self.last_time)
        self.last_sent = sent
        self.last_recv = recv
        self.last_time = current_time
        return int(upload), int(download)

    def get_bytes(self):
        counters = psutil.net_io_counters()
        return counters.bytes_sent, counters.bytes_recv

    @rumps.timer(1)
    def render_state_bar(self, sender):
        upload, download = self.get_speed()
        upload = self.human_speed(upload)
        download = self.human_speed(download)
        self.title = "U:" + upload + " D:" + download

    def human_speed(self, num):
        num = float(num)
        units = ['B/s', 'K/s', 'M/s', 'G/s']
        result = str(int(num)) + units[0]
        for i in range(len(units)):
            if num >= 1000:
                num = num / 1024
                result = ("%.2f" % num) + units[i+1]
            else:
                break
        return result


if __name__ == "__main__":
    IStat().run()
