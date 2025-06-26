from typing import List

from src.controller.schema.market_schema import ItemStatisticResponse


class RecommendationService:
    def generate_recommendation_text(
            self,
            all_item_stats: List[ItemStatisticResponse],
    ) -> str:
        """
        아이템 통계를 기반으로 추천 텍스트를 생성합니다.
        """
        recommendation_text = '추천을 생성할 충분한 데이터가 없습니다.'
        profitable_items = [item for item in all_item_stats if item.profit_per_hour > 0]

        if profitable_items:
            profitable_items.sort(key=lambda x: x.profit_per_hour, reverse=True)
            recommendation_parts = [
                f'{item.item_name} (시간당 예상 수익: {item.profit_per_hour} 골드)'
                for item in profitable_items
            ]
            recommendation_text = (
                    '시간당 예상 수익을 고려할 때, 다음 아이템을 획득하는 것이 유리할 수 있습니다: '
                    + ', '.join(recommendation_parts)
            )
        return recommendation_text
