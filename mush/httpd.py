__doc__="""
NAME
    httpd - lightweight HTTP file server

SYNOPSIS
    httpd(root="/www",port=80,background=False)

DESCRIPTION
    Serves files over HTTP.

EXAMPLES
    httpd()
    httpd("/www",background=True)
"""
import asyncio
import os
import mush
fsio=mush._load_internal("_fsio")
runtime=mush._load_internal("_runtime")
_MIME={
    ".html":"text/html",
    ".htm":"text/html",
    ".css":"text/css",
    ".js":"application/javascript",
    ".json":"application/json",
    ".txt":"text/plain",
    ".png":"image/png",
    ".jpg":"image/jpeg",
    ".jpeg":"image/jpeg",
}
def _mime(path):
    if "." in path:
        return _MIME.get(
            "."+path.rsplit(".",1)[1].lower(),
            "application/octet-stream",
        )
    return "application/octet-stream"
def _path(root,path):
    parts=[]
    for part in path.split("?",1)[0].split("/"):
        if part in ("","."):
            continue
        if part=="..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return root.rstrip("/")+"/"+"/".join(parts) if parts else root
def _dir(path):
    return os.stat(path)[0]&0x4000
async def _send(writer,data):
    if isinstance(data,str):
        data=data.encode()
    writer.write(data)
    await writer.drain()
async def _reply(writer,code,text,headers=None):
    await _send(
        writer,
        "HTTP/1.1 {} {}\r\n".format(
            code,
            text,
        ),
    )
    if headers:
        for key,value in headers.items():
            await _send(
                writer,
                "{}: {}\r\n".format(
                    key,
                    value,
                ),
            )
    await _send(writer,"\r\n")
async def _file(writer,path):
    await _reply(
        writer,
        200,
        "OK",
        {
            "Content-Type":_mime(path),
            "Content-Length":str(os.stat(path)[6]),
            "Connection":"close",
        },
    )
    for chunk in fsio["read_chunks"](path):
        writer.write(chunk)
        await writer.drain()
async def _list(writer,path,url):
    body="<html><body><h1>Index of {}</h1><ul>".format(url)
    for name in sorted(os.listdir(path)):
        body+='<li><a href="{}">{}</a></li>'.format(
            name,
            name,
        )
    body+="</ul></body></html>"
    await _reply(
        writer,
        200,
        "OK",
        {
            "Content-Type":"text/html",
            "Content-Length":str(len(body)),
        },
    )
    await _send(writer,body)
async def _handle(reader,writer,root):
    try:
        line=await reader.readline()
        if not line:
            return
        try:
            method,path,_=line.decode().split()
        except Exception:
            await _reply(writer,400,"Bad Request")
            return
        while True:
            line=await reader.readline()
            if line in (b"",b"\r\n"):
                break
        if method!="GET":
            await _reply(writer,405,"Method Not Allowed")
            return
        path=_path(root,path)
        try:
            is_dir=_dir(path)
        except Exception:
            await _reply(writer,404,"Not Found")
            return
        if is_dir:
            if not path.endswith("/"):
                await _reply(
                    writer,
                    301,
                    "Moved Permanently",
                    {
                        "Location":path+"/",
                    },
                )
                return
            index=path.rstrip("/")+"/index.html"
            try:
                if not _dir(index):
                    await _file(writer,index)
                    return
            except Exception:
                pass
            await _list(writer,path,path)
        else:
            await _file(writer,path)
    except Exception as e:
        print("httpd:",e)
    finally:
        try:
            writer.close()
        except Exception:
            pass
async def serve(root,port):
    async def client(reader,writer):
        await _handle(reader,writer,root)
    await asyncio.start_server(
        client,
        "0.0.0.0",
        port,
    )
    print(
        "httpd: serving {} on port {}".format(
            root,
            port,
        )
    )
    while True:
        await asyncio.sleep(3600)
async def _serve_task(root,port):
    try:
        await serve(root,port)
    finally:
        runtime["unregister"]("httpd")
def main(root="/www",port=80,background=False):
    if background:
        task=asyncio.create_task(
            _serve_task(
                root,
                port,
            )
        )
        runtime["register"](
            "httpd",
            task,
        )
        return
    asyncio.run(
        serve(
            root,
            port,
        )
    )
