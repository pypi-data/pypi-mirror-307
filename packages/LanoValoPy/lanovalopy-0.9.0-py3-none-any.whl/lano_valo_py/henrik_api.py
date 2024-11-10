from typing import List, Optional
from urllib.parse import quote

from .based_api import BasedApi
from .valo_types.valo_enums import (
    AccountVersion,
    FeaturedItemsVersion,
    LeaderboardVersions,
    MMRVersions,
)
from .valo_types.valo_models import (
    AccountFetchByPUUIDOptionsModel,
    AccountFetchOptionsModel,
    FetchOptionsModel,
    GetContentFetchOptionsModel,
    GetCrosshairFetchOptionsModel,
    GetEsportsMatchesFetchOptionsModel,
    GetFeaturedItemsFetchOptionsModel,
    GetLeaderboardOptionsModel,
    GetLifetimeMMRHistoryFetchOptionsModel,
    GetMatchesByPUUIDFetchOptionsModel,
    GetMatchesFetchOptionsModel,
    GetMatchFetchOptionsModel,
    GetMMRByPUUIDFetchOptionsModel,
    GetMMRFetchOptionsModel,
    GetMMRHistoryByPUUIDFetchOptionsModel,
    GetMMRHistoryFetchOptionsModel,
    GetMMRStoredHistoryByPUUIDResponseModel,
    GetMMRStoredHistoryOptionsModel,
    GetPremierTeamFetchOptionsModel,
    GetRawFetchOptionsModel,
    GetStatusFetchOptionsModel,
    GetStoreOffersFetchOptionsModel,
    GetVersionFetchOptionsModel,
    GetWebsiteFetchOptionsModel,
)
from .valo_types.valo_responses import (
    AccountResponseModelV1,
    AccountResponseModelV2,
    APIResponseModel,
    BinaryData,
    BuildGameInfoResponseModel,
    BundleResponseModelV2,
    CommunityNewsResponseModel,
    ContentResponseModel,
    EsportMatchDataResponseModel,
    FeaturedBundleResponseModelV1,
    LeaderboardDataResponseModelV2,
    LeaderboardDataResponseModelV3,
    MatchResponseModel,
    MMRHistoryByPuuidResponseModelV1,
    MMRResponseModel,
    PremierLeagueMatchesWrapperResponseModel,
    PremierTeamResponseModel,
    StatusDataResponseModel,
    StoreOffersResponseModelV1,
    StoreOffersResponseModelV2,
    V1StoredMmrHistoryResponse,
)


class HenrikAPI(BasedApi):
    BASE_URL = "https://api.henrikdev.xyz/valorant"

    def __init__(self, token: Optional[str] = None):
        """Initialize the client.

        Args:
            token (str, optional): The token to use for requests. Defaults to None.
        """
        self.token = token
        self.headers = {"User-Agent": "unofficial-valorant-api/python/1.0"}
        if self.token:
            self.headers["Authorization"] = self.token

    async def get_account(
        self, options: AccountFetchOptionsModel
    ) -> AccountResponseModelV1 | AccountResponseModelV2:
        """
        Gets the account information for a given name and tag.

        Args:
            options (AccountFetchOptionsModel): The options for the request.

        Returns:
            AccountResponseModelV1 | AccountResponseModelV2: The account information.
        """
        self._validate(options.model_dump())
        query = self._query({"force": options.force})
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/{options.version.name}/account/{encoded_name}/{encoded_tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match options.version:
            case AccountVersion.v1:
                return AccountResponseModelV1(**result.data)
            case AccountVersion.v2:
                return AccountResponseModelV2(**result.data)
            case _:
                raise ValueError("Invalid version")

    async def get_account_by_puuid(
        self, options: AccountFetchByPUUIDOptionsModel
    ) -> AccountResponseModelV1:
        """
        Gets the account information for a given puuid.

        Args:
            options (AccountFetchByPUUIDOptionsModel): The options for the request.

        Returns:
            AccountResponseModelV1: The account information.
        """
        self._validate(options.model_dump())
        query = self._query({"force": options.force})
        url = f"{self.BASE_URL}/v1/by-puuid/account/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return AccountResponseModelV1(**result.data)

    async def get_mmr_by_puuid(
        self, options: GetMMRByPUUIDFetchOptionsModel
    ) -> MMRResponseModel:
        """
        Gets the MMR information for a given puuid.

        Args:
            options (GetMMRByPUUIDFetchOptionsModel): The options for the request.

        Returns:
            MMRResponseModel: The MMR information.
        """
        self._validate(options.model_dump())
        query = self._query({"filter": options.filter})
        encoded_region = quote(options.region)
        encoded_version = quote(options.version)
        url = f"{self.BASE_URL}/{encoded_version}/by-puuid/mmr/{encoded_region}/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MMRResponseModel(**result.data)

    async def get_mmr_history_by_puuid(
        self, options: GetMMRHistoryByPUUIDFetchOptionsModel
    ) -> MMRHistoryByPuuidResponseModelV1:
        """
        Gets the MMR history for a given puuid.

        Args:
            options (GetMMRHistoryByPUUIDFetchOptionsModel): The options for the request.

        Returns:
            MMRHistoryByPuuidResponseModelV1: The MMR history.
        """
        self._validate(options.model_dump())
        url = (
            f"{self.BASE_URL}/v1/by-puuid/mmr-history/{options.region}/{options.puuid}"
        )
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MMRHistoryByPuuidResponseModelV1(**result.data)

    async def get_matches_by_puuid(
        self, options: GetMatchesByPUUIDFetchOptionsModel
    ) -> List[MatchResponseModel]:
        self._validate(options.model_dump())
        query = self._query(
            {"filter": options.filter, "map": options.map, "size": options.size}
        )
        url = f"{self.BASE_URL}/v3/by-puuid/matches/{options.region}/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return [MatchResponseModel(**match) for match in result.data]

    async def get_content(
        self, options: GetContentFetchOptionsModel
    ) -> ContentResponseModel:
        """
        Gets the content for the given locale. This endpoints returns basic contant data like season id's or skins.
        If you need more data, please refer to https://valorant-api.com which also has image data

        Args:
            options (GetContentFetchOptionsModel): The options for the request.

        Returns:
            ContentResponseModel: The content.
        """
        query = self._query({"locale": quote(options.locale)})
        url = f"{self.BASE_URL}/v1/content"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return ContentResponseModel(**result.data)

    async def get_leaderboard(
        self, options: GetLeaderboardOptionsModel
    ) -> LeaderboardDataResponseModelV3 | LeaderboardDataResponseModelV2:
        """
        Gets the leaderboard for the given options.

        Args:
            options (GetLeaderboardOptionsModel): The options for the request.

        Returns:
            LeaderboardDataResponseModelV3 | LeaderboardDataResponseModelV2: The leaderboard data.
        """
        if options.name and options.tag and options.puuid:
            raise ValueError(
                "Too many parameters: You can't search for name/tag and puuid at the same time, please decide between name/tag and puuid"
            )
        self._validate({"version": options.version, "region": options.region})
        query = self._query(
            {
                "start": options.start,
                "end": options.end,
                "name": options.name,
                "tag": options.tag,
                "puuid": options.puuid,
                "season": options.season,
            }
        )

        encoded_region = quote(options.region)
        encoded_version = quote(options.version)

        url = f"{self.BASE_URL}/{encoded_version}/leaderboard/{encoded_region}"
        if query:
            url += f"?{query}"

        if encoded_version == LeaderboardVersions.v3:
            url += "/pc"

        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match encoded_version:
            case LeaderboardVersions.v3:
                return LeaderboardDataResponseModelV3(**result.data)
            case LeaderboardVersions.v2:
                return LeaderboardDataResponseModelV2(**result.data)
            case _:
                raise ValueError(f"Invalid version: {encoded_version}")

    async def get_matches(
        self, options: GetMatchesFetchOptionsModel
    ) -> List[MatchResponseModel]:
        self._validate(options.model_dump())
        query = self._query(
            {"filter": options.filter, "map": options.map, "size": options.size}
        )
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        encoded_region = quote(options.region)

        url = (
            f"{self.BASE_URL}/v3/matches/{encoded_region}/{encoded_name}/{encoded_tag}"
        )
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return [MatchResponseModel(**match) for match in result.data]

    async def get_match(self, options: GetMatchFetchOptionsModel) -> MatchResponseModel:
        """
        Gets the match data for the given match id.

        Args:
            options (GetMatchFetchOptionsModel): The options for the request.

        Returns:
            MatchResponseModel: The match data.
        """
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v2/match/{options.match_id}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MatchResponseModel(**result.data)

    async def get_mmr_history(
        self, options: GetMMRHistoryFetchOptionsModel
    ) -> MMRResponseModel:
        """
        Returns the latest competitive games with RR movement for each game

        Args:
            options (GetMMRHistoryFetchOptionsModel): The options for the request.

        Returns:
            MMRResponseModel: The MMR history.
        """
        self._validate(options.model_dump())
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        encoded_region = quote(options.region)
        url = f"{self.BASE_URL}/v1/mmr-history/{encoded_region}/{encoded_name}/{encoded_tag}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MMRResponseModel(**result.data)

    async def get_lifetime_mmr_history(
        self, options: GetLifetimeMMRHistoryFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query({"page": options.page, "size": options.size})
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/v1/lifetime/mmr-history/{options.region}/{encoded_name}/{encoded_tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_mmr(self, options: GetMMRFetchOptionsModel) -> MMRResponseModel:
        """
        Gets the MMR information for a given name and tag.

        Args:
            options (GetMMRFetchOptionsModel): The options for the request.

        Returns:
            MMRResponseModel: The MMR information.
        """
        self._validate(options.model_dump())
        query = self._query({"filter": options.filter})
        encoded_region = quote(options.region)
        encoded_version = quote(options.version)
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/{encoded_version}/mmr/{encoded_region}/{encoded_name}/{encoded_tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MMRResponseModel(**result.data)

    async def get_raw_data(self, options: GetRawFetchOptionsModel) -> APIResponseModel:
        """
        Make direct requests to the riot server and get the response without additional parsing from us

        Args:
            options (GetRawFetchOptionsModel): The options for the request.

        Returns:
            errors (APIResponseModel): The response from the server.
        """
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v1/raw"
        fetch_options = FetchOptionsModel(
            url=url, type="POST", body=options.model_dump()
        )
        return await self._fetch(fetch_options)

    async def get_status(
        self, options: GetStatusFetchOptionsModel
    ) -> StatusDataResponseModel:
        """
        Gets the status server for the given region.

        Args:
            options (GetStatusFetchOptionsModel): The options for the request.

        Returns:
            StatusDataResponseModel: The status server for the given region.
        """
        self._validate(options.model_dump())
        encoded_region = quote(options.region)
        url = f"{self.BASE_URL}/v1/status/{encoded_region}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return StatusDataResponseModel(**result.data)

    async def get_featured_items(
        self, options: GetFeaturedItemsFetchOptionsModel
    ) -> FeaturedBundleResponseModelV1 | List[BundleResponseModelV2] | APIResponseModel:
        self._validate(options.model_dump())
        encoded_version = quote(options.version)
        url = f"{self.BASE_URL}/{encoded_version}/store-featured"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match encoded_version:
            case FeaturedItemsVersion.v1:
                return FeaturedBundleResponseModelV1(**result.data)
            case FeaturedItemsVersion.v2:
                return [BundleResponseModelV2(**x) for x in result.data]
            case _:
                raise ValueError(f"Invalid version: {encoded_version}")

        return await self._fetch(fetch_options)

    async def get_offers(
        self, options: GetStoreOffersFetchOptionsModel
    ) -> StoreOffersResponseModelV1 | StoreOffersResponseModelV2:
        """
        Gets the store offers.

        Args:
            options (GetStoreOffersFetchOptionsModel): The options for the request.

        Returns:
            StoreOffersResponseModelV1: The store offers.

        Raises:
            ValueError: If the version is invalid.
        """
        self._validate(options.model_dump())
        encoded_version = quote(options.version)
        url = f"{self.BASE_URL}/{encoded_version}/store-offers"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match encoded_version:
            case FeaturedItemsVersion.v1:
                return StoreOffersResponseModelV1(**result.data)
            case FeaturedItemsVersion.v2:
                return [StoreOffersResponseModelV2(**x) for x in result.data]
            case _:
                raise ValueError(f"Invalid version: {encoded_version}")

    async def get_version(
        self, options: GetVersionFetchOptionsModel
    ) -> BuildGameInfoResponseModel:
        """
        Gets the current build version and branch for a given region.

        Args:
            options (GetVersionFetchOptionsModel): The options for the request.

        Returns:
            BuildGameInfoResponseModel: The current build version and branch.
        """
        self._validate(options.model_dump())
        encoded_region = quote(options.region)
        url = f"{self.BASE_URL}/v1/version/{encoded_region}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return BuildGameInfoResponseModel(**result.data)

    async def get_website(
        self, options: GetWebsiteFetchOptionsModel
    ) -> List[CommunityNewsResponseModel]:
        """
        Gets the community news for a given country code and filter.

        Args:
            options (GetWebsiteFetchOptionsModel): The options for the request.

        Returns:
            List[CommunityNewsResponseModel]: The community news.
        """
        self._validate({"country_code": options.country_code})
        query = self._query({"filter": options.filter})
        encoded_country_code = quote(options.country_code)
        url = f"{self.BASE_URL}/v1/website/{encoded_country_code}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return [CommunityNewsResponseModel(**x) for x in result.data]

    async def get_crosshair(self, options: GetCrosshairFetchOptionsModel) -> BinaryData:
        """
        Gets a crosshair image as a binary response.

        Args:
            options (GetCrosshairFetchOptionsModel): The options for the request.

        Returns:
            BinaryData: The binary response from the server. This binary response is a PNG image.
        """
        self._validate(options.model_dump())
        query = self._query({"id": options.code, "size": options.size})
        url = f"{self.BASE_URL}/v1/crosshair/generate"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url, rtype="arraybuffer")
        return await self._fetch(fetch_options)

    async def get_esports_matches(
        self, options: GetEsportsMatchesFetchOptionsModel
    ) -> List[EsportMatchDataResponseModel]:
        """
        Gets the current esports matches.

        Returns:
            List[EsportsMatchResponseModel]: The current esports matches.
        """
        query = self._query(
            {
                "region": options.region.name if options.region else None,
                "league": options.league.name if options.league else None,
            }
        )
        url = f"{self.BASE_URL}/v1/esports/schedule"

        if query:
            url += f"?{query}"

        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return [EsportMatchDataResponseModel(**x) for x in result.data]

    async def get_premier_team(
        self, options: GetPremierTeamFetchOptionsModel
    ) -> PremierTeamResponseModel:
        """
        Gets the premier team.

        Args:
            options (GetPremierTeamFetchOptionsModel): The options for the request.

        Returns:
            PremierTeamResponseModel: The premier team.
        """
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v1/premier/{options.team_name}/{options.team_tag}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return PremierTeamResponseModel(**result.data)

    async def get_premier_team_history(
        self, options: GetPremierTeamFetchOptionsModel
    ) -> PremierLeagueMatchesWrapperResponseModel:
        """
        Gets the premier team history.

        Args:
            options (GetPremierTeamFetchOptionsModel): The options for the request.

        Returns:
            PremierLeagueMatchesWrapperResponseModel: The premier team history.
        """
        self._validate(options.model_dump())
        url = (
            f"{self.BASE_URL}/v1/premier/{options.team_name}/{options.team_tag}/history"
        )
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return PremierLeagueMatchesWrapperResponseModel(**result.data)

    async def get_premier_team_by_id(self, team_id: str) -> PremierTeamResponseModel:
        """
        Gets the premier team.

        Args:
            options (GetPremierTeamFetchOptionsModel): The options for the request.

        Returns:
            PremierTeamResponseModel: The premier team.
        """
        self._validate({"team_id": team_id})
        url = f"{self.BASE_URL}/v1/premier/{team_id}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return PremierTeamResponseModel(**result.data)

    async def get_premier_team_history_by_id(
        self, team_id: str
    ) -> PremierLeagueMatchesWrapperResponseModel:
        """
        Gets the premier team history.

        Args:
            options (GetPremierTeamFetchOptionsModel): The options for the request.

        Returns:
            PremierLeagueMatchesWrapperResponseModel: The premier team history.
        """
        self._validate({"team_id": team_id})
        url = f"{self.BASE_URL}/v1/premier/{team_id}/history"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return PremierLeagueMatchesWrapperResponseModel(**result.data)

    async def get_stored_mmr_history(
        self, options: GetMMRStoredHistoryOptionsModel
    ) -> List[V1StoredMmrHistoryResponse]:
        self._validate(options.model_dump())

        if options.version is MMRVersions.v1:
            url = f"{self.BASE_URL}/{options.version.value}/stored-mmr-history/{options.region.value}/{options.name}/{options.tag}"
        else:
            url = f"{self.BASE_URL}/{options.version.value}/stored-mmr-history/{options.region.value}/{options.platform}/{options.name}/{options.tag}"

        url = f"{self.BASE_URL}/{options.version.value}/stored-mmr-history/{options.region.value}/{options.name}/{options.tag}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match options.version:
            case MMRVersions.v1:
                return [V1StoredMmrHistoryResponse(**x) for x in result.data]
            case MMRVersions.v2:
                return [V1StoredMmrHistoryResponse(**x) for x in result.data]
            case _:
                raise ValueError("Invalid version")

        return V1StoredMmrHistoryResponse(**result.data)

    async def get_stored_mmr_history_by_puuid(
        self, options: GetMMRStoredHistoryByPUUIDResponseModel
    ) -> List[V1StoredMmrHistoryResponse]:
        self._validate(options.model_dump())

        if options.version is MMRVersions.v1:
            url = f"{self.BASE_URL}/{options.version.value}/by-puuid/stored-mmr-history/{options.region.value}/{options.puuid}"
        else:
            url = f"{self.BASE_URL}/{options.version.value}/by-puuid/stored-mmr-history/{options.region.value}/{options.platform}/{options.puuid}"

        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match options.version:
            case MMRVersions.v1:
                return [V1StoredMmrHistoryResponse(**x) for x in result.data]
            case MMRVersions.v2:
                return [V1StoredMmrHistoryResponse(**x) for x in result.data]
            case _:
                raise ValueError("Invalid version")

        return V1StoredMmrHistoryResponse(**result.data)
