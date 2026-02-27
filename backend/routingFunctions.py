import re
from functionsToPython import variable_declaration,for_each_loops,display_content,variable_calc,do_blocks,procedures,assign_content,finds,available,run_procedures
from functionsToProgress import variable_declaration_progress,print_to_display,function_declaration,if_blocks,variable_assignment

def progress_to_python(input_arr):
    display_still = False
    assign_still = False
    end_of_find = True
    variable_list = []
    python_lines = []
    procedure_arr = []
    procedure_name = ""
    indent = 0
    display_line = ""
    assign_line = ""
    end_of_loop = True
    for_array = []
    for_server_started = False
    is_single_line_if = False
    tables_find = []
    run_statement_still = False
    run_lines = []
    for line in input_arr:  
            clean_line = line.strip()
            if not clean_line: continue
            
            if clean_line == "END.":
                indent -= 1
            
            elif bool(re.match("define\s+variable",clean_line,re.IGNORECASE)):
                line,variable_list = variable_declaration(clean_line,variable_list)
                python_lines.append(line)
            elif (bool(re.match(r'^\s*for\s+each(?=(?:[^"]*"[^"]*")*[^"]*$)', clean_line, re.IGNORECASE)) or end_of_loop == False) or (bool(re.match(r'^\s*for\s+first(?=(?:[^"]*"[^"]*")*[^"]*$)', clean_line, re.IGNORECASE)) or end_of_loop == False):
                if clean_line[len(clean_line) - 1] != ":":
                    end_of_loop = False
                    for_array.append(clean_line)
                    continue
                else:
                    for_array.append(clean_line)
                    clean_line = " ".join(for_array)
                    end_of_loop = True
                if end_of_loop:
                    return_line,variable_list,for_server_started = for_each_loops(clean_line,variable_list,for_server_started)
                    line_to_space = return_line.split("\n")
                    line = ""
                    for item in line_to_space:
                        line += f'\n{'\t' * indent}{item}'
                    python_lines.append(line)
                    indent += 1
            elif bool(re.match(r'^\s*find(?=(?:[^"]*"[^"]*")*[^"]*$)',clean_line,re.IGNORECASE)) or end_of_find == False:
                if clean_line[len(clean_line) - 1] != ".":
                    end_of_find = False
                    for_array.append(clean_line)
                    continue
                else:
                    for_array.append(clean_line)
                    clean_line = " ".join(for_array)
                    end_of_find = True
                if end_of_find:
                    for_array.clear()
                    line_to_clean,for_server_started,variable_list = finds(clean_line,for_server_started,variable_list)
                    line_to_space = line_to_clean.split("\n")
                    line = ""
                    for item in line_to_space:
                        line += f'\n{'\t' * indent}{item}'
                python_lines.append(line)
            elif bool(re.search("run",clean_line,re.IGNORECASE)) or run_statement_still == True:
                if clean_line[len(clean_line) - 1] != ".":
                    run_statement_still = True
                    run_lines.append(clean_line)
                    continue
                else:
                    run_lines.append(clean_line)
                    clean_line = " ".join(run_lines)
                    run_statement_still = False
                    line = run_procedures(clean_line)
                    
                    python_lines.append(f'\n{'\t' * indent}{line}')
            elif bool(re.search("available",clean_line,re.IGNORECASE)) and any(var in clean_line for var in tables_find):
                python_lines.append(available(clean_line))
                indent += 1
                if "DO:" in clean_line.upper():
                    is_single_line_if = False
                else:
                    is_single_line_if = True
            elif bool(re.match("assign",clean_line.lower(),re.IGNORECASE)) or assign_still == True:
                if "lookup" in clean_line.lower():
                    clean_line = clean_line.replace(",",";")
                elif "entry" in clean_line.lower():
                    clean_line = clean_line.replace(",",";")
                if clean_line[len(clean_line) - 1] != ".":
                    assign_line += f'|{clean_line}'
                    assign_still = True
                    continue
                else:
                    assign_line += f'|{clean_line}'
                    assign_still = False
                    line_to_space= assign_content(assign_line.strip("|"),variable_list).split("\n")
                    line = ""
                    for item in line_to_space:
                        line += f'\n{'\t' * indent}{item}'
                    python_lines.append(line)
                    assign_line = ""
            elif (bool(re.match("display",clean_line,re.IGNORECASE)) or bool(re.match("message",clean_line,re.IGNORECASE))) or display_still == True:
                if clean_line[len(clean_line) - 1] != ".":
                    display_line += f',{clean_line}'
                    display_still = True
                    continue
                else:
                    display_line += f',{clean_line}'
                    display_still = False
                    clean_line = re.sub(r"^(MESSAGE|DISPLAY)\s+", "", display_line.strip(","), flags=re.IGNORECASE)
                    clean_line = re.sub(r"VIEW-AS\s+ALERT-BOX.*", "", clean_line, flags=re.IGNORECASE)
                    parts = re.findall(r'"[^"]*"|\S+', clean_line.strip("."))
                    python_lines.append(f"{'\t' * indent}{display_content(parts)}")
                    display_line = ""
            elif bool(re.search(r"\bthen\b|\belse\b", clean_line, re.IGNORECASE)):
                if is_single_line_if and clean_line.upper().startswith("ELSE"):
                    indent -= 1
                    is_single_line_if = False
                python_lines.append(f'{'\t' * indent}{do_blocks(clean_line,variable_list)}') 
                indent += 1
                if "DO:" in clean_line.upper():
                    is_single_line_if = False
                else:
                    is_single_line_if = True
            elif clean_line == "DO:":
                indent += 1     
            elif bool(re.match("procedure",clean_line,re.IGNORECASE)):
                procedure_name = clean_line[0 + len("procedure "):].strip().strip(":")
                procedure_arr.append({procedure_name : []})
                indent += 1
            elif bool (re.search("input\s+parameter",clean_line,re.IGNORECASE)):
                procedure_arr[0][procedure_name].append(clean_line)
            elif bool (re.search("output\s+parameter",clean_line,re.IGNORECASE)):
                procedure_arr[0][procedure_name].append(clean_line)
                line, variable_list,output_var = procedures(procedure_arr,variable_list)
                python_lines.append(line)
                
            elif clean_line == "END PROCEDURE.":
                python_lines.append(f'{'\t' * indent}return {output_var}')
                indent -= 1
                output_var = ""
                procedure_arr.clear()
            elif any(var in clean_line for var in variable_list):
                python_lines.append(f'{'\t' * indent}{variable_calc(clean_line,variable_list)}') 

            #if is_single_line_if and not clean_line.upper().startswith("ELSE"):
             #   indent -= 1
             #   is_single_line_if = False
    if for_server_started:
        importArr = ["import sqlite3"]
        importArr.extend(python_lines)
        return importArr
    return python_lines

def python_to_progress(input_arr):
    variable_lines = []
    variable_list = []
    indent = 0
    progress_lines = []
    for line in input_arr:  
        clean_line = line.strip()     
        if bool(re.match("print\(",clean_line,re.IGNORECASE)):
            line = print_to_display(clean_line)
            progress_lines.append(line)
        elif bool(re.match("def",clean_line,re.IGNORECASE)):
            indent += 1
            line,variable_list = function_declaration(clean_line,variable_list,indent)
            progress_lines.append(line)
        elif(bool(re.match("if",clean_line,re.IGNORECASE)) or bool(re.match("else:",clean_line,re.IGNORECASE))):
            indent += 1
            progress_lines.append(if_blocks(clean_line,"if" if bool(re.match("if",clean_line,re.IGNORECASE)) else "else"))
        elif bool(re.search(":",clean_line,re.IGNORECASE) and bool(re.search("=",clean_line,re.IGNORECASE))):
            line,variable_list = variable_declaration_progress(clean_line,variable_list)
            variable_lines.append(line)
        elif bool(re.search("=",clean_line,re.IGNORECASE)) and not any(var in clean_line for var in variable_list):
            line,variable_list = variable_assignment(clean_line,variable_list)
            variable_lines.append(line)
    variable_lines.extend(progress_lines)
    return variable_lines