from unittest.mock import Mock

import pytest

from adapter.mabinogi.model.AuctionItemDto import AuctionItemDto
from src.controller.markets import get_items
from src.controller.schema.market_schema import MarketItemRequest, MarketItemResponse
from src.services.market_service import MarketService


@pytest.fixture
def mock_market_service():
    return Mock(spec=MarketService)


@pytest.fixture
def mock_market_item_request():
    return MarketItemRequest.as_param(item_name="고급 가죽")


class TestMarketsController:
    def test_get_items_success(self, mock_market_service, mock_market_item_request):
        """
        get_items 함수가 MarketService를 호출하고 MarketItemResponse를 반환하는지 테스트
        """

        # Arrange
        mock_auction_items = [
            AuctionItemDto(
                item_name="고급 가죽",
                item_display_name="고급 가죽",
                item_count=1,
                auction_price_per_unit=2000,
                date_auction_expire="2025-07-01T10:00:00.000Z",
                auction_item_category="재료",
                item_option=[]
            ),
            AuctionItemDto(
                item_name="고급 가죽",
                item_display_name="고급 가죽",
                item_count=1,
                auction_price_per_unit=3000,
                date_auction_expire="2025-07-01T11:00:00.000Z",
                auction_item_category="재료",
                item_option=[]
            ),
        ]
        mock_market_service.get_market_items.return_value = mock_auction_items

        # Act
        response = get_items(request=mock_market_item_request, service=mock_market_service)

        # Assert
        mock_market_service.get_market_items.assert_called_once_with(mock_market_item_request)
        assert isinstance(response, list)
        assert all(isinstance(item, MarketItemResponse) for item in response)
        assert len(response) == len(mock_auction_items)
        for i, item_response in enumerate(response):
            assert item_response.item_name == mock_auction_items[i].item_name
            assert item_response.item_display_name == mock_auction_items[i].item_display_name
            assert item_response.item_count == mock_auction_items[i].item_count
            assert item_response.auction_price_per_unit == mock_auction_items[i].auction_price_per_unit
            assert item_response.date_auction_expire is not None
            assert item_response.date_auction_expire_kst is not None
            assert item_response.auction_item_category == mock_auction_items[i].auction_item_category
            assert item_response.item_option == mock_auction_items[i].item_option
