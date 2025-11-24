import google.generativeai as genai
import os

from dotenv import  load_dotenv

load_dotenv()

# API Key 설정
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


class Gemini:
    def __init__(self, system_instruction):
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction=system_instruction
        )

    def extract(self, content):
        response = self.model.generate_content(content)
        return response.text

# def get_info(results):
#     genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
#
#     system_instruction = f"""당신은 디스코드 알림 메시지를 전문적으로 작성하는 봇입니다.
#
#     항상 다음 규칙을 지켜 메시지를 생성하세요.
#
#     1️⃣ 메시지 제목은 **항상 "📢 검쨩봇의 추천노기"** 로 고정합니다.
#     2️⃣ 분석표는 **디스코드에서 보기 편한 표 형식**으로 작성하며, 코드 블록 없이 작성합니다.
#     3️⃣ 표 컬럼은 항상 다음 순서와 이름을 유지합니다:
#        - 아이템
#        - 단위 시간
#        - 기대 획득 수
#        - 경매장 최저가 평균
#        - 매물 수
#        - 1시간 기대 수익률
#             4️⃣ 추천 아이템이 있다면, 해당 행에 🔥 이모지를 붙입니다.
#             5️⃣ 결론 섹션은 항상 **💡 결론** 제목으로 시작하고, 추천 아이템과 이유를 간단히 설명합니다.
#             6️⃣ 주의 사항이 있으면 ⚠️ 이모지를 사용하여 추가합니다.
#             7️⃣ 메시지 전체 톤은 친근하지만 전문적인 느낌을 유지합니다.
#
#         **출력 예시:**
#
#
#         **📢 검쨩봇의 추천노기**
#         - 아이템 획득 위치를 알려줘
#         - 단위 시간, 기대 획득 수, 최저가 평균, 매물 수 , 1시간 예상수익률을 표로 만들어줘
#
#         💡 결론
#         - 결론은 어떤 아이템은 데이터를 분석해서 어떤 아이템을 획득하는 게 좋은지 판단해준 내용을 써줘
#
#         """
#
#     model = genai.GenerativeModel(
#         "gemini-2.0-flash",
#         system_instruction=system_instruction
#     )
#
#     response = model.generate_content(results)
#     # print(response.text)
#     return response.text
