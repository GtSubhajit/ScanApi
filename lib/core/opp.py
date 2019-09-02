import re
import logging
import subprocess
from ..paths.helper import MEDIUM
from ..thirdparty.Gasset.asset import main as Gasset
from ..thirdparty.Sublist3r.sublist3r import main as Sublist3r

opp_logger = logging.getLogger("opp")
opp_logger.addHandler(logging.NullHandler())

class ProcessBase(object):
    def __init__(self):        
        self.pro = None
        self.name = None
        self.threads = 25
        self.result = None
        self.command = None
        self.pattern = None

    def extract_data(self):
        data = re.findall(self.pattern, self.result[0].decode("utf-8"))
        error = self.result[1].decode("utf-8")
        opp_logger.info("Getting {0} result".format(self.name))
        return {self.name : {"error": error, "data": data}}
    
    def exec_command(self):
        opp_logger.debug("Starting {0}".format(self.name))
        self.pro = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.result = self.pro.communicate()
        return self.extract_data()

class SubOver(ProcessBase):
    def __init__(self, file):
        ProcessBase.__init__(self)
        self.name = "SubOver"
        self.command = "subover -t {0} -a -l {1}".format(self.threads, file)
        self.pattern = r"\[31\;1\;4m(\D+)\u001b\[0m\] Takeover Possible At (\S+)"

class GoBuster(ProcessBase):
    def __init__(self, domain):
        ProcessBase.__init__(self)
        self.name = "GoBuster"
        self.command = "gobuster -t {0} -r -l -f -e -q -w {1} -u {2}".format(self.threads, MEDIUM, domain)
        self.pattern = r"(\S+) \(Status: (\d+)\) \[Size: (\d+)\]"

class AssetFinder(ProcessBase):
    def __init__(self, domain):
        ProcessBase.__init__(self)
        self.name = "AssetFinder"
        self.command = "assetfinder -subs-only {0}".format(domain)
        self.pattern = r"(.+)\n"

class Amass(ProcessBase):
    def __init__(self, domain):
        ProcessBase.__init__(self)
        self.name = "Amass"
        self.command = "amass enum -passive -d {0}".format(domain)
        self.pattern = r"(.+)\n"