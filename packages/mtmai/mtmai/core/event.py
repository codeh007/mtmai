from pydantic import BaseModel


async def emit_flow_event(event: str, resource_id: str, data: dict | BaseModel = {}):
    from prefect.events import emit_event

    _data = data.model_dump() if isinstance(data, BaseModel) else data
    event = emit_event(
        event=event,
        resource={
            **_data,
            "prefect.resource.id": str(resource_id),
        },
    )
    return event
