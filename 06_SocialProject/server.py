import asyncio
import cowsay

clients = {}
cow_to_client = {}
client_to_cow = {}


def get_available_cows(registered_cows):
    return list(set(cowsay.list_cows()) - set(registered_cows))


async def chat_handler(reader, writer):
    peername = writer.get_extra_info('peername')
    client_id = f"{peername[0]}:{peername[1]}"
    clients[client_id] = asyncio.Queue()

    send_task = asyncio.create_task(reader.readline())
    receive_task = asyncio.create_task(clients[client_id].get())

    while not reader.at_eof():
        done, _ = await asyncio.wait(
            [send_task, receive_task], return_when=asyncio.FIRST_COMPLETED
        )

        for task in done:
            if task is send_task:
                send_task = asyncio.create_task(reader.readline())
                msg = task.result().decode().strip()
                await handle_message(client_id, msg)
            elif task is receive_task:
                receive_task = asyncio.create_task(clients[client_id].get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()

    send_task.cancel()
    receive_task.cancel()
    print(f"{client_id} DONE")
    del clients[client_id]
    writer.close()
    await writer.wait_closed()


async def handle_message(sender, message):
    if message == "who":
        await clients[sender].put(list(cow_to_client.keys()))
    elif message == "cows":
        await clients[sender].put(get_available_cows(cow_to_client.keys()))
    elif message == "compl@who":
        await clients[sender].put("compl@" + str(list(cow_to_client.keys())))
    elif message == "compl@cows":
        await clients[sender].put("compl@" + str(get_available_cows(cow_to_client.keys())))
    elif message.startswith("login"):
        cow_name = message.split()[1]
        if cow_name in get_available_cows(cow_to_client.keys()):
            cow_to_client[cow_name] = sender
            client_to_cow[sender] = cow_name
    elif message.startswith("say"):
        target_cow = message.split()[1]
        if target_cow in cow_to_client:
            await clients[cow_to_client[target_cow]].put(
                cowsay.cowsay(message.split()[2], cow=client_to_cow[sender])
            )
    elif message.startswith("yield"):
        for addr in client_to_cow:
            if addr != sender:
                await clients[addr].put(
                    cowsay.cowsay(message.split()[1], cow=client_to_cow[sender])
                )
    elif message.startswith("quit"):
        cow_to_client.pop(client_to_cow[sender], None)
        client_to_cow.pop(sender, None)


async def main():
    server = await asyncio.start_server(chat_handler, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
