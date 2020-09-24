import argparse
import crawler
import logging


parser = argparse.ArgumentParser()

parser.add_argument('crawler_name', type=str, help="Specify the crawler name.")
parser.add_argument('input_file', type=str,
                    help='Input file path in which the data is the seeds for crawler.')
parser.add_argument('output_file', type=str,
                    help='Output file path where the data crawler from the web save.')
parser.add_argument('--input_format', type=str, default="xlsx",
                    help='The format suffix of "input_file".')
parser.add_argument('--output_format', type=str, default="xlsx",
                    help='The format suffix of "output_file"')
parser.add_argument('--resume', action='store_true', default=False,
                    help='Whether resume from the latest checkpoints or not.')
parser.add_argument('--src_column', type=int, default=0,
                    help="The column of source language seeds.")
parser.add_argument('--tgt_column', type=int, default=1,
                    help="The column of target language seeds.")
parser.add_argument('--src_lang', type=int, default=0,
                    help="Determine which language the source seeds are.")
parser.add_argument('--tgt_lang', type=int, default=1,
                    help="Determine which language the target seeds are.")
parser.add_argument('--skip_first_row', type=bool, default=True,
                    help="Whether skip first row of files.")

args = parser.parse_args()

crawler_class_name = args.crawler_name + "Crawler"
try:
    Crawler = getattr(crawler, crawler_class_name)
except AttributeError as e:
    raise AttributeError("Crawler {} don't exist.".format(crawler_class_name))

if args.input_format == "xlsx":
    logging.log(logging.INFO, "Reading data from {}.".format(args.input_format))
    spider = Crawler.from_excel(args.input_file,
                                src_column=args.src_column,
                                tgt_column=args.tgt_column,
                                skip_first_row=args.skip_first_row,
                                src_lang=args.src_lang,
                                tgt_lang=args.tgt_lang)
else:
    raise AttributeError(
        "The input format {} is not supported.".format(args.input_format))

logging.log(logging.INFO, "Crawling data from the web.")
spider.crawl()

if args.output_format == "xlsx":
    logging.log(logging.INFO, "Saving data to {}.".format(args.output_file))
    spider.save_as_xlsx(args.output_file)
else:
    raise AttributeError(
        "The output format {} is not supported.".format(args.output_file))
