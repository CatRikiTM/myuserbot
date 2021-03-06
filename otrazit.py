async def make(client, message, o):
    reply = message.reply_to_message
    if reply.photo or reply.sticker:
        if reply.photo:
            downloads = await client.download_media(reply.photo.file_id)
        else:
            downloads = await client.download_media(reply.sticker.file_id)
        path = f"{downloads}"
        img = Image.open(path)
        await message.delete()
        w, h = img.size
        if o in [1, 2]:
            if o == 2:
                img = ImageOps.mirror(img)
            part = img.crop([0, 0, w // 2, h])
            img = ImageOps.mirror(img)
        else:
            if o == 4:
                img = ImageOps.flip(img)
            part = img.crop([0, 0, w, h // 2])
            img = ImageOps.flip(img)
        img.paste(part, (0, 0))
        img.save(path)
        if reply.photo:
            return await reply.reply_photo(photo=path)
        elif reply.sticker:
            return await reply.reply_sticker(sticker=path)
        os.remove(path)

    return await message.edit("<b>Реплай на фото.</b>")

@app.on_message(filters.command(["отразить1", "отразить2", "отразить3", "отразить4"], prefixes="."))
async def mirror_flip(client: Client, message: Message):
    await message.edit("<b>Processing...</b>")
    param = {"отразить1": 1, "отразить2": 2, "отразить3": 3, "отразить4": 4}[message.command[0]]
    await make(client, message, param)
