# Game scripts can be placed in this file.

# Declare the characters used by this game. The color parameter colors the character name.

define e = Character("스콘부짱")
define y = Character("스콘부")
define config.gl2 = True


image bg = "gui/background_2.png"

image sukonbu = Live2D("Resources/Sukonbu", base=.6, loop = True, fade=True)

init python:
    import socket
    import time
    thinking = 0
    total_data = bytes()
    renpy.block_rollback()
    ip_port = ('127.0.0.1', 9000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(ip_port)


# The game starts here.

label start:
    $ renpy.block_rollback()
    scene bg
    show sukonbu m01

    jump chooseMic

label chooseMic:
    $ renpy.block_rollback()
    menu KRmodelChoice:
        e "마이크 사용여부를 체크합니다. \n만약, 마이크가 없다면 무조건 사용하지 않음을 선택하셔야 합니다!\n\n음성 호출 방법 : 스콘부짱 or 후부짱 + 대화내용\n대화 종료 : 스콘부짱 or 후부짱 + 음성 인식 종료"
        "마이크를 사용합니다.":
            python:
                client.send(("1").encode())
        "마이크를 사용하지 않거나 없습니다.":
            python:
                client.send(("0").encode())        
    jump talk_keyboard


label getApiKey:
    $ renpy.block_rollback()

    python:
        token = renpy.input("open AI API KEY를 입력해주세요")
        client.send(token.encode())
    
    jump uploadSetting
    return
    

label uploadSetting:
    $ renpy.block_rollback()
    python:
        token = renpy.input("원하는 배경 설정을 입력해주세요")
        client.send(token.encode())
    jump uploadInit

label uploadInit:
    $ renpy.block_rollback()
    python:
        token = renpy.input("해당 캐릭터의 첫 대사를 입력해주세요")
        client.send(token.encode())
    jump talk_keyboard

    
label talk_keyboard:
    $ renpy.block_rollback()
    
    show sukonbu m01

    python:
        message = renpy.input("스콘부짱에게 무엇을 물어볼까요?")
        client.send(message.encode())
        data = bytes()
    jump checkRes

label checkRes:
    $ renpy.block_rollback()
    if(thinking == 0):
        e "..."

    python:
        client.setblocking(0)
        try:
                data = client.recv(1024)
                total_data += data
        except:
                data = bytes()
                client.setblocking(1)
    
    if(len(data) > 0 and len(data) < 1024):
        python:
            response = total_data.decode()
            total_data = bytes()
            thinking = 0
        jump answer
    else:
        $ renpy.block_rollback()
        e "......"
        $ thinking = 1
        jump checkRes

        


label voice_toggle_on: #토글 온
    $ renpy.block_rollback()
    python:
        message = "Melissa asked sukonbu to toggle on voice mode."
        client.send(message.encode())
        data = bytes()
    jump checkRes_voice_toggle    

label voice_on: #1회용 온
    $ renpy.block_rollback()
    python:
        message = "Melissa asked sukonbu to turn on voice mode."
        client.send(message.encode())
        data = bytes()
    jump checkRes_voice



label checkRes_voice:
    $ renpy.block_rollback()
    if(thinking == 0):
        e "스콘부짱이 음성인식을 동작시켰어요."

    python:
        client.setblocking(0)
        try:
                data = client.recv(1024)
                total_data += data
        except:
                data = bytes()
                client.setblocking(1)
    
    if(len(data) > 0 and len(data) < 1024):
        python:
            response = total_data.decode()
            total_data = bytes()
            thinking = 0
        jump answer
    else:
        $ renpy.block_rollback()
        e "스콘부짱이 음성인식을 동작시켰어요."
        $ thinking = 1
        jump checkRes_voice


label checkRes_voice_toggle:
    $ renpy.block_rollback()
    if(thinking == 0):
        e "스콘부짱이 음성인식을 동작시켰어요."

    python:
        client.setblocking(0)
        try:
                data = client.recv(1024)
                total_data += data
        except:
                data = bytes()
                client.setblocking(1)
    
    if(len(data) > 0 and len(data) < 1024):
        python:
            response = total_data.decode()
            total_data = bytes()
            thinking = 0
        jump answer_toggle
    else:
        $ renpy.block_rollback()
        e "루시아가 음성인식을 동작시켰어요."
        $ thinking = 1
        jump checkRes_voice_toggle        
        


label answer:
    show sukonbu talking
    voice "/audio/test.ogg"
    $ renpy.block_rollback()
    e "[response]"
    voice sustain
    
    $ client.send("음성 재생 완료".encode())
    jump talk_keyboard

label answer_toggle:
    show sukonbu talking
    if response == ("voice is error."):
        jump voice_toggle_on  
    voice "/audio/test.ogg"
    $ renpy.block_rollback()
    e "[response]"
    
    voice sustain
    $ client.send("음성 재생 완료".encode())
    python:
        print("음성 재생 결과 값은 ? : " +response)

    if response == ("음성인식 모드를 종료하는 것이다. 필요하면 바로 준비하는것이다!"):
        jump talk_keyboard
    elif response == ("현재 음성인식 기능을 사용 할 수 없는 것이다."):
        jump talk_keyboard    
    else:
        python:
            message = "sukonbu voice mode loop."
            client.send(message.encode())
            data = bytes()
        jump checkRes_voice_toggle    