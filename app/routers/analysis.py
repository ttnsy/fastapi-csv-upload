from typing import Annotated

import pyarrow.parquet as pq
from fastapi import APIRouter, HTTPException, Query

from app.crud import get_metadata_by_name
from app.dependencies import ParquetPathDep, SessionDep
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
    parquet_path: ParquetPathDep,
    session: SessionDep,
):
    metadata = get_metadata_by_name(session, stored_name)
    if not metadata:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = pq.read_table(parquet_path).to_pandas()

    result = aggregate_dataframe(df, metadata, params)
    return result.to_dict(orient="records")
