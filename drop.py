@bot.command()

async def drop(ctx, param1: str = None, param2: str = None):

    if param1 is None or param2 is None:
        await ctx.send("**<:emoji_29:1249468115650088961> Parâmetro faltando!**\n> Use `Adrop [tipo] [quantidade]` (o tipo pode ser `Bronze`, `Prata`, `Ouro`, `Platina`, `Diamante`, `Esmeralda` ou `Safira`, e a quantidade deve ser um número maior que zero).")
        return

    if param2.isdigit():
        quantidade = int(param2)
        tipo = param1
    else:
        await ctx.send("**<:emoji_29:1249468115650088961> Parâmetro faltando ou inválido!**\n> Use `Adrop [tipo] [quantidade]` (o tipo pode ser `Bronze`, `Prata`, `Ouro`, `Platina`, `Diamante`, `Esmeralda` ou `Safira`, e a quantidade deve ser um número maior que zero).")
        return

    if quantidade <= 0:
        await ctx.send("**Quantidade inválida!**\n> A quantidade deve ser um número maior que zero.")
        return

    tipo = tipo.capitalize()

    if tipo not in ["Bronze", "Prata", "Ouro", "Platina", "Diamante", "Esmeralda", "Safira"]:
        await ctx.send("**Tipo de caixa inválido!**\n> Use `Bronze`, `Prata`, `Ouro`, `Platina`, `Diamante`, `Esmeralda` ou `Safira`.")
        return

    if quantidade > 3:
        await ctx.send("**<:emoji_5:1247758441595015241> Limite máximo de 3 caixas por drop!**")
        return

    drop_message = await ctx.send(f"# <:emoji_29:1249468047899492412> {quantidade} caixa(s) de {tipo} foi(ram) dropada(s) no chat! Aperte o botão abaixo para pegar o(s) drop(s).")

    async def claim_drop(interaction: discord.Interaction):
        rewards = {
            "Bronze": (1000, 5000),
            "Prata": (5000, 10000),
            "Ouro": (10000, 20000),
            "Platina": (20000, 50000),
            "Diamante": (50000, 100000),
            "Esmeralda": (100000, 200000),
            "Safira": (200000, 500000)
        }

        total_reward = 0
        user_id = str(interaction.user.id)
        
        data = load_data()

        for _ in range(quantidade):
            min_reward, max_reward = rewards[tipo]
            reward = random.randint(min_reward, max_reward)
            total_reward += reward
            data["balances"][user_id] = data.get("balances", {}).get(user_id, 0) + reward

        save_data(data)

        await interaction.response.send_message(f"Parabéns! Você pegou o(s) drop(s) de {tipo} e ganhou um total de **{total_reward:,} Lunaris** 🪙.", ephemeral=True)
        await drop_message.delete()

    button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Resgatar Recompensa(s)", custom_id="claim_drop", emoji="🎁")
    button.callback = claim_drop

    view = discord.ui.View()
    view.add_item(button)

    await drop_message.edit(view=view)