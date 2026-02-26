from datetime import date,datetime
from collections import Counter

#This is where a declaration is converted
def variable_declaration(abl_string,variables):
    orig_arr = abl_string.split(" ")
    if "initial" in abl_string.lower():
        idx = abl_string.lower().find("initial")
        initial_val = abl_string[idx + len("initial"):].strip().replace(".", "")
        abl_string = abl_string[:idx].strip().lower()
    else:
        initial_val = ""
    input_arr = abl_string.lower().split(" ")
    var_idx = orig_arr.index("variable") if "variable" in orig_arr else (orig_arr.index("VARIABLE") if "VARIABLE" in orig_arr else orig_arr.index("VAR"))
    var_name = orig_arr[var_idx + 1]
    var_type = input_arr[input_arr.index("as") + 1]
    variables.append(var_name)
    type_dict = {
        "integer": f"{var_name}: int = {initial_val if initial_val != "" else 0}",
        "character": f"{var_name}: str = {initial_val if initial_val != "" else f'""'}",
        "logical": f"{var_name}: bool = {initial_val if initial_val != "" else True}",
        "int64": f"{var_name}: int = {initial_val if initial_val != "" else 0}",
        "decimal": f"{var_name}: float = {initial_val if initial_val != "" else 0}",
        "date": f"{var_name}: datetime.date = {initial_val if initial_val != "" else date.today()}",
        "datetime": f"{var_name}: datetime.datetime = {initial_val if initial_val != "" else datetime.now()}",
    }
    return type_dict[var_type],variables

#FOR EACH loops get converted here
def for_each_loops(input_line,variable_list,start_db):
    print("for eaches 2", input_line)
    return_lines = []
    to_strip = ["NO-ERROR","NO-LOCK","EXCLUSIVE-LOCK","FOR","LAST","FIRST"]
    if start_db == False:
        return_lines.append("conn = sqlite3.connect(':memory:')")
        return_lines.append("cursor = conn.cursor()")
        start_db = True
    template = {
        "type": "",
        "table": "",
        "where": [
            {
                "left":"",
                "operator":"",
                "right": ""
            }
        ],
        "order_by":[
            {
                "field":"",
                "direction":"",
            }
        ],
        "lock":""
    }
    idx = input_line.lower().find("first")
    type = "first" if idx != -1 else ""
    if idx == -1:
        idx = input_line.lower().find("last")
        type = "last" if idx != -1 else ""
    if idx == -1:
        idx = input_line.lower().find("each")
        type = "each" if idx != -1 else ""
    if idx == -1:
        return ""
    for word in to_strip:
        input_line = input_line.replace(word, "")
    print("for eaches:",input_line)
    template["type"] = input_line[0:(idx + len(type))]
    if "where" in input_line.lower():
        table = input_line[0:input_line.lower().find("where")].strip().strip(".")
    elif "by" in input_line.lower():
        table = input_line[0:input_line.lower().find("by")].strip().strip(".")
    else:
        table = input_line[0:].strip().strip(".")
    template["table"] = table
    variable_list.append(table)
    if "by" in input_line.lower():
        end = input_line.lower().find("ascending") if ("ascending" in input_line.lower() or "asc" in input_line.lower()) else (input_line.lower().find("descending") or input_line.lower().find("desc"))
        template["order_by"][0]["field"] = input_line[input_line.lower().find("by") + 2 :end].strip()
        template["order_by"][0]["direction"] = "DESC" if ("descending" in input_line.lower() or "desc" in input_line.lower()) else "ASC"
        where_end = input_line.lower().find("by")
    else:
        where_end = input_line.lower().find("no-") if "no-" in input_line.lower() else input_line.lower().find("exclusive-") if "exclusive-" in input_line.lower() else len(input_line)
    where = input_line[input_line.lower().find("where"):where_end].strip()
    template["where"][0]["operator"] = "begins" if "begins" in where.lower() else "matches" if "matches" in where.lower() else "==" if ("=" in where or "eq" in where.lower()) else ("!=") 
    operator = where.find(template["where"][0]["operator"].upper())
    template["where"][0]["left"] = where[(where.find(".") + 1):operator].strip()
    template["where"][0]["right"] = where[operator + len(template["where"][0]["operator"]):].strip()
    
    query = f"'SELECT * FROM {template['table']} "
    if "where" in input_line.lower():
        query += f'WHERE {template["where"][0]["left"]} {template["where"][0]["operator"]} {template["where"][0]["right"].strip(":")}'
    if "by" in input_line.lower():
        query += f'BY {template["order_by"][0]["field"]} {template["order_by"][0]["direction"]} '    
    if type == "first" or type == "last":
        query += "LIMIT 1"

    query += "'"
    return_lines.append(f"cursor.execute({query})")
    if type == "first" or type == "last":
        return_lines.append(f"{template['table'].lower()} = cursor.fetchone()")
        return_lines.append(f'if {template["table"].lower()}:')
        
    else :
        return_lines.append(f"for {template['table'].lower()} in cursor:")
    return "\n".join(return_lines),variable_list,start_db

#This deals with DISPLAY and MESSAGE statements
def display_content(input_line):
    print("display statement 1",input_line)
    return_string = ""
    for i,word in enumerate(input_line[0].split(",")):
        
        if word.lower() == "message":
            return_string = return_string
        elif word.lower() == "display":
            return_string = return_string
        else:
            return_string += f'{word},'
    to_display = return_string.strip(",")
    return f'print({to_display})'

#This line works with any variable calculations in the code somewhere
def variable_calc(input_line):
    operators = ["+","-","/","*","MOD",">","<","<=",">="]
    operators = {
        "MOD":"%",
        "MODULO":"%"
    }
    new_string = ""
    words = input_line.split(" ")
    word_counts = Counter(words)
    duplicates = [word for word, count in word_counts.items() if count > 1]
    assembly = False
    for index,word in enumerate(words):
        if word in duplicates:
            assembly = True
            if words[index + 1] == "=" and words[index + 2] == word:
                new_string += f'{word} {words[index + 3]}= {words[len(words) - 1]}'
    if assembly == False:
        new_string = input_line
            
    return new_string
#This code converts Progress do and else do blocks
def do_blocks(input_line,variable_list):
    operators = ["+","-","/","*","MOD",">","<","<=",">=","or","and","="]
    print("if block",input_line)
    return_string = ""
    if "else" in input_line.lower():
        return "else:"
    for word in input_line.split():
        if word.lower() == "if":
            return_string += "if "
        elif '.' in word:
            if word[0:word.find(".")] in variable_list:
              return_string += f'{word[0:word.find(".")]}[{word[word.find(".") + 1:]}]'
        elif word in variable_list: 
            return_string += f'{word} '
        elif word.lower() in operators:
            if word == "=" or word.lower() == "eq":
                return_string += "== "
            elif word == "<>" or word.lower() == "ne":
                return_string += "!= "
            else:
                return_string += f'{word.lower()} '
        elif "lookup" in word:
            print("do",word)
        else:
            try:
                value = int(word)
                return_string += f'{word} '
            except ValueError:
                continue
    return_string += ":"
    return return_string.strip()
#This works with the procedure definitions in progress
def procedures(input_arr,variable_list):
    par_names = []
    output_type = []
    output_var = ""
    variables = {
        "DECIMAL":"float",
        "INTEGER": "int",
        "CHARACTER": 'str',
        "LOGICAL":"bool",
        "INT64":"int",
        "DATE":"datetime.date",
        "DATETIME":"datetime.datetime"

    }
    proc_name = list(input_arr[0].keys())[0]
    return_line = f'def {proc_name}('
    for item in input_arr[0][proc_name]:
        new_line = item.split()
        variable_list.append(new_line[3])
        if new_line[1].lower() == "input":
            par_names.append(f'{new_line[3]}:{variables[new_line[5]]}')
        else:
            output_type.append(f'->{variables[new_line[5]]}')
            output_var += f'{new_line[3]},'
    return_line += ",".join(par_names)
    return_line += f") {''.join(output_type)}:"    
    return return_line,variable_list,output_var.strip(",")
 #Assign statements get handled here   
def assign_content(input_line,variable_list):
    if input_line[len("assign")] == ",":
        assign = input_line[input_line.find(","):].strip().strip(",").strip(".").split(",")
    else:
        if "ASSIGN" in input_line:
            input_line = input_line.replace("ASSIGN","")
        elif "assign" in input_line:
            input_line = input_line.replace("assign","")
        assign = input_line.strip().strip(",").strip(".").split(",")

    for i, entry in enumerate(assign):
        print("variable assign 2",variable_list)
        if entry[0:entry.find(".")] in variable_list:
              left = f'{entry[0:entry.find(".")]}["{entry[entry.find(".") + 1:entry.find("=")].strip()}"]'
              right = entry[entry.find("="):]
              assign[i] = f'{left} {right}'
              
        #iPos = LOOKUP("Green", cList).
        elif "lookup" in entry.lower():
            assign[i] = lookups(entry)
        elif "entry" in entry.lower():
            assign[i] = entries(entry)
        assign[i] = variable_calc(assign[i])
    return "\n".join(assign)
#Find firsts or find lasts get handled here
def finds(input_line,db_started,variable_list):
    end_operators = ["=","eq","<>","ne"]
    to_strip = ["NO-ERROR","NO-LOCK","EXCLUSIVE-LOCK","FIND","LAST","FIRST"]
    return_lines = []
    line = input_line
    for word in to_strip:
        line = line.replace(word, "")
    if db_started == False:
        return_lines.append("conn = sqlite3.connect(':memory:')")
        return_lines.append("cursor = conn.cursor()")
        db_started = True
    template = {
        "table": "",
        "where": [
            {
                "left":"",
                "operator":"",
                "right": ""
            }
        ],
        "order_by":[
            {
                "field":"",
                "direction":"",
            }
        ],
    }
    if "where" in line.lower():
        template["table"] = line[0:line.lower().find("where")].strip().strip(".")
    else:
        template["table"] = line[0:].strip().strip(".")
    return_string = f"'SELECT * FROM {template['table']} "
    if "where" in line.lower():
        template["where"][0]["operator"] = next((var.lower() for var in end_operators if var.lower() in line), None).strip()
        template["where"][0]["left"] = line[line.lower().find("where") + len("WHERE"):line.find(template["where"][0]["operator"])].strip()
        template["where"][0]["right"] = line[line.find(template["where"][0]["operator"]) + 1:].strip().strip(".")
        return_string += f'WHERE {template["where"][0]["left"]} {template["where"][0]["operator"]} {template["where"][0]["right"]}'

    return_string += " LIMIT 1'"
    return_lines.append(f"cursor.execute({return_string})")
    return_lines.append(f"{template['table'].lower()} = cursor.fetchone()")
    variable_list.append(template['table'].strip())
    print("finds 2",variable_list)
    return "\n".join(return_lines),db_started,variable_list

def available(input_line):
    #IF AVAILABLE member THEN
    table_name = input_line[input_line.lower().find("available") + len("AVAILABLE"):input_line.lower().find("then")].strip()
    
    return f'if {table_name}:'
#Run statements used to run procedures get used here
def run_procedures(input_line):
    proc_name = input_line[len("RUN "):input_line.find("(")].strip()
    string_array = input_line[input_line.find("("):input_line.find(")")].strip().strip("(")
    arr = string_array.split(",")
    input_list = ""
    output_list = ""
    for par in arr:
        if "input" in par.lower():
            var = par.lower().replace("input", "").strip()
            input_list += f'{var},'
        elif "output" in par.lower():
            var = par.lower().replace("output", "").strip()
            output_list += f'{var},' 
    input_list = input_list.strip(",")
    output_list = output_list.strip(",")
    return_string = f'{output_list} = {proc_name}({input_list})'
    return return_string

def lookups(input_line):
    var = input_line[0:input_line.find("=")].strip()
    what = input_line[input_line.find("(") + 1:input_line.find(";")].strip()
    check_list = input_line[input_line.find(";") + 1:input_line.find(")")].strip()
    return f'{var} = {check_list}.find({what})'
    
def entries(input_line):
    print("entries 1",input_line)
    var = input_line[0:input_line.find("=")].strip()
    print("entries",input_line[input_line.find("(") + 1:input_line.find(";")].strip())
    idx = int(input_line[input_line.find("(") + 1:input_line.find(";")].strip()) - 1
    list = input_line[input_line.find(";") + 1:input_line.find(")")].strip()
    return f'{var} = {list}.split(",")[{idx}]'
