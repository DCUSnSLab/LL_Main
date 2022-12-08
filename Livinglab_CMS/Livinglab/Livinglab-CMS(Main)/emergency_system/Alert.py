
# 경보음(window 전용)
import pyaudio, wave

# 비상경보
def Alert(que):

    # durationWin = 1000  # milliseconds
    # durationLix = 0.8  # seconds
    # freq = 900         # Hz
    chunk = 1024
    wav_path = 'siren.wav'

    while True:
        p = pyaudio.PyAudio()
        # 호출 신호 확인
        val = que.get()
        if val is not None:

            # # TODO 추후 경고음성으로 대체(ex) pyaudio를 이용하여 삐용삐용음성 재생)
            # if osValue == "Windows":
            #     winsound.Beep(freq, durationWin)
            #
            # # TODO if system's OS is Linux or MAC, then install the module in below
            # # TODO "sudo apt install sox"
            # # TODO When you want to speak some sentense, then install the module in below
            # # TODO "sudo apt install speech-dispatcher"
            # elif osValue == "Linux":
            #     os.system('play -nq -t alsa synth {} sine []'.format(durationLix, freq))
            #     os.system('spd-say "Attention, This is an emergency."')

            with wave.open(wav_path, 'rb') as f:

                stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                                channels=f.getnchannels(),
                                rate=f.getframerate(),
                                output=True)
                data = f.readframes(chunk)

                while data:
                    stream.write(data)
                    data = f.readframes(chunk)

            stream.stop_stream()
            stream.close()
            p.terminate()

