# predict関数で使用するライブラリをimport。
# Djangoが提供する「render」関数をimport。「render」関数は特定のテンプレートとデータを元にHTMLを作成。
from django.shortcuts import render
# 「ImageUploadForm」クラスをimport。「views.py」で「ImageUploadForm」クラスを利用できるようにする。
from .forms import ImageUploadForm
# Djangoのプロジェクト設定情報を取り扱うモジュールをインポート。
from django.conf import settings
# Kerasの「load_model」関数をインポート。予測モデルを読み込むために使用。
from tensorflow.keras.models import load_model
# Kerasの「load_img」関数と「img_to_array」関数をインポート。アップロードされた画像を予測モデルに入力できる形式へと変換するために使用。
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
# 入力データの前処理に使う「preprocess_input」関数と出力データの情報取得に使う「decode_predictions」関数をimport。
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
# 主にデータの取り扱いを担う「io」モジュールの「BytesIO」をインポート。アップロードされた画像ファイルを予測モデルに適した形式へ変換するために使用。
from io import BytesIO
# OS関連の操作をする「os」モジュールをインポート。予測モデルのファイルパスを生成するために使用。
import os

# predict関数とリクエストによる処理の分岐の実装。
# アクセスがGETリクエスト（ユーザーがアプリケーションのトップページへ通常通りアクセスする場合）か，
# POSTリクエスト（「判定」ボタンをクリックしてトップページが表示される場合）かによって処理を分岐させる。
# リクエストを受け取って処理を行う「predict」関数を定義。
def predict(request):
    # HTTPメソッドによって処理を分岐。GETメソッドはブラウザで特定のURLにアクセスするときに使用される。
    if request.method == 'GET':
        # 新たな画像アップロードフォームを生成し「form」変数に代入。
        # 「ImageUploadForm()」の引数に何も指定しない場合，アップロードフォームの初期状態（フォームに画像をアップロードしていない空の状態）を生成。
        form = ImageUploadForm()

        # HTMLテンプレートを生成・表示させるための処理。
        # 「render」関数は指定されたテンプレート（本教材では「home.html」）を用いてHTMLを生成し，リクエスト元にレスポンスする役割を持つ。
        # 1つ目の引数はリクエスト情報を含むオブジェクト。「render」関数に渡すことで，リクエストに関連する情報をHTMLテンプレートが利用できるようになる。
        # 2つ目の引数は表示するHTMLテンプレートのファイルの名前。
        # 3つ目の引数は連想配列。「'form'」というキーに「form」変数（画像アップロードのフォーム）を値として設定。
        # 「'home.html'」テンプレート内で「form」変数を活用して画像アップロードフォームを表示できるようになる。
        return render(request, 'home.html', {'form': form})
    
    # HTTPメソッドによって処理を分岐。POSTメソッドはフォームを通じてデータを送信するときに使用される。
    if request.method == 'POST':
        # POSTリクエストで送信されたデータを引数として「ImageUploadForm」クラスのインスタンスを作成し，「form」変数に代入。
        # 「request.POST」はファイル以外の送信されたデータ，「request.FILES」は送信されたファイルを意味する。
        form = ImageUploadForm(request.POST, request.FILES)
        # 送信されたフォームのデータが適切か（例：必要なフィールドが全部含まれているか，画像が破損していないかなど）をチェック。
        if form.is_valid():
            # フォームから送信された画像データを取得して「img_file」変数に代入。「form.cleaned_data」は送信されたデータの連想配列。
            # 「'image'」というキーに対応するデータはアップロードされた画像。
            img_file = form.cleaned_data['image']
            # アップロードフォームから取得した画像データを，画像ファイルのように扱えるよう変換。
            img_file = BytesIO(img_file.read())

            # ここから予測モデルに合わせた前処理。
            # 画像ファイルをロードし，サイズを縦256ピクセル×横256ピクセルにリサイズ。
            img = load_img(img_file, target_size = (224, 224))
            # 予測モデルにインプットする形（array形式）に変換。
            img_array = img_to_array(img)
            # 予測モデルの入力データの形状に合わせて配列を変換。（サンプル数，画像の縦ピクセル数，画像の横ピクセル数，画像の色のチャネル数）
            img_array = img_array.reshape((1, 224, 224, 3))
            # preprocess_inputで前処理。
            img_array = preprocess_input(img_array)

            # 「os」モジュールの「path.join」関数を使用して予測モデルのファイルパスを生成。「path.join」関数は引数を結合してパスを生成。
            # 「settings.BASE_DIR」はDjangoのプロジェクトのルートディレクトリを表すため，
            # 「os.path.join(settings.BASE_DIR, 'prediction', 'models', 'model.h5')」はプロジェクトのルートディレクトリからの予測モデルの相対パスを表す。
            model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'vgg16.h5')
            # 「load_model」関数で予測モデルをロード。「path.join」によって生成したパスを活用してモデルを指定。
            model = load_model(model_path)
            # 予測モデルを使って画像データの判定をし，予測結果を「result」変数に代入。
            # 予測結果は配列形式で返される。1つ目の要素が猫である確率，2つ目の要素が犬である確率。
            # 「result」変数が[0.2, 0.8]である場合は画像が猫である確率は0.2（20%），犬である確率は0.8（80%）であることを意味する。
            result = model.predict(img_array)

            # 予測結果（可能性の高い上位5つのカテゴリとそのカテゴリに属する確率）を変数に代入。
            prediction = decode_predictions(result, top = 5)[0]

            # リクエストデータから「img_data」というキーの値を取得。
            # 「img_data」キーの値はhome.htmlにおいて，name属性が「img_data」である隠しフィールドに設定した画像データ。
            img_data = request.POST.get('img_data')

            # 「home.html」というテンプレートを使って画像アップロードフォームと予測結果を表示するHTMLを生成。
            # 「prediction」変数を活用して予測結果を表示するために3つ目の引数に，予測結果である「prediction」変数，
            # 画像データをHTMLテンプレートへ渡してHTMLテンプレート内で画像データも使用できるように「'img_data': img_data」を追加。
            return render(request, 'home.html', {'form': form, 'prediction': prediction, 'img_data': img_data})
        
        # 「form.is_valid()」が「False」だった場合GETリクエストと同様の処理を行う。
        else:
            form = ImageUploadForm()
            return render(request, 'home.html', {'form': form})

