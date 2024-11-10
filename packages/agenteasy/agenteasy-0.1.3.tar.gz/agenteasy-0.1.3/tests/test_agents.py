import tests
import pytest
from agenteasy.agent import AIAgent
from agenteasy.models import *
from agenteasy.storage import setup_storage, StorageRedis

agent = AIAgent(GPT(model="gpt-3.5-turbo"))
aagent = AIAgent(GPT(model="gpt-3.5-turbo"), model_async=True)


def test_generate():
    content = agent.generate(
        messages=[{"role": "user", "content": "直接返回两个字：通过"}]
    )
    assert "通过" in content


def test_generate_longer():
    content = agent.generate(
        messages=[{"role": "user", "content": "你是谁？"}], max_tokens=8
    )
    assert len(content) > 10


@pytest.mark.asyncio
async def test_agenerate():
    content = await aagent.agenerate(
        messages=[{"role": "user", "content": "直接返回两个字：通过"}]
    )
    assert "通过" in content


def test_backend():
    from agenteasy.config import settings

    bk_agent = AIAgent(GPT(model="gpt-3.5-turbo"))
    setup_storage(bk_agent, StorageRedis(url=settings.REDIS_URL))
    num = bk_agent.generate(
        messages=[{"role": "user", "content": "给个30000以内的随机整数"}],
        use_backend_cache=False,
    )
    num_compare = bk_agent.generate(
        messages=[{"role": "user", "content": "给个30000以内的随机整数"}],
        use_backend_cache=False,
    )
    assert num != num_compare
    num_cache = bk_agent.generate(
        messages=[{"role": "user", "content": "给个30000以内的随机整数"}]
    )
    assert num_cache == num_compare
