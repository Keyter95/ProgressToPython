from fastapi import FastAPI,Request # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from routingFunctions import progress_to_python,python_to_progress


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/convert")
async def converter(request: Request):
    body = await request.json()
    input = body["code"]
    fromLang = body["from"]
    toLang = body["to"]
    
    input_arr = input.split("\n")
    return_lines = []
    
    output_var = ""
    if fromLang == "progress" and toLang == "python":
       return_lines = progress_to_python(input_arr)
        
    elif fromLang == "python" and toLang == "progress":
        print("bernadette 13--->",input_arr)
        return_lines = python_to_progress(input_arr)

    elif fromLang == toLang:
        return_lines = input_arr
    return {"converted_code": "\n".join(return_lines)}


