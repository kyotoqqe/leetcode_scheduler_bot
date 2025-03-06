from aiogram.filters import Filter
from aiogram.types import Message
import re


class LeetcodeLinkFilter(Filter):
    async def __call__(self, message: Message):
        if not message.text.startswith("https://"):
            return False

        link_details = message.text[8:].split("/")

        if len(link_details) < 3:
            return False

        domain, type_, titleSlug, *_ = link_details

        if domain != "leetcode.com":
            return False

        if type_ != "problems":
            return False

        if not re.match(r"^[a-z0-9-]+$", titleSlug):
            return False
        return True
