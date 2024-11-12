from buco_db_controller.models.xgoals import XGoals
from buco_db_controller.repositories.xgoals_repository import XGoalsRepository
from buco_db_controller.services.fixture_service import FixtureService


class XGoalsService:
    fbref = 'fbref'
    understat = 'understat'
    flashscore = 'flashscore'

    def __init__(self):
        self.fbref_xgoals_repository = XGoalsRepository(self.fbref)
        self.understat_xgoals_repository = XGoalsRepository(self.understat)
        self.flashscore_xgoals_repository = XGoalsRepository(self.flashscore)
        self.fixture_service = FixtureService()

    def upsert_many_fixture_xg(self, xgoals, source):
        if source == self.fbref:
            self.fbref_xgoals_repository.upsert_many_fixture_xg(xgoals)
        elif source == self.understat:
            self.understat_xgoals_repository.upsert_many_fixture_xg(xgoals)
        elif source == self.flashscore:
            self.flashscore_xgoals_repository.upsert_many_fixture_xg(xgoals)

    def get_xgoals(self, fixture_id: int) -> XGoals:
        xgoals = self.get_prioritized_xgoals([fixture_id])[0]
        return xgoals

    def get_xgoals_over_season(self, team_id: int, league_id: int, season: int, prior: bool = True) -> list[XGoals]:
        fixture_ids = self.fixture_service.get_fixture_ids(team_id, league_id, season)

        if prior:
            return self.get_prioritized_xgoals(fixture_ids)
        else:
            return self.get_average_xgoals(fixture_ids)

    def get_h2h_xgoals(self, team1_id: int, team2_id: int, league_id: int, season: int, prior: bool = True) -> list[XGoals]:
        h2h_fixture_ids = self.fixture_service.get_h2h_fixture_ids(team1_id, team2_id, league_id, season)
        if prior:
            return self.get_prioritized_xgoals(h2h_fixture_ids)
        else:
            return self.get_average_xgoals(h2h_fixture_ids)

    def get_prioritized_xgoals(self, fixture_ids: list[int]) -> list[XGoals]:
        xgoals_data = {
            self.fbref: [XGoals.from_dict(x) for x in self.fbref_xgoals_repository.get_many_xgoals(fixture_ids)],
            self.understat: [XGoals.from_dict(x) for x in self.understat_xgoals_repository.get_many_xgoals(fixture_ids)],
            self.flashscore: [XGoals.from_dict(x) for x in self.flashscore_xgoals_repository.get_many_xgoals(fixture_ids)],
        }

        prioritized_xgoals = []
        for fixture_id in fixture_ids:
            for source in [self.fbref, self.understat, self.flashscore]:
                xgoal = next((x for x in xgoals_data[source] if x.fixture_id == fixture_id), None)
                if xgoal and xgoal.ht_xg and xgoal.at_xg:
                    prioritized_xgoals.append(xgoal)
                    break

        return prioritized_xgoals

    def get_average_xgoals(self, fixture_ids: list[int]) -> list[XGoals]:
        xgoals_data = {
            self.fbref: [XGoals.from_dict(x) for x in self.fbref_xgoals_repository.get_many_xgoals(fixture_ids)],
            self.understat: [XGoals.from_dict(x) for x in self.understat_xgoals_repository.get_many_xgoals(fixture_ids)],
            self.flashscore: [XGoals.from_dict(x) for x in self.flashscore_xgoals_repository.get_many_xgoals(fixture_ids)],
        }

        averaged_xgoals = []
        for fixture_id in fixture_ids:
            home_xgs = []
            away_xgs = []
            ht = at = ht_goals = at_goals = None

            for source in xgoals_data:
                xgoal = next((x for x in xgoals_data[source] if x.fixture_id == fixture_id), None)
                if xgoal:
                    # Collecting xg values
                    if xgoal.ht_xg is not None:
                        home_xgs.append(xgoal.ht_xg)
                    if xgoal.at_xg is not None:
                        away_xgs.append(xgoal.at_xg)

                    # Collecting other data (assuming consistency across sources)
                    ht = xgoal.ht or ht
                    at = xgoal.at or at
                    ht_goals = xgoal.ht_goals if ht_goals is None else ht_goals
                    at_goals = xgoal.at_goals if at_goals is None else at_goals

            if home_xgs and away_xgs and ht and at:
                averaged_xgoal = XGoals(
                    fixture_id=fixture_id,
                    ht=ht,
                    at=at,
                    ht_xg=sum(home_xgs) / len(home_xgs),
                    at_xg=sum(away_xgs) / len(away_xgs),
                    ht_goals=ht_goals,
                    at_goals=at_goals
                )
                averaged_xgoals.append(averaged_xgoal)

        return averaged_xgoals
