from fastapi import APIRouter

from app.api.v1 import auth, profiles, jobs, matches, applications, outreach

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(matches.router, prefix="/matches", tags=["Matches"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(outreach.router, prefix="/outreach", tags=["Outreach"])
