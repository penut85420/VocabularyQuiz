import json
import os
import threading
from random import shuffle
from threading import Thread
from time import time

from gtts import gTTS
from playsound import playsound


class VoiceManager:
    VOICE_PATH = './voices'

    def __init__(self):
        if not os.path.exists('./voices'):
            os.mkdir('./voices')
        self.voice = dict()
        for dir_path, dir_list, file_list in os.walk('./voices'):
            for file_name in file_list:
                if file_name.endswith('.mp3'):
                    full_path = os.path.join(dir_path, file_name)
                    self.voice[file_name[:-4]] = full_path
    
    def get_path(self, text):
        return os.path.join(VoiceManager.VOICE_PATH, '%s.mp3' % text)

    def play(self, text):
        vpath = self.get_path(text)
        if not self.voice.get(text, None):
            tts = gTTS(text=text, lang='en')
            tts.save(vpath)
        playsound(vpath)

class QuizResult:
    def __init__(self):
        self.wrong = 0
        self.correct = 0
        self.time_cost = time()
    
    def summarize(self):
        self.time_cost = time() - self.time_cost
        self.total = self.wrong + self.correct
        self.acc = self.correct / self.total * 100

    def __str__(self):
        return '\n'.join([
            '[Result]',
            'Correct: {0.correct}/{0.total}'.format(self),
            'Accuracy: %5.2f%%' % self.acc,
            'Time Cost: %.1fs\n' % self.time_cost
        ])

class Vocabulary:
    DATA_PATH = './data'
    
    def __init__(self):
        self.vocabulary = self._load_vocabulary()
        self.title_list = self._get_title_list()

    def get_vocabulary(self, idx):
        shuffle(self.vocabulary[idx]['vocabulary'])
        return self.vocabulary[idx]['vocabulary']

    def _load_vocabulary(self):
        vocabulary = list()
        idx = 0
        for dir_path, dir_list, file_list in os.walk(Vocabulary.DATA_PATH):
            for file_name in file_list:
                full_path = os.path.join(dir_path, file_name)
                if not full_path.endswith('.json'):
                    continue
                
                with open(full_path, 'r', encoding='UTF-8') as fin:
                    vocabulary.append(json.load(fin))
        return vocabulary
    
    def _get_title_list(self):
        title = list()
        for voc in self.vocabulary:
            title.append(voc['title'])
        return title

class Quiz:
    def __init__(self, data):
        self.data = data
        self.vm = VoiceManager()
    
    def run_quiz(self):
        data = self.data
        result = QuizResult()
        for d in data:
            print(d['cht'])
            ans = input(' > ')
            if ans != d['eng']:
                result.wrong += 1
                print('Wrong: %s' % d['eng'])
            else:
                result.correct += 1
                print('Correct!')
            print()
            Thread(target=self.vm.play, args=(d['eng'], )).start()
        result.summarize()
        print(result)

class Main:
    def __init__(self):
        self.vocabulary = Vocabulary()
    
    def run(self):
        while True:
            print('=== Choose Vocabulary Set ===')
            for i, t in enumerate(self.vocabulary.title_list):
                print('[%s] %s' % (chr(i+ord('A')), t))
            print('[%s] %s' % ('0', 'Exit'))
            
            chs = input(' > ')
            if chs[0] == '0':
                print('Bye!')
                exit(0)
            
            print()
            chs = ord(chs[0].upper()) - ord('A')
            data = self.vocabulary.get_vocabulary(chs)
            q = Quiz(data)
            q.run_quiz()

if __name__ == "__main__":
    Main().run()
