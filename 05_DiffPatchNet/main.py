import asyncio
import cowsay

clients = {}
cow2code = {}
code2cow = {}


def get_free_cows(registered):
    return list(set(cowsay.list_cows()) - set(registered))


async def chat(reader, writer):
    peername = writer.get_extra_info('peername')
    me = f"{peername[0]}:{peername[1]}"
    clients[me] = asyncio.Queue()

    send_task = asyncio.create_task(reader.readline())
    receive_task = asyncio.create_task(clients[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send_task, receive_task], return_when=asyncio.FIRST_COMPLETED
        )

        for task in done:
            if task is send_task:
                send_task = asyncio.create_task(reader.readline())
                msg = task.result().decode().strip()
                await handle_message(me, msg)

            elif task is receive_task:
                receive_task = asyncio.create_task(clients[me].get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()

    send_task.cancel()
    receive_task.cancel()
    print(f"{me} DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def handle_message(sender, message):
    if message == "who":
        await clients[sender].put(list(cow2code.keys()))
    elif message == "cows":
        await clients[sender].put(get_free_cows(cow2code.keys()))
    elif message.startswith("login"):
        cow_name = message.split()[1]
        if cow_name in get_free_cows(cow2code.keys()):
            cow2code[cow_name] = sender
            code2cow[sender] = cow_name
    elif message.startswith("say"):
        target_cow = message.split()[1]
        if target_cow in cow2code:
            await clients[cow2code[target_cow]].put(
                cowsay.cowsay(message.split()[2], cow=code2cow[sender])
            )
    elif message.startswith("yield"):
        for addr in code2cow:
            if addr != sender:
                await clients[addr].put(
                    cowsay.cowsay(message.split()[1], cow=code2cow[sender])
                )
    elif message.startswith("quit"):
        cow2code.pop(code2cow[sender], None)
        code2cow.pop(sender, None)


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
