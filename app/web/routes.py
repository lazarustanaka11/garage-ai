from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "Dashboard",
        },
    )


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "title": "Login",
        },
    )
    
@router.get("/customers", response_class=HTMLResponse)
def customers(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="customers.html",
        context={
            "title": "Customers",
        },
    )
    
@router.get("/vehicles", response_class=HTMLResponse)
def vehicles(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="vehicles.html",
        context={
            "title": "Vehicles",
        },
    )
    

@router.get("/repair-jobs", response_class=HTMLResponse)
def repair_jobs(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="repair_jobs.html",
        context={
            "title": "Repair Jobs",
        },
    )

@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "title": "Register",
        },
    )
