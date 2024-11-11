import requests
from box import Box
from bs4 import BeautifulSoup


def parse_proxy_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    div_tag = soup.find('div', class_='data kq-well')
    if div_tag:
        pre_tag = div_tag.find('pre')
        if pre_tag:
            pre_text = pre_tag.get_text()
            return pre_text
        else:
            return None
    else:
        return None


def _get_ip_ipinfo(proxy_proxies=None) -> Box:
    """ipinfo.io"""
    try:
        rsp = requests.get('https://ipinfo.io/json',
                           timeout=3,
                           proxies=proxy_proxies
                           )
        if rsp.status_code == 200:
            data = rsp.json()
            ip = data.get('ip')
            region = data.get('region')
            country = data.get('country')
            city = data.get('city')
            org = data.get('org')
            return Box(status=True, ip=ip, 地区=region, 国家=country, 城市=city, org=org)
        else:
            return Box(status=False, ip='0.0.0.0', error=str(rsp.status_code))
    except Exception as e:
        return Box(status=False, ip='0.0.0.0', error=str(e))


def _get_ip_api(proxy_proxies=None) -> Box:
    try:
        rsp = requests.get('http://ip-api.com/json/?lang=zh-CN',
                           timeout=3,
                           proxies=proxy_proxies
                           )
        if rsp.status_code == 200:
            data = rsp.json()
            ip = data.get('query')
            country = data.get('country')
            region = data.get('regionName')
            city = data.get('city')
            org = data.get('as')
            return Box(status=True, ip=ip, 地区=region, 国家=country, 城市=city, org=org)
        else:
            return Box(status=False, ip='0.0.0.0', error=str(rsp.status_code))
    except Exception as e:
        return Box(status=False, ip='0.0.0.0', error=str(e))


def _get_ip_ipapi(proxy_proxies=None) -> Box:
    try:
        rsp = requests.get('https://ipapi.co/json/',
                           timeout=3,
                           proxies=proxy_proxies
                           )
        if rsp.status_code == 200:
            data = rsp.json()
            ip = data.get('ip', '0.0.0.0')
            region = data.get('region', None)
            country = data.get('country', None)
            city = data.get('city', None)
            org = data.get('org', None)
            return Box(status=True, ip=ip, 地区=region, 国家=country, 城市=city, org=org)
        else:
            return Box(status=False, ip='0.0.0.0', error=str(rsp.status_code))
    except Exception as e:
        return Box(status=False, ip='0.0.0.0', error=str(e))


def _get_cip(proxy_proxies=None):
    """获取http代理ip"""
    try:
        rsp = requests.get('https://cip.cc',
                           timeout=3,
                           proxies=proxy_proxies
                           )
        proxy_info = parse_proxy_info(rsp.content)
        if proxy_info:
            return proxy_info
        else:
            return None
    except Exception as e:
        print(f'获取http代理ip失败:{e}')
        return None


def GetHttpIp(proxy_proxies=None):
    """获取http代理ip"""
    ip_api_list = [_get_ip_ipinfo, _get_ip_api, _get_ip_ipapi]
    for ip_api in ip_api_list:
        ip_info = ip_api(proxy_proxies)
        if ip_info.status:
            ip_info.api_name = ip_api.__name__
            ip_info.index = ip_api_list.index(ip_api)
            return ip_info


if __name__ == '__main__':
    print(GetHttpIp())
    pass
