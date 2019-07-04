import json
import os
import re
import threading
from datetime import datetime as DT
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
        text = re.sub('[<>:"/|?*]', '_', text)
        path = os.path.join(VoiceManager.VOICE_PATH, '%s.mp3' % text)

        return path

    def play(self, text):
        vpath = self.get_path(text)
        if not self.voice.get(text, None):
            tts = gTTS(text=text, lang='en')
            tts.save(vpath)
        playsound(vpath)

class QuizResult:
    RESULT_PATH = './results'
    
    def __init__(self, title):
        self.title = title
        self.wrong = 0
        self.correct = 0
        self.time_cost = time()
        self.answer_pair = [('[Answer]', '[User Input]')]
    
    def summarize(self):
        self.time_cost = time() - self.time_cost
        self.total = self.wrong + self.correct
        self.acc = self.correct / self.total * 100
        self.finish_date = DT.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save()

    def __str__(self):
        return '\n'.join([
            '=== Result ===',
            'Title: %s' % self.title,
            'Correct: {0.correct}/{0.total}'.format(self),
            'Accuracy: %5.2f%%' % self.acc,
            'Time Cost: %.1fs' % self.time_cost,
            'Finish Date: %s\n' % self.finish_date,
        ])
    
    def save(self):
        if not os.path.exists(QuizResult.RESULT_PATH):
            os.mkdir(QuizResult.RESULT_PATH)
        filename = 'result_%s_%s.txt' % (DT.now().strftime('%Y-%m-%d_%H%M%S'), self.title)
        with open(os.path.join(QuizResult.RESULT_PATH, filename), 'w', encoding='UTF-8') as fout:
            fout.write(str(self))
            fout.write('\n=== Answering Detail ===\n')
            alen, blen = 0, 0
            for a, b in self.answer_pair:
                alen = max(alen, len(a))
                blen = max(blen, len(b))
            for a, b in self.answer_pair:
                fout.write('%-*s | %-*s\n' % (alen, a, blen, b))

class ResultRecords:
    RECORDS_PATH = './results/records.json'
    
    def __init__(self):
        self.records = self._load_records()
    
    def _load_records(self):
        if not os.path.exists(ResultRecords.RECORDS_PATH):
            return dict()
        with open(ResultRecords.RECORDS_PATH, 'r', encoding='UTF-8') as fin:
            return json.load(fin)
    
    def _save_records(self):
        with open(ResultRecords.RECORDS_PATH, 'w', encoding='UTF-8') as fout:
            json.dump(self.records, fout, ensure_ascii=False, indent=2)
    
    def get_record(self, title):
        return self.records.get(title, 0)
    
    def update_record(self, result):
        acc = self.get_record(result.title)
        self.records[result.title] = max(result.acc, acc)
        self._save_records()

class Vocabulary:
    DATA_PATH = './data'
    
    def __init__(self):
        self.vocabulary = self._load_vocabulary()
        self.title_list = self._get_title_list()

    def get_vocabulary(self, idx):
        shuffle(self.vocabulary[idx]['vocabulary'])
        return self.vocabulary[idx]

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
        self.title = data['title']
        self.data = data['vocabulary']
        self.vm = VoiceManager()
    
    def run_quiz(self):
        data = self.data
        result = QuizResult(self.title)
        for d in data:
            print(d['cht'])
            ans = input(' > ')
            if ans != d['eng']:
                result.wrong += 1
                result.answer_pair.append((d['eng'], '**%s**' % ans))
                print('Wrong: %s' % d['eng'])
            else:
                result.correct += 1
                result.answer_pair.append((d['eng'], ans))
                print('Correct!')
            print()
            Thread(target=self.vm.play, args=(d['eng'], )).start()
        result.summarize()
        print(result)
        return result

class Main:
    def __init__(self):
        self.vocabulary = Vocabulary()
        self.records = ResultRecords()
    
    def run(self):
        while True:
            print('=== Choose Vocabulary Set ===')
            for i, t in enumerate(self.vocabulary.title_list):
                print('[%s] %s' % (chr(i+ord('A')), t), end=' ')
                acc = self.records.get_record(t)
                if acc > 0:
                    print('[%.0f%%]' % acc, end='')
                print()
            print('[%s] %s' % ('0', 'Exit'))
            
            chs = input(' > ')
            while chs == '':
                chs = input(' > ')
            
            if chs == '0':
                print('Bye!')
                exit(0)
            
            print()
            chs = ord(chs[0].upper()) - ord('A')
            
            data = self.vocabulary.get_vocabulary(chs)
            q = Quiz(data)
            result = q.run_quiz()
            self.records.update_record(result)

if __name__ == "__main__":
    Main().run()
