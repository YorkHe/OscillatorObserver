import unittest
from ..libs.oscilloscope import tek, wave, usb_devices
from ..libs.utils import error

class TestTek(unittest.TestCase):
    def test_channel_parameters(self):
        channel = tek.ChannelParameters(1)
        self.assertEqual(channel.channel, 1)
        self.assertEqual(channel.x_unit, 0)
        self.assertEqual(channel.x_inc, 0)
        self.assertEqual(channel.y_unit, 0)
        self.assertEqual(channel.y_mult, 0)
        self.assertEqual(channel.y_off, 0)
        self.assertEqual(channel.y_zero, 0)

    def test_find_instrument(self):
        device  = usb_devices.find_instrument("TDS1012B")
        self.assertIsNotNone(device)

    def test_init(self):
        self.device = tek.TDS1012B()
        self.assertIsNotNone(self.device.visa)
        self.assertEqual(self.device.identity, "TDS1012B")
        self.assertIsNotNone(self.device.channel1)
        self.assertIsNotNone(self.device.channel2)

    def test_query(self):
        content = self.device.query("*IDN?")
        self.assertNotIsInstance(content, error.Error)
        self.assertIsNotNone(content)

    def test_write(self):
        content = self.device.write("*IDN?")
        self.assertNotIsInstance(content, error.Error)

    def test_read(self):
        self.device.write("*IDN?")
        content = self.device.read()
        self.assertNotIsInstance(content, error.Error)
        self.assertIsNotNone(content, error.Error)

    def test_clear_queue(self):
        content = self.device.clear_queue()
        self.assertNotIsInstance(content, error.Error)

    def test_set_channel(self):
        content = self.device.set_channel(1)
        self.assertNotIsInstance(content, error.Error)

    def test_get_scale_parameters(self):
        channel = tek.ChannelParameters(1)
        content = self.device.get_scale_parameters(channel)
        self.assertNotIsInstance(content, error.Error)
        self.assertIsInstance(channel.x_unit, str)
        self.assertIsInstance(channel.x_inc, float)
        self.assertIsInstance(channel.y_unit, str)
        self.assertIsInstance(channel.y_mult, float)
        self.assertIsInstance(channel.y_off, float)
        self.assertIsInstance(channel.y_zero, float)

    def test_get_wave_form(self):
        channel = tek.ChannelParameters(1)
        self.device.get_scale_parameters(channel)
        e,x,y = self.device.get_wave_form(channel)

        self.assertEqual(e, {})
        self.assertIsInstance(x, list)
        self.assertIsInstance(y, list)
        self.assertGreater(len(x), 0)
        self.assertGreater(len(y), 0)

class TestWave(unittest.TestCase):
    def get_data(self):
        data = open("../data/0930/60.txt", "r+").read()
        self.data_x = []
        self.data_y = []
        x = 0

        for d in data.split('\n'):
            if d:
                delta_x, y = d.split("\t")
                delta_x = float(delta_x)
                y = float(y)
                x = x + delta_x
                self.data_x.append(x)
                self.data_y.append(y)

    def test_init(self):
        self.get_data()
        self.wave = wave.Wave(self.data_x, self.data_y)
        self.assertEqual(self.wave.waveData_x, self.data_x)
        self.assertEqual(self.wave.waveData_y, self.data_y)
        self.assertEqual(self.wave.filtered_wave_x, [])
        self.assertEqual(self.wave.filtered_wave_y, [])
        self.assertIsInstance(self.wave.method, dict)

    def test_get_wave(self):
        x, y = self.wave.get_wave()
        self.assertEqual(x, self.data_x)
        self.assertEqual(y, self.data_y)

    def test_median_filtered(self):
        content = self.wave.median_filtered()
        self.assertIsInstance(content, list)
        self.assertEqual(len(content), len(self.data_y))

    def test_fft_filtered(self):
        content = self.wave.fft_filtered()
        self.assertIsInstance(content, list)
        self.assertEqual(len(content), len(self.data_y))

    def test_filter(self):
        self.wave.filter()
        self.assertEqual(self.wave.filtered_wave_y, self.wave.median_filtered())
        self.assertEqual(self.wave.filtered_wave_x, self.wave.waveData_x)

    def test_find_peak(self):
        content = self.wave.find_peak(0.3, True)
        self.assertIsInstance(content, list)
        self.assertGreater(len(content), 0)

    def test_find_minimum_point(self):
        content_filtered_x, content_filtered_y = self.wave.find_minimum_point(True)
        content_not_filtered_x, content_not_filtered_y = self.wave.find_minimum_point(False)
        self.assertIsInstance(content_filtered_x, float)
        self.assertIsInstance(content_filtered_y, float)
        self.assertIsInstance(content_not_filtered_x, float)
        self.assertIsInstance(content_not_filtered_y, float)



if __name__ == "main":
    unittest.main()