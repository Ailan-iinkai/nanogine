#!/bin/bash

# cacheディレクトリを作成
mkdir -p cache

# python3の仮想環境を有効化するなど、適切なPythonの実行環境をセットアップする必要がある場合は、そのコマンドを追加してください。

# requirement.txtを使ってpipでライブラリをインストール
python3 -m pip install -r requirements.txt

# ライブラリのインストールが完了したら、cacheディレクトリ内に作業用ファイルを配置して操作を行うなど、必要な処理を実行できます。
