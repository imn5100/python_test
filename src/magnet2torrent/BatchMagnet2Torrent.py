import libtorrent as lt
import time


def magnet2t(link, tfile):
    sess = lt.session()
    params = {
        "save_path": './tfile/',
        "storage_mode": lt.storage_mode_t.storage_mode_sparse,
        "paused": True,
        "auto_managed": True,
        "duplicate_is_error": True
    }

    handle = lt.add_magnet_uri(sess, link, params)
    state_str = ['queued', 'checking', 'downloading metadata', 'downloading',
                 'finished', 'seeding', 'allocating']
    while (not handle.has_metadata()):
        s = handle.status()
        print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % (
            s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.
            num_peers, state_str[s.state])
        time.sleep(5)
        print handle.has_metadata()

    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)

    t = open(tfile, "wb")
    t.write(lt.bencode(torfile.generate()))
    t.close()
    print '%s  generated!' % tfile


def main():
    f = open('magnet_list.txt', 'r')
    magnet_list = f.read().split('\\n')
    f.close()
    for i in range(len(magnet_list)):
        if magnet_list[i] != '':
            magnet2t(magnet_list[i], 'torrent/%s.torrent' % str(i))


if __name__ == '__main__':
    main()
