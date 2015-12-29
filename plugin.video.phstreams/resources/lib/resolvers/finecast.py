# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        page = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        page = 'http://www.finecast.tv/embed4.php?u=%s&vw=640&vh=450' % page

        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = page

        result = client.request(page, referer=referer)

        var = re.compile('var\s(.+?)\s*=\s*\'(.+?)\'').findall(result)
        for i in range(100):
            for v in var: result = result.replace("'+%s+'" % v[0], "'+%s+'" % v[1])
            for v in var: result = result.replace("'+%s" % v[0], "'+%s" % v[1])

        result = re.sub('("|\'|\,|\+)', '', result)

        url = re.compile('file\s*:\s*(.+?)\n').findall(result)
        url = [i for i in url if '.m3u8' in i][0]
        return url
    except:
       return


