#!/usr/bin/env python3
# encoding: utf-8

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__all__ = ["main"]
__doc__ = "\t\t🌍🚢 python 反向代理服务 🕷️🕸️"


def main():
    from argparse import ArgumentParser, RawTextHelpFormatter

    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-H", "--host", default="0.0.0.0", help="ip 或 hostname，默认值：'0.0.0.0'")
    parser.add_argument("-P", "--port", type=int, help="端口号，如果不提供，则自动确定")
    parser.add_argument("-b", "--base-url", default="http://localhost", help="被代理的服务的 base_url，默认值：'http://localhost'")
    parser.add_argument("-d", "--debug", action="store_true", help="启用 debug 模式（会输出更详细的信息）")
    parser.add_argument("-v", "--version", action="store_true", help="输出版本号")

    args = parser.parse_args()
    if args.version:
        from reverse_proxy import __version__
        print(".".join(map(str, __version__)))
        return

    from reverse_proxy import make_application

    app = make_application(base_url=args.base_url)

    from uvicorn import run

    debug = args.debug
    if debug:
        getattr(app, "logger").level = 10
        app.show_error_details = True
    run(
        app, 
        host=args.host, 
        port=args.port, 
        reload=debug, 
        proxy_headers=True, 
        forwarded_allow_ips="*", 
        timeout_graceful_shutdown=1, 
    )


if __name__ == "__main__":
    from pathlib import Path
    from sys import path

    path[0] = str(Path(__file__).parents[1])
    main()

