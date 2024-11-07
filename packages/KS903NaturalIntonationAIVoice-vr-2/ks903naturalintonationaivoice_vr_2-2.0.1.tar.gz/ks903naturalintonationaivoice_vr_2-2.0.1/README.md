# README.md

# KS903NaturalIntonationAIVoice_vr_2

## 概要

`KS903NaturalIntonationAIVoice_vr_2` は、自然なイントネーションでテキストを音声化するための音声合成AIライブラリです。このライブラリを使用することで、PDF、DOCX、画像、CSV、およびTXTファイルからテキストを抽出し、日本語および英語で音声とともに表示する機能を提供します。

## インストール

このライブラリは`pip`を使用してインストールできます。また、動作確認としてWindodosの音声合成適用バージョンが必要です。これにより、音声合成機能が実装されています。
使用方法？使い方の例として！
コマンドラインで以下のように実行します。
このライブラリは、`pip` を使用してインストールできます。

以下のコマンドで依存関係をインストールしてください。
```bash
pip install KS903NaturalIntonationAIVoice_vr_2

これで、KS903NaturalIntonationAIVoice_vr_2 を簡単にインストールして利用できるようになります。

使用方法？使い方の例として！
以下のコマンドで KS903NaturalIntonationAIVoice_vr_2 を実行し、指定したファイルからテキストを読み取り、音声出力します。

bash
コードをコピーする

python ks903_say_voice0.py <file_path>


例として、example.pdf というPDFファイルからテキストを抽出して音声合成する場合は次のように実行します：


例として、example.pdf というPDFファイルからテキストを抽出して音声合成する場合は次のように実行します：

bash
コードをコピーする
python ks903_say_voice0.py example.pdf
ファイルを指定せずに起動した場合は、標準入力から直接テキストを入力し、音声合成を行います。

クラスとメソッドの概要
KS903NaturalIntonationAIVoice_vr_2
このクラスは、テキスト抽出と音声合成機能を提供します。

__init__(self)
音声エンジンの初期設定を行います。

extract_text_from_pdf(pdf_path)
PDFファイルからテキストを抽出します。

extract_text_from_docx(docx_path)
DOCXファイルからテキストを抽出します。

extract_text_from_image(image_path)
画像ファイル（JPGまたはPNG）からテキストを抽出します。

extract_text_from_csv(csv_path)
CSVファイルからテキストを抽出します。

extract_text_from_txt(txt_path)
TXTファイルからテキストを抽出します。

extract_text(file_path)
ファイルの種類に応じて適切な抽出メソッドを呼び出し、テキストを取得します。

speech_text(text, lang, times)
指定された言語でテキストを音声合成します。

print_text(text, speech_duration)
テキストを一文字ずつ表示します。

process_text(text)
テキストを処理し、日本語または英語で音声合成と表示を行います。

process_file(file_path)
指定されたファイルからテキストを抽出し、process_text メソッドを使用して音声合成と表示を行います。

ks903_aivoice_vr2_run()
スクリプトのエントリーポイントです。ファイルが指定されていればそれを読み込み、指定がなければ標準入力からテキストを読み取ります。


一括の開発ライブとして

一括Pythonファイル単体でまとめるときは以下の書き方で行います。

# ks903_aivoice_vr2_run.py

from KS903_Natural_Voice_0002 import  KS903NaturalIntonationAIVoice_vr_2

# クラスのインスタンスを生成
instance = KS903NaturalIntonationAIVoice_vr_2()

# ks903_aivoice_vr2_run() メソッドを明示的に呼び出す
instance.ks903_aivoice_vr2_run()


以上のような書き方をすればPYTHONファイルも単体て書き込むことができます。ぜひほかの開発環境にもお試しください。

以上、これでご説明を終わりとします。

