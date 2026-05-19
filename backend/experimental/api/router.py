from fastapi import FastAPI, HTTPException

from app.core.logger import logger

try:
    from experimental.civilization.civilization_core import initialize_civilization
    from experimental.civilization.evolution_cycle import evolve_civilization
    from experimental.agi.agi_supervisor import supervise
except Exception as experimental_import_error:
    initialize_civilization = None
    evolve_civilization = None
    supervise = None
    logger.warning("Experimental routes disabled: %s", experimental_import_error)


def register_experimental_routes(app: FastAPI, extract_last_message):
    @app.post("/initialize-civilization")
    async def initialize_civilization_route():
        if initialize_civilization is None:
            raise HTTPException(status_code=503, detail="Experimental module indisponível")
        return initialize_civilization()

    @app.post("/evolve-civilization")
    async def evolve_civilization_route():
        if evolve_civilization is None:
            raise HTTPException(status_code=503, detail="Experimental module indisponível")
        return evolve_civilization("")

    @app.get("/civilization")
    async def civilization_status():
        if initialize_civilization is None:
            raise HTTPException(status_code=503, detail="Experimental module indisponível")
        return initialize_civilization()

    @app.post("/civilization/evolve")
    async def civilization_evolve(req):
        if evolve_civilization is None:
            raise HTTPException(status_code=503, detail="Experimental module indisponível")
        prompt = extract_last_message(req)
        return evolve_civilization(prompt)

    @app.post("/supervise")
    async def supervise_route(req):
        if supervise is None:
            raise HTTPException(status_code=503, detail="Experimental module indisponível")
        task = extract_last_message(req)
        return supervise(task)

    @app.post("/agi")
    async def agi_route(req):
        if supervise is None:
            raise HTTPException(status_code=503, detail="Experimental module indisponível")
        prompt = extract_last_message(req)
        return supervise(prompt)
