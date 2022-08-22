import random


def create_wav_file():
    f = open("wav.scp","w+")
    for i in range(1, 2057):
        line = "a-"+str(i)+" "+"downloads/LJSpeech-1.1/wavs/"+str(i)+".wav\n"
        f.write(line)
    f.close()

def create_text_file():
    with open("ljs_audio_text_train_filelist.txt","r") as f:
        f_write = open("text", "w+")
        for line in f:
            lst = line.split('|')
            sen = "a-" + lst[0] + " " + lst[1] + "\n"
            f_write.write(sen)
            
    f.close()
    f_write.close()

def create_utt2spk():
    f = open("utt2spk","w+")
    for i in range(1, 2057):
        line = "a-"+str(i)+" "+"LJ\n"
        f.write(line)
    f.close()

def create_spk2utt():
    f = open("valid_utt2spk","r")
    f_2 = open("valid_spk2utt","w+")
    f_2.write("LJ ")
    lst = []
    for line in f:
        lst = line.split(" ")
        #print(lst[0] + " ")
        f_2.write(lst[0] + " ")
    f.close()
    f_2.close()

def random_split(file_name):
    f = open(file_name, "r")
    random.seed(123)
    f_train = open("train_text", "w+")
    f_valid = open("valid_text", "w+")
    f_test = open("test_text", "w+")
    for line in f:
        r = random.random()
        if r < 0.8:
            f_train.write(line)
        elif r < 0.9:
            f_valid.write(line)
        else:
            f_test.write(line)
    f.close()
    f_train.close()
    f_valid.close()
    f_test.close()

#create_utt2spk()

random_split("text")

#create_spk2utt()
