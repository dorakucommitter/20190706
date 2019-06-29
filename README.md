# 実行環境作成

## anacondaを使う場合

1. python3.6実行環境をの作成

    ```bash
    conda create --name=py36 python=3.6
    ```

2. python3.6実行環境への切り替え
    - Linux、macOS

        ```bash
        source activate py36
        ```

    - Windows

        ```console
        activate py36
        ```

## pyenv-virtualenvを使う場合

macOSではbrewコマンドでインストールしてできるので、簡単にインストールできますが、Linuxの場合、aptやyumではインストールできないので、インストール自体が面倒です。Windowsに至ってはインストール方法自体が分かりません。  
Linuxbrewを使えば楽かも知れない、と思いつつ試してはいません．．．

1. インストール
    - macOS

        ```bash
        brew install pyenv
        brew install pyenv-virtualenv
        ```

    - Linux
        - pyenv-virtualenvのインストール

            ```bash
            git clone https://github.com/pyenv/pyenv.git ~/.pyenv
            git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
            ```

        - $HOME/.bashrcへの追加

            ```bash
            export PYENV_ROOT=$HOME/.pyenv
            export PATH=$PYENV_ROOT/bin:$PATH
            if command -v pyenv 1>/dev/null 2>&1; then
                eval "$(pyenv init -)"
            fi
            eval "$(pyenv virtualenv-init -)"
            ```

        - $HOME/.bashrcの再読込み

            ```bash
            source $HOME/.bashrc
            ```

2. python実行環境への切り替え
    - pythonビルドツールのインストール
        - CentOS

            ```bash
            sudo yum -y groupinstall "Development Tools"
            sudo yum -y install readline-devel \
                    zlib-devel bzip2-devel sqlite-devel openssl-devel
            ```

        - Debian系Linux

            ```bash
            sudo apt install -y gcc make \
                    libssl-dev libbz2-dev  \
                    libreadline-dev libsqlite3-dev zlib1g-dev
            ```

    - python3.6実行環境のインストール

        ```bash
        pyenv install 3.6.8
        pyenv virtualenv 3.6.8 mnist
        pyenv activate mnist
        pip install --upgrade pip
        ```

## virtualenvを使う場合

virtualenvの仮装環境は、作成は楽なのですが、pythonのバージョンが切り替えられないので、tensorflowのようにpythonのバージョン縛りがキツいライブラリ使いたい時には使えないことがあります。

```bash
virtualenv virt
source ./virt/bin/activate
pip install --upgrade pip
```

## ライブラリのインストール

- pythonライブラリ

    ```bash
    pip install --upgrade \
        tensorflow keras chainer sklearn \
        opencv-python pillow matplotlib numpy \
        pydotplus graphviz \
        jupyter flask
    ```

- Debian Linux

    ```bash
    sudo apt-get install graphviz
    ```

- macOS

    ```bash
    brew install graphviz
    ```

pipでインストールするgraphvizは、OSにインストールされたgraphvizを呼び出すモジュールなので、OSに本体となるgraphvizをインストールする必要があります。  
requirement.txtをgithubにおいておくと、ライブラリバージョンが抱える脆弱性を指摘するメールが鬱陶しいので、pipコマンドのみにしました。

### jupyter notebookの起動

```bash
jupyter notebook --config=./jupyter_nb_cfg.py --no-browser
```

を実行すると、ネットワーク上の他のPCからパスワードやトークン無しでアクセスできます。セキュリティ的にアレなので、火壁の内側だけで運用する場合だけに限定した方がよいです。  
ちなみに、コンフィグファイルの拡張子は「.py」である必要があるっぽいです。

## よくある？問題

### macOSでmatplitlibとpylabを使おうとしたらRuntimeError

下記の内容で$HOME/.matplotlib/matplotlibrcを作成し、matplitlibの描画バックエンドを指定してあげれば直るようです。

```bash
backend : TkAgg
```

### pyenvの仮想環境でTkinterがimportできない

python環境インストール時にTkのビルドライブラリをインストールしていないと起こる現象らしいです。

```bash
sudo apt-get install tk-dev
pyenv install 3.6.8
```

のような感じで、Tkライブラリインストール後、python環境を新規インストールまたは上書きインストールするとimport出来るようになるはずです。

## dotコマンドが無い

Graphvizというアプリをインストールする必要があります。

- macOS

    ```bash
    brew install graphviz

    ・・・
    ==> libtool
    In order to prevent conflicts with Apple's own libtool we have prepended a "g"
    so, you have instead: glibtool and glibtoolize.
    ```

    libtoolのところでWarning？のようなメッセージが出ることが稀によくあるみたいですが、とりあえずdotコマンド使えたので深く考えないことにして>
います。

- Windows
    [Graphviz - Graph Visualization Software](https://graphviz.gitlab.io/)のDownload → Stable x.xx Windows install packagesからインストーラ
ーファイルをダウンロードできます。
