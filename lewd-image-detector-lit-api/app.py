
import uvicorn
import lightning as L
from lewd_image_detector_lit_api import app as api


class FastAPIWork(L.LightningWork):
    """
    API Work component to run the image classifier put behind the api
    """
    def __init__(self, parallel: bool = False, **kwargs):
        super().__init__(parallel=parallel, **kwargs)
    
    def run(self):
        uvicorn.run(api, host=self.host, port=self.port)



class RootFlow(L.LightningFlow):
    """
    Root flow for Lightning app
    """
    def __init__(self):
        super().__init__()
        self.fastapi_work = FastAPIWork()
    
    def run(self, *args, **kwargs) -> None:
        self.fastapi_work.run()
    
    def configure_layout(self):
        return {"name":"Swagger", "content":self.fastapi_work.url}


if __name__=="__main__":
    app = L.LightningApp(RootFlow())
