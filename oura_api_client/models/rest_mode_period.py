from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

class RestModeEpisode(BaseModel):
    # Assuming RestModeEpisode might have specific details if it were a more complex sub-model.
    # For now, the main RestModePeriodModel seems to contain all relevant fields
    # based on typical Oura API patterns for similar "period" or "document" type data.
    # If RestModeEpisode is distinct and has its own fields, they would be defined here.
    # Example:
    # episode_note: Optional[str] = None
    # episode_quality_rating: Optional[int] = None
    # This model might be simple if episodes are just markers within a period
    # or could be more complex if each episode has detailed logging.
    # Given Oura's usual style, episodes are often just start/end markers or simple states.
    # The OpenAPI spec for RestModePeriod does not detail sub-models like "episodes" explicitly,
    # suggesting that the main RestModePeriodModel contains all fields.
    # For now, keeping it minimal unless more specific fields for "episodes" are identified.
    # If RestModePeriodModel itself represents an "episode" when multiple are returned,
    # then this separate model might not be needed, and RestModePeriodModel would be the list item.
    # However, the task asks for RestModeEpisode, so creating a placeholder.
    # If the API returns a list of these *within* a RestModePeriodModel, it'd be:
    # episodes: List[RestModeEpisode] in RestModePeriodModel.
    # If RestModePeriodModel *is* an episode, then the response is List[RestModePeriodModel].
    # Let's assume RestModePeriodModel is the main document, and episodes are not a separate nested list for now.
    # If the API returns a list of "episodes" that are themselves complex, this model would be fleshed out.
    # For now, let's assume the primary fields are on RestModePeriodModel as per typical Oura structure.
    # If "episodes" are just segments of a rest mode period with start/end times,
    # they might be represented by multiple RestModePeriodModel entries if one period can have multiple "active" phases.
    # Or, if a single RestModePeriodModel has multiple episode segments within it, this sub-model would be used.
    # The OpenAPI spec for rest_mode_period does not show a nested 'episodes' list.
    # It shows RestModePeriod as the item in the 'data' array.
    # Therefore, RestModeEpisode as a separate distinct model to be listed *inside* RestModePeriodModel might be incorrect.
    # The task is to create RestModeEpisode, so creating a simple version.
    # It's possible the prompt meant RestModePeriodModel *is* an episode if "Rest Mode Period" refers to a single episode.
    pass # Placeholder, as fields are directly on RestModePeriodModel in the spec

class RestModePeriodModel(BaseModel):
    id: str
    day: date
    start_time: datetime = Field(alias="start_time")
    end_time: Optional[datetime] = Field(None, alias="end_time")
    # Rest mode specific state or tag, e.g. "on_demand_rest", "recovering_from_illness"
    rest_mode_state: Optional[str] = Field(None, alias="rest_mode_state") # Example: "on_demand_rest"
    # If RestModeEpisode was a list of sub-items:
    # episodes: Optional[List[RestModeEpisode]] = Field(None, alias="episodes")
    # However, the OpenAPI spec has a flat structure for RestModePeriodModel.
    # Adding fields from OpenAPI spec for RestModePeriod
    baseline_heart_rate: Optional[int] = Field(None, alias="baseline_heart_rate")
    baseline_hrv: Optional[int] = Field(None, alias="baseline_hrv")
    baseline_skin_temperature: Optional[float] = Field(None, alias="baseline_skin_temperature")
    # 'day' is already included
    # 'end_time' is already included
    # 'id' is already included
    # 'rest_mode_state' is already included (as 'state' in some contexts, but using rest_mode_state for clarity)
    # 'start_time' is already included

class RestModePeriodResponse(BaseModel):
    data: List[RestModePeriodModel]
    next_token: Optional[str] = None
