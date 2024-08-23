import json,os,sys
from datetime import datetime as Date



JSON_PATH = "./data/data.json"



def ft_exit(exit_status:int, exit_msg:str):
    print(exit_msg)
    exit(exit_status)

# get new id

def get_next_id()-> tuple[int,int]:
    
    if os.path.exists(JSON_PATH) and os.path.isfile(JSON_PATH):
        json_data: dict = {}
        number_of_tasks:int = 0
        length:int = 0
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            try:
                json_data = json.load(create_json_file)
                length = len(json_data["tasks"])
                number_of_tasks = int(json_data["next-index"])
            except json.decoder.JSONDecodeError or KeyError:
                print("Empty file")
                number_of_tasks = 1
        return number_of_tasks,length
    else:
        with open(file=JSON_PATH,mode="w",encoding="utf-8") as create_json_file:
            create_json_file.write("")
    return 1,0



# create task

def create_task(discreption:str) -> bool:
    
    id:int = get_next_id()[0]
    new_task:dict = {"id":id,"discription":discreption,"status":"todo","createdAt":str(Date.now()),"updatedAt":str(Date.now())}
    if id == 1:
        with open(file=JSON_PATH,mode="w+",encoding="utf-8") as json_file:
            json.dump({"tasks":[new_task],"next-index":2},json_file,indent=4)
    else: 
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            old_data:dict = json.load(create_json_file)
            old_data["tasks"].append(new_task)
            old_data["next-index"] = int(old_data["next-index"]) + 1
            with open(file=JSON_PATH,mode="w+",encoding="utf-8") as json_file:
                json.dump(old_data,json_file,indent=4)
            
    
    
    return True



#update task

def update_task(mood:str, value: str, index: int) -> bool:
    
    id:int = get_next_id()[0]
    if id == 1 or id < index:
        ft_exit(5,"Index out of range")
    elif value == "":
        ft_exit(6,"Value should be not empty")
    else: 
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            old_data:dict = json.load(create_json_file)
            if mood == "update":
                old_data["tasks"][index]["discription"] = value
                old_data["tasks"][index]["updatedAt"] = str(Date.now())
            elif mood == "mark-in-progress" or mood == "mark-done":
                old_data["tasks"][index]["status"] = value
                old_data["tasks"][index]["updatedAt"] = str(Date.now())
            with open(file=JSON_PATH,mode="w+",encoding="utf-8") as json_file:
                json.dump(old_data,json_file,indent=4)


    return True


#delete task

def delete_task(index: int) -> bool:
    
    id:int = get_next_id()[0]
    if id == 1 or id < index:
        ft_exit(8,"Index out of range")
        
    else: 
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            old_data:dict = json.load(create_json_file)
            old_data["tasks"] = [task for task in old_data["tasks"] if task["id"] != index]
            with open(file=JSON_PATH,mode="w+",encoding="utf-8") as json_file:
                json.dump(old_data,json_file,indent=4)


    return True



# list tasks

def list_tasks(target:str|None=None):
    
    id:int = get_next_id()[1]
    if id == 0:
        ft_exit(10,"No data was saved")
    else: 
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            old_data:dict = json.load(create_json_file)
            if target is None:
                print(old_data["tasks"])
            elif target == "done" or target == "todo" or target == "in-progress":
                print([task for task in old_data["tasks"] if task["status"] == target])
            else:
                ft_exit(11,"invalid information")

    return True

if sys.argv[1] == "add":
    if len(sys.argv) == 3:
        create_task(discreption=sys.argv[2])
    else:
        ft_exit(1,"Wrong number of arguments")
elif sys.argv[1] == "update":
    if len(sys.argv) == 4:
        update_task(mood="update",value=sys.argv[3],index=int(sys.argv[2]) - 1)
    else:
        ft_exit(2,"Wrong number of arguments")
elif sys.argv[1] == "mark-in-progress":
    if len(sys.argv) == 3:
        update_task(mood="mark-in-progress",value="in-progress",index=int(sys.argv[2]) - 1)
    else:
        ft_exit(3,"Wrong number of arguments")
elif sys.argv[1] == "mark-done":
    if len(sys.argv) == 3:
        update_task(mood="mark-done",value="done",index=int(sys.argv[2]) - 1)
    else:
        ft_exit(4,"Wrong number of arguments")
elif sys.argv[1] == "delete":
    if len(sys.argv) == 3:
        delete_task(index=int(sys.argv[2]))
    else:
        ft_exit(7,"Wrong number of arguments")
elif sys.argv[1] == "list":
    if len(sys.argv) == 2:
        list_tasks()
    elif len(sys.argv) == 3:
        list_tasks(target=sys.argv[2])
    else:
        ft_exit(9,"Wrong number of arguments")