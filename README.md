# StatsD Redis Monitor

This is a simple Pythonapplication for monitoring statistics about 1-*N* Redis installations, using AWS Lambda and StatsD.

## Running on AWS Lambda

1. Run `./bin/build-lambda-pkg.sh` to create a lambda deployment package.
2. Upload The resulting Zip file (in `dist/`) to AWS lambda as a CloudWatch scheduled job. For more information on how to do this, reference the [Lambda Canary tutorial](https://docs.aws.amazon.com/lambda/latest/dg/with-scheduledevents-example.html).
3. Configure the CloudWatch trigger event to send JSON event data to the Lambda function. The JSON structure should look like this.

```
{
    "configs": [
        {
            "redis_host": "project-a.redis.foobar.com",
            "redis_port": 6379,
            "redis_db": 0,
            "redis_password": "baz",
            "statsd_host": "statsd.foobar.com",
            "statsd_port": 8125,
            "statsd_prefix": "redis.project-a"
        },
        {
            "redis_host": "project-b.redis.foobar.com",
            "redis_port": 6379,
            "redis_db": 0,
            "redis_password": "baz",
            "statsd_host": "statsd.foobar.com",
            "statsd_port": 8125,
            "statsd_prefix": "redis.project-b"
        }
    ]
}
```

Each time the Lambda function is triggered, it loops through each configuration block in the `configs` list, runs the `INFO` command on the Redis server, and sends data to the StatsD server. Each key sent to StatsD is prefixed with the given prefix string. This allows for common features like grouping redis data with a global top-level key or sending an API key with each statistic (required for services like [HostedGraphite](https://www.hostedgraphite.com/)).

The following statistics are extracted and sent to StatsD:

- `connected_clients`
- `connected_slaves`
- `db([0-9]+).keys`
- `db([0-9]+).expires`
- `db([0-9]+).avg_ttl`
- `evicted_keys`
- `expired_keys`
- `instantaneous_input_kbps`
- `instantaneous_ops_per_sec`
- `instantaneous_output_kbps`
- `keyspace_hits`
- `keyspace_misses`
- `latest_fork_usec`
- `lru_clock`
- `master_repl_offset`
- `migrate_cached_sockets`
- `pubsub_channels`
- `pubsub_patterns`
- `rdb_changes_since_last_save`
- `rdb_last_bgsave_time_sec`
- `rejected_connections`
- `repl_backlog_active`
- `repl_backlog_first_byte_offset`
- `repl_backlog_histlen`
- `repl_backlog_size`
- `total_commands_processed`
- `total_connections_received`
- `total_net_input_bytes`
- `total_net_output_bytes`
- `uptime_in_days`
- `uptime_in_seconds`
- `used_cpu_sys`
- `used_cpu_sys_children`
- `used_cpu_user`
- `used_cpu_user_children`
- `used_memory`
- `used_memory_lua`
- `used_memory_peak`
- `used_memory_rss`
