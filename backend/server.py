from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio, os, sys

# TODO: Change the reading logic to Arduino

someone_in_despatxet = False
read_task = None 

@asynccontextmanager
async def lifespan(app: FastAPI):
    global read_task
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "testfile.txt"))
    read_task = asyncio.create_task(read(file_path))
    
    yield
    
    # Shutdown logic
    if read_task is not None:
        read_task.cancel()
        try:
            await read_task
        except asyncio.CancelledError:
            pass

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #! For development only, restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"occupied": someone_in_despatxet}

async def read(filepath: str):
    global someone_in_despatxet
    while True:
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    data = file.read()
                    if "YES" in data:
                        someone_in_despatxet = True
                    else:
                        someone_in_despatxet = False
            else:
                print(f"File {filepath} does not exist.")
                sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}")
        await asyncio.sleep(1)
