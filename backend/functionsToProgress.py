operators = {
    "!=":"<>",
    "==":"="
}
def variable_declaration_progress(string,variables):
    template = {
        "name": "",
        "type": "",
        "initial_val": ""
    }
    template["name"] = string[0:string.find(":")].strip()
    template["type"] = string[string.find(":") + 1:string.find("=") - 1].strip()
    template["initial_val"] = string[string.find("=") + 1:].strip()
    
    variables.append(template["name"])
    type_dict = {
        "int": f"DEFINE VARIABLE {template['name']} AS INTEGER NO-UNDO INITIAL {template['initial_val']}.",
        "str": f"DEFINE VARIABLE {template['name']} AS CHARACTER NO-UNDO INITIAL {template['initial_val']}.",
        "bool": f"DEFINE VARIABLE {template['name']} AS LOGICAL NO-UNDO INITIAL {template['initial_val']}.",
        "float": f"DEFINE VARIABLE {template['name']} AS DECIMAL NO-UNDO INITIAL {template['initial_val']}.",
        "datetime.date": f"DEFINE VARIABLE {template['name']} AS DATE NO-UNDO INITIAL {template['initial_val']}.",
        "datetime.datetime": f"DEFINE VARIABLE {template['name']} AS DATETIME NO-UNDO INITIAL {template['initial_val']}.",
    }
    returnString = type_dict[template["type"]] if template["type"] in type_dict else "No match found"
    return returnString,variables

def print_to_display(input_string):
    clean_line = input_string[input_string.find("(") + 1:input_string.find(")")].strip()
    clean_arr = clean_line.split(",")
    return_line = "DISPLAY\n"
    for index,item in enumerate(clean_arr):
        return_line += item
        if index < len(clean_arr) - 1:
            return_line += "\n"
        else:
            return_line += "."
    return return_line

def function_declaration(input_line,variable_list,indent):
    variables = {
        "float":"DECIMAL",
        "int": "INTEGER",
        "str": 'CHARACTER',
        "bool":"LOGICAL",
        "datetime.date":"DATE",
        "datetime.datetime":"DATETIME"
    }
    proc_name = input_line[len("def "):input_line.find("(")].strip()
    outputs = input_line[input_line.find("->") + 1:input_line.find(":")]
    inputs = input_line[input_line.find("(") + 1:input_line.find(")")].split(",")
    if "->" in input_line:
        outputs = input_line[input_line.find("->") + 2:input_line.find(":")].strip()
        outputs = [x.strip() for x in outputs.split(",")]
    else:
        outputs = []
    return_arr = [f'PROCEDURE {proc_name}:']
    for var in inputs:
        if ":" in var:
            var_name = var[0:var.find(":")]
            var_type = variables[var[var.find(":") + 1:].strip()]
            return_arr.append(f'{'\t' * indent}DEFINE INPUT PARAMETER {var_name} AS {var_type} NO-UNDO.')

            variable_list.append(var_name)

    for out in outputs:
        if ":" in out:
            var_name, var_type = out.split(":")
            var_type = variables[var_type.strip()]
            return_arr.append(f"{'\t' * indent}DEFINE OUTPUT PARAMETER {var_name.strip()} AS {var_type} NO-UNDO.")

    return "\n".join(return_arr),variable_list

def if_blocks(input_line,type):
    #if customers[customer_id] != "Active":
    arr = input_line.split()
    if type =="if":
        return_sentence = f"IF "
        for item in arr:
            if item == "if":
                continue
            var = item.strip().strip(":")
            if var in operators:
                return_sentence += f'{operators[var]} '
            else:
                return_sentence += f'{var} '
        return_sentence += "THEN DO:"
    else:
        return_sentence = "ELSE DO:"
    return return_sentence

def variable_assignment(input_line,variable_list):
    variables = {
        "float":"DECIMAL",
        "int": "INTEGER",
        "str": 'CHARACTER',
        "bool":"LOGICAL",
        "datetime.date":"DATE",
        "datetime.datetime":"DATETIME"
    }
    template = {
        "name":"",
        "type":"",
        "initial":""
    }
    template["name"] = input_line[0:input_line.find("=")].strip()
    value = type(input_line[input_line.find("=") + 1:].strip())
    template["type"] = variables[value] if value in variables else "CHARACTER"
    template["initial"] = input_line[input_line.find("=") + 1:].strip()
    variable_list.append(template["name"])
    return f'DEFINE VARIABLE {template["name"]} AS {template["type"]} NO-UNDO INITIAL {template["initial"]}.',variable_list

