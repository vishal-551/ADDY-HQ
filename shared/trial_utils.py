from __future__ import annotations

from datetime import datetime

from shared.date_utils import add_days, is_expired, utcnow
from shared.enums import AccessSource, AccessStatus, PlanType


def calculate_trial_window(trial_days: int, now: datetime | None = None) -> tuple[datetime, datetime]:
    start = now or utcnow()
    end = add_days(start, trial_days)
    return start, end


def can_start_trial(*, has_previous_trial: bool, has_active_paid_plan: bool, trials_enabled: bool) -> bool:
    return trials_enabled and not has_previous_trial and not has_active_paid_plan


def trial_access_payload(guild_id: int, trial_days: int) -> dict[str, object]:
    start_at, end_at = calculate_trial_window(trial_days)
    return {
        "guild_id": guild_id,
        "plan": PlanType.TRIAL.value,
        "status": AccessStatus.ACTIVE.value,
        "source": AccessSource.TRIAL.value,
        "starts_at": start_at,
        "expires_at": end_at,
    }


def trial_is_active(expires_at: datetime | None) -> bool:
    return not is_expired(expires_at)
