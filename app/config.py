from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv


load_dotenv()


def _parse_admin_ids(raw: str) -> List[int]:
    if not raw.strip():
        return []
    ids: List[int] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        ids.append(int(item))
    return ids


@dataclass(frozen=True)
class Settings:
    bot_token: str
    eternal_api_key: str
    eternal_api_url: str
    upi_id: str
    port: int
    admin_user_ids: List[int]
    timezone: str
    retention_enabled: bool
    payment_wall_enabled: bool
    eternal_model: str
    database_path: str
    callback_secret: str
    external_access_enabled: bool
    payments_db_host: str
    payments_db_port: int
    payments_db_user: str
    payments_db_pass: str
    payments_db_name: str
    subs_db_host: str
    subs_db_port: int
    subs_db_user: str
    subs_db_pass: str
    subs_db_name: str
    payments_db_check_query: str
    subs_db_check_query: str


def get_settings() -> Settings:
    retention_value = os.getenv("RETENTION_ENABLED", "false").strip().lower()
    payment_wall_value = os.getenv("PAYMENT_WALL_ENABLED", "true").strip().lower()
    external_access_value = os.getenv("EXTERNAL_ACCESS_ENABLED", "false").strip().lower()
    return Settings(
        bot_token=os.getenv("BOT_TOKEN", "").strip(),
        eternal_api_key=os.getenv("ETERNAL_API_KEY", "").strip(),
        eternal_api_url=os.getenv(
            "ETERNAL_API_URL", "https://open.eternalai.org/v1/chat/completions"
        ).strip(),
        upi_id=os.getenv("UPI_ID", "").strip(),
        port=int(os.getenv("PORT", "8000")),
        admin_user_ids=_parse_admin_ids(os.getenv("ADMIN_USER_IDS", "")),
        timezone=os.getenv("TIMEZONE", "Asia/Kolkata").strip(),
        retention_enabled=retention_value in {"1", "true", "yes", "on"},
        payment_wall_enabled=payment_wall_value in {"1", "true", "yes", "on"},
        eternal_model=os.getenv("ETERNAL_MODEL", "uncensored-eternal-ai-1.0").strip(),
        database_path=os.getenv("DATABASE_PATH", "savita.db").strip(),
        callback_secret=os.getenv("CALLBACK_SECRET", "").strip(),
        external_access_enabled=external_access_value in {"1", "true", "yes", "on"},
        payments_db_host=os.getenv("PAYMENTS_DB_HOST", "").strip(),
        payments_db_port=int(os.getenv("PAYMENTS_DB_PORT", "3306")),
        payments_db_user=os.getenv("PAYMENTS_DB_USER", "").strip(),
        payments_db_pass=os.getenv("PAYMENTS_DB_PASS", "").strip(),
        payments_db_name=os.getenv("PAYMENTS_DB_NAME", "").strip(),
        subs_db_host=os.getenv("SUBS_DB_HOST", "").strip(),
        subs_db_port=int(os.getenv("SUBS_DB_PORT", "3306")),
        subs_db_user=os.getenv("SUBS_DB_USER", "").strip(),
        subs_db_pass=os.getenv("SUBS_DB_PASS", "").strip(),
        subs_db_name=os.getenv("SUBS_DB_NAME", "").strip(),
        payments_db_check_query=os.getenv(
            "PAYMENTS_DB_CHECK_QUERY",
            (
                "SELECT 1 FROM payments "
                "WHERE (telegram_id = %s OR username = %s) "
                "AND status IN ('success','paid','approved','completed') "
                "ORDER BY id DESC LIMIT 1"
            ),
        ).strip(),
        subs_db_check_query=os.getenv(
            "SUBS_DB_CHECK_QUERY",
            (
                "SELECT 1 FROM subscriptions "
                "WHERE (telegram_id = %s OR username = %s) "
                "AND status = 'active' "
                "AND (expires_at IS NULL OR expires_at > NOW()) "
                "ORDER BY id DESC LIMIT 1"
            ),
        ).strip(),
    )
