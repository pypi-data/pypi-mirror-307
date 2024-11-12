from typing import List

from buco_db_controller.models.fixture_stats import FixtureStats
from buco_db_controller.repositories.fixture_stats_repository import FixtureStatsRepository
from buco_db_controller.services.fixture_service import FixtureService


class FixtureStatsService:
    football = 'api_football'
    flashscore = 'flashscore'

    def __init__(self):
        self.api_footbal_repository = FixtureStatsRepository(self.football)
        self.flashscore_repository = FixtureStatsRepository(self.flashscore)
        self.fixture_service = FixtureService()

    def upsert_many_fixture_stats(self, fixture_stats: List[dict], source):
        if source == self.football:
            self.api_footbal_repository.upsert_many_fixture_stats(fixture_stats)
        elif source == self.flashscore:
            self.flashscore_repository.upsert_many_fixture_stats(fixture_stats)

    def get_fixture_stats(self, fixture_id: int) -> dict[str, FixtureStats]:
        api_footbal_response = self.api_footbal_repository.get_fixture_stats(fixture_id)
        flashscore_response = self.flashscore_repository.get_fixture_stats(fixture_id)

        if not api_footbal_response.get('data', []) and not flashscore_response.get('data', []):
            raise ValueError(f'No fixture stats found for fixture {fixture_id}')

        api_footbal_fixture_stats = FixtureStats.from_dict(api_footbal_response)
        flashscore_fixture_stats = FixtureStats.from_dict(flashscore_response)

        fixture_stats = {
            self.football: api_footbal_fixture_stats,
            self.flashscore: flashscore_fixture_stats,
        }
        return fixture_stats

    def get_fixture_stats_over_season(self, team_id: int, league_id: int, season: int) -> dict[str, List[FixtureStats]]:
        fixture_ids = self.fixture_service.get_fixture_ids(team_id, league_id, season)
        api_football_fixture_stats = self._get_fixture_stats_by_fixture_ids(fixture_ids, self.api_footbal_repository)
        flashscore_fixture_stats = self._get_fixture_stats_by_fixture_ids(fixture_ids, self.flashscore_repository)
        fixture_stats = {
            self.football: api_football_fixture_stats,
            self.flashscore: flashscore_fixture_stats,
        }
        return fixture_stats

    @classmethod
    def _get_fixture_stats_by_fixture_id(cls, fixture_id, repistory) -> list[FixtureStats]:
        fixture_stats = repistory.get_fixture_stats(fixture_id)
        fixture_stats = [FixtureStats.from_dict(fixture_stat) for fixture_stat in fixture_stats]
        return fixture_stats

    @classmethod
    def _get_fixture_stats_by_fixture_ids(cls, fixture_ids, repistory) -> list[FixtureStats]:
        fixture_stats = repistory.get_team_fixture_stats(fixture_ids)
        fixture_stats = [FixtureStats.from_dict(fixture_stat) for fixture_stat in fixture_stats]
        return fixture_stats
