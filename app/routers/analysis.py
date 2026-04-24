from typing import Annotated

import pyarrow.parquet as pq
from fastapi import APIRouter, HTTPException, Query

from app.crud import get_metadata_by_name
from app.dependencies import SessionDep, UploadDirDep
from app.schemas import AnalysisParams
from app.utils.analysis import aggregate_dataframe

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{stored_name}")
async def get_value_analysis(
    stored_name: str,
    params: Annotated[AnalysisParams, Query()],
    upload_dir: UploadDirDep,
    session: SessionDep,
):
    parquet_path = (upload_dir / stored_name).with_suffix(".parquet")
    if not parquet_path.exists():
        raise HTTPException(status_code=404, detail="Data file not found")

    metadata = get_metadata_by_name(session, stored_name)
    if not metadata:
        raise HTTPException(status_code=404, detail="Dataset not found")

    table = pq.read_table(parquet_path)
    df = table.to_pandas()

    result = aggregate_dataframe(df, metadata, params)
    return result.to_dict(orient="records")
    return result.to_dict(orient="records")
