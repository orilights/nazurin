from time import time

from nazurin.database import Database
from nazurin.models import Illust

from .api import Kemono
from .config import COLLECTION

patterns = [
    # https://kemono.party/fanbox/user/12345/post/12345
    # https://kemono.party/patreon/user/12345/post/12345
    # https://kemono.party/fantia/user/12345/post/12345
    # https://kemono.party/boosty/user/abcdef/post/a1b2c3-d4e5f6-7890
    # https://kemono.party/dlsite/user/RG12345/post/RE12345
    # https://kemono.party/gumroad/user/12345/post/aBc1d2
    # https://kemono.su/subscribestar/user/abcdef/post/12345
    # https://kemono.su/fanbox/user/12345/post/12345/revision/12345
    r"kemono\.(?:party|su)/(\w+)/user/([\w-]+)/post/([\w-]+)(?:/revision/(\d+))?"
]


async def handle(match) -> Illust:
    service = match.group(1)
    user_id = match.group(2)
    post_id = match.group(3)
    revision_id = match.group(4)
    db = Database().driver()
    collection = db.collection(COLLECTION)

    illust = await Kemono().fetch(service, user_id, post_id, revision_id)
    illust.metadata["collected_at"] = time()
    identifier = filter(lambda x: x, [service, user_id, post_id, revision_id])
    await collection.insert("_".join(identifier), illust.metadata)
    return illust
