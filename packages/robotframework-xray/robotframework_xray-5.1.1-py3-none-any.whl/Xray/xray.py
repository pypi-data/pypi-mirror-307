import json, requests, os
from ntpath import join
from datetime import datetime

class Xray:
    def authentication(self) -> str:
        json_data = json.dumps({"client_id": self.config.xray_client_id(), "client_secret": self.config.xray_client_secret()})
        resp = requests.post(f"{self.config.xray_api()}/authenticate", data=json_data, headers={"Content-Type":"application/json"})
            
        if resp.status_code == 200:
            return f"Bearer {resp.json()}"
        else:
            print("------------------------------------------------------------------------------")
            print("An authentication error occurred, see more details:")
            print(f"Status code: {resp.status_code}")
            print(json.dumps(resp.json(), indent=4))

    def getTestPlan(self) -> str:
        try:            
            json_data = f'''
                {{
                    getTestPlans(jql: "key = '{ self.config.test_plan() }'", limit: 1) {{
                        results {{
                            issueId
                        }}
                    }}
                }}
            '''

            resp = requests.post(
                f'{self.config.xray_api()}/graphql',
                json={
                    'query': json_data
                },
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': Xray.authentication(self)
                },
            )

            if resp.status_code != 200:
                print("Unfortunately an error occurred while getting the issueId")
                print(f"Status code: {resp.status_code}")
                print(json.dumps(resp.json(), indent=4))
            else:
                if self.config.debug():
                    print(json.dumps(resp.json(), indent=4))
                return str(resp.json().get('data').get('getTestPlans').get('results')[0].get('issueId'))
        except Exception as error:
            print("An error occurred in the Xray class in the getTestPlan function with the following message:")
            print(error)
        
    def addTestExecutionsToTestPlan(self, issueId: str, testExecIssueId: str):
        try:
            if self.config.debug():
                print("------------------------------------------------------------------------------")
                print("The addTestExecutionsToTestPlan function obtained the following parameters:")
                print(f"issueId: {issueId}")
                print(f"testExecIssueId: {testExecIssueId}")

            json_data = f'''
                mutation {{
                    addTestExecutionsToTestPlan(
                        issueId: "{ issueId }",
                        testExecIssueIds: ["{ testExecIssueId }"]
                    ) {{
                        addedTestExecutions
                        warning
                    }}
                }}
            '''

            resp = requests.post(
                f'{self.config.xray_api()}/graphql',
                json={
                    'query': json_data
                },
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': Xray.authentication(self)
                },
            )

            if resp.status_code != 200:
                print("Unfortunately, an error occurred while adding the results to the Test Plan.")
                print(f"Error code {resp.status_code}")
                print(json.dumps(resp.json(), indent=4))
                print("------------------------------------------------------------------------------")
            else:
                if self.config.debug():
                    print(json.dumps(resp.json(), indent=4))
                    print("------------------------------------------------------------------------------")
        except Exception as error:
            print("An error occurred in the Xray class in the addTestExecutionsToTestPlan function with the following message:")
            print(error)
            print("------------------------------------------------------------------------------")

    def importExecutionCucumber(self, cucumber_name, key: str = None):
        try:
            if self.config.debug():
                print("\n------------------------------------------------------------------------------")
                print("The importExecutionCucumber function obtained the following parameters:")
                print(f"cucumber_name: {cucumber_name}")
                print(f"key: {key}")

            resp = requests.post(f'{self.config.xray_api()}/import/execution/cucumber', 
                data = open(self.config.cucumber_path() + f'/{cucumber_name}.json', 'rb'),
                params = { 
                    'projectKey': self.config.project_key(),
                },
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': Xray.authentication(self)
                }
            )

            if self.config.debug():
                print(json.dumps(resp.json(), indent=4))
                print("------------------------------------------------------------------------------")

            issueId = Xray.getTestPlan(self)
            Xray.addTestExecutionsToTestPlan(self, issueId, str(resp.json().get('id')))
            
            if resp.status_code == 200:
                print(f"File '{join(self.config.cucumber_path(), f'{cucumber_name}.json')}' has been generated!")
                print("------------------------------------------------------------------------------")
                splitInfo = resp.json().get('self').split('/')
                print(f"Results can be found in {splitInfo[0]}//{splitInfo[2]}/browse/{resp.json().get('key')}")
                if self.config.debug():
                    print(json.dumps(resp.json(), indent=4))
                print("------------------------------------------------------------------------------")
            else:
                print("Unfortunately there was an error sending the results")
                print(f"Error code {resp.status_code}")
                print(json.dumps(resp.json(), indent=4))
                print("------------------------------------------------------------------------------")
        except Exception as error:
            print("An error occurred in the Xray class in the import Execution Cucumber function with the following message:")
            print(error)
            print("------------------------------------------------------------------------------")