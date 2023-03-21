# Game scripts can be placed in this file.

# Declare the characters used by this game. The color parameter colors the character name.

define e = Character("히요리")
define y = Character("사용자")
define config.gl2 = True

image hiyori = Live2D("Resources/Hiyory", base=.6, loop = True, fade=True)

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
    # Display a background. A placeholder image is displayed here by default, but you can also add a file in the image directory
    # (named bg room.png or bg room.jpg) to display.

    # scene bg library

    # Display character portrait. A placeholder image is used here, but you can also add a named
    # eileen happy.png to replace it.  
    show hiyori m01

    # show eileen happy

    # Lines of dialogue are shown here.


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
    jump inputMethod


label inputMethod:
    $ renpy.block_rollback()
    show hiyori m01
    menu inputMethod1: #input 1
        e "입력 방법을 선택해주세요"

        "키보드 입력":
            python:
                client.send(("0").encode())
                keyboard = True
            jump outputMethod
        "음성인식 입력":
            python:
                client.send(("1").encode())
                keyboard = False
            jump voiceInputMethod
    
    


label voiceInputMethod:
    $ renpy.block_rollback()
    menu inputLanguageChoice: #input 2
        e "입력 언어를 선택해주세요"

        "中文":
            #block of code to run
            python:
                client.send(("0").encode())
            jump outputMethod
        "日本語":
            #block of code to run
            python:
                client.send(("1").encode())
            jump outputMethod
        "영어":
            python:
                client.send(("2").encode())
            jump outputMethod
        "한국어":
            python:
                client.send(("3").encode())
            jump outputMethod


label outputMethod:
    $ renpy.block_rollback()
    menu languageChoice: #input 3
        e "출력 언어를 선택해주세요"

        # "中文":
        #     #block of code to run
        #     python:
        #         client.send(("0").encode())
        #     jump modelChoiceCN
        # "日本語":
        #     #block of code to run
        #     python:
        #         client.send(("1").encode())
        #     jump modelChoiceJP
        # "English":
        #     python:
        #         client.send(("2").encode())
        #     jump modelChoiceEN
        "한국어":
            python:
                client.send(("3").encode())
            jump modelChoiceKR

        
# label modelChoiceCN:
#     $ renpy.block_rollback()
#     menu CNmodelChoice:
#         e "我们来选择一个角色作为语音输出"

#         "綾地寧々":
#             python:
#                 client.send(("0").encode())
#         "在原七海":
#             python:
#                 client.send(("1").encode())
#         "小茸":
#             python:
#                 client.send(("2").encode())
#         "唐乐吟":
#             python:
#                 client.send(("3").encode())
    
#     if keyboard:
#         jump talk_keyboard
#     else:
#         jump talk_voice
    

# label modelChoiceJP:
#     $ renpy.block_rollback()
#     menu JPmodelChoice:
#         e "音声出力するキャラクターを選びましょう"

#         "綾地寧々":
#             python:
#                 client.send(("0").encode())
#         "因幡めぐる":
#             python:
#                 client.send(("1").encode())
#         "朝武芳乃":
#             python:
#                 client.send(("2").encode())
#         "常陸茉子":
#             python:
#                 client.send(("3").encode())
#         "ムラサメ":
#             python:
#                 client.send(("4").encode())
#         "鞍馬小春":
#             python:
#                 client.send(("5").encode())
#         "在原七海":
#             python:
#                 client.send(("6").encode())

#     if keyboard:
#         jump talk_keyboard
#     else:
#         jump talk_voice

# label modelChoiceEN:
#     $ renpy.block_rollback()
#     menu ENmodelChoice: #input 0
#         e "Choose a character to output voice"

#         "Aya":
#             python:
#                 client.send(("0").encode())

label modelChoiceKR: # 수아, 미미르, 아린, 연화, 유화, 선배
    $ renpy.block_rollback()
    menu KRmodelChoice:
        e "음성 출력할 캐릭터를 선택해주세요"

        "수아":
            python:
                client.send(("0").encode())
        "미미르":
            python:
                client.send(("1").encode())
        "아린":
            python:
                client.send(("2").encode())
        "연화":
            python:
                client.send(("3").encode())
        "유화":
            python:
                client.send(("4").encode())
        "선배":
            python:
                client.send(("5").encode())


    if keyboard:
        jump talk_keyboard
    else:
        jump talk_voice
    
label talk_keyboard:
    $ renpy.block_rollback()
    show hiyori m02
    python:
        message = renpy.input("나：")
        client.send(message.encode())
        data = bytes()
    jump checkRes


label talk_voice:
    $ renpy.block_rollback()
    if(thinking == 0):
        show hiyori m02
    y "나："
    python:
        client.setblocking(0)
        try:
                finishInput = client.recv(1024)
        except:
                finishInput = bytes()
                client.setblocking(1)

    if(len(finishInput) > 0):
        $ finishInput = finishInput.decode()
        $ renpy.block_rollback()
        y "[finishInput]"
        $ thinking = 0
        jump checkRes
    $ thinking = 1
    jump talk_voice


label checkRes:
    $ renpy.block_rollback()
    if(thinking == 0):
        show hiyori m03
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

        


label answer:
    show hiyori talking
    voice "/audio/test.ogg"
    $ renpy.block_rollback()
    e "[response]"
    voice sustain
    
    if keyboard:
        $ client.send("음성 재생 완료".encode())
        jump talk_keyboard
    else:
        $ client.send("음성 재생 완료".encode())
        jump talk_voice