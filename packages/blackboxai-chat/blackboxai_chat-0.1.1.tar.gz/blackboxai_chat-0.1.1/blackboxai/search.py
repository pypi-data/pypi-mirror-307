import os
import aiohttp
import asyncio
import requests
import uuid

from blackboxai import constants

TIMEOUT = 60 * 3  # 3min


async def asearch_code(query: str, code_string: str, code_id: str = None):
    payload = {
        'query': query,
        'codebaseString': code_string,
        'codebaseId': code_id or str(uuid.uuid4())
    }
    headers = {'Content-Type': 'application/json'}

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as session:
            async with session.post(constants.rag_endpoint, json=payload, headers=headers) as response:
                if response.status != 200:
                    return {'response': ''}
                _response = await response.json()
                return {'response': _response['context']}
    except Exception as e:
        return {'response': ''}


def search_code(query: str, code_string: str, code_id: str = None):
    payload = {
        'query': query,
        'codebaseString': code_string,
        'codebaseId': code_id or str(uuid.uuid4())
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(constants.rag_endpoint, json=payload, headers=headers, timeout=TIMEOUT)
        if response.status_code != 200:
            return None
        _response = response.json()
        return _response['context']
    except Exception as e:
        return None
