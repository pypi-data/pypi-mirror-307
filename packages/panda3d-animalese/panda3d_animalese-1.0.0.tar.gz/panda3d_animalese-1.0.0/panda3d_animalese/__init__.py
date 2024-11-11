"""
Animalese Synthetizer for Panda3D.
"""

from panda3d import core as p3d
from panda3d_toolbox import runtime
from direct.interval.IntervalGlobal import *
import random

class AnimaleseLibrary(object):
    """
    Library of audio files used for the animalese synth.
    """

    def __init__(self, folder: str, extension: str = 'wav'):
        """
        Initialize the AnimaleseLibrary object.
        """

        self.folder = folder
        self.extension = extension

        self.sounds = {}

    def load(self) -> None:
        """
        Loads the audio files used for the animalese synth.
        """

        keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','th','sh',' ','.']
        for index,ltr in enumerate(keys):
            num = index+1
            if num < 10:
                num = '0' + str(num)

            sound_filename = f'{self.folder}/sound{num}.{self.extension}'
            sound = runtime.loader.loadSfx(sound_filename)
            self.sounds[ltr] = sound

    def is_loaded(self) -> bool:
        """
        Returns True if the audio files have been loaded.
        """

        return len(self.sounds) > 0

class AnimaleseSynth(object):
    """
    Animalese synthetizer for playing text as animalese.
    """

    def __init__(self, library: AnimaleseLibrary):
        """
        Initialize the AnimaleseSynth object.
        """
    
        self.library = library

    def __get_character_sound(self, i: int, char: str, text: str) -> p3d.AudioSound:
        """
        Returns the sound for the given character.
        """

        try:
            if char == 's' and text[i+1] == 'h':
                return self.library.sounds['sh']
            elif char == 't' and text[i+1] == 'h': 
                return self.library.sounds['th']
            elif char == 'h' and (text[i-1] == 's' or text[i-1] == 't'):
                return None
            elif char == ',' or char == '?':
                return self.library.sounds['.']
            elif char == text[i-1]: 
                return None
        except:
            pass

        if not char.isalpha() and char != '.':
            return None

        return self.library.sounds[char]

    def __queue_play_steps(self, steps: list, i: int, text: str, sound: p3d.AudioSound, rng: float = 0.25) -> None:
        """
        Play the animalese synth for a single character.
        """
            
        if text[len(text)-1] == '?':
            if i >= len(text)*.8:
                octaves = random.random() * rng + (i-i*.8) * .1 + 2.1
            else:
                octaves = random.random() * rng + 2.0
        else:
            octaves = random.random() * rng + 2.3

        steps.append(Func(sound.set_play_rate, octaves))
        steps.append(Func(sound.play))
        steps.append(Wait(sound.length()/octaves))

    def play(self, text: str, rng: float = 0.25) -> None:
        """
        Play the animalese synth for the given text.
        """

        if not self.library.is_loaded():
            self.library.load()

        sync_steps = []
        text = text.lower()
        for i, char in enumerate(text):
            sound = self.__get_character_sound(i, char, text)
            if sound is not None:
                self.__queue_play_steps(sync_steps, i, text, sound, rng)

        synth_sequence = Sequence(*sync_steps)
        synth_sequence.start()