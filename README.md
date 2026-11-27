# レコメンドシステム

飲食店レコメンドの試作です。グルメアプリ「Gohan」のレコメンド方法を検討するために作りました。

## 仕組み

1. 質問に y/n で答えていくと、好みのジャンル・価格帯・距離・最低評価からユーザープロフィールを作ります
2. 店舗データ（ジャンル、価格帯、評価、距離など）を pandas で用意し、特徴量を標準化します
3. プロフィールと各店舗のコサイン類似度を計算し、似ている順におすすめを出します

実行した様子:

![実行画面](img/image.png)

## 実行方法

```bash
git clone

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate  # Windows

# パッケージのインストール
pip install -r requirements.txt

# アプリの実行
python3 main.py
```

# requiremets.txtの更新
requirements.txtを一度消すこと
``` bash
rm requirements.txt

pip install pipreqs

# 現在のディレクトリを確認
pwd
# 出力例: /Users/username/project

# プロジェクトディレクトリで pipreqs を実行
pipreqs /Users/username/project

```