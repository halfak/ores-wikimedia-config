#!/usr/bin/env python3
"""
Run a celery worker node.

:Usage:
    ores_celery.py -h | --help
    ores_celery.py [--config=<path>]...

:Options:
    -h --help        Prints this documentation
    --config=<path>  The path to a yaml config directory
                     [default: config]
"""
import docopt
import glob
import logging
import logging.config

import yamlconf

from ores.score_processors import Celery

args = docopt.docopt(__doc__)
yamls = []
for path in args['--config']:
    path = "{}/*.yaml".format(path)
    yamls += [open(p) for p in sorted(glob.glob(path))]
config = yamlconf.load(*yamls)

with open("logging_config.yaml") as f:
    logging_config = yamlconf.load(f)
    logging.config.dictConfig(logging_config)

if 'data_paths' in config['ores'] and \
    'nltk' in config['ores']['data_paths']:
    import nltk
    nltk.data.path.append(config['ores']['data_paths']['nltk'])

score_processor = Celery.from_config(config, config['ores']['score_processor'])
application = score_processor.application

if __name__ == '__main__':
    logging.getLogger('ores').setLevel(logging.DEBUG)
    application.worker_main(argv=["celery_worker", "--loglevel=INFO"])
