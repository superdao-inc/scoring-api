import random

from locust import HttpUser, task, between, SequentialTaskSet, TaskSet
from app.wallet.similar_wallets_api import SimilarWalletsApi


WALLETS = [
    '0x88ba103bd36357842b2967247fd6dc188fb2ae5d',
    '0x068da7031f2ad9d4ce55587cc7fb090d52063bdd',
    '0x8dd0ade6da6278ec85523923b375b094b2dad043',
    '0x28d8997d5e9a09471a189618701eb02ffb45659d',
    '0xdaa8a78089ef0098a14af2148a8768cf7d104640',
    '0x4ee430067302e73c0e2682a615a5155f049bea98',
    '0x96036228e7ec72a65a3ec4339c804704a17de92a',
    '0xe935e618d6773570d84b7e976965b4d11a34dab4',
    '0xbd450568f6e3b49aeade221cb124bf1fb48375b7',
    '0x32d51103f89ba2fcc35998ef9875fcaae36321fe',
]

SIMILAR_WALLETS = [
    '0xcd35548d33d7f49f4cb2d08fd3e0fc7565752223',
    '0xea23c259b637f72d80697d4a4d1302df9f64530b',
    '0x641cf4f47ddfd1dac1bdee36069f09481064b031',
    '0xd3777432b700f681e5169ec51138ac888519c0ed',
    '0xef4d102aa7e014032671122979e8c473c5a62b4c',
]


CLAIMED = [
    ('0x514910771af9ca656af840dff83e8264ecf986ca', 'ETHEREUM'),
    ('0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f', 'POLYGON'),
    ('0x6b175474e89094c44da98b954eedeac495271d0f', 'ETHEREUM'),
    ('0x1871464f087db27823cff66aa88599aa4815ae95', 'POLYGON'),
    ('0xd26114cd6ee289accf82350c8d8487fedb8a0c07', 'ETHEREUM'),
    ('0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85', 'ETHEREUM'),
    ('0x0d8775f648430679a709e98d2b0cb6250d2887ef', 'ETHEREUM'),
    ('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', 'ETHEREUM'),
    ('0x0f5d2fb29fb7d3cfee444a200298f468908cc942', 'ETHEREUM'),
    ('0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270', 'POLYGON'),
]


LABEL_AUDIENCES = ['voter', 'whale', 'zombie', 'audience:defi', 'audience:culture:art']


FIXED_LIST_AUDIENCES = [
    'stargate_snapshot_voters_list',
    'superrare_snapshot_voters_list',
    'superrobots_w1_claimed_list',
    'superrobots_w2_claimed_list',
    'talent_protocol_list',
    'uniswap_snapshot_voters_list',
    'uniswap_users',
    'wallapp_list',
]


NFT_HOLDERS_CONTRACTS = [
    '0xdac17f958d2ee523a2206206994597c13d831ec7',
    '0x8ef7e72eaaab6b95112ea036f9b77083846c28f8',
    '0x2055244a719229d669488e389388f2d653a452f4',
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
    '0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce',
    '0x5d666f215a85b87cb042d59662a7ecd2c8cc44e6',
    '0xc2132d05d31c914a87c6611c10748aeb04b58e8f',
    '0x7ceb23fd6bc0add59e62ac25578270cff1b9f619',
    '0x963ea907e0c53ce98a0fd9765ee9682ee9c2a69f',
    '0xc0098d41e50f721f9026112ee1ad986d2fce9be6',
]


ORDERABLE_COLUMNS = ['superrank', 'created_at', 'wallet_usd_cap', 'nfts_count', 'twitter_followers_count']


LEADERBOARD_TABS = ['superrank', 'wallet_usd_cap', 'tx_count', 'twitter_followers_count']


async def mocked_get_index_similar_wallets(self, address: str, n = 5):
    return SIMILAR_WALLETS


SimilarWalletsApi.get_index_similar_wallets = mocked_get_index_similar_wallets


def task_factory(path, name):
    def _locust(locust):
        locust.client.get(path, name=name)
    return _locust


# analytics
@task
def get_events_stats_task(self):
    self.client.get(
        '/v1/analytics/63584b6b-ed36-465b-ad0f-0ab3235d6bff/events_stats',
        name='/v1/analytics/[tracker_id]/events_stats'
    )


# wallet
@task
def get_wallet_attributes_task(self):
    wallet = random.choice(WALLETS)
    self.client.get(
        f'/v1/wallet/attributes/{wallet}',
        name='/v1/wallet/attributes/[wallet]',
    )


@task
def get_wallet_similar_wallets_task(self):
    wallet = random.choice(WALLETS)
    self.client.get(
        f'/v1/wallet/similar/{wallet}',
        name='/v1/wallet/similar/[wallet]',
    )


# leaderboard
leaderboard_tasks = []
for column in LEADERBOARD_TABS:
    for direction in ['ASC', 'DESC']:
        leaderboard_tasks.append(
            task_factory(
                path=f'/v1/wallet/leaderboard?order_by_field={column}&order_by_direction={direction}&limit=20',
                name=f'/v1/wallet/leaderboard {column} {direction}'
            )
        )


# claimed
# label audience
# nft holders
# fixed_list
claimed_tasks = []
audience_tasks = []
nft_holders_tasks = []
fixed_lists_tasks = []
for column in ORDERABLE_COLUMNS:
    for direction in ['ASC', 'DESC']:
        query_params = f'order_by_field={column}&order_by_direction={direction}&limit=20'
        claimed_contract, blockchain = random.choice(CLAIMED)
        claimed_tasks.append(
            task_factory(
                path=f'/v2/claimed/{claimed_contract}/{blockchain}?{query_params}',
                name=f'/v2/claimed/[claimed_contract] {column} {direction}'
            )
        )

        audience_tasks.append(
            task_factory(
                path=f'/v2/audience/{random.choice(LABEL_AUDIENCES)}?{query_params}',
                name=f'/v2/audience/[audience] {column} {direction}'
            )
        )

        nft_holders_tasks.append(
            task_factory(
                path=f'/v1/nft_holders/{random.choice(NFT_HOLDERS_CONTRACTS)}?{query_params}',
                name=f'/v1/nft_holders/[contract] {column} {direction}'
            )
        )

        fixed_lists_tasks.append(
            task_factory(
                path=f'/v2/fixed_list/{random.choice(FIXED_LIST_AUDIENCES)}?{query_params}',
                name=f'/v2/fixed_list/[column] {column} {direction}'
            )
        )


 # top colletions
top_collections_tasks = []
top_collections_mapping = {
    'audience': LABEL_AUDIENCES,
    'fixed_list': FIXED_LIST_AUDIENCES,
    'claimed': CLAIMED,
}
for audience_type, audiences in top_collections_mapping.items():
    audience_id = random.choice(audiences)
    for use_whilisted in ['true', 'false']:
        top_collections_tasks.append(
            task_factory(
                path=f'/v1/top-collections/?audience_id={audience_id}&audience_type={audience_type}&top_n=10&use_whitelisted_activities={use_whilisted}',
                name='/v1/top-collections/ {audience_type} ' + ('whitelisted' if use_whilisted == 'true' else 'not whitelisted')
            )
        )


class SeparateTasks(SequentialTaskSet):
    tasks = [
        # get_events_stats_task,
        # get_wallet_attributes_task,
        # get_wallet_similar_wallets_task,
        # *leaderboard_tasks,
        # *claimed_tasks,
        # *audience_tasks,
        *nft_holders_tasks,
        # *fixed_lists_tasks,
    ]


class RandomTasks(TaskSet):
    tasks = [
        # get_events_stats_task,
        # get_wallet_attributes_task,
        # get_wallet_similar_wallets_task,
        # *leaderboard_tasks,
        # *claimed_tasks,
        # *audience_tasks,
        *nft_holders_tasks,
        # *fixed_lists_tasks,
    ]


class AllTasks(SequentialTaskSet):
    tasks = [
        # get_events_stats_task,
        # get_wallet_attributes_task,
        # get_wallet_similar_wallets_task,
        # *leaderboard_tasks,
        # *claimed_tasks,
        # *audience_tasks,
        *nft_holders_tasks,
        # *fixed_lists_tasks,  
    ]


class MainTaskSet(TaskSet):
    @task
    def separate_tasks(self):
        self.schedule_task(SeparateTasks)

    @task
    def random_tasks(self):
        self.schedule_task(RandomTasks)

    @task
    def all_tasks(self):
        self.schedule_task(AllTasks)


class ApiUser(HttpUser):
    tasks = [MainTaskSet]

    wait_time = between(1, 2)
