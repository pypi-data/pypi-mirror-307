import json, base64, re
from robot.libraries.BuiltIn import BuiltIn
from dateutil import parser
from datetime import datetime
from bs4 import BeautifulSoup

# import config as Config, xray as Xray
from .config import Config
from .xray import Xray

class ListenerV2:
    """Optional base class for listeners using the listener API version 2."""
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.execution = []
        self.suite_index = 0
        self.test_index = 0
        self.starttime = 0
        self.config = Config
        self.xray = Xray
        self.steps = []

    def start_suite(self, name: str, attributes):
        """Called when a suite starts."""
        if self.config.debug():
            print("The following configurations have been loaded:")
            print(f"PROJECT_KEY: {self.config.project_key()}")
            print(f"TEST_PLAN: {self.config.test_plan()}")
            print(f"CUCUMBER_PATH: {self.config.cucumber_path()}")
            print(f"XRAY_API: {self.config.xray_api()}")
            print(f"XRAY_CLIENT_ID: {self.config.xray_client_id()}")
            print(f"XRAY_CLIENT_SECRET: {self.config.xray_client_secret()}")
            print("==============================================================================")

        self.execution.append({
            "keyword": "Feature",
            "name": attributes.get('longname'),
            "line": 1,
            "description": attributes.get('doc'),
            "tags": [],
            "id": attributes.get('id'),
            "uri": attributes.get('source'),
            "elements": []
        })

    def end_suite(self, name: str, attributes):
        """Called when a suite end."""
        self.suite_index = self.suite_index + 1
        self.test_index = 0

    def start_test(self, name: str, attributes):
        """Called when a test or task starts."""
        self.execution[self.suite_index]['elements'].append({
            "keyword": "Scenario" if attributes.get('template') == "" else "Scenario Outline",
            "name": attributes.get('originalname'),
            "line": attributes.get('lineno'),
            "description": attributes.get('doc'),
            "tags": [],
            "id": attributes.get('id'),
            "type": "scenario",
            "steps": []
        })
    
    def end_test(self, name: str, attributes):
        """Called when a test or task ends."""
        for tag_index, tag in enumerate(attributes.get('tags')):
            self.execution[self.suite_index]['elements'][self.test_index]['tags'].append({
                "name": f"@{tag}",
                "line": attributes.get('lineno'),
            })

        self.execution[self.suite_index]['elements'][self.test_index]['steps'] = self.steps
        self.steps = []

        test_plan = self.config.test_plan()
        execution_date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        cucumber_name = f'Cucumber_{test_plan}_{execution_date}'

        with open(self.config.cucumber_path() + f'/{cucumber_name}.json', 'w') as report_file:
            json.dump(self.execution, report_file, indent=4)

        self.execution[self.suite_index]['elements'] = []
        self.xray.importExecutionCucumber(self, cucumber_name, test_plan)

    def start_keyword(self, name: str, attributes):
        """Called when a keyword or a control structure like IF starts.

        The type of the started item is in ``attributes['type']``. Control
        structures can contain extra attributes that are only relevant to them.
        """
        if attributes.get('kwname').split()[0].lower() in ['given', 'when', 'then', 'and', 'but', '*']:
            self.starttime = attributes.get('starttime')
            self.steps.append({
                "embeddings": [],
                "keyword": attributes.get('kwname').split()[0].capitalize(),
                "name": attributes.get('kwname').replace(attributes.get('kwname').split()[0], '').strip(),
                "line": attributes.get('lineno'),
                "match": {
                    "arguments": [],
                    "location": f"{attributes.get('source')}:{attributes.get('lineno')}"
                },
                "result": {
                    "status": attributes.get('status'),
                    "duration": attributes.get('starttime')
                }
            })

    def end_keyword(self, name: str, attributes):
        """Called when a keyword or a control structure like IF ends.

        The type of the started item is in ``attributes['type']``. Control
        structures can contain extra attributes that are only relevant to them.
        """
        if attributes.get('kwname').split()[0].lower() in ['given', 'when', 'then', 'and', 'but', '*']:
            date1 = parser.parse(self.starttime)
            date2 = parser.parse(attributes.get('endtime'))
            diff = date2 - date1
            self.steps[-1]['result']['status'] = ("passed" if attributes.get('status').lower() == "pass" else ("failed" if attributes.get('status').lower() == "fail" else "skipped"))
            self.steps[-1]['result']['duration'] = diff.microseconds*10000

    def log_message(self, message):
        """Called when a normal log message are emitted.

        The messages are typically logged by keywords, but also the framework
        itself logs some messages. These messages end up to output.xml and
        log.html.
        """        
        if message.get('level') == 'FAIL':
            texto_bytes = message.get('message').encode('utf-8')
            texto_base64 = base64.b64encode(texto_bytes)
            self.steps[-1]['embeddings'].append({ "mime_type": "text/plain", "data": f"{texto_base64.decode('utf-8')}" })

        if message.get('message').__contains__('data:image/png;base64,'):
            match = re.search(r'src="([^"]+)"', message.get('message'))
            if match:
                base64_src = match.group(1)
                self.steps[-1]['embeddings'].append({ "mime_type": "image/png", "data": f"{base64_src.replace('data:image/png;base64,', '')}" })
