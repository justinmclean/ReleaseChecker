# Copyright 2021 Justin Mclean
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from bs4 import BeautifulSoup
import urllib.request
import re

downloadPages = [
    "http://age.apache.org",
    "http://annotator.apache.org",
	"https://brpc.apache.org/download/",
	"http://crail.apache.org/download/",
	"http://datalab.apache.org/#download",
	"http://doris.apache.org/master/en/downloads/downloads.html",
	"http://eventmesh.apache.org/download",
	"https://flagon.apache.org/releases/",
	"https://heron.apache.org/download",
	"https://hivemall.apache.org/download.html",
	"https://hop.apache.org/download/",
	"https://inlong.apache.org/download/main/",
	"https://kyuubi.apache.org/releases.html",
	"https://livy.apache.org/download/",
	"https://milagro.apache.org/docs/downloads/",
	"https://mxnet.apache.org/get_started/download",
	"https://nemo.apache.org/pages/downloads/",
	"https://nlpcraft.apache.org/download.html",
	"https://nuttx.apache.org/download/",
	"https://pagespeed.apache.org/doc/download",
	"https://pegasus.apache.org/en/docs/downloads/",
	"https://ponymail.apache.org/downloads.html",
	"https://shenyu.apache.org/download",
	"https://spot.apache.org/download/",
	"https://streampipes.apache.org/download",
	"https://teaclave.apache.org/download/",
	"https://toree.apache.org/download/",
	"https://training.apache.org/downloads.html",
	"https://tuweni.apache.org/download",
	"https://yunikorn.apache.org/community/download"
]

for page in downloadPages:
    response = urllib.request.urlopen(page)
    data = response.read()
    soup = BeautifulSoup(data,'lxml')

    print()
    print("Checking " + page)

    alllinks = soup('a')
    missing = True
    shamissing = True
    keysmissing = True
    for link in alllinks:
        if link.has_attr('href'):
            href =  link['href']
            text = link.contents
            if href.endswith('.zip') or href.endswith('.tar.gz') or href.endswith('.tzg') or href.endswith('.msi') or href.endswith('.rpm') or href.endswith('.zip') or href.endswith('?action=download'):
                if href.startswith('http://www.apache.org/dist/') or href.startswith('https://www.apache.org/dist/'):
                    print("Please change link to" + href + " to not use http://www.apache.org/dist/ and use https://www.apache.org/dyn/closer.lua instead")
                if href.startswith('http://downloads.apache.org/') or href.startswith('https://downloads.apache.org/'):
                    print("Please change link to" + href + " to not use http://downloads.apache.org/ and use https://www.apache.org/dyn/closer.lua instead")
                if href.startswith('http://dist.apache.org/repos/dist/dev') or href.startswith('https://dist.apache.org/repos/dist/dev'):
                    print("Please change link to " + href + " to release area and use https://www.apache.org/dyn/closer.lua")
                if href.startswith('http://dist.apache.org/repos/dist/release') or href.startswith('https://dist.apache.org/repos/dist/release'):
                    print("Please change link to " + href + " to use https://www.apache.org/dyn/closer.lua to download releases")
                if href.startswith('https://downloads.apache.org/incubator/'):
                    print("Please change link to " + href + " to use https://www.apache.org/dyn/closer.lua to download releases")
                if href.find('closer.cgi') > 0 or href.find('mirrors.cgi') > 0:
                    print("Please change link to " + href + " to use https://www.apache.org/dyn/closer.lua not closer.cgi or mirrors.cgi to download releases")
                if href.startswith('https://dlcdn.apache.org') or href.startswith('http://dlcdn.apache.org'):
                     print("Please change link to " + href + " to use https://www.apache.org/dyn/closer.lua not dlcdn.apache.org to download releases")       
            if href.endswith('.sha512') or href.endswith('.sha256') or href.endswith('.asc'):
                shamissing = False
                if  href.startswith('http://www.apache.org/dist/') or href.startswith('https://www.apache.org/dist/'):
                    print("Please change link to " + href + " to go via https://downloads.apache.org/. https://www.apache.org/dist/ has been deprecated.")
                if not href.startswith('https://downloads.apache.org/') and not href.startswith('https://archive.apache.org/dist'):
                    print("Please change link to " + href + " to go via https://downloads.apache.org/ or https://archive.apache.org/dist")
            if href.endswith('.sha'):
                 print("for link " + href + " .sha should no longer be used. Please change ot use .sha256 or .sha512.")
            if href.endswith('KEYS') or href.endswith('KEYS.txt'):
                keysmissing = False
                if not href.startswith('https://downloads.apache.org/'):
                    print("Please change link to " + href + " to go via https://downloads.apache.org/")
                
    if shamissing:
        print("Links to signatures and hashes are missing")

    if keysmissing:
        print("Links to KEYS are missing")
