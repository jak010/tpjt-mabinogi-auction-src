import json
from functools import lru_cache

import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types.generative_service import GenerateContentResponse


class GoogleLLM:

    @classmethod
    @lru_cache(maxsize=1)
    def cached_model(cls):
        return genai.GenerativeModel(
            'gemini-2.0-flash',
            # system_instruction=system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )

    @classmethod
    def execute(cls, input_content1, input_content2):
        """ DB에 저장된 채용공고에서 요구 기술스택, 요구 포지션을 추출해 저장하기 """
        genai.configure(api_key="AIzaSyAzGw5l8QTFwJqNgLgV7TBK9m1j5_wPHo8")

        content = f"입력된 두 데이터를 보고 수익성이 어떤지 비교 분석해주세요:{input_content1}, {input_content2}"

        generative_model = cls.cached_model()

        response: GenerateContentResponse = generative_model.generate_content(content)


        print(response)
