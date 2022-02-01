base_url = 'https://m.weibo.cn/detail/'
url = 'https://m.weibo.cn/comments/hotflow?id='


Cookie = {
    'Cookie': 'SUB=_2A25MwFUODeRhGeBN61UZ9i_JyzSIHXVsS3tGrDV6PUJbktCOLVGtkW1NRI2sWD_3K_Poll6O4HOJRwtGXo35rtdg; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whqz-SQ7V87zQjpoLCFTnO_5NHD95Qce05N1hqpSK5RWs4DqcjKMcLjUJHEqrHjdsHXPf9DdJ_LwBtt; _T_WM=67984125606; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=958f9a; M_WEIBOCN_PARAMS=luicode=10000011&lfid=100103type%3D1%26q%3Dsilverbullet_Vinkey&fid=1076036307861508&uicode=10000011' # 这里要填
}

headers = {
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': '958f9a',   # 这里要填
    'Accept': 'application/json, text/plain, */*'
}


# 数据id号，要爬取的微博的id号
weiboComment = [{
    'id': 1,
    'weibo_id': 'u/5977512966?uid=5977512966&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D李靓蕾'  # 这里要填
}]
