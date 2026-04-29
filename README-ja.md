# termsudoku

ターミナル用の数独パズルゲームです。ペンシルマーク、ヒント、-richによる美しいTUI渲染を備えています。

## 特徴

- **Rich TUI** -- カラー表示された网格による美しいターミナルインターフェース
- **ペンシルマーク** -- 各セルの候補数字を記録
- **冲突検出** -- 無効な配置を即座にハイライト
- **プログレッシブヒント** -- 複数の解法テクニックを解説
- **タイマー＆統計** -- 解答時間と手数を記録
- **パズル生成** -- バックトラッキングアルゴリズムによる4つの難易度

## インストール

```bash
pip install termsudoku
```

またはソースから:

```bash
git clone https://github.com/izag8216/termsudoku.git
cd termsudoku
pip install -e .
```

## 使い方

```bash
termsudoku play --difficulty hard
termsudoku play --difficulty easy
```

矢印キーで移動、数字で入力、`h`でヒント。

## 操作

| キー | 動作 |
|------|------|
| 矢印キー | セル移動 |
| 1-9 | セルに数字を入力 |
| Backspace | セルをクリア |
| p | ペンシルマークモード切替 |
| Ctrl+Z | アンドゥ |
| h | ヒントを取得 |
| Space | 一時停止/再開 |
| q | 終了 |

## ライセンス

MIT License
