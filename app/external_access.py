from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pymysql


@dataclass(frozen=True)
class ExternalMySQLConfig:
    enabled: bool
    payments_host: str
    payments_port: int
    payments_user: str
    payments_pass: str
    payments_name: str
    subs_host: str
    subs_port: int
    subs_user: str
    subs_pass: str
    subs_name: str
    payments_query: str
    subs_query: str


class ExternalSubscriptionVerifier:
    """
    Verifies access against external xibots MySQL databases.

    Query conventions:
    - payments_query receives two parameters: (telegram_id, username_or_empty)
    - subs_query receives two parameters: (telegram_id, username_or_empty)
    - Any returned row is treated as a positive access signal.
    """

    def __init__(self, cfg: ExternalMySQLConfig) -> None:
        self.cfg = cfg

    def _query_exists(
        self,
        *,
        host: str,
        port: int,
        user: str,
        password: str,
        db: str,
        query: str,
        telegram_id: int,
        username: Optional[str],
    ) -> bool:
        if not query.strip():
            return False
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db,
            connect_timeout=4,
            read_timeout=4,
            write_timeout=4,
            cursorclass=pymysql.cursors.Cursor,
            autocommit=True,
        )
        try:
            with conn.cursor() as cur:
                cur.execute(query, (telegram_id, username or ""))
                row = cur.fetchone()
                return row is not None
        finally:
            conn.close()

    def has_access(self, telegram_id: int, username: Optional[str]) -> bool:
        if not self.cfg.enabled:
            return False

        paid = self._query_exists(
            host=self.cfg.payments_host,
            port=self.cfg.payments_port,
            user=self.cfg.payments_user,
            password=self.cfg.payments_pass,
            db=self.cfg.payments_name,
            query=self.cfg.payments_query,
            telegram_id=telegram_id,
            username=username,
        )
        if paid:
            return True

        active_sub = self._query_exists(
            host=self.cfg.subs_host,
            port=self.cfg.subs_port,
            user=self.cfg.subs_user,
            password=self.cfg.subs_pass,
            db=self.cfg.subs_name,
            query=self.cfg.subs_query,
            telegram_id=telegram_id,
            username=username,
        )
        return active_sub
