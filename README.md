1. 데모 사용법

release 에 가서 

sukonbuTTS.zip과 USE_CONSOLE.zip, USE_CONSOLE.z01 또는  NO_CONSOLE.zip, NO_CONSOLE.z01 을 다운받는다.

USED CONSOLE 은 콘솔이 나오는 버전이며 콘솔에서 대화가 어떻게 진행되는지 확인과 대화 복사가 가능하다..

NO CONSOLE 은 콘솔이 나오지 않는 버전이며 순수 스콘부짱 프로그램만 보인다.

그러나 프로그램을 종료하고도 콘솔창이 뒤에서 도는경우가 있어서 작업관리자에서 직접 종료해야하는 문제점이 생길 수 있음을 참고해야한다. 또한 NOT USED CONSOLE 은 콘솔창이 나오지 않으므로 대화의 복사가 불가하다.


![16](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/a3c09ff6-ef3a-4246-9eb6-b25b84c68656)

다운받은 파일을 압축 푼 다음에 sukonbuTTS.zip에 있는 폴더 2개를 넣어준다.


![17](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/22cbc4b0-196f-4192-8cee-186f4d240bb8)

sukonbuGPT.exe 를 우클릭해서 바탕화면에 바로가기 만들기 한다음에 실행 시킨다.


![18](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/ddc903aa-d69c-4da8-8c4a-038e60351a77)
![19](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/a6c33eed-549a-4364-a577-6195dbc05d85)

이미지와 같이 환경설정 - 프로젝트 경로를 누른다음에 압축 푼 폴더를 잡아준다.

이후 돌아가기를 클릭해서 프로젝트명이 위의 이미지처럼 ChatSukonbuJJ 으로 나온다면 프로젝트 실행을 누르면 동작한다.

2. 직접 빌드하기


![20](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/6bcc565c-bf6c-412d-8760-e5cfed7af1c5)

아나콘다를 다운받는다.

만약, 구할 수 있다면 Anaconda3-2020.11 버전을 구하는것도 좋다.


![21](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/893e2c40-c8ea-41fa-9a22-c32627c09117)

시작메뉴에서 anaconda prompt 를 찾아서 실행한다음에 다음과 같이 입력한다.

conda create -n <name> python=3.8

<name>은 자기가 원하는 이름을 지정해주고 반드시 파이썬 3.8버전으로 한다.


![22](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/809d364c-4c9f-4a7d-884c-554fdb9ee46b)

procced y/n 나오면 y치고 기다린다.


![23](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/b14dad59-5730-4530-be79-76247f58615b)

가상환경 활성화를 위해 다음과 같이 입력한다.

conda activate <name>

<name>은 자기가 원하는 이름을 지정해준다.


![24](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/94d9ac74-ce4a-44db-bdab-27df0b0fae35)

그다음 경로를 수정해준다.

cd <자기가 원하는 경로>

이후 git init 을 통해 github 파일 저장소를 지정해준다.

만약 git init 이 에러가 난다면 pip install git 입력 후 설치되고나서 해보자.

그 이후에 git clone https://github.com/MelissaJSM/ChatSukonbuJJ.git 입력 후 깃허브 파일이 복사가 된다.


![25](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/45e6a24c-6be2-497f-9943-08cd2f233b4c)

cd ChatSukonbuJJ 를 입력해서 깃허브에 다운받은 파일 경로로 이동해준 다음에

python -m venv venv 를 입력 후 venv 가상환경 생성이 됨을 확인 한 다음에

venv\Scripts\activate 를 해준다.

그러면 위의 이미지처럼 가상환경이 잡힌다.


![26](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/ebc938c8-4adb-4bb1-8ca2-9c10e98ce4e7)


pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cu117

를 입력해서 파이토치를 다운받아준다.


![27](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/3a6d4f91-9cb7-4112-9592-bcc5d3b42595)

pip install -r requirements.txt 를 입력해서 필수 파일을 다운받아준다.


![28](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/5b139815-b1dc-426a-9d4f-642b16eb9d03)

깃허브 파일을 다운받은 곳에 릴리즈 링크로 가서 sukonbuTTS.zip를 다운받은다음에 나오는 폴더를 붙여넣기 해준다.


![29](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/4dc90975-2f36-4d67-8e7e-84441c7dd3e5)

마지막으로 python server.py 를 입력해주고 렌파이 클라이언트와 연결 대기중... 이 뜨면 성공이다.
하지만 토큰값이 없어서 정상동작 하진않으니 아래 내용까지 수정해주도록 한다.


![30](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/160e6b90-2884-40d2-b72f-d9b94c724e64)

이후 아나콘다를 꺼버렸다면 이미지와 같이 진행한다.

conda activate <name>

cd <지정한 경로\ChatSukonbuJJ> - 드라이브 까지 다적어야 된다!. ex) cd c:\ChatSukonbuJJ

venv\Scripts\activate


![31](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/ede8de12-52a2-4de0-b483-db8d0dda5f63)

ChatSukonbuJJ 폴더에서 server.py 를 열어보면 다음과 같이 되어있다.

self.model 부분에서 gpt버전을 변경 할 수 있다.
위에 모델리스트를 적어놨으니 그걸 복붙하면 된다.


![32](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/8fc316ae-60d5-44ab-9bfb-46d64fcf29ea)

session_token 분에 open ai api 에서 발급받은 토큰을 입력해주면 된다.


![33](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/55f39022-3334-41af-8119-472c2c0e8ef4)

음성 호출 이름을 변경 할 수 있다.

그런데 스콘부 스콤부 스콤프... 라고 해놓은 이유는 스콘부 라는 발음자체를 제대로 인식 못해서 그렇다.
이후 다시 python server.py 를 하고 난 뒤 폴더 내부에서 renpy-8.0.3-sdk 폴더를 들어 간 뒤 renpy.exe를 실행 시킨다.


![34](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/196d0ecf-a15e-4f3c-b027-9a86adb13425)
![35](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/9c85a14b-2d5b-4515-ba98-ecf2e09c9b03)

ChatSukonbuJJ 경로를 지정해 준 뒤 프로젝트 실행을 해주면 된다.

위의 파일 수정하기에서 scripts, options, gui, screens는 스콘부GPT 프로그램의 이미지와 동작등을 수정 할 수 있으니 천천히 보면 된다.



3. 실행 프로그램 만들기


![36](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/95c8a598-fd68-4873-a95c-8c0eaa90a176)

가상환경 연결까지 다해놓은 상태에서 pip install pyinstaller 를 입력해준다.


![37](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/668741df-8ddf-4d77-b80c-965673dd5830)

다음 중 하나를 입력한다.

실행 시 콘솔창 보임
pyinstaller --icon=window_icon.ico server.py

실행 시 콘솔창 안보임.
pyinstaller -w --icon=window_icon.ico server.py 


![38](https://github.com/MelissaJSM/ChatSukonbuJJ/assets/91932382/0e7c905f-678a-4453-87ad-36ac2fe9f613)

ChatSukonbuJJ 폴더에 dist 라는 폴더가 생겼을거다.

dist 안에 server 폴더안에 _internal, server.exe 파일을 데모판을 다운받은다음에 거기폴더에 넣어주고
ChatSukonbuJJ 폴더내에 ChatSukonbuJJ 폴더가 하나더있을텐데 그거랑 renpy-8.0.3-sdk폴더와 userfile 폴더를 데모판 폴더에 넣어준다.

이후 sukonbuGPT.exe 을 실행시켜주고 렌파이 경로 다시잡아주고 실행하면 된다.

이러면 수정된 파일로 돌아가게된다.


동작 영상

<iframe width="560" height="315" src="https://www.youtube.com/embed/Okx18A8Hs9E?si=mZWXXuinOWPTOI6Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>




