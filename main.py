from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    resume: str
    jobDesc: str

@app.post("/generate")
async def generate(data: RequestData):
    prompt = f"""
You are a professional resume writer.

Resume:
{data.resume}

Job Description:
{data.jobDesc}

Tasks:
1. Rewrite resume tailored to job
2. Add ATS keywords
3. Improve bullet points
4. Create a short cover letter

Output clearly with headings.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"result": response.choices[0].message.content}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)