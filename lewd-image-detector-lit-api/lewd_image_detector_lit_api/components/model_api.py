import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from .lewd_image_detector_model import LewdImageDetector

# load model
lewd_img_detector_model = LewdImageDetector()
# print('model loaded')

description = """<h3>An API for a DL model to detect if an input image is a lewd image or not. 
                This is an important content moderation application which we are using for chat app integration</h3>"""

app = FastAPI(title='Bumble Lewd image detector model API', description=description)

# Data Model Validation class for predict api
class RequestModel(BaseModel):
    encoded_image_str: str

@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")

@app.get("/api/health")
def health():
    return True

@app.post("/api/predict")
async def predict_api(request: RequestModel):
    lewd_image_flag = lewd_img_detector_model.predict(encoded_image_str=request.encoded_image_str)
    return {"lewd_image_flag": lewd_image_flag}


if __name__ == "__main__":
    uvicorn.run(app)