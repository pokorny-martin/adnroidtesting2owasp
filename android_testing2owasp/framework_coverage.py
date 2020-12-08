import typing
from .scenario import TestScenario
from .arch import *
from .storage import *
from .network import *
from .platform import *
from .code import *
from .resilience import *


class FrameworkCoverage:
    scenarios: typing.Dict[str, TestScenario] = {}

    def __init__(self, path=""):
        self.path = path

    def get_scenario(self, scenario):
        pass

    def get_scenario_arch(self, number):
        pass

    def parse(self, framework):
        if framework == "Androwarn":
            self.parse_Androwarn()
        elif framework == "AndroPyTool":
            self.parse_AndroPyTool()
        elif framework == "AndroBugs":
            self.parse_AndroBugs()
        elif framework == "MobSF":
            self.parse_MobSF()

    def parse_Androwarn(self):
        import json

        def parse_files(js):
            return set(js[2]["apk_file"][2][1])

        def parse_activities(js):
            return set(js[3]["androidmanifest.xml"][2][1])

        def parse_log(js):
            x = js[1]["analysis_results"][1][1]
            return set([i.replace("This application logs the message '", "").strip()[:-1] for i in x])

        def parse_cert(js):
            return js[2]["apk_file"][3][1][0].find("True") >= 0

        data = None
        with open(self.path, "r") as f:
            data = f.read()
        js = json.loads(data)
        files = parse_files(js)
        activities = parse_activities(js)
        logs = parse_log(js)
        cert = parse_cert(js)
        self.scenarios["Arch1"] = Arch1(files=files, activities=activities)
        self.scenarios["Storage3"] = Storage3(log_sources=logs)
        self.scenarios["Code1"] = Code1(valid=cert)

    def parse_AndroPyTool(self):
        import json

        def parse_permissions(permissions):
            return set(permissions)

        def parse_activities(activities):
            return set(activities.keys())

        def parse_strings(strings):
            return set(strings.keys())

        data = None
        with open(self.path, "r") as f:
            data = f.read()
        js = json.loads(data)

        permissions = parse_permissions(js["Static_analysis"]["Permissions"])
        activities = parse_activities(js["Static_analysis"]["Activities"])
        strings = parse_strings(js["Static_analysis"]["Strings"])
        self.scenarios["Arch1"] = Arch1(activities=activities)
        self.scenarios["Storage3"] = Storage3(strings=strings)
        self.scenarios["Storage8"] = Storage8(strings=strings)
        self.scenarios["Platform1"] = Platform1(permissions=permissions)

    def parse_AndroBugs(self):
        data = None
        with open(self.path, "r") as f:
            data = f.read()
        lines = data.split("\n")
        y = []
        x = []
        for line in lines:
            if len(line) == 0:
                continue
            if line[0] == "[":
                y.append(x)
                x = []
            x.append(line)
        y.append(x[:-3])
        y = y[1:]
        for line in y:
            first_space = line[0].find(" ")
            criticality = line[0][:first_space].replace("[", "").replace("]", "")
            header = line[0][first_space+1:]
            details = line[1:]
            if details[-1][0] == "-" and details[-1][-1] == "-":
                details = details[:-1]
            detail = "\n".join([detail.strip() for detail in details])
            if header.find("KeyStore") >= 0:
                if detail.lower().find("checking") >= 0:
                    key_store = not detail.lower().find("not using") >= 0
                    d = detail if key_store else None
                    self.scenarios["Storage1"] = Storage1(key_store, d)
            elif header.find("External Storage Accessing") >= 0:
                access = detail.lower().find("access found") >= 0
                self.scenarios["Storage2"] = Storage2(access, [detail[detail.find("=>"):]])
            elif header.find("AndroidManifest Adb Backup Checking") >= 0:
                adb_back_up = detail.lower().find("ENABLED") >= 0
                self.scenarios["Storage8"] = Storage8(adb_back_up=adb_back_up)
            elif header.find("SSL_Security") >= 0:
                if detail.lower().find("under ssl") >= 0:
                    not_ssl_urls = not detail.lower().find("urls that are not") >= 0
                    scenario = Network1(not_ssl=not_ssl_urls, detail=["\n".join(detail.split("\n")[1:])])
                    try:
                        self.scenarios["Network1"] = self.scenarios["Network1"].combine(scenario)
                    except KeyError:
                        self.scenarios["Network1"] = scenario
                elif detail.lower().find("getinsecure") >= 0:
                    get_insecure = not detail.lower().find("did not")
                    d = ["\n".join(detail.split("\n")[1:])]
                    if len(d) == 0:
                        d = None
                    scenario = Network1(get_insecure=get_insecure, detail=d)
                    try:
                        self.scenarios["Network1"] = self.scenarios["Network1"].combine(scenario)
                    except KeyError:
                        self.scenarios["Network1"] = scenario
                elif detail.lower().find("webviewclient") >= 0:
                    web_view_client = not detail.lower().find("did not")
                    d = ["\n".join(detail.split("\n")[1:])]
                    if len(d) == 0:
                        d = None
                    scenario = Network1(web_view_client=web_view_client, detail=d)
                    try:
                        self.scenarios["Network1"] = self.scenarios["Network1"].combine(scenario)
                    except KeyError:
                        self.scenarios["Network1"] = scenario
                elif detail.lower().find("x509") >= 0:
                    vulnerable_x509_certificate = not detail.lower().find("did not")
                    d = ["\n".join(detail.split("\n")[1:])]
                    if len(d) == 0:
                        d = None
                    scenario = Network1(web_view_client=vulnerable_x509_certificate, detail=d)
                    try:
                        self.scenarios["Network1"] = self.scenarios["Network1"].combine(scenario)
                    except KeyError:
                        self.scenarios["Network1"] = scenario
            elif header.find("WebView") >= 0:
                js_in_web_view = not detail.lower().find("did not detect \"setJavaScriptEnabled(true)\"") >= 0
                self.scenarios["Platform5"] = Platform5(js_in_web_view)
            elif header.find("Executing \"root\" or System Privilege Checking") >= 0:
                root = not detail.lower().find("did not") >= 0
                self.scenarios["Resilience1"] = Resilience1(root)
            elif header.find("Android Debug Mode") >= 0:
                has_code_checking = not detail.find("Did not detect") >= 0
                self.scenarios["Resilience2"] = Resilience2(has_code_checking)
            elif header.find("App Sandbox Permission Checking") >= 0:
                has_sandbox_permission_checking = False
                if detail.lower().find("security issues") >= 0 and detail.lower().find("found") >= 0:
                    has_sandbox_permission_checking = True
                self.scenarios["Resilience3"] = Resilience3(has_sandbox_permission_checking,
                                                            ["\n".join(detail[detail.find("=>"):].split("\n")[:-1])])
            elif header.find("Getting Signature Code Checking") >= 0:
                has_code_checking = detail.lower().find("has code checking") > 0
                self.scenarios["Resilience6"] = Resilience6(has_code_checking, [detail[detail.find("=>"):]])
            elif header.find("Getting IMEI and Device ID") >= 0:
                gets_device_id = detail.lower().find("did not") < 0
                scenario = Resilience10(device_id=gets_device_id)
                try:
                    self.scenarios["Resilience10"] = self.scenarios["Resilience10"].combine(scenario)
                except KeyError:
                    self.scenarios["Resilience10"] = scenario
            elif header.find("Getting ANDROID_ID") >= 0:
                gets_android_id = detail.lower().find("did not") < 0
                scenario = Resilience10(android_id=gets_android_id)
                try:
                    self.scenarios["Resilience10"] = self.scenarios["Resilience10"].combine(scenario)
                except KeyError:
                    self.scenarios["Resilience10"] = scenario

    def parse_MobSF(self):
        import json

        def parse_activity(activities):
            a = []
            for activity in activities:
                start = activity.find("(") + 1
                if start == 0:
                    continue
                end = activity.find(")")
                a.append(activity[start:end])
            return set(a)

        with open(self.path, "r") as f:
            data = f.read()
        js = json.loads(data)

        self.scenarios["Arch1"] = Arch1(activities=set(js["activities"]), files=set(js["files"]))
        external_storage = "android.permission.WRITE_EXTERNAL_STORAGE" in js["permissions"]
        self.scenarios["Storage2"] = Storage2(external_storage_permission=external_storage)
        strings = set(js["strings"])
        self.scenarios["Storage3"] = Storage3(strings=strings)
        urls = set([url['urls'][0] for url in js["urls"]])
        trackers = set([list(tracker.values())[0] for tracker in js["trackers"]["trackers"]])
        self.scenarios["Storage4"] = Storage4(trackers=trackers, urls=urls)
        shared_services = [activity["title"] for activity in js["manifest_analysis"]
                           if activity["title"].find("exported=true") >= 0]
        shared_services = parse_activity(shared_services)
        self.scenarios["Storage6"] = Storage6(shared_services=shared_services)
        adb_back_up = [activity["title"] for activity in js["manifest_analysis"]
                       if activity["desc"].find("backup") >= 0 and
                       activity["desc"].find("adb") >= 0 and
                       activity["title"].find("true") >= 0]
        adb_back_up = len(adb_back_up) > 0
        self.scenarios["Storage8"] = Storage8(adb_back_up=adb_back_up, strings=strings)
        permissions = set(js["permissions"].keys())
        self.scenarios["Platform1"] = Platform1(permissions=permissions)
        self.scenarios["Platform4"] = Platform4(shared_services=shared_services)
        intent_filters = [activity["title"] for activity in js["manifest_analysis"]
                          if activity["desc"].find("intent-filter") >= 0]
        intent_filters = parse_activity(intent_filters)
        self.scenarios["Platform9"] = Platform9(intent_filters)
        self.scenarios["Code1"] = Code1(js["certificate_analysis"]["certificate_info"].find("True") >= 0)
        debuggable = [activity["title"] for activity in js["manifest_analysis"]
                      if activity["title"].find("debug") >= 0 and
                      activity["title"].lower().find("true") >= 0]
        debuggable = len(debuggable) >= 0
        self.scenarios["Code2"] = Code2(not debuggable)

        for library in js["binary_analysis"]:
            is_stripped = library["symbol"]["is_stripped"]
            name = library["name"]
            try:
                self.scenarios["Code3"] = self.scenarios["Code3"].combine(Code3(name, is_stripped))
            except KeyError:
                self.scenarios["Code3"] = Code3(name, is_stripped)

        for library in js["binary_analysis"]:
            is_stripped = library["symbol"]["is_stripped"]
            name = library["name"]
            try:
                self.scenarios["Code4"] = self.scenarios["Code4"].combine(Code4(name, is_stripped, not debuggable))
            except KeyError:
                self.scenarios["Code4"] = Code4(name, is_stripped, not debuggable)

        for dex in js["apkid"].keys():
            pass

    def combine(self, other):
        if not isinstance(other, self.__class__):
            return None
        new = self.__class__()
        for key in self.scenarios.keys():
            new.scenarios[key] = self.scenarios[key]
        for key in other.scenarios.keys():
            try:
                current = new.scenarios[key]
                new.scenarios[key] = current.combine(other.scenarios[key])
            except KeyError:
                new.scenarios[key] = other.scenarios[key]
        return new

    def to_json(self):
        import json
        scenarios = []
        for key, value in self.scenarios.items():
            scenarios.append({key: value.to_dict()})
        scenarios = sorted(scenarios, key=lambda x: list(x.keys())[0])
        return json.dumps(scenarios)
