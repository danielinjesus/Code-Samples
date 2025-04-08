# 한글 폰트 설치
sudo apt-get update
sudo apt-get install fonts-nanum
=============================
# 설치된 한글 폰트 목록 불러오기(파이썬)
import subprocess
# fc-list 명령어를 사용하여 한글이 지원되는 폰트를 리스트로 가져오기
result = subprocess.run(["fc-list", ":lang=ko", "--format=%{file}\n"], stdout=subprocess.PIPE, text=True)
font_list = result.stdout.splitlines()
print("설치된 한글 폰트 목록:")
for font in font_list:
    print(font)
=============================(출력값)
설치된 한글 폰트 목록:
/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf
/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf
/usr/share/fonts/truetype/nanum/NanumSquareB.ttf
/usr/share/fonts/truetype/nanum/NanumSquareR.ttf
/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf
================================
# 이미지에 bounding box와 텍스트 그리기(파이썬)
draw = ImageDraw.Draw(image)
try:
    font = ImageFont.truetype(font_path, font_size)
except Exception:
    font = ImageFont.load_default()

for item in loaded_results:
    bbox, text, conf = item
    draw.line(bbox + [bbox[0]], fill=(0, 255, 0), width=2)  # bbox 그리기
    text_position = (bbox[0][0], max(bbox[0][1] - 25, 0))
    draw.text(text_position, text, fill=(255, 0, 0), font=font)  # 텍스트 추가

# 주석이 추가된 이미지 저장
image.save(annotated_img_file)
print("Annotated 이미지가 저장되었습니다:", annotated_img_file)