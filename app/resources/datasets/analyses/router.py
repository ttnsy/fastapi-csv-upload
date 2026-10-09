from typing import Annotated

import pyarrow.parquet as pq
from fastapi import APIRouter, Query

from app.api.annotations import SessionDep, UploadDirDep
from app.resources.datasets.analyses.schema import AnalysisParams
from app.resources.datasets.analyses.service import aggregate_dataframe
from app.resources.datasets.service import get_dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("/{stored_name}/analysis", status_code=200)
async def get_value_analysis(
    stored_name: str,
    params: Annotated[AnalysisParams, Query()],
    upload_dir: UploadDirDep,
    session: SessionDep,
):
    metadata, path = get_dataset(stored_name, session, upload_dir)
    df = pq.read_table(path).to_pandas()
    return aggregate_dataframe(df, metadata, params).to_dict(orient="records")
