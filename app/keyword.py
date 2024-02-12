import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_keywords(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Please read the following text carefully, considering its language and content. "
                           "After reading, analyze the main themes, ideas, and subjects covered in the text. "
                           "Identify the five most significant and relevant keywords that encapsulate the essence "
                           "of the text, ensuring that these keywords are in the same language as the input text. "
                           "These keywords should reflect the core topics, concepts, or terms that are pivotal to "
                           "understanding the text's content. Each keyword should not exceed three words in length. "
                           "Return these keywords in a list format, limited to a maximum of five, as follows: "
                           "[\"keyword 1\", \"keyword 2\", \"keyword 3\", \"keyword 4\", \"keyword 5\"]. "
                           "Ensure that your selection of keywords is precise, concise, and accurately represents "
                           "the critical elements of the text."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    # return response.choices[0].message.content
    # -> Elasticsearch, 확장성, 검색 기능, 비정형 데이터, 최적화된 언어 기반 검색
    return [keyword.strip() for keyword in response.choices[0].message.content.split(",")]


if __name__ == "__main__":
    print(extract_keywords(
        "Elasticsearch는 확장성이 뛰어난 검색 기능입니다. 즉, 다양한 소스의 비정형 데이터 유형을 가져와서 최적화된 언어 기반 검색을 위한 특별한 형식으로 저장합니다"))
