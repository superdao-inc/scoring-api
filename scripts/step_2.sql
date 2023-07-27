ALTER TABLE ONLY public.analytics_events_counts ADD CONSTRAINT analytics_events_counts_pkey PRIMARY KEY (tracker_id, event_type, timestamp);

ALTER TABLE ONLY public.analytics_events_sources ADD CONSTRAINT analytics_events_sources_pkey PRIMARY KEY (tracker_id, event_type, source);

ALTER TABLE ONLY public.analytics_wallet_last_events ADD CONSTRAINT analytics_wallet_last_events_pkey PRIMARY KEY (tracker_id, address);

ALTER TABLE ONLY public.claimed ADD CONSTRAINT claimed_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270 ADD CONSTRAINT claimed_0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x0d8775f648430679a709e98d2b0cb6250d2887ef ADD CONSTRAINT claimed_0x0d8775f648430679a709e98d2b0cb6250d2887ef_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x0f5d2fb29fb7d3cfee444a200298f468908cc942 ADD CONSTRAINT claimed_0x0f5d2fb29fb7d3cfee444a200298f468908cc942_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x111111111117dc0aa78b770fa6a738034120c302 ADD CONSTRAINT claimed_0x111111111117dc0aa78b770fa6a738034120c302_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x1871464f087db27823cff66aa88599aa4815ae95 ADD CONSTRAINT claimed_0x1871464f087db27823cff66aa88599aa4815ae95_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x1a13f4ca1d028320a707d99520abfefca3998b7f ADD CONSTRAINT claimed_0x1a13f4ca1d028320a707d99520abfefca3998b7f_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6 ADD CONSTRAINT claimed_0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x1f9840a85d5af5bf1d1762f925bdaddc4201f984 ADD CONSTRAINT claimed_0x1f9840a85d5af5bf1d1762f925bdaddc4201f984_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x28424507fefb6f7f8e9d3860f56504e4e5f5f390 ADD CONSTRAINT claimed_0x28424507fefb6f7f8e9d3860f56504e4e5f5f390_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x2b591e99afe9f32eaa6214f7b7629768c40eeb39 ADD CONSTRAINT claimed_0x2b591e99afe9f32eaa6214f7b7629768c40eeb39_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x3506424f91fd33084466f402d5d97f05f8e3b4af ADD CONSTRAINT claimed_0x3506424f91fd33084466f402d5d97f05f8e3b4af_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x3845badade8e6dff049820680d1f14bd3903a5d0 ADD CONSTRAINT claimed_0x3845badade8e6dff049820680d1f14bd3903a5d0_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7 ADD CONSTRAINT claimed_0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x4092678e4e78230f46a1534c0fbc8fa39780892b ADD CONSTRAINT claimed_0x4092678e4e78230f46a1534c0fbc8fa39780892b_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x4a220e6096b25eadb88358cb44068a3248254675 ADD CONSTRAINT claimed_0x4a220e6096b25eadb88358cb44068a3248254675_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x4d224452801aced8b2f0aebe155379bb5d594381 ADD CONSTRAINT claimed_0x4d224452801aced8b2f0aebe155379bb5d594381_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x4dc3643dbc642b72c158e7f3d2ff232df61cb6ce ADD CONSTRAINT claimed_0x4dc3643dbc642b72c158e7f3d2ff232df61cb6ce_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x4e15361fd6b4bb609fa63c81a2be19d873717870 ADD CONSTRAINT claimed_0x4e15361fd6b4bb609fa63c81a2be19d873717870_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x514910771af9ca656af840dff83e8264ecf986ca ADD CONSTRAINT claimed_0x514910771af9ca656af840dff83e8264ecf986ca_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85 ADD CONSTRAINT claimed_0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x60d55f02a771d515e077c9c2403a1ef324885cec ADD CONSTRAINT claimed_0x60d55f02a771d515e077c9c2403a1ef324885cec_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x6982508145454ce325ddbe47a25d4ec3d2311933 ADD CONSTRAINT claimed_0x6982508145454ce325ddbe47a25d4ec3d2311933_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x6b175474e89094c44da98b954eedeac495271d0f ADD CONSTRAINT claimed_0x6b175474e89094c44da98b954eedeac495271d0f_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x6b3595068778dd592e39a122f4f5a5cf09c90fe2 ADD CONSTRAINT claimed_0x6b3595068778dd592e39a122f4f5a5cf09c90fe2_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359 ADD CONSTRAINT claimed_0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x8a953cfe442c5e8855cc6c61b1293fa648bae472 ADD CONSTRAINT claimed_0x8a953cfe442c5e8855cc6c61b1293fa648bae472_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x8df3aad3a84da6b69a4da8aec3ea40d9091b2ac4 ADD CONSTRAINT claimed_0x8df3aad3a84da6b69a4da8aec3ea40d9091b2ac4_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0x92e52a1a235d9a103d970901066ce910aacefd37 ADD CONSTRAINT claimed_0x92e52a1a235d9a103d970901066ce910aacefd37_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b ADD CONSTRAINT claimed_0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f ADD CONSTRAINT claimed_0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xb8c77482e45f1f44de1745f52c74426c631bdd52 ADD CONSTRAINT claimed_0xb8c77482e45f1f44de1745f52c74426c631bdd52_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xbbbbca6a901c926f240b89eacb641d8aec7aeafd ADD CONSTRAINT claimed_0xbbbbca6a901c926f240b89eacb641d8aec7aeafd_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xc00e94cb662c3520282e6f5717214004a7f26888 ADD CONSTRAINT claimed_0xc00e94cb662c3520282e6f5717214004a7f26888_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f ADD CONSTRAINT claimed_0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xc944e90c64b2c07662a292be6244bdf05cda44a7 ADD CONSTRAINT claimed_0xc944e90c64b2c07662a292be6244bdf05cda44a7_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xd1d2eb1b1e90b638588728b4130137d262c87cae ADD CONSTRAINT claimed_0xd1d2eb1b1e90b638588728b4130137d262c87cae_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xd26114cd6ee289accf82350c8d8487fedb8a0c07 ADD CONSTRAINT claimed_0xd26114cd6ee289accf82350c8d8487fedb8a0c07_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xd533a949740bb3306d119cc777fa900ba034cd52 ADD CONSTRAINT claimed_0xd533a949740bb3306d119cc777fa900ba034cd52_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xd6df932a45c0f255f85145f286ea0b292b21c90b ADD CONSTRAINT claimed_0xd6df932a45c0f255f85145f286ea0b292b21c90b_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xe06bd4f5aac8d0aa337d13ec88db6defc6eaeefe ADD CONSTRAINT claimed_0xe06bd4f5aac8d0aa337d13ec88db6defc6eaeefe_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xe41d2489571d322189246dafa5ebde1f4699f498 ADD CONSTRAINT claimed_0xe41d2489571d322189246dafa5ebde1f4699f498_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xe530441f4f73bdb6dc2fa5af7c3fc5fd551ec838 ADD CONSTRAINT claimed_0xe530441f4f73bdb6dc2fa5af7c3fc5fd551ec838_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xf3e014fe81267870624132ef3a646b8e83853a96 ADD CONSTRAINT claimed_0xf3e014fe81267870624132ef3a646b8e83853a96_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xf4d2888d29d722226fafa5d9b24f9164c092421e ADD CONSTRAINT claimed_0xf4d2888d29d722226fafa5d9b24f9164c092421e_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c ADD CONSTRAINT claimed_0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.claimed_default ADD CONSTRAINT claimed_default_pkey PRIMARY KEY (claimed_contract, wallet_b, blockchain);

ALTER TABLE ONLY public.dictionary ADD CONSTRAINT dictionary_pkey PRIMARY KEY (key);

ALTER TABLE ONLY public.fixed_lists ADD CONSTRAINT fixed_lists_pkey PRIMARY KEY (list_id, wallet, wallet_b);

ALTER TABLE ONLY public.fixed_lists ADD CONSTRAINT fixed_lists_wallet_list_id_key UNIQUE (wallet, list_id);

ALTER TABLE ONLY public.input_activity_metadata ADD CONSTRAINT input_activity_metadata_pkey PRIMARY KEY (address);

ALTER TABLE ONLY public.nft_holders ADD CONSTRAINT nft_holders_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x0 ADD CONSTRAINT nft_holders_0x0_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x1 ADD CONSTRAINT nft_holders_0x1_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x2 ADD CONSTRAINT nft_holders_0x2_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x3 ADD CONSTRAINT nft_holders_0x3_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x4 ADD CONSTRAINT nft_holders_0x4_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x5 ADD CONSTRAINT nft_holders_0x5_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x6 ADD CONSTRAINT nft_holders_0x6_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x7 ADD CONSTRAINT nft_holders_0x7_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x8 ADD CONSTRAINT nft_holders_0x8_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0x9 ADD CONSTRAINT nft_holders_0x9_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0xa ADD CONSTRAINT nft_holders_0xa_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0xb ADD CONSTRAINT nft_holders_0xb_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0xc ADD CONSTRAINT nft_holders_0xc_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0xd ADD CONSTRAINT nft_holders_0xd_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0xe ADD CONSTRAINT nft_holders_0xe_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.nft_holders_0xf ADD CONSTRAINT nft_holders_0xf_pkey PRIMARY KEY (contract_prefix, token_contract, wallet_b);

ALTER TABLE ONLY public.top_collections ADD CONSTRAINT top_collections_chain_audience_slug_audience_type_token_add_key PRIMARY KEY (chain, audience_slug, audience_type, token_address);

ALTER TABLE ONLY public.top_whitelisted_collections ADD CONSTRAINT top_whitelisted_collections_pkey PRIMARY KEY (chain, audience_slug, audience_type, token_address);

ALTER TABLE ONLY public.wallet_attributes ADD CONSTRAINT wallet_attributes_pkey PRIMARY KEY (wallet);

CREATE INDEX idx_top_collections_audience_slug_audience_type_holders_count
  ON public.top_collections (audience_slug
                           , audience_type
                           , holders_count);

CREATE INDEX idx_top_collections_audience_slug_audience_type_nft_count
  ON public.top_collections (audience_slug
                           , audience_type
                           , nft_count);

CREATE INDEX idx_top_whitelisted_collections_slug_type_holders
  ON public.top_whitelisted_collections (audience_slug
                                       , audience_type
                                       , holders_count);

CREATE INDEX idx_top_whitelisted_collections_slug_type_nft_count
  ON public.top_whitelisted_collections (audience_slug
                                       , audience_type
                                       , nft_count);

CREATE INDEX ix_analytics_events_counts_event_type
  ON public.analytics_events_counts (event_type);

CREATE INDEX ix_analytics_events_counts_timestamp
  ON public.analytics_events_counts (timestamp);

CREATE INDEX ix_analytics_wallet_last_events_address
  ON public.analytics_wallet_last_events (address);

CREATE INDEX ix_analytics_wallet_last_events_last_event
  ON public.analytics_wallet_last_events (last_event);

CREATE INDEX ix_analytics_wallet_last_events_tracker_id
  ON public.analytics_wallet_last_events (tracker_id);

CREATE INDEX ix_fixed_lists_list_id
  ON public.fixed_lists (list_id);

CREATE INDEX ix_fixed_lists_wallet
  ON public.fixed_lists (wallet);

CREATE INDEX ix_fixed_lists_wallet_b
  ON public.fixed_lists (wallet_b);

CREATE INDEX ix_input_activity_metadata_address
  ON public.input_activity_metadata (address);

CREATE INDEX ix_top_collections_audience_slug
  ON public.top_collections (audience_slug);

CREATE INDEX ix_top_collections_audience_type
  ON public.top_collections (audience_type);

CREATE INDEX ix_top_collections_token_address
  ON public.top_collections (token_address);

CREATE INDEX ix_top_whitelisted_collections_audience_slug
  ON public.top_whitelisted_collections (audience_slug);

CREATE INDEX ix_top_whitelisted_collections_audience_type
  ON public.top_whitelisted_collections (audience_type);

CREATE INDEX ix_top_whitelisted_collections_token_address
  ON public.top_whitelisted_collections (token_address);

CREATE INDEX "ix_wa__column_1_ASC_wallet_b"
  ON public.wallet_attributes (created_at
                             , wallet_b);

CREATE INDEX "ix_wa__column_1_DESC_wallet_b"
  ON public.wallet_attributes (created_at DESC NULLS LAST
                             , wallet_b);

CREATE INDEX "ix_wa__column_2_ASC_wallet_b"
  ON public.wallet_attributes (nfts_count
                             , wallet_b);

CREATE INDEX "ix_wa__column_2_DESC_wallet_b"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST
                             , wallet_b);

CREATE INDEX "ix_wa__column_3_ASC_wallet_b"
  ON public.wallet_attributes (twitter_followers_count
                             , wallet_b);

CREATE INDEX "ix_wa__column_3_DESC_wallet_b"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST
                             , wallet_b);

CREATE INDEX "ix_wa__column_4_ASC_wallet_b"
  ON public.wallet_attributes (wallet_usd_cap
                             , wallet_b);

CREATE INDEX "ix_wa__column_4_DESC_wallet_b"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST
                             , wallet_b);

CREATE INDEX "ix_wa__column_5_ASC_wallet_b"
  ON public.wallet_attributes (superrank
                             , wallet_b);

CREATE INDEX "ix_wa__column_5_DESC_wallet_b"
  ON public.wallet_attributes (superrank DESC NULLS LAST
                             , wallet_b);

CREATE INDEX "ix_wa__label_10__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_10__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:defi}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_11__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:developers}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_12__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:donor}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_13__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:early_adopters}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_14__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:gaming}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_15__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:investor}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_16__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:professional}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_17__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{nft_trader}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_18__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{passive}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_19__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{zombie}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_1__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{whale}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_2__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{voter}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_3__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{influencer}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_4__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{hunter}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_5__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{nonhuman}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_6__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:art}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_7__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:fasion}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_8__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:music}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_1_ASC"
  ON public.wallet_attributes (created_at)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_1_DESC"
  ON public.wallet_attributes (created_at DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_2_ASC"
  ON public.wallet_attributes (nfts_count)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_2_DESC"
  ON public.wallet_attributes (nfts_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_3_ASC"
  ON public.wallet_attributes (twitter_followers_count)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_3_DESC"
  ON public.wallet_attributes (twitter_followers_count DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_4_ASC"
  ON public.wallet_attributes (wallet_usd_cap)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_4_DESC"
  ON public.wallet_attributes (wallet_usd_cap DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_5_ASC"
  ON public.wallet_attributes (superrank)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX "ix_wa__label_9__column_5_DESC"
  ON public.wallet_attributes (superrank DESC NULLS LAST)
  WHERE labels @> CAST('{audience:culture:luxury}' AS varchar[]);

CREATE INDEX ix_wa__search__wallet_ens_name_lower
  ON public.wallet_attributes ((lower(CAST('ens_name' AS text)))
                             , (lower(CAST('wallet' AS text))));

CREATE INDEX ix_wa__wallet
  ON public.wallet_attributes (wallet);

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x0d8775f648430679a709e98d2b0cb6250d2887ef_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x0f5d2fb29fb7d3cfee444a200298f468908cc942_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x111111111117dc0aa78b770fa6a738034120c302_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x1871464f087db27823cff66aa88599aa4815ae95_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x1a13f4ca1d028320a707d99520abfefca3998b7f_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x1f9840a85d5af5bf1d1762f925bdaddc4201f984_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x28424507fefb6f7f8e9d3860f56504e4e5f5f390_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x2b591e99afe9f32eaa6214f7b7629768c40eeb39_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x3506424f91fd33084466f402d5d97f05f8e3b4af_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x3845badade8e6dff049820680d1f14bd3903a5d0_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x4092678e4e78230f46a1534c0fbc8fa39780892b_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x4a220e6096b25eadb88358cb44068a3248254675_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x4d224452801aced8b2f0aebe155379bb5d594381_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x4dc3643dbc642b72c158e7f3d2ff232df61cb6ce_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x4e15361fd6b4bb609fa63c81a2be19d873717870_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x514910771af9ca656af840dff83e8264ecf986ca_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x60d55f02a771d515e077c9c2403a1ef324885cec_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x6982508145454ce325ddbe47a25d4ec3d2311933_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x6b175474e89094c44da98b954eedeac495271d0f_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x6b3595068778dd592e39a122f4f5a5cf09c90fe2_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x8a953cfe442c5e8855cc6c61b1293fa648bae472_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x8df3aad3a84da6b69a4da8aec3ea40d9091b2ac4_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0x92e52a1a235d9a103d970901066ce910aacefd37_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xb8c77482e45f1f44de1745f52c74426c631bdd52_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xbbbbca6a901c926f240b89eacb641d8aec7aeafd_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xc00e94cb662c3520282e6f5717214004a7f26888_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xc944e90c64b2c07662a292be6244bdf05cda44a7_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xd1d2eb1b1e90b638588728b4130137d262c87cae_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xd26114cd6ee289accf82350c8d8487fedb8a0c07_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xd533a949740bb3306d119cc777fa900ba034cd52_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xd6df932a45c0f255f85145f286ea0b292b21c90b_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xe06bd4f5aac8d0aa337d13ec88db6defc6eaeefe_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xe41d2489571d322189246dafa5ebde1f4699f498_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xe530441f4f73bdb6dc2fa5af7c3fc5fd551ec838_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xf3e014fe81267870624132ef3a646b8e83853a96_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xf4d2888d29d722226fafa5d9b24f9164c092421e_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c_pkey;

ALTER INDEX public.claimed_pkey ATTACH PARTITION public.claimed_default_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x0_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x1_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x2_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x3_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x4_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x5_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x6_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x7_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x8_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0x9_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0xa_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0xb_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0xc_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0xd_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0xe_pkey;

ALTER INDEX public.nft_holders_pkey ATTACH PARTITION public.nft_holders_0xf_pkey