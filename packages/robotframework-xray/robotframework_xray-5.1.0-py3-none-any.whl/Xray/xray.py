import json, requests, os
from ntpath import join
from datetime import datetime

class Xray:
    def authentication(self) -> str:
        json_data = json.dumps({'client_id': self.config.xray_client_id(), 'client_secret': self.config.xray_client_secret()})
        resp = requests.post(f'{self.config.xray_api()}/authenticate', data=json_data, headers={'Content-Type':'application/json'})
            
        if resp.status_code == 200:
            return 'Bearer ' + resp.json()
        else:
            print(resp.json())
            print(f"Authentication error: {resp.status_code}")

    def getTestPlan(self, key: str):
        try:
            if self.config.debug():
                print("\n------------------------------------------------------------------------------")
                print("The getTestPlan function is being executed!")
                print(f"The function received key {key}")
            
            json_data = f'''
                {{
                    getTestPlans(jql: "key = '{ key }'", limit: 1) {{
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
                print("Unfortunately an error occurred while getting the issueId from TestPlan")
                print(f"Error code {resp.status_code}")
                print("------------------------------------------------------------------------------")
            else:
                if self.config.debug():
                    print(json.dumps(resp.json(), indent=4))
                    print("------------------------------------------------------------------------------")
                return resp.json().get('data').get('getTestPlans').get('results')[0].get('issueId')
        except Exception as error:
            print("An error occurred in the Xray class in the getTestPlan function with the following message:")
            print(error)
            print("------------------------------------------------------------------------------")
        
    def addTestExecutionsToTestPlan(self, issueId: str, testExecIssueId: str):
        try:
            if self.config.debug():
                print("\n------------------------------------------------------------------------------")
                print("The addTestExecutionsToTestPlan function is being executed!")
                print(f"The function received issueId {issueId} and testExecIssueId {testExecIssueId}")

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
                print("\nImport of test results are being sent.")
                print("Please wait a moment...")
                print("------------------------------------------------------------------------------")
                print("The importExecutionCucumber function is being executed!")
                print(f"The function received key {key}")

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

            if key != None:
                issueId = Xray.getTestPlan(self, key)
                Xray.addTestExecutionsToTestPlan(self, str(issueId), str(resp.json().get('id')))
            
            if resp.status_code == 200:
                print(f"\nFile '{join(self.config.cucumber_path(), f'{cucumber_name}.json')}' has been generated!")
                if self.config.debug():
                    print(json.dumps(resp.json(), indent=4))
                splitInfo = resp.json().get('self').split('/')
                print(f"Results can be found in {splitInfo[0]}//{splitInfo[2]}/browse/{resp.json().get('key')}")
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