CREATE TABLE card_trader_products(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
    ,expansion_id BIGINT NOT NULL
    ,expansion_name TEXT NOT NULL
    ,blueprint_id TEXT NOT NULL
    ,product_id BIGINT NOT NULL
    ,product_name TEXT NOT NULL
    ,product_quantity INTEGER NOT NULL
    ,product_price_cents INTEGER NOT NULL
    ,product_currency TEXT NOT NULL
    ,product_description TEXT
    ,user_id BIGINT NOT NULL
    ,user_name TEXT NOT NULL
    ,user_country TEXT NOT NULL
    ,insert_timestamp TIMESTAMPTZ NOT NULL
    
    --,PRIMARY KEY (product_id)
);
