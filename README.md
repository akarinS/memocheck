memocheck.py
==========

Kotoのzアドレスで受け取ったメモを確認する。  
（memocheck.pyはkoto-cliと同じディレクトリに移す必要がありません。）

使用準備
----------

    sudo apt install python3 python3-pip
    sudo pip3 install requests

    git clone https://github.com/akarinS/memocheck
    chmod u+x ./memocheck/memocheck.py

使用方法
----------

memocheck.pyはどのディレクトリにあっても構いません。

実行

    ./memocheck/memocheck.py

実行したらzアドレスを選択してください。  
選択したアドレスで受け取ったメモを見ることができます。  

注意
---------

memocheck.pyはkoto.confのrpcuserやrpcpasswordを読み込みます。  
これはkotodにデータを要求することだけに使われますが、不安な方はmemocheck_sub.pyを使用してください。  
  
macでも多分動くと思いますが確認はしてません。  
なお、Windowsはサポートしていません。 34~36行目の部分を書き換えると動くかもしれません。  
python3やpip3などは、それぞれのOSのやり方でインストールしてみてください。
  
＊自己責任で使用するようお願いします。
  
  
memocheck_sub.py
==========

Kotoのzアドレスで受け取ったメモを確認する。  
（memocheck_sub.pyはkoto-cliと同じディレクトリに移す必要があります。）

使用準備
----------

    sudo apt install python3

    git clone https://github.com/akarinS/memocheck
    chmod u+x memocheck/memocheck_sub.py

memocheck_sub.pyをkoto-cliと同じディレクトリへ移動

    cp memocheck/memocheck_sub.py 
    
使用方法
----------

実行

    ~/koto/src/memocheck_sub.py

実行したらzアドレスを選択してください。  
選択したアドレスで受けっとたメモを見ることができます。

注意
---------

こちらも確認はしてませんが、macで動くと思います。  
windowsでも、もしかすると動くかもしれません。  
python3は、それぞれのOSのやり方でインストールしてみてください。  
  
＊自己責任で使用するようお願いします。

