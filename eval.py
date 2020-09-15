@commands.command(name="eval")
@commands.is_owner()
async def eval_fn(ctx, *, code):
    code.strip("` ")
    code = "\n".join(f"    {i}" for i in code.splitlines()) #Adds an extra layer of indentation
    code = f"async def eval_expr():\n{code}" #wraps the code inside an async function
    def send(text): #Function for sending message to discord if code has any usage of print function
        bot.loop.create_task(ctx.send(text))
    env = {
        "bot": bot,
        "client": bot,
        "ctx": ctx,
        "print": send,
        "_author": ctx.author,
        "_message": ctx.message,
        "_channel": ctx.channel,
        "_guild": ctx.guild
    }
    env.update(globals())
    try:
        exec(code, env)
        eval_expr = env["eval_expr"]
        result = await eval_expr()
        if result:
            await ctx.send(result)
    except:
        await ctx.send(f"```{traceback.format_exc()}```")