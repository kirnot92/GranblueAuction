import re
import requests
import YahooAuctionKeyStore
from xml.etree import ElementTree as XML


url = 'https://auctions.yahooapis.jp/AuctionWebService/V2/sellingList?'
key = YahooAuctionKeyStore.key
seller_id = '&sellerID='

class _seller:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

seller_list = [
    #_seller('and_samsun', '「', '」'),
    _seller('sandlasv', '○●', '<'),
    _seller('chinja0123', '・', '<'),
    _seller('park_chea', '「', '」', )
]

#name           start       end         cut
#and_samsun     「           」           [:-1]
#sandlasv       ○●         <           [:]
#chinja0123     ・          <           [:-2]
#park_chea      「           」           [:-3]


def get_items_from_seller(seller):
    req_url = url + key + seller_id + seller.name
    print(req_url)
    response = requests.get(req_url)

    tree = XML.fromstring(response.content)

    item_set = tree.getchildren()[0].getchildren()
    return item_set[1:]

def get_desc_from_item(item):
    desc_url = item.getchildren()[2].text
    print(item.getchildren()[3].text)
    req_url = desc_url + key
    response = requests.get(req_url)
    tree = XML.fromstring(response.content)
    desc = tree.getchildren()[0].getchildren()[31]
    return desc.text

'''
def get_names_using_delimiter(seller, desc):
    scan = re.compile('['+seller.start+']'+'(.+?)'+'['+seller.end+']')
    # [seller.start](.+?)[seller.end]
    l = scan.findall(desc)
    return l
'''
def remove_tag(desc):
    scan = re.compile('(<.+?>)')
    for i in list(set(scan.findall(desc))):
        desc = desc.replace(i, '')
    return desc



def asdf(desc):
    desc_nt = remove_tag(desc)
    desc_sp = desc_nt.split('\n')

    start = {}
    former = desc_sp[0][0]
    for line in desc_sp:
        if line == '' or line  == ' ':
            continue
        if former == line[0]:
            if line[0] not in start.keys():
                start[line[0]] = 1
            else:
                start[line[0]] += 1
        former = line[0]

    print(start)


def get_names_using_delimiter(desc):
    jpscan = re.compile(u'([a-zA-Z\u4E00-\u9FFF\u3040-\u309F)ー(\u30A0-\u30FF]+)', re.UNICODE)

    deli_list = {}

    desc_nt = remove_tag(desc)
    desc_sp = desc_nt.split('\n')
    for i in range(len(desc_sp)):
        if len(desc_sp[i]) != 0:
            if desc_sp[i][len(desc_sp[i])-1]==' ':
                desc_sp[i] = desc_sp[i][:-1]
        desc_sp[i] = '#'+desc_sp[i]+'$'

    former_deli = "#$"
    for i in range(len(desc_sp)):
        line = desc_sp[i]
        jp_list = jpscan.findall(line)
        for jp in jp_list:
            length = len(jp)
            start = line.find(jp)
            forward = line[start-1]
            backward = line[start+length]

            deli = forward+backward
            if deli =='#$':
                continue
            if deli in deli_list.keys():
                if former_deli == deli:
                    deli_list[deli] += 1
            else:
                deli_list[deli] = 1
            former_deli = deli


    delete_list = []
    for deli in deli_list.keys():
        if deli_list[deli] == 1:
            delete_list.append(deli)
    for d in delete_list:
        del deli_list[d]

    print(deli_list)

    for deli in deli_list.keys():
        l = []
        for line in desc_sp:
            start = line.find(deli[0])
            end = line.find(deli[1])

            if start!=-1 and end!=-1:
                l.append(line[start+1:end] )
        deli_list[deli] = l

    for deli in deli_list.keys():
        print(deli,str(len(deli_list[deli])), deli_list[deli])





seller = seller_list[2]
print(seller.name)
items = get_items_from_seller(seller)
desc = get_desc_from_item(items[0])
#get_names_using_delimiter(desc)
asdf(desc)



