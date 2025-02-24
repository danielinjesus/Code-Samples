# pip install googletrans==4.0.0-rc1
import googletrans; translator = googletrans.Translator()

str1 = "날씨가 참 좋네요!"
result1 = translator.translate(str1, src="ko", dest="en")
print(result1.text)