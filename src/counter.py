import pydub
import numpy as np
import os
from matplotlib import pyplot as plt

class SilenceCounter():
    def __init__(self, wav_path, normalize=True):
        self.audio = pydub.AudioSegment.from_wav(wav_path)
        
        if normalize:
            self.audio = pydub.effects.normalize(self.audio)

    def count(self, min_silence_sec=1, rel_silence_db_thresh=0, visualize=False):
        
        silence_thresh = self.audio.dBFS - 16 + rel_silence_db_thresh

        silence = pydub.silence.detect_silence(self.audio, min_silence_len=int(min_silence_sec * 10000),
                                               silence_thresh=silence_thresh)

        silence = [((start/1000),(stop/1000)) for start, stop in silence] # in sec
        
        if visualize:
            signal = np.frombuffer(self.audio._data, np.int16)
            
            plt.figure(figsize=(15, 5))
            plt.plot(np.arange(len(signal)) / self.audio.frame_rate, signal, alpha=0.5)
            
            cmap = plt.get_cmap("tab10")
            
            for i, (start, stop) in enumerate(silence):
                plt.axvline(x=start, ls='-', color=cmap(i % 10))
                plt.axvline(x=stop, ls='--', color=cmap(i % 10))
            
            plt.xlabel('duration (s)')
            plt.ylabel('amplitude')
            plt.show()
        
        return sum([stop - start for start, stop in silence])
