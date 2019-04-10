from django.http import HttpResponse
from django.shortcuts import render
import urllib.request
import urllib.parse
import json

# Create your views here.


def transform_page(request):
    # url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc"
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    # url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
    fate = request.POST.get('translate1', '有道翻译全程支持')
    data = {}
    data["i"] = fate
    data["from"] = "AUTO"
    data["to"] = "AUTO"
    data["smartresult"] = "dict"
    data["client"] = "fanyideskweb"
    data["salt"] = "1543046504127"
    data["sign"] = "778d7c117ff263dcf89dac41ef150516"
    data["doctype"] = "json"
    data["version"] = "2.1"
    data["keyfrom"] = "fanyi.web"
    data["action"] = "FY_BY_CLICKBUTTION"
    data["typoResult"] = "false"
    head = {}
    # head['Referer'] = "https://h.bilibili.com/9532003"
    head['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:63.0) Gecko/20100101 Firefox/63.0"

    data = urllib.parse.urlencode(data).encode("utf-8")
    html = urllib.request.Request(url, data, head)
    html = urllib.request.urlopen(html)
    html = html.read().decode("utf-8")
    html = json.loads(html)
    html = html['translateResult'][0]
    char = ''
    for i in html:
        char = char + i['tgt']
    dictionary = {}
    dictionary['html'] = char
    dictionary['fate'] = fate
    return render(request, 'App/transform_page.html', dictionary)

