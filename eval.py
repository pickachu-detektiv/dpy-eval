@bot.command(name="eval")
@commands.is_owner()
async def eval_fn(ctx, *, code):
    language_specifiers = ["python", "py", "javascript", "js", "html", "css", "php", "md", "markdown", "go", "golang", "c", "c++", "cpp", "c#", "cs", "csharp", "java", "ruby", "rb", "coffee-script", "coffeescript", "coffee", "bash", "shell", "sh", "json", "http", "pascal", "perl", "rust", "sql", "swift", "vim", "xml", "yaml"]
    loops = 0
    while code.startswith("`"):
        code = "".join(list(code)[1:])
        loops += 1
        if loops == 3:
            loops = 0
            break
    for language_specifier in language_specifiers:
        if code.startswith(language_specifier):
            code = code.lstrip(language_specifier)
    while code.endswith("`"):
        code = "".join(list(code)[0:-1])
        loops += 1
        if loops == 3:
            break
    code = "\n".join(f"    {i}" for i in code.splitlines()) #Adds an extra layer of indentation
    code = f"async def eval_expr():\n{code}" #Wraps the code inside an async function
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
        "_guild": ctx.guild,
        "_me": ctx.me
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
