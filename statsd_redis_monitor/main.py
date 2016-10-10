#!/usr/bin/env python
import argparse
import redis
import statsd
import logging
import logging.config


logging_config = {
    'version': 1,
    'formatters': {
        'cli': {
            'format': '%(asctime)s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'cli',
            'level': logging.DEBUG,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': logging.INFO,
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


def get_redis_info(host, port=6379, db=0, password=None):
    r = redis.StrictRedis(host=host, port=port, db=db, password=password)
    rawinfo = r.info()
    return {
        'connected_clients': rawinfo.get('connected_clients'),
        'connected_slaves': rawinfo.get('connected_slaves'),
        'db%s.keys' % db: rawinfo.get('db%s' % db, {}).get('keys'),
        'db%s.expires' % db: rawinfo.get('db%s' % db, {}).get('expires'),
        'db%s.avg_ttl' % db: rawinfo.get('db%s' % db, {}).get('avg_ttl'),
        'evicted_keys': rawinfo.get('evicted_keys'),
        'expired_keys': rawinfo.get('expired_keys'),
        'instantaneous_input_kbps': rawinfo.get('instantaneous_input_kbps'),
        'instantaneous_ops_per_sec': rawinfo.get('instantaneous_ops_per_sec'),
        'instantaneous_output_kbps': rawinfo.get('instantaneous_output_kbps'),
        'keyspace_hits': rawinfo.get('keyspace_hits'),
        'keyspace_misses': rawinfo.get('keyspace_misses'),
        'latest_fork_usec': rawinfo.get('latest_fork_usec'),
        'lru_clock': rawinfo.get('lru_clock'),
        'master_repl_offset': rawinfo.get('master_repl_offset'),
        'migrate_cached_sockets': rawinfo.get('migrate_cached_sockets'),
        'pubsub_channels': rawinfo.get('pubsub_channels'),
        'pubsub_patterns': rawinfo.get('pubsub_patterns'),
        'rdb_changes_since_last_save': rawinfo.get('rdb_changes_since_last_save'),
        'rdb_last_bgsave_time_sec': rawinfo.get('rdb_last_bgsave_time_sec'),
        'rejected_connections': rawinfo.get('rejected_connections'),
        'repl_backlog_active': rawinfo.get('repl_backlog_active'),
        'repl_backlog_first_byte_offset': rawinfo.get('repl_backlog_first_byte_offset'),
        'repl_backlog_histlen': rawinfo.get('repl_backlog_histlen'),
        'repl_backlog_size': rawinfo.get('repl_backlog_size'),
        'total_commands_processed': rawinfo.get('total_commands_processed'),
        'total_connections_received': rawinfo.get('total_connections_received'),
        'total_net_input_bytes': rawinfo.get('total_net_input_bytes'),
        'total_net_output_bytes': rawinfo.get('total_net_output_bytes'),
        'uptime_in_days': rawinfo.get('uptime_in_days'),
        'uptime_in_seconds': rawinfo.get('uptime_in_seconds'),
        'used_cpu_sys': rawinfo.get('used_cpu_sys'),
        'used_cpu_sys_children': rawinfo.get('used_cpu_sys_children'),
        'used_cpu_user': rawinfo.get('used_cpu_user'),
        'used_cpu_user_children': rawinfo.get('used_cpu_user_children'),
        'used_memory': rawinfo.get('used_memory'),
        'used_memory_lua': rawinfo.get('used_memory_lua'),
        'used_memory_peak': rawinfo.get('used_memory_peak'),
        'used_memory_rss': rawinfo.get('used_memory_rss'),
    }


def report_redis_info(statsd_host, statsd_port, statsd_prefix, info):
    c = statsd.StatsClient(statsd_host, statsd_port)
    for key, value in info.items():
        full_key = '%s.%s' % (statsd_prefix, key)
        logger.debug('%s => %s' % (full_key, value))
        c.gauge(full_key, value)



def main(redis_host, redis_port, redis_db, redis_password, statsd_host, statsd_port, statsd_prefix):
    info = get_redis_info(redis_host, redis_port, redis_db, redis_password)
    report_redis_info(statsd_host, statsd_port, statsd_prefix, info)
    logger.info("Updated stats for %s:%s:%s" % (redis_host, redis_port, redis_db))



def handle_lambda(event, context):
    for config in event.get('configs', []):
        main(redis_host=config['redis_host'],
             redis_port=config.get('redis_port', 6379),
             redis_db=config.get('redis_db', 0),
             redis_password=config.get('redis_password', None),
             statsd_host=config['statsd_host'],
             statsd_port=config.get('statsd_port', 8125),
             statsd_prefix=config.get('statsd_prefix', 'redis'))
    logger.info('Done')
    return {
        'message' : 'Updated Metrics'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Backup a pypi-server instance to Amazon S3')
    parser.add_argument('--redis-host', type=str, required=True)
    parser.add_argument('--redis-port', type=int, required=False, default=6379)
    parser.add_argument('--redis-db', type=int, required=False, default=0)
    parser.add_argument('--redis-password', type=str, required=False, default=None)
    parser.add_argument('--statsd-host', type=str, required=True)
    parser.add_argument('--statsd-port', type=int, required=False, default=8125)
    parser.add_argument('--statsd-prefix', type=str, required=False, default='redis')
    args = parser.parse_args()
    main(redis_host=args.redis_host,
         redis_port=args.redis_port,
         redis_db=args.redis_db,
         redis_password=args.redis_password,
         statsd_host=args.statsd_host,
         statsd_port=args.statsd_port,
         statsd_prefix=args.statsd_prefix)
