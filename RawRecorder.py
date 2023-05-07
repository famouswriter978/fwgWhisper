# -*- coding: utf-8 -*-
# A borrowed snippet of code

"""recorder.py
https://gist.github.com/sloria/5693955
>>>import time
Provides WAV recording functionality via two approaches:

Blocking mode (record for a set duration):
>>> rec = Recorder(channels=2)
>>> with rec.open('blocking.wav', 'wb') as recfile:
...     recfile.record(duration=5.0)

Non-blocking mode (start and stop recording):
>>> rec = Recorder(channels=2)
>>> with rec.open('nonblocking.wav', 'wb') as recfile2:
...     recfile2.start_recording()
...     time.sleep(5.0)
...     recfile2.stop_recording()
"""

import pyaudio
import wave


class Recorder(object):
    """A recorder class for recording audio to a WAV file.
    Records in mono by default.
    """

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, file_name, mode='wb'):
        return RecordingFile(file_name, mode, self.channels, self.rate, self.frames_per_buffer)


class RecordingFile(object):
    def __init__(self, file_name, mode, channels,
                 rate, frames_per_buffer):
        self.file_name = file_name
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.file_name, self.mode)
        self._stream = None
        # Check input device
        # id = self._pa.get_default_input_device_info()
        # print('id', id['name'])

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue

        return callback

    def _prepare_file(self, file_name, mode='wb'):
        wavefile = wave.open(file_name, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer,
                                     stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self
