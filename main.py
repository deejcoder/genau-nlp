import uvicorn
import apps


uvicorn.run(apps.web_app, host="0.0.0.0", port=8000)



