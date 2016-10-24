from django.shortcuts import render
import requests, json
from bs4 import BeautifulSoup
from django.http import HttpResponse

def homepage(request):
    if request.method == 'POST':
        p_action = str(request.POST.get('action', ''))
        action_block = False
        if p_action == 'block':
            action_block = True
        response = requests.get('http://admin:password@192.168.1.1/DEV_control.htm')
        soup = BeautifulSoup(response.text, "html.parser")
        resp_url = soup.find('form').get('action')

        num_macs = str(len(soup.findAll('span', {'name':'rule_mac'})))
        mac_list = [x.text for x in soup.findAll('span', {'name':'rule_mac'})]

        block_mac = ['C0:EE:FB:21:0C:89']

        rule_set = num_macs
        for mac in mac_list:
            rule_set += ":"+mac
            if mac in block_mac and action_block:
                rule_set += ":0"
            else:
                rule_set += ":1"

        url = "http://admin:asakura@192.168.1.1/"+resp_url
        end_url = "http://192.168.1.1/"+resp_url
        headers = {'Origin': 'http://192.168.1.1', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-US,en;q=0.8', 'Upgrade-Insecure-Requests':'1', 'Authorization':'Basic YWRtaW46YXNha3VyYQ==', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36', 'Cache-Control': 'max-age=0', 'Referer': end_url, 'Connection': 'keep-alive'}
        payload = {'enable_acl': 'enable_acl', 'access_all': 'allow_all', 'select': '-1', 'rule_status_org': 'allow', 'enable_access_control': '1', 'access_all_setting': '1', 'allowed_text': 'Allowed', 'blocked_text': 'Blocked', 'rule_settings': rule_set, 'router_access_user': '192.168.1.50'}
        if action_block:
            payload['block'] = 'block'
        else:
            payload['allow'] = 'allow'

        r = requests.post(url, data=payload, headers=headers)

        return HttpResponse('Ok')
    else:
        return render(request, 'home.html')