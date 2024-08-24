import json,os,sys
from datetime import datetime as Date



JSON_PATH = "./data/data.json"



def ft_exit(exit_status:int, exit_msg:str) -> None:
    print(exit_msg)
    exit(exit_status)

def ft_help(mood:str) -> None:
    if mood == "add":
        print("for adding new  task use this syntax:\n")
        print("     EXECFILE add DISCRIPTION")
        print("         EXECFILE: execution file")
        print("         DISCRIPTION: discription of new task\n\n")
    elif mood == "update":
        print("for updating discription of task use this syntax:\n")
        print("     EXECFILE update INDEX DISCRIPTION")
        print("         EXECFILE: execution file")
        print("         INDEX: index of target task")
        print("         DISCRIPTION: discription of new task\n\n")
        print("for updating status of task to in-progress use this syntax:\n")
        print("     EXECFILE mark-in-progress INDEX\n\n")
        print("for updating status of task to done use this syntax:\n")
        print("     EXECFILE mark-done INDEX\n\n")
    elif mood == "delete":
        print("for deleting task use this syntax:\n")
        print("     EXECFILE delete INDEX\n\n")
        print("         EXECFILE: execution file")
        print("         INDEX: index of target task")
    elif mood == "list":
        for array in ["","todo","in-progress","done"]:
            print(f"for list all {array} tasks use this syntax:\n")
            print(f"     EXECFILE list {array}\n\n")

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

def create_task(discreption:str) -> None:
    
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
            print(f"Task added successfully (ID: {id})")



#update task

def update_task(mood:str, value: str, index: int) -> None:
    
    id,lenght = get_next_id()
    if id == 1 or lenght == 0:
        ft_exit(5,"No data was saved")
    elif id < index:
        ft_exit(6,"Index out of range")
    elif value == "":
        ft_exit(7,"Value should be not empty")
    elif index < 0:
        ft_exit(8,"Negative numbers are note valid")
    else: 
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            old_data:dict = json.load(create_json_file)
            try:
                for i,task in enumerate(old_data["tasks"]):
                    if task["id"] == index:
                        if mood == "update":
                            old_data["tasks"][i]["discription"] = value
                            old_data["tasks"][i]["updatedAt"] = str(Date.now())
                        elif mood == "mark-in-progress" or mood == "mark-done":
                            old_data["tasks"][i]["status"] = value
                            old_data["tasks"][i]["updatedAt"] = str(Date.now())
                with open(file=JSON_PATH,mode="w+",encoding="utf-8") as json_file:
                    json.dump(old_data,json_file,indent=4)
            except IndexError:
                print("404 target not found")



#delete task

def delete_task(index: int) -> None:
    
    id,lenght = get_next_id()
    if id == 1  or lenght == 0:
        ft_exit(10,"No data was saved")
    elif id < index:
        ft_exit(11,"Index out of range")
    elif index < 0:
        ft_exit(12,"Negative numbers are note valid")
        
    else: 
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            old_data:dict = json.load(create_json_file)
            try:
                old_data["tasks"] = [task for task in old_data["tasks"] if task["id"] != index]
                with open(file=JSON_PATH,mode="w+",encoding="utf-8") as json_file:
                    json.dump(old_data,json_file,indent=4)
            except IndexError:
                print("404 target not found")



# list tasks

def list_tasks(target:str|None=None):
    
    lenght:int = get_next_id()[1]
    if lenght == 0:
        ft_exit(14,"No data was saved")
    else: 
        with open(file=JSON_PATH,mode="r",encoding="utf-8") as create_json_file:
            old_data:dict = json.load(create_json_file)
            if target is None:
                print(old_data["tasks"])
            elif target == "done" or target == "todo" or target == "in-progress":
                print([task for task in old_data["tasks"] if task["status"] == target])
            else:
                ft_exit(15,"invalid information")

    return True


try:
    if sys.argv[1] == "add":
        if len(sys.argv) == 3:
            create_task(discreption=sys.argv[2])
        else:
            ft_exit(1,"Wrong number of arguments")
    elif sys.argv[1] == "update":
        if len(sys.argv) == 4:
            update_task(mood="update",value=sys.argv[3],index=int(sys.argv[2]))
        else:
            ft_exit(2,"Wrong number of arguments")
    elif sys.argv[1] == "mark-in-progress":
        if len(sys.argv) == 3:
            update_task(mood="mark-in-progress",value="in-progress",index=int(sys.argv[2]))
        else:
            ft_exit(3,"Wrong number of arguments")
    elif sys.argv[1] == "mark-done":
        if len(sys.argv) == 3:
            update_task(mood="mark-done",value="done",index=int(sys.argv[2]))
        else:
            ft_exit(4,"Wrong number of arguments")
    elif sys.argv[1] == "delete":
        if len(sys.argv) == 3:
            delete_task(index=int(sys.argv[2]))
        else:
            ft_exit(9,"Wrong number of arguments")
    elif sys.argv[1] == "list":
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3:
            list_tasks(target=sys.argv[2])
        else:
            ft_exit(13,"Wrong number of arguments")
    elif sys.argv[1] == "-h":
        if len(sys.argv) == 3:
            ft_help(mood=sys.argv[2])
        else:
            print("here is all available information:\n -h [add], [update], [delete], or [list]")
    else:
        raise ValueError
    
except ValueError:
    print("Wrong input please valid your information.\ncheck \"-h\" for more information about syntax")