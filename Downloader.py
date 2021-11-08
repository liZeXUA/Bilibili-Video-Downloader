from requests import get, post

class Download_Bilibili_Video:
    def open_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
                   'Referer': 'https://www.bilibili.com/'}
        res = get(url, headers = headers)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res

    def BV_to_AV(self, bv):
        if bv.isdigit():
            return bv
        bv = list(bv[2:])
        keys = {'1': 13, '2': 12, '3': 46, '4': 31, '5': 43, '6': 18, '7': 40, '8': 28, '9': 5,
                'A': 54, 'B': 20, 'C': 15, 'D': 8, 'E': 39, 'F': 57, 'G': 45, 'H': 36, 'J': 38, 'K': 51, 'L': 42, 'M': 49, 'N': 52, 'P': 53, 'Q': 7, 'R': 4, 'S': 9, 'T': 50, 'U': 10, 'V': 44, 'W': 34, 'X': 6, 'Y': 25, 'Z': 1,
                'a': 26, 'b': 29, 'c': 56, 'd': 3, 'e': 24, 'f': 0, 'g': 47, 'h': 27, 'i': 22, 'j': 41, 'k': 16, 'm': 11, 'n': 37, 'o': 2, 'p': 35, 'q': 21, 'r': 17, 's': 33, 't': 30, 'u': 48, 'v': 23, 'w': 55, 'x': 32, 'y': 14, 'z': 19}
        for i in range(len(bv)):
            bv[i] = keys[bv[i]]
        bv[0] *= (58 ** 6)
        bv[1] *= (58 ** 2)
        bv[2] *= (58 ** 4)
        bv[3] *= (58 ** 8)
        bv[4] *= (58 ** 5)
        bv[5] *= (58 ** 9)
        bv[6] *= (58 ** 3)
        bv[7] *= (58 ** 7)
        bv[8] *= 58
        return str((sum(bv) - 100618342136696320) ^ 177451812)

    def get_video_info(self, aid, cid):
        url = f"https://api.bilibili.com/x/web-interface/view?aid={aid}&cid={cid}"
        res = self.open_url(url).json()
        if res['message'] == '0':
            res = res['data']
            info = {}
            info['title'] = res['title']
            info['intro'] = res['desc']
            info['author'] = res['owner']['name']
            info['stat'] = res['stat']
            return info
        return False

    def get_cid(self, aid):
        res = self.open_url(f"https://api.bilibili.com/x/player/pagelist?aid={aid}&jsonp=jsonp").json()
        if res['message'] == '0':
            cid = res["data"][0]["cid"]
            return cid
        return False

    def download_video(self, aid, cid, filename):
        res = self.open_url(f"https://api.bilibili.com/x/player/playurl?avid={aid}&cid={cid}&qn=64").json()
        url = res["data"]["durl"][0]["url"]
        print(f"Ready to download {filename}...")
        f = open(filename, "ab")
        print("Start downloading...")
        video = self.open_url(url)
        f.write(video.content)
        print("Download completed")

    def main(self):
        bv = input("Please enter video BV or AV number:")
        aid = self.BV_to_AV(bv)
        cid = self.get_cid(aid)
        if not cid:
            print("The BV or AV number you entered is wrong!")
            return False
        info = self.get_video_info(aid, cid)
        self.download_video(aid, cid, info['title'] + ".flv")
        return True

DBV = Download_Bilibili_Video()
if __name__ == "__main__":
    print('''
██████╗       |
██╔══██╗      |    Welcome to Bilibili Video Downloader
██████╔╝      |
██╔══██╗      |    
██████╔╝      |    Version 1.0.0
╚═════╝       |
''')
    try:
        DBV.main()
    except:
        raise RuntimeError("Download error, please try again.")
    finally:
        DBV.main()
