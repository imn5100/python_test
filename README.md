# python_test</br>
python tools</br>
一些简单的python小工具：</br>
目前包括：</br>
Crawler DMHY的爬虫，获取当日anime更新资源(主要是magnet)。并存储于mysql，使用redis map数据结构判重，避免重复拉取数据。</br>
magnet to torrent .基于libtorrent 的 magnet转torrent,torrent转magnet，torrent下载文件 脚本。</br>
文件下载脚本：通过python调用aria2下载文件，目前支持 http,https,ftp,magnet,torrent 下载方式。支持断点续传。<br>
python 版本2.7<br>
