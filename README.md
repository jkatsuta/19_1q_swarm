# お手軽アルゴリズムで、群れっぽい動きをつくってみる。

### 概要
書籍[「作って動かすALife」](https://www.amazon.co.jp/%E4%BD%9C%E3%81%A3%E3%81%A6%E5%8B%95%E3%81%8B%E3%81%99ALife-%E2%80%95%E5%AE%9F%E8%A3%85%E3%82%92%E9%80%9A%E3%81%97%E3%81%9F%E4%BA%BA%E5%B7%A5%E7%94%9F%E5%91%BD%E3%83%A2%E3%83%87%E3%83%AB%E7%90%86%E8%AB%96%E5%85%A5%E9%96%80-%E5%B2%A1-%E7%91%9E%E8%B5%B7/dp/4873118476/ref=sr_1_1?adgrpid=53626124112&amp;hvadid=259131798438&amp;hvdev=c&amp;hvlocphy=1009308&amp;hvnetw=g&amp;hvpos=1t1&amp;hvqmt=e&amp;hvrand=8550447354966873735&amp;hvtargid=kwd-498809778674&amp;jp-ad-ap=0&amp;keywords=%E4%BD%9C%E3%81%A3%E3%81%A6%E5%8B%95%E3%81%8B%E3%81%99alife&amp;qid=1554809467&amp;s=gateway&amp;sr=8-1)の第4章を参考に"群れ"について遊んだ結果（実験）を書いている。

### ブログ
この実験についての詳細は以下通りlab_notebookにまとまっているが、ハイライトをまとめたものは[ブログ](XX)にもまとまっているので参考にどうぞ。

### 構成
- alifebook_lib/
    - 元ネタの同名ライブラリに同じ。
- alifebook_chap04/
    - run_**.py: 元ネタから改変した、群れ作成プログラム。
        - 以下のコマンドで動作する。たとえば、
            - $python run_boid.py --conf {CONFIGURE_FILE} --sleep_time {SLEEP_TIME} --update_ratio {UPDATE_RATIO}
            - {CONFIGURE_FILE}: configures/のファイルを指定。パラメータ毎に群れの振る舞いが変化する。
            - {SLEEP_TIME}: 群れが動き始めるまで停止している時間 (sec; 手動で収録してたので必要だった。普通は必要ない）
            - {UPDATE_RATIO}: 0.0~1.0。lab_notebook/exp4_boid_hunter_update_ratio.ipynb を参照。
    - configures/
        - 設定ファイル。上記のコマンドの引数。
    - lab_notebook/
        - 実験ノート集。以下の順番で見ることを推奨。
        - 実験1: exp1_boid.ipynb
        - 実験2: exp2_boid_prey.ipynb
        - 実験3: exp3_boid_hunter.ipynb
        - 実験4: exp4_boid_hunter_update_ratio.ipynb
    - videos/
        - 実験結果の動画集（実験ノート参照）。

### 元ネタ
- 「作って動かすALife」の[GitHubのlink](https://github.com/alifelab/alife_book_src)
    - このGitHubでは、上記リンクのchap04のコードを改変して使っている。
