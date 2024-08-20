# フォームの作成

# Djangoから「forms」モジュールをimport。
from django import forms

# 「forms」モジュールの「Form」クラスを継承して，画像をアップロードするための「ImageUploadForm」クラスを定義し，「image」変数に代入。
# ※ アップロードするファイルが画像形式である場合「forms.ImageField()」を利用。
class ImageUploadForm(forms.Form):
    image = forms.ImageField()