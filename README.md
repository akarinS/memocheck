memocheck.py
==========

Kotoのzアドレスで受け取ったメモを確認する。  

使用準備
----------

    sudo apt install python3

    git clone https://github.com/akarinS/memocheck
    cp memocheck/memocheck.py ~/koto/src/memocheck.py
    chmod u+x ~koto/src/memocheck.py

使用方法
----------

実行

    ~/koto/src/memocheck.py

実行するとzアドレスを選択できるので選んでください。  
そのアドレスで受け取ったメモを見ることができます。  
  
  
memocheck_dev.py
==========

まだ途中！  
Kotoのzアドレスで受け取ったメモを確認する。  
（koto-cliのあるディレクトリに移す必要なし）  

使用準備
----------

    sudo python3 python3-pip
    sudo pip3 requests

    git clone https://github.com/akarinS/memocheck
    chmod u+x memocheck/memocheck_dev.py

今はここを適切に設定することが必要

    """memocheck.py"""
    15: rpcuser = "rpcuser"
    16: rpcpassword = "rpcpassword"
    17: rpcport = "8432"

実行
----------

    ./memocheck/memocheck_dev.py

