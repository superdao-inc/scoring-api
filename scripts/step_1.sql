CREATE TYPE public.audiencetype AS ENUM ('AUDIENCE'
                                       , 'CLAIMED'
                                       , 'FIXED_LIST'
                                       , 'ANALYTICS');

CREATE TYPE public.blockchaintype AS ENUM ('ETHEREUM'
                                         , 'POLYGON');

CREATE TYPE public.dictionaryvaluetype AS ENUM ('INTEGER');

CREATE TYPE public.walleteventstype AS ENUM ('WALLET_CONNECT'
                                           , 'FORM_SUBMIT');

CREATE TABLE public.analytics_events_counts (
    tracker_id varchar NOT NULL
  , event_type varchar NOT NULL
  , timestamp timestamp NOT NULL
  , count integer NOT NULL
);

CREATE TABLE public.analytics_events_sources (
    tracker_id varchar NOT NULL
  , event_type varchar NOT NULL
  , source varchar NOT NULL
  , count integer NOT NULL
);

CREATE TABLE public.analytics_wallet_last_events (
    tracker_id varchar NOT NULL
  , address varchar NOT NULL
  , last_event public.walleteventstype NOT NULL
  , last_event_timestamp timestamp NOT NULL
  , source varchar
  , updated timestamp NOT NULL
);

CREATE TABLE public.claimed (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
) PARTITION BY list (claimed_contract);

CREATE TABLE public.claimed_0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x0d8775f648430679a709e98d2b0cb6250d2887ef (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x0f5d2fb29fb7d3cfee444a200298f468908cc942 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x111111111117dc0aa78b770fa6a738034120c302 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x1871464f087db27823cff66aa88599aa4815ae95 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x1a13f4ca1d028320a707d99520abfefca3998b7f (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x1f9840a85d5af5bf1d1762f925bdaddc4201f984 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x28424507fefb6f7f8e9d3860f56504e4e5f5f390 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x2b591e99afe9f32eaa6214f7b7629768c40eeb39 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x3506424f91fd33084466f402d5d97f05f8e3b4af (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x3845badade8e6dff049820680d1f14bd3903a5d0 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x4092678e4e78230f46a1534c0fbc8fa39780892b (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x4a220e6096b25eadb88358cb44068a3248254675 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x4d224452801aced8b2f0aebe155379bb5d594381 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x4dc3643dbc642b72c158e7f3d2ff232df61cb6ce (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x4e15361fd6b4bb609fa63c81a2be19d873717870 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x514910771af9ca656af840dff83e8264ecf986ca (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x60d55f02a771d515e077c9c2403a1ef324885cec (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x6982508145454ce325ddbe47a25d4ec3d2311933 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x6b175474e89094c44da98b954eedeac495271d0f (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x6b3595068778dd592e39a122f4f5a5cf09c90fe2 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x8a953cfe442c5e8855cc6c61b1293fa648bae472 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x8df3aad3a84da6b69a4da8aec3ea40d9091b2ac4 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0x92e52a1a235d9a103d970901066ce910aacefd37 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xb8c77482e45f1f44de1745f52c74426c631bdd52 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xbbbbca6a901c926f240b89eacb641d8aec7aeafd (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xc00e94cb662c3520282e6f5717214004a7f26888 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xc944e90c64b2c07662a292be6244bdf05cda44a7 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xd1d2eb1b1e90b638588728b4130137d262c87cae (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xd26114cd6ee289accf82350c8d8487fedb8a0c07 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xd533a949740bb3306d119cc777fa900ba034cd52 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xd6df932a45c0f255f85145f286ea0b292b21c90b (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xe06bd4f5aac8d0aa337d13ec88db6defc6eaeefe (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xe41d2489571d322189246dafa5ebde1f4699f498 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xe530441f4f73bdb6dc2fa5af7c3fc5fd551ec838 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xf3e014fe81267870624132ef3a646b8e83853a96 (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xf4d2888d29d722226fafa5d9b24f9164c092421e (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.claimed_default (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , blockchain public.blockchaintype NOT NULL
  , claimed_contract varchar NOT NULL
);

CREATE TABLE public.dictionary (
    key varchar NOT NULL
  , value varchar
  , value_type public.dictionaryvaluetype NOT NULL
  , updated timestamp DEFAULT now() NOT NULL
);

CREATE TABLE public.fixed_lists (
    list_id varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.input_activity_metadata (
    address varchar NOT NULL
  , chain public.blockchaintype
  , name varchar NOT NULL
  , external_url varchar NOT NULL
  , image_url varchar NOT NULL
);

CREATE TABLE public.nft_holders (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
) PARTITION BY list (contract_prefix);

CREATE TABLE public.nft_holders_0x0 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x1 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x2 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x3 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x4 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x5 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x6 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x7 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x8 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0x9 (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0xa (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0xb (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0xc (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0xd (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0xe (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.nft_holders_0xf (
    contract_prefix varchar NOT NULL
  , token_contract varchar NOT NULL
  , wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
);

CREATE TABLE public.top_collections (
    chain public.blockchaintype NOT NULL
  , audience_slug varchar NOT NULL
  , audience_type public.audiencetype NOT NULL
  , token_address varchar NOT NULL
  , nft_count integer NOT NULL
  , holders_count integer
  , total_nft_count integer
  , total_holders_count integer
  , updated timestamp NOT NULL
);

CREATE TABLE public.top_whitelisted_collections (
    chain public.blockchaintype NOT NULL
  , audience_slug varchar NOT NULL
  , audience_type public.audiencetype NOT NULL
  , token_address varchar NOT NULL
  , nft_count integer NOT NULL
  , holders_count integer
  , total_nft_count integer
  , total_holders_count integer
  , updated timestamp NOT NULL
);

CREATE TABLE public.wallet_attributes (
    wallet varchar NOT NULL
  , wallet_b bytea NOT NULL
  , created_at timestamp
  , ens_name varchar
  , email varchar
  , labels varchar[]
  , last_month_tx_count integer
  , last_month_in_volume integer
  , last_month_out_volume integer
  , last_month_volume integer
  , nfts_count integer
  , twitter_avatar_url varchar
  , twitter_followers_count integer
  , twitter_url varchar
  , twitter_username varchar
  , twitter_location varchar
  , twitter_bio varchar
  , tx_count integer
  , wallet_usd_cap bigint
  , whitelist_activity varchar[]
  , superrank integer
);

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270 FOR VALUES IN ('0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x0d8775f648430679a709e98d2b0cb6250d2887ef FOR VALUES IN ('0x0d8775f648430679a709e98d2b0cb6250d2887ef');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x0f5d2fb29fb7d3cfee444a200298f468908cc942 FOR VALUES IN ('0x0f5d2fb29fb7d3cfee444a200298f468908cc942');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x111111111117dc0aa78b770fa6a738034120c302 FOR VALUES IN ('0x111111111117dc0aa78b770fa6a738034120c302');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x1871464f087db27823cff66aa88599aa4815ae95 FOR VALUES IN ('0x1871464f087db27823cff66aa88599aa4815ae95');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x1a13f4ca1d028320a707d99520abfefca3998b7f FOR VALUES IN ('0x1a13f4ca1d028320a707d99520abfefca3998b7f');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6 FOR VALUES IN ('0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x1f9840a85d5af5bf1d1762f925bdaddc4201f984 FOR VALUES IN ('0x1f9840a85d5af5bf1d1762f925bdaddc4201f984');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x28424507fefb6f7f8e9d3860f56504e4e5f5f390 FOR VALUES IN ('0x28424507fefb6f7f8e9d3860f56504e4e5f5f390');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x2b591e99afe9f32eaa6214f7b7629768c40eeb39 FOR VALUES IN ('0x2b591e99afe9f32eaa6214f7b7629768c40eeb39');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x3506424f91fd33084466f402d5d97f05f8e3b4af FOR VALUES IN ('0x3506424f91fd33084466f402d5d97f05f8e3b4af');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x3845badade8e6dff049820680d1f14bd3903a5d0 FOR VALUES IN ('0x3845badade8e6dff049820680d1f14bd3903a5d0');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7 FOR VALUES IN ('0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x4092678e4e78230f46a1534c0fbc8fa39780892b FOR VALUES IN ('0x4092678e4e78230f46a1534c0fbc8fa39780892b');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x4a220e6096b25eadb88358cb44068a3248254675 FOR VALUES IN ('0x4a220e6096b25eadb88358cb44068a3248254675');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x4d224452801aced8b2f0aebe155379bb5d594381 FOR VALUES IN ('0x4d224452801aced8b2f0aebe155379bb5d594381');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x4dc3643dbc642b72c158e7f3d2ff232df61cb6ce FOR VALUES IN ('0x4dc3643dbc642b72c158e7f3d2ff232df61cb6ce');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x4e15361fd6b4bb609fa63c81a2be19d873717870 FOR VALUES IN ('0x4e15361fd6b4bb609fa63c81a2be19d873717870');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x514910771af9ca656af840dff83e8264ecf986ca FOR VALUES IN ('0x514910771af9ca656af840dff83e8264ecf986ca');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85 FOR VALUES IN ('0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x60d55f02a771d515e077c9c2403a1ef324885cec FOR VALUES IN ('0x60d55f02a771d515e077c9c2403a1ef324885cec');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x6982508145454ce325ddbe47a25d4ec3d2311933 FOR VALUES IN ('0x6982508145454ce325ddbe47a25d4ec3d2311933');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x6b175474e89094c44da98b954eedeac495271d0f FOR VALUES IN ('0x6b175474e89094c44da98b954eedeac495271d0f');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x6b3595068778dd592e39a122f4f5a5cf09c90fe2 FOR VALUES IN ('0x6b3595068778dd592e39a122f4f5a5cf09c90fe2');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359 FOR VALUES IN ('0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x8a953cfe442c5e8855cc6c61b1293fa648bae472 FOR VALUES IN ('0x8a953cfe442c5e8855cc6c61b1293fa648bae472');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x8df3aad3a84da6b69a4da8aec3ea40d9091b2ac4 FOR VALUES IN ('0x8df3aad3a84da6b69a4da8aec3ea40d9091b2ac4');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0x92e52a1a235d9a103d970901066ce910aacefd37 FOR VALUES IN ('0x92e52a1a235d9a103d970901066ce910aacefd37');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b FOR VALUES IN ('0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f FOR VALUES IN ('0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xb8c77482e45f1f44de1745f52c74426c631bdd52 FOR VALUES IN ('0xb8c77482e45f1f44de1745f52c74426c631bdd52');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xbbbbca6a901c926f240b89eacb641d8aec7aeafd FOR VALUES IN ('0xbbbbca6a901c926f240b89eacb641d8aec7aeafd');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xc00e94cb662c3520282e6f5717214004a7f26888 FOR VALUES IN ('0xc00e94cb662c3520282e6f5717214004a7f26888');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f FOR VALUES IN ('0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xc944e90c64b2c07662a292be6244bdf05cda44a7 FOR VALUES IN ('0xc944e90c64b2c07662a292be6244bdf05cda44a7');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xd1d2eb1b1e90b638588728b4130137d262c87cae FOR VALUES IN ('0xd1d2eb1b1e90b638588728b4130137d262c87cae');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xd26114cd6ee289accf82350c8d8487fedb8a0c07 FOR VALUES IN ('0xd26114cd6ee289accf82350c8d8487fedb8a0c07');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xd533a949740bb3306d119cc777fa900ba034cd52 FOR VALUES IN ('0xd533a949740bb3306d119cc777fa900ba034cd52');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xd6df932a45c0f255f85145f286ea0b292b21c90b FOR VALUES IN ('0xd6df932a45c0f255f85145f286ea0b292b21c90b');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xe06bd4f5aac8d0aa337d13ec88db6defc6eaeefe FOR VALUES IN ('0xe06bd4f5aac8d0aa337d13ec88db6defc6eaeefe');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xe41d2489571d322189246dafa5ebde1f4699f498 FOR VALUES IN ('0xe41d2489571d322189246dafa5ebde1f4699f498');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xe530441f4f73bdb6dc2fa5af7c3fc5fd551ec838 FOR VALUES IN ('0xe530441f4f73bdb6dc2fa5af7c3fc5fd551ec838');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xf3e014fe81267870624132ef3a646b8e83853a96 FOR VALUES IN ('0xf3e014fe81267870624132ef3a646b8e83853a96');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xf4d2888d29d722226fafa5d9b24f9164c092421e FOR VALUES IN ('0xf4d2888d29d722226fafa5d9b24f9164c092421e');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c FOR VALUES IN ('0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c');

ALTER TABLE ONLY public.claimed ATTACH PARTITION public.claimed_default DEFAULT;

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x0 FOR VALUES IN ('0x0');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x1 FOR VALUES IN ('0x1');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x2 FOR VALUES IN ('0x2');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x3 FOR VALUES IN ('0x3');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x4 FOR VALUES IN ('0x4');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x5 FOR VALUES IN ('0x5');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x6 FOR VALUES IN ('0x6');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x7 FOR VALUES IN ('0x7');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x8 FOR VALUES IN ('0x8');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0x9 FOR VALUES IN ('0x9');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0xa FOR VALUES IN ('0xa');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0xb FOR VALUES IN ('0xb');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0xc FOR VALUES IN ('0xc');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0xd FOR VALUES IN ('0xd');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0xe FOR VALUES IN ('0xe');

ALTER TABLE ONLY public.nft_holders ATTACH PARTITION public.nft_holders_0xf FOR VALUES IN ('0xf')