from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentData(BaseModel):
    course: str
    type: str
    grade: str
    username: str
    password: str

@app.post("/start-solve")
async def start_solve(data: StudentData):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://qureo.education", timeout=60000)
            await page.fill('input[type="text"]', data.username)
            await page.fill('input[type="password"]', data.password)
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
            return {"status": "success", "message": f"تم الدخول بنجاح لحساب {data.username}"}
        except Exception as e:
            return {"status": "error", "message": f"حدث خطأ: {str(e)}"}
        finally:
            await browser.close()