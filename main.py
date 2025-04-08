import re
import numpy as np
from wordcloud import WordCloud
from PIL import Image, ImageDraw, ImageFont

def create_inverted_mask(image_path):
    # 画像をRGBAモードで読み込み
    img = Image.open(image_path).convert('RGBA')
    data = np.array(img)
    
    # 新しい画像配列を作成（白背景に黒のマスク）
    new_data = np.zeros_like(data)
    new_data[..., 3] = 255  # 初期値は完全不透明

    # アルファチャンネルが0（透過）の部分を白に変換
    transparent_area = (data[..., 3] == 0)
    new_data[transparent_area] = [255, 255, 255, 255]  # 白（不透明）

    # アルファチャンネルが255（不透明）の部分を黒に変換
    opaque_area = (data[..., 3] == 255)
    new_data[opaque_area] = [0, 0, 0, 255]  # 黒（不透明）

    # PIL.Image オブジェクトに変換S
    return Image.fromarray(new_data, 'RGBA')

from PIL import Image
word_list = []
with open('./assets/Test/sample.txt', encoding='utf-8') as f:
    text = f.read().replace('\n', '').replace(' ', '')
    
#変数text中に格納されたアンケート内の不要な文字や記号を削除する。
#re.subで正規表現を使った文字列の削除。
text = re.sub('\u3000', '', text)
text = re.sub('・', '', text)
text = re.sub('「', '', text)
text = re.sub('」', '', text)
text = re.sub('（', '', text)
text = re.sub('）', '', text)
#re.subで正規表現を使った文字列の半角空白への置換。
text = re.sub('\n', ' ', text)
text = re.sub('\\n', '', text)
text = re.sub('\\n', ' ', text)

#ユニコード正規化
import unicodedata

text_sample = unicodedata.normalize('NFKC', text)
print('UNICODEの正規化後：{}'.format(text_sample))

# janomeを使った形態素解析
from janome.tokenizer import Tokenizer

#対象のテキストをtokenizeする
t = Tokenizer()
tokenized_text = t.tokenize(text)

words_list=[]
#tokenizeされたテキストをfor文を使ってhinshiとhinshi2に格納する。
for token in tokenized_text:
    tokenized_word = token.surface
    hinshi = token.part_of_speech.split(',')[0]
    hinshi2 = token.part_of_speech.split(',')[1]
    #抜き出す品詞を指定する
    if hinshi == "名詞":
        if (hinshi2 != "数") and (hinshi2 != "代名詞") and (hinshi2 != "非自立"):
            words_list.append(tokenized_word)

words_wakachi=" ".join(words_list)

# マスク画像をRGBAモードで読み込み

mask_image = create_inverted_mask('./assets/Mask/mask.png')
mask = np.array(mask_image)
FONT_PATH='./assets/font/Noto_Sans_JP/static/NotoSansJP_Regular.ttf'


# アルファチャンネルをマスクとして使用
wc = WordCloud(
    font_path='./assets/font/Noto_Sans_JP/static/NotoSansJP_Regular.ttf',
    mask=mask,
    background_color=None,  # 透明背景

    max_font_size=100,
    contour_width=3  ,       # 輪郭線を除去
    random_state=42
).generate(words_wakachi)
wc.to_file('./wagahai.png')
# 最初の単語の情報を取得
first_word_info = wc.layout_[2]
word, font_size, (x, y), _, _ = first_word_info


# 生成したワードクラウド画像を取得
image = wc.to_image()

# 座標を画像に描画して確認
draw = ImageDraw.Draw(image)
# 座標変換関数
def relative_to_pixel(x_rel, y_rel, width, height, scale):
    x = (x_rel) 
    y = (y_rel)
    return (float(x), float(y))

# レイアウト情報をプロット
for i, (word, font_size, (x, y), color, _) in enumerate(wc.layout_):
    x_conv, y_conv = (y + (font_size / 2),x+ (font_size / 2))
    # 中心座標に赤い点を描画
    draw.ellipse([(x_conv-(font_size / 2), y_conv-(font_size / 2)), (x_conv+(font_size / 2), y_conv+(font_size / 2))], fill='red')

# 確認用画像を保存
image.save('wordcloud_with_coordinates.png')