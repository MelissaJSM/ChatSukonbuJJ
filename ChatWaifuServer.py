from scipy.io.wavfile import write
from text import text_to_sequence
from models import SynthesizerTrn
import utils
import commons
import sys
import re
from pydub import AudioSegment
import torch
from torch import no_grad, LongTensor
import logging
import argparse
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import requests
import os
import openai

chinese_model_path = ".\model\CN\model.pth"
chinese_config_path = ".\model\CN\config.json"
japanese_model_path = ".\model\JP\model.pth"
japanese_config_path = ".\model\JP\config.json"
english_model_path = ".\model\EN\model.pth"
english_config_path = ".\model\EN\config.json"
korean_model_path = ".\model\KR\model.pth"
korean_config_path = ".\model\KR\config.json"
inputVoice = -1

#########################################
#Voice Recognition
q = queue.Queue()
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)
try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])

    if args.model is None:
        model = Model(lang="en-us")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None
        
except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)

def voice_input(language):
    model = Model(lang=language)
    print("You:")
    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                           dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                a = json.loads(rec.Result())
                a = str(a['text'])
                a = ''.join(a.split())
                if(len(a) > 0):
                    print(a)
                    user_input = a
                    return user_input
            if dump_fn is not None:
                dump_fn.write(data)

######Socket######
import socket
ip_port = ('127.0.0.1', 9000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
s.bind(ip_port)
s.listen(5)


### TTS ###
logging.getLogger('numba').setLevel(logging.WARNING)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text


def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text

class vits():
    def __init__(self, model_id):
        if model_id == 0:
            model = chinese_model_path
            config = chinese_config_path
        elif model_id == 1:
            model = japanese_model_path
            config = japanese_config_path
        elif model_id == 2:
            model = english_model_path
            config = english_config_path
        elif model_id == 3:
            model = korean_model_path
            config = korean_config_path

        hps_ms = utils.get_hparams_from_file(config)
        n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
        self.n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0

        self.net_g_ms = SynthesizerTrn(
            self.n_symbols,
            hps_ms.data.filter_length // 2 + 1,
            hps_ms.train.segment_size // hps_ms.data.hop_length,
            n_speakers=n_speakers,
            **hps_ms.model).to(device)
        _ = self.net_g_ms.eval()
        self.hps_ms = hps_ms
        utils.load_checkpoint(model, self.net_g_ms)

    def generateSound(self, inputString, id):
        if self.n_symbols != 0:
            text = inputString

            length_scale, text = get_label_value(
                text, 'LENGTH', 1, 'length scale')
            noise_scale, text = get_label_value(
                text, 'NOISE', 0.667, 'noise scale')
            noise_scale_w, text = get_label_value(
                text, 'NOISEW', 0.8, 'deviation of noise')
            cleaned, text = get_label(text, 'CLEANED')

            stn_tst = get_text(text, self.hps_ms, cleaned=cleaned)
            
            speaker_id = id
            out_path = "output.wav"

            with no_grad():
                x_tst = stn_tst.unsqueeze(0).to(device)
                x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
                sid = LongTensor([speaker_id]).to(device)
                audio = self.net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale,
                                        noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.to(device).cpu().float().numpy()

            write(out_path, self.hps_ms.data.sampling_rate, audio)
            print('Successfully saved!')
            # torch.cuda.empty_cache()

get_dir = lambda x: os.path.split(os.path.realpath(x))[0]

def download_file(url, save_dir):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(os.path.join(save_dir, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

class openai_session():

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        self.messages = []
        self.model = "gpt-3.5-turbo"

    def save(self):
        with open("log.txt", 'w', encoding='utf-8') as f:
            for message in self.messages:
                f.write(message['role'] + ": " + message['content'] + "\n")

    def set_role(self, role):
        prefix = "이제부터 당신은 다음과 같은 역할을 맡아 대화를 진행합니다: \n"
        self.messages.append({"role": "system", "content": prefix + role})

    def set_greeting(self, greeting):
        self.messages.append({"role": "assistant", "content": greeting})
    
    def send_message(self, message):
        try:
            self.messages.append({"role": "user", "content": message})
            res = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages if len(self.messages) <= 10 else self.messages[0] + self.messages[-9:]
            )
            answer = res['choices'][0]['message']['content']
            print(answer)
            self.messages.append({"role": "assistant", "content": answer})
            self.save()
        except:
            answer = "앗.. 뭐라고 하셨었죠? 다시 한번 말씀해 주실 수 있나요?"
            self.messages.append({"role": "assistant", "content": answer})
        return answer

if __name__ == "__main__":
    print("렌파이 클라이언트와 연결 대기중...")
    if not os.path.isfile(korean_model_path):
        os.makedirs(get_dir(korean_model_path), exist_ok=True)
        print("한국어 모델 체크포인트 파일이 없습니다.해당 파일을 다운로드 받습니다.")
        url = 'https://huggingface.co/spaces/skytnt/moe-tts/resolve/main/saved_model/6/model.pth'
        download_file(url, get_dir(korean_model_path))
    if not os.path.isfile(korean_config_path):
        os.makedirs(get_dir(korean_config_path), exist_ok=True)
        print("한국어 모델 설정 파일이 없습니다.해당 파일을 다운로드 받습니다.")
        url = 'https://huggingface.co/spaces/skytnt/moe-tts/resolve/main/saved_model/6/config.json'
        download_file(url, get_dir(korean_config_path))

    client, client_addr = s.accept()
    print("렌파이 클라이언트와 연결되었습니다. 렌파이에서 API KEY를 입력해주세요.")
    print("API KEY는 https://platform.openai.com/account/api-keys 에서 발급할 수 있습니다.")
    total_data = bytes()
    while True:
        data = client.recv(1024)
        total_data += data
        if len(data) < 1024:
            break
    session_token = total_data.decode()

    if(session_token):
        print(f"API KEY: {session_token[-8:]}")
        oai = openai_session(session_token)

        total_data = bytes()
        while True:
            data = client.recv(1024)
            total_data += data
            if len(data) < 1024:
                break
        Setting = total_data.decode()
        oai.set_role(Setting)
        print("배경 설정: "+ Setting)

        total_data = bytes()
        while True:
            data = client.recv(1024)
            total_data += data
            if len(data) < 1024:
                break
        Setting = total_data.decode()
        oai.set_greeting(Setting)
        print("인사말: "+ Setting)

        inputMethod = int(client.recv(1024).decode()) #inputMethod: Keyboard/Voice
        if(inputMethod == 0): #Keyboard
            print("키보드 모드로 설정되었습니다.")
        elif(inputMethod == 1): #voice
            print("음성인식 모드로 설정되었습니다.")
            inputVoice = int(client.recv(1024).decode())  # voiceInputMethod: CN/JP/EN/KO
            if(inputVoice == 0):
                voiceModel = "cn"
                print("입력 언어를 중국어로 설정했습니다.")
            elif(inputVoice == 1):
                voiceModel = "ja"
                print("입력 언어를 일본어로 설정했습니다.")
            elif(inputVoice == 2):
                voiceModel = "en-us"
                print("입력 언어를 영어로 설정했습니다.")
            elif(inputVoice == 3):
                voiceModel = "ko"
                print("입력 언어를 한국어로 설정했습니다.")

        outputMethod = int(client.recv(1024).decode()) #outputMethod: CN/JP
        if(outputMethod == 0):
            print("출력 언어를 중국어로 설정했습니다.")
        elif(outputMethod == 1):
            print("출력 언어를 일본어로 설정했습니다.")
        elif(outputMethod == 2):
            print("출력 언어를 영어로 설정했습니다.")
        elif(outputMethod == 3):
            print("출력 언어를 한국어로 설정했습니다.")

        speaker = int(client.recv(1024).decode())  # outputMethod: CN/JP

        tts = vits(outputMethod)


    while True:
        if(inputMethod == 0): #Keyboard
            total_data = bytes()
            while True:
                data = client.recv(1024)
                total_data += data
                if len(data) < 1024:
                    break
            question = total_data.decode()

        elif(inputMethod == 1): #Voice
            question = voice_input(voiceModel)
            client.send(question.encode())

        print("Question Received: " + question)

        # if (inputVoice == 1 or inputVoice == 2 or inputVoice == -1):
        #     if outputMethod == 0:
        #         question = question + " 使用中文回答"
        #     if outputMethod == 1:
        #         question = question + " 日本語で答えてください"
        #     if outputMethod == 2:
        #         question = question + " Please answer in English"
        #     if outputMethod == 3:
        #         question = question + " 한국어로 답해주세요"

        answer = oai.send_message(question)
        print("ChatGPT:")
        print(answer)
        tts.generateSound(answer, speaker)

        # convert wav to ogg
        src = "./output.wav"
        dst = "./ChatWaifuGameL2D/game/audio/test.ogg"
        sound = AudioSegment.from_wav(src)
        sound.export(dst, format="ogg")
        # send response to UI
        client.send(answer.encode())
        # finish playing audio
        print(client.recv(1024).decode())