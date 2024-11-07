import base64, json
from ntpath import join
from robot.libraries.BuiltIn import BuiltIn
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime

class Report:
    def cucumber(self, report_json, test_plan):
        try:
            cucumber = []

            for suite_index, suite in enumerate(report_json):
                cucumber.append({
                    "keyword": "Feature",
                    "name": suite.get('longname'),
                    "line": 1,
                    "description": suite.get('doc'),
                    "tags": [],
                    "id": suite.get('id'),
                    "uri": suite.get('source'),
                    "elements": [],
                })

                for test_index, test in enumerate(suite.get('tests')):
                    if test.get('template') != "":
                        cucumber[suite_index]['elements'].append({
                            "keyword": "Scenario Outline",
                            "name": test.get('originalname'),
                            "line": test.get('lineno'),
                            "description": test.get('doc'),
                            "tags": [],
                            "id": test.get('id'),
                            "type": "scenario",
                            "steps": [],
                        })
                    else:
                        cucumber[suite_index]['elements'].append({
                            "keyword": "Scenario",
                            "name": test.get('originalname'),
                            "line": test.get('lineno'),
                            "description": test.get('doc'),
                            "tags": [],
                            "id": test.get('id'),
                            "type": "scenario",
                            "steps": [],
                        })

                    for tag_index, tag in enumerate(test.get('tags')):
                        cucumber[suite_index]['elements'][test_index]['tags'].append({
                            "name": "@{}".format(tag),
                            "line": test.get('lineno'),
                        })
                
                    screenshots = []
                    _step_index = 0

                    for step_index, step in enumerate(test.get('keywords')):
                        for message_index, message in enumerate(step.get('messages')):
                            if message.get('message').__contains__('<a href='):
                                soup = BeautifulSoup(message.get('message'), 'html.parser')
                                image_src = soup.a.get_text()

                                if image_src.__contains__('.jpg'):                                
                                    with open(image_src, 'rb') as img_file:
                                        b64_string = base64.b64encode(img_file.read())
                                        screenshots.append({ "mime_type": "image/jpeg", "data": "{}".format(b64_string.decode('utf-8')) })
                            
                            if message.get('message').__contains__('<img'):
                                soup = BeautifulSoup(message.get('message'), 'html.parser')
                                image_src = soup.img.get('src')

                                if not image_src.__contains__('data:image/png;base64,'):                                
                                    with open(join(BuiltIn().get_variable_value('${OUTPUT_DIR}'), image_src), 'rb') as img_file:
                                        b64_string = base64.b64encode(img_file.read())
                                        screenshots.append({ "mime_type": "image/png", "data": "{}".format(b64_string.decode('utf-8')) })
                                else:
                                    screenshots.append({ "mime_type": "image/png", "data": "{}".format(image_src.replace('data:image/png;base64,', '')) })
                                
                        if step.get('kwname').split()[0].lower() in ['given', 'when', 'then', 'and', 'but', '*']:
                            date1 = parser.parse(step.get('starttime'))
                            date2 = parser.parse(step.get('endtime'))
                            diff = date2 - date1

                            cucumber[suite_index]['elements'][test_index]['steps'].append({
                                "embeddings": screenshots,
                                "keyword": step.get('kwname').split()[0].capitalize(),
                                "name": step.get('kwname').replace(step.get('kwname').split()[0], '').strip(),
                                "line": step.get('lineno'),
                                "match": {
                                    "arguments": [],
                                    "location": "{}:{}".format(step.get('source'), step.get('lineno'))
                                },
                                "result": {
                                    "status": ("passed" if step.get('status').lower() == "pass" else ("failed" if step.get('status').lower() == "fail" else "skipped")),
                                    "duration": diff.microseconds*10000,
                                }
                            })

                            if _step_index > 0:
                                if step.get('kwname').replace(step.get('kwname').split()[0], '').strip() not in ['Capture Page Screenshot', 'Capture Element Screenshot', 'Take Screenshot', 'Take Screenshot Without Embedding']:
                                    cucumber[suite_index]['elements'][test_index]['steps'][_step_index-1]['embeddings'] = screenshots

                            _step_index = _step_index + 1
                            
                            screenshots = []
            
            execution_date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
            report_name = f'Report_{test_plan}_{execution_date}'
            cucumber_name = f'Cucumber_{test_plan}_{execution_date}'

            with open(self.config.cucumber_path() + f'/{report_name}.json', 'w') as report_file:
                json.dump(report_json, report_file, indent=4)
                
            with open(self.config.cucumber_path() + f'/{cucumber_name}.json', 'w') as report_file:
                json.dump(cucumber, report_file, indent=4)

            return [report_name, cucumber_name]
        except Exception as error:
            print("Ocorreu um erro na classe Report na função cucumber com a seguinte mensagem:")
            print(error)
            print("------------------------------------------------------------------------------")