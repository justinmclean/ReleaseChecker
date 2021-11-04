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


distareas = [
    "age",
    "annotator",
    "brpc",
    "crail",
    "datalab",
    "doris",
    "eventmesh",
    "flagon",
    "heron",
    "hivemall",
    "hop",
    "inlong",
    "kyuubi",
    "livy",
    "milagro",
    "mxnet",
    "nemo",
    "nlpcraft",
    "nuttx",
    "pagespeed",
    "pegasus",
    "ponymail",
    "shenyu",
    "spot",
    "streampipes",
    "teaclave",
    "toree",
    "training",
    "tuweni",
    "yunikorn"
]

downloadPages = [
    "https://age.apache.org",
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

i = 0
for project in distareas:
    disturl = "https://dist.apache.org/repos/dist/release/incubator/" + project + "/"
    #disturl = "https://dist.apache.org/repos/dist/release/" + project + "/"
    archiveurl = "https://archive.apache.org/dist/incubator/" + project + "/"

    print()
    print("Checking " + project)
    print(disturl)
    print(downloadPages[i])

    response = urllib.request.urlopen(disturl)
    data = response.read()
    soup = BeautifulSoup(data,'lxml')
    distlinks = soup('a')

    downloadresponse = urllib.request.urlopen(downloadPages[i])
    downloaddata = downloadresponse.read()
    downloadsoup = BeautifulSoup(downloaddata,'lxml')
    alldownloadlinks = downloadsoup('a')

    # TODO check archives as well
    #archiveresponse = urllib.request.urlopen(archiveurl)
    #archivedata = archiveresponse.read()
    #archiveurlsoup = BeautifulSoup(archivedata,'lxml')
    #archivelinks = archiveurlsoup('a')

    downloadlinks = {}
    versions = {}
    alllinks = []

    # TODO check archives as well
    #for link in distlinks:
    #    if link.has_attr('href'):
    #        link['archive'] = False
    #        alllinks.append(link)

    #for link in archivelinks:
    #    if link.has_attr('href'):
    #        link['archive'] = True
    #        alllinks.append(link)

    for link in alldownloadlinks:
        if link.has_attr('href'):
            href = link['href']
            if href.endswith('.zip') or href.endswith('.tar.gz') or href.endswith('.tzg') or href.endswith('.msi') or href.endswith('.rpm') or href.endswith('.zip') or href.startswith('https://www.apache.org/dyn') or href.startswith('http://www.apache.org/dyn'):
                if not href.endswith("closer.cgi#verify"):
                    downloadlinks[href] = False
    
    for link in distlinks:
        href =  link['href']
        text = link.contents[0].replace("/","")
        versions[text] = False

        if text == "KEYS" or text == ".." or text == "Parent Directory" or href.startswith("?") or text.startswith("LICENSE") or text == text.startswith("NOTICE") or text.startswith("CHANGELOG"):
            versions[text] = True
            continue

        for downloadlink in alldownloadlinks:
            if downloadlink.has_attr('href'):
                href =  downloadlink['href']
                if href.endswith('.zip') or href.endswith('.tar.gz') or href.endswith('.tzg') or href.endswith('.msi') or href.endswith('.rpm') or href.endswith('.zip') or href.startswith('https://www.apache.org/dyn') or href.startswith('http://www.apache.org/dyn'):
                    if href.find(text) > 0:
                        versions[text] = True
                        downloadlinks[href] = True
                    # TODO for now assume all archive links are OK
                    if href.startswith("https://archive.apache.org/") or href.startswith("http://archive.apache.org/"):
                        versions[text] = True
                        downloadlinks[href] = True

    for version in versions:
        if not versions[version]:
            print("Download for version " + version + " missing in download page " + downloadPages[i])  

    for href in downloadlinks:
         if not downloadlinks[href]:
            print("Download " + href + " missing in dist area " + distareas[i])  

    i = i + 1
