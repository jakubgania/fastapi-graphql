from fastapi import APIRouter, HTTPException
import httpx

from config import get_settings

settings = get_settings()

router = APIRouter(prefix="/graphql")

@router.post("/github-profile")
async def github_profile():
    query = """
    query {
        viewer {
            login
            name
            bio
            avatarUrl
        }
    }
    """

    headers = {
        "Authorization": f"Bearer {settings.github_api_token}",
        "Conent-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.github_graphql_endpoint,
            json={"query": query},
            headers=headers
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    
    return response.json()

@router.get("/github-profile/{username}")
async def github_profile(username: str):
    query = """
    query($username: String!) {
        user(login: $username) {
            id
            login
            avatarUrl
            url
            name
            bio
            twitterUsername
            websiteUrl
            followers {
                totalCount
            }
            following {
                totalCount
            }
        }
    }
    """

    headers = {
        "Authorization": f"Bearer {settings.github_api_token}",
        "Content-Type": "application/json",
    }

    variables = {
        "username": username
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.github_graphql_endpoint,
            json={"query": query, "variables": variables},
            headers=headers
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    

    return response.json()