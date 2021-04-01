# import python models
import urllib.request as request
import urllib.parse as parse
from lxml import etree
from pydub import AudioSegment
import os
from colorama import init


def removefiles(lists):
    for i in lists:
        fileName = i['word'] + '.mp3'
        try:
            os.remove(fileName)
        except Exception as e:
            print(e)


class FindWord:
    def __init__(self, word):
        self.baseUrl = 'https://dictionary.cambridge.org'
        chineseUrlTmp = '/zhs/词典/英语-汉语-简体/'
        chineseUrl = parse.quote(chineseUrlTmp)
        url = self.baseUrl + chineseUrl + word
        self.word = word
        self.url = url

    def getaudio(self):
        requestData = ('user-agent',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57')
        opener = request.build_opener()
        opener.addheaders = [requestData]
        request.install_opener(opener)
        data = request.urlopen(self.url).read().decode('utf-8')
        treeData = etree.HTML(data)
        xpath1 = '//*[@id="ampaudio1"]/source[1]/@src'
        xpath2 = '//*[@id="ampaudio2"]/source[1]/@src'
        audio1 = treeData.xpath(xpath1)
        self.audio1 = self.baseUrl + audio1[0]
        audio2 = treeData.xpath(xpath2)
        self.audio2 = self.baseUrl + audio2[0]

    def putaudio(self):
        return self.audio1, self.audio2


if __name__ == '__main__':
    wordKeys = input('words(ex: word1 word2 ...): ')
    choiceSort = input('need sort words?(y/n): ')
    if choiceSort == 'y' or choiceSort == 'Y':
        wordsTmp = sorted(wordKeys.split(' '))
    else:
        wordsTmp = wordKeys.split(' ')
    words = []
    for i in wordsTmp:
        if i in words:
            print('word: {} is repeat'.format(i))
        else:
            words.append(i)
    choiceSplit = input('need auto split?(y/n): ')
    if choiceSplit == 'y' or choiceSplit == 'Y':
        result = []
        failedresult = []
        wordNumber = 1
        listenNumber = 1
        for i in words:
            try:
                word = FindWord(i)
                word.getaudio()
                tmpUrl = word.putaudio()[0]
                result.append({'word': i, 'audio': tmpUrl})
                fileName = i + '.mp3'
                fileName2 = i + '.mp31'
                request.urlretrieve(tmpUrl, filename=fileName2)
                tmpMp3 = AudioSegment.from_mp3(fileName2)
                silentAudio = AudioSegment.silent(1000)
                emptyAudio = AudioSegment.empty()
                emptyAudio += silentAudio
                emptyAudio += tmpMp3
                emptyAudio.export(fileName)
                os.remove(fileName2)
                print('success download audio, word: {}'.format(i))
                # print(tmpUrl)
                # print('finish word: {}'.format(i))
            except:
                print('failed word: {}'.format(i))
                failedresult.append(i)
        try:
            sleepTime = int(input('interval time?: '))
        except:
            print('input value not rule of type, default value is 1.')
            sleepTime = 1
        repeatChoice = input('need repeat?(y/n):')
        if (repeatChoice == 'y') or (repeatChoice == 'Y'):
            number = int(input('number of repeat time:'))
            print('merge audio files......')
            audioTmp = AudioSegment.empty()
            silentAudio = AudioSegment.silent((sleepTime - 1) * 1000)
            silentAudio2 = AudioSegment.silent(1000)
            audioTmp += silentAudio2
            for i in result:
                # print(i['word'], end=' ')
                for j in range(number):
                    fileName = i['word'] + '.mp3'
                    try:
                        mpsFile = AudioSegment.from_mp3(fileName)
                        audioTmp += mpsFile
                        audioTmp += silentAudio
                    except:
                        failedresult.append(fileName)
                        break
                if wordNumber % 20 != 0:
                    wordNumber += 1
                else:
                    outName = 'listen-' + str(listenNumber) + '.mp3'
                    print('output audio file {}'.format(outName))
                    audioTmp.export(outName)
                    listenNumber += 1
                    del audioTmp
                    audioTmp = AudioSegment.empty()
                    audioTmp += silentAudio2
                    wordNumber += 1
            outName = 'listen-' + str(listenNumber) + '.mp3'
            audioTmp.export(outName)
            print('merge audio files successful!')
        else:
            # print('successful find words:')
            print('merge audio files......')
            audioTmp = AudioSegment.empty()
            silentAudio = AudioSegment.silent(((sleepTime - 1) * 1000))
            silentAudio2 = AudioSegment.silent(1000)
            audioTmp += silentAudio2
            for i in result:
                # print(i['word'], end=' ')
                fileName = i['word'] + '.mp3'
                try:
                    mpsFile = AudioSegment.from_mp3(fileName)
                    audioTmp += mpsFile
                    audioTmp += silentAudio
                except:
                    failedresult.append(fileName)
                if wordNumber % 20 != 0:
                    wordNumber += 1
                else:
                    outName = 'listen-' + str(listenNumber) + '.mp3'
                    print('output audio file {}'.format(outName))
                    audioTmp.export(outName)
                    listenNumber += 1
                    del audioTmp
                    audioTmp = AudioSegment.empty()
                    audioTmp += silentAudio2
                    wordNumber += 1
                outName = 'listen-' + str(listenNumber) + '.mp3'
                audioTmp.export(outName)
            # audioTmp.export('listen.mp3')
            # print('merge audio files successful!')
        init(autoreset=True)
        print('\033[32msuccess find words:\033[0m')
        for i in result:
            print(i['word'], end=' ')
        print()
        if len(failedresult) != 0:
            print('\033[31mcan not find words:\033[0m')
            for i in failedresult:
                print(i, end=' ')
            print()
        commChoice = input('remove all audio files?(y/n): ')
        if commChoice == 'y' or commChoice == 'Y':
            removefiles(result)
        # elif commChoice == 'Y':
        #     removefiles(result)
        else:
            print('not delete audio files')
        file1 = open('result.txt', 'w+')
        file1.write('success find words: ')
        for i in result:
            content = str(i['word']) + ' '
            file1.write(content)
        if len(failedresult) != 0:
            file1.write('\n')
            file1.write('can not find words: ')
            for i in failedresult:
                content = str(i) + ' '
                file1.write(content)
        file1.close()
        tmp1 = input('enter any key to exit....')
    else:
        result = []
        failedresult = []
        for i in words:
            try:
                word = FindWord(i)
                word.getaudio()
                tmpUrl = word.putaudio()[0]
                result.append({'word': i, 'audio': tmpUrl})
                fileName = i + '.mp3'
                fileName2 = i + '.mp31'
                request.urlretrieve(tmpUrl, filename=fileName2)
                tmpMp3 = AudioSegment.from_mp3(fileName2)
                silentAudio = AudioSegment.silent(1000)
                emptyAudio = AudioSegment.empty()
                emptyAudio += silentAudio
                emptyAudio += tmpMp3
                emptyAudio.export(fileName)
                os.remove(fileName2)
                print('success download audio, word: {}'.format(i))
                # print(tmpUrl)
                # print('finish word: {}'.format(i))
            except:
                print('failed word: {}'.format(i))
                failedresult.append(i)
        try:
            sleepTime = int(input('interval time?: '))
        except:
            print('input value not rule of type, default value is 1.')
            sleepTime = 1
        repeatChoice = input('need repeat?(y/n):')
        if (repeatChoice == 'y') or (repeatChoice == 'Y'):
            number = int(input('number of repeat time:'))
            print('merge audio files......')
            audioTmp = AudioSegment.empty()
            silentAudio = AudioSegment.silent((sleepTime - 1) * 1000)
            silentAudio2 = AudioSegment.silent(1000)
            audioTmp += silentAudio2
            for i in result:
                # print(i['word'], end=' ')
                for j in range(number):
                    fileName = i['word'] + '.mp3'
                    try:
                        mpsFile = AudioSegment.from_mp3(fileName)
                        audioTmp += mpsFile
                        audioTmp += silentAudio
                    except:
                        failedresult.append(fileName)
                        break
            audioTmp.export('listen.mp3')
            print('merge audio files successful!')
        else:
            # print('successful find words:')
            print('merge audio files......')
            audioTmp = AudioSegment.empty()
            silentAudio = AudioSegment.silent(((sleepTime - 1) * 1000))
            silentAudio2 = AudioSegment.silent(1000)
            audioTmp += silentAudio2
            for i in result:
                # print(i['word'], end=' ')
                fileName = i['word'] + '.mp3'
                try:
                    mpsFile = AudioSegment.from_mp3(fileName)
                    audioTmp += mpsFile
                    audioTmp += silentAudio
                except:
                    failedresult.append(fileName)
            audioTmp.export('listen.mp3')
            print('merge audio files successful!')
        init(autoreset=True)
        print('\033[32msuccess find words:\033[0m')
        for i in result:
            print(i['word'], end=' ')
        print()
        if len(failedresult) != 0:
            print('\033[31mcan not find words:\033[0m')
            for i in failedresult:
                print(i, end=' ')
            print()
        commChoice = input('remove all audio files?(y/n): ')
        if commChoice == 'y' or commChoice == 'Y':
            removefiles(result)
        # elif commChoice == 'Y':
        #     removefiles(result)
        else:
            print('not delete audio files')
        file1 = open('result.txt', 'w+')
        file1.write('success find words: ')
        for i in result:
            content = str(i['word']) + ' '
            file1.write(content)
        if len(failedresult) != 0:
            file1.write('\n')
            file1.write('can not find words: ')
            for i in failedresult:
                content = str(i) + ' '
                file1.write(content)
        file1.close()
        tmp1 = input('enter any key to exit....')
