# Romaji-phonem

[![PyPI version](https://badge.fury.io/py/romaji-phonem.svg)](https://pypi.org/project/romaji-phonem)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

アルファベット列をローマ字読みする軽量 Python ライブラリ.

このライブラリは日本語話者に固有な文化に合わせて開発されているため,
ドキュメントは日本語のみで書かれています.

This documentation is written only in Japanese,
because this library is developed for the unique culture of Japanese speakers.

## 概要

テキスト中に現れるアルファベット列を, それをローマ字読みしたカタカナ列に変換します.
[ヘボン式ローマ字](https://ja.wikipedia.org/wiki/%E3%83%98%E3%83%9C%E3%83%B3%E5%BC%8F%E3%83%AD%E3%83%BC%E3%83%9E%E5%AD%97)
を参考にしつつ, 規則に現れないアルファベット列に対処したり,
多少英語に近い発音になるようチューニングしています.

このライブラリは, アルファベット交じりのテキストを音声合成エンジンに入力する目的で開発されました.
たとえば, [VOICEVOX](https://voicevox.hiroshiba.jp/) は ver. 0.21.1 時点で,
アルファベットをアルファベットのまま読み上げるようになっています.
アルファベットの列をそれらしいカタカナに変換することで,
とりあえず流暢な音声を合成することを目指しました.

変換は完全にルールベースで行われ, 記号として聞き取れるレベルを目指しています.
英単語として正しい読み方は目指していません.

その代わり, 依存ライブラリは全くなく, Python のみで書かれており,
非常に簡単に動作させることができます.

## インストール

```shell
pip install romaji-phonem
```

## 使い方・仕様

半角アルファベット列を含む文字列を入力すると, それらしいカタカナを出力します.

```
>>> from romajiphonem import phonemize
>>> phonemize("an apple")
'アン・アップレ'
>>> phonemize("Flutter Mane")
'フルッテア・マネ'

```

アルファベット 3 文字以上のものを変換します. 2 文字の連続はそのまま残ります.

```
>>> phonemize("相手のIncineroarのDDラリアット!")
'相手のインシネロアアのDDラリアット!'

```

## ライセンス

[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

Copyright (c) 2024 もち (Mochi)
