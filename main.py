import math
import requests
import re
import json
import time
avidmatch = re.compile(r"[a|A][v|V]([0-9]+)")
bvidmatch = re.compile(r"[b|B][v|V]([a-zA-Z0-9]{10})")
videoid = str(input("请输入视频的avid/BVid:"))
if avidmatch.match(videoid):
    avid = videoid[2:]
elif bvidmatch.match(videoid):
    bv = videoid
    BvNo1 = bv[2:]
    keys = {'1':'13', '2':'12', '3':'46', '4':'31', '5':'43', '6':'18', '7':'40', '8':'28', '9':'5','A':'54', 'B':'20', 'C':'15', 'D':'8', 'E':'39', 'F':'57', 'G':'45', 'H':'36', 'J':'38', 'K':'51', 'L':'42', 'M':'49', 'N':'52', 'P':'53', 'Q':'7', 'R':'4', 'S':'9', 'T':'50', 'U':'10', 'V':'44', 'W':'34', 'X':'6', 'Y':'25', 'Z':'1','a': '26', 'b': '29', 'c': '56', 'd': '3', 'e': '24', 'f': '0', 'g': '47', 'h': '27', 'i': '22', 'j': '41', 'k': '16', 'm': '11', 'n': '37', 'o': '2','p': '35', 'q': '21', 'r': '17', 's': '33', 't': '30', 'u': '48', 'v': '23', 'w': '55', 'x': '32', 'y': '14','z':'19'}
    BvNo2 = []
    for index, ch in enumerate(BvNo1):
        BvNo2.append(int(str(keys[ch])))
    BvNo2[0] = int(BvNo2[0] * math.pow(58, 6));
    BvNo2[1] = int(BvNo2[1] * math.pow(58, 2));
    BvNo2[2] = int(BvNo2[2] * math.pow(58, 4));
    BvNo2[3] = int(BvNo2[3] * math.pow(58, 8));
    BvNo2[4] = int(BvNo2[4] * math.pow(58, 5));
    BvNo2[5] = int(BvNo2[5] * math.pow(58, 9));
    BvNo2[6] = int(BvNo2[6] * math.pow(58, 3));
    BvNo2[7] = int(BvNo2[7] * math.pow(58, 7));
    BvNo2[8] = int(BvNo2[8] * math.pow(58, 1));
    BvNo2[9] = int(BvNo2[9] * math.pow(58, 0));
    sum = 0
    for i in BvNo2:
        sum += i
    sum -= 100618342136696320
    temp = 177451812
    avid = sum ^ temp 
else:
    print("What's up!你看看你输入了个啥?")
    exit(1)
def billibili_urlcatch(url):
    param = {"aid" : avid}
    head = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0  uacq" }
    try:
        get = requests.get(url , headers=head , params=param)
        dictionary = get.json()
    except:
        print("没有获取到任何信息! 请检查您的网络链接!")
        exit(1)
    if dictionary["code"] == 0:
        pass
    elif dictionary["code"] == -400:
        print("请求错误, 请检查您输入的av/BV号是否正确")
        exit(1)
    elif dictionary["code"] == -403:
        print("您没有权限查看该视频的信息")
        exit(1)
    elif dictionary["code"] == -404:
        print("没有找到这个视频, 请检查您输入的av/BV号所对应的视频是否存在")
        exit(1)
    elif dictionary["code"] == 62002:
        print("稿件目前没有开放浏览")
        exit(1)
    elif dictionary["code"] == 62004:
        print("稿件还在审核中, 如果您需要催审可以联系B站官方客服")
        exit(1)
    elif not dictionary["code"] is None:
        print("您的请求有误! 错误代码为: " + str(dictionary["code"]) + " , 报错提示信息为: " + str(dictionary["message"]))
        exit(1)
    else:
        print("程序出现了其它错误")
        exit(3)
    return dictionary["data"]
information = billibili_urlcatch(f"https://api.bilibili.com/x/web-interface/view")#视频详细信息
state = billibili_urlcatch(f"https://api.bilibili.com/x/web-interface/archive/stat")#视频状态
def is_key_right(key1,key2):
    if key1 == key2:
        return key1
    else:
        print("数据校验出现错误!")
        exit(1)
aid = is_key_right(information["aid"],state["aid"])
bvid = is_key_right(information["bvid"],state["bvid"])
cpr = is_key_right(information["copyright"],state["copyright"])
subtitle = information["subtitle"]
owner = information["owner"]
print("稿件标题: "+information["title"])
print("av号: av"+str(aid))
print("BV号: "+bvid)
print("稿件分区: "+information["tname"])
print("稿件分Part总数: "+str(information["videos"]))
if cpr == 1:
    print("稿件类型: 原创")
elif cpr == 2:
    print("稿件类型: 转载")
else:
    print("稿件类型: 既不是原创也不是转载")
print("稿件播放数: "+str(state["view"]))
print("稿件点赞数: "+str(state["like"]))
print("稿件硬币数: "+str(state["coin"]))
print("稿件收藏数: "+str(state["favorite"]))
print("稿件分享数: "+str(state["share"]))
print("稿件弹幕数: "+str(state["danmaku"]))
print("稿件评论数: "+str(state["reply"]))
print("稿件历史最高排行:"+str(state["his_rank"]))
if state["no_reprint"] == 0:
    print("该稿件允许转载, 转载请您标明稿件链接: https://bilibili.com/video/av"+str(aid))
elif state["no_reprint"] == 1:
    print("该稿件禁止转载")
else:
    print("该稿件没有标明自己是否允许转载, 建议转载前询问UP主")
print("UP主: "+owner["name"])
print("UP主UID: "+str(owner["mid"]))
print("UP主头像: "+owner["face"])
print("UP主投稿时间: "+str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(information["ctime"]))))
print("稿件发布时间: "+str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(information["pubdate"]))))
print("视频简介: "+information["desc"])
st1 = {1:"橙色通过",0:"开放浏览",-1:"待审",-2:"被打回",-3:"网警锁定",-4:"视频撞车被锁定",-5:"管理员锁定",-6:"修复待审",-7:"暂缓审核",-8:"补档待审",-9:"等待转码",-10:"延迟审核",-11:"视频源待修",-12:"存储失败",-13:"允许评论待审",-14:"临时回收站",-15:"分发中",-16:"转码失败",-20:"创建未提交",-30:"创建已提交",-40:"定时发布",-100:"用户删除"}
print("稿件状态: "+st1[information["state"]])
if information["state"] == -4:
    print("撞车视频av号跳转: av"+str(information["forward"]))
else:
    pass
print("稿件封面图片: "+information["pic"])
print("与视频同步发布的动态(若无则为空): "+information["dynamic"])
print("稿件总时长(单位为秒): "+str(information["duration"]))
print("稿件参与的活动ID: "+str(information["mission_id"]))
print("稿件分Part信息:")
pages = information["pages"]
for pgs in pages:
    ptt = "第"+str(pgs["page"])+"个视频"
    print("这是"+ptt)
    print(ptt+"的CID: "+str(pgs["cid"]))
    fr = {"vupload":"B站上传","hunan":"芒果TV","qq":"腾讯"}
    print(ptt+"的来源: "+fr[pgs["from"]])
    print(ptt+"的标题: "+pgs["part"])
    print(ptt+"的持续时间(单位为秒): "+str(pgs["duration"]))
    if "dimension" in pgs:
        dimension = pgs["dimension"]
        print(ptt+"的宽度: "+str(dimension["width"]))
        print(ptt+"的高度: "+str(dimension["height"]))
    else:
        pass
if "staff" in information:
    staff = information["staff"]
    ask = 0
    print("联合投稿信息:")
    for stfif in staff:
        ask+=1
        meta1 = "第"+str(ask)+"位成员的"
        meta2 = "第"+str(ask)+"位成员"
        print(meta1+"UID: "+str(stfif["mid"]) )
        print(meta1+"职位: "+stfif["title"] )
        print(meta1+"昵称: "+stfif["name"] )
        print(meta1+"头像: "+stfif["face"] )
        vip = stfif["vip"]
        official = stfif["official"]
        if vip["status"] == 1:
            if vip["type"] == 1:
                print(meta1+"会员类型为: 大会员" )
            elif vip["type"] == 2:
                print(meta1+"会员类型为: 年度大会员" )
            elif vip["type"] == 0:
                print(meta1+"会员类型为: 正式会员" )
            else:
                print(meta1+"会员类型为: 参数错误" )
        elif vip["status"] == 0:
            print(meta1+"会员类型为: 正式会员" )
        else:
            print(meta1+"会员类型为: 参数错误" )
        if official["type"] == 0:
            offtp = {0:"无",1:"个人认证:知名UP主",2:"个人认证:大V达人",3:"机构认证:企业",4:"机构认证:组织",5:"机构认证:媒体",6:"机构认证:政府",7:"个人认证:高能主播",9:"个人认证:社会知名人士"}
            print(meta1+"UP主认证级别: "+offtp[official["role"]])
            if "title" in official:
                print(meta1+"UP主认证名: "+official["title"])
            else:
                pass
            if "desc" in official:
                print(meta1+"UP主认证备注: "+official["desc"])
        elif official["type"] == -1:
            print(meta2+"没有UP主认证")
        else:
            print(meta2+"可能有也可能没有UP主认证")
        print(meta1+"粉丝数: "+str(stfif["follower"]))
else:
    pass
if subtitle["allow_submit"]:
    print("该视频允许提交字幕")
else:
    print("该视频不允许提交字幕")
ccl = subtitle["list"]
if len(ccl) == 0:
    print("该视频没有字幕")
else:
    for cc in ccl:
        print("字幕ID: "+str(cc["id"]))
        cct = "字幕ID为"+str(cc["id"])+"的字幕"
        print(cct+"所使用的语言: "+cc["lan"])
        print(cct+"所使用的语言名称: "+cc["lan_doc"])
        if cc["is_lock"]:
            print(cct+"已被UP主锁定")
        else:
            print(cct+"没有被UP主锁定")
        print(cct+"文件下载链接(JSON格式): "+cc["subtitle_url"])
        authorid = cc["author"]
        uid = is_key_right(authorid["mid"],cc["mid"])
        print(cct+"上传者的UID: "+str(uid))
        print(cct+"上传者的昵称: "+authorid["name"])
        print(cct+"上传者的性别: "+authorid["sex"])
        print(cct+"上传者的头像: "+authorid["face"])
        print(cct+"上传者的签名: "+authorid["sign"])