#Эта функция позволяет вам записывать в таблицу Notion данные, которые вводит пользователь
import json, requests

token = 'secret_1PmjHBOhy2spGcAVsk7gXUmLXN0ptPYpsjer4J7kkxN'
db_id = 'a01b24fc542b4999a7be23230b19d75d'

headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json',
    'Notion-Version': '2021-05-13'
}



def createPage(name, course, number, databaseId=db_id, headers=headers):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": databaseId },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "Course": {
                "select": 
                    {
                        'name': course
                    }
                
                
            },
            "Status": {
                "select": 
                    {
                        'name':'Not started'
                    }
                
            },
            "Phone": {
                "rich_text": [
                    {
                        "text": {
                            "content": number
                        }
                    }
                ]
            }

        }
    }
    
    data = json.dumps(newPageData)
    res = requests.request("POST", createUrl, headers=headers, data=data)
    print(res.status_code)


