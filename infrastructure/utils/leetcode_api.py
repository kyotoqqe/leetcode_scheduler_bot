from aiohttp import ClientSession, ClientError
import logging
import re

logger = logging.getLogger(__name__)


class LeetcodeAPIError(Exception):
    """Ошибка запроса к API LeetCode"""


class ParsingError(Exception):
    """Ошибка парсинга ссылки"""


class LeetCodeAPI:
    def __init__(self, session: ClientSession):
        self.url = "https://leetcode.com/graphql/"
        self.session = session

    def link_parser(self, link: str):

        link_details = link[8:].split("/")

        if len(link_details) < 3:
            raise ParsingError("Произошла ошибка парсинга")

        domain, type_, titleSlug, *_ = link_details

        if domain != "leetcode.com":
            raise ParsingError("Передан не корректный домен")

        if type_ != "problems":
            raise ParsingError("Произошла ошибка парсинга")

        if not re.match(r"^[a-z0-9-]+$", titleSlug):
            raise ParsingError("Передана не корректная ссылка")

        return titleSlug

    async def get_problem_detail(self, link):
        headers = {
            "Content-Type": "application/json"
        }
        query = """
            query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                content
                difficulty
                }
            }
        """
        try:
            variables = {"titleSlug": self.link_parser(link)}
            async with self.session.post(url=self.url, json={"query": query, "variables": variables}, headers=headers) as session:
                response = await session.json()
                if session.status != 200:
                    raise LeetcodeAPIError(f"Ошибка API: {session.status}")
                title = response["data"]["question"]["title"]
                difficulty = response["data"]["question"]["difficulty"]
                problem_link = f"https://leetcode.com/problems/{variables['titleSlug']}/description/"
                return {"title": title, "difficulty": difficulty, "link": problem_link}
        except ClientError as e:
            logger.error(f"Произошла ошибка сети :{e}")
            raise LeetcodeAPIError(f"Произошла ошибка сети :{e}")
        except ParsingError as e:
            logger.error(f"Произошла ошибка парсинга: :{e}")
            raise ParsingError(f"Произошла ошибка парсинга: {e}")
