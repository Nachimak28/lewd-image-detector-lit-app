
import os
import uvicorn
import lightning as L
from dataclasses import dataclass
from lewd_image_detector_lit_api import app as api

@dataclass
class CustomBuildConfig(L.BuildConfig):
    """
    Custom build config defined for API work component.
    """
    def build_commands(self):
        return ["sudo apt-get update", 
                "sudo apt-get install -y unzip",
                "curl --output private_detector.zip https://storage.googleapis.com/private_detector/private_detector.zip",
                "unzip -x private_detector.zip"
                ]


class FastAPIWork(L.LightningWork):
    """
    API Work component to run the image classifier put behind the api
    """
    def __init__(self, parallel: bool = False, **kwargs):
        super().__init__(parallel=parallel, cloud_build_config=CustomBuildConfig(), **kwargs)
    
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
        if os.environ.get("TESTING_LAI"):
            print("⚡ Lightning Research App! ⚡")
        self.fastapi_work.run()
    
    def configure_layout(self):
        return {"name":"Swagger", "content":self.fastapi_work.url}


if __name__=="__main__":
    app = L.LightningApp(RootFlow())
