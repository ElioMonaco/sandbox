-- CREATE EXTENSION IF NOT EXISTS pg_cron;

-- SELECT cron.schedule(
--   'recluster-orders',
--   '0 3 * * *', 
--   'CLUSTER orders USING idx_orders_created_at'
-- );