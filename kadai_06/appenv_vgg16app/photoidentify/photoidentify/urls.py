"""
URL configuration for photoidentify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# URLの設定
# ユーザーがアプリケーションにアクセスした際のURLとそれに対応するViewの関連付けをする。この関連付けはルーティングと呼ばれる。
# 最初から書いてある。Djangoの管理画面の設定に関する記述。今回のアプリケーションでは管理画面を使わないため不要。消してもよい。
from django.contrib import admin
# 最初から書いてある。「path」関数をインポートする記述。URLとViewを結びつける役割を持つため必要。
from django.urls import path
# 作成したViewの「predict」関数をインポートする記述。URLと「predict」関数との紐づけを可能にする。
from prediction.views import predict

# 最初から書いてある。Djangoの管理画面の設定に関する記述。今回のアプリケーションでは管理画面を使わないため不要。消してもよい。
urlpatterns = [
    path('admin/', admin.site.urls),
    # 「path」関数を使って，ルートURLをViewの「predict」関数と結びつける。
    # 「name='predict'」によりこのURLに「predict」という名称を付けている。
    # この名称はテンプレートやViewからこのURLを参照する際に使用可能。
    # ※ ルートURL：「http://ドメイン/]のこと。ローカル開発環境の場合「http://127.0.0.1:8000/」がルートURLになる。
    path('', predict, name = 'predict'),
]

